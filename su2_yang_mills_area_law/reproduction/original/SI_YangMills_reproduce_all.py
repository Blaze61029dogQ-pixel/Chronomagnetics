#!/usr/bin/env python3
# CONFIDENTIAL — DO NOT SHARE · DO NOT COPY · DO NOT REPRODUCE
"""
SI_YangMills_reproduce_all.py
=============================
One-file reproduction of every computation in the SI Yang–Mills programme
(Record v1.4 + addendum v1.5, Paper 1, Paper 2, Track 5 spec v0.1), 28 Sept. 2026.


Usage
-----
    python3 SI_YangMills_reproduce_all.py              # quick mode (all sections, reduced grids)
    python3 SI_YangMills_reproduce_all.py --full       # exact grids used in the papers (slow)
    python3 SI_YangMills_reproduce_all.py --sections S1,S5 --full
    python3 SI_YangMills_reproduce_all.py --json report.json


Requirements: Python 3.9+, numpy, scipy, mpmath.
- Exact rational arithmetic (fractions.Fraction) for the series certificates.
- mpmath at 30–60 digits for the special-function values.
- IEEE-754 double precision (numpy) for the lattice / Monte Carlo checks.
- Fixed seeds throughout, and no intermediate rounding.
- Exit status 1 if any check FAILs.


Tiers attached to each check
----------------------------
- EXACT  — exact identity / rational computation (proof-supporting)
- CERT   — certificate component (exact rationals + rigorous majorant tails)
- NUM    — high-precision numerical evidence (not a proof over a continuum)
- MC     — Monte Carlo evidence (statistical)
- REG    — regression against a value quoted in a document


Sections
--------
- S1  Track 1 / Paper 1 §3: Neumann-flow constant, moments, closed forms, series certificates, tails, grid minima
- S2  Theorem C (Paper 1 §5): Bakry–Émery sharpness, TV obstruction, chordal-W1 sharpness, mean-field point
- S3  Proposition/Conjecture D (Paper 1 §6): MAD values, transverse monotonicity, MAD grid, TV ranges
- S4  DF80 normalisation (Paper 1 Remark 7.1)
- S5  Track 2 (Paper 2 §§2–3): geometry, plaquette-exponent audit; consistency checks of the (analytically proved) covariance estimate
- S6  Sharpness and blocks (Paper 2 §5): lever-1, geodesic metric, inner-Dobrushin identity, plaquette block, MC
- S7  Track 4 (Paper 2 §4): character coefficients, 2D exact gap, mass bounds
- S8  Track 3: SU(N) zero-field linear response (MC)
- S9  Track 5 spec: Lemma A ingredients, Wilson calibration, 2D prototype, critical physical scale
- S10 Asymptotic-scaling constants (SU(2))
"""
import argparse, itertools, json, math, sys, time
from fractions import Fraction as Fr
from math import factorial
import numpy as np
import sys
import math
import mpmath as mpm
from mpmath import mp, mpf


# ----------------------------------------------------------------------------------------------------------
# reporting
# ----------------------------------------------------------------------------------------------------------
RESULTS = []
def check(section, cid, desc, tier, ok, value=None, expected=None):
    status = "INFO" if ok is None else ("PASS" if bool(ok) else "FAIL")
    RESULTS.append(dict(section=section, id=cid, desc=desc, tier=tier, status=status,
                        value=None if value is None else str(value),
                        expected=None if expected is None else str(expected)))
    v = "" if value is None else f"  value={value}"
    e = "" if expected is None else f"  expected={expected}"
    print(f"  [{status}] {cid:<8} {tier:<5} {desc}{v}{e}", flush=True)


def close(x, y, tol):
    return abs(mpf(x) - mpf(y)) <= mpf(tol)


def s(x, n=20):
    return mpm.nstr(x, n)


# ----------------------------------------------------------------------------------------------------------
# shared special functions (mpmath)
# ----------------------------------------------------------------------------------------------------------
def I(n, x):
    return mpm.besseli(n, x)


# f(r) = E_sigma[e^{r t}] = 2 I1(r)/r and its derivatives in closed form, from (I_nu/r^nu)' = I_{nu+1}/r^nu
def f0(r): return 2*I(1, r)/r
def f1(r): return 2*I(2, r)/r
def f2(r): return 2*I(2, r)/r**2 + 2*I(3, r)/r
def f3(r): return 6*I(3, r)/r**2 + 2*I(4, r)/r


def FB(r):   # 24 r^2 I1^2 (1/4 - B_bound)
    return 6*r**2*I(1, r)**2 - 64*I(2, r)**2 - 96*I(3, r)**2 - r**2*I(2, 2*r)


def DA(r):   # 12 f^4 (1/4 - A_bound)
    F0, F1, F2, F3 = f0(r), f1(r), f2(r), f3(r)
    return (3*F0**4 - 32*(F2*F0 - F1**2)**2 - 32*(F3*F0 - F2*F1)**2
            - 4*(f2(2*r)*F0**2 - 2*F0*F1*f1(2*r) + F1**2*f0(2*r)))


def A_bound(r): return mpf(1)/4 - DA(r)/(12*f0(r)**4)
def B_bound(r): return mpf(1)/4 - FB(r)/(24*r**2*I(1, r)**2)
def a_ratio(r): return I(2, r)/I(1, r)      # vMF mean component a(r) = I2/I1


# ----------------------------------------------------------------------------------------------------------
# exact power-series arithmetic (Fractions), coefficient lists in powers of r
# ----------------------------------------------------------------------------------------------------------
class Series:
    def __init__(self, N): self.N = N
    def zero(self): return [Fr(0)]*(self.N+1)
    def I(self, n, scale=1):
        c = self.zero(); m = 0
        while 2*m+n <= self.N:
            c[2*m+n] = Fr(scale**(2*m+n), 2**(2*m+n)*factorial(m)*factorial(m+n)); m += 1
        return c
    def mul(self, a, b):
        c = self.zero()
        na = [(i, x) for i, x in enumerate(a) if x]; nb = [(j, y) for j, y in enumerate(b) if y]
        for i, x in na:
            for j, y in nb:
                if i+j <= self.N: c[i+j] += x*y
        return c
    def add(self, *terms):
        c = self.zero()
        for coef, sr in terms:
            for i, x in enumerate(sr):
                if x: c[i] += coef*x
        return c
    def shift(self, sr, p):
        c = self.zero()
        for i, x in enumerate(sr):
            if x and i+p <= self.N: c[i+p] = x
        return c
    def deriv(self, sr):
        c = self.zero()
        for i, x in enumerate(sr):
            if i >= 1 and x: c[i-1] = i*x
        return c
    def at2r(self, sr): return [x*Fr(2)**i for i, x in enumerate(sr)]


# ==========================================================================================================
# S1 — Track 1 / Paper 1 §3
# ==========================================================================================================
def S1(full):
    mp.dps = 50  # section-local precision (no inherited state)
    print("\nS1  Track 1: Neumann flow, closed forms, Bessel certificates")
    mp.dps = 50
    # Neumann-flow constant |B^4|^{1/2} / |S^3|^{1/2} = 1/2  (the audited 'sqrt2' question)
    val = mpm.sqrt(mpm.pi**2/2)/mpm.sqrt(2*mpm.pi**2)
    check("S1", "1.1", "Neumann constant |B4|^1/2/|S3|^1/2 = 1/2 (no sqrt2 defect)", "EXACT", close(val, mpf(1)/2, 1e-45), s(val, 25))
    # moments on S^3 (law of t: (2/pi) sqrt(1-t^2) dt;  E[n2^2 | t] = (1-t^2)/3)
    w = lambda t: 2/mpm.pi*mpm.sqrt(1-t*t)
    En2 = mpm.quad(lambda t: (1-t*t)/3*w(t), [-1, 1])
    En12n22 = mpm.quad(lambda t: t*t*(1-t*t)/3*w(t), [-1, 1])
    U1 = mpm.quad(lambda t: (2*t)**2*w(t), [-1, 1]); U2 = mpm.quad(lambda t: (4*t*t-1)**2*w(t), [-1, 1])
    check("S1", "1.2", "E_sigma[n2^2] = 1/4 (= Var_sigma(v.n); Theorem B attainment)", "EXACT", close(En2, mpf(1)/4, 1e-40), s(En2))
    check("S1", "1.3", "E_sigma[n1^2 n2^2] = 1/24", "EXACT", close(En12n22, mpf(1)/24, 1e-40), s(En12n22))
    check("S1", "1.4", "||U1(t)|| = ||U2(t)|| = 1 (zonal Chebyshev-U normalisation)", "EXACT", close(U1, 1, 1e-40) and close(U2, 1, 1e-40))
    norm = mpm.quad(w, [-1, 1])
    check("S1", "1.4b", "law of t is normalised: int (2/pi) sqrt(1-t^2) dt = 1 (radical audit)", "EXACT", close(norm, 1, 1e-40), s(norm, 20))
    # closed-form derivatives of f vs numerical differentiation
    mp.dps = 30
    r0 = mpf('1.7'); fn = lambda r: 2*I(1, r)/r
    errs = [abs(f1(r0)-mpm.diff(fn, r0, 1)), abs(f2(r0)-mpm.diff(fn, r0, 2)), abs(f3(r0)-mpm.diff(fn, r0, 3))]
    check("S1", "1.5", "closed forms f', f'', f''' (Bessel recurrences) vs numerical diff", "EXACT", max(errs) < mpf(10)**-20, s(max(errs), 3))
    # Proposition 3.3 closed forms vs direct quadrature
    def Es(phi, r): return mpm.quad(lambda t: phi(t)*mpm.e**(r*t)*2/mpm.pi*mpm.sqrt(1-t*t), [-1, 1])
    worst = mpf(0)
    for r in [mpf('0.7'), mpf('2.3'), mpf(4)]:
        fr = f0(r); a = a_ratio(r)
        d = [4*(Es(lambda t: (1-t*t)/3, r)/fr)**2 - 4*(I(2, r)/(r*I(1, r)))**2,
             24*(Es(lambda t: t*(1-t*t)/3, r)/fr)**2 - 24*(I(3, r)/(r*I(1, r)))**2,
             Es(lambda t: (1-t*t)/3*mpm.e**(r*t), r)/fr**2 - I(2, 2*r)/(8*I(1, r)**2),
             4*(Es(lambda t: t*t, r)/fr - a*a)**2 - 4*(f2(r)*fr - f1(r)**2)**2/fr**4,
             (4*Es(lambda t: t**3, r)/fr - 4*a*Es(lambda t: t*t, r)/fr)**2 - 16*(f3(r)*fr - f2(r)*f1(r))**2/fr**4,
             Es(lambda t: (t-a)**2*mpm.e**(r*t), r)/fr**2 - (f2(2*r)*fr**2 - 2*fr*f1(r)*f1(2*r) + f1(r)**2*f0(2*r))/fr**4]
        worst = max(worst, max(abs(x) for x in d))
    check("S1", "1.6", "Prop 3.3 closed forms (beta1,beta2,|n2F|^2,alpha1,alpha2,|(t-a)F|^2) vs quadrature", "EXACT", worst < mpf(10)**-20, s(worst, 3))


    # ---- series certificate for F_B (exact to k=80, majorant tail k>=81)
    t0 = time.time()
    SB = Series(2*81+2)
    I1s, I2s, I3s, I2_2r = SB.I(1), SB.I(2), SB.I(3), SB.I(2, 2)
    FBs = SB.add((6, SB.shift(SB.mul(I1s, I1s), 2)), (-64, SB.mul(I2s, I2s)), (-96, SB.mul(I3s, I3s)), (-1, SB.shift(I2_2r, 2)))
    c = [FBs[2*k] for k in range(0, 81)]
    exp_c = [Fr(1, 1152), Fr(7, 92160), Fr(1, 368640), Fr(17, 371589120), Fr(1, 9909043200)]
    check("S1", "1.7", "F_B: c0..c3 = 0 and c4..c8 exact rationals as in Lemma 3.4", "CERT",
          all(c[k] == 0 for k in range(4)) and c[4:9] == exp_c, [str(x) for x in c[4:9]])
    check("S1", "1.8", "F_B: c9 < 0 (first negative coefficient)", "CERT", c[9] < 0, float(c[9]))
    S_B = sum(abs(c[k])*Fr(16)**(k-4) for k in range(9, 81))
    check("S1", "1.9", "F_B: sum_{9<=k<=80} |c_k| 16^{k-4}", "CERT", abs(float(S_B) - 2.1438097929853266e-05) < 1e-17, float(S_B), "2.1438e-5")
    # exact rational tail majorants: I_nu(x) <= (x/2)^nu e^x / nu!,  e < 27183/10000
    E_UP = Fr(27183, 10000)
    def IU(nu, x): return Fr(x, 2)**nu * E_UP**x / factorial(nu)
    Rr = 8
    MBq = 6*Rr**2*IU(1, Rr)**2 + 64*IU(2, Rr)**2 + 96*IU(3, Rr)**2 + Rr**2*IU(2, 2*Rr)
    tailBq = MBq*Fr(1, 16**4)*Fr(16, Rr*Rr)**81
    check("S1", "1.10", "F_B tail k>=81: majorant bounded in EXACT RATIONALS (elementary Bessel bound, e<2.7183)", "CERT", tailBq < Fr(6, 10**43), f"{float(tailBq):.3e}", "<= 5.4e-43")
    margq = c[4] - S_B - tailBq
    check("S1", "1.11", "F_B/r^8 > 8.466e-4 on (0,4]  (Lemma 3.4; exact rational margin)", "CERT", margq > Fr(8466, 10**7), f"{float(margq):.12e}")
    mp.dps = 60; R = mpf(8)
    # ---- series certificate for D_A (nonnegative coefficients to K-1, majorant tail k>=K)
    K = 190 if full else 71
    SA = Series(2*K+2)
    ff = SA.zero(); m = 0
    while 2*m <= SA.N:
        ff[2*m] = Fr(1, 4**m*factorial(m)*factorial(m+1)); m += 1
    g1, g2, g3 = SA.deriv(ff), SA.deriv(SA.deriv(ff)), SA.deriv(SA.deriv(SA.deriv(ff)))
    F0, F1, F2 = SA.at2r(ff), SA.at2r(g1), SA.at2r(g2)
    fsq = SA.mul(ff, ff)
    T1 = SA.add((1, SA.mul(g2, ff)), (-1, SA.mul(g1, g1)))
    T2 = SA.add((1, SA.mul(g3, ff)), (-1, SA.mul(g2, g1)))
    T3 = SA.add((1, SA.mul(F2, fsq)), (-2, SA.mul(SA.mul(ff, g1), F1)), (1, SA.mul(SA.mul(g1, g1), F0)))
    DAs = SA.add((3, SA.mul(fsq, fsq)), (-32, SA.mul(T1, T1)), (-32, SA.mul(T2, T2)), (-4, T3))
    d = [DAs[2*k] for k in range(0, K)]
    check("S1", "1.12", "D_A: d0=0, d1=3/8, d2=9/64, d3=143/5760; odd powers vanish", "CERT",
          d[0] == 0 and d[1:4] == [Fr(3, 8), Fr(9, 64), Fr(143, 5760)] and all(DAs[2*k+1] == 0 for k in range(K-1)))
    nonneg = all(d[k] >= 0 for k in range(1, K))
    check("S1", "1.13", f"D_A: all exact coefficients d_k >= 0 for 1 <= k <= {K-1}", "CERT", nonneg)
    if full:
        S2 = sum(abs(d[k])*Fr(16)**(k-1) for k in range(71, 190))
        check("S1", "1.14", "D_A: exact sum_{71..189} |d_k|16^{k-1} (draft's '4.7e-3' is not reproducible)", "REG",
              float(S2) < 1e-80, f"{float(S2):.4e}", "2.08e-85")
    mp.dps = 60
    MA = (3*f0(R)**4 + 32*(f2(R)*f0(R) + f1(R)**2)**2 + 32*(f3(R)*f0(R) + f2(R)*f1(R))**2
          + 4*(f2(2*R)*f0(R)**2 + 2*f0(R)*f1(R)*f1(2*R) + f1(R)**2*f0(2*R)))
    def fUq(j, x):
        if j == 0: return 2*IU(1, x)/x
        if j == 1: return 2*IU(2, x)/x
        if j == 2: return 2*IU(2, x)/x**2 + 2*IU(3, x)/x
        return 6*IU(3, x)/x**2 + 2*IU(4, x)/x
    MAq = (3*fUq(0, Rr)**4 + 32*(fUq(2, Rr)*fUq(0, Rr) + fUq(1, Rr)**2)**2 + 32*(fUq(3, Rr)*fUq(0, Rr) + fUq(2, Rr)*fUq(1, Rr))**2
           + 4*(fUq(2, 2*Rr)*fUq(0, Rr)**2 + 2*fUq(0, Rr)*fUq(1, Rr)*fUq(1, 2*Rr) + fUq(1, Rr)**2*fUq(0, 2*Rr)))
    tailAq = MAq*Fr(1, 16)*Fr(16, Rr*Rr)**K
    check("S1", "1.15", f"D_A tail k>={K}: majorant bounded in EXACT RATIONALS, divided by r^2", "CERT",
          tailAq < (Fr(1, 10**98) if full else Fr(1, 10**25)), f"{float(tailAq):.3e}")
    check("S1", "1.16", "D_A/r^2 >= 3/8 - tail > 0.3749 on (0,4]  (Lemma 3.4; exact rational)", "CERT", Fr(3, 8) - tailAq > Fr(3749, 10**4))
    print(f"      (series certificates: {time.time()-t0:.1f}s)")
    # ---- direct grid minima
    mp.dps = 50
    step = 1 if full else 8
    rs = [mpf(k)/200 for k in range(1, 801, step)]
    if mpf(1)/200 not in rs: rs = [mpf(1)/200] + rs
    fb = [FB(r)/r**8 for r in rs]; da = [DA(r)/r**2 for r in rs]
    ib = min(range(len(rs)), key=lambda i: fb[i]); ia = min(range(len(rs)), key=lambda i: da[i])
    check("S1", "1.17", "grid min F_B/r^8 = 8.6806e-4 at r=0.005 (above certificate)", "NUM",
          close(fb[ib], mpf('8.6806e-4'), 1e-8) and rs[ib] == mpf(1)/200, s(fb[ib], 10))
    check("S1", "1.18", "grid min D_A/r^2 = 0.3750035 at r=0.005 (above certificate)", "NUM",
          close(da[ia], mpf('0.3750035'), 1e-7) and rs[ia] == mpf(1)/200, s(da[ia], 10))
    # Levin (1980) comparison: general-N Neumann constant and exact Q beyond the certified window (NUM)
    ok_N = all(close(mpm.sqrt((2*mpm.pi**(mpf(N)/2)/mpm.gamma(mpf(N)/2))/N)/mpm.sqrt(2*mpm.pi**(mpf(N)/2)/mpm.gamma(mpf(N)/2)), 1/mpm.sqrt(N), 1e-40) for N in range(2, 9))
    check("S1", "1.20", "general N: |B^N|^1/2/|S^{N-1}|^1/2 = N^-1/2, so Neumann bound = 1/N at zero field (Levin conj. sharp)", "EXACT", ok_N)
    xg, wg = np.polynomial.legendre.leggauss(4000); th = (xg+1)*np.pi/2; tt = np.cos(th); dens = (2/np.pi)*np.sin(th)**2*wg*np.pi/2
    def exactAB(r, K=80):
        g = np.exp(r*(tt-1)); Z = (g*dens).sum(); F = g/Z; a = (tt*F*dens).sum()
        Uk = [np.ones_like(tt), 2*tt]; Ck = [np.ones_like(tt), 4*tt]
        for k in range(2, K+1): Uk.append(2*tt*Uk[-1]-Uk[-2])
        for n in range(2, K+1): Ck.append((2*tt*(n+1)*Ck[-1]-(n+2)*Ck[-2])/n)
        A = sum(((tt-a)*F*Uk[k]*dens).sum()**2/k for k in range(1, K+1))
        B = sum((((1-tt*tt)/3)*F*Ck[k-1]*dens).sum()**2/((1-tt*tt)/3*Ck[k-1]**2*dens).sum()/k for k in range(1, K+1))
        return A, B
    rs_ex = [0.5, 2, 4, 6, 10, 20, 30]; Ls = [0.5*np.sqrt(max(*exactAB(r))) for r in rs_ex]
    check("S1", "1.21", "exact Neumann-flow bound < 1/4 and decreasing for r in [0.5,30] (Levin conj. N=4 beyond window; NUM)", "NUM",
          all(L < 0.25 for L in Ls) and all(Ls[i] > Ls[i+1] for i in range(len(Ls)-1)), ", ".join(f"{L:.4f}" for L in Ls))
    # Theorem 3.8 (Levin's conjecture, N = 4): interval certificate for r >= 4
    iv = mpm.iv; iv.dps = 40
    def I_enc(n, x):
        h2 = (x/2)**2; term = (x/2)**n/factorial(n); ssum = iv.mpf(0); m = 0
        while True:
            ssum += term; qq = h2/((m+1)*(m+n+1)); term = term*qq; m += 1
            if qq.b < 0.5 and term.b < ssum.a*mpf(10)**-35: break
        return ssum + iv.mpf([0, (term*2).b])
    a_enc = lambda x: I_enc(2, x)/I_enc(1, x)
    rr = iv.mpf(4); ar = a_enc(rr); hh = mpf(1)/64; worst_c = 0.0; ncell = 0
    while rr.a < 256:
        while True:
            r2 = rr + hh; ar2 = a_enc(r2); Alo, Ahi = ar.a, ar2.b
            U = 1 - iv.mpf(Alo)**2 - 3*iv.mpf(Alo)/r2
            bnd = 2*U**2/(1 - iv.mpf(Ahi)) + iv.mpf(Ahi)**2/rr**2
            if U.a >= 0 and bnd.b < mpf(1)/16: break
            hh = hh/2
        worst_c = max(worst_c, float(bnd.b)); ncell += 1; rr, ar = r2, ar2; hh = min(hh*2, mpf(8))
    tail_c = float((8*(1 - iv.mpf(ar.a)) + iv.mpf(1)/rr**2).b)
    check("S1", "1.22", f"Thm 3.8 (Levin conj. N=4): interval certificate Lambda^2<1/16 on [4,{float(rr.a):.2f}] ({ncell} cells) + tail", "CERT",
          worst_c < 1/16 and tail_c < 1/16, f"max cell <= {math.ceil(worst_c*1e6)/1e6:.6f}, tail <= {math.ceil(tail_c*1e6)/1e6:.6f} (outward-rounded)")
    mp.dps = 30
    b12 = lambda r, N: (lambda a: N*(a/r)**2)(I(mpf(N)/2, r)/I(mpf(N)/2-1, r))
    wN = lambda t, N: (1-t*t)**(mpf(N-3)/2)
    def beta2(r, N):
        Zs = mpm.quad(lambda t: wN(t, N)*mpm.exp(r*t), [-1, 1]); Z0 = mpm.quad(lambda t: wN(t, N), [-1, 1])
        num = mpm.quad(lambda t: (1-t*t)/(N-1)*t*wN(t, N)*mpm.exp(r*t), [-1, 1])/Zs
        den = mpm.quad(lambda t: (1-t*t)/(N-1)*t*t*wN(t, N), [-1, 1])/Z0
        return num**2/den
    B5 = b12(mpf('0.3'), 5) + beta2(mpf('0.3'), 5)/2
    check("S1", "1.23", "Remark 3.9: for N=5 the Neumann-flow B >= beta1+beta2/2 exceeds 1/5 at r=0.3 (method fails for N>=5)", "NUM", B5 > mpf(1)/5, s(B5, 8))
    # Paper 1 Thm 3.9 (Levin's conjecture, N = 3): run the standalone certificate and parse its verdict
    import subprocess, os
    cert = os.path.join(os.path.dirname(os.path.abspath(__file__)), "levin_N3_certificate.py")
    if os.path.exists(cert):
        out = subprocess.run([sys.executable, cert], capture_output=True, text=True, timeout=250).stdout
        okN3 = "CERTIFIED" in out and "NOT certified" not in out
        line = [l for l in out.splitlines() if l.startswith("strong:")]
        check("S1", "1.25", "Thm 3.9 (Levin conj. N=3): rational weak-field series (k<=120, c_k>=0) + interval strong-field cells, overlap [3.3,3.5]", "CERT",
              okN3, line[0][:110] if line else out[-120:])
    else:
        check("S1", "1.25", "Thm 3.9 certificate file present next to this script", "CERT", False, "levin_N3_certificate.py missing")
    # Paper 2 Cor. cor:chat (Chatterjee corollary): one-block smoothing Lipschitz bound, numerical consistency test
    rs = np.random.default_rng(7)
    def _unit(n): v = rs.normal(size=(n, 4)); return v/np.linalg.norm(v, axis=1, keepdims=True)
    def _qm(a, b):
        w1,x1,y1,z1 = a[...,0],a[...,1],a[...,2],a[...,3]; w2,x2,y2,z2 = b[...,0],b[...,1],b[...,2],b[...,3]
        return np.stack([w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2, w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2], -1)
    Qs = _unit(60000); worst_s = 0.0
    for _ in range(80):
        bW = rs.uniform(0.05, 0.6); nk = int(rs.integers(1, 7)); fixed = _unit(6); Aq, Bq = _unit(nk), _unit(nk)
        vv = _unit(1)[0]; cc = rs.uniform(-0.9, 0.9); fv = np.where(Qs @ vv > cc, 1.0, -1.0)
        def Fw(w):
            st = fixed.copy(); st[:nk] = _qm(_qm(Aq, np.broadcast_to(w, (nk, 4))), Bq)
            eta = bW*(st*np.array([1,-1,-1,-1])).sum(0); lw = Qs @ eta; ww = np.exp(lw - lw.max()); return (fv*ww).sum()/ww.sum()
        w0 = _unit(1)[0]; w1 = w0 + 0.05*rs.normal(size=4); w1 /= np.linalg.norm(w1)
        worst_s = max(worst_s, abs(Fw(w0) - Fw(w1))/(2*nk*bW*np.linalg.norm(w0 - w1)))
    check("S1", "1.24", "Paper 2 Cor. (Chatterjee): one-block smoothing |dF| <= 2 n_k bW ||f|| |dw| (80 random vMF blocks, discontinuous f)", "NUM", worst_s <= 1.0, f"max ratio {worst_s:.4f}")
    mp.dps = 50
    Lmax = max(mpm.sqrt(max(A_bound(r), B_bound(r)))/2 for r in [mpf('0.3'), mpf(1), mpf('2.5'), mpf(4)])
    check("S1", "1.19", "Corollary 3.6: (1/2)sqrt(max(A,B)) < 1/4 at sample r in (0,4]", "NUM", Lmax < mpf(1)/4, s(Lmax, 15))


# ==========================================================================================================
# S2 — Theorem C
# ==========================================================================================================
def S2(full):
    mp.dps = 50  # section-local precision (no inherited state)
    print("\nS2  Theorem C: limits of single-site criteria on the slab")
    rng = np.random.default_rng(6)
    L = 4; N = L**3
    def idx(x, y, z): return ((x % L)*L + (y % L))*L + (z % L)
    bonds = [(idx(x, y, z), idx(x+dx, y+dy, z+dz)) for x in range(L) for y in range(L) for z in range(L)
             for (dx, dy, dz) in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]]
    def tangent(n):
        M = np.linalg.qr(np.column_stack([n, rng.normal(size=(4, 3))]))[0]; return M[:, 1:]
    def randSO4():
        Q, Rr = np.linalg.qr(rng.normal(size=(4, 4))); Q = Q*np.sign(np.diag(Rr))
        if np.linalg.det(Q) < 0: Q[:, 0] *= -1
        return Q
    def min_eig(K, n, Rb):
        E = [tangent(n[i]) for i in range(N)]; H = np.zeros((3*N, 3*N))
        for i in range(N): H[3*i:3*i+3, 3*i:3*i+3] += 2*np.eye(3)
        for (i, j), Rm in zip(bonds, Rb):
            nn = n[i] @ Rm @ n[j]
            H[3*i:3*i+3, 3*i:3*i+3] += K*nn*np.eye(3); H[3*j:3*j+3, 3*j:3*j+3] += K*nn*np.eye(3)
            B = -K*E[i].T @ Rm @ E[j]; H[3*i:3*i+3, 3*j:3*j+3] += B; H[3*j:3*j+3, 3*i:3*i+3] += B.T
        return np.linalg.eigvalsh(H).min()
    e0 = np.array([1., 0, 0, 0])
    stag = np.array([e0*(-1)**(x+y+z) for x in range(L) for y in range(L) for z in range(L)])
    I4 = [np.eye(4)]*len(bonds)
    nrand = 5 if full else 2
    for K in [0.1, 1/6, 0.25]:
        me = min_eig(K, stag, I4)
        check("S2", f"2.1-{K:.3f}", f"BE: staggered config attains Ric+Hess V = 2-12K at K={K:.4f}", "EXACT", abs(me-(2-12*K)) < 1e-10, f"{me:.12f}", f"{2-12*K:.12f}")
        wr = min(min_eig(K, np.array([v/np.linalg.norm(v) for v in rng.normal(size=(N, 4))]), [randSO4() for _ in bonds]) for _ in range(nrand))
        check("S2", f"2.2-{K:.3f}", "BE: random configs/environments stay above 2-12K", "NUM", wr > 2-12*K, f"{wr:.6f}")
    check("S2", "2.3b", "Levin (1980) baselines: slab 4/(6 sqrt5) = 2/(3 sqrt5), links 4/(18 sqrt5) = 2/(9 sqrt5); ours improve both by sqrt5", "EXACT",
          close((mpf(2)/3)/(mpf(2)/(3*mpm.sqrt(5))), mpm.sqrt(5), 1e-25) and close((mpf(2)/9)/(mpf(2)/(9*mpm.sqrt(5))), mpm.sqrt(5), 1e-25) and mpf(2)/(9*mpm.sqrt(5)) > mpf(1)/12,
          f"{s(mpf(2)/(3*mpm.sqrt(5)), 8)}, {s(mpf(2)/(9*mpm.sqrt(5)), 8)}")
    check("S2", "2.3", "CNS25b condition (N+2)/2-1-4N beta(d-1)>0 at N=2,d=4 <=> beta_W<1/6", "EXACT", Fr(4)*Fr(1, 24) == Fr(1, 6))
    mp.dps = 30
    KTV = mpm.findroot(lambda K: 6*mpm.struvel(1, K) - I(1, K), 0.4)
    check("S2", "2.4", "K_TV = root of 6 L1(K) = I1(K)", "REG", mpm.nstr(KTV, 20) == '0.39629095688184401321', s(KTV, 22), "0.39629095688184401321")
    check("S2", "2.5", "L1/I1 = 1/6 at K_TV", "EXACT", close(mpm.struvel(1, KTV)/I(1, KTV), mpf(1)/6, 1e-25))
    worst = mpf(0)
    for K in [mpf('0.2'), KTV, mpf('1.3')]:
        fK = 2*I(1, K)/K
        tv = mpm.quad(lambda t: (2/mpm.pi)*mpm.sqrt(1-t*t)*abs(mpm.exp(K*t)-mpm.exp(-K*t))/fK, [-1, 0, 1])/2
        worst = max(worst, abs(tv - mpm.struvel(1, K)/I(1, K)))
    check("S2", "2.6", "TV(mu_eta, mu_-eta) = L1(K)/I1(K) (quadrature, three K)", "EXACT", worst < mpf(10)**-20, s(worst, 3))
    mp.dps = 20
    vals = [mpm.struvel(1, mpf(k)/100)/I(1, mpf(k)/100) for k in range(1, 301)]
    check("S2", "2.7", "L1/I1 increasing on (0,3] (grid consistency; proof in 2.7b)", "NUM", all(vals[i] < vals[i+1] for i in range(len(vals)-1)))
    # proof ingredients (Paper 1 §5.2): R = E_nu[tanh(Kt)], nu ∝ sqrt(1-t^2) cosh(Kt) on [0,1];
    # R' = E_nu[t sech^2(Kt)] + Cov_nu(tanh(Kt), t tanh(Kt)), both terms >= 0 (association)
    mp.dps = 30
    wf = lambda t: mpm.sqrt(1-t*t); worst_r = mpf(0); worst_d = mpf(0); pos = True
    for K in [mpf('0.05'), mpf('0.4'), mpf('2'), mpf('7')]:
        Dn = mpm.quad(lambda t: wf(t)*mpm.cosh(K*t), [0, 1]); Ev = lambda gg: mpm.quad(lambda t: gg(t)*wf(t)*mpm.cosh(K*t), [0, 1])/Dn
        Rk = mpm.struvel(1, K)/I(1, K)
        worst_r = max(worst_r, abs(Rk - mpm.quad(lambda t: wf(t)*mpm.sinh(K*t), [0, 1])/Dn))
        t1 = Ev(lambda t: t*mpm.sech(K*t)**2)
        cv = Ev(lambda t: t*mpm.tanh(K*t)**2) - Ev(lambda t: mpm.tanh(K*t))*Ev(lambda t: t*mpm.tanh(K*t))
        worst_d = max(worst_d, abs(mpm.diff(lambda x: mpm.struvel(1, x)/I(1, x), K) - (t1 + cv))); pos &= (t1 > 0 and cv >= 0)
    check("S2", "2.7b", "monotonicity proof: Poisson form of L1/I1, derivative decomposition, both terms >= 0", "EXACT",
          worst_r < mpf(10)**-25 and worst_d < mpf(10)**-20 and pos, f"{s(worst_r, 3)}, {s(worst_d, 3)}")
    mp.dps = 40
    dl = mpf('1e-12')
    check("S2", "2.8", "chordal-W1 attainment: a(|delta|)/|delta| -> 1/4 at eta=0 (C_xy >= K/4)", "EXACT", close(a_ratio(dl)/dl, mpf(1)/4, 1e-20), s(a_ratio(dl)/dl, 20))
    Wat = mpm.sqrt(6)/(32*mpm.pi**3)*mpm.gamma(mpf(1)/24)*mpm.gamma(mpf(5)/24)*mpm.gamma(mpf(7)/24)*mpm.gamma(mpf(11)/24)
    KIR = 4*Wat/6
    check("S2", "2.10", "Thm C(iv): infrared-bound threshold K_IR = 4 G_Z3(0) = 1.0109 (Watson closed form); >= numerical K_c 0.936", "EXACT",
          mpm.nstr(KIR, 5) == '1.0109' and KIR > mpf('0.9361'), s(KIR, 12))
    sR = mpm.sqrt(mpm.pi**2/3 - mpf(5)/2)
    check("S2", "2.11", "Royer (1986) Thm 3.6 baseline: 2/sqrt(pi^2/3-5/2) = 2.2504 reproduces his N=4 table value 2.25", "EXACT",
          mpm.nstr(2/sR, 3) == '2.25', s(2/sR, 10))
    check("S2", "2.12", "Royer-derivable ranges: slab 1/(3s) = 0.37506, links 1/(9s) = 0.12502; ours exceed by 2s = 1.7775", "EXACT",
          abs(1/(3*sR) - mpf('0.375060604')) < 1e-8 and abs(1/(9*sR) - mpf('0.1250202014')) < 1e-9, f"{float(1/(3*sR)):.8f}, {float(1/(9*sR)):.9f}, factor {float(2*sR):.6f}")
    check("S2", "2.9", "row sum 6K/4 = 1 at K = 2/3 = n/z (O(4) mean-field point)", "EXACT", Fr(6)*Fr(2, 3)/4 == 1 and Fr(4, 6) == Fr(2, 3))


# ==========================================================================================================
# S3 — Proposition / Conjecture D
# ==========================================================================================================
def MAD(r, th):
    c, sn = mpm.cos(th), mpm.sin(th)
    if r == 0: fr = mpf(1); a = mpf(0)
    else: fr = 2*I(1, r)/r; a = I(2, r)/I(1, r)
    def g(t):
        A = c*(t-a); B = sn*mpm.sqrt(1-t*t)
        if B == 0: return abs(A)
        return (A*A+B*B)/(2*B) if abs(A) <= B else abs(A)
    wt = lambda t: (2/mpm.pi)*mpm.sqrt(1-t*t)*mpm.exp(r*t)/fr
    pts = [mpf(-1)] + [mpf(-1)+mpf(k)/20 for k in range(1, 40)] + [mpf(1)]
    return mpm.quad(lambda t: g(t)*wt(t), pts)


def S3(full):
    mp.dps = 50  # section-local precision (no inherited state)
    print("\nS3  Proposition D / Conjecture D: mean absolute deviation of vMF laws")
    mp.dps = 20
    target = 4/(3*mpm.pi)
    e0 = mpm.quad(lambda t: abs(t)*(2/mpm.pi)*mpm.sqrt(1-t*t), [-1, 0, 1])
    check("S3", "3.1", "Prop D(b): E_0|v.n| = 4/(3 pi)", "EXACT", close(e0, target, 1e-18), s(e0))
    tv = [mpm.quad(lambda x: mpm.sqrt(1-x*x)*mpm.sqrt(1-x*x)*mpm.exp(r*x), [-1, 1])/mpm.quad(lambda x: mpm.sqrt(1-x*x)*mpm.exp(r*x), [-1, 1])/2
          for r in [mpf(k)/4 for k in range(0, 41)]]
    check("S3", "3.2", "Prop D(c): transverse MAD E|n2| nonincreasing in r on [0,10]", "NUM",
          all(tv[i+1] <= tv[i] for i in range(len(tv)-1)) and close(tv[0], target, 1e-15), s(tv[0]))
    reg = {'0.05': '0.424386659701183', '0.5': '0.421799431922554', '2': '0.389976705624786', '10': '0.236246547591046'}
    rlist = ['0.05', '0.2', '0.5', '1', '2', '3', '4', '6', '10'] if full else ['0.05', '0.5', '2', '10']
    nth = 21 if full else 11
    allbelow = True; allat90 = True
    for rv in rlist:
        r = mpf(rv)
        vals = [(MAD(r, th), th) for th in [mpm.pi*k/(2*(nth-1)) for k in range(nth)]]
        mx = max(vals)
        allbelow &= mx[0] < target; allat90 &= close(mx[1], mpm.pi/2, 1e-12)
        if rv in reg:
            check("S3", f"3.3-{rv}", f"MAD max over theta at r={rv} (quoted in addendum v1.5)", "REG",
                  mpm.nstr(mx[0], 15) == reg[rv], mpm.nstr(mx[0], 15), reg[rv])
    check("S3", "3.4", "Conjecture D evidence: grid max < 4/(3pi) and always at theta=90 deg", "NUM", allbelow and allat90)
    check("S3", "3.5", "unconditional TV range: 6 * (1/2 * 2K * 1/2) = 3K < 1 <=> K < 1/3", "EXACT", Fr(6)*Fr(1, 2)*2*Fr(1, 3)*Fr(1, 2) == 1)
    # Prop D(d): exact curvatures kappa_par = 13/(120 pi), kappa_perp = 1/(30 pi) (kink-aware quadrature + Richardson)
    mp.dps = 40
    def MAD_par(r):
        a = I(2, r)/I(1, r); Zr = 2*I(1, r)/r
        return mpm.quad(lambda t: abs(t-a)*(2/mpm.pi)*mpm.sqrt(1-t*t)*mpm.exp(r*t)/Zr, [-1, a, 1])
    def MAD_perp(r):
        num = mpm.quad(lambda x: (1-x*x)*mpm.exp(r*x), [-1, 1]); den = mpm.quad(lambda x: mpm.sqrt(1-x*x)*mpm.exp(r*x), [-1, 1])
        return num/den/2
    def kappa(fun):
        k1 = (target - fun(mpf('0.01')))/mpf('0.01')**2; k2 = (target - fun(mpf('0.02')))/mpf('0.02')**2
        return k1 + (k1-k2)/3
    kpar, kperp = kappa(MAD_par), kappa(MAD_perp)
    check("S3", "3.7", "Prop D(d): longitudinal curvature = 13/(120 pi)", "EXACT", close(kpar, 13/(120*mpm.pi), 1e-9), s(kpar, 12), s(13/(120*mpm.pi), 12))
    check("S3", "3.8", "Prop D(d): transverse curvature = 1/(30 pi) = -Cov_0(sqrt(1-x^2), x^2)/4", "EXACT",
          close(kperp, 1/(30*mpm.pi), 1e-9) and close(-mpm.quad(lambda x: (mpm.sqrt(1-x*x)*x*x - mpm.sqrt(1-x*x)/4)*(2/mpm.pi)*mpm.sqrt(1-x*x), [-1, 1])/4, 1/(30*mpm.pi), 1e-30),
          s(kperp, 12), s(1/(30*mpm.pi), 12))
    mp.dps = 20
    Kc = mpm.pi/8
    check("S3", "3.6", "conditional TV range: 6 * (1/2 * 2K * 4/(3pi)) = 8K/pi = 1 at K = pi/8", "EXACT",
          close(6*(mpf(1)/2*2*Kc*4/(3*mpm.pi)), 1, 1e-18), s(Kc, 6))


# ==========================================================================================================
# S4 — DF80 normalisation
# ==========================================================================================================
def S4(full):
    mp.dps = 50  # section-local precision (no inherited state)
    print("\nS4  DF80 normalisation (Paper 1, Remark 7.1)")
    rng = np.random.default_rng(80)
    def phi(S):
        S0, S1_, S2_, S3_ = S
        return np.array([[S0+1j*S3_, -S1_+1j*S2_], [S1_+1j*S2_, S0-1j*S3_]])
    def unit(): v = rng.normal(size=4); return v/np.linalg.norm(v)
    def phiinv(U): return np.array([U[0, 0].real, U[1, 0].real, U[1, 0].imag, U[0, 0].imag])
    r = []
    for _ in range(5):
        S1_, S2_ = unit(), unit()
        r.append(np.trace(np.linalg.inv(phi(S1_)) @ phi(S2_)).real/(S1_ @ S2_))
    check("S4", "4.1", "Tr(phi(S1)^-1 phi(S2)) / (S1.S2) = 2 (5 random pairs)", "EXACT", max(abs(x-2) for x in r) < 1e-12, np.round(r, 12).tolist())
    L = 4; N = L*L; idx = lambda x, y: (x % L)*L + (y % L)
    bonds = [(idx(x, y), idx(x+1, y)) for x in range(L) for y in range(L)] + [(idx(x, y), idx(x, y+1)) for x in range(L) for y in range(L)]
    g = [phi(unit()) for _ in range(N)]
    b = {e: phi(unit()) for e in bonds}; t = {e: phi(unit()) for e in bonds}
    S = np.array([phiinv(u) for u in g])
    def O(h, k): return np.column_stack([phiinv(h @ phi(e) @ np.linalg.inv(k)) for e in np.eye(4)])
    act = sum(np.trace(np.linalg.inv(g[i]) @ b[(i, j)] @ g[j] @ np.linalg.inv(t[(i, j)])).real for (i, j) in bonds)
    nbr = {i: [] for i in range(N)}
    for (i, j) in bonds:
        nbr[i].append((j, O(b[(i, j)], t[(i, j)]))); nbr[j].append((i, O(np.linalg.inv(b[(i, j)]), np.linalg.inv(t[(i, j)]))))
    SDS = -sum(S[i] @ sum(S[i] - Oij @ S[j] for (j, Oij) in nbr[i]) for i in range(N))
    check("S4", "4.2", "vertical-plaquette action = (S,Delta S) + 2(nu-1)|Lambda0| (not half of it)", "EXACT",
          abs(act - (SDS + 2*2*N)) < 1e-10, f"{act:.13f}", f"{SDS + 4*N:.13f}")
    check("S4", "4.3", "consequence: DF argument supports beta_W < 1/(2(nu-1)) = 1/6 at nu=4", "EXACT", Fr(1, 2*(4-1)) == Fr(1, 6))


# ==========================================================================================================
# S5 — Track 2 (Paper 2 §§2–3)
# ==========================================================================================================
E4 = np.eye(4, dtype=int)
def plaq_links(x, m, n):
    x = np.array(x)
    return [(tuple(x), m), (tuple(x+E4[m]), n), (tuple(x+E4[n]), m), (tuple(x), n)]
def plaqs_of_link(link):
    x, m = link; x = np.array(x); out = []
    for n in range(4):
        if n == m: continue
        for base in [x, x-E4[n]]:
            a, b = (m, n) if m < n else (n, m)
            out.append((tuple(base), a, b))
    return out
def link_nbrs(link):
    s_ = set()
    for (x, a, b) in plaqs_of_link(link): s_ |= set(plaq_links(x, a, b))
    s_.discard(link); return s_
def midpoint(link): x, m = link; return np.array(x, float) + 0.5*E4[m]
def pcentre(p): x, a, b = p; return np.array(x, float) + 0.5*(E4[a]+E4[b])


def S5(full):
    mp.dps = 50  # section-local precision (no inherited state)
    print("\nS5  Track 2: geometry, plaquette-exponent audit, covariance lemma on exact systems")
    l0 = ((0, 0, 0, 0), 0)
    nb = link_nbrs(l0)
    check("S5", "5.1", "each link has exactly 18 plaquette-neighbours in Z^4 (6 staples, 3 links each)", "EXACT", len(nb) == 18, len(nb))
    check("S5", "5.2", "Lemma 2.5: neighbours have l_inf midpoint distance <= 1", "EXACT",
          max(np.abs(midpoint(l)-midpoint(l0)).max() for l in nb) <= 1)
    check("S5", "5.3", "alpha = 18 * beta_W/4 = 9 beta_W/2; threshold 2/9; ratio to SZZ 1/12 is 8/3", "EXACT",
          Fr(18)*Fr(2, 9)/4 == 1 and Fr(2, 9)/Fr(1, 12) == Fr(8, 3))
    # plaquette covariance exponent: dist_C(l,l') >= ||c_p - c_p'||_inf - 1, with equality attained (BFS in Z^4)
    B = 5 if full else 4
    p0 = ((0, 0, 0, 0), 0, 1); src = plaq_links(*p0)
    def inbox(link): return all(-B <= c <= B for c in link[0])
    dist = {}
    for s0 in src:
        seen = {s0: 0}; frontier = [s0]
        while frontier:
            nxt = []
            for u in frontier:
                for v in link_nbrs(u):
                    if v not in seen and inbox(v): seen[v] = seen[u]+1; nxt.append(v)
            frontier = nxt
        for k, v in seen.items(): dist[k] = min(dist.get(k, 10**9), v)
    ok = True; tight = 0; npl = 0; worst_mid = True
    c0 = pcentre(p0)
    rng_ = range(-3, 4)
    for x in itertools.product(rng_, repeat=4):
        for a in range(4):
            for b in range(a+1, 4):
                p = (x, a, b); cd = np.abs(pcentre(p)-c0).max()
                if cd > 3: continue
                npl += 1
                dmin = min(dist[l] for l in plaq_links(*p))
                ok &= dmin >= cd - 1 - 1e-12
                tight += int(abs(dmin - (cd - 1)) < 1e-12)
    # Lemma 2.5 consequence, single source: dist_C(l0, l) >= ||m_l - m_l0||_inf
    seen = {src[0]: 0}; frontier = [src[0]]
    while frontier:
        nxt = []
        for u in frontier:
            for v in link_nbrs(u):
                if v not in seen and inbox(v): seen[v] = seen[u]+1; nxt.append(v)
        frontier = nxt
    m0 = midpoint(src[0])
    for l, dv in seen.items():
        if np.abs(midpoint(l)-m0).max() <= 3: worst_mid &= dv >= np.abs(midpoint(l)-m0).max() - 1e-12
    check("S5", "5.4", f"audit: min dist_C over link pairs >= ||c_p-c_p'||_inf - 1 for all {npl} plaquettes within l_inf 3", "EXACT", ok)
    check("S5", "5.5", "audit: the '-1' is attained (pairs with dist_C = ||c_p-c_p'||_inf - 1 exist)", "EXACT", tight > 0, f"{tight} tight plaquettes")
    check("S5", "5.4b", "Lemma 2.5: dist_C(l,l') >= ||m_l - m_l'||_inf (BFS, all links within l_inf 3)", "EXACT", worst_mid)
    check("S5", "5.6", "plaquette constant D^2 * 4 * 4 = 64 (D = 2 chordal diameter)", "EXACT", 2**2*4*4 == 64)
    # isometry of left/right multiplication
    rng = np.random.default_rng(11)
    def qmul(a, b):
        w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
        return np.array([w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2, w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2])
    worst = 0
    for _ in range(2000):
        u, up, a, b = [v/np.linalg.norm(v) for v in rng.normal(size=(4, 4))]
        worst = max(worst, abs(np.linalg.norm(qmul(qmul(a, u), b)-qmul(qmul(a, up), b)) - np.linalg.norm(u-up)))
    check("S5", "5.7", "left/right quaternion multiplication is a chordal isometry", "EXACT", worst < 1e-14, f"{worst:.2e}")
    # covariance lemma on exactly solvable systems (cycle of n sites, q states, line metric)
    rng7 = np.random.default_rng(7)
    def build(n, q, beta):
        states = list(itertools.product(range(q), repeat=n))
        def H(s_): return beta*sum(np.cos(2*np.pi*(s_[i]-s_[(i+1) % n])/q) for i in range(n))
        w = np.array([np.exp(H(s_)) for s_ in states]); mu = w/w.sum()
        def cond(i, s_):
            v = np.array([np.exp(H(s_[:i]+(a,)+s_[i+1:])) for a in range(q)]); return v/v.sum()
        def W1(p, r_): return np.abs(np.cumsum(p-r_)[:-1]).sum()
        C = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    C[i, j] = max(W1(cond(i, s_), cond(i, s_[:j]+(bb,)+s_[j+1:]))/abs(s_[j]-bb) for s_ in states for bb in range(q) if bb != s_[j])
        return states, mu, C, H, cond, W1
    def run(n, q, beta, trials=200):
        states, mu, C, H, cond, W1 = build(n, q, beta); D = q-1
        alpha = C.sum(1).max(); M = np.linalg.inv(np.eye(n)-C); worst = 0.0
        for _ in range(trials):
            ph = rng7.normal(size=(n, q)); ps = rng7.normal(size=(n, q))
            f = np.array([sum(ph[k, s_[k]] for k in range(n)) for s_ in states]); g = np.array([sum(ps[k, s_[k]] for k in range(n)) for s_ in states])
            df = np.array([max(abs(ph[k, a]-ph[k, b])/abs(a-b) for a in range(q) for b in range(q) if a != b) for k in range(n)])
            dg = np.array([max(abs(ps[k, a]-ps[k, b])/abs(a-b) for a in range(q) for b in range(q) if a != b) for k in range(n)])
            cov = (mu*f*g).sum()-(mu*f).sum()*(mu*g).sum()
            worst = max(worst, abs(cov)/(D**2*df @ M @ dg))
        return alpha, worst
    exp_run = {(4, 3, 0.3): 0.04058579503278953, (5, 3, 0.5): 0.02945825058404763, (4, 4, 0.4): 0.00508942173054685,
               (5, 2, 0.6): 0.12626222919506613, (6, 3, 0.35): 0.03997886304645346}
    cfgs = list(exp_run) if full else [(4, 3, 0.3), (5, 3, 0.5), (4, 4, 0.4), (5, 2, 0.6)]
    allok = True
    for cfg in cfgs:
        al, wv = run(*cfg)
        allok &= wv <= 1
        check("S5", f"5.8-{cfg[0]}{cfg[1]}-{cfg[2]}", f"consistency (not used in proofs): covariance estimate on exact system {cfg}, max|Cov|/bound (alpha={al:.4f})", "REG",
              abs(wv - exp_run[cfg]) < 1e-9 and wv <= 1, f"{wv:.12f}", f"{exp_run[cfg]:.12f}")
    exp_adv = {(5, 2, 0.85): (0.9354090706030991, 0.06432134075289173), (5, 2, 1.0): (0.9640275800758171, 0.03934365329862564),
               (4, 3, 0.9): (0.9887840759510775, 0.007273115886897108), (6, 2, 0.9): (0.9468060128462686, 0.06130418086165018)}
    advs = list(exp_adv) if full else [(5, 2, 0.85), (4, 3, 0.9)]
    for cfg in advs:
        states, mu, C, H, cond, W1 = build(*cfg); n, q = cfg[0], cfg[1]; D = q-1
        alpha = C.sum(1).max(); M = np.linalg.inv(np.eye(n)-C); X = np.array(states, float); wv = 0
        for i in range(n):
            for j in range(n):
                cov = (mu*X[:, i]*X[:, j]).sum()-(mu*X[:, i]).sum()*(mu*X[:, j]).sum(); wv = max(wv, abs(cov)/(D**2*M[i, j]))
        ea, ew = exp_adv[cfg]
        check("S5", f"5.9-{cfg[0]}{cfg[1]}-{cfg[2]}", f"consistency (not used in proofs): near-critical exact system {cfg}", "REG",
              abs(alpha-ea) < 1e-9 and abs(wv-ew) < 1e-9 and wv <= 1, f"alpha={alpha:.10f} ratio={wv:.10f}")
    # step-level checks of the lemma's proof on one exact system
    from scipy.linalg import expm
    rng11 = np.random.default_rng(11)
    n, q, beta = 4, 3, 0.9
    states = list(itertools.product(range(q), repeat=n)); Ns = len(states); ix = {s_: i for i, s_ in enumerate(states)}
    def H(s_): return beta*sum(np.cos(2*np.pi*(s_[i]-s_[(i+1) % n])/q) for i in range(n))
    w = np.array([np.exp(H(s_)) for s_ in states]); mu = w/w.sum()
    Lg = np.zeros((Ns, Ns))
    for a_, s_ in enumerate(states):
        for i in range(n):
            v = np.array([np.exp(H(s_[:i]+(x,)+s_[i+1:])) for x in range(q)]); v /= v.sum()
            for x in range(q): Lg[a_, ix[s_[:i]+(x,)+s_[i+1:]]] += v[x]
            Lg[a_, a_] -= 1
    rev = np.abs(np.diag(mu) @ Lg - (np.diag(mu) @ Lg).T).max()
    check("S5", "5.10", "consistency: heat-bath generator is mu-reversible (proved: tower property)", "EXACT", rev < 1e-15, f"{rev:.2e}")
    f = rng11.normal(size=Ns); g = rng11.normal(size=Ns)
    cov_exact = (mu*f*g).sum()-(mu*f).sum()*(mu*g).sum()
    # exact spectral evaluation: S = D^{1/2} L D^{-1/2} symmetric; int_0^inf e^{t lam} dt = -1/lam for lam < 0
    Dh = np.sqrt(mu); Ssym = (Dh[:, None]*Lg)/Dh[None, :]; Ssym = (Ssym+Ssym.T)/2
    lam, V = np.linalg.eigh(Ssym)
    wts = np.array([0.0 if abs(l_) < 1e-12 else 1.0 for l_ in lam])      # -lam * (-1/lam) = 1 on lam != 0
    Kint = (V*wts) @ V.T                                                  # = -D^{1/2} (int L e^{tL} dt) D^{-1/2}
    cov_spec = (mu*g*((Kint @ (Dh*f))/Dh)).sum()
    rel_s = abs(cov_exact-cov_spec)/abs(cov_exact)
    check("S5", "5.11", "consistency: Cov = -int E[g L P_t f] dt, exact spectral integration (proved: Prop 2.5 step c)", "EXACT", rel_s < 1e-10, f"rel err {rel_s:.2e}")
    if full:
        ts = np.linspace(0, 60, 6001)
        vals = [-(mu*g*(Lg @ (expm(t*Lg) @ f))).sum() for t in ts]
        cov_semi = np.trapezoid(vals, ts) if hasattr(np, 'trapezoid') else np.trapz(vals, ts)
        rel = abs(cov_exact-cov_semi)/abs(cov_exact)
        check("S5", "5.11b", "same identity by time quadrature (6001 nodes, as in check123.py)", "NUM", rel < 1e-5, f"rel err {rel:.2e}")
    def cond(i, s_):
        v = np.array([np.exp(H(s_[:i]+(x,)+s_[i+1:])) for x in range(q)]); return v/v.sum()
    def W1(p, r_): return np.abs(np.cumsum(p-r_)[:-1]).sum()
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j: C[i, j] = max(W1(cond(i, s_), cond(i, s_[:j]+(bb,)+s_[j+1:]))/abs(s_[j]-bb) for s_ in states for bb in range(q) if bb != s_[j])
    def delta(h):
        d = np.zeros(n)
        for a_, s_ in enumerate(states):
            for j in range(n):
                for bb in range(q):
                    if bb != s_[j]: d[j] = max(d[j], abs(h[a_]-h[ix[s_[:j]+(bb,)+s_[j+1:]]])/abs(s_[j]-bb))
        return d
    worst = 0
    for t in ([0.5, 1, 2, 5, 10] if full else [1, 5]):
        Pt = expm(t*Lg); M = expm(-t*(np.eye(n)-C))
        for _ in range(20 if full else 5):
            ff = np.array([sum(rng11.normal()*s_[k] + rng11.normal()*np.sin(s_[k]) for k in range(n)) for s_ in states])
            worst = max(worst, (delta(Pt @ ff)/np.maximum(delta(ff) @ M, 1e-12)).max())
    check("S5", "5.12", "consistency: propagation bound (proved: Lemma 2.4/2.5), ratio <= 1", "NUM", worst <= 1, f"{worst:.4f}")
    check("S5", "5.13", "consistency: e^{-t(I-C)} entrywise nonnegative (proved: Metzler matrix)", "NUM", expm(-3*(np.eye(n)-C)).min() > 0, f"{expm(-3*(np.eye(n)-C)).min():.4f}")


# ==========================================================================================================
# S6 — sharpness and block criteria (Paper 2 §5)
# ==========================================================================================================


    tot, dist, mult = _block_incidences()
    check("S5", "5.20", "plaquette block: 60 exterior incidences, 44 distinct links (28 single, 16 double) [audit]", "EXACT",
          (tot, dist, mult[1], mult[2]) == (60, 44, 28, 16), f"{tot}, {dist}, {dict(mult)}")
    mp.dps = 30
    aB = lambda b: I(2, b)/I(1, b)
    prov = mpm.findroot(lambda b: b/4*(15 + 7*aB(b)) - 1, 0.26)
    cond = mpm.findroot(lambda b: 15*b*(1 + aB(b))/4 - 1, 0.25)
    check("S5", "5.21", "Cor. 5.5: proved block ceiling 0.25887 (28 single @ 1/4+a/4, 16 double @ 1/2); conditional 0.25096", "EXACT",
          abs(prov - mpf('0.2588701356256244')) < 1e-15 and abs(cond - mpf('0.2509623052607262')) < 1e-15, f"{mpm.nstr(prov, 16)}, {mpm.nstr(cond, 16)}")




def _block_incidences():
    from collections import Counter
    d = 4
    def plaq(l):
        x, mu = l; out = []
        for nu in range(d):
            if nu == mu: continue
            for sg in (1, -1):
                b = list(x)
                if sg == -1: b[nu] -= 1
                b = tuple(b)
                out.append(frozenset([(b, mu), (b, nu), (tuple(b[i] + (i == mu) for i in range(d)), nu), (tuple(b[i] + (i == nu) for i in range(d)), mu)]))
        return out
    x0 = (5, 5, 5, 5); p0 = frozenset([(x0, 0), (x0, 1), ((6, 5, 5, 5), 1), ((5, 6, 5, 5), 0)])
    inc = Counter()
    for l in p0:
        for pp in plaq(l):
            if pp != p0:
                for k in pp:
                    if k not in p0: inc[k] += 1
    return sum(inc.values()), len(inc), Counter(inc.values())




def S6(full):
    mp.dps = 50  # section-local precision (no inherited state)
    print("\nS6  Sharpness and block criteria")
    mp.dps = 25
    def Lavg(r0, d, th):
        def L(t):
            ex = r0+t*d*mpm.cos(th); ey = t*d*mpm.sin(th); r = mpm.sqrt(ex**2+ey**2)
            if r < 1e-9: return mpf(1)/4
            c = (ex*mpm.cos(th)+ey*mpm.sin(th))/r
            return mpm.sqrt(c**2*A_bound(r)+(1-c**2)*B_bound(r))/2
        return mpm.quad(L, [0, 1])
    bW = mpf(2)/9
    r0s = [0, bW, 2*bW, 3*bW, 5*bW] if full else [0, bW]
    ds = [mpf('0.1'), bW, 2*bW] if full else [mpf('0.1'), bW]
    ths = [0, mpm.pi/4, mpm.pi/2, 3*mpm.pi/4, mpm.pi] if full else [0, mpm.pi/2]
    worst = max(Lavg(r0, d, th) for r0 in r0s for d in ds for th in ths)
    if full:
        check("S6", "6.1", "lever 1: sup averaged L at beta_W=2/9 -> implied threshold 0.2222684", "REG",
              mpm.nstr(1/(18*worst), 7) == '0.2222684', s(1/(18*worst), 16), "0.2222683841613224")
    else:
        check("S6", "6.1", "lever 1 (subset): averaged L < 1/4, threshold gain < 1e-4 over 2/9", "NUM",
              worst < mpf(1)/4 and 1/(18*worst) - bW < mpf('1e-4'), s(1/(18*worst), 12))
    mp.dps = 30
    geo = mpm.quad(lambda th: th*mpm.cos(th)*mpm.sin(th)**2, [0, mpm.pi])/(mpm.pi/2)
    check("S6", "6.2", "geodesic metric: Cov(theta, cos theta) = -8/(9 pi) and 8/(9 pi) > 1/4", "EXACT",
          close(geo, -8/(9*mpm.pi), 1e-25) and 8/(9*mpm.pi) > mpf(1)/4, s(geo, 15))
    check("S6", "6.3", "inner-Dobrushin identity: (n_out b/4)/(1 - n_in b/4) = 1 at b = 2/9 for every n_in", "EXACT",
          all((Fr(18-k)*Fr(2, 9)/4)/(1-Fr(k)*Fr(2, 9)/4) == 1 for k in range(0, 18)))
    mp.dps = 40
    a = lambda b: I(2, b)/I(1, b)
    LB = lambda b: mpf(1)/4 + a(b)/4
    UB = lambda b: mpf(1)/4 + a(b)/4 + b*a(b)/16
    b0 = mpf('0.3')
    check("S6", "6.4", "plaquette block at beta_W=0.3: a, lower and upper bounds on L_V(0)", "REG",
          mpm.nstr(a(b0), 19) == '0.07472032259655370244' and mpm.nstr(LB(b0), 20) == '0.26868008064913842561'
          and mpm.nstr(UB(b0), 20) == '0.27008108669782380753', f"{s(a(b0))} [{s(LB(b0))}, {s(UB(b0))}]")
    check("S6", "6.5", "inner-Dobrushin value at 0.3: (1/4)/(1-3*0.3/4) = 0.32258...", "EXACT", close((mpf(1)/4)/(1-3*b0/4), mpf(10)/31, 1e-35))
    bup = mpm.findroot(lambda b: 15*b*LB(b) - 1, 0.25); blo = mpm.findroot(lambda b: 15*b*UB(b) - 1, 0.25)
    check("S6", "6.6", "block ceiling 15 b (1/4 + a/4) = 1", "REG", s(bup, 30).startswith('0.2509623052607262413'), s(bup, 22))
    check("S6", "6.7", "zero-field lower end 15 b (1/4 + a/4 + b a/16) = 1", "REG", s(blo, 30).startswith('0.2500952152983506551'), s(blo, 22))
    g1 = 100*(blo/bW-1); g2 = 100*(bup/bW-1)
    check("S6", "6.8", "gains over 2/9: 12.54% .. 12.93%", "REG", mpm.nstr(g1, 4) == '12.54' and mpm.nstr(g2, 4) == '12.93', f"{s(g1, 8)} .. {s(g2, 8)}")
    rng = np.random.default_rng(29)
    def haar(M): v = rng.normal(size=(M, 4)); return v/np.linalg.norm(v, axis=1, keepdims=True)
    def vmf(eta):
        M = len(eta); k = np.linalg.norm(eta, axis=1); x = np.empty(M); todo = np.arange(M)
        while len(todo):
            kk = k[todo]; u = rng.random(len(todo)); xs = 1 + np.log(u + (1-u)*np.exp(-2*kk))/kk
            okk = rng.random(len(todo)) < np.sqrt(1 - xs**2); x[todo[okk]] = xs[okk]; todo = todo[~okk]
        e = eta/k[:, None]; p = rng.normal(size=(M, 4)); p -= (p*e).sum(1, keepdims=True)*e
        p /= np.linalg.norm(p, axis=1, keepdims=True); return x[:, None]*e + np.sqrt(1-x**2)[:, None]*p
    Nmc = 1_000_000 if full else 200_000; acc = []
    for _ in range(5):
        P = haar(Nmc); qv = vmf(0.3*P)
        acc.append((np.mean(qv[:, 0]**2)-qv[:, 0].mean()**2, np.mean(P[:, 0]*qv[:, 0])-P[:, 0].mean()*qv[:, 0].mean()))
    acc = np.array(acc); m = acc.mean(0); se = acc.std(0, ddof=1)/np.sqrt(5)
    ex2 = float(a(b0)/4)
    check("S6", "6.9", "MC pair model: Cov(q1,q1)=1/4 and Cov(P1,q1)=a/4 within 5 s.e.", "MC",
          abs(m[0]-0.25) < 5*se[0]+1e-4 and abs(m[1]-ex2) < 5*se[1]+1e-4, f"{m[0]:.5f}±{se[0]:.5f}, {m[1]:.5f}±{se[1]:.5f} (exact {ex2:.5f})")


# ==========================================================================================================
# S7 — Track 4 (Paper 2 §4)
# ==========================================================================================================
def S7(full):
    mp.dps = 50  # section-local precision (no inherited state)
    print("\nS7  Track 4: transfer matrix")
    mp.dps = 40
    worst = mpf(0); worstc = mpf(0); pos = True
    for b in [mpf('0.1'), mpf(2)/9, mpf('0.6')]:
        for twoj in range(0, 6):
            nn = twoj+1
            cq = 2/mpm.pi*mpm.quad(lambda t: mpm.exp(b*mpm.cos(t))*mpm.sin(nn*t)*mpm.sin(t), [0, mpm.pi])
            cf = 2*nn*I(nn, b)/b; worst = max(worst, abs(cq-cf)); pos &= cf > 0
        sm = sum(2*(k+1)*I(k+1, b)/b*(k+1) for k in range(0, 60)); worstc = max(worstc, abs(sm-mpm.exp(b)))
    check("S7", "7.1", "character coefficients c_j = 2(2j+1) I_{2j+1}(b)/b (quadrature)", "EXACT", worst < mpf(10)**-35, s(worst, 3))
    check("S7", "7.2", "c_j > 0 (T >= 0, injectivity on H_phys)", "EXACT", pos)
    check("S7", "7.3", "completeness sum_j c_j d_j = e^b", "EXACT", worstc < mpf(10)**-35, s(worstc, 3))
    okg = True; okr = True
    for k in range(1, 67):
        b = mpf(k)/100
        okg &= -2*mpm.log(I(2, b)/I(1, b)) >= -mpm.log(3*b/2); okr &= I(2, b)/I(1, b) <= b/4
    check("S7", "7.4", "2D: exact gap -2 ln(I2/I1) >= bound -ln(3b/2) on (0, 0.66]; I2/I1 <= b/4", "NUM", okg and okr)
    check("S7", "7.5", "at beta_W=0.2: m >= -ln(0.9) = 0.1054; strong-coupling glueball -4 ln(I2/I1) = 11.99", "REG",
          mpm.nstr(-mpm.log(mpf('0.9')), 4) == '0.1054' and mpm.nstr(-4*mpm.log(a_ratio(mpf('0.2'))), 4) == '11.99')
    rows = [(bv, -mpm.log(9*mpf(bv)/2)) for bv in ['0.05', '0.10', '0.15', '0.20', '0.22']]
    check("S7", "7.6", "mass bound m >= -log(9 beta_W/2) table", "INFO", None, "; ".join(f"{b}:{s(v, 8)}" for b, v in rows))


# ==========================================================================================================
# S8 — Track 3: SU(N) zero-field linear response (MC)
# ==========================================================================================================
def _rp_exact():
    """Exact check of Paper 2 Lemma T7 (i),(ii) conventions: 2D Z2 gauge theory, torus Ls=2, Nt=4, full enumeration."""
    import itertools
    Ls, Nt, beta = 2, 4, 0.7
    links = [('s', x, tt) for tt in range(Nt) for x in range(Ls)] + [('t', x, tt) for tt in range(Nt) for x in range(Ls)]
    idx = {l: i for i, l in enumerate(links)}; nL = len(links)
    plaq = [(idx[('s',x,tt)], idx[('t',(x+1)%Ls,tt)], idx[('s',x,(tt+1)%Nt)], idx[('t',x,tt)]) for tt in range(Nt) for x in range(Ls)]
    confs = np.array(list(itertools.product([1,-1], repeat=nL)), dtype=np.int8)
    w = np.exp(beta*sum(np.prod(confs[:, list(q)], axis=1) for q in plaq)); w /= w.sum()
    def refl(sig):
        perm = np.empty(nL, int)
        for l in links:
            kind, x, tt = l
            if kind == 's': perm[idx[l]] = idx[('s', x, sig(tt) % Nt)]
            else:
                a, b = sig(tt) % Nt, sig(tt+1) % Nt
                perm[idx[l]] = idx[('t', x, a if (a+1) % Nt == b else b)]
        return perm
    th, thp = refl(lambda s_: -s_), refl(lambda s_: 1-s_)
    def mineig(vars_, perm):
        vs = [idx[v] for v in vars_]
        mons = [S for r in range(len(vs)+1) for S in itertools.combinations(vs, r)]
        Fv = np.stack([np.prod(confs[:, list(S)], axis=1) if S else np.ones(len(confs)) for S in mons], 1).astype(np.float32)
        Fr = np.stack([np.prod(confs[:, [perm[i] for i in S]], axis=1) if S else np.ones(len(confs)) for S in mons], 1).astype(np.float32)
        M = ((Fr*w[:, None].astype(np.float32)).T @ Fv).astype(float)
        return float(np.linalg.eigvalsh((M+M.T)/2).min())
    k = Nt//2
    good_i  = [('s',x,tt) for tt in (0, 1) for x in range(Ls)] + [('t',x,0) for x in range(Ls)] + [('s',x,k) for x in range(Ls)]
    good_ii = [('s',x,tt) for tt in range(1, k+1) for x in range(Ls)] + [('t',x,tt) for tt in range(1, k) for x in range(Ls)]
    bad_i   = [('s',x,1) for x in range(Ls)] + [('t',x,0) for x in range(Ls)] + [('t',x,Nt-1) for x in range(Ls)]
    bad_ii  = [('s',x,tt) for tt in (1, 2, 3) for x in range(Ls)]
    return mineig(good_i, th), mineig(good_ii, thp), mineig(bad_i, th), mineig(bad_ii, thp)


def S8(full):
    mp.dps = 50  # section-local precision (no inherited state)
    print("\nS8  Track 3: SU(N) zero-field linear response N*L_N")
    rng = np.random.default_rng(7)
    def haar_su(N, M):
        Z = (rng.normal(size=(M, N, N))+1j*rng.normal(size=(M, N, N)))/np.sqrt(2)
        Q, Rr = np.linalg.qr(Z); d = np.diagonal(Rr, axis1=1, axis2=2); Q = Q*(d/np.abs(d))[:, None, :]
        det = np.linalg.det(Q); Q = Q.copy(); Q[:, :, 0] *= (np.conj(det)/np.abs(det))[:, None]; return Q
    M = 400_000 if full else 100_000
    for N, expv in [(2, 1.0), (3, 0.5), (4, 0.5)]:
        U = haar_su(N, M)
        X = np.concatenate([U.real.reshape(M, -1), U.imag.reshape(M, -1)], 1)
        Xc = X - X.mean(0); lam = np.linalg.eigvalsh(Xc.T @ Xc/M).max()
        tol = 3*np.sqrt(2*N*N/M)           # sampling scale of the top eigenvalue of a (2N^2)-dim covariance
        check("S8", f"8.1-N{N}", f"Haar SU({N}): N * lambda_max(Cov of real coordinates) = {expv} (tol {tol:.3f}; estimator biased upward)", "MC",
              abs(N*lam - expv) < tol, f"{N*lam:.4f}")
        # exact covariance (Paper 2, Prop. 6.1): I/(2N) for N>=3; for N=2: (1/4)[[I+EE, 0],[0, I-EE]] with EE = eps (x) eps
        if N >= 3:
            Cex = np.eye(2*N*N)/(2*N)
        else:
            eps = np.array([[0, 1], [-1, 0.]]); EE = np.kron(eps, eps)
            Cex = np.block([[0.25*(np.eye(4)+EE), np.zeros((4, 4))], [np.zeros((4, 4)), 0.25*(np.eye(4)-EE)]])
        dev = np.abs(Xc.T @ Xc/M - Cex).max(); lam_ex = np.linalg.eigvalsh(Cex).max()
        check("S8", f"8.0-N{N}", f"exact Haar covariance (Prop 6.1): N*lambda_max = {N*lam_ex:.1f}; MC entrywise deviation within 6/sqrt(M)", "EXACT",
              abs(N*lam_ex - expv) < 1e-12 and dev < 6/np.sqrt(M), f"dev={dev:.5f}")
        Uf = U.reshape(M, -1); nc = np.abs(Uf.T @ Uf/M).max()        # max |E[U_ij U_kl]| (non-conjugate)
        if N >= 3:
            check("S8", f"8.2-N{N}", f"centre invariance: max|E[U_ij U_kl]| = 0 for SU({N}) (within 6/sqrt(M))", "MC", nc < 6/np.sqrt(M), f"{nc:.5f}")
        else:
            check("S8", "8.2-N2", "SU(2) has no such constraint: max|E[U_ij U_kl]| = 1/2 (E[U11 U22] = E|a|^2)", "MC", abs(nc-0.5) < 0.01, f"{nc:.4f}")


# ==========================================================================================================
# S9 — Track 5 specification v0.1
# ==========================================================================================================
    e1, e2, n1, n2 = _rp_exact()
    check("S7", "7.10", "Paper 2 Lemma T7: site- and link-plane RP Gram matrices PSD (exact Z2 enumeration); negative controls fail", "EXACT",
          e1 > -1e-5 and e2 > -1e-5 and n1 < -0.5 and n2 < -0.5, f"min eig (i) {e1:.1e}, (ii) {e2:.1e}; controls {n1:.2f}, {n2:.2f}")




def S9(full):
    mp.dps = 50  # section-local precision (no inherited state)
    print("\nS9  Track 5: endpoint lemma ingredients, calibration, 2D prototype")
    mp.dps = 30
    q_i = np.array([0, 1, 0, 0.]); q_j = np.array([0, 0, 1, 0.])
    def qmul(a, b):
        w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
        return np.array([w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2, w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2])
    comm = np.linalg.norm(qmul(q_i, q_j)-qmul(q_j, q_i))
    check("S9", "9.1", "|[Y,Z]| = 2|Y||Z| for orthonormal imaginary unit quaternions (unit S^3)", "EXACT", abs(comm-2) < 1e-15, comm)
    w = lambda t: 2/mpm.pi*mpm.sqrt(1-t*t)
    var = mpm.quad(lambda t: t*t*w(t), [-1, 1]); grad = mpm.quad(lambda t: (1-t*t)*w(t), [-1, 1])
    check("S9", "9.2", "Poincare on unit S^3 with lambda_1 = 3 is attained by n1: Var = (1/3)E|grad n1|^2", "EXACT", close(var, grad/3, 1e-25), f"{s(var, 10)} = {s(grad/3, 10)}")
    ratio = max(th/(2*mpm.sin(th/2)) for th in [mpm.pi*k/1000 for k in range(1, 1001)])
    check("S9", "9.3", "geodesic <= (pi/2) chordal on S^3 (max ratio at antipodes)", "EXACT", close(ratio, mpm.pi/2, 1e-25), s(ratio, 15))
    x = mpm.findroot(lambda b: (mpm.pi/6)*mpm.exp(12*b)*6*3*2*b - 1, 0.03)
    check("S9", "9.4", "Lemma A calibration on pure Wilson: 6 pi b e^{12 b} = 1", "REG", mpm.nstr(x, 10) == '0.03489948577', s(x, 12), "0.03489948577")
    check("S9", "9.5", "ratio of sharp 2/9 to Lemma-A threshold", "INFO", None, s((mpf(2)/9)/x, 5))
    # 2D prototype with analytic derivatives of the zonal function Phi = log w
    mp.dps = 30
    ngrid = 400
    ths = [mpm.pi*(i+mpf(1)/2)/ngrid for i in range(ngrid)]
    def alpha_from_coef(coef):
        s0 = mpf(0); g_ = mpf(0); h_ = mpf(0)
        for th in ths:
            st, ct = mpm.sin(th), mpm.cos(th); W = W1 = W2 = mpf(0)
            for k, c in enumerate(coef):
                mm = k+1; smt, cmt = mpm.sin(mm*th), mpm.cos(mm*th)
                Nn = mm*cmt*st - smt*ct
                W += c*smt/st; W1 += c*Nn/st**2; W2 += c*((1-mm*mm)*smt*st**2 - 2*ct*Nn)/st**3
            P0 = mpm.log(W); P1 = W1/W; P2 = (W2*W - W1**2)/W**2
            s0 = max(s0, abs(P0)); g_ = max(g_, abs(P1)); h_ = max(h_, max(abs(P2), abs(P1*ct/st)))
        return (mpm.pi/6)*mpm.exp(4*s0)*6*(g_+h_)
    def coef_lattice(beta, B2, kmax=60):
        return [(k+1)*(I(k+1, beta)/I(1, beta))**B2 for k in range(kmax)]
    def coef_heat(l, kmax=60):
        return [(k+1)*mpm.exp(-l*l*k*(k+2)/8) for k in range(kmax)]
    exp_lat = {('3.5', '0.5'): '0.257826', ('3.5', '0.25'): '0.29303', ('3.5', '0.125'): '0.30256',
               ('3.0', '0.5'): '1.38233', ('3.0', '0.25'): '1.57717', ('3.0', '0.125'): '1.63059'}
    keys = list(exp_lat) if full else [('3.5', '0.5'), ('3.5', '0.25')]
    for (lv, av) in keys:
        l, a = mpf(lv), mpf(av)
        al = alpha_from_coef(coef_lattice(4/(a*a), (l/a)**2))
        check("S9", f"9.6-{lv}-{av}", f"2D exact decimation: alpha at l={lv}, a={av} (g=1)", "REG",
              mpm.nstr(al, 6) == exp_lat[(lv, av)] or mpm.nstr(al, 5) == exp_lat[(lv, av)], mpm.nstr(al, 8), exp_lat[(lv, av)])
    for lv, ev in [('3.5', '0.30580231'), ('3.0', '1.6488293')]:
        al = alpha_from_coef(coef_heat(mpf(lv)))
        check("S9", f"9.7-{lv}", f"continuum heat-kernel alpha at l={lv}", "REG", mpm.nstr(al, 8) == ev, mpm.nstr(al, 10), ev)
    if full:
        lstar = mpm.findroot(lambda l: alpha_from_coef(coef_heat(l)) - 1, mpf('3.14'))
        check("S9", "9.8", "critical physical scale l* (alpha_cont = 1)", "REG", mpm.nstr(lstar, 8) == '3.1374032', s(lstar, 10), "3.1374032")
    else:
        a1 = alpha_from_coef(coef_heat(mpf('3.137'))); a2 = alpha_from_coef(coef_heat(mpf('3.138')))
        check("S9", "9.8", "critical physical scale l* in (3.137, 3.138) (bracket)", "NUM", a1 > 1 > a2, f"{s(a1, 8)} > 1 > {s(a2, 8)}")


# ==========================================================================================================
# S10 — asymptotic scaling constants (SU(2))
# ==========================================================================================================
def S10(full):
    mp.dps = 50  # section-local precision (no inherited state)
    print("\nS10 Asymptotic-scaling constants (SU(2))")
    Nc = 2
    # b0 = 11N/(3*16 pi^2), b1 = 34N^2/(3*(16 pi^2)^2);  b1/(2 b0^2) = 51/121 exactly (pi cancels)
    ratio = Fr(34*Nc**2, 3)/(2*Fr(11*Nc, 3)**2)
    check("S10", "10.1", "b1/(2 b0^2) = 51/121 (exact, pi-independent)", "EXACT", ratio == Fr(51, 121), str(ratio))
    mp.dps = 30
    b0 = mpf(11)*Nc/(3*16*mpm.pi**2)
    check("S10", "10.2", "1/(8 b0) = 3 pi^2/11 (a Lambda ~ exp(-(3pi^2/11) beta_W))", "EXACT", close(1/(8*b0), 3*mpm.pi**2/11, 1e-25), s(1/(8*b0), 10))
    check("S10", "10.3", "b0 value", "REG", mpm.nstr(b0, 8) == '0.046438876', s(b0, 10))


# ==========================================================================================================
SECTIONS = dict(S1=S1, S2=S2, S3=S3, S4=S4, S5=S5, S6=S6, S7=S7, S8=S8, S9=S9, S10=S10)


def main():
    ap = argparse.ArgumentParser(description="Reproduce all SI Yang-Mills computations")
    ap.add_argument("--full", action="store_true", help="use the exact grids/sizes of the papers (slow)")
    ap.add_argument("--sections", default=",".join(SECTIONS), help="comma-separated subset, e.g. S1,S5")
    ap.add_argument("--json", default=None, help="write a JSON report to this path")
    args = ap.parse_args()
    print(f"SI Yang-Mills reproduction — mode: {'FULL' if args.full else 'QUICK'}  (numpy {np.__version__}, mpmath {mpm.__version__})")
    t0 = time.time()
    for name in args.sections.split(","):
        name = name.strip(); ts = time.time()
        SECTIONS[name](args.full)
        print(f"      [{name} done in {time.time()-ts:.1f}s]", flush=True)
    npass = sum(r["status"] == "PASS" for r in RESULTS); nfail = sum(r["status"] == "FAIL" for r in RESULTS)
    ninfo = sum(r["status"] == "INFO" for r in RESULTS)
    print(f"\nSUMMARY: {npass} PASS, {nfail} FAIL, {ninfo} INFO   ({time.time()-t0:.1f}s total)")
    for r in RESULTS:
        if r["status"] == "FAIL": print(f"  FAIL {r['section']} {r['id']}: {r['desc']}  value={r['value']} expected={r['expected']}")
    if args.json:
        with open(args.json, "w") as fh:
            json.dump(dict(mode="full" if args.full else "quick", results=RESULTS), fh, indent=1)
    sys.exit(1 if nfail else 0)


if __name__ == "__main__":
    main()