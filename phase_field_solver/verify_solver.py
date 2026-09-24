#!/usr/bin/env python3
"""Independent exact limits, variational derivatives, dynamics, and restart tests."""
import argparse
from dataclasses import asdict, replace
import json
from pathlib import Path
import tempfile
import time
import unittest

import numpy as np
from scipy.linalg import eigh
from scipy.special import ellipj

import phasefield as pf

METRICS = {}


def record(name, value):
    METRICS[name] = pf.exact_float(value)


def resolution(k=2, points=32, kz=None):
    return pf.Resolution(k, k if kz is None else kz, points, points)


def config_for(op):
    return pf.normalize_config({"model": asdict(op.model), "resolution": asdict(op.resolution)})


def complex_reference(model, k, points=64):
    """Independent complex Fourier weak assembly using FFT coefficient integrals."""
    t,z=np.meshgrid(2*np.pi*np.arange(points)/points,
                    2*np.pi*np.arange(points)/points,indexing="ij")
    g=pf.geometry(model,t,z)
    modes=np.array([(a,b) for a in range(-k,k+1) for b in range(-k,k+1)])
    diff=(modes[:,None,:]-modes[None,:,:]) % points
    def mat(x):
        fft=np.fft.fft2(x)/(points*points)
        return fft[diff[:,:,0],diff[:,:,1]]
    l,p=modes[:,0],modes[:,1]
    w=g["area"]*g["N"]
    M=mat(g["area"]/g["N"])
    K=l[:,None]*l[None,:]*mat(w*g["itt"])
    K=K+(l[:,None]*p[None,:]+p[:,None]*l[None,:])*mat(w*g["itz"])
    K=K+p[:,None]*p[None,:]*mat(w*g["izz"])+mat(w*g["mass2"])
    return eigh(K,M,eigvals_only=True)


class Verification(unittest.TestCase):
    def test_01_flat_geometry(self):
        m=pf.Model(amplitude=0,radius=2,axial_scale=3)
        t,z=np.meshgrid(np.linspace(0,6,17),np.linspace(0,6,19),indexing="ij")
        g=pf.geometry(m,t,z)
        self.assertTrue(np.all(g["det"]==36))
        self.assertTrue(np.all(g["H"]==0.25))
        self.assertTrue(np.all(g["KG"]==0))
        self.assertTrue(np.all(g["itz"]==0))

    def test_02_curvature_against_embedding(self):
        m=pf.Model(amplitude=0.17,n=3,m=2)
        t,z=np.meshgrid(np.arange(11)*0.43,np.arange(13)*0.37,indexing="ij")
        g=pf.geometry(m,t,z)
        er=np.stack([np.cos(t),np.sin(t),np.zeros_like(t)],axis=-1)
        et=np.stack([-np.sin(t),np.cos(t),np.zeros_like(t)],axis=-1)
        ez=np.zeros_like(er);ez[...,2]=1
        xt=g["Rt"][...,None]*er+g["R"][...,None]*et
        xz=g["Rz"][...,None]*er+m.axial_scale*ez
        normal=np.cross(xt,xz);normal/=np.linalg.norm(normal,axis=-1)[...,None]
        xtt=(g["Rtt"]-g["R"])[...,None]*er+2*g["Rt"][...,None]*et
        xtz=g["Rtz"][...,None]*er+g["Rz"][...,None]*et
        xzz=g["Rzz"][...,None]*er
        for key,x in [("btt",xtt),("btz",xtz),("bzz",xzz)]:
            self.assertLess(np.max(np.abs(g[key]+np.sum(normal*x,axis=-1))),2e-14)

    def test_03_gauss_bonnet(self):
        op=pf.SurfaceSolver(pf.Model(amplitude=0.2,n=2,m=3),resolution(0,128))
        error=abs(op.cell_weight*np.dot(op.geom["area"],op.geom["KG"]))
        record("gauss_bonnet_absolute_residual",error)
        self.assertLess(error,1e-11)
        self.assertGreaterEqual(np.min(op.geom["H"]**2-op.geom["KG"]),-1e-14)

    def test_04_flat_spectrum(self):
        op=pf.SurfaceSolver(pf.Model(amplitude=0,quartic=0),resolution(2))
        actual=op.spectrum(op.ndof).values
        expected=np.sort([l*l+p*p/2.25+0.25 for l in range(-2,3) for p in range(-2,3)])
        error=np.max(np.abs(actual-expected));record("flat_spectrum_max_error",error)
        self.assertLess(error,2e-13)

    def test_05_constant_mode_curved(self):
        op=pf.SurfaceSolver(pf.Model(amplitude=0.23,mass2=0.75),resolution(3,48))
        value=op.spectrum(1).values[0]
        record("curved_constant_mode_error",abs(value-0.75))
        self.assertLess(abs(value-0.75),1e-12)

    def test_06_lapse_exact_ground(self):
        op=pf.SurfaceSolver(pf.Model(amplitude=0,lapse_amplitude=0.2,quartic=0),
                            resolution(8,128,kz=0))
        actual=op.spectrum(1).values[0]
        record("lapse_ground_error",abs(actual-6/25))
        self.assertLess(abs(actual-6/25),2e-12)
        q=op.project(op.geom["N"].reshape(op.theta.shape)**(-0.5))
        residual=op.K@q-(6/25)*(op.M@q)
        self.assertLess(op.dual_norm(residual),1e-6)

    def test_07_independent_complex_assembly(self):
        model=pf.Model(amplitude=0.12,lapse_amplitude=0.13,lapse_m=1,
                       potential_amplitude=0.07,curvature_h2=0.08,curvature_k=-0.03)
        op=pf.SurfaceSolver(model,resolution(3,64))
        error=np.max(np.abs(op.spectrum(op.ndof).values-complex_reference(model,3)))
        record("independent_complex_spectrum_error",error)
        self.assertLess(error,2e-11)

    def test_08_phase_translation_invariance(self):
        a=pf.Model(amplitude=0.15,potential_amplitude=0.06)
        b=replace(a,phase_theta=0.37,phase_zeta=-0.29,
                  potential_phase_theta=0.37,potential_phase_zeta=-0.29)
        v1=pf.SurfaceSolver(a,resolution(3,64)).spectrum(10).values
        v2=pf.SurfaceSolver(b,resolution(3,64)).spectrum(10).values
        self.assertLess(np.max(np.abs(v1-v2)),2e-12)

    def test_09_mass_shift_and_lapse_scaling(self):
        a=pf.SurfaceSolver(pf.Model(amplitude=0.11),resolution(2))
        b=pf.SurfaceSolver(replace(a.model,mass2=a.model.mass2+0.5),resolution(2))
        c=pf.SurfaceSolver(replace(a.model,lapse_scale=2),resolution(2))
        va=a.spectrum(8).values
        self.assertLess(np.max(np.abs(b.spectrum(8).values-va-0.5)),1e-12)
        self.assertLess(np.max(np.abs(c.spectrum(8).values-4*va)),1e-12)

    def test_10_eigen_residual_and_orthogonality(self):
        op=pf.SurfaceSolver(pf.Model(lapse_amplitude=0.2),resolution(3,48))
        sp=op.spectrum(20)
        record("eigen_max_scaled_residual",np.max(sp.residuals))
        self.assertLess(np.max(sp.residuals),1e-13)
        self.assertLess(sp.mass_orthogonality_error,1e-12)

    def test_11_potential_second_order(self):
        errors=[]
        for eps in [0.1,0.05,0.025]:
            op=pf.SurfaceSolver(pf.Model(amplitude=0,quartic=0,potential_amplitude=eps),
                                resolution(5,48))
            actual=op.spectrum(1).values[0]
            errors.append(abs(actual-(0.25-eps*eps/(40/9))))
        ratios=[errors[i]/errors[i+1] for i in range(2)]
        for i,x in enumerate(ratios):record(f"potential_fourth_order_remainder_ratio_{i}",x)
        self.assertTrue(all(14<x<18 for x in ratios))

    def test_12_energy_gradient(self):
        op=pf.SurfaceSolver(pf.Model(lapse_amplitude=0.17,quartic=0.8),resolution(2))
        rng=np.random.default_rng(20260924)
        q=rng.normal(size=op.ndof)*0.03
        direction=rng.normal(size=op.ndof);direction/=np.linalg.norm(direction)
        h=1e-5
        numerical=(op.potential_energy(q+h*direction)-op.potential_energy(q-h*direction))/(2*h)
        analytic=op.force(q)@direction
        self.assertLess(abs(numerical-analytic),2e-7)

    def test_13_hessian_directional_derivative(self):
        op=pf.SurfaceSolver(pf.Model(quartic=0.7),resolution(2))
        rng=np.random.default_rng(4701)
        q=rng.normal(size=op.ndof)*0.03;d=rng.normal(size=op.ndof)
        h=1e-6
        num=(op.force(q+h*d)-op.force(q-h*d))/(2*h)
        self.assertLess(np.linalg.norm(num-op.hessian(q)@d)/np.linalg.norm(num),2e-9)

    def test_14_cubic_projection_dealiasing(self):
        m=pf.Model(amplitude=0,quartic=1,mass2=0)
        a=pf.SurfaceSolver(m,resolution(3,13))
        b=pf.SurfaceSolver(m,resolution(3,64))
        rng=np.random.default_rng(552)
        q=rng.normal(size=a.ndof)*0.05
        self.assertLess(np.max(np.abs(a.force(q)-b.force(q))),2e-12)

    def test_15_full_field_duffing(self):
        op=pf.SurfaceSolver(pf.Model(amplitude=0.1,mass2=1.25,quartic=0.75),
                            resolution(1,32))
        T=2.0;A=0.5;om=np.sqrt(1.25+0.75*A*A);parameter=3/46
        exact=A*ellipj(om*T,parameter)[1]
        errors=[]
        for steps in [100,200,400]:
            state=pf.initial_state(op,op.project(A),dt=T/steps)
            pf.integrate(op,state,steps,sample_every=steps)
            errors.append(np.max(np.abs(op.field(state.q)-exact)))
        ratios=[errors[i]/errors[i+1] for i in range(2)]
        for i,x in enumerate(ratios):record(f"duffing_field_error_ratio_{i}",x)
        self.assertTrue(all(3.8<x<4.2 for x in ratios))

    def test_16_corrugated_nonlinear_energy_order(self):
        op=pf.SurfaceSolver(pf.Model(quartic=0.8,lapse_amplitude=0.15),resolution(2))
        q=op.project(0.2*np.cos(op.theta)*np.cos(op.zeta)+0.03)
        errors=[]
        for steps in [50,100,200]:
            state=pf.initial_state(op,q,dt=1/steps)
            hist=pf.integrate(op,state,steps,sample_every=1)
            errors.append(max(abs(x["balance_defect"]) for x in hist["samples"]))
        for i in range(2):record(f"nonlinear_energy_error_ratio_{i}",errors[i]/errors[i+1])
        self.assertTrue(all(3.6<errors[i]/errors[i+1]<4.4 for i in range(2)))

    def test_17_manufactured_nonlinear_forcing(self):
        op=pf.SurfaceSolver(pf.Model(amplitude=0,quartic=0.6,mass2=0.3),resolution(3))
        profile=0.1*np.cos(op.theta)*np.cos(op.zeta);omega=1.3
        k2=1+1/2.25
        def drive(t):
            phi=profile*np.cos(omega*t)
            return op.weak_source((k2+0.3-omega**2)*phi+0.6*phi**3)
        errors=[]
        for steps in [40,80,160]:
            state=pf.initial_state(op,op.project(profile),dt=1/steps)
            pf.integrate(op,state,steps,drive=drive,sample_every=steps)
            errors.append(np.max(np.abs(op.field(state.q)-profile*np.cos(omega))))
        self.assertTrue(all(3.5<errors[i]/errors[i+1]<4.5 for i in range(2)))
        record("manufactured_finest_max_field_error",errors[-1])

    def test_18_exact_damping_loss(self):
        op=pf.SurfaceSolver(pf.Model(amplitude=0,mass2=0,quartic=0),resolution(0,16))
        state=pf.initial_state(op,op.project(0.2),op.project(0.3),dt=0.01)
        hist=pf.integrate(op,state,100,damping=0.7,sample_every=1)
        self.assertLess(abs(state.velocity[0]-0.3*np.exp(-0.7)),2e-14)
        error=max(abs(x["balance_defect"]) for x in hist["samples"])
        record("damping_balance_absolute_error",error)
        self.assertLess(error,2e-13)

    def test_19_negative_mode_is_retained(self):
        op=pf.SurfaceSolver(pf.Model(amplitude=0,mass2=-1,quartic=0),resolution(0,16))
        self.assertEqual(op.spectrum(1).report()["classification"][0],"negative")
        state=pf.initial_state(op,op.project(0.1),dt=0.005)
        pf.integrate(op,state,200,sample_every=200)
        self.assertLess(abs(state.q[0]-0.1*np.cosh(1)),2e-6)

    def test_20_broken_vacuum_equilibrium(self):
        op=pf.SurfaceSolver(pf.Model(amplitude=0.1,mass2=-1,quartic=1),resolution(2))
        result=pf.equilibrium(op,op.project(0.6))
        self.assertTrue(result["converged"])
        self.assertLess(np.max(np.abs(op.field(result["q"])-1)),2e-9)
        self.assertAlmostEqual(result["hessian_spectrum"].values[0],2,places=8)
        record("broken_vacuum_dual_residual",result["residual"])

    def test_21_zero_stationary_is_classified_unstable(self):
        op=pf.SurfaceSolver(pf.Model(mass2=-1,quartic=1),resolution(1))
        result=pf.equilibrium(op,np.zeros(op.ndof))
        self.assertTrue(result["converged"])
        self.assertEqual(result["stationary_classification"],"negative")

    def test_22_nonuniform_equilibrium(self):
        op=pf.SurfaceSolver(pf.Model(mass2=-0.5,quartic=1,potential_amplitude=0.2),
                            resolution(3,48))
        result=pf.equilibrium(op,op.project(0.7))
        self.assertTrue(result["converged"],result["reason"])
        self.assertLess(result["residual"],result["tolerance"]*1.01)
        self.assertEqual(result["stationary_classification"],"positive")
        self.assertGreater(np.ptp(op.field(result["q"])),0.01)
        record("nonuniform_equilibrium_dual_residual",result["residual"])

    def test_23_restart_exact_same_environment(self):
        op=pf.SurfaceSolver(pf.Model(quartic=0.4),resolution(1))
        config=config_for(op)
        config["drive"]["amplitude"]=0.02;config["damping"]=0.03
        drive=pf.configured_drive(op,config)
        q=op.project(0.1*np.cos(op.theta)*np.cos(op.zeta))
        a=pf.initial_state(op,q,dt=0.01);b=pf.initial_state(op,q,dt=0.01)
        pf.integrate(op,a,80,drive=drive,damping=0.03)
        pf.integrate(op,b,37,drive=drive,damping=0.03)
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"checkpoint.npz"
            pf.save_checkpoint(path,op,b,config)
            op2,b2,c2=pf.load_checkpoint(path)
            pf.integrate(op2,b2,43,drive=pf.configured_drive(op2,c2),damping=0.03)
        self.assertTrue(np.array_equal(a.q,b2.q))
        self.assertTrue(np.array_equal(a.velocity,b2.velocity))
        self.assertEqual(a.work,b2.work);self.assertEqual(a.dissipated,b2.dissipated)

    def test_24_checkpoint_tamper_rejected(self):
        op=pf.SurfaceSolver(pf.Model(),resolution(1))
        state=pf.initial_state(op,np.zeros(op.ndof))
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"checkpoint.npz"
            pf.save_checkpoint(path,op,state,config_for(op))
            with np.load(path,allow_pickle=False) as archive:
                arrays={key:archive[key].copy() for key in archive.files}
            arrays["q"][0]+=1
            pf.atomic_npz(path,**arrays)
            with self.assertRaises(pf.SolverError):pf.load_checkpoint(path)

    def test_25_checkpoint_wrong_operator_rejected(self):
        op=pf.SurfaceSolver(pf.Model(),resolution(1))
        other=pf.SurfaceSolver(replace(op.model,mass2=1),resolution(1))
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"checkpoint.npz"
            pf.save_checkpoint(path,op,pf.initial_state(op,np.zeros(op.ndof)),config_for(op))
            with self.assertRaises(pf.SolverError):pf.load_checkpoint(path,other)

    def test_26_bad_geometry_and_nonfinite_rejected(self):
        for kwargs in [dict(radius=0.1,amplitude=0.1),dict(lapse_amplitude=1),
                       dict(quartic=-1),dict(mass2=float("nan")),dict(n=True)]:
            with self.assertRaises(pf.SolverError):pf.Model(**kwargs)
        with self.assertRaises(pf.SolverError):pf.SurfaceSolver(
            pf.Model(),pf.Resolution(3,3,12,16))
        with self.assertRaises(pf.SolverError):pf.normalize_config({"mode1":{}})

    def test_27_timestep_guard_preserves_state(self):
        op=pf.SurfaceSolver(pf.Model(amplitude=0,quartic=0),resolution(2))
        state=pf.initial_state(op,np.ones(op.ndof)*0.01,dt=10)
        q=state.q.copy()
        with self.assertRaises(pf.SolverError):pf.integrate(op,state,1)
        self.assertEqual(state.step,0);self.assertTrue(np.array_equal(q,state.q))

    def test_28_basis_and_quadrature_convergence(self):
        m=pf.Model(amplitude=0.1,lapse_amplitude=0.1,quartic=0)
        vals=[pf.SurfaceSolver(m,resolution(k,64)).spectrum(6).values for k in [2,3,4]]
        changes=[np.max(np.abs(vals[i+1]-vals[i])) for i in range(2)]
        self.assertLess(changes[1],changes[0])
        a=pf.SurfaceSolver(m,resolution(4,48)).spectrum(6).values
        self.assertLess(np.max(np.abs(a-vals[-1])),2e-11)
        for i,x in enumerate(changes):record(f"basis_refinement_change_{i}",x)

    def test_29_real_field_contract(self):
        op=pf.SurfaceSolver(pf.Model(),resolution(0,16))
        with self.assertRaises(pf.SolverError):op.vector(np.array([1+1j]))
        with self.assertRaises(pf.SolverError):op.vector(np.array([float("inf")]))
        self.assertEqual(pf.scalar("1/8"),0.125)
        with self.assertRaises(pf.SolverError):pf.scalar("1/0")

    def test_30_finite_resource_budget(self):
        with self.assertRaises(pf.SolverError):
            pf.SurfaceSolver(pf.Model(),pf.Resolution(20,20,128,128,1))


class ReceiptResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.records=[]
    def startTest(self,test):
        self.started=time.perf_counter()
        super().startTest(test)
    def addSuccess(self,test):
        self.records.append({"test":test.id(),"status":"passed",
                             "seconds":time.perf_counter()-self.started})
        super().addSuccess(test)
    def addFailure(self,test,err):
        self.records.append({"test":test.id(),"status":"failed","detail":self._exc_info_to_string(err,test)})
        super().addFailure(test,err)
    def addError(self,test,err):
        self.records.append({"test":test.id(),"status":"error","detail":self._exc_info_to_string(err,test)})
        super().addError(test,err)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,default=Path("verification.json"))
    args=parser.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Verification)
    result=unittest.TextTestRunner(verbosity=2,resultclass=ReceiptResult).run(suite)
    pf.write_json(args.out,{"environment":pf.environment(),"tests_run":result.testsRun,
                           "failures":len(result.failures),"errors":len(result.errors),
                           "successful":result.wasSuccessful(),"tests":result.records,
                           "metrics":METRICS,
                           "scope":"implementation verification; not physical validation or a continuum proof"})
    return 0 if result.wasSuccessful() else 1


if __name__=="__main__":
    raise SystemExit(main())
