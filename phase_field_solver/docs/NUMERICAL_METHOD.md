# Numerical method and verification contract

## 1. Problem definition

Let both coordinates theta and zeta have period 2 pi. A fundamental axial cell of a corrugated tube is represented locally by

$$
X(\theta,\zeta)=\big(R(\theta,\zeta)\cos\theta,\,
R(\theta,\zeta)\sin\theta,\,a\zeta\big),
\qquad
R=R_0+A\sin(n\theta+\delta_\theta)\cos(m\zeta+\delta_\zeta).
$$

The identification in zeta is by an ambient translation through axial distance 2 pi a. Thus the metric and curvature fields are periodic, while X itself changes by that translation. The intrinsic periodic quotient has torus topology. No false assertion of a periodic Euclidean axial coordinate is needed.

The constraints R0 > |A| and a > 0 keep the radius positive and the metric nonsingular. The code imposes n,m as positive integers. A = 0 recovers a circular cylinder. All quantities are in a consistent user chosen system of units; the code does not infer or convert units.

Write the induced spatial metric as gamma_ab and set

$$
ds^2=-N(\theta,\zeta)^2dt^2+\gamma_{ab}dx^a dx^b.
$$

The shift is zero. The lapse is fixed:

$$
N=N_0\left[1+\epsilon_N
\cos(n_N\theta+\eta_\theta)\cos(m_N\zeta+\eta_\zeta)\right],
\quad N_0>0,\quad |\epsilon_N|<1.
$$

The continuum field is a single real scalar. Define

$$
U=U_c+U_a\sin(n_U\theta+\xi_\theta)\cos(m_U\zeta+\xi_\zeta)
+\alpha_H H^2+\alpha_K K_G,\qquad c=m_0^2+2U.
$$

The potential energy density is c phi²/2 + lambda phi⁴/4. The implementation allows negative c, including negative mass2, but requires lambda >= 0. The symbols mass2 and m0² denote a signed quadratic coefficient; a negative value is intentionally allowed despite the conventional squared notation.

The undriven action is

$$
S=\int dt\,d\theta\,d\zeta\,N\sqrt{\gamma}
\left[
\frac{\phi_t^2}{2N^2}
-\frac12\gamma^{ab}\partial_a\phi\partial_b\phi
-\frac12c\phi^2-\frac{\lambda}{4}\phi^4
\right].
$$

Here sqrt(gamma) is the positive area density, not a coordinate average. Static geometry and lapse are assumptions in the variation. The resulting positive time equation, with optional source s and phenomenological coordinate time damping beta, is

$$
\frac{1}{N^2}(\phi_{tt}+\beta\phi_t)
-\frac{1}{N\sqrt{\gamma}}
\partial_a\left(N\sqrt{\gamma}\gamma^{ab}\partial_b\phi\right)
+c\phi+\lambda\phi^3=s.
$$

Multiplication by N² shows that the source produces acceleration N²s. Damping beta is spatially uniform per unit coordinate time in this implementation. It is not automatically a locally prescribed proper time damping law. A source written on the right of a differently signed covariant Klein–Gordon equation must be translated to this convention before comparison.

## 2. Geometry without finite difference curvature

Let Rt, Rz and their second derivatives denote analytical derivatives. The first fundamental form is

$$
E=R^2+R_\theta^2,\quad F=R_\theta R_\zeta,\quad
G=a^2+R_\zeta^2,
$$

$$
D=EG-F^2=a^2(R^2+R_\theta^2)+R^2R_\zeta^2>0,\quad
\sqrt{\gamma}=\sqrt D,
$$

$$
\gamma^{\theta\theta}=G/D,\quad
\gamma^{\theta\zeta}=-F/D,\quad
\gamma^{\zeta\zeta}=E/D.
$$

For the outward normal and second fundamental form convention b_ab = -normal dot X_ab,

$$
b_{\theta\theta}=\frac{a(R^2+2R_\theta^2-RR_{\theta\theta})}{\sqrt D},
\quad
b_{\theta\zeta}=\frac{a(R_\theta R_\zeta-RR_{\theta\zeta})}{\sqrt D},
\quad
b_{\zeta\zeta}=-\frac{aR R_{\zeta\zeta}}{\sqrt D}.
$$

Then

$$
H=\frac{G b_{\theta\theta}-2F b_{\theta\zeta}+E b_{\zeta\zeta}}{2D},
\qquad
K_G=\frac{b_{\theta\theta}b_{\zeta\zeta}-b_{\theta\zeta}^2}{D}.
$$

The cylinder has H = 1/(2R0) and KG = 0 under this convention. H² and KG are independent of reversal of the normal. The identity H² - KG = (kappa1 - kappa2)²/4 is nonnegative at every point of a regular surface.

The code computes these formulas directly from the sinusoidal radius, avoiding a finite difference curvature stencil. Verification compares b_ab with independently constructed embedding tangent vectors, their cross product normal, and second embedding derivatives. It also checks the integral of KG over a periodic cell against the zero Euler characteristic prediction. These are complementary checks: an integrated identity alone would not establish pointwise geometry accuracy.

## 3. Trial space and quadrature

In each coordinate the real basis is

$$
b_0(x)=1,\quad b_{2k-1}(x)=\sqrt2\cos(kx),\quad
b_{2k}(x)=\sqrt2\sin(kx),\quad 1\le k\le K.
$$

It is orthonormal with respect to the angular average (2 pi)^-1 integral, not the unnormalized integral. The tensor product spans every real trigonometric field with rectangular Fourier cutoffs Ktheta,Kzeta. Its dimension is

$$
d=(2K_\theta+1)(2K_\zeta+1),\qquad
\phi_h=\sum_{j=1}^d q_j b_j(\theta,\zeta).
$$

There is no removal of sine partners or duplicate eigenvalues. The real basis spans the same real field space as conjugate paired complex Fourier coefficients.

The uniform quadrature points exclude the endpoint and have cell weight w0 = (2 pi)²/(Qtheta Qzeta). Let B contain basis values and Dtheta,Dzeta their analytical derivatives. Grid points and coefficient tensor products are flattened in C order, with the zeta index varying fastest. This is why op.field returns shape (Qtheta,Qzeta).

Define diagonal quadrature weight arrays

$$
w_M=w_0\sqrt{\gamma}/N,\qquad
w_K=w_0N\sqrt{\gamma}.
$$

The real mass matrix is positive definite when the sampled basis has full rank because

$$
x^T Mx=\sum_g(w_M)_g(Bx)_g^2>0\quad(x\ne0).
$$

The required grid size makes the retained trigonometric columns distinct and independent. Positive radius and lapse make every mass weight positive.

### Cubic aliasing and variable coefficients

The implementation requires Qtheta > 4Ktheta and Qzeta > 4Kzeta. For constant weights, a cubic Galerkin force component is an integral of one test function times three trial functions. Its maximum Fourier degree is 4K in each coordinate. A periodic trapezoidal grid with Q > 4K integrates all those nonconstant modes to zero exactly in exact arithmetic. The same argument applies to the quartic energy.

This is not an exact alias elimination theorem for curved geometry. Factors such as sqrt(D), 1/N, and inverse metric coefficients generally have infinitely many Fourier modes. Their products with the retained basis have no finite bandwidth. Even a finite bandwidth nonconstant weight would require a correspondingly stronger total degree condition. The code's coefficient harmonic resolution checks are necessary input checks, not a proof of adequate quadrature for all products.

For analytic coefficients whose complex singularities stay sufficiently far from the real coordinates, periodic trapezoidal quadrature converges rapidly. Near radius or lapse degeneracy that convergence can deteriorate. Independent quadrature refinement remains compulsory for an accuracy claim. Increasing the trial cutoff at fixed inadequate quadrature does not fix an integration error.

## 4. Variational assembly

Periodic integration by parts gives the semidiscrete system

$$
M\ddot q+\beta M\dot q+Kq+
\lambda B^T[w_K\odot(Bq)^3]=f(t),
$$

with

$$
M=B^T\operatorname{diag}(w_M)B,
$$

$$
\begin{aligned}
K={}&D_\theta^T\operatorname{diag}(w_K\gamma^{\theta\theta})D_\theta
+D_\zeta^T\operatorname{diag}(w_K\gamma^{\zeta\zeta})D_\zeta\\
&+D_\theta^T\operatorname{diag}(w_K\gamma^{\theta\zeta})D_\zeta
+D_\zeta^T\operatorname{diag}(w_K\gamma^{\theta\zeta})D_\theta
+B^T\operatorname{diag}(w_Kc)B.
\end{aligned}
$$

The physical source samples give f = B^T(wK times s). No extra application of M belongs in that source covector. Projection of a sampled field g instead solves Mq = B^T(wM times g).

The formulas include the off diagonal metric terms, area density, lapse in the kinetic weight, lapse in the potential weight, and the factor 2 multiplying U. Omitting any of these changes the continuum model.

The matrices are checked for finite values and symmetry before final arithmetic symmetrization. Mass solves use a Cholesky factorization; an explicit matrix inverse is not formed. SciPy supplies the symmetric generalized eigensolver and Cholesky routines. Its generalized eigenproblem assumes a positive definite second matrix, a requirement ensured mathematically by the weights and checked numerically by factorization. See the official [eigh documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh.html) and [cho_factor documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.cho_factor.html).

The discrete potential and total energy are

$$
V_h(q)=\tfrac12q^TKq+\tfrac{\lambda}{4}\sum_g(w_K)_g(Bq)_g^4,
\qquad
E_h(q,v)=\tfrac12v^TMv+V_h(q).
$$

The force is exactly the derivative of this quadrature defined potential in real arithmetic. Its Hessian is

$$
H_h(q)=K+3\lambda B^T\operatorname{diag}(w_K(Bq)^2)B.
$$

Directional finite differences verify the gradient and Hessian implementation. This consistency is useful even before quadrature has converged: the finite system retains a coherent energy, though it may not yet accurately approximate the continuum energy.

## 5. Spectra, instabilities, and normalization

Linearization about zero solves Kv = nu Mv, with v_i^T M v_j = delta_ij. For a stationary background qstar replace K by Hh(qstar). In the undamped system, positive nu gives coordinate time frequency sqrt(nu), and negative nu gives exponential growth rate sqrt(-nu).

Uniformly replacing N by cN multiplies every squared frequency by c². With N = 1, a constant change in mass2 shifts each squared frequency by the same amount. The mass shift statement is not valid without qualification for spatially varying lapse, because the kinetic and potential weights differ.

For a flat cylinder with constant lapse N0 and constant c,

$$
\nu_{\ell p}=N_0^2\left(\ell^2/R_0^2+p^2/a^2+c\right).
$$

Every integer pair within the rectangular cutoff is counted. On any allowed curved surface with N = 1 and constant c, the constant function has eigenvalue c, since its spatial gradient vanishes. If the gradient energy is nonnegative, this is also the lowest eigenvalue.

A more sensitive lapse check uses a unit radius cylinder, c = 1/4, and N = 1 + epsilon cos(theta). In the zeta constant sector, psi = N^-1/2 satisfies

$$
-N\partial_\theta(N\partial_\theta\psi)+\tfrac14N^2\psi
=\tfrac14(1-\epsilon^2)\psi.
$$

To verify it, substitution gives the coefficient
N N''/2 - (N')²/4 + N²/4, which reduces to (1-epsilon²)/4. This positive eigenfunction is the ground state of the periodic scalar Sturm–Liouville operator. At epsilon = 1/5 the exact squared frequency is 6/25. A finite Fourier basis approximates psi rather than representing it exactly, so the executable test has a stated tolerance and a projected residual check.

For each numerical eigenpair the report records

$$
\rho_i=\frac{\|Hv_i-\nu_i Mv_i\|_2}
{(\|H\|_F+|\nu_i|\|M\|_F)\|v_i\|_2},
$$

and the maximum entrywise error in V^T M V - I. These are algebraic diagnostics. The zero classification threshold is a binary64 scale dependent heuristic, not a proven eigenvalue enclosure. Near a zero crossing, refine the basis and quadrature and inspect conditioning before classifying stability.

For a multiple or nearly multiple eigenvalue, individual eigenvectors can rotate inside the eigenspace. A comparison of individual coefficient vectors can therefore fail while the spectral subspaces agree. The current sweep reports sorted eigenvalues; it does not match eigenvector branches or compute subspace principal angles.

## 6. Time integration and energy accounting

With fixed M, the undamped unforced finite dimensional Hamiltonian has a quadratic kinetic term and a coordinate dependent potential. In canonical variables p = Mv, velocity Verlet is a symmetric second order symplectic splitting. That statement applies to the Hamiltonian finite system; damping destroys symplecticity.

For timestep h, the implementation composes an exact damping half step with a Verlet step and another exact damping half step:

$$
v_a=e^{-\beta h/2}v_n,\qquad
v_{1/2}=v_a+\tfrac h2 M^{-1}(f(t_n)-F(q_n)),
$$

$$
q_{n+1}=q_n+h v_{1/2},
$$

$$
v_b=v_{1/2}+\tfrac h2 M^{-1}(f(t_{n+1})-F(q_{n+1})),
\qquad v_{n+1}=e^{-\beta h/2}v_b.
$$

Here F is the assembled gradient of Vh. For sufficiently smooth solutions and forcing at fixed spatial discretization, the method has second order global time accuracy over a fixed finite time interval.

The coordinate times are calculated as t_origin + global_integer_step times h. They are not accumulated by repeatedly adding h. A resumed run therefore evaluates the configured source at the same floating point times as an uninterrupted run.

In the continuum finite system,

$$
\frac{dE_h}{dt}=f(t)^Tv-\beta v^TMv.
$$

The reported work increment uses h[f(tn)^Tvn + f(tn+1)^Tvn+1]/2. The damping increment is the exact kinetic energy removed by the two discrete damping subflows:

$$
\Delta D=\tfrac12(v_n^TMv_n-v_a^TMv_a)
+\tfrac12(v_b^TMv_b-v_{n+1}^TMv_{n+1}).
$$

This is exact for those damping maps in real arithmetic, not an exact evaluation of the continuous dissipated energy for an arbitrary nonlinear trajectory. The cumulative diagnostic is E - E_initial - W + D. It is expected to decrease at second order under timestep refinement in the tested smooth regimes. Verlet does not preserve the original nonlinear energy exactly, even with zero source and damping.

Only sampled diagnostics are retained. A reported maximum sampled energy defect is not a maximum over every intermediate state unless sample_every is one. The checkpoint callback runs at the same recording cadence and at the final step.

### Timestep guard

For a single stable harmonic oscillator Verlet requires h sqrt(nu) < 2. The code chooses a guard below that boundary, default 1.8. Since lambda is nonnegative, the nonlinear Hessian contribution satisfies the discrete generalized bound

$$
x^T(H_h(q)-K)x
\le 3\lambda\max_g(N_g^2\phi_g^2)\,x^T Mx.
$$

Consequently, max(|nu_min(K)|,|nu_max(K)|) + 3 lambda max_g(Ng phi_g)² bounds the absolute generalized Hessian scale at the sampled state. The implementation checks h times its square root before a step and at the proposed new position.

This bound concerns the quadrature defined finite matrices at those positions. It does not control every intervening nonlinear state, resolve forcing time scales, guarantee a requested phase accuracy, or stabilize physical negative modes. Rejecting a too large step preserves the last committed state. The fixed timestep resume command does not silently change h; to use a different timestep, construct an explicitly documented new initial state in the API.

## 7. Stationary solver

Equilibrium search sets F(q) = 0 with zero configured drive. Damping has no effect on the stationary equation. The supplied initial position becomes the seed; initial velocity is irrelevant.

The stopping residual is the mass dual norm

$$
r(q)=\sqrt{F(q)^T M^{-1}F(q)},\qquad
r(q)\le {\rm atol}+{\rm rtol}\,r(q_{\rm initial}).
$$

Defaults are atol = 10^-11 and rtol = 10^-10. They are finite dimensional residual tolerances in the selected units, not field error estimates.

The search computes the smallest generalized Hessian eigenvalue, adds a positive mass shift when needed, and solves a positive modified Newton system. The target lower eigenvalue floor is 10^-6. An Armijo backtracking line search with coefficient 10^-4 requests sufficient energy decrease. A nonfinite or non descent direction falls back to a mass preconditioned negative gradient. There are at most 50 line search halvings per outer step.

Near the binary64 energy comparison floor, a candidate can instead be accepted when its energy differs by no more than 16 machine epsilons times max(1,|V|) and its residual improves by a factor greater than two. This exception is stated explicitly because a literal strict energy decrease can stall once residual improvements are smaller than the energy representation can resolve.

The solver reports convergence status, termination reason, the full outer iteration trace, residual, tolerance, energy, and a Hessian spectrum. It returns an unsuccessful command status if residual convergence was not reached.

At c < 0, lambda > 0 and spatially constant coefficients, constant states phi = plus or minus sqrt(-c/lambda) are stationary minima, while zero is stationary with a negative constant mode. The test suite checks both outcomes. The search is local; no enumeration of domains, defects, metastable branches, or saddle points is claimed.

## 8. Restart and integrity

A checkpoint stores coefficient position and velocity, timestep, integer step count, time origin, initial energy, cumulative work, cumulative dissipation, normalized configuration, schema, solver version, solver source hash, and operator fingerprint. A content digest covers the metadata and canonical little endian coefficient bytes.

Writes use a temporary file in the destination directory, flush and file fsync, then atomic replacement. This reduces partial overwrite risk. There is no claim of a transactional multi file result set or full durability against every filesystem or power failure.

The reader uses allow_pickle=False, checks the content digest, rejects source and version mismatches, reconstructs the operator, and checks its fingerprint. Fingerprints describe the model, resolution, basis convention, and version; they do not establish cross platform numerical equivalence or authenticate hostile files.

The split run verification executes 37 steps, saves, reloads, executes 43 more steps, and compares against a continuous 80 step driven damped nonlinear run. Position, velocity, work, and dissipation agree bit for bit in the recorded environment. Numerical libraries, BLAS implementations, thread counts, and floating point reductions can vary across machines, so this observation must not be extrapolated to a universal bitwise guarantee.

On a handled numerical failure in evolution, the command saves the last committed state and a failure report. A hard process interruption can recover only the most recently written checkpoint, whose spacing follows the sampling cadence. History is written at successful completion; interrupted runs do not promise a complete history file.

## 9. Verification design and error separation

The release includes exact geometric limits, pointwise embedding checks, integrated geometry identities, exact flat spectra, a variable lapse exact solution, a separately assembled complex Fourier reference, phase symmetry checks, energy derivatives, nonlinear analytic and manufactured solutions, negative mode evolution, equilibrium classification, and checkpoint failure tests.

The complex reference uses FFT integrals in a complex Fourier basis and a separately constructed matrix formula. It shares the analytical geometry routine with the production implementation. It independently checks assembly and basis equivalence, not every geometry formula. The embedding curvature checks cover that separate concern.

The nonlinear Duffing test is a full field evolution whose invariant constant spatial subspace has an analytic Jacobi elliptic solution. It therefore tests time stepping and nonlinear projection but does not alone test spatial mode transfer. The varying corrugated field energy study and manufactured nonconstant source test provide additional coverage.

The manufactured solution on a flat cylinder prescribes phi = A cos(theta) cos(zeta) cos(omega t) and constructs the physical source analytically, including the cubic term. Time refinement then measures the field error at a common final time. A manufactured source built by simply calling the solver force would be a weaker independent check; this source uses the continuum flat mode formula.

Three distinct errors must be studied:

1. Algebraic error in solving the finite matrix or nonlinear stationarity problem.
2. Spatial approximation error from finite trial cutoff and finite quadrature.
3. Time discretization error at a fixed spatial problem.

For a stationary solve, a small residual can coexist with a poorly resolved profile. For a spectrum, a small eigensolver residual can coexist with an inaccurate Galerkin eigenvalue. For a trajectory, bounded sampled energy error can coexist with an unacceptable accumulated phase error.

The converge command runs two separate sequences: varying a common cutoff in both coordinates with the configured quadrature fixed, and varying a common point count in both coordinates with the configured cutoff fixed. Sorted eigenvalue differences are reported without extrapolating a certified limit. It does not automatically rerun every equilibrium or transient at higher resolution.

A defensible application should first resolve the static coefficients by quadrature, then establish stability of the desired low spectral quantities or equilibrium observables under basis refinement, and finally demonstrate timestep convergence for each time dependent observable. Repeat spatial checks if nonlinearity generates finer field structure. Choose tolerances from the observable and units before making an accuracy claim.

## 10. Precision, provenance, and scope of rigor

Input fractions are parsed as rational values and then converted to binary64. Decimal strings, integers, and finite real numbers are accepted; booleans and nonfinite values are rejected. This avoids ambiguous input interpretation but does not make subsequent arithmetic rational.

Key output floats carry both their exact binary64 decimal expansion and hexadecimal representation. This preserves the stored value without decimal rounding for presentation. It does not turn a binary64 computation into an arbitrary precision calculation. Numerical uncertainty is determined by conditioning, truncation, quadrature, timestep, and comparison evidence.

The archive includes the exact source and execution receipts. The manifest provides per file SHA256 hashes. The source hash in each example report connects that report to the solver used. Dependency versions are recorded, but dependency wheel hashes and full platform images are not distributed.

This release provides a transparent, reproducible reference implementation with explicit invariants, independent checks, and measured convergence in specified cases. It does not supply a formal proof of every code path, interval arithmetic bounds, a posteriori certified continuum eigenvalue enclosures, a complete nonlinear existence theory, or validation against experiment. Those are different tasks with additional assumptions and evidence requirements.

The method is intentionally specialized: analytic geometry, a variational basis suited to double periodicity, exact derivative matrices, coherent quadrature energy, reusable mass factorization, and preserved mode multiplicities. Further optimization would be justified by measured bottlenecks and cross checks against this reference. No unmeasured speedup is claimed.
