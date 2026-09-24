# Geometry Coupled Phase Field Theory
## Expanded variational, geometric, spectral, gravitational, quantum, and computational monograph

**Prepared for James Lockwood**  
**Revision date: 24 September 2026**  
**Status: mathematical model development with executed computational benchmarks**

This monograph develops the supplied geometry coupled scalar construction into a collection of explicitly defined continuum models. It retains the original cylindrical background, corrugated radial graph, quadratic geometry coupling, quartic scalar interaction, and optional fermion sector. It supplies the variational derivations, geometric identities, operator domains, boundary conditions, stability criteria, limiting cases, dimensional conventions, and reproducible computations needed to make those ingredients mathematically testable.

The central object is an action together with its domain and data. A drawing of a corrugated surface, an assigned potential, and a wave pattern do not determine one unique theory. Several inequivalent theories can realize that description. The document therefore specifies each realization independently and states exactly when equations may be transferred between them.

All displayed analytical identities are exact unless an expansion parameter or approximation symbol is present. Numerical examples are dimensionless mathematical benchmarks, not measurements and not fitted predictions. Exact input fractions are retained. Computed floating point values are accompanied by their arithmetic provenance; the complete numerical receipt records the exact decimal value of each stored binary64 number and its hexadecimal representation. Those extra digits describe the computation, not established continuum accuracy.

The scope includes classical field dynamics, perturbative quantum structure, and explicit geometric realizations. It does not establish experimental confirmation, uniqueness, a ultraviolet completion, or novelty of the general scalar, Yukawa, curvature coupling, and membrane ingredients. A specific realization could become a research contribution through a new theorem, controlled derivation, distinctive prediction, or independently reproduced observation. The mathematical task here is to make such a contribution assessable.

---

## Contents


- [Part I. Definition of the theories](#part-i-definition-of-the-theories)
  - [1. What the model actually specifies](#1-what-the-model-actually-specifies)
  - [2. Conventions and symbol dictionary](#2-conventions-and-symbol-dictionary)
  - [3. Geometry, topology, and domain](#3-geometry-topology-and-domain)
  - [4. Dimensional bookkeeping in bulk and on the surface](#4-dimensional-bookkeeping-in-bulk-and-on-the-surface)

- [Part II. The conservative scalar theory](#part-ii-the-conservative-scalar-theory)
  - [5. Action, variation, and source conventions](#5-action-variation-and-source-conventions)
  - [6. Canonical positivity and its precise limitations](#6-canonical-positivity-and-its-precise-limitations)
  - [7. Exact cylindrical wave operator](#7-exact-cylindrical-wave-operator)
  - [8. The profile coefficient and Cartesian regularity](#8-the-profile-coefficient-and-cartesian-regularity)
  - [9. Boundary actions and boundary conditions](#9-boundary-actions-and-boundary-conditions)
  - [10. Cauchy data and compatibility](#10-cauchy-data-and-compatibility)
  - [11. Canonical variables on a general static background](#11-canonical-variables-on-a-general-static-background)

- [Part III. Conservation, operators, and stability](#part-iii-conservation-operators-and-stability)
  - [12. Stress tensor from metric variation](#12-stress-tensor-from-metric-variation)
  - [13. Exact local exchange identity](#13-exact-local-exchange-identity)
  - [14. Energy balance with a varying coefficient](#14-energy-balance-with-a-varying-coefficient)
  - [15. Static equilibrium and the weighted elliptic operator](#15-static-equilibrium-and-the-weighted-elliptic-operator)
  - [16. Hilbert space, quadratic form, and self adjointness](#16-hilbert-space-quadratic-form-and-self-adjointness)
  - [17. Rayleigh quotient and strict versus marginal stability](#17-rayleigh-quotient-and-strict-versus-marginal-stability)
  - [18. A variational instability criterion](#18-a-variational-instability-criterion)
  - [19. Static existence and the direct method](#19-static-existence-and-the-direct-method)
  - [20. Nonlinear stability near an equilibrium](#20-nonlinear-stability-near-an-equilibrium)

- [Part IV. Explicit spectra and mode coupling](#part-iv-explicit-spectra-and-mode-coupling)
  - [21. Exact free cylindrical modes](#21-exact-free-cylindrical-modes)
  - [22. Cylindrical radial transformation and its endpoint](#22-cylindrical-radial-transformation-and-its-endpoint)
  - [23. Corrugation as an external Fourier potential](#23-corrugation-as-an-external-fourier-potential)
  - [24. Perturbative shifts and exact two mode diagonalization](#24-perturbative-shifts-and-exact-two-mode-diagonalization)
  - [25. A fully specified second order benchmark](#25-a-fully-specified-second-order-benchmark)
  - [26. Bloch sectors, lattice connectivity, and parity](#26-bloch-sectors-lattice-connectivity-and-parity)
  - [27. Phase offsets and observable registration](#27-phase-offsets-and-observable-registration)
  - [28. Localized modes, band edges, and far field conditions](#28-localized-modes-band-edges-and-far-field-conditions)

- [Part V. Nonlinear dynamics and controlled approximations](#part-v-nonlinear-dynamics-and-controlled-approximations)
  - [29. Uniform vacua and fluctuation masses](#29-uniform-vacua-and-fluctuation-masses)
  - [30. Gradient correction to a slowly varying broken state](#30-gradient-correction-to-a-slowly-varying-broken-state)
  - [31. Bifurcation from a simple zero eigenvalue](#31-bifurcation-from-a-simple-zero-eigenvalue)
  - [32. Exact real mode projection](#32-exact-real-mode-projection)
  - [33. Single mode dynamics and the exact Duffing solution](#33-single-mode-dynamics-and-the-exact-duffing-solution)
  - [34. Resonance, leakage, and the limits of a modal reduction](#34-resonance-leakage-and-the-limits-of-a-modal-reduction)
  - [35. Parametric modulation as an explicitly powered system](#35-parametric-modulation-as-an-explicitly-powered-system)
  - [36. Domain walls and a useful exact nonlinear solution](#36-domain-walls-and-a-useful-exact-nonlinear-solution)
  - [37. Scaling obstruction for static isolated lumps](#37-scaling-obstruction-for-static-isolated-lumps)
  - [38. Characteristics and the two different WKB limits](#38-characteristics-and-the-two-different-wkb-limits)

- [Part VI. Exact corrugated surface geometry](#part-vi-exact-corrugated-surface-geometry)
  - [39. Tangent vectors and first fundamental form](#39-tangent-vectors-and-first-fundamental-form)
  - [40. Unit normal and second fundamental form](#40-unit-normal-and-second-fundamental-form)
  - [41. Exact intrinsic and extrinsic curvature](#41-exact-intrinsic-and-extrinsic-curvature)
  - [42. Exact Laplace–Beltrami operator](#42-exact-laplacebeltrami-operator)
  - [43. Controlled small amplitude geometry expansion](#43-controlled-small-amplitude-geometry-expansion)
  - [44. First variation of the surface wave operator](#44-first-variation-of-the-surface-wave-operator)
  - [45. First curvature variation around a cylinder](#45-first-curvature-variation-around-a-cylinder)
  - [46. Surface field action and worldvolume curvature](#46-surface-field-action-and-worldvolume-curvature)
  - [47. Intrinsic coupling, extrinsic coupling, and thin confinement](#47-intrinsic-coupling-extrinsic-coupling-and-thin-confinement)

- [Part VII. Dynamical surfaces and material closure](#part-vii-dynamical-surfaces-and-material-closure)
  - [48. A surface that moves requires a new kinematic specification](#48-a-surface-that-moves-requires-a-new-kinematic-specification)
  - [49. Static elastic functional and shape variation](#49-static-elastic-functional-and-shape-variation)
  - [50. Scalar stress acting on a surface](#50-scalar-stress-acting-on-a-surface)
  - [51. Dynamical membrane energy balance](#51-dynamical-membrane-energy-balance)
  - [52. A covariant material field generating the bulk coefficient](#52-a-covariant-material-field-generating-the-bulk-coefficient)

- [Part VIII. A consistent fermion sector](#part-viii-a-consistent-fermion-sector)
  - [53. Clifford convention tied to the spacetime signature](#53-clifford-convention-tied-to-the-spacetime-signature)
  - [54. Spin connection and the Hermitian action](#54-spin-connection-and-the-hermitian-action)
  - [55. Explicit cylindrical Dirac operator](#55-explicit-cylindrical-dirac-operator)
  - [56. Current, stress, and exchange with the scalar](#56-current-stress-and-exchange-with-the-scalar)
  - [57. Spin structure and boundary data](#57-spin-structure-and-boundary-data)
  - [58. Symmetries of the Yukawa theory and radiative closure](#58-symmetries-of-the-yukawa-theory-and-radiative-closure)

- [Part IX. Gravitational closure](#part-ix-gravitational-closure)
  - [59. Why a prescribed coefficient is not a complete gravitational source](#59-why-a-prescribed-coefficient-is-not-a-complete-gravitational-source)
  - [60. Scalar tensor action and boundary term](#60-scalar-tensor-action-and-boundary-term)
  - [61. Complete scalar tensor Euler equations](#61-complete-scalar-tensor-euler-equations)
  - [62. Trace elimination and a scalar kinetic diagnostic](#62-trace-elimination-and-a-scalar-kinetic-diagnostic)
  - [63. Einstein frame and health of the kinetic sector](#63-einstein-frame-and-health-of-the-kinetic-sector)
  - [64. Curvature of the lapse only metric](#64-curvature-of-the-lapse-only-metric)
  - [65. General ADM system and constraints](#65-general-adm-system-and-constraints)
  - [66. Scalar variables and sources in ADM form](#66-scalar-variables-and-sources-in-adm-form)
  - [67. Homogeneous cosmological reduction as a consistency test](#67-homogeneous-cosmological-reduction-as-a-consistency-test)
  - [68. Test field limits and the size of back reaction](#68-test-field-limits-and-the-size-of-back-reaction)

- [Part X. Continuous phase, gauge fields, and dissipation](#part-x-continuous-phase-gauge-fields-and-dissipation)
  - [69. A complex scalar with a normalization inherited from two real fields](#69-a-complex-scalar-with-a-normalization-inherited-from-two-real-fields)
  - [70. Current sign fixed by the transformation](#70-current-sign-fixed-by-the-transformation)
  - [71. Gauge completion with an explicit sign convention](#71-gauge-completion-with-an-explicit-sign-convention)
  - [72. Winding, vortices, and finite energy](#72-winding-vortices-and-finite-energy)
  - [73. Dissipative order parameter dynamics on a fixed manifold](#73-dissipative-order-parameter-dynamics-on-a-fixed-manifold)
  - [74. Damped waves and fluctuation dissipation](#74-damped-waves-and-fluctuation-dissipation)

- [Part XI. Green functions, quantization, and effective theory](#part-xi-green-functions-quantization-and-effective-theory)
  - [75. Retarded response and the sign of the source](#75-retarded-response-and-the-sign-of-the-source)
  - [76. Integrating out a quadratic scalar exactly](#76-integrating-out-a-quadratic-scalar-exactly)
  - [77. Heavy field expansion and its locality conditions](#77-heavy-field-expansion-and-its-locality-conditions)
  - [78. Symplectic form and mode normalization for quantization](#78-symplectic-form-and-mode-normalization-for-quantization)
  - [79. Static vacuum energy and geometry dependence](#79-static-vacuum-energy-and-geometry-dependence)
  - [80. Quadratic fluctuation determinant](#80-quadratic-fluctuation-determinant)
  - [81. Heat kernel structure and local counterterms](#81-heat-kernel-structure-and-local-counterterms)
  - [82. Flat space one loop potential with fixed normalization](#82-flat-space-one-loop-potential-with-fixed-normalization)
  - [83. Pure scalar running and the quartic convention](#83-pure-scalar-running-and-the-quartic-convention)
  - [84. Effective operator basis and cutoff hierarchy](#84-effective-operator-basis-and-cutoff-hierarchy)
  - [85. Higher derivatives and spurious high frequency roots](#85-higher-derivatives-and-spurious-high-frequency-roots)
  - [86. Quantum state, semiclassical gravity, and what remains unspecified](#86-quantum-state-semiclassical-gravity-and-what-remains-unspecified)

- [Part XII. Numerical formulation and reproducibility](#part-xii-numerical-formulation-and-reproducibility)
  - [87. The numerical problem must be specified before discretization](#87-the-numerical-problem-must-be-specified-before-discretization)
  - [88. Weak formulation and discrete matrices](#88-weak-formulation-and-discrete-matrices)
  - [89. Fourier Galerkin assembly without differentiating sampled metrics](#89-fourier-galerkin-assembly-without-differentiating-sampled-metrics)
  - [90. Ritz values, residuals, and what they certify](#90-ritz-values-residuals-and-what-they-certify)
  - [91. Exact constant mode as a geometry test](#91-exact-constant-mode-as-a-geometry-test)
  - [92. An exact nonconstant lapse ground state](#92-an-exact-nonconstant-lapse-ground-state)
  - [93. Geometry quadrature and topological checks](#93-geometry-quadrature-and-topological-checks)
  - [94. Time integration and a separate temporal error test](#94-time-integration-and-a-separate-temporal-error-test)
  - [95. Stability restrictions and nonlinear aliasing](#95-stability-restrictions-and-nonlinear-aliasing)
  - [96. Manufactured solutions for a full PDE implementation](#96-manufactured-solutions-for-a-full-pde-implementation)
  - [97. Mesh convergence, eigenvalue multiplicity, and mode tracking](#97-mesh-convergence-eigenvalue-multiplicity-and-mode-tracking)
  - [98. Conditioning, precision, and exact numeric reporting](#98-conditioning-precision-and-exact-numeric-reporting)
  - [99. Reproducibility receipt and computational scope](#99-reproducibility-receipt-and-computational-scope)
  - [100. Numerical interpretation before the tables](#100-numerical-interpretation-before-the-tables)
  - [101. Executed geometric integrals](#101-executed-geometric-integrals)
  - [102. Executed surface and potential spectra](#102-executed-surface-and-potential-spectra)
  - [103. Executed lapse and radial benchmarks](#103-executed-lapse-and-radial-benchmarks)
  - [104. Executed nonlinear temporal benchmark](#104-executed-nonlinear-temporal-benchmark)

- [Part XIII. Further analytical reductions and exact examples](#part-xiii-further-analytical-reductions-and-exact-examples)
  - [105. A corrugated boundary is a third spectral mechanism](#105-a-corrugated-boundary-is-a-third-spectral-mechanism)
  - [106. Thin layer dimensional reduction with explicit normalization](#106-thin-layer-dimensional-reduction-with-explicit-normalization)
  - [107. Curvature corrections in a tubular neighborhood](#107-curvature-corrections-in-a-tubular-neighborhood)
  - [108. A useful exact localized mode with a negative local mass region](#108-a-useful-exact-localized-mode-with-a-negative-local-mass-region)
  - [109. Exact normalization and nonlinear overlap for the localized example](#109-exact-normalization-and-nonlinear-overlap-for-the-localized-example)
  - [110. Ground state transformation and a general positivity proof](#110-ground-state-transformation-and-a-general-positivity-proof)
  - [111. Unitary conversion of the lapse weighted Hilbert space](#111-unitary-conversion-of-the-lapse-weighted-hilbert-space)
  - [112. Generalized geometric perturbation inside a degenerate subspace](#112-generalized-geometric-perturbation-inside-a-degenerate-subspace)
  - [113. Resolvent projection and the error in a two mode model](#113-resolvent-projection-and-the-error-in-a-two-mode-model)
  - [114. Ray transport in a variable effective mass](#114-ray-transport-in-a-variable-effective-mass)
  - [115. Restoring units without changing the field normalization silently](#115-restoring-units-without-changing-the-field-normalization-silently)

- [Part XIV. Observables, inference, and falsification](#part-xiv-observables-inference-and-falsification)
  - [116. The observable map](#116-the-observable-map)
  - [117. Structural parameter degeneracies](#117-structural-parameter-degeneracies)
  - [118. Sensitivity of generalized eigenvalues](#118-sensitivity-of-generalized-eigenvalues)
  - [119. Fisher information and its limitations](#119-fisher-information-and-its-limitations)
  - [120. A discriminating sequence of experiments](#120-a-discriminating-sequence-of-experiments)
  - [121. Distinguishing ordinary geometry effects from an additional interaction](#121-distinguishing-ordinary-geometry-effects-from-an-additional-interaction)
  - [122. Stopping rules and falsifiable outcomes](#122-stopping-rules-and-falsifiable-outcomes)
  - [123. Research claims supported by the present work](#123-research-claims-supported-by-the-present-work)
  - [124. Minimum complete model for each intended use](#124-minimum-complete-model-for-each-intended-use)

- [Part XV. Detailed algebraic audits](#part-xv-detailed-algebraic-audits)
  - [125. Derivation of the nonminimal stress variation](#125-derivation-of-the-nonminimal-stress-variation)
  - [126. Bianchi consistency of the scalar tensor equation](#126-bianchi-consistency-of-the-scalar-tensor-equation)
  - [127. Conformal covariance and the quartic interaction](#127-conformal-covariance-and-the-quartic-interaction)
  - [128. Energy estimate for a bounded domain](#128-energy-estimate-for-a-bounded-domain)
  - [129. Local versus global lower bounds on an infinite domain](#129-local-versus-global-lower-bounds-on-an-infinite-domain)
  - [130. No net work from a static ground state](#130-no-net-work-from-a-static-ground-state)
  - [131. A complete dependency chain for one canonical surface model](#131-a-complete-dependency-chain-for-one-canonical-surface-model)
  - [132. Compact canonical equation collection](#132-compact-canonical-equation-collection)

- [Part XVI. Provenance and reusable computational record](#part-xvi-provenance-and-reusable-computational-record)
  - [133. Source document and revision scope](#133-source-document-and-revision-scope)
  - [134. Primary references and their role](#134-primary-references-and-their-role)
  - [135. Exact provenance record](#135-exact-provenance-record)
  - [136. Complete executable verification source](#136-complete-executable-verification-source)
  - [137. Complete execution receipt](#137-complete-execution-receipt)
  - [138. Defined continuation points](#138-defined-continuation-points)

---

# Part I. Definition of the theories

## 1. What the model actually specifies

The supplied construction contains five distinct kinds of information:

1. A real scalar field \(\phi\), interpreted as an order parameter or relativistic scalar.
2. A static cylindrical spacetime metric with lapse \(N\).
3. A quadratic modulation \(U(x)\phi^2\), possibly associated with a corrugated structure.
4. An embedded radial graph describing a tube.
5. Optional additional dynamics for spinors, spacetime curvature, or the tube itself.

These ingredients must not be silently identified. A radial graph is an embedding. A lapse is part of a Lorentzian metric. A scalar potential is a constitutive coefficient. Intrinsic curvature is a metric invariant. Extrinsic curvature depends on an embedding and its normal. They are connected only after an explicit prescription is chosen.

The following table fixes the independent models used throughout.

| Model | Dynamical unknowns | Prescribed data | Governing structure |
|---|---|---|---|
| Bulk scalar | \(\phi\) | \(g_{\mu\nu},U\) | Semilinear Klein–Gordon equation |
| Bulk scalar and fermion | \(\phi,\psi,\bar\psi\) | \(g_{\mu\nu},U\) | Klein–Gordon and Dirac equations |
| Scalar with material source | \(\phi,\chi\) | \(g_{\mu\nu}\) | Two coupled field equations, \(U=u(\chi)\) |
| Scalar tensor gravity | \(g_{\mu\nu},\phi\) | Potential, matter content, initial data | Metric and scalar Euler equations |
| Prescribed surface scalar | \(\varphi\) | Embedded surface \(X\), surface coefficients | Wave equation on the induced metric |
| Elastic surface with scalar | \(X,\varphi\) | Elastic law, environment, boundary data | Shape equation and scalar equation |
| Dissipative order parameter | \(\varphi\) | Surface or bulk geometry, mobility | Gradient flow or conserved diffusion |

The word “phase” has two legitimate meanings here. A real scalar can represent an order parameter distinguishing phases of matter. A continuously variable internal phase requires a complex field or a field valued on a circle. A real Klein–Gordon field is not automatically a \(U(1)\) phase variable.

## 2. Conventions and symbol dictionary

The spacetime metric has signature
\[
g_{\mu\nu}:\quad (-,+,+,+).
\]
The curvature convention is
\[
R^\rho{}_{\sigma\mu\nu}
=
\partial_\mu\Gamma^\rho_{\nu\sigma}
-\partial_\nu\Gamma^\rho_{\mu\sigma}
+\Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma}
-\Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma},
\qquad
R_{\sigma\nu}=R^\rho{}_{\sigma\rho\nu}.
\]
Thus a spatially flat de Sitter metric with constant Hubble parameter \(H_{\mathrm{dS}}\) has
\[
\mathcal R=12H_{\mathrm{dS}}^2.
\]
The symbol \(\mathcal R\) denotes spacetime Ricci scalar. The tube radius is \(R(\theta,\zeta)\). The two symbols are kept distinct.

Natural units \(\hbar=c=1\) apply unless restored explicitly. A coordinate angle has dimension zero. A time coordinate has length dimension when \(c=1\).

| Symbol | Meaning |
|---|---|
| \(\phi\) | Real bulk scalar |
| \(\varphi\) | Real scalar intrinsic to a surface worldvolume |
| \(\psi,\bar\psi\) | Dirac field and its adjoint |
| \(N>0\) | Lapse |
| \(h_{ij}\) | Spatial metric on a time slice |
| \(\beta^i\) | Shift |
| \(p=n^\mu\nabla_\mu\phi\) | Scalar derivative along the future unit normal |
| \(\pi=\sqrt h\,p\) | Canonical momentum density |
| \(U\) | External quadratic coefficient, mass dimension two |
| \(V\) | Scalar self potential |
| \(W=V+U\phi^2\) | Total scalar potential density |
| \(\lambda\) | Quartic coefficient in \(V=\frac12m_\phi^2\phi^2+\frac{\lambda}{4}\phi^4+V_0\) |
| \(\xi\) | Nonminimal scalar curvature coupling |
| \(F(\phi)\) | Coefficient of \(\mathcal R\) in the form \(\frac12F\mathcal R\) |
| \(M_{\mathrm{Pl}}^2=(8\pi G)^{-1}\) | Reduced Planck mass squared |
| \(\gamma_{ab}\) | Induced spatial surface metric |
| \(q_{AB}\) | Induced Lorentzian worldvolume metric |
| \(b_{ab}\) | Surface second fundamental form, outward convex cylinder positive |
| \(H=\frac12\gamma^{ab}b_{ab}\) | Mean curvature |
| \(K_G=\det(b^a{}_b)\) | Gaussian curvature |
| \(a=L_z/(2\pi)\) | Axial length per unit phase \(\zeta\) |
| \(n,m\) | Positive integers labeling corrugation harmonics |
| \(\mathsf M,\mathsf K\) | Discrete mass and stiffness matrices |
| \(\nu_j=\omega_j^2\) | Squared normal mode frequency |

The sign convention for \(p\) is fixed throughout. A formulation using \(-n^\mu\nabla_\mu\phi\) must reverse both momentum evolution and the relation between momentum and \(\dot\phi\). This document uses the positive normal derivative.

## 3. Geometry, topology, and domain

The bulk cylindrical coordinates are
\[
x^\mu=(t,r,\theta,z),\qquad
ds^2=-N^2(r,z)\,dt^2+dr^2+r^2d\theta^2+dz^2.
\]
A convenient finite domain is
\[
\Omega=\{r_{\mathrm{in}}\le r\le r_{\mathrm{out}},\quad
\theta\in\mathbb R/(2\pi\mathbb Z),\quad
z\in\mathbb R/(L_z\mathbb Z)\}.
\]
For an annulus, \(r_{\mathrm{in}}>0\), cylindrical coordinates are nonsingular. For a solid cylinder, \(r_{\mathrm{in}}=0\), the axis is a coordinate degeneration, not an ordinary inner boundary. Smoothness must be imposed in Cartesian coordinates or through the equivalent angular regularity conditions.

The corrugated graph is
\[
R(\theta,\zeta)
=
R_0+A\sin(n\theta+\delta_\theta)\cos(m\zeta+\delta_\zeta),
\qquad z=a\zeta.
\]
A sufficient global regularity condition is
\[
R_0>|A|,\qquad a>0.
\]
It guarantees a positive radius and a nondegenerate induced metric. It does not by itself ensure a controlled small slope expansion.

There are three different axial constructions:

- An infinite periodically corrugated tube in \(\mathbb R^3\), with \(\zeta\in\mathbb R\).
- A finite segment with physical end boundaries.
- A periodic computational cell with ends identified.

For the embedding
\[
X(\theta,\zeta)=(R\cos\theta,R\sin\theta,a\zeta),
\]
one has
\[
X(\theta,\zeta+2\pi)=X(\theta,\zeta)+(0,0,2\pi a).
\]
Consequently, the formula does not embed a compact torus into ordinary \(\mathbb R^3\) when \(\zeta\) is identified modulo \(2\pi\). It defines either a periodic covering surface or a surface in an ambient space with periodic axial identification. Its metric can nevertheless descend to a smooth abstract two torus. That distinction matters for global embeddings, topology, boundary forces, and the interpretation of curvature integrals.

## 4. Dimensional bookkeeping in bulk and on the surface

In \(D\) spacetime dimensions, a canonically normalized real scalar has mass dimension
\[
[\phi]=\frac{D-2}{2}.
\]
A Dirac field has
\[
[\psi]=\frac{D-1}{2}.
\]
The quartic and Yukawa couplings have dimensions
\[
[\lambda]=4-D,\qquad [g_Y]=\frac{4-D}{2}.
\]
Thus in a four dimensional bulk,
\[
[\phi]=1,\quad[\psi]=\frac32,\quad[\lambda]=[g_Y]=[\xi]=0,
\quad [m_\phi]=[M]=1,\quad [U]=[\mathcal R]=2.
\]
For an intrinsic \(2+1\) dimensional surface theory,
\[
[\varphi]=\frac12,\qquad [\lambda_\Sigma]=1.
\]
A bulk scalar restricted to a surface does not automatically acquire canonical surface normalization. The normalization depends on the transverse wavefunction, layer thickness, and microscopic confinement mechanism. A reduction must therefore distinguish \(\phi|_\Sigma\) from the canonically normalized \(\varphi\).

The geometric quantities satisfy
\[
[R_0]=[A]=[a]=-1,\quad [H]=1,\quad[K_G]=[\mathcal R_\Sigma]=2.
\]
The integer \(m\) in the corrugation is not a mass. The physical axial wavenumber of that harmonic is
\[
k_{\mathrm{corr}}=\frac{m}{a}=\frac{2\pi m}{L_z}.
\]

A useful dimensional audit is to assign every term in the bulk scalar equation dimension three. For example,
\[
[\Box\phi]=[m_\phi^2\phi]=[U\phi]=[\lambda\phi^3]=[g_Y\bar\psi\psi]=3.
\]
The analogous surface equation has dimension \(5/2\), and therefore uses a dimensionful surface quartic coupling.

---

# Part II. The conservative scalar theory

## 5. Action, variation, and source conventions

For prescribed geometry and a prescribed scalar coefficient \(U(x)\), define
\[
S_\phi=\int_{\mathcal M}d^4x\,\sqrt{-g}
\left[-\frac12g^{\mu\nu}\nabla_\mu\phi\nabla_\nu\phi
-V(\phi)-U(x)\phi^2-J(x)\phi\right].
\]
The source convention is fixed by the term \(-J\phi\). Its field equation will therefore have \(+J\) on the right of the Klein–Gordon operator.

The first variation at fixed \(g,U,J\) is
\[
\delta S_\phi
=
\int_{\mathcal M}\sqrt{-g}
\left[-\nabla^\mu\phi\,\nabla_\mu\delta\phi
-\left(V'(\phi)+2U\phi+J\right)\delta\phi\right]d^4x.
\]
Using
\[
\nabla^\mu\phi\,\nabla_\mu\delta\phi
=
\nabla_\mu(\delta\phi\nabla^\mu\phi)-\delta\phi\,\Box_g\phi,
\]
gives
\[
\delta S_\phi
=
\int_{\mathcal M}\sqrt{-g}
\left[\Box_g\phi-V'(\phi)-2U\phi-J\right]\delta\phi\,d^4x
-\int_{\partial\mathcal M}\delta\phi\,\nabla^\mu\phi\,d\Sigma_\mu.
\]
The directed boundary element avoids a hidden sign ambiguity between timelike and spacelike boundary pieces. On a timelike outer wall, its outward normal is spacelike and the surface term is
\[
-\int_{\partial\mathcal M_{\mathrm{wall}}}\sqrt{|q_\partial|}
\,s^\mu\nabla_\mu\phi\,\delta\phi\,d^3y.
\]

The bulk Euler equation is
\[
\boxed{\Box_g\phi-V'(\phi)-2U\phi=J.}
\]
For the quartic potential,
\[
V(\phi)=V_0+\frac12m_\phi^2\phi^2+\frac{\lambda}{4}\phi^4,
\]
the equation is
\[
\boxed{\Box_g\phi-(m_\phi^2+2U)\phi-\lambda\phi^3=J.}
\]
The factor two follows directly from differentiating \(U\phi^2\). It is not an adjustable convention after the action has been fixed.

The additive constant \(V_0\) has no effect on this scalar equation when the metric is prescribed. It contributes to the stress tensor and therefore matters in a gravitational theory.

## 6. Canonical positivity and its precise limitations

In a local inertial frame,
\[
\mathcal L_\phi
=
\frac12\dot\phi^2-\frac12|\nabla\phi|^2-W(\phi,x),
\]
with \(J=0\). The canonical kinetic energy is positive:
\[
\mathcal H_\phi
=
\frac12\dot\phi^2+\frac12|\nabla\phi|^2+W.
\]
This establishes the absence of a wrong sign scalar kinetic term. It does not establish \(W\ge0\), boundedness of a spatially integrated energy on every domain, or stability of every solution.

Set
\[
b(x)=m_\phi^2+2U(x).
\]
For \(\lambda>0\), completing the square yields
\[
\frac{\lambda}{4}\phi^4+\frac12b\phi^2
=
\frac{\lambda}{4}\left(\phi^2+\frac b\lambda\right)^2
-\frac{b^2}{4\lambda}.
\]
A sharper lower bound uses \(b_-=\max(-b,0)\):
\[
\frac{\lambda}{4}\phi^4+\frac12b\phi^2
\ge-\frac{b_-^2}{4\lambda}.
\]
Thus on a finite volume domain with bounded \(b_-\), the energy is bounded below. On an infinite volume domain, the integral of the lower bound may diverge. One then needs a specified vacuum subtraction, decay of the negative part, or another coercive estimate.

If \(b<0\), \(\phi=0\) can be unstable while the full quartic energy remains bounded below. This is the standard difference between instability of one configuration and absence of any lower energy bound.

For \(\lambda<0\), the quartic truncation is unbounded below at large field. A higher even power can stabilize a classical polynomial, but the resulting higher dimensional operators introduce a cutoff dependent effective theory. Their presence must be incorporated into both the equations and the stated range of validity.

## 7. Exact cylindrical wave operator

For
\[
g_{\mu\nu}=\operatorname{diag}(-N^2,1,r^2,1),
\]
the inverse and volume density are
\[
g^{\mu\nu}=\operatorname{diag}(-N^{-2},1,r^{-2},1),
\qquad \sqrt{-g}=Nr.
\]
The exact scalar d'Alembertian is
\[
\Box_g\phi
=
\frac1{Nr}\partial_\mu(Nr\,g^{\mu\nu}\partial_\nu\phi).
\]
For \(N=N(r,z)\),
\[
\boxed{
\Box_g\phi=
-\frac1{N^2}\phi_{tt}
+\phi_{rr}
+\left(\frac1r+\frac{N_r}{N}\right)\phi_r
+\frac1{r^2}\phi_{\theta\theta}
+\phi_{zz}
+\frac{N_z}{N}\phi_z.
}
\]
Therefore
\[
\frac1{N^2}\phi_{tt}
-\frac1{Nr}\partial_r(Nr\phi_r)
-\frac1{Nr}\partial_\theta\left(\frac Nr\phi_\theta\right)
-\frac1{Nr}\partial_z(Nr\phi_z)
+V'(\phi)+2U\phi=-J.
\]
The right side is \(-J\) because this expression is the negative of the covariant Euler equation.

Multiplication by \(Nr\) gives the conservative coordinate form
\[
\partial_t\left(\frac rN\phi_t\right)
-\partial_r(Nr\phi_r)
-\partial_\theta\left(\frac Nr\phi_\theta\right)
-\partial_z(Nr\phi_z)
+Nr\left[V'(\phi)+2U\phi+J\right]=0.
\]
This form is suitable for finite volume and weak finite element formulations. Conservation depends on discretizing the fluxes and weights consistently, not merely on retaining the symbol \(r\) somewhere in the code.

For time dependent \(N\), the temporal term must remain in divergence form. Expanding it adds a term proportional to \(N_t\phi_t\). The static operator formula cannot be reused unchanged.

## 8. The profile coefficient and Cartesian regularity

The phenomenological profile is
\[
U(r,\theta,z)
=
U_0e^{-\mu r}
+U_1\sin(n\theta+\delta_\theta)
\cos\left(\frac{mz}{a}+\delta_\zeta\right).
\]
On an annular domain this is smooth for smooth lapse and finite parameters. Its derivatives are
\[
U_r=-\mu U_0e^{-\mu r},
\]
\[
U_\theta=nU_1\cos(n\theta+\delta_\theta)
\cos\left(\frac{mz}{a}+\delta_\zeta\right),
\]
\[
U_z=-\frac maU_1\sin(n\theta+\delta_\theta)
\sin\left(\frac{mz}{a}+\delta_\zeta\right).
\]

On a domain containing the axis, a nonzero angular harmonic with radius independent amplitude has no unique value at \(r=0\). Moreover, \(e^{-\mu r}=e^{-\mu\sqrt{x^2+y^2}}\) is generally not differentiable at the origin when \(\mu U_0\ne0\). These profiles may still be studied as bounded or weak coefficients, but they do not meet a smooth Cartesian coefficient hypothesis.

A smooth axis compatible model can instead use
\[
U_{\mathrm{smooth}}
=
U_0e^{-\mu^2r^2}
+U_1\left(\frac r{L}\right)^n
e^{-r^2/L^2}
\sin(n\theta+\delta_\theta)
\cos\left(\frac{mz}{a}+\delta_\zeta\right).
\]
The angular numerator is a linear combination of
\[
\operatorname{Re}(x+iy)^n,\qquad
\operatorname{Im}(x+iy)^n,
\]
so it extends smoothly through the axis. This is a distinct potential with distinct radial scattering and coupling matrix elements. It should be selected explicitly when a smooth solid cylinder is intended.

An exponential radial profile remains a legitimate annular model. Regularization is a physical modeling choice if the axis is included, not a harmless relabeling.

## 9. Boundary actions and boundary conditions

A variational problem includes boundary data. For the scalar:

**Dirichlet data**
\[
\phi|_{\partial\Omega}=f_\partial,\qquad
\delta\phi|_{\partial\Omega}=0.
\]

**Natural Neumann data**
\[
s^iD_i\phi|_{\partial\Omega}=0.
\]

**Robin data**
\[
s^iD_i\phi+\alpha\phi=0
\]
follow from adding a wall action
\[
S_{\partial\phi}
=
-\frac12\int dt\int_{\partial\Omega}N\sqrt{\sigma}\,
\alpha\phi^2\,d^2y
\]
for a static wall and real \(\alpha\). The corresponding energy includes
\[
E_{\partial\phi}
=
\frac12\int_{\partial\Omega}N\sqrt{\sigma}\,\alpha\phi^2\,d^2y.
\]
For \(\alpha<0\), the boundary contribution can destabilize a system with a nonnegative bulk mass. Real Robin data ensure symmetry of the linear operator, but do not ensure positivity.

Absorbing boundaries usually define an open evolution problem rather than a self adjoint cavity spectrum. A normal derivative condition designed for one propagation angle or one dispersion relation is generally not exactly nonreflecting for every mode. Its reflection error belongs in the numerical uncertainty budget.

At a regular axis, an angular mode behaves as
\[
\phi_\ell(r,z)=r^{|\ell|}f_\ell(r^2,z)
\]
for smooth \(f_\ell\). Thus \(\partial_r\phi_0=0\) at the axis, while nonzero angular modes vanish there. Imposing the same scalar Neumann condition on every Fourier mode does not reproduce Cartesian regularity.

## 10. Cauchy data and compatibility

For a fixed globally hyperbolic spacetime, initial scalar data on a Cauchy hypersurface are
\[
\phi|_{\Sigma_0}=\phi_0,\qquad
p|_{\Sigma_0}=p_0,
\qquad
p=n^\mu\nabla_\mu\phi.
\]
For a static lapse and zero shift,
\[
p_0=\frac1N\phi_t|_{\Sigma_0}.
\]
Classical smooth solutions with boundaries require compatible data. For homogeneous Dirichlet data, for example,
\[
\phi_0|_{\partial\Omega}=0,\qquad
Np_0|_{\partial\Omega}=0.
\]
Higher regularity requires higher time derivatives obtained from the PDE to satisfy the boundary conditions as well.

On a smooth compact spatial domain, take smooth \(N,U\), a lapse bounded above and below away from zero, and a smooth potential. Standard local semilinear wave theory then supplies local solutions in sufficiently regular Sobolev spaces. For the cubic defocusing nonlinearity in three spatial dimensions, the nonlinearity is energy subcritical. Energy estimates are therefore particularly useful. A global statement still depends on the domain, boundary conditions, geometry, forcing, and the coercivity actually available.

The linear globally hyperbolic theory, including retarded and advanced Green operators, is developed in [Bär, Ginoux, and Pfäffle, Wave Equations on Lorentzian Manifolds and Quantization](https://arxiv.org/abs/0806.1036). Nonlinear conclusions in this monograph are stated with their separate hypotheses; they are not inferred merely from existence of a linear Green function.

## 11. Canonical variables on a general static background

Let
\[
ds^2=-N^2(\mathbf x)dt^2+h_{ij}(\mathbf x)dx^idx^j.
\]
The action becomes
\[
S_\phi
=
\int dt\,d^3x
\left[
\frac{\sqrt h}{2N}\dot\phi^2
-N\sqrt h\left(\frac12h^{ij}D_i\phi D_j\phi+W\right)
\right].
\]
The canonical momentum density is
\[
\boxed{\pi=\frac{\sqrt h}{N}\dot\phi=\sqrt h\,p.}
\]
The Hamiltonian is
\[
\boxed{
E=
\int_\Omega d^3x
\left[
\frac{N}{2\sqrt h}\pi^2
+N\sqrt h\left(\frac12|D\phi|_h^2+W\right)
\right]+E_\partial.
}
\]
Its first Hamilton equation gives
\[
\dot\phi=\frac{N}{\sqrt h}\pi=Np.
\]
Its second gives
\[
\dot\pi
=
\partial_i(N\sqrt h\,h^{ij}\partial_j\phi)
-N\sqrt h\left[V'(\phi)+2U\phi\right].
\]
These reproduce the covariant field equation. The canonical momentum \(\pi\), the normal derivative \(p\), and the coordinate derivative \(\dot\phi\) are different objects. Confusing them changes both numerical mass matrices and mode normalization.

For the cylindrical metric,
\[
\sqrt h=r,\qquad \pi=\frac rN\dot\phi.
\]
The local energy density measured by the static unit normal is
\[
\rho=\frac12p^2+\frac12|D\phi|_h^2+W.
\]
The conserved Killing energy is
\[
E=\int_\Omega N\rho\,dV_h+E_\partial,
\]
rather than simply the unweighted integral of \(\rho\).

---

# Part III. Conservation, operators, and stability

## 12. Stress tensor from metric variation

When \(U\) is an independent prescribed scalar under metric variation,
\[
T_{\mu\nu}
=
-\frac2{\sqrt{-g}}\frac{\delta S_\phi}{\delta g^{\mu\nu}}
\]
gives, with \(J=0\),
\[
\boxed{
T_{\mu\nu}
=
\nabla_\mu\phi\nabla_\nu\phi
-g_{\mu\nu}
\left[\frac12(\nabla\phi)^2+V(\phi)+U\phi^2\right].
}
\]
The derivation uses
\[
\delta\sqrt{-g}=-\frac12\sqrt{-g}\,g_{\mu\nu}\delta g^{\mu\nu}
\]
and the fact that \(\nabla_\mu\phi=\partial_\mu\phi\) for a scalar. Contracting with a unit timelike vector \(n^\mu\) gives the positive kinetic terms in the energy density.

The tensor trace in four dimensions is
\[
T=-(\nabla\phi)^2-4V-4U\phi^2.
\]
For any null vector \(k^\mu\),
\[
T_{\mu\nu}k^\mu k^\nu=(k^\mu\nabla_\mu\phi)^2\ge0.
\]
Thus a minimally coupled classical canonical real scalar obeys the null energy condition independently of the sign of its potential. Negative potential energy is not a negative kinetic norm. The weak and dominant energy conditions impose additional requirements and cannot be inferred from the null contraction alone.

If \(U\) depends on the metric, the displayed stress tensor is incomplete. A coefficient such as \(U=\xi\mathcal R/2\) has a nontrivial metric variation and must be treated in the scalar tensor section.

## 13. Exact local exchange identity

Direct differentiation gives
\[
\nabla_\mu T^\mu{}_\nu
=
\left(\Box_g\phi-V'(\phi)-2U\phi\right)\nabla_\nu\phi
-\phi^2\nabla_\nu U.
\]
On the homogeneous scalar equation,
\[
\boxed{\nabla_\mu T^\mu{}_\nu=-\phi^2\nabla_\nu U.}
\]
With the source convention \(-J\phi\), if \(J\) is not included in the scalar stress tensor, the identity becomes
\[
\nabla_\mu T^\mu{}_\nu=J\nabla_\nu\phi-\phi^2\nabla_\nu U.
\]
If the source interaction is included in the stress tensor, its algebraic contribution and its explicit derivative must also be included. Assigning interaction energy between subsystems is partly conventional; varying the complete action removes the ambiguity.

For a vector field \(K^\mu\), define
\[
\mathcal J^\mu=T^\mu{}_\nu K^\nu.
\]
Then
\[
\nabla_\mu\mathcal J^\mu
=
-\phi^2K^\nu\nabla_\nu U
+\frac12T^{\mu\nu}\mathcal L_Kg_{\mu\nu}
\]
on the unsourced scalar equation. Therefore a conserved charge requires both a metric symmetry and invariance of the external coefficient under that symmetry.

For an angular Killing vector in an axisymmetric metric,
\[
\nabla_\mu(T^\mu{}_\theta)=-\phi^2\partial_\theta U.
\]
The right side is the torque density transferred between the field and the imposed structure. Periodic angular dependence can conserve a discrete symmetry while destroying continuous angular momentum conservation.

## 14. Energy balance with a varying coefficient

On a static background, differentiate the canonical energy directly and integrate the gradient term by parts:
\[
\frac{dE}{dt}
=
\int_\Omega N\sqrt h\,\phi^2\partial_tU\,d^3x
+\int_{\partial\Omega}N\sqrt\sigma\,\dot\phi\,s^iD_i\phi\,d^2y
\]
for \(J=0\), with any boundary energy included consistently.

Define outward energy flux
\[
\mathcal F_{\mathrm{out}}
=
-\int_{\partial\Omega}N\sqrt\sigma\,\dot\phi\,s^iD_i\phi\,d^2y.
\]
Then
\[
\boxed{
\frac{dE}{dt}
=
\int_\Omega N\phi^2\partial_tU\,dV_h-\mathcal F_{\mathrm{out}}.
}
\]
The lapse factor is fixed by the time coordinate defining the Killing energy. It is not an unspecified convention once the action and \(t\) have been selected.

For homogeneous Dirichlet, homogeneous Neumann, periodic boundaries, or a static Robin wall with its wall energy included, the net conservative boundary contribution vanishes. If \(U\) is time independent, energy is conserved.

If \(g_{\mu\nu}\) itself changes in time, the Hamiltonian acquires additional explicit metric work terms. One cannot use the static formula to conclude energy conservation on a driven or expanding geometry.

## 15. Static equilibrium and the weighted elliptic operator

A static field \(\phi_0\) satisfies
\[
-\frac1{N\sqrt h}\partial_i(N\sqrt h\,h^{ij}\partial_j\phi_0)
+V'(\phi_0)+2U\phi_0=0.
\]
This is the Euler equation of the static Killing energy
\[
E_{\mathrm{stat}}[\phi]
=
\int_\Omega N\left[\frac12|D\phi|_h^2+W(\phi,x)\right]dV_h+E_\partial.
\]
The factor \(N\) belongs in both the energy measure and the elliptic operator. Replacing the operator by \(-\Delta_h+W''\) is correct only for constant lapse, or after a separately derived transformation.

Linearize about a static solution:
\[
\phi=\phi_0+\eta,\qquad
M^2(\mathbf x)=V''(\phi_0)+2U.
\]
Then
\[
\frac1{N^2}\eta_{tt}
-\frac1{N\sqrt h}\partial_i(N\sqrt h\,h^{ij}\partial_j\eta)
+M^2\eta=0.
\]
Set \(\eta=e^{-i\omega t}u(\mathbf x)\). The exact generalized eigenproblem is
\[
\boxed{
-\partial_i(N\sqrt h\,h^{ij}\partial_j u)
+N\sqrt h\,M^2u
=
\omega^2\frac{\sqrt h}{N}u.
}
\]
The temporal mass weight is \(\sqrt h/N\), while the spatial energy weight is \(N\sqrt h\). This is the central operator distinction for nonconstant lapse.

## 16. Hilbert space, quadratic form, and self adjointness

Define
\[
\mathcal H=L^2\left(\Omega,\frac{dV_h}{N}\right),
\qquad
\langle u,v\rangle_{\mathcal H}
=
\int_\Omega\frac{u^*v}{N}\,dV_h.
\]
The linear evolution operator is
\[
Au
=
-\frac N{\sqrt h}\partial_i(N\sqrt h\,h^{ij}\partial_j u)
+N^2M^2u.
\]
Then
\[
\eta_{tt}+A\eta=0.
\]
Its quadratic form is
\[
\mathfrak a[u,v]
=
\int_\Omega N\left(h^{ij}D_iu^*D_jv+M^2u^*v\right)dV_h
+\int_{\partial\Omega}N\alpha u^*v\,dS_h
\]
for Robin data. Integration by parts gives
\[
\langle u,Av\rangle_{\mathcal H}=\mathfrak a[u,v].
\]
For Dirichlet data, the form domain is \(H_0^1(\Omega)\). For Neumann or Robin data, it is \(H^1(\Omega)\), subject to the geometry and regularity assumptions.

On a compact smooth domain, with \(0<N_{\min}\le N\le N_{\max}<\infty\), bounded real \(M^2\), and a semibounded real boundary form, the form defines a semibounded self adjoint operator. Its resolvent is compact under the usual elliptic hypotheses, so the spectrum is discrete with finite multiplicities and an orthonormal mode basis.

On a noncompact domain, one must distinguish point spectrum, continuous spectrum, essential spectrum, and resonances. A negative spectral infimum need not correspond to an isolated square integrable eigenfunction. It still signals exponentially growing components in the spectral evolution when the negative spectral subspace is nontrivial.

The formal differential expression and its self adjoint realization are separate pieces of the theory. Boundary and regularity conditions select the realization.

## 17. Rayleigh quotient and strict versus marginal stability

The lowest spectral value is characterized by
\[
\boxed{
\nu_{\min}
=
\inf_{u\ne0}
\frac{\displaystyle
\int_\Omega N\left(|Du|_h^2+M^2|u|^2\right)dV_h
+\int_{\partial\Omega}N\alpha|u|^2dS_h}
{\displaystyle\int_\Omega N^{-1}|u|^2dV_h}.
}
\]
For a negative discrete eigenvalue \(\nu=-\Gamma^2\),
\[
q(t)=c_+e^{\Gamma t}+c_-e^{-\Gamma t}.
\]
For a positive eigenvalue,
\[
q(t)=c_1\cos(\sqrt\nu\,t)+c_2\sin(\sqrt\nu\,t).
\]
For a zero eigenvalue,
\[
q(t)=c_1+c_2t.
\]
Thus \(A\ge0\) excludes exponentially growing linear modes, but a zero mode can produce secular growth. A uniform positive lower bound
\[
A\ge\nu_*I,\qquad \nu_*>0
\]
gives a coercive linear energy and bounded oscillatory evolution in the associated energy norm.

A symmetry zero mode is often physically harmless only after quotienting the symmetry or fixing its conserved momentum. A bifurcation zero mode usually demands nonlinear analysis. Neither case should be labeled strictly stable merely because there is no negative eigenvalue.

For homogeneous Dirichlet conditions and \(M^2\ge-M_-^2\), a sufficient condition for positivity is
\[
\lambda_1(-\Delta_h)>M_-^2,
\]
where the lapse boundedness is used to compare weighted and unweighted forms. If \(M^2\ge0\), the conclusion is immediate from the form. Quantitative lower bounds require retaining \(N_{\min}\) and \(N_{\max}\), rather than inserting them with an uncontrolled sign into a negative potential term.

## 18. A variational instability criterion

Suppose \(N=1\), and the domain contains a ball \(B_L\) of radius \(L\) on which
\[
M^2\le-\mu_*^2.
\]
Choose a Dirichlet test function supported in that ball. Then
\[
\frac{\int(|\nabla u|^2+M^2u^2)}
{\int u^2}
\le
\frac{\int|\nabla u|^2}{\int u^2}-\mu_*^2.
\]
Using the ground Dirichlet eigenfunction in the ball gives
\[
\nu_{\min}\le\lambda_1(B_L)-\mu_*^2.
\]
In three Euclidean dimensions,
\[
\lambda_1(B_L)=\frac{\pi^2}{L^2}.
\]
Hence
\[
\boxed{\mu_*L>\pi}
\]
is a sufficient condition for a negative mode in this comparison problem.

The condition is sufficient rather than necessary. A shallower but wider profile can also be unstable. A narrow negative region can remain stable because the gradient energy required to localize the field is too large. This supplies a direct mathematical reason that the pointwise condition \(M^2<0\) cannot replace a spectral calculation.

For variable lapse, the same proof uses the weighted quotient and controlled extrema of \(N\). The threshold changes quantitatively, while the competition between gradient cost and negative potential energy remains.

## 19. Static existence and the direct method

On a bounded domain with suitable boundary data, let
\[
\lambda>0,\qquad U\in L^\infty,\qquad
0<N_{\min}\le N\le N_{\max}.
\]
The static energy contains positive gradient and quartic terms. A negative quadratic coefficient can be controlled by Young's inequality:
\[
C\phi^2\le\epsilon\phi^4+\frac{C^2}{4\epsilon},
\qquad \epsilon>0.
\]
Choosing \(\epsilon\) below the available quartic coefficient gives a lower bound and controls the relevant Sobolev norm, subject to a Poincaré estimate or the quartic control of the constant mode.

A minimizing sequence is bounded in \(H^1\) and \(L^4\). On a bounded three dimensional domain, compact embedding into \(L^p\) for \(p<6\) permits a strongly convergent subsequence in \(L^4\), while the gradient term is weakly lower semicontinuous. The direct method therefore supplies an energy minimizer under these assumptions.

The minimizer solves the weak elliptic equation. Smooth coefficients and boundary regularity allow elliptic regularity to improve its regularity. Existence does not imply uniqueness. For a symmetric double well, at least a pair of sign related minimizers can occur. Metastable states, interfaces, and sign changing solutions require separate analysis.

If \(M^2=m_\phi^2+2U\ge0\), \(J=0\), and homogeneous boundary data are imposed, multiply the static equation by \(\phi\) and integrate:
\[
\int_\Omega N\left(|D\phi|^2+M^2\phi^2+\lambda\phi^4\right)dV_h=0.
\]
For \(\lambda>0\), every term is nonnegative, so \(\phi=0\). This is a useful nonexistence result for spontaneous nonzero static configurations in that parameter regime.

## 20. Nonlinear stability near an equilibrium

Let \(\phi_0\) be a static solution. The energy difference is
\[
E[\phi_0+\eta,p]-E[\phi_0,0]
=
\frac12\|p\|_{L^2(NdV_h)}^2
+\frac12\mathfrak a[\eta,\eta]
+\int_\Omega N\left(\lambda\phi_0\eta^3+\frac{\lambda}{4}\eta^4\right)dV_h
\]
for the quartic theory.

A positive quadratic form with a uniform gap controls sufficiently small perturbations if the cubic remainder is bounded by the controlled Sobolev norm. On a bounded smooth three dimensional domain,
\[
H^1\hookrightarrow L^6,
\]
so the cubic and quartic remainders can be estimated by Hölder and Sobolev inequalities. If \(\phi_0\) is bounded and the Hessian is coercive, sufficiently small perturbations remain in a neighborhood controlled by the conserved energy.

The statement is local in field amplitude and conditional on continuation of the well posed evolution. It is stronger than checking a few eigenvalues and weaker than proving global attraction. A conservative system does not generally relax to the equilibrium. It can oscillate indefinitely.

If the Hessian has symmetry zero modes, one studies orbital stability: the perturbation remains close to the symmetry orbit of the solution rather than to one fixed representative. If a genuine negative mode exists, the equilibrium is an energy saddle and linear instability is already present.

---

# Part IV. Explicit spectra and mode coupling

## 21. Exact free cylindrical modes

For \(N=1\), constant \(U=U_c\), and linearization about \(\phi_0=0\), define
\[
m_c^2=m_\phi^2+2U_c.
\]
Use
\[
u(r,\theta,z)=f_\ell(r)e^{i\ell\theta}e^{ik_zz}.
\]
The radial equation is
\[
f_\ell''+\frac1rf_\ell'
+\left(\omega^2-k_z^2-m_c^2-\frac{\ell^2}{r^2}\right)f_\ell=0.
\]
For \(k_\perp^2=\omega^2-k_z^2-m_c^2>0\),
\[
f_\ell=c_1J_{|\ell|}(k_\perp r)+c_2Y_{|\ell|}(k_\perp r).
\]
Smoothness at the axis selects \(c_2=0\). In a solid cylinder with Dirichlet outer wall \(r=R_b\),
\[
k_\perp=\frac{j_{|\ell|,s}}{R_b},
\]
where \(j_{\nu,s}\) is the \(s\)-th positive zero of \(J_\nu\). For axial period \(L_z=2\pi a\),
\[
\boxed{
\omega_{\ell ps}^2
=
\frac{j_{|\ell|,s}^2}{R_b^2}
+\frac{p^2}{a^2}
+m_c^2.
}
\]
The exact threshold for the first Dirichlet instability in this constant coefficient solid cylinder is
\[
m_c^2=-\frac{j_{0,1}^2}{R_b^2}
\]
when the axial zero mode is allowed.

For Neumann data, positive radial eigenvalues arise from zeros of \(J'_{|\ell|}\), together with the constant \(\ell=0\) radial zero mode. For an annulus, both Bessel branches are allowed and the boundary determinant selects the spectrum.

The radial normalization identity
\[
\int_0^{R_b}rJ_\ell^2\left(\frac{j_{\ell,s}r}{R_b}\right)dr
=
\frac{R_b^2}{2}J_{\ell+1}^2(j_{\ell,s})
\]
provides exact normalization and an independent quadrature check.

## 22. Cylindrical radial transformation and its endpoint

Set
\[
f_\ell(r)=r^{-1/2}\chi_\ell(r).
\]
Then
\[
\left[-\frac{d^2}{dr^2}
+\frac{\ell^2-\frac14}{r^2}
+m_\phi^2+2U(r)+k_z^2\right]\chi_\ell
=
\omega^2\chi_\ell.
\]
The coefficient \(-1/(4r^2)\) for \(\ell=0\) is the critical inverse square term generated by the measure transformation. It does not represent an independently inserted attractive physical potential.

The transformed radial Hilbert norm is
\[
\int_0^\infty r|f_\ell|^2dr=\int_0^\infty|\chi_\ell|^2dr.
\]
At the axis,
\[
\chi_\ell\sim r^{|\ell|+1/2}.
\]
For \(\ell=0\), the second local branch behaves as \(\sqrt r\log r\). The regular Cartesian scalar domain selects the first branch. A formal one dimensional inverse square Hamiltonian without that endpoint information describes a larger family of self adjoint extensions and can introduce spurious states.

In a WKB allowed region, define
\[
k_r^2(r)=\omega^2-k_z^2-m_\phi^2-2U(r)-\frac{\ell^2-\frac14}{r^2}.
\]
Then
\[
\chi(r)\sim k_r^{-1/2}
\exp\left(\pm i\int^r k_r(s)\,ds\right)
\]
requires
\[
|k_r'|\ll|k_r|^2.
\]
The approximation fails at turning points and near the singular endpoint. Airy matching or a uniform approximation is needed at a simple turning point; axis regularity is handled by the Bessel structure.

## 23. Corrugation as an external Fourier potential

Let
\[
f(\theta,\zeta)=\sin(n\theta+\delta_\theta)\cos(m\zeta+\delta_\zeta),
\qquad U=U_{\mathrm{base}}+U_1f.
\]
The four nonzero Fourier coefficients are
\[
f_{sn,tm}=\frac{s}{4i}e^{i(s\delta_\theta+t\delta_\zeta)},
\qquad s,t\in\{+1,-1\}.
\]
For the operator perturbation \(2U_1f\),
\[
\langle\ell',p'|\delta A|\ell,p\rangle
=
\frac{sU_1}{2i}e^{i(s\delta_\theta+t\delta_\zeta)}
\]
when
\[
\ell'-\ell=sn,\qquad p'-p=tm,
\]
and it vanishes otherwise, before any radial overlap is included.

In a bulk cylinder, different angular sectors have different radial eigenfunctions. The full matrix element is the displayed angular and axial coefficient times
\[
\int r\,dr\,f_{\ell's'}^*(r)f_{\ell s}(r)
\]
for a radius independent modulation, or the appropriately weighted integral for a radial envelope. The radial quantum number is not automatically conserved.

The physical field is real. Complex Fourier coefficients must satisfy
\[
q_{-\ell,-p}=q_{\ell p}^*
\]
with the corresponding radial conventions. A real sine and cosine basis avoids treating conjugate modes as independent real degrees of freedom.

## 24. Perturbative shifts and exact two mode diagonalization

For an isolated normalized eigenmode of a self adjoint operator,
\[
A=A_0+\epsilon B,
\]
ordinary perturbation theory gives
\[
\nu_a(\epsilon)
=
\nu_a^{(0)}
+\epsilon B_{aa}
+\epsilon^2\sum_{b\ne a}
\frac{|B_{ba}|^2}{\nu_a^{(0)}-\nu_b^{(0)}}
+O(\epsilon^3)
\]
when the mode is spectrally isolated and the expansion is valid.

A zero mean corrugation has zero diagonal matrix element for a constant modulus plane Fourier mode on a straight periodic cylinder. Its first nonzero nondegenerate shift is often second order. This does not imply that every degenerate multiplet has zero first order splitting.

For a pair of modes with reduced matrix
\[
\begin{pmatrix}\nu_a&v\\v^*&\nu_b\end{pmatrix},
\]
the exact two dimensional eigenvalues are
\[
\boxed{
\nu_\pm
=
\frac{\nu_a+\nu_b}{2}
\pm\sqrt{\left(\frac{\nu_a-\nu_b}{2}\right)^2+|v|^2}.
}
\]
At degeneracy, the squared frequency gap is
\[
\nu_+-\nu_-=2|v|.
\]
If both eigenvalues remain positive, the frequency gap is
\[
\omega_+-\omega_-=
\frac{2|v|}{\sqrt{\nu_+}+\sqrt{\nu_-}}.
\]
A squared frequency splitting and a frequency splitting are different observables.

The two mode formula is exact for the projected matrix. It is an approximation to the full field theory unless the two dimensional subspace is invariant or couplings to its complement have been bounded.

## 25. A fully specified second order benchmark

Consider a straight surface cylinder with
\[
R_0=1,\quad a=\frac32,\quad m_\Sigma^2=\frac14,
\quad n=2,\quad m=1,\quad U_1=\frac1{10}.
\]
The unperturbed constant mode has
\[
\nu_{00}^{(0)}=\frac14.
\]
Each of the four directly coupled modes has gap
\[
\Delta=\frac{n^2}{R_0^2}+\frac{m^2}{a^2}
=4+\frac49=\frac{40}{9}.
\]
Each coupling has magnitude \(U_1/2\). Hence
\[
\delta\nu_{00}^{(2)}
=
-4\frac{(U_1/2)^2}{\Delta}
=
-\frac{U_1^2}{\Delta}
=
-\frac9{4000}.
\]
The second order estimate is therefore exactly
\[
\boxed{\nu_{00}=\frac{991}{4000}+O(U_1^4).}
\]
The absence of an odd power in this example follows from a coordinate translation that maps \(U_1\) to \(-U_1\), leaving the periodic domain invariant.

The computations later in the monograph compare this analytical estimate with the full Fourier Galerkin spectrum at several cutoffs. That comparison quantifies the accuracy of the perturbative truncation for a declared parameter value.

This potential benchmark is distinct from changing the surface metric itself. A corrugated metric with constant mass retains an exact constant Laplace–Beltrami eigenfunction; a nonconstant external potential generally does not.

## 26. Bloch sectors, lattice connectivity, and parity

For an infinite tube with axial period
\[
L_{\mathrm{cell}}=\frac{2\pi a}{m},
\]
write
\[
u(\theta,z)=e^{iqz}v_q(\theta,z),
\qquad v_q(\theta,z+L_{\mathrm{cell}})=v_q(\theta,z).
\]
The quasimomentum is defined modulo \(m/a\). A standard Brillouin interval is
\[
-\frac{m}{2a}\le q<\frac{m}{2a}.
\]
Finite periodic cells sample a discrete set of these quasimomenta. Their discrete eigenvalues are not the entire infinite system band structure.

Repeated application of the elementary shifts \((\pm n,\pm m)\) connects
\[
(\ell,p)\longrightarrow(\ell+an,p+bm)
\]
only when
\[
a\equiv b\pmod2.
\]
Indeed, each elementary step changes both scaled indices by an odd integer. Conversely, integer combinations of \((n,m)\) and \((n,-m)\) generate every pair with that parity condition.

The coefficient is invariant under
\[
(\theta,\zeta)\mapsto
\left(\theta+\frac\pi n,\zeta+\frac\pi m\right),
\]
because both trigonometric factors change sign. This additional combined translation explains the parity selection rule. The separate periods \(2\pi/n\) and \(2\pi/m\) do not exhaust the discrete structure.

The connectivity rule applies to repeated scattering by this potential. Other harmonics, boundaries, disorder, or nonlinear interactions can connect sectors that the pure quadratic modulation leaves separate.

## 27. Phase offsets and observable registration

For a perfectly periodic domain with otherwise translation invariant coefficients,
\[
\theta'=\theta+\frac{\delta_\theta}{n},
\qquad
\zeta'=\zeta+\frac{\delta_\zeta}{m}
\]
removes both phase offsets. The corresponding operators are related by a unitary coordinate translation. Their spectra are exactly identical.

The offsets become observable relative to another structure: a boundary, defect, source, anisotropic material axis, detector location, or second modulation. Spectral changes then depend on relative phases, not on an absolute origin assigned to one isolated sinusoid.

This observation provides both an inference restriction and a numerical test. A periodic implementation with no other registered structure should give phase independent eigenvalues. If changing only \(\delta_\theta,\delta_\zeta\) shifts its converged spectrum, either the intended symmetry has been broken by the discretization or the actual model includes an additional registered feature.

Eigenfunctions themselves translate with the pattern. A detector fixed in laboratory coordinates can therefore measure a changing mode amplitude at its position even when the eigenvalues are invariant.

## 28. Localized modes, band edges, and far field conditions

For an asymptotically constant flat bulk coefficient,
\[
U(\mathbf x)\to U_\infty,
\]
the free continuum begins at
\[
\nu_{\mathrm{edge}}=m_\phi^2+2U_\infty
\]
in the unrestricted three dimensional problem. In a fixed axial sector, add \(k_z^2\). In a waveguide, add the lowest transverse threshold appropriate to the boundary conditions.

A stable bound state requires
\[
0<\nu_{\mathrm{bound}}<\nu_{\mathrm{edge}}.
\]
A negative eigenvalue is spatially localized in some problems but dynamically unstable. Localization is not synonymous with stability.

If the angular and axial corrugation persists at arbitrarily large radius, its zero mean does not make it disappear from the far field operator. The proper continuum or band threshold belongs to that limiting periodic or anisotropic operator. Dropping a coefficient because its average is zero is not an asymptotic theorem.

For a genuinely axisymmetric, \(z\)-independent, constant positive mass far field, the static linear radial equation is
\[
\phi_{rr}+\frac1r\phi_r-m_\infty^2\phi=0.
\]
The decaying branch is
\[
\phi\propto K_0(m_\infty r),
\qquad
K_0(m_\infty r)\sim
\sqrt{\frac{\pi}{2m_\infty r}}e^{-m_\infty r}.
\]
This describes a tail, not a globally regular isolated solution. The \(K_0\) branch is logarithmically singular at the axis and must be matched to an interior solution or used outside a source region.

---

# Part V. Nonlinear dynamics and controlled approximations

## 29. Uniform vacua and fluctuation masses

When \(U=U_c\) is constant and gradients vanish, stationary points satisfy
\[
\phi\left(m_c^2+\lambda\phi^2\right)=0,
\qquad m_c^2=m_\phi^2+2U_c.
\]
For \(\lambda>0\):

- If \(m_c^2>0\), the unique minimum is \(\phi=0\).
- If \(m_c^2=0\), the minimum is quartically flat at quadratic order.
- If \(m_c^2<0\), there are two minima
\[
\phi=\pm v,\qquad v^2=-\frac{m_c^2}{\lambda}.
\]

At a broken minimum,
\[
M_{\mathrm{fluc}}^2=W''(v)
=m_c^2+3\lambda v^2=-2m_c^2.
\]
The potential difference is
\[
W(v)-W(0)=-\frac{(m_c^2)^2}{4\lambda}.
\]
The notation \((m_c^2)^2\) emphasizes that \(m_c^2\) may be negative.

For nonconstant \(U\), the pointwise expression
\[
v_{\mathrm{local}}(x)=
\sqrt{-\frac{m_\phi^2+2U(x)}{\lambda}}
\]
is at most a local approximation where its radicand is positive. Substitution into the full static equation leaves gradient terms. Its accuracy requires the spatial variation scale to exceed the local healing length and fails near zeros of the radicand.

## 30. Gradient correction to a slowly varying broken state

Let
\[
b(x)=m_\phi^2+2U(x)<0,
\qquad
v(x)=\sqrt{-b(x)/\lambda}.
\]
Define the weighted spatial operator
\[
L_Nf=\frac1{N\sqrt h}\partial_i(N\sqrt h\,h^{ij}\partial_jf).
\]
The static equation is
\[
-L_N\phi+b\phi+\lambda\phi^3=0.
\]
Set
\[
\phi=v+\delta v.
\]
Since \(bv+\lambda v^3=0\), the linearized correction satisfies
\[
\left[-L_N-2b\right]\delta v=L_Nv
\]
up to quadratic terms in \(\delta v\).

If derivatives of the correction are small compared with \(|b|\delta v\),
\[
\boxed{\delta v\simeq\frac{L_Nv}{-2b}.}
\]
A sufficient local expansion parameter has the form
\[
\epsilon_{\mathrm{grad}}
\sim
\frac1{|b|L_U^2}\ll1,
\]
with additional control on derivatives of \(N\) and \(b\). The correction grows near \(b=0\), showing explicitly why a local algebraic vacuum approximation loses control at an interface between symmetric and broken regions.

The exact inverse
\[
\delta v=\left[-L_N-2b\right]^{-1}L_Nv
\]
is nonlocal. The local expression is the first term in a derivative expansion of that inverse.

## 31. Bifurcation from a simple zero eigenvalue

Let a control parameter \(s\) vary the linear operator \(A_s\), and suppose at \(s=s_c\),
\[
A_{s_c}u_0=0,\qquad
\langle u_0,u_0\rangle_{\mathcal H}=1,
\]
with a simple kernel and a positive spectral gap on its orthogonal complement. Assume a \(\phi\mapsto-\phi\) symmetric quartic theory.

Write
\[
\phi=a\,u_0+w,\qquad
\langle u_0,w\rangle_{\mathcal H}=0.
\]
Solving the complementary equation gives
\[
w=O(a^3,a(s-s_c))
\]
under the invertibility hypothesis. Projection onto \(u_0\) yields
\[
0=\nu_0(s)a+\lambda C_4a^3+\text{higher terms},
\]
where
\[
C_4=\int_\Omega N\,u_0^4\,dV_h>0.
\]
Therefore the leading nonzero branch satisfies
\[
\boxed{a^2=-\frac{\nu_0(s)}{\lambda C_4}.}
\]
For \(\lambda>0\), a branch emerges on the side \(\nu_0(s)<0\). This is the usual supercritical pitchfork structure in the reduced problem.

A degenerate kernel requires a multicomponent amplitude equation. A source or odd scalar interaction generally unfolds the pitchfork. A sign change in a pointwise mass is not sufficient to identify \(s_c\); the zero eigenvalue of the global weighted problem defines it.

## 32. Exact real mode projection

Take a real orthonormal basis
\[
\langle u_a,u_b\rangle_{\mathcal H}=\delta_{ab},
\qquad
Au_a=\nu_au_a,
\]
and expand
\[
\phi(t,x)=\sum_aq_a(t)u_a(x)
\]
about the zero background. Substituting in the action gives
\[
L_{\mathrm{modes}}
=
\frac12\sum_a\dot q_a^2
-\frac12\sum_a\nu_aq_a^2
-\frac{\lambda}{4}\sum_{abcd}C_{abcd}q_aq_bq_cq_d,
\]
with
\[
\boxed{C_{abcd}=\int_\Omega N\,u_au_bu_cu_d\,dV_h.}
\]
The exact infinite mode equations are
\[
\ddot q_a+\nu_aq_a+\lambda\sum_{bcd}C_{abcd}q_bq_cq_d=0.
\]
The \(N\) weight in the quartic overlap differs from the \(1/N\) weight in the mode normalization.

A finite mode truncation is an approximation, but deriving it from the truncated action preserves its Hamiltonian structure exactly:
\[
E_{\mathrm{trunc}}
=
\frac12\sum_a\dot q_a^2+\frac12\sum_a\nu_aq_a^2
+\frac{\lambda}{4}\sum_{abcd}C_{abcd}q_aq_bq_cq_d.
\]
A projection that uses inconsistent quadrature or mismatched weights need not conserve this energy.

Around a nonzero \(\phi_0\), cubic terms in the fluctuation action generate quadratic terms in the fluctuation equations. The zero background four mode expression should not be reused without those terms.

## 33. Single mode dynamics and the exact Duffing solution

For a single normalized real mode, define
\[
g=\lambda C_4.
\]
The reduced equation is
\[
\ddot q+\omega_0^2q+gq^3=0.
\]
For \(g>0\), \(\omega_0^2>0\), and
\[
q(0)=A_q,\qquad\dot q(0)=0,
\]
an exact solution is
\[
\boxed{
q(t)=A_q\,\operatorname{cn}(\Omega t,k),
}
\]
where
\[
\Omega^2=\omega_0^2+gA_q^2,
\qquad
k^2=\frac{gA_q^2}{2(\omega_0^2+gA_q^2)}.
\]
Here the Jacobi elliptic function has modulus \(k\). Software often takes the parameter \(k^2\), which must be distinguished from \(k\).

The exact period is
\[
T=\frac{4K(k)}{\Omega},
\]
where
\[
K(k)=\int_0^{\pi/2}\frac{d\alpha}{\sqrt{1-k^2\sin^2\alpha}}.
\]
The physical oscillation frequency is
\[
\omega_{\mathrm{nl}}=\frac{2\pi}{T}.
\]
Its small amplitude expansion is
\[
\omega_{\mathrm{nl}}
=
\omega_0
+\frac{3gA_q^2}{8\omega_0}
-\frac{21g^2A_q^4}{256\omega_0^3}
+O(A_q^6).
\]

The exact oscillator supplies an independent numerical benchmark. It does not prove that the field remains in one mode. Field mode leakage is small only if the generated harmonics and combination frequencies remain sufficiently detuned from other modes and the nonlinear overlap coefficients are controlled.

## 34. Resonance, leakage, and the limits of a modal reduction

A cubic nonlinearity acting on \(q\propto\cos\omega t\) generates
\[
\cos^3\omega t=\frac34\cos\omega t+\frac14\cos3\omega t.
\]
Thus another mode near \(3\omega\) can be resonantly excited even when its initial amplitude is zero. More generally, four wave interactions involve combinations
\[
\pm\omega_a\pm\omega_b\pm\omega_c\pm\omega_d.
\]
A small coefficient is not sufficient for a uniform long time approximation when a denominator approaches zero.

A controlled reduction should declare:

1. The retained mode subspace.
2. The size of the initial discarded component.
3. The nonlinear amplitude parameter.
4. The smallest relevant detuning.
5. The time interval over which the error is claimed.
6. The conserved quantities used to monitor leakage.

For a driven mode, the distinction between resonant transfer, parametric growth, and static spectral mixing is essential. A static corrugation mixes eigenfunctions and shifts frequencies. A time varying corrugation can supply energy and produce parametric instability. A conservative quartic interaction redistributes energy among modes without supplying net energy.

These mechanisms can coexist, but their diagnostic signatures differ.

## 35. Parametric modulation as an explicitly powered system

Suppose a projected mode obeys
\[
\ddot q+\left[\omega_0^2+\epsilon\cos(\Omega_dt)\right]q=0.
\]
Near the primary resonance \(\Omega_d=2\omega_0\), weak modulation produces Mathieu type instability. At exact resonance, the leading amplitude growth exponent is
\[
\Gamma_{\mathrm{par}}=\frac{|\epsilon|}{4\omega_0}
\]
under the small modulation assumption
\[
|\epsilon|\ll\omega_0^2.
\]
For detuning \(\delta=\Omega_d-2\omega_0\), the leading resonance tongue satisfies
\[
\Gamma_{\mathrm{par}}^2
=
\left(\frac{\epsilon}{4\omega_0}\right)^2-\left(\frac\delta2\right)^2.
\]
This is an asymptotic formula, not an exact arbitrary amplitude result.

The work source is the explicitly time dependent coefficient:
\[
\dot E=\frac12\dot{\omega^2}(t)q^2.
\]
In a geometric realization, the actuator or mechanical mode supplying the modulation must lose the energy gained by the field, unless it is externally powered. A growing wave in a prescribed time dependent geometry is therefore not evidence of energy production by a passive static structure.

Adding damping changes the instability threshold. If the equation contains \(2\gamma\dot q\), the leading net growth exponent is \(\Gamma_{\mathrm{par}}-\gamma\) at exact resonance.

## 36. Domain walls and a useful exact nonlinear solution

For a one dimensional real scalar with
\[
W(\phi)=\frac{\lambda}{4}(\phi^2-v^2)^2,
\]
the static equation is
\[
-\phi''+\lambda\phi(\phi^2-v^2)=0.
\]
Multiply by \(\phi'\):
\[
\frac{d}{dx}\left[-\frac12(\phi')^2+W(\phi)\right]=0.
\]
A wall connecting \(-v\) and \(+v\) has vanishing integration constant, so
\[
\frac12(\phi')^2=W(\phi).
\]
Integration gives
\[
\boxed{
\phi_{\mathrm{wall}}(x)=v\tanh\left(v\sqrt{\frac\lambda2}(x-x_0)\right).
}
\]
Its characteristic width is
\[
\ell_{\mathrm{wall}}=\frac{\sqrt2}{v\sqrt\lambda},
\]
and its energy per transverse area is
\[
\boxed{
\sigma_{\mathrm{wall}}=\frac{2\sqrt{2\lambda}}{3}v^3.
}
\]

This wall is protected by differing boundary vacua in one transverse direction. A closed bubble in three dimensions has additional curvature and pressure dynamics. The planar wall formula does not establish a stable localized particle in three dimensions.

A slowly varying external \(U\) can pin or distort a wall. A first collective coordinate approximation inserts \(\phi_{\mathrm{wall}}(x-X(t))\) into the action and computes the induced potential for \(X\). Its validity depends on weak deformation and separation from internal wall modes.

## 37. Scaling obstruction for static isolated lumps

Consider a real scalar in \(d\) flat spatial dimensions with
\[
E[\phi]=T+V_{\mathrm{int}},
\]
where
\[
T=\frac12\int|\nabla\phi|^2d^dx,\qquad
V_{\mathrm{int}}=\int W(\phi)d^dx.
\]
Assume finite energy, fixed vacuum at infinity, no external spatial scale, and \(W\ge0\). Under
\[
\phi_\ell(x)=\phi(x/\ell),
\]
the energy is
\[
E(\ell)=\ell^{d-2}T+\ell^dV_{\mathrm{int}}.
\]
A stationary solution must satisfy
\[
(d-2)T+dV_{\mathrm{int}}=0.
\]
For \(d\ge3\), every term is nonnegative, so a nontrivial finite energy static lump is excluded under these hypotheses.

The conclusion changes if one changes the assumptions: a boundary, external potential, gauge field, higher derivative term, nontrivial topology, time dependent charge carrying field, or gravity can change the scaling balance. Each mechanism needs its own stability analysis. The presence of a corrugated shape alone is not a derivation of particlelike localization.

This scaling calculation is included explicitly so that claims of self confinement can be checked against the actual energy functional rather than inferred from a visually localized waveform.

## 38. Characteristics and the two different WKB limits

For the scalar PDE, the principal symbol is
\[
P(x,k)=g^{\mu\nu}k_\mu k_\nu.
\]
Its characteristic covectors satisfy
\[
P(x,k)=0.
\]
Mass, external potential, and polynomial self interaction are lower order terms and do not change this characteristic cone.

For
\[
\phi=Ae^{iS/\epsilon}
\]
in
\[
(\Box-M^2)\phi=0
\]
with fixed \(M\), the leading order \(\epsilon^{-2}\) equation is
\[
g^{\mu\nu}\partial_\mu S\partial_\nu S=0.
\]
This is the high frequency limit at fixed mass.

A different scaling,
\[
(\epsilon^2\Box-M^2)\phi=0,
\]
gives at leading order
\[
g^{\mu\nu}\partial_\mu S\partial_\nu S+M^2=0.
\]
This is a massive Hamilton–Jacobi or semiclassical scaling. Restoring \(\hbar\), it corresponds to keeping the physical mass fixed while the wave operator carries \(\hbar^2\).

In a locally constant medium,
\[
\omega^2=|\mathbf k|^2+M^2,
\qquad
v_g=\frac{|\mathbf k|}{\sqrt{|\mathbf k|^2+M^2}}<1.
\]
The group speed of a massive wave packet and the characteristic front speed answer different questions. A field with a mass term still has the metric null cone as its front propagation cone.

---

# Part VI. Exact corrugated surface geometry

## 39. Tangent vectors and first fundamental form

Write
\[
X(\theta,\zeta)=R(\theta,\zeta)e_r(\theta)+a\zeta e_z,
\]
with
\[
e_r=(\cos\theta,\sin\theta,0),\qquad
e_\theta=(-\sin\theta,\cos\theta,0).
\]
Then
\[
X_\theta=R_\theta e_r+Re_\theta,\qquad
X_\zeta=R_\zeta e_r+ae_z.
\]
Define
\[
E=R^2+R_\theta^2,\qquad
B=R_\theta R_\zeta,\qquad
G=a^2+R_\zeta^2.
\]
The induced metric is
\[
\boxed{
\gamma_{ab}=
\begin{pmatrix}E&B\\B&G\end{pmatrix}.
}
\]
Its determinant is
\[
\boxed{
D=EG-B^2=a^2(R^2+R_\theta^2)+R^2R_\zeta^2.
}
\]
The inverse is
\[
\boxed{
\gamma^{ab}
=
\frac1D
\begin{pmatrix}G&-B\\-B&E\end{pmatrix}.
}
\]
The area element is
\[
dA=\sqrt D\,d\theta\,d\zeta.
\]

For \(R>0\) and \(a>0\),
\[
D\ge a^2R^2>0.
\]
This gives an exact positivity proof, independent of numerical sampling. On a compact cell with bounded derivatives and a positive radius lower bound, the induced metric is uniformly positive definite.

For the harmonic radius,
\[
R_\theta=An\cos(n\theta+\delta_\theta)\cos(m\zeta+\delta_\zeta),
\]
\[
R_\zeta=-Am\sin(n\theta+\delta_\theta)\sin(m\zeta+\delta_\zeta),
\]
\[
R_{\theta\theta}=-An^2\sin(n\theta+\delta_\theta)\cos(m\zeta+\delta_\zeta),
\]
\[
R_{\zeta\zeta}=-Am^2\sin(n\theta+\delta_\theta)\cos(m\zeta+\delta_\zeta),
\]
\[
R_{\theta\zeta}=-Anm\cos(n\theta+\delta_\theta)\sin(m\zeta+\delta_\zeta).
\]

## 40. Unit normal and second fundamental form

The oriented cross product is
\[
X_\theta\times X_\zeta
=
aRe_r-aR_\theta e_\theta-RR_\zeta e_z.
\]
Choose the outward unit normal
\[
\boxed{
\mathbf n=
\frac{aRe_r-aR_\theta e_\theta-RR_\zeta e_z}{\sqrt D}.
}
\]
The second derivatives are
\[
X_{\theta\theta}=(R_{\theta\theta}-R)e_r+2R_\theta e_\theta,
\]
\[
X_{\theta\zeta}=R_{\theta\zeta}e_r+R_\zeta e_\theta,
\]
\[
X_{\zeta\zeta}=R_{\zeta\zeta}e_r.
\]
Use the convention
\[
b_{ab}=-\mathbf n\cdot X_{ab}.
\]
Then
\[
\boxed{
b_{\theta\theta}
=
\frac a{\sqrt D}
\left(R^2+2R_\theta^2-RR_{\theta\theta}\right),
}
\]
\[
\boxed{
b_{\theta\zeta}
=
\frac a{\sqrt D}
\left(R_\theta R_\zeta-RR_{\theta\zeta}\right),
}
\]
\[
\boxed{
b_{\zeta\zeta}
=
-\frac{aR}{\sqrt D}R_{\zeta\zeta}.
}
\]
For a straight cylinder, \(R=R_0\), these give
\[
b_{\theta\theta}=R_0,\qquad
b_{\zeta\zeta}=0.
\]
The principal curvatures are \(1/R_0\) and \(0\), so
\[
H=\frac1{2R_0},\qquad K_G=0.
\]
Reversing the normal changes \(b\) and \(H\) by a sign but leaves \(K_G\) and \(H^2\) unchanged.

## 41. Exact intrinsic and extrinsic curvature

The mean curvature is
\[
\boxed{
H=
\frac{Gb_{\theta\theta}-2Bb_{\theta\zeta}+Eb_{\zeta\zeta}}{2D}.
}
\]
The Gaussian curvature is
\[
\boxed{
K_G=
\frac{b_{\theta\theta}b_{\zeta\zeta}-b_{\theta\zeta}^2}{D}.
}
\]
The intrinsic scalar curvature is
\[
\boxed{\mathcal R_\Sigma=2K_G.}
\]
The squared second fundamental form is
\[
|b|^2=b_{ab}b^{ab}=4H^2-2K_G.
\]
If \(k_1,k_2\) are principal curvatures,
\[
H^2-K_G=\frac14(k_1-k_2)^2\ge0.
\]
This identity is an exact independent algebraic check on a geometry implementation. Its numerical evaluation should remain nonnegative up to arithmetic and differentiation errors.

The straight cylinder is intrinsically flat and extrinsically curved. Therefore an intrinsic term \(\xi\mathcal R_\Sigma\varphi^2\) vanishes on it, while an extrinsic term proportional to \(H^2\varphi^2\) does not. These couplings are physically distinguishable and should not be grouped into one unspecified “curvature.”

For a smooth periodic metric on an abstract two torus,
\[
\int_\Sigma K_G\,dA=2\pi\chi(\Sigma)=0.
\]
The numerical benchmark checks this integral on the periodic cell. Local \(K_G\) need not vanish; positive and negative contributions cancel globally.

## 42. Exact Laplace–Beltrami operator

The scalar surface Laplacian is
\[
\Delta_\gamma\varphi
=
\frac1{\sqrt D}\partial_a\left(\sqrt D\,\gamma^{ab}\partial_b\varphi\right).
\]
Substituting the inverse metric gives
\[
\boxed{
\begin{aligned}
\Delta_\gamma\varphi
={}&
\frac1{\sqrt D}\partial_\theta
\left[
\frac{G}{\sqrt D}\varphi_\theta
-\frac{B}{\sqrt D}\varphi_\zeta
\right]\\
&+
\frac1{\sqrt D}\partial_\zeta
\left[
-\frac{B}{\sqrt D}\varphi_\theta
+\frac{E}{\sqrt D}\varphi_\zeta
\right].
\end{aligned}
}
\]
This expression is exact for the radial graph. It includes both metric anisotropy and mixed derivatives.

For periodic fields,
\[
\int_\Sigma u^*(-\Delta_\gamma v)\,dA
=
\int_\Sigma\gamma^{ab}\partial_au^*\partial_bv\,dA.
\]
Thus \(-\Delta_\gamma\) is nonnegative and
\[
\Delta_\gamma1=0
\]
exactly. On a connected compact surface, the constant functions span its zero eigenspace.

For \(A=0\),
\[
\Delta_\gamma
=
\frac1{R_0^2}\partial_\theta^2+\frac1{a^2}\partial_\zeta^2.
\]
The exact free surface spectrum is
\[
\nu_{\ell p}
=
\frac{\ell^2}{R_0^2}+\frac{p^2}{a^2}+m_\Sigma^2+2U_c.
\]
This is distinct from the bulk spectrum: there is no independent radial Bessel index after the normal degree of freedom has been removed.

## 43. Controlled small amplitude geometry expansion

Write
\[
R=R_0+\eta(\theta,\zeta).
\]
A small radius displacement is not the only required small quantity. For a controlled metric expansion, require
\[
\frac{|\eta|}{R_0}\ll1,\qquad
\frac{|\eta_\theta|}{R_0}\ll1,\qquad
\frac{|\eta_\zeta|}{a}\ll1.
\]
For the harmonic corrugation this includes
\[
\frac{|A|}{R_0}\ll1,\qquad
\frac{|A|n}{R_0}\ll1,\qquad
\frac{|A|m}{a}\ll1.
\]
Curvature expansions additionally involve second derivatives, so high harmonic number can amplify curvature even when the radius modulation is small.

Through quadratic order in a common amplitude parameter,
\[
\sqrt D
=
aR_0+a\eta
+\frac a{2R_0}\eta_\theta^2
+\frac{R_0}{2a}\eta_\zeta^2
+O(\eta^3)
\]
with derivatives counted at fixed harmonic numbers. A pure \(\eta^2\) term cancels in the area element.

For the zero mean harmonic profile,
\[
\frac{\operatorname{Area}}{4\pi^2aR_0}
=
1+\frac{A^2}{8}
\left(\frac{n^2}{R_0^2}+\frac{m^2}{a^2}\right)
+O(A^4).
\]
The area is even in \(A\) because a phase translation sends \(A\) to \(-A\). The absence of a cubic integrated term uses that symmetry and should not be assumed for an arbitrary perturbation.

## 44. First variation of the surface wave operator

To first order,
\[
\sqrt D=a(R_0+\eta)+O(\eta^2),
\]
\[
\sqrt D\,\gamma^{\theta\theta}
=
\frac a{R_0}-\frac a{R_0^2}\eta+O(\eta^2),
\]
\[
\sqrt D\,\gamma^{\zeta\zeta}
=
\frac{R_0}{a}+\frac\eta a+O(\eta^2),
\qquad
\sqrt D\,\gamma^{\theta\zeta}=O(\eta^2).
\]
Expanding the full divergence form gives
\[
\boxed{
\Delta_\gamma
=
\Delta_0
-\frac{2\eta}{R_0^3}\partial_\theta^2
-\frac{\eta_\theta}{R_0^3}\partial_\theta
+\frac{\eta_\zeta}{a^2R_0}\partial_\zeta
+O(\eta^2).
}
\]
There is no first order \(\eta\,\partial_\zeta^2\) term after the inverse area factor is included. The two contributions cancel.

The first order operator written in the unperturbed coordinate measure need not look Hermitian by itself, because the Hilbert space measure changes with the geometry. The safe perturbation formula uses both stiffness and mass variations.

Let
\[
\mathsf K(\epsilon)u=\nu(\epsilon)\mathsf M(\epsilon)u,
\qquad u^\dagger\mathsf M_0u=1.
\]
Then
\[
\boxed{
\nu'(0)=u^\dagger\left[\mathsf K'(0)-\nu(0)\mathsf M'(0)\right]u.
}
\]
This generalized Hellmann–Feynman formula handles the varying measure directly. Ignoring \(\mathsf M'\) can produce a false geometric frequency shift.

## 45. First curvature variation around a cylinder

For an outward normal displacement \(\eta\) of a straight cylinder, the standard variation identity in the stated convention is
\[
\delta(2H)=-\left(\Delta_0+|b_0|^2\right)\eta.
\]
Since \(|b_0|^2=R_0^{-2}\),
\[
\boxed{
H
=
\frac1{2R_0}
-\frac12\left[
\frac{\eta_{\theta\theta}}{R_0^2}
+\frac{\eta_{\zeta\zeta}}{a^2}
+\frac{\eta}{R_0^2}
\right]
+O(\eta^2).
}
\]
The first Gaussian curvature correction is
\[
\boxed{
K_G=-\frac{\eta_{\zeta\zeta}}{a^2R_0}+O(\eta^2).
}
\]
For a radius depending only on \(\theta\), the surface is a generalized cylinder and its Gaussian curvature vanishes exactly. The absence of a first order \(\eta_{\theta\theta}\) term in \(K_G\) is consistent with that geometric fact.

For the harmonic displacement,
\[
\delta H=
\frac A2
\left[
\frac{n^2-1}{R_0^2}+\frac{m^2}{a^2}
\right]
\sin(n\theta+\delta_\theta)\cos(m\zeta+\delta_\zeta),
\]
\[
\delta K_G=
\frac{Am^2}{a^2R_0}
\sin(n\theta+\delta_\theta)\cos(m\zeta+\delta_\zeta).
\]
The intrinsic and extrinsic curvature responses therefore carry different dependence on the harmonic integers. Measuring several harmonic families can, in principle, distinguish their couplings.

## 46. Surface field action and worldvolume curvature

For a prescribed static surface with lapse \(N_\Sigma\),
\[
ds_\Sigma^2=-N_\Sigma^2dt^2+\gamma_{ab}d\sigma^ad\sigma^b.
\]
The intrinsic surface action is
\[
S_\Sigma
=
\int dt\,d^2\sigma\,N_\Sigma\sqrt\gamma
\left[
\frac{\dot\varphi^2}{2N_\Sigma^2}
-\frac12\gamma^{ab}\partial_a\varphi\partial_b\varphi
-V_\Sigma(\varphi)-U_\Sigma\varphi^2
\right].
\]
Its equation is
\[
-\frac1{N_\Sigma^2}\varphi_{tt}
+\frac1{N_\Sigma\sqrt\gamma}
\partial_a(N_\Sigma\sqrt\gamma\,\gamma^{ab}\partial_b\varphi)
-V_\Sigma'(\varphi)-2U_\Sigma\varphi=0.
\]
All of the weighted spectral formulas carry over with \(dV_h\) replaced by \(dA\).

The scalar curvature of the \(2+1\) dimensional static worldvolume is
\[
\mathcal R[q]
=
\mathcal R_\Sigma-\frac2{N_\Sigma}\Delta_\gamma N_\Sigma.
\]
For \(N_\Sigma=1\),
\[
\mathcal R[q]=2K_G.
\]
For nonconstant lapse, coupling to the spacetime worldvolume curvature and coupling to the curvature of its spatial slices are different theories.

The conformal coupling in \(D\) spacetime dimensions is
\[
\xi_D=\frac{D-2}{4(D-1)}.
\]
Thus a \(2+1\) dimensional worldvolume scalar has \(\xi_3=1/8\), whereas a \(3+1\) dimensional bulk scalar has \(\xi_4=1/6\). Transferring the bulk coefficient to the surface without a derivation changes the conformal theory.

## 47. Intrinsic coupling, extrinsic coupling, and thin confinement

A local surface coefficient can be written
\[
U_\Sigma
=
\frac12\xi_{\mathrm{int}}\mathcal R_\Sigma
+\alpha_HH^2+\alpha_KK_G.
\]
Because \(\mathcal R_\Sigma=2K_G\), only one linear combination of \(\xi_{\mathrm{int}}\) and \(\alpha_K\) is independent in this basis. The \(H^2\) term is independent because it depends on the embedding.

A separate construction starts with a nonrelativistic particle in three dimensions, confines it strongly in the normal direction, and subtracts the transverse ground energy. Under the thin layer assumptions, the effective surface Hamiltonian contains
\[
\boxed{
V_{\mathrm{geom}}
=
-\frac{\hbar^2}{2m_{\mathrm p}}(H^2-K_G).
}
\]
This confinement generated potential is associated with [da Costa, Quantum mechanics of a constrained particle](https://link.aps.org/doi/10.1103/PhysRevA.23.1982). It is not an automatic term in every classical or relativistic scalar theory on a surface.

For a straight cylinder,
\[
V_{\mathrm{geom}}=-\frac{\hbar^2}{8m_{\mathrm p}R_0^2}.
\]
For a sphere, \(H^2=K_G\), so this particular potential vanishes. The contrast illustrates its dependence on anisotropy of the principal curvatures rather than on intrinsic curvature alone.

A microscopic derivation must state the confinement potential, transverse state, separation of scales, and the order of limits. One should not insert this coefficient into the relativistic model solely because both systems involve a curved surface.

---

# Part VII. Dynamical surfaces and material closure

## 48. A surface that moves requires a new kinematic specification

A time dependent embedding
\[
X=X(t,\sigma^1,\sigma^2)
\]
does not generally produce a block diagonal induced spacetime metric. If the ambient spacetime is Minkowski and the worldvolume embedding is
\[
Y^\mu=(t,X^I),
\]
then
\[
q_{tt}=-1+|\dot X|^2,\qquad
q_{ta}=\dot X\cdot X_a,\qquad
q_{ab}=X_a\cdot X_b.
\]
A lapse and shift decomposition can be applied to this metric, but one cannot simply replace the static spatial metric by \(\gamma_{ab}(t)\) while keeping every other component unchanged.

There are two useful physical models:

1. A relativistic worldvolume theory with its induced Lorentzian metric.
2. A nonrelativistic elastic membrane with material time, inertia, bending energy, and a scalar propagating or relaxing on the moving surface.

These choices differ in kinetic terms, characteristic speeds, constraints, and the interpretation of reparameterization invariance. The static geometry formulas are shared, but the evolution laws are not.

For a material membrane, tangential motion can carry physical labels, density, and strain. For a fluid membrane, tangential reparameterization can partly be gauge freedom. The constitutive model decides which variables are physical.

## 49. Static elastic functional and shape variation

For a nonrelativistic static membrane, a definite energy is
\[
E_{\mathrm{mem}}
=
\int_\Sigma
\left[
\sigma+\frac{\kappa_b}{2}(2H-C_0)^2+\kappa_GK_G
\right]dA-p_{\mathrm{ext}}\mathcal V.
\]
Here \(\sigma\) is surface tension, \(\kappa_b\) is bending stiffness, \(C_0\) is spontaneous curvature, and \(p_{\mathrm{ext}}\) is a pressure difference defined by the sign of the volume term.

Under an outward normal displacement
\[
\delta X=f\mathbf n,
\]
the stated curvature convention gives
\[
\delta\gamma_{ab}=2fb_{ab},
\qquad
\delta dA=2Hf\,dA,
\]
\[
\delta(2H)=-\Delta_\gamma f-|b|^2f,
\qquad
\delta\mathcal V=\int_\Sigma f\,dA.
\]
For a closed surface with fixed topology, constant \(\kappa_G\) contributes only a topological constant. It affects boundary conditions on an open surface, and a variable \(\kappa_G\) is not topological.

Set \(C=2H\). After integrating by parts on a closed surface, the normal Euler derivative is
\[
\boxed{
\frac1{dA}\frac{\delta E_{\mathrm{mem}}}{\delta f}
=
2\sigma H-p_{\mathrm{ext}}
+\kappa_b\left[
-\Delta_\gamma C
-(C-C_0)|b|^2
+H(C-C_0)^2
\right].
}
\]
For \(C_0=0\), this becomes
\[
2\sigma H-p_{\mathrm{ext}}
-2\kappa_b\left[\Delta_\gamma H+2H(H^2-K_G)\right]=0.
\]
For a sphere, the bending contribution vanishes when \(C_0=0\), and the tension pressure balance is \(p_{\mathrm{ext}}=2\sigma H\), consistent with the sign convention.

The relation between membrane stresses, normal shape balance, and tangential identities is developed in [Capovilla and Guven, Stresses in lipid membranes](https://arxiv.org/abs/cond-mat/0203148). The explicit variation above fixes the conventions used here.

## 50. Scalar stress acting on a surface

Add a static scalar energy
\[
E_\varphi
=
\int_\Sigma
\left[\frac12\gamma^{ab}\partial_a\varphi\partial_b\varphi
+W_\Sigma(\varphi)\right]dA,
\]
initially taking \(W_\Sigma\) independent of curvature and holding the material scalar coordinate values fixed during the normal variation.

Since
\[
\delta\gamma^{ab}=-2fb^{ab},
\]
one obtains
\[
\boxed{
\delta E_\varphi
=
\int_\Sigma f
\left[
2H\left(\frac12|D\varphi|^2+W_\Sigma\right)
-b^{ab}\partial_a\varphi\partial_b\varphi
\right]dA.
}
\]
The total shape equation is the membrane Euler derivative plus this scalar force density.

This explicitly closes one version of geometry field back reaction. The field modifies the shape through its gradient stress and potential energy. The resulting shape modifies the Laplace–Beltrami operator governing the field.

If \(W_\Sigma\) contains \(H^2\varphi^2\) or \(K_G\varphi^2\), further curvature variation terms appear. They include derivatives of \(\varphi^2\) after integration by parts. Such terms cannot be represented solely by replacing \(W_\Sigma\) in the algebraic expression above.

A static prescribed corrugation need not solve the total shape equation. It may be maintained by external forces, boundary constraints, material inhomogeneity, or an actuator. Those supports should be declared if mechanical equilibrium is claimed.

## 51. Dynamical membrane energy balance

A nonrelativistic membrane can be assigned kinetic energy
\[
T_X=\frac12\int_{\Sigma(t)}\rho_s|v|^2\,dA,
\]
with a surface mass density \(\rho_s\) and a specified transport law. For conserved material mass,
\[
\partial_t(\rho_s\,dA)+\text{tangential transport}=0.
\]
Treating \(\rho_s\) as a fixed constant during arbitrary area changes instead describes exchange with a reservoir or a constrained incompressible formulation, depending on the rest of the model.

The membrane and scalar together have an energy exchange identity. Work done by the normal scalar force on the membrane is balanced by the explicit geometry dependence of the scalar energy, plus boundary and external work. This identity is the mechanical analogue of total stress conservation in a covariant bulk theory.

A simple radial collective coordinate \(A(t)\) can be introduced by restricting
\[
R(\theta,\zeta,t)=R_0+A(t)f(\theta,\zeta).
\]
Substitution into the full action yields an effective kinetic coefficient, restoring potential, and field coupling for \(A\). This is a model reduction, not the general shape equation. It excludes all shape harmonics orthogonal to \(f\), including potentially unstable ones.

A meaningful reduced simulation should compare its retained shape mode with the spectrum of the full linearized elastic operator.

## 52. A covariant material field generating the bulk coefficient

An explicit closure for an externally assigned \(U\) is to introduce a scalar material field \(\chi\):
\[
S_{\phi\chi}
=
\int\sqrt{-g}\,d^4x
\left[
-\frac12(\nabla\phi)^2-V(\phi)
-\frac12(\nabla\chi)^2-P(\chi)
-u(\chi)\phi^2
\right].
\]
The equations are
\[
\boxed{\Box\phi-V'(\phi)-2u(\chi)\phi=0,}
\]
\[
\boxed{\Box\chi-P'(\chi)-u'(\chi)\phi^2=0.}
\]
The total stress tensor obtained from this action is covariantly conserved on both equations.

The split scalar stress obeys
\[
\nabla_\mu T_\phi^\mu{}_\nu
=
-\phi^2u'(\chi)\nabla_\nu\chi,
\]
while the complementary sector supplies the opposite exchange. Thus the externally prescribed coefficient limit can be understood as freezing a source field with sufficiently large inertia or externally maintained configuration.

This does not uniquely determine \(u\) or \(P\). A dynamical closure is a mathematical specification of the missing degrees of freedom, not a derivation of their microscopic constitutive law. The latter requires additional physical input.

A corrugated equilibrium \(\chi_0\) must solve its own equation with the intended boundaries and supports. Simply assigning \(\chi_0\) to reproduce a chosen \(U\) leaves that mechanical question open.

---

# Part VIII. A consistent fermion sector

## 53. Clifford convention tied to the spacetime signature

To retain the familiar Hermitian Dirac Hamiltonian while using the spacetime signature \((-+++)\), this monograph defines matrices \(\Gamma^{\hat a}\) by
\[
\boxed{\{\Gamma^{\hat a},\Gamma^{\hat b}\}=-2\eta^{\hat a\hat b}I,}
\qquad
\eta^{\hat a\hat b}=\operatorname{diag}(-1,1,1,1).
\]
Thus
\[
(\Gamma^{\hat0})^2=I,\qquad
(\Gamma^{\hat i})^2=-I,
\]
and one can choose
\[
(\Gamma^{\hat0})^\dagger=\Gamma^{\hat0},
\qquad
(\Gamma^{\hat i})^\dagger=-\Gamma^{\hat i}.
\]
Define
\[
\bar\psi=\psi^\dagger\Gamma^{\hat0},
\qquad
\Gamma^\mu=e^\mu{}_{\hat a}\Gamma^{\hat a}.
\]
Then
\[
\{\Gamma^\mu,\Gamma^\nu\}=-2g^{\mu\nu}I.
\]

With this convention the Dirac equation is
\[
(i\Gamma^\mu D_\mu-m_f)\psi=0.
\]
For constant \(m_f\) in flat spacetime,
\[
(i\Gamma^\mu\partial_\mu+m_f)
(i\Gamma^\nu\partial_\nu-m_f)
=
\Box-m_f^2.
\]
Thus every spinor component satisfies the physical Klein–Gordon dispersion
\[
\omega^2=|\mathbf k|^2+m_f^2.
\]

An alternative convention uses matrices \(\gamma^\mu=i\Gamma^\mu\), which satisfy \(\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}\). The corresponding first order equation is \((\gamma^\mu D_\mu-m_f)\psi=0\). The factor of \(i\), Clifford sign, and adjoint must be changed together. The explicit flat space factorization is the decisive check.

## 54. Spin connection and the Hermitian action

For the stated Clifford convention, define
\[
D_\mu\psi=(\partial_\mu+\Omega_\mu)\psi,
\qquad
D_\mu\bar\psi=\partial_\mu\bar\psi-\bar\psi\Omega_\mu,
\]
with
\[
\boxed{
\Omega_\mu=-\frac18\omega_{\hat a\hat b\mu}
[\Gamma^{\hat a},\Gamma^{\hat b}].
}
\]
The minus sign follows from the minus sign in the Clifford algebra. The connection is fixed so that the gamma matrices are covariantly constant.

Take
\[
\mathcal L_{\psi}
=
\frac i2\left[
\bar\psi\Gamma^\mu D_\mu\psi
-(D_\mu\bar\psi)\Gamma^\mu\psi
\right]
-(M+g_Y\phi)\bar\psi\psi.
\]
Variation with respect to \(\bar\psi\) and \(\psi\) gives
\[
\boxed{(i\Gamma^\mu D_\mu-M-g_Y\phi)\psi=0,}
\]
\[
\boxed{i(D_\mu\bar\psi)\Gamma^\mu+(M+g_Y\phi)\bar\psi=0.}
\]
The scalar equation is
\[
\boxed{
\Box\phi-V'(\phi)-2U\phi-g_Y\bar\psi\psi=0.
}
\]
The local effective fermion mass is
\[
m_f(x)=M+g_Y\phi(x).
\]

The classical spinor fields used in an action principle are Grassmann valued when representing a fermionic field theory. A numerical commuting spinor wavefunction can instead represent a one particle or mean field approximation, but then its interpretation and back reaction prescription must be declared. A c-number \(\bar\psi\psi\) is not automatically a many body quantum expectation value.

## 55. Explicit cylindrical Dirac operator

Use the orthonormal coframe
\[
e^{\hat0}=Ndt,\quad e^{\hat1}=dr,\quad
e^{\hat2}=r\,d\theta,\quad e^{\hat3}=dz.
\]
Cartan's torsion free equation gives
\[
\omega^{\hat0}{}_{\hat1}=\frac{N_r}{N}e^{\hat0},
\qquad
\omega^{\hat0}{}_{\hat3}=\frac{N_z}{N}e^{\hat0},
\qquad
\omega^{\hat2}{}_{\hat1}=\frac1r e^{\hat2},
\]
together with the components related by metric antisymmetry.

The contracted spinor derivative is
\[
\boxed{
\Gamma^\mu D_\mu
=
\frac{\Gamma^{\hat0}}N\partial_t
+\Gamma^{\hat1}\left(\partial_r+\frac1{2r}+\frac{N_r}{2N}\right)
+\frac{\Gamma^{\hat2}}r\partial_\theta
+\Gamma^{\hat3}\left(\partial_z+\frac{N_z}{2N}\right).
}
\]
The \(1/(2r)\) term is a frame connection term. The lapse derivative terms are required by the gravitational connection.

Multiplying the Dirac equation by \(N\Gamma^{\hat0}\) gives a Hamiltonian form
\[
i\partial_t\psi=H_D\psi,
\]
with
\[
H_D
=
-iN\alpha^{\hat1}\left(\partial_r+\frac1{2r}+\frac{N_r}{2N}\right)
-i\frac N r\alpha^{\hat2}\partial_\theta
-iN\alpha^{\hat3}\left(\partial_z+\frac{N_z}{2N}\right)
+N\beta_Dm_f,
\]
where
\[
\alpha^{\hat i}=\Gamma^{\hat0}\Gamma^{\hat i},
\qquad
\beta_D=\Gamma^{\hat0}.
\]
The matrices \(\alpha^{\hat i}\) and \(\beta_D\) are Hermitian. With a static metric and appropriate zero flux boundary data, \(H_D\) is symmetric in the natural spinor norm
\[
\int r\,dr\,d\theta\,dz\,\psi^\dagger\psi.
\]
A self adjoint domain still has to be specified.

## 56. Current, stress, and exchange with the scalar

The fermion current is
\[
j^\mu=\bar\psi\Gamma^\mu\psi.
\]
The Dirac equation and its adjoint imply
\[
\nabla_\mu j^\mu=0.
\]
In the orthonormal static frame,
\[
j^{\hat0}=\psi^\dagger\psi\ge0.
\]
The conserved particle number convention is
\[
Q=-\int_{\Sigma_t}n_\mu j^\mu\,dV_h.
\]
For the static cylindrical frame,
\[
Q=\int r\,dr\,d\theta\,dz\,\psi^\dagger\psi.
\]

Using the full field dependent mass in \(\mathcal L_\psi\), the on shell Hilbert stress tensor in the present minus Clifford convention is
\[
\boxed{
T_{\mu\nu}^{\psi}
=
-\frac i4
\left[
\bar\psi\Gamma_\mu D_\nu\psi
+\bar\psi\Gamma_\nu D_\mu\psi
-(D_\nu\bar\psi)\Gamma_\mu\psi
-(D_\mu\bar\psi)\Gamma_\nu\psi
\right].
}
\]
The sign is tied to \(\Gamma_\mu=g_{\mu\nu}\Gamma^\nu\) and to the definition \(T_{\mu\nu}=-2\delta S/\sqrt{-g}\delta g^{\mu\nu}\). In flat space its \(T_{00}\) gives the positive energy of a positive frequency particle solution.

The scalar stress excluding the Yukawa interaction obeys
\[
\nabla_\mu T_\phi^\mu{}_\nu
=
g_Y\bar\psi\psi\,\nabla_\nu\phi-\phi^2\nabla_\nu U.
\]
The fermion sector with \(m_f=M+g_Y\phi\) supplies
\[
\nabla_\mu T_\psi^\mu{}_\nu
=
-g_Y\bar\psi\psi\,\nabla_\nu\phi.
\]
Their sum therefore has only the external \(U\) exchange. No separate Yukawa stress should be added on top of a full on shell fermion stress in a way that counts the same interaction twice.

## 57. Spin structure and boundary data

A scalar is periodic under \(\theta\to\theta+2\pi\). Spinor components in a rotating cylindrical tetrad need not obey the same component condition. A \(2\pi\) frame rotation acts by minus the identity in the spin representation.

On a solid cylinder embedded in ordinary space, the spin structure extending through the axis is fixed by smooth Cartesian spinors. The rotating tetrad components encode that extension with their appropriate angular behavior. On an annular domain, the angular cycle is noncontractible and more than one spin structure can be considered. On a periodically identified axial direction, periodic and antiperiodic spin structures are also distinct choices.

A spinor boundary condition must make the probability flux through a reflecting wall vanish and define a self adjoint Hamiltonian domain. Imposing scalar Dirichlet data independently on every component is generally not the natural first order boundary problem.

The current boundary form is
\[
\int_{\partial\Omega}\bar\psi\Gamma^\mu s_\mu\chi\,dS.
\]
Self adjoint boundary conditions select a subspace on which this form vanishes for allowed pairs of spinors. A particular bag, chiral, or spectral boundary condition should be declared before reporting a fermion spectrum.

## 58. Symmetries of the Yukawa theory and radiative closure

The isolated scalar quartic action is invariant under \(\phi\to-\phi\). The interaction \(g_Y\phi\bar\psi\psi\) is not invariant under that scalar transformation alone.

If \(M=0\), a combined discrete chiral transformation can reverse \(\bar\psi\psi\) together with \(\phi\). The exact transformation depends on the gamma convention, but the physical requirement is that the scalar bilinear change sign while the kinetic term remains invariant.

If \(M\ne0\), the mass term generally breaks that combined symmetry. Quantum loops then allow scalar operators that are absent from the even quartic ansatz:
\[
a_1\phi,\qquad a_3\phi^3,
\]
as well as curvature dependent odd terms such as
\[
c_{\mathcal R\phi}\mathcal R\phi
\]
when not prohibited by another symmetry.

One can choose renormalization conditions setting some renormalized coefficients to zero at one scale, but that is not the same as a symmetry protecting them. A quantum model must contain the full set of counterterms permitted by its declared symmetries.

Therefore the simple even quartic plus massive Yukawa theory is a valid classical truncation, but its restricted scalar potential is not automatically closed under renormalization.

---

# Part IX. Gravitational closure

## 59. Why a prescribed coefficient is not a complete gravitational source

Einstein's equation requires
\[
M_{\mathrm{Pl}}^2(G_{\mu\nu}+\Lambda g_{\mu\nu})
=T_{\mu\nu}^{\mathrm{total}}.
\]
Taking a covariant divergence and using the Bianchi identity gives
\[
\nabla_\mu T_{\mathrm{total}}^\mu{}_\nu=0.
\]
A scalar with an arbitrary external \(U(x)\) has
\[
\nabla_\mu T_\phi^\mu{}_\nu=-\phi^2\nabla_\nu U.
\]
Thus the scalar stress alone is not generally an admissible complete source for the Einstein equation.

There are consistent alternatives:

- Keep the metric prescribed and interpret the scalar as an open subsystem.
- Include the material or field degrees of freedom generating \(U\).
- Derive \(U\) from curvature and perform its full metric variation.
- Include an external source stress whose exchange is explicitly specified and conserved in total.

Writing a coordinate function inside a generally covariant integral can be formally covariant if that function is treated as an external scalar source. It still produces a Ward identity with external source exchange. Covariant notation alone does not make the system dynamically closed.

## 60. Scalar tensor action and boundary term

A definite scalar tensor action is
\[
\boxed{
S=
\int_{\mathcal M}\sqrt{-g}\,d^4x
\left[
\frac12F(\phi)\mathcal R
-\frac12Z(\phi)(\nabla\phi)^2
-V(\phi)+\mathcal L_m
\right]
+S_\partial.
}
\]
For the canonical nonminimal model,
\[
F(\phi)=M_{\mathrm{Pl}}^2-\xi\phi^2,
\qquad Z(\phi)=1.
\]
A cosmological constant can be included through
\[
V_0=M_{\mathrm{Pl}}^2\Lambda.
\]

For a nonnull boundary with induced metric fixed and scalar boundary value fixed, the curvature boundary term is
\[
S_\partial=\int_{\partial\mathcal M}\epsilon\sqrt{|q_\partial|}\,
F(\phi)K_\partial\,d^3y,
\]
where \(\epsilon=n_\mu n^\mu=\pm1\) and the orientation and definition of \(K_\partial\) are fixed consistently with the directed boundary convention. Corners require joint terms when present.

The \(F K_\partial\) term generalizes the Einstein boundary term. If scalar boundary values are varied, further scalar boundary conditions and terms must be treated consistently. A well posed metric variation is not obtained by retaining only the bulk curvature integral.

## 61. Complete scalar tensor Euler equations

Varying the metric gives
\[
\boxed{
F G_{\mu\nu}
=
Z\nabla_\mu\phi\nabla_\nu\phi
-g_{\mu\nu}\left[\frac12Z(\nabla\phi)^2+V\right]
+T_{\mu\nu}^{m}
+\nabla_\mu\nabla_\nu F-g_{\mu\nu}\Box F.
}
\]
Varying the scalar gives
\[
\boxed{
Z\Box\phi+\frac12Z'(\nabla\phi)^2
+\frac12F'\mathcal R-V'
+\frac{\partial\mathcal L_m}{\partial\phi}=0
}
\]
when the matter dependence on \(\phi\) contains no derivatives. Derivative couplings require the corresponding Euler derivative instead of an ordinary partial derivative.

For \(Z=1\), \(F=M_{\mathrm{Pl}}^2-\xi\phi^2\), and Yukawa coupling,
\[
\boxed{\Box\phi-V'-\xi\mathcal R\phi-g_Y\bar\psi\psi=0.}
\]
The metric equation becomes
\[
\boxed{
(M_{\mathrm{Pl}}^2-\xi\phi^2)G_{\mu\nu}
=
T_{\mu\nu}^{\phi,\mathrm{min}}+T_{\mu\nu}^{m}
+\xi\left(g_{\mu\nu}\Box-\nabla_\mu\nabla_\nu\right)\phi^2.
}
\]
Here the minimal scalar stress contains \(V\) but not an additional \(U\phi^2\), because the nonminimal term has already been varied.

The scalar tensor coupling is a covariant local interaction. Its coefficient \(\xi\) remains an independent parameter unless an additional symmetry or microscopic derivation fixes it.

## 62. Trace elimination and a scalar kinetic diagnostic

For \(Z=1\) and matter independent of \(\phi\), trace the metric equation:
\[
-F\mathcal R
=
-(\nabla\phi)^2-4V+T_m-3\Box F.
\]
Since
\[
\Box F=-2\xi\left[\phi\Box\phi+(\nabla\phi)^2\right],
\]
and
\[
\Box\phi=V'+\xi\mathcal R\phi,
\]
one obtains
\[
\boxed{
\left[F+6\xi^2\phi^2\right]\mathcal R
=
(1-6\xi)(\nabla\phi)^2
+4V-6\xi\phi V'-T_m.
}
\]
Define
\[
D_F=F+6\xi^2\phi^2
=M_{\mathrm{Pl}}^2+\xi(6\xi-1)\phi^2.
\]
For a canonical scalar and \(F>0\), one has \(D_F>0\).

For
\[
V=V_0+\frac12m_\phi^2\phi^2+\frac{\lambda}{4}\phi^4,
\]
the numerator becomes
\[
(1-6\xi)(\nabla\phi)^2
+4V_0+(2-6\xi)m_\phi^2\phi^2
+(1-6\xi)\lambda\phi^4-T_m.
\]
At \(\xi=1/6\), \(m_\phi=V_0=T_m=0\),
\[
\mathcal R=0
\]
in this classical on shell system, provided the denominator is nonzero.

If matter depends on \(\phi\), the scalar source contributes an additional term to the trace elimination. The formula above is explicitly restricted to scalar independent matter and should not be combined unchanged with the Yukawa source.

## 63. Einstein frame and health of the kinetic sector

For \(F>0\), define
\[
g_{\mu\nu}^{E}=\frac{F(\phi)}{M_{\mathrm{Pl}}^2}g_{\mu\nu}.
\]
After the conformal transformation and a boundary integration, the gravitational and scalar part takes the form
\[
S=\int\sqrt{-g_E}\,d^4x
\left[
\frac{M_{\mathrm{Pl}}^2}{2}\mathcal R_E
-\frac12K_E(\phi)(\nabla_E\phi)^2
-V_E(\phi)
\right],
\]
where
\[
\boxed{
K_E(\phi)=M_{\mathrm{Pl}}^2\left[
\frac{Z}{F}+\frac32\left(\frac{F'}F\right)^2
\right],
}
\]
\[
\boxed{V_E=\frac{M_{\mathrm{Pl}}^4}{F^2}V.}
\]
A canonically normalized scalar \(\chi_E\) satisfies
\[
\frac{d\chi_E}{d\phi}=\sqrt{K_E}.
\]

For \(Z=1\),
\[
K_E
=
M_{\mathrm{Pl}}^2\frac{F+6\xi^2\phi^2}{F^2}.
\]
Thus \(F>0\) ensures both a positive tensor kinetic term and a positive scalar kinetic term in this simple model. For general \(Z\), the additional condition is
\[
ZF+\frac32(F')^2>0.
\]

A conformal transformation is invertible only within its regular domain. Approaching \(F=0\) invalidates this frame map and signals loss of the simple effective description. One should not evolve across that surface and assume that the same healthy degrees of freedom persist.

Frame changes redistribute couplings between matter and geometry; physical observables require consistent transformations of units, rods, clocks, and matter couplings. The possibility of singular frame maps is discussed in [Järv, Kuusk, and Saal, Scalar tensor cosmology at the general relativity limit](https://arxiv.org/abs/0705.4644).

## 64. Curvature of the lapse only metric

For a static metric
\[
ds^2=-N^2dt^2+h_{ij}dx^idx^j
\]
with flat spatial \(h\), the Ricci components are
\[
R_{tt}=N\Delta_hN,\qquad
R_{ij}=-N^{-1}D_iD_jN,
\]
and
\[
\boxed{\mathcal R=-2N^{-1}\Delta_hN.}
\]
In the cylindrical coordinates,
\[
\Delta_hN=N_{rr}+\frac1rN_r+N_{zz}.
\]
The independent Einstein components are
\[
G_{tt}=0,
\]
\[
G_{rr}=\frac{N_r/r+N_{zz}}N,
\qquad
G_{\theta\theta}=\frac{r^2(N_{rr}+N_{zz})}N,
\]
\[
G_{zz}=\frac{N_{rr}+N_r/r}N,
\qquad
G_{rz}=-\frac{N_{rz}}N.
\]
These follow directly from the Ricci tensor and the scalar contraction.

For minimally coupled Einstein matter with \(\Lambda=0\), the \(tt\) equation forces \(T_{tt}=0\). A generic positive energy scalar distribution is therefore incompatible with this restricted metric as a self gravitating solution.

For scalar tensor gravity, derivative terms in \(F\) enter the constraint and can alter that simple inference. The ansatz remains highly restrictive and must satisfy every independent equation. A lapse chosen to produce a desired \(\mathcal R\) is not automatically a solution of the full scalar tensor system.

## 65. General ADM system and constraints

Use
\[
ds^2=-N^2dt^2+h_{ij}(dx^i+\beta^idt)(dx^j+\beta^jdt),
\]
and
\[
K_{ij}=-\frac12\mathcal L_nh_{ij}.
\]
For minimally coupled Einstein gravity,
\[
{}^{(3)}R+K^2-K_{ij}K^{ij}
=
2\Lambda+\frac{2\rho}{M_{\mathrm{Pl}}^2},
\]
\[
D_j(K^{ij}-h^{ij}K)=\frac{j^i}{M_{\mathrm{Pl}}^2}.
\]
Define
\[
\rho=T_{\mu\nu}n^\mu n^\nu,\quad
j_i=-h_i{}^\mu n^\nu T_{\mu\nu},\quad
S_{ij}=h_i{}^\mu h_j{}^\nu T_{\mu\nu}.
\]
The metric evolution is
\[
(\partial_t-\mathcal L_\beta)h_{ij}=-2NK_{ij}.
\]
The curvature evolution is
\[
\begin{aligned}
(\partial_t-\mathcal L_\beta)K_{ij}
={}&-D_iD_jN
+N\left({}^{(3)}R_{ij}+KK_{ij}-2K_{ik}K^k{}_j-\Lambda h_{ij}\right)\\
&-\frac N{M_{\mathrm{Pl}}^2}
\left[S_{ij}-\frac12h_{ij}(S-\rho)\right].
\end{aligned}
\]
Lapse and shift require gauge choices. The ADM identities do not alone guarantee a numerically robust hyperbolic evolution formulation. Generalized harmonic, BSSN, or another suitable formulation may be preferable.

The underlying decomposition, constraints, and coordinate choices are treated in [Gourgoulhon, 3+1 Formalism and Bases of Numerical Relativity](https://arxiv.org/abs/gr-qc/0703035). The displayed equations specify the convention needed for the scalar system here.

## 66. Scalar variables and sources in ADM form

With
\[
p=n^\mu\nabla_\mu\phi,
\]
the scalar evolution is
\[
\boxed{(\partial_t-\beta^iD_i)\phi=Np,}
\]
\[
\boxed{
(\partial_t-\beta^iD_i)p
=
N\left[D^iD_i\phi+Kp-V'(\phi)-2U\phi-J\right]
+D^iN\,D_i\phi.
}
\]
For a minimally coupled scalar,
\[
\rho=\frac12p^2+\frac12|D\phi|^2+W,
\]
\[
j_i=-pD_i\phi,
\]
\[
S_{ij}
=
D_i\phi D_j\phi
+h_{ij}\left[\frac12p^2-\frac12|D\phi|^2-W\right].
\]
The momentum sign follows directly from its definition and should be checked against the chosen sign of \(K_{ij}\).

For time symmetric initial data \(p=0\), \(K_{ij}=0\), the momentum constraint is automatically satisfied for the scalar sector, while the Hamiltonian constraint becomes
\[
{}^{(3)}R=2\Lambda+\frac{2\rho}{M_{\mathrm{Pl}}^2}.
\]
A flat spatial metric then imposes a nontrivial restriction on the energy density. This is another way to see why positive scalar energy cannot generally be added to a flat spatial slice with a static lapse and zero extrinsic curvature.

Nonminimal coupling modifies the constraint sources through derivatives of \(F\). One can derive a Jordan frame system or transform to a regular Einstein frame, but the minimal source formulas must not be used unchanged.

## 67. Homogeneous cosmological reduction as a consistency test

For a spatially flat FLRW metric,
\[
ds^2=-dt^2+a_{\mathrm{cos}}^2(t)d\mathbf x^2,
\qquad
H_{\mathrm{cos}}=\frac{\dot a_{\mathrm{cos}}}{a_{\mathrm{cos}}},
\]
a homogeneous scalar tensor model with \(Z=1\) obeys
\[
\boxed{
3FH_{\mathrm{cos}}^2
=
\rho_m+\frac12\dot\phi^2+V-3H_{\mathrm{cos}}\dot F,
}
\]
\[
\boxed{
-2F\dot H_{\mathrm{cos}}
=
\rho_m+p_m+\dot\phi^2+\ddot F-H_{\mathrm{cos}}\dot F,
}
\]
\[
\boxed{
\ddot\phi+3H_{\mathrm{cos}}\dot\phi+V'
-\frac12F'\mathcal R=0,
}
\]
with
\[
\mathcal R=6(\dot H_{\mathrm{cos}}+2H_{\mathrm{cos}}^2).
\]
For \(F=M_{\mathrm{Pl}}^2-\xi\phi^2\), the scalar equation contains \(+\xi\mathcal R\phi\).

The first equation is a constraint. Differentiating it and using matter conservation and the scalar equation reproduces the second equation when the system is regular. This provides an internal numerical consistency check.

These equations define a possible cosmological specialization. They do not supply a cosmological fit, dark energy explanation, or observationally allowed parameter region. Those require an explicit potential, matter content, initial conditions, and comparison with measurements.

## 68. Test field limits and the size of back reaction

A prescribed geometry approximation requires that the field stress be small compared with the geometric scale being held fixed. A useful dimensionless estimate is
\[
\epsilon_{\mathrm{grav}}
\sim
\frac{\rho L^2}{M_{\mathrm{Pl}}^2}.
\]
For \(\epsilon_{\mathrm{grav}}\ll1\), metric perturbations sourced over scale \(L\) can be small in an appropriate weak field setting. Boundary conditions, long range accumulation, and resonance can still matter.

For nonminimal coupling, one must also control
\[
\left|\frac{\xi\phi^2}{M_{\mathrm{Pl}}^2}\right|
\]
and derivative contributions from \(F\). A small scalar potential energy alone does not guarantee a small modification of the effective gravitational kinetic coefficient.

For an elastic surface, the analogous criterion compares scalar normal stresses with bending and tension restoring forces. A representative bending force scale is \(\kappa_b/L^3\), while a tension force scale is \(\sigma/L\). The relevant ratios depend on the scalar normalization and geometry.

A self consistent hierarchy should state which small parameter suppresses each neglected back reaction. Calling a background “fixed” is a model definition; calling it a controlled approximation additionally requires that estimate.

---

# Part X. Continuous phase, gauge fields, and dissipation

## 69. A complex scalar with a normalization inherited from two real fields

Introduce
\[
\chi=\frac{\phi_1+i\phi_2}{\sqrt2}
=\frac{\rho}{\sqrt2}e^{i\vartheta}.
\]
Use
\[
\mathcal L_\chi
=
-\nabla_\mu\chi^*\nabla^\mu\chi
-m_\phi^2|\chi|^2-\lambda|\chi|^4-2U|\chi|^2.
\]
In real components,
\[
\mathcal L_\chi
=
-\frac12\sum_{a=1}^2(\nabla\phi_a)^2
-\frac12(m_\phi^2+2U)(\phi_1^2+\phi_2^2)
-\frac{\lambda}{4}(\phi_1^2+\phi_2^2)^2.
\]
Thus restricting to \(\phi_2=0\) recovers the original real scalar normalization exactly.

Variation with respect to \(\chi^*\) gives
\[
\boxed{
\Box\chi-(m_\phi^2+2U)\chi-2\lambda|\chi|^2\chi=0.
}
\]
The factor two in the quartic term follows from the chosen \(\lambda|\chi|^4\). A convention with \(\lambda|\chi|^4/2\) defines a different numerical coupling.

In amplitude and phase variables,
\[
\mathcal L_\chi
=
-\frac12(\nabla\rho)^2
-\frac12\rho^2(\nabla\vartheta)^2
-\frac12(m_\phi^2+2U)\rho^2
-\frac{\lambda}{4}\rho^4.
\]
The amplitude equation is
\[
\boxed{
\Box\rho-\rho(\nabla\vartheta)^2
-(m_\phi^2+2U)\rho-\lambda\rho^3=0,
}
\]
and the phase equation is
\[
\boxed{\nabla_\mu(\rho^2\nabla^\mu\vartheta)=0.}
\]
These polar variables are singular where \(\rho=0\). Cartesian field components remain the preferred variables near vortex cores or zeros of the field.

## 70. Current sign fixed by the transformation

Choose the global symmetry convention
\[
\delta\chi=-i\alpha\chi,\qquad
\delta\vartheta=-\alpha.
\]
Its current is
\[
\boxed{
j^\mu=-i\left(\chi^*\nabla^\mu\chi-\chi\nabla^\mu\chi^*\right)
=\rho^2\nabla^\mu\vartheta.
}
\]
The opposite group parameter convention reverses the current and charge; it does not change the conservation equation.

For \(\vartheta=-\omega t\) in flat spacetime,
\[
j^0=\rho^2\omega.
\]
Thus positive \(\omega\) gives positive charge under this convention. The hypersurface charge is
\[
Q=-\int_{\Sigma_t}n_\mu j^\mu\,dV_h.
\]

The real scalar has a conserved symplectic structure, but no analogous continuous internal phase charge. Writing a real standing wave as a complex exponential for algebraic convenience does not introduce a physical \(U(1)\) symmetry. The complex field theory has an additional real degree of freedom and a different configuration space.

A static phase gradient contributes energy and can support currents. Whether it remains stable depends on the amplitude equation, boundary conditions, topology, and coupling to any gauge field or environment.

## 71. Gauge completion with an explicit sign convention

Define
\[
D_\mu\chi=(\nabla_\mu+iqA_\mu)\chi,
\]
with gauge transformation
\[
A_\mu\to A_\mu+\partial_\mu\alpha,\qquad
\chi\to e^{-iq\alpha}\chi.
\]
Then
\[
v_\mu=\partial_\mu\vartheta+qA_\mu
\]
is gauge invariant. Use
\[
\mathcal L
=
-(D_\mu\chi)^*D^\mu\chi
-m_\phi^2|\chi|^2-\lambda|\chi|^4-2U|\chi|^2
-\frac14F_{\mu\nu}F^{\mu\nu}.
\]
The scalar equation is
\[
D_\mu D^\mu\chi-(m_\phi^2+2U)\chi-2\lambda|\chi|^2\chi=0.
\]
The Maxwell equation is
\[
\boxed{\nabla_\mu F^{\mu\nu}=j_{\mathrm{em}}^\nu,}
\]
where
\[
\boxed{
j_{\mathrm{em}}^\nu
=
-iq\left[\chi^*D^\nu\chi-\chi(D^\nu\chi)^*\right]
=q\rho^2v^\nu.
}
\]
Gauge invariance and the scalar equation imply
\[
\nabla_\mu j_{\mathrm{em}}^\mu=0.
\]

In a broken homogeneous vacuum with \(\rho=v\), the gauge field mass is
\[
m_A^2=q^2v^2.
\]
The radial scalar mass is
\[
m_\rho^2=2\lambda v^2.
\]
Both expressions follow from expanding the same action. Their ratio
\[
\frac{m_\rho^2}{m_A^2}=\frac{2\lambda}{q^2}
\]
is independent of field normalization once the action convention has been fixed.

## 72. Winding, vortices, and finite energy

For a nonzero complex field on a closed loop,
\[
w=\frac1{2\pi}\oint d\vartheta\in\mathbb Z.
\]
This integer is well defined only when the amplitude does not vanish on the loop. It can change when a zero crosses the loop or boundary conditions permit phase escape.

For an ungauged global vortex in two spatial dimensions, the far field phase gradient behaves as
\[
|\nabla\vartheta|\sim\frac{|w|}{r}.
\]
With \(\rho\to v\), its energy grows logarithmically with the outer radius:
\[
E_{\mathrm{far}}
=
\pi v^2w^2\log\left(\frac{R_{\mathrm{out}}}{R_{\mathrm{core}}}\right).
\]
Thus an isolated global vortex has no finite total energy on the infinite plane, although finite systems and vortex pairs are meaningful.

For a gauged field, finite energy requires
\[
v_\mu=\partial_\mu\vartheta+qA_\mu\to0
\]
at large spatial distance. The magnetic flux is then
\[
\oint A_i\,dx^i=-\frac{2\pi w}{q}
\]
in the present convention. Its magnitude is quantized in units \(2\pi/|q|\).

A real double well scalar instead supports disconnected vacuum sectors and domain walls. Its topology is associated with \(\pi_0\) of the vacuum manifold, while a complex broken phase has \(\pi_1(S^1)=\mathbb Z\). The two defect classes should not be conflated.

## 73. Dissipative order parameter dynamics on a fixed manifold

Let the free energy be
\[
\mathcal F[\varphi]
=
\int_\Sigma
\left[
\frac{\kappa_\varphi}{2}|D\varphi|_\gamma^2
+V_\Sigma(\varphi)+U_\Sigma\varphi^2
\right]dA.
\]
The variational derivative with respect to the invariant measure is
\[
\mu_{\mathrm{chem}}
=
-\kappa_\varphi\Delta_\gamma\varphi
+V_\Sigma'(\varphi)+2U_\Sigma\varphi.
\]
For nonconserved relaxation,
\[
\partial_t\varphi=-\Gamma\mu_{\mathrm{chem}},
\qquad \Gamma\ge0.
\]
Then, for a fixed geometry and time independent coefficients,
\[
\boxed{
\frac{d\mathcal F}{dt}
=
-\int_\Sigma\Gamma\mu_{\mathrm{chem}}^2\,dA\le0.
}
\]
For a conserved order parameter,
\[
\partial_t\varphi
=
D_a\left(MD^a\mu_{\mathrm{chem}}\right),
\qquad M\ge0.
\]
Under periodic or zero chemical flux boundaries,
\[
\frac d{dt}\int_\Sigma\varphi\,dA=0,
\]
\[
\boxed{
\frac{d\mathcal F}{dt}
=
-\int_\Sigma M|D\mu_{\mathrm{chem}}|^2\,dA\le0.
}
\]

The first equation is Allen–Cahn type and the second is Cahn–Hilliard type. Their invariant energy laws follow directly from the declared gradient flow. Their time variable and mobility are material quantities, not automatically relativistic proper time and fundamental constants.

On a moving surface, the transport theorem adds area change and material advection. Conservation then applies to the transported density with the correct evolving measure.

## 74. Damped waves and fluctuation dissipation

A damped wave model in a specified environmental rest frame is
\[
\phi_{tt}+\gamma\phi_t-\Delta\phi+W'(\phi)=0,
\qquad \gamma\ge0.
\]
Its energy satisfies
\[
\frac{dE}{dt}=-\gamma\int\phi_t^2\,d^3x
\]
for closed boundaries. The lost energy is transferred to omitted environment degrees of freedom.

A covariant phenomenological form is
\[
\Box\phi-W'(\phi)-\gamma u^\mu\nabla_\mu\phi=0,
\]
where \(u^\mu\) is the environmental four velocity. It introduces a preferred physical rest frame supplied by the environment; it is not a conservative single scalar action of the original form.

At finite temperature, an equilibrium open system description generally pairs dissipation with noise. A Markovian classical Langevin approximation has
\[
\phi_{tt}+\gamma\phi_t-\Delta\phi+W'(\phi)=\eta,
\]
with a noise covariance tied to \(\gamma\) and temperature in the chosen normalization. A quantum environment typically produces frequency dependent dissipation and colored noise instead.

No stochastic term is assumed in the deterministic benchmarks of this document. Adding damping to stabilize a numerical calculation changes the physical dynamics unless it is explicitly treated as a numerical device whose effect vanishes in the intended limit.

---

# Part XI. Green functions, quantization, and effective theory

## 75. Retarded response and the sign of the source

Define
\[
P=\Box_g-M^2(x).
\]
The retarded Green function satisfies
\[
P_xG_{\mathrm R}(x,x')
=
\frac{\delta^{(4)}(x-x')}{\sqrt{-g(x')}},
\]
with support only when \(x\) lies in the causal future of \(x'\). The delta denominator may be written using \(x\) equivalently in the distributional identity.

For
\[
P\phi=J,
\]
the solution is
\[
\phi=\phi_{\mathrm{hom}}
+\int G_{\mathrm R}(x,x')J(x')\,dV_{g'}.
\]
For the quartic Yukawa theory,
\[
J=\lambda\phi^3+g_Y\bar\psi\psi
\]
when the linear mass coefficient is included in \(P\). This is an exact integral equation but remains nonlinear and implicit.

In a static mode basis, the positive time form is
\[
\ddot q_a+\nu_aq_a=-J_a.
\]
For \(\nu_a=\omega_a^2>0\),
\[
q_a(t)
=
q_a^{\mathrm{hom}}(t)
-\int_{t_0}^t\frac{\sin[\omega_a(t-s)]}{\omega_a}J_a(s)\,ds.
\]
At \(\nu_a=0\), the kernel becomes \(t-s\). Near a soft mode, susceptibility increases, but finite damping, nonlinear saturation, source bandwidth, and observation time determine the actual response.

Retarded and Feynman Green functions implement different boundary prescriptions. A causal response problem should not be solved by substituting a Feynman kernel without explaining the conversion.

## 76. Integrating out a quadratic scalar exactly

Set \(\lambda=0\) and define
\[
\mathcal O=-\Box_g+M^2(x).
\]
After integration by parts,
\[
S_\phi
=
-\frac12\langle\phi,\mathcal O\phi\rangle-\langle J,\phi\rangle,
\]
where the bracket includes the spacetime invariant measure and a declared inverse prescription.

Complete the square:
\[
\begin{aligned}
S_\phi
={}&
-\frac12
\left\langle\phi+\mathcal O^{-1}J,\,
\mathcal O(\phi+\mathcal O^{-1}J)\right\rangle\\
&+\frac12\langle J,\mathcal O^{-1}J\rangle.
\end{aligned}
\]
The stationary solution is
\[
\phi_*=-\mathcal O^{-1}J.
\]
The tree level induced action is therefore
\[
\boxed{S_{\mathrm{ind}}=\frac12\langle J,\mathcal O^{-1}J\rangle.}
\]
For \(J=g_Y\bar\psi\psi\), this is a nonlocal four fermion interaction with an exact factor \(g_Y^2/2\) in the quadratic scalar approximation.

The Gaussian path integral also produces a determinant. Its definition requires a contour, boundary prescription, and regularization. A retarded inverse is natural for a classical response equation, while an in out effective action uses the appropriate Feynman prescription. Dissipative quantum evolution requires a closed time path construction rather than a naive real local action.

## 77. Heavy field expansion and its locality conditions

For constant positive \(M^2\) and derivatives small compared with \(M\),
\[
\mathcal O^{-1}
=
(M^2-\Box)^{-1}
=
\frac1{M^2}
+\frac{\Box}{M^4}
+\frac{\Box^2}{M^6}+\cdots.
\]
Then
\[
S_{\mathrm{ind}}
=
\frac1{2M^2}\int J^2
+\frac1{2M^4}\int J\Box J+\cdots.
\]
Integration by parts gives
\[
\int J\Box J=-\int(\nabla J)^2
\]
up to boundary terms. Thus the first derivative correction is fixed once the source convention and operator are fixed.

For a spatially varying mass,
\[
\mathcal O=M^2(x)-\Box,
\]
multiplication by \(M^{-2}(x)\) does not commute with derivatives. The expansion is ordered:
\[
\mathcal O^{-1}
=
M^{-2}
+M^{-2}\Box M^{-2}
+M^{-2}\Box M^{-2}\Box M^{-2}
+\cdots.
\]
Derivatives act on both the source and the coefficient.

A local heavy field approximation requires a spectral gap, slow coefficient variation, and source frequencies below the gap. It fails near an instability, a bound state approaching zero frequency, a rapid interface, or a resonant source. A large bare \(m_\phi\) is insufficient if \(2U\) nearly cancels its mass squared in a relevant mode.

## 78. Symplectic form and mode normalization for quantization

For two solutions \(u,v\) of the real linearized equation with the same real coefficient,
\[
\omega^\mu(u,v)=u\nabla^\mu v-v\nabla^\mu u
\]
is divergence free. Its integral over a Cauchy surface is the conserved symplectic form
\[
\Omega(u,v)=\int_{\Sigma_t}
\left(u\,n^\mu\nabla_\mu v-v\,n^\mu\nabla_\mu u\right)dV_h.
\]
Complexifying the solution space gives the Klein–Gordon product
\[
(u,v)_{\mathrm{KG}}
=
i\int_{\Sigma_t}
\left(u^*n^\mu\nabla_\mu v-vn^\mu\nabla_\mu u^*\right)dV_h.
\]
For a static background and spatial modes normalized by
\[
\int_\Omega\frac{u_a^*u_b}{N}dV_h=\delta_{ab},
\]
positive frequency modes are
\[
f_a(t,x)=\frac{e^{-i\omega_at}}{\sqrt{2\omega_a}}u_a(x).
\]
Then
\[
(f_a,f_b)_{\mathrm{KG}}=\delta_{ab}.
\]
The field expansion is
\[
\widehat\eta=\sum_a\left(a_af_a+a_a^\dagger f_a^*\right),
\]
with
\[
[a_a,a_b^\dagger]=\delta_{ab}.
\]

A negative eigenvalue does not define a stable harmonic oscillator vacuum. A zero mode also requires separate treatment because the factor \(1/\sqrt{2\omega}\) becomes singular. Stable mode quantization therefore requires more than formal canonical commutators.

## 79. Static vacuum energy and geometry dependence

For positive discrete modes, the formal zero point energy is
\[
E_{\mathrm{vac}}^{\mathrm{formal}}=\frac12\sum_a\omega_a.
\]
This sum is ultraviolet divergent. A geometry dependent energy difference can become finite after a consistent regularization, subtraction, and specification of material or boundary counterterms.

A change in a regulated spectral sum is not automatically a universal force. It may contain cutoff dependent surface tension, bending stiffness, vacuum density, or boundary energy terms. Those must be matched to physical parameters before a finite prediction is assigned.

If the geometry varies slowly, a renormalized vacuum energy contributes to an effective shape force
\[
f_{\mathrm{vac}}=-\frac1{\sqrt\gamma}\frac{\delta E_{\mathrm{vac}}^{\mathrm{ren}}}{\delta X_\perp}.
\]
If it varies rapidly, particle production and nonadiabatic energy transfer can occur. The energy comes from the agent changing the geometry or from another dynamical sector.

A static ground state of a time independent Hamiltonian is passive with respect to cyclic unitary operations: its expectation energy cannot be lowered below the ground energy. Geometry dependent vacuum structure therefore does not imply a cyclic source of net work without another resource or state change.

## 80. Quadratic fluctuation determinant

Expand a classical solution as
\[
\phi=\phi_{\mathrm{cl}}+\eta.
\]
For prescribed \(g,U\), the quadratic action is
\[
S^{(2)}
=
-\frac12\int\sqrt{-g}\,\eta
\left[-\Box_g+V''(\phi_{\mathrm{cl}})+2U\right]\eta\,d^4x
\]
after the boundary terms are treated.

With curvature coupling, the scalar fluctuation operator on a fixed metric is
\[
\mathcal D=-\Box_g+m_\phi^2+3\lambda\phi_{\mathrm{cl}}^2+2U+\xi\mathcal R.
\]
If the metric fluctuates too, scalar and metric perturbations mix; this one scalar determinant is then only one block of the full gauge fixed Hessian.

A formal Lorentzian one loop contribution is
\[
\Gamma^{(1)}_\phi=\frac i2\operatorname{Tr}\log(\mathcal D-i0),
\]
with the prescription determined by the chosen quantum state and boundary conditions. The fermion determinant contributes with the Grassmann sign:
\[
\Gamma^{(1)}_\psi=-i\operatorname{Tr}\log(i\Gamma^\mu D_\mu-m_f).
\]

These expressions are starting points for a renormalized calculation, not finite answers. A physically meaningful curved spacetime quantum construction must specify states and local covariant renormalization. The framework and role of physically admissible states are reviewed by [Hollands and Wald, Quantum fields in curved spacetime](https://arxiv.org/abs/1401.2026).

## 81. Heat kernel structure and local counterterms

After an appropriate Euclidean continuation in a setting where it is justified, consider a scalar Laplace type operator
\[
D_E=-\nabla_E^2+Q.
\]
The short proper time expansion has the form
\[
\operatorname{Tr}e^{-sD_E}
\sim
\frac1{(4\pi s)^{D/2}}
\sum_{j\ge0}s^j\int a_{2j}(x)\,dV_E,
\]
plus boundary contributions when boundaries are present.

For a scalar operator without a bundle curvature,
\[
a_0=1,\qquad a_2=\frac{\mathcal R}{6}-Q.
\]
In four dimensions, the integrated local coefficient controlling logarithmic ultraviolet structure contains, up to total derivatives,
\[
\boxed{
a_4=
\frac12\left(Q-\frac{\mathcal R}{6}\right)^2
+\frac1{180}
\left(R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
-R_{\mu\nu}R^{\mu\nu}\right)
+\text{total derivatives}.
}
\]
The sign convention for \(Q\) is fixed by \(D_E=-\nabla_E^2+Q\).

For
\[
Q=m_\phi^2+3\lambda\phi_{\mathrm{cl}}^2+2U+\xi\mathcal R,
\]
the square generates terms involving
\[
m_\phi^4,\quad m_\phi^2\phi^2,\quad\phi^4,\quad
\mathcal R\phi^2,\quad U\phi^2,\quad U^2,\quad U\mathcal R,\quad\mathcal R^2.
\]
Therefore an arbitrary external coefficient is itself part of the renormalization problem. Curvature and source counterterms are not optional if the corresponding divergences are present.

Boundary heat coefficients add boundary operators and depend on the chosen boundary conditions. The heat kernel method and the distinction between bulk and boundary coefficients are described in [Vassilevich, Heat kernel expansion: user's manual](https://arxiv.org/abs/hep-th/0306138).

## 82. Flat space one loop potential with fixed normalization

For a constant scalar background in flat space, define
\[
M_s^2(\phi)=m_\phi^2+3\lambda\phi^2,
\qquad
M_f(\phi)=M+g_Y\phi.
\]
In a conventional minimal subtraction scheme, the scalar and one Dirac fermion contributions have the familiar local form
\[
V_1(\phi)
=
\frac{M_s^4}{64\pi^2}
\left[\log\left(\frac{M_s^2}{\mu_R^2}\right)-\frac32\right]
-\frac{4M_f^4}{64\pi^2}
\left[\log\left(\frac{M_f^2}{\mu_R^2}\right)-\frac32\right]
+\text{counterterms}.
\]
This expression assumes a stable expansion with positive scalar fluctuation mass squared and a specified renormalization prescription. If \(M_s^2<0\), an imaginary part or an alternative treatment reflects instability of the chosen background; the naive real logarithm is not a valid stable effective potential.

The factor four counts the components of one Dirac field. Additional species, degeneracies, and gauge interactions change the expression.

Expanding \((M+g_Y\phi)^4\) demonstrates directly why odd scalar powers are generated when \(M\ne0\). The one loop potential also depends on the renormalization conditions fixing the vacuum location, scalar mass, and self coupling. It does not determine those physical inputs without matching.

The local potential approximation omits derivative terms and nonlocal dependence. It is suitable only when the background varies slowly compared with the masses being integrated out.

## 83. Pure scalar running and the quartic convention

For a pure four dimensional real scalar with
\[
V=\frac12m_\phi^2\phi^2+\frac{\lambda}{4}\phi^4,
\]
the conventional coupling \(g\) in \(g\phi^4/4!\) is
\[
g=6\lambda.
\]
The one loop pure scalar beta function is therefore
\[
\boxed{
\mu_R\frac{d\lambda}{d\mu_R}
=
\frac{9\lambda^2}{8\pi^2}+O(\lambda^3).
}
\]
Likewise, in the corresponding mass independent scheme,
\[
\mu_R\frac{dm_\phi^2}{d\mu_R}
=
\frac{3\lambda m_\phi^2}{8\pi^2}+\cdots,
\]
\[
\mu_R\frac{d\xi}{d\mu_R}
=
\frac{3\lambda}{8\pi^2}\left(\xi-\frac16\right)+\cdots.
\]
These formulas are restricted to the pure scalar model at the stated order. Yukawa and gauge fields add contributions and can change the running qualitatively.

The one loop solution for the quartic coefficient is
\[
\frac1{\lambda(\mu_R)}
=
\frac1{\lambda(\mu_0)}
-\frac9{8\pi^2}\log\left(\frac{\mu_R}{\mu_0}\right).
\]
A formal pole in this truncated running marks failure of weak coupling extrapolation, not a reliable prediction of a physical singularity.

Conformal coupling is distinguished by the massless classical symmetry and by the structure of the scalar running. Quantum scale dependence and curvature anomalies still remain. Classical conformal invariance is not a statement that all quantum traces vanish.

## 84. Effective operator basis and cutoff hierarchy

In four dimensions, organize the local theory by mass dimension:
\[
\mathcal L_{\mathrm{EFT}}
=
\mathcal L_{\le4}
+\sum_{d>4}\frac{c_d}{\Lambda_{\mathrm{EFT}}^{d-4}}\mathcal O_d.
\]
The dimension four and lower sector can contain
\[
1,\quad\phi,\quad\phi^2,\quad\phi^3,\quad\phi^4,\quad
(\nabla\phi)^2,\quad\mathcal R,\quad\mathcal R\phi,\quad\mathcal R\phi^2,
\]
subject to symmetries, together with fermion, gauge, and source operators.

Pure curvature squares
\[
\mathcal R^2,\qquad
R_{\mu\nu}R^{\mu\nu},\qquad
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
\]
have dimension four. Their coefficients are dimensionless; they are not dimension six operators merely because they contain more derivatives than Einstein gravity.

Examples of higher dimensional scalar operators include
\[
\frac{c_6}{\Lambda_{\mathrm{EFT}}^2}\phi^6,\qquad
\frac{c_{R\partial}}{\Lambda_{\mathrm{EFT}}^2}\mathcal R(\nabla\phi)^2,
\qquad
\frac{c_8}{\Lambda_{\mathrm{EFT}}^4}[(\nabla\phi)^2]^2.
\]
For fermions,
\[
\phi^2\bar\psi\psi
\]
has dimension five and requires one inverse power of the cutoff.

The cutoff expansion needs control of momenta, curvature, gradients, and sometimes field amplitude:
\[
\frac{E}{\Lambda_{\mathrm{EFT}}}\ll1,\qquad
\frac{\sqrt{|\mathcal R|}}{\Lambda_{\mathrm{EFT}}}\ll1,
\qquad
\frac{|\nabla\phi|}{\Lambda_{\mathrm{EFT}}^2}\ll1.
\]
Large fields can invalidate a polynomial amplitude expansion even at low momentum unless a symmetry protects the field range.

The low energy treatment of gravity as an effective field theory is supported by [Donoghue, General relativity as an effective field theory](https://arxiv.org/abs/gr-qc/9405057). It does not require interpreting a finite higher derivative truncation as an exact theory at all frequencies.

## 85. Higher derivatives and spurious high frequency roots

Suppose a low energy propagator is expanded as
\[
D^{-1}(k)=k^2+m^2+\frac{c}{\Lambda^2}k^4+\cdots.
\]
If the truncated polynomial is solved exactly, it can introduce an additional root at a frequency of order \(\Lambda\). That root lies outside the regime in which the truncated derivative expansion was controlled.

A perturbative effective treatment expands observables in \(k^2/\Lambda^2\) or uses order reduction to avoid assigning physical initial data to the spurious high frequency solution. A genuinely fundamental higher derivative theory needs a separate degrees of freedom and stability analysis.

Certain combinations of higher derivatives are degenerate and avoid an extra propagating mode. Establishing degeneracy requires examining the kinetic matrix or constraints; it does not follow from the word “geometric.”

For the present canonical scalar tensor action with \(F(\phi)\mathcal R\) and first derivatives of \(\phi\), the field equations are second order before gauge fixing. Adding arbitrary curvature invariants changes that structure. Each proposed completion must therefore be audited independently rather than accepted as a harmless extension.

## 86. Quantum state, semiclassical gravity, and what remains unspecified

A semiclassical gravitational equation has the schematic form
\[
M_{\mathrm{Pl}}^2(G_{\mu\nu}+\Lambda g_{\mu\nu})
+\text{renormalized curvature variations}
=
\langle T_{\mu\nu}\rangle_{\mathrm{ren}}.
\]
The expectation value depends on the quantum state. A background metric and an action do not generally select a unique vacuum in a nonstationary spacetime.

A complete calculation must specify:

1. The state or initial two point function.
2. The renormalization prescription.
3. The finite gravitational counterterms.
4. Boundary conditions and material idealizations.
5. The range where stress fluctuations are small enough for a mean stress description.
6. The treatment of the higher derivative terms generated by renormalization.

The present monograph supplies the classical action and the fluctuation operators needed to formulate this problem. It does not claim to have solved the fully coupled semiclassical Einstein equation for the corrugated geometry.

A formal determinant, a zero point mode sum, and a self consistent quantum corrected solution are different levels of completion. Keeping those levels separate makes the research program falsifiable and prevents a calculation at one level from being used as evidence for another.

---

# Part XII. Numerical formulation and reproducibility

## 87. The numerical problem must be specified before discretization

A reproducible field calculation needs a complete problem record. At minimum it contains the action convention, dimension, domain, geometry, parameter values, initial data, boundary data, source protocol, numerical representation, and target observable.

For the main surface benchmarks in this document, the choices are:

| Input | Exact mathematical value |
|---|---|
| Surface radius scale | \(R_0=1\) |
| Axial scale | \(a=3/2\) |
| Corrugation amplitude | \(A=1/10\) |
| Harmonics | \(n=2,\ m=1\) |
| Offsets | \(\delta_\theta=\delta_\zeta=0\) |
| Scalar mass squared | \(m_\Sigma^2=1/4\) |
| Surface lapse | \(N_\Sigma=1\) |
| Boundary conditions | Periodic in both phase coordinates |
| Nonlinear coupling in spectral runs | \(\lambda_\Sigma=0\) |
| External potential in geometry run | \(U_\Sigma=0\) |
| External potential in separate potential run | \(A=0,\ U_\Sigma=(1/10)\sin(2\theta)\cos\zeta\) |
| Fourier cutoffs | \(|\ell|,|p|\le K,\ K=3,5,7,9\) |
| Standard geometry quadrature | \(128\) points per phase coordinate |

The two spectral experiments alter different terms in the action. Their results should not be merged into a claim that “corrugation produces one universal shift.” The geometric and potential mechanisms have separately specified inputs and can be compared precisely.

No random seed is required because these calculations contain no random sampling. Arithmetic, dependency versions, and source code are recorded in the computational appendix.

## 88. Weak formulation and discrete matrices

For a static scalar background, choose real or complex basis functions \(v_i\) satisfying the essential boundary conditions. Define
\[
\mathsf M_{ij}
=
\int_\Omega\frac{v_i^*v_j}{N}\,dV_h,
\]
\[
\mathsf K_{ij}
=
\int_\Omega N
\left(h^{ab}D_av_i^*D_bv_j+M^2v_i^*v_j\right)dV_h
+\int_{\partial\Omega}N\alpha v_i^*v_j\,dS_h.
\]
Then
\[
\boxed{\mathsf M\ddot{\mathbf q}+\mathsf K\mathbf q+\mathbf f_{\mathrm{nl}}(\mathbf q)=\mathbf s(t).}
\]
For the linear spectrum,
\[
\boxed{\mathsf K\mathbf u=\nu\mathsf M\mathbf u.}
\]
The mass matrix should be Hermitian positive definite on a linearly independent basis. The stiffness matrix should be Hermitian for the declared conservative boundary conditions. A negative stiffness eigenvalue can be physical; a nonsymmetric stiffness matrix in an intended self adjoint model generally indicates a formulation or assembly issue.

The nonlinear force must be the gradient of the discretized potential energy:
\[
f_{\mathrm{nl},i}
=
\lambda\int_\Omega N\,v_i^*
\left(\sum_jq_jv_j\right)^3dV_h
\]
for a real field. If complex Fourier coefficients are used, the real field constraint is enforced before interpreting this expression.

The discrete energy is
\[
E_h=
\frac12\dot{\mathbf q}^\dagger\mathsf M\dot{\mathbf q}
+\frac12\mathbf q^\dagger\mathsf K\mathbf q
+V_{\mathrm{nl},h}.
\]
Its time derivative vanishes for the exact semidiscrete conservative equations. Time integration introduces a separate approximation.

## 89. Fourier Galerkin assembly without differentiating sampled metrics

On the periodic surface, use
\[
v_{\ell p}=e^{i\ell\theta+ip\zeta}.
\]
Let
\[
s=\sqrt D,\qquad
C^{ab}=s\gamma^{ab}.
\]
A common factor \((2\pi)^2\) can be omitted from both matrices. With Fourier coefficients defined by cell averages,
\[
\mathsf M_{ij}=\widehat{s}_{k_i-k_j},
\]
\[
\mathsf K_{ij}
=
\ell_i\ell_j\widehat{C^{\theta\theta}}_{k_i-k_j}
+(\ell_ip_j+p_i\ell_j)\widehat{C^{\theta\zeta}}_{k_i-k_j}
+p_ip_j\widehat{C^{\zeta\zeta}}_{k_i-k_j}
+\widehat{sM^2}_{k_i-k_j}.
\]
This is the exact Galerkin structure when the Fourier coefficient integrals are exact. The implementation approximates those integrals by periodic trapezoidal quadrature and FFT.

No numerical differentiation of the metric is needed in this weak formulation. The radius derivatives entering the metric are evaluated analytically. This avoids amplification of metric sampling noise by repeated differentiation.

For a real geometry,
\[
\widehat f_{-k}=\widehat f_k^*,
\]
which ensures Hermitian matrices up to arithmetic errors. The mixed metric term is essential; dropping it changes the surface operator at quadratic order in corrugation slope.

Increasing the Fourier cutoff improves the trial space. Increasing the quadrature resolution improves the coefficient integrals. These are distinct convergence directions and are varied separately in the verification suite.

## 90. Ritz values, residuals, and what they certify

For a conforming Galerkin method with exact integrals, the min–max principle makes discrete low eigenvalues upper bounds to their continuum counterparts. Enlarging a nested trial space lowers these Ritz values, with multiplicity handled appropriately.

In the actual computation, quadrature and floating point errors perturb that property. Tiny nonmonotonic changes at the arithmetic floor should not be interpreted as physical effects. A finite matrix result is not an interval certified continuum eigenvalue.

For a computed eigenpair \((\widehat\nu,\widehat u)\), the algebraic residual is
\[
r=\mathsf K\widehat u-\widehat\nu\mathsf M\widehat u.
\]
The implementation reports the scaled residual
\[
\epsilon_{\mathrm{alg}}
=
\frac{\|r\|_2}
{\left(\|\mathsf K\|_2+|\widehat\nu|\|\mathsf M\|_2\right)\|\widehat u\|_2}.
\]
A small residual verifies the solution of the assembled matrix problem. It does not measure basis truncation error, quadrature error, geometry model error, or uncertainty in physical coefficients.

A useful error hierarchy is
\[
\text{model choice}
\;\to\;
\text{continuum problem}
\;\to\;
\text{basis truncation}
\;\to\;
\text{quadrature}
\;\to\;
\text{algebraic solve}.
\]
Accuracy at a later stage cannot compensate for an uncontrolled earlier stage.

## 91. Exact constant mode as a geometry test

For any connected closed or periodic smooth surface,
\[
-\Delta_\gamma1=0.
\]
With constant \(M^2=m_\Sigma^2\) and unit lapse,
\[
A1=m_\Sigma^2.
\]
Since the Laplacian is nonnegative, this is exactly the ground eigenvalue:
\[
\boxed{\nu_0=m_\Sigma^2.}
\]
For the declared benchmark,
\[
\boxed{\nu_0=\frac14}
\]
for every admissible corrugation amplitude, including beyond perturbation theory.

The numerical value may differ from \(1/4\) at the algebraic arithmetic level because a dense generalized eigensolver is used. That discrepancy should be reported as numerical error, not as a geometric mass correction.

An intrinsic curvature potential \(\xi\mathcal R_\Sigma\), extrinsic curvature potential, nonconstant \(U_\Sigma\), or nonconstant lapse changes the operator and can remove this exact result. The theorem applies to the specific operator \(-\Delta_\gamma+m_\Sigma^2\).

This benchmark is particularly useful because it tests the mass matrix and variable area element together. An implementation that discretizes the Laplacian inconsistently can spuriously shift the constant mode even when its pointwise derivatives vanish.

## 92. An exact nonconstant lapse ground state

Consider a one dimensional periodic spatial circle with metric
\[
ds^2=-N^2(x)dt^2+dx^2,\qquad
N(x)=1+\epsilon\cos x,\qquad |\epsilon|<1.
\]
Let the scalar mass squared be
\[
M^2=\frac14.
\]
The weighted evolution operator is
\[
Au=-N(Nu')'+\frac14N^2u,
\]
acting in
\[
L^2([0,2\pi],N^{-1}dx).
\]
Take
\[
u_0=N^{-1/2}.
\]
Since
\[
u_0'=-\frac12N^{-3/2}N',
\]
one finds
\[
\frac{Au_0}{u_0}
=
-\frac14(N')^2+\frac12NN''+\frac14N^2.
\]
Using
\[
N''=1-N,\qquad
(N')^2=\epsilon^2-(N-1)^2,
\]
all \(x\) dependence cancels:
\[
\boxed{Au_0=\frac{1-\epsilon^2}{4}u_0.}
\]

This is the ground state because \(u_0>0\). More explicitly, for \(u=u_0f\), integration by parts yields the ground state representation
\[
\mathfrak a[u,u]-\nu_0\|u\|_{\mathcal H}^2
=
\int_0^{2\pi}Nu_0^2|f'|^2dx\ge0.
\]
For \(\epsilon=1/5\),
\[
\boxed{\nu_0=\frac6{25}.}
\]
The numerical lapse benchmark checks this exact value. A solver that replaces the weighted problem by \(-\partial_x^2+1/4\) would incorrectly retain \(1/4\).

## 93. Geometry quadrature and topological checks

The geometry benchmark evaluates
\[
\operatorname{Area}=\int_0^{2\pi}\int_0^{2\pi}\sqrt D\,d\theta\,d\zeta,
\]
\[
I_K=\int K_G\,dA,\qquad
I_{H^2}=\int H^2\,dA.
\]
It uses \(Q=32,64,128,256\) equally spaced points in each phase coordinate.

The exact geometric expectations are:

- \(D>0\) because \(R>0\) and \(a>0\).
- \(H^2-K_G\ge0\) pointwise.
- \(I_K=0\) for the smooth periodic quotient metric.
- The \(A\to0\) area is \(4\pi^2aR_0\).
- The \(A\to0\) curvature integral is
\[
I_{H^2}=\frac{\pi^2a}{R_0}.
\]

Numerical minima sampled on a grid are not rigorous global minima. The exact lower bound
\[
R\ge R_0-|A|
\]
and
\[
D\ge a^2(R_0-|A|)^2
\]
supply global statements independently of sampling. For the benchmark,
\[
R\ge\frac9{10},
\qquad
D\ge\frac{729}{400}.
\]
The sampled minimum can be compared with these bounds, but the proof comes from the analytic expression.

The small nonzero computed \(I_K\) measures arithmetic and quadrature cancellation. It is not evidence of a nonzero Euler characteristic.

## 94. Time integration and a separate temporal error test

For the modal Hamiltonian
\[
H(q,p)=\frac12p^2+\frac12\omega_0^2q^2+\frac g4q^4,
\]
the velocity Verlet update is
\[
p_{n+1/2}=p_n-\frac{\Delta t}{2}(\omega_0^2q_n+gq_n^3),
\]
\[
q_{n+1}=q_n+\Delta t\,p_{n+1/2},
\]
\[
p_{n+1}=p_{n+1/2}
-\frac{\Delta t}{2}(\omega_0^2q_{n+1}+gq_{n+1}^3).
\]
This method is second order and symplectic. It does not preserve the exact original Hamiltonian at every step, but for stable smooth dynamics it has a nearby modified Hamiltonian interpretation over suitable time scales.

The benchmark uses
\[
\omega_0^2=\frac54,\qquad
g=\frac34,\qquad
A_q=\frac12,\qquad
T_{\mathrm{end}}=20.
\]
The exact elliptic parameter is
\[
k^2=\frac3{46}.
\]
The timestep sequence is
\[
\Delta t=\frac1{50},\quad\frac1{100},\quad\frac1{200},
\]
corresponding to \(1000,2000,4000\) steps.

The final position and momentum are compared with the exact Jacobi elliptic solution. The maximum absolute energy drift is recorded over the whole trajectory. The position error ratio approaches four under timestep halving, as expected for second order convergence.

A field simulation additionally requires a spatial convergence test. Passing this oscillator test verifies the temporal integrator in a nonlinear conservative setting; it does not establish convergence of a spatial PDE discretization.

## 95. Stability restrictions and nonlinear aliasing

For a linear semidiscrete system
\[
\mathsf M\ddot q+\mathsf Kq=0
\]
with positive eigenvalues \(\nu_j\), leapfrog stability requires
\[
\Delta t\sqrt{\nu_{\max}}\le2
\]
in exact arithmetic. Equality is a marginal endpoint; practical computations retain a margin.

A quartic nonlinearity changes local oscillation frequencies. A timestep selected from the initial linear spectrum can become inadequate if the amplitude grows. A safe adaptive criterion must account for the evolving Hessian or use an integrator designed for the resulting stiffness.

For a Fourier representation retaining frequencies through \(K\), a cubic product contains frequencies through \(3K\). To project that product back onto the retained modes without aliasing, the product quadrature must resolve differences between the product spectrum and the test spectrum. In one dimension, a uniform grid with more than \(4K\) points is sufficient for exact polynomial Fourier projection in this simple cubic setting. Tensor product analogues apply in multiple directions.

The familiar padding rules for quadratic nonlinearities should not be transferred blindly to cubic terms. Filtering or de-aliasing changes discrete high frequency behavior; its effect should be stated and checked against the chosen weak projection.

Variable metric coefficients are not finite Fourier polynomials in general. Their product quadrature therefore requires convergence rather than a finite exact mode count alone.

## 96. Manufactured solutions for a full PDE implementation

A manufactured solution verifies the assembled PDE independently of naturally occurring eigenmodes. Choose a smooth function satisfying the boundary conditions, for example
\[
\phi_{\mathrm{ex}}(t,\theta,\zeta)
=
\cos(\omega t)\left[1+\epsilon_s\cos\theta\cos\zeta\right]
\]
on a periodic surface. Define the source by direct substitution:
\[
J_{\mathrm{ex}}
=
\Box_q\phi_{\mathrm{ex}}
-m_\Sigma^2\phi_{\mathrm{ex}}
-\lambda_\Sigma\phi_{\mathrm{ex}}^3
-2U_\Sigma\phi_{\mathrm{ex}}.
\]
Then the source driven PDE has the prescribed exact solution with matching initial data.

This test probes metric derivatives, mixed terms, nonlinear assembly, source sign, and temporal integration. Its source must be computed by an independent analytical or symbolic route if it is to detect an implementation error in the operator. Reusing the same discrete operator to manufacture the source can make the test tautological.

For bulk cylindrical geometry, a smooth Cartesian polynomial times a periodic axial factor can test axis handling. A manufactured expression singular at \(r=0\) does not validate a smooth axis code.

The present executed suite covers the linear surface operator and a nonlinear temporal reduction. A complete production PDE solver would add manufactured solution tests, boundary reflection tests, and field energy convergence before claiming nonlinear surface dynamics.

## 97. Mesh convergence, eigenvalue multiplicity, and mode tracking

A convergence report should track eigenvalues and eigenspaces. Near degeneracy, individual eigenvectors can rotate arbitrarily within a nearly degenerate subspace. Comparing their raw components between resolutions can therefore exaggerate error.

For a cluster, compare the spectral projector or the principal angles between the mass normalized subspaces. A mode label based only on sorted eigenvalue order can switch at an avoided crossing. Symmetry sectors, overlap with a reference basis, and continuation in parameters provide more reliable tracking.

For three resolutions \(h,h/2,h/4\), an observed order estimate is
\[
p_{\mathrm{obs}}
=
\log_2
\left|
\frac{Q_h-Q_{h/2}}{Q_{h/2}-Q_{h/4}}
\right|.
\]
This formula assumes a leading algebraic error law with a nonzero coefficient and requires all three calculations to be in that regime. Spectral methods can converge faster than any fixed algebraic order for analytic data, so a finite \(p_{\mathrm{obs}}\) may not have a useful asymptotic interpretation.

A stopping rule should compare numerical uncertainty with the scientific effect being tested. If the predicted splitting is smaller than the resolution change, it is unresolved. Reporting many digits of a matrix eigenvalue does not resolve that problem.

## 98. Conditioning, precision, and exact numeric reporting

The generalized eigenproblem can be reduced using a Cholesky factorization
\[
\mathsf M=LL^\dagger,
\qquad
L^{-1}\mathsf K L^{-\dagger}y=\nu y.
\]
This is appropriate when \(\mathsf M\) is positive definite. Explicitly forming \(\mathsf M^{-1}\mathsf K\) can destroy visible Hermiticity and worsen conditioning.

A highly corrugated geometry, large lapse contrast, nearly dependent basis, or extreme aspect ratio can produce ill conditioned matrices. Increasing arithmetic precision is useful only after the formulation and scaling have been checked.

The numerical receipt in this document records each stored binary64 number as an exact decimal and as a hexadecimal float. This prevents display rounding from obscuring the recorded arithmetic. It does not turn a floating point result into an exact continuum value.

There are three distinct meanings of precision:

- Exact symbolic precision, such as \(\nu_0=6/25\).
- Arithmetic precision, such as a particular binary64 value.
- Verified numerical accuracy, inferred from residuals, convergence, or rigorous bounds.

Physical significant figures add a fourth layer and depend on uncertainty in measured inputs. The benchmarks use exact mathematical inputs and contain no physical measurement uncertainty. Values such as \(1/10\) are converted to their nearest representable binary64 value only inside the numerical implementation, with that limitation declared.

## 99. Reproducibility receipt and computational scope

The executable appendix uses Python, NumPy, and SciPy. It computes:

1. Explicit Clifford anticommutator checks for the stated convention.
2. Bessel roots and direct function residuals.
3. Surface area and curvature integrals at four quadrature resolutions.
4. Corrugated surface spectra at four Fourier cutoffs.
5. External potential spectra on a straight cylinder at the same cutoffs.
6. A variable lapse periodic spectrum at three cutoffs.
7. A separate quadrature refinement at fixed Fourier cutoff.
8. Duffing trajectory errors and energy drift against an exact solution.
9. Assertions for the flat cylinder, constant surface mode, exact lapse ground state, and temporal convergence.

The code is deterministic. The complete source and output are embedded so that the document remains self contained. The receipt is an execution record, not a claim that every theorem in the monograph was machine proved.

The checks address independent risks: wrong Clifford sign, incorrect geometry factors, loss of the constant mode, omission of lapse weights, basis truncation, quadrature error, and temporal integration error. They are selected for their diagnostic value rather than for a large count of superficially passing tests.

## 100. Numerical interpretation before the tables

The surface geometry calculation changes excited eigenvalues while retaining the exact ground value \(1/4\). The separate potential calculation shifts the ground value below \(1/4\), consistent with the negative second order shift \(-9/4000\). The difference between the second order estimate and the converged finite basis value measures higher order potential mixing at the chosen amplitude.

The variable lapse calculation reproduces the exact ground value \(6/25\). It therefore tests a feature absent from a flat unweighted Laplacian. The Duffing timestep error ratios approach four, consistent with the integrator's second order accuracy.

The table values that follow are exact decimal expansions of stored machine numbers. Their interpretation is constrained by the adjacent cutoff and quadrature comparisons. Residuals assess the finite matrix solve. They do not certify that the last decimal is a continuum digit.

These experiments establish that the selected mathematical implementation behaves consistently with its exact limits and perturbative structure. They do not establish that a laboratory system realizes the selected action, that the couplings have been measured, or that the model is a new fundamental interaction.

## 101. Executed geometric integrals

Every numeric cell below is an exact decimal representation of the stored binary64 value. The exact Gaussian curvature integral is zero; its nonzero entries are numerical residuals.

| Points per coordinate | Area | Integral of Gaussian curvature | Integral of mean curvature squared |
| --- | --- | --- | --- |
| 32 | 59.545452879848568272791453637182712554931640625 | 5.5277613874308684797925131406529344522092495051168725694878958165645599365234375E-13 | 15.1973861857146115283967446885071694850921630859375 |
| 64 | 59.545452879848568272791453637182712554931640625 | 6.4203879199401465259081620305690930555048666350526076485039084218442440032958984375E-17 | 15.1973861857030971833637522649951279163360595703125 |
| 128 | 59.54545287984857537821881123818457126617431640625 | 2.140129306646715714068581411494855344472602754076449860232145283589488826692104339599609375E-17 | 15.1973861857030971833637522649951279163360595703125 |
| 256 | 59.54545287984857537821881123818457126617431640625 | 1.712103445317372447995348688412789679995493877825811501747210741086746565997600555419921875E-17 | 15.1973861857030971833637522649951279163360595703125 |


## 102. Executed surface and potential spectra

The listed eigenvalues are squared frequencies. The constant ground mode in the geometry experiment is exactly one quarter. Decimal discrepancies from that fraction are numerical.

### Corrugated metric, zero external potential

| Fourier cutoff | Matrix dimension | Lowest squared frequency | Next squared frequency | Third squared frequency |
| --- | --- | --- | --- | --- |
| 3 | 49 | 0.25000000000000011102230246251565404236316680908203125 | 0.6915788054956963915032019940554164350032806396484375 | 0.6961106902018820985489355734898708760738372802734375 |
| 5 | 121 | 0.24999999999999611421941381195210851728916168212890625 | 0.691577881656254334075129008851945400238037109375 | 0.6961102077555982869938588919467292726039886474609375 |
| 7 | 225 | 0.2500000000000295319324550291639752686023712158203125 | 0.69157788090181349094365259588812477886676788330078125 | 0.69611020724719996355389639575150795280933380126953125 |
| 9 | 361 | 0.25000000000002120525977034048992209136486053466796875 | 0.69157788090143335058002094228868372738361358642578125 | 0.69611020724447414398383671141345985233783721923828125 |


| Cutoff | Maximum scaled algebraic residual | Maximum Hermiticity discrepancy |
| --- | --- | --- |
| 3 | 4.8857379755354558629750410255440720903004152807225235477517344406805932521820068359375E-16 | 1.9947301009923321357462866313814632706541599992447998113132001662961556576192378997802734375E-17 |
| 5 | 4.617455707296191945545762950919868719371435519978341677216349125956185162067413330078125E-16 | 3.583561317026776129509378522892929870652852303238196374213231365501997061073780059814453125E-17 |
| 7 | 5.291633310098403650577077671853971571819521212652615016480694976053200662136077880859375E-16 | 1.8908140758317276149527186887368681329077020592498159512473421273170970380306243896484375E-16 |
| 9 | 1.18478085407164929734618878569465855737314415215000185099825102952308952808380126953125E-15 | 1.8908140758317276149527186887368681329077020592498159512473421273170970380306243896484375E-16 |


### Straight cylinder, sinusoidal external potential

| Fourier cutoff | Matrix dimension | Lowest squared frequency | Next squared frequency | Third squared frequency |
| --- | --- | --- | --- | --- |
| 3 | 49 | 0.247749716642788830878174621830112300813198089599609375 | 0.69069781644021521760379300758359022438526153564453125 | 0.6935068621193927196344475305522792041301727294921875 |
| 5 | 121 | 0.24774948726337886473203298010048456490039825439453125 | 0.69069735578059410219253777540870942175388336181640625 | 0.69350681214280296416063720243982970714569091796875 |
| 7 | 225 | 0.247749487260288725476442550643696449697017669677734375 | 0.6906973557740077040989490342326462268829345703125 | 0.693506812142352213612639388884417712688446044921875 |
| 9 | 361 | 0.247749487260273404398702723483438603579998016357421875 | 0.69069735577400559467520224643521942198276519775390625 | 0.69350681214228415694122986678848974406719207763671875 |


| Cutoff | Maximum scaled algebraic residual | Maximum Hermiticity discrepancy |
| --- | --- | --- |
| 3 | 4.267351663960705050554378113983782397766939789747475675341092937742359936237335205078125E-16 | 4.3178049498783581719085367314691604371986427722486696911818881972067174501717090606689453125E-18 |
| 5 | 4.1040025414295491448736624254081641316870907444484817272467580551165156066417694091796875E-16 | 4.3178049498783581719085367314691604371986427722486696911818881972067174501717090606689453125E-18 |
| 7 | 5.96853331934107490874350955047958027966542061959476228594212443567812442779541015625E-16 | 4.3178049498783581719085367314691604371986427722486696911818881972067174501717090606689453125E-18 |
| 9 | 1.275738677695655983694028057972657548191819550098546898198037524707615375518798828125E-15 | 4.3178049498783581719085367314691604371986427722486696911818881972067174501717090606689453125E-18 |


### Finest cutoff spectrum, including multiplicities

| Ordered index | Corrugated metric | External potential |
| --- | --- | --- |
| 0 | 0.25000000000002120525977034048992209136486053466796875 | 0.247749487260273404398702723483438603579998016357421875 |
| 1 | 0.69157788090143335058002094228868372738361358642578125 | 0.69069735577400559467520224643521942198276519775390625 |
| 2 | 0.69611020724447414398383671141345985233783721923828125 | 0.69350681214228415694122986678848974406719207763671875 |
| 3 | 1.240222636882539308800232902285642921924591064453125 | 1.238386397900666846538797472021542489528656005859375 |
| 4 | 1.240222636882613027609068012679927051067352294921875 | 1.238386397900697044605067276279442012310028076171875 |
| 5 | 1.677093650491118470569062992581166326999664306640625 | 1.69230261989189845195369343855418264865875244140625 |
| 6 | 1.67709365049113667822666684514842927455902099609375 | 1.69230261989189845195369343855418264865875244140625 |
| 7 | 1.691498653156310094658465459360741078853607177734375 | 1.702660896891451169921083419467322528362274169921875 |
| 8 | 1.6914986531563283023160693119280040264129638671875 | 1.702660896891451169921083419467322528362274169921875 |


The exact difference between the stored finest potential ground value and the second order estimate 991/4000 is -5.12739726595601297276516561396420001983642578125E-7. This is a comparison of the numerical value with the perturbative expression, not a certified all orders remainder bound.

The maximum absolute change among the first nine stored geometry eigenvalues from cutoff 7 to cutoff 9 is 9.9801056308024271856993436813354492187500E-11. This gives an observed truncation sensitivity at these cutoffs; it is not a rigorous continuum error enclosure.

### Quadrature refinement at fixed Fourier cutoff 7

| Quadrature points per coordinate | Lowest excited squared frequency | Third squared frequency |
| --- | --- | --- |
| 64 | 0.69157788090180272178031373186968266963958740234375 | 0.696110207247190526658187081920914351940155029296875 |
| 96 | 0.69157788090180949414076394532457925379276275634765625 | 0.69611020724717909136103344280854798853397369384765625 |
| 128 | 0.69157788090181349094365259588812477886676788330078125 | 0.69611020724719996355389639575150795280933380126953125 |


## 103. Executed lapse and radial benchmarks

The lapse ground eigenvalue is exactly 6/25. The higher values are numerical eigenvalues of the declared periodic operator.

| Fourier cutoff | Lowest squared frequency | Second squared frequency | Third squared frequency |
| --- | --- | --- | --- |
| 8 | 0.24000000000000032418512319054570980370044708251953125 | 1.19674769527484503583991681807674467563629150390625 | 1.2163852121136553563474080874584615230560302734375 |
| 16 | 0.239999999999969571007341073709540069103240966796875 | 1.19674769527484681219675621832720935344696044921875 | 1.216385212113636260511384534765966236591339111328125 |
| 24 | 0.240000000000036683989179664422408677637577056884765625 | 1.1967476952747677643174029071815311908721923828125 | 1.21638521211359229567960937856696546077728271484375 |


The Bessel roots below verify the radial spectral building blocks. Their exact definitions are the corresponding positive zeros of the Bessel function; the decimal entries record their computed representations.

| Angular order | First positive root | Second positive root | Third positive root | Maximum absolute function residual |
| --- | --- | --- | --- | --- |
| 0 | 2.404825557695772442201587182353250682353973388671875 | 5.52007811028631056871063265134580433368682861328125 | 8.653727912911012509766806033439934253692626953125 | 1.040353654866447615182703286451465231599946379835615328790510147882741875946521759033203125E-16 |
| 1 | 3.831705970207512468306276787188835442066192626953125 | 7.0155866698156188476787065155804157257080078125 | 10.1734681350627216289694842998869717121124267578125 | 2.43500876579685830365477449589424523738336969373718954301466510514728724956512451171875E-16 |
| 2 | 5.13562230184068280181008958606980741024017333984375 | 8.41724414039986612579014035873115062713623046875 | 11.6198411721490604264772628084756433963775634765625 | 2.58902878456593245018838810614093019051232670395268353757955992477945983409881591796875E-16 |


## 104. Executed nonlinear temporal benchmark

The exact period is the elliptic integral expression given earlier. Its computed stored value is 5.329266301866848465351722552441060543060302734375.

| Steps through time 20 | Final position error | Final momentum error | Maximum energy error |
| --- | --- | --- | --- |
| 1000 | 0.00026742056766544154700060431650854297913610935211181640625 | 0.0000441809950804117335110277053900063037872314453125 | 0.0000226074476152582359844700476969592273235321044921875 |
| 2000 | 0.0000668526529534717306457736185620888136327266693115234375 | 0.00001103049525408295039596850983798503875732421875 | 0.000005651857166333318360784687683917582035064697265625 |
| 4000 | 0.00001671300755205773480582820411655120551586151123046875 | 0.00000275670179672449222607610863633453845977783203125 | 0.000001412963962998947664573279325850307941436767578125 |


The position error ratios under timestep halving are 4.0001489223107054016281836084090173244476318359375, 4.0000372611116734589131738175638020038604736328125. Their convergence toward four is the expected second order signature.

### Independent check summary

| Check | Recorded absolute discrepancy |
| --- | --- |
| flat cylinder max error | 2.220446049250313080847263336181640625E-16 |
| corrugated constant mode error | 2.120525977034048992209136486053466796875E-14 |
| lapse exact ground error | 3.6692870963861423661001026630401611328125E-14 |


The Clifford anticommutator discrepancy is 0. This calculation uses explicit matrix entries that are exactly representable in the stated arithmetic. The flat cylinder, constant surface mode, lapse ground state, and Duffing convergence assertions all completed successfully in the recorded run.

---

# Part XIII. Further analytical reductions and exact examples

## 105. A corrugated boundary is a third spectral mechanism

The same radial graph can define the boundary of a bulk domain,
\[
\Omega_R=\{0\le r<R(\theta,\zeta)\},
\]
instead of defining the manifold on which the scalar lives. A Dirichlet bulk scalar on \(\Omega_R\), a scalar intrinsic to its surface, and a scalar in a fixed cylinder with a corrugated potential are three inequivalent problems.

For a simple Dirichlet eigenvalue of
\[
-\Delta u+M^2u=\nu u,
\qquad u|_{\partial\Omega}=0,
\qquad \int_\Omega|u|^2dV=1,
\]
a small outward boundary displacement \(f\) gives the Hadamard shape derivative
\[
\boxed{
\delta\nu
=
-\int_{\partial\Omega}f\,|\partial_nu|^2\,dS
}
\]
when \(M^2\) is a fixed spatial constant. The formula follows by differentiating the boundary condition,
\[
\delta u|_{\partial\Omega}=-f\partial_nu,
\]
and integrating the perturbed eigen equation against \(u\).

An outward enlargement \(f\ge0\) therefore lowers Dirichlet eigenvalues at first order. This differs from the intrinsic surface constant mode, which remains exactly at \(M^2\) under a metric deformation.

For a degenerate bulk eigenspace, the first order splitting is obtained from the boundary matrix
\[
B_{ab}
=
-\int_{\partial\Omega}f\,(\partial_nu_a)^*(\partial_nu_b)\,dS.
\]
The corrugation harmonics impose selection rules through this integral, but the radial derivatives and wall geometry determine its magnitude.

If the physical potential moves with the material boundary, its variation contributes additional terms. The derivative above applies to a fixed constant bulk potential and a moving Dirichlet wall.

## 106. Thin layer dimensional reduction with explicit normalization

Let \(y\) be a normal coordinate across a thin layer of thickness \(d\), and \(\sigma^a\) be surface coordinates. In a locally flat approximation, expand
\[
\phi(t,\sigma,y)=\sum_\alpha\chi_\alpha(y)\varphi_\alpha(t,\sigma),
\]
with
\[
\int dy\,\chi_\alpha\chi_\beta=\delta_{\alpha\beta}.
\]
Suppose the transverse operator obeys
\[
\left[-\partial_y^2+V_\perp(y)\right]\chi_\alpha
=\epsilon_\alpha\chi_\alpha.
\]
Keeping one transverse mode gives
\[
m_\Sigma^2=m_4^2+\epsilon_0
\]
plus any averaged quadratic coefficient and curvature corrections derived from the full coordinate measure.

The quartic coupling becomes
\[
\boxed{
\lambda_\Sigma=\lambda_4\int dy\,\chi_0^4.
}
\]
For an ideal Dirichlet layer
\[
-\frac d2<y<\frac d2,
\qquad
\chi_0(y)=\sqrt{\frac2d}\cos\left(\frac{\pi y}{d}\right),
\]
one has
\[
\epsilon_0=\frac{\pi^2}{d^2},
\qquad
\int\chi_0^4dy=\frac3{2d},
\]
so
\[
\boxed{\lambda_\Sigma=\frac{3\lambda_4}{2d}.}
\]
This explicitly reproduces the mass dimension one of the surface quartic coupling.

The one mode approximation requires tangential frequencies, nonlinear shifts, and geometric mixing to be small compared with the transverse excitation gap. As \(d\to0\), the transverse mass diverges unless a subtraction or tuning is part of the physical model. A low energy surface field is therefore not obtained merely by deleting one coordinate.

## 107. Curvature corrections in a tubular neighborhood

For the normal displacement map
\[
X_y(\sigma)=X(\sigma)+y\mathbf n(\sigma),
\]
the principal tangent stretch factors in the present curvature convention are
\[
1+yk_1,\qquad1+yk_2.
\]
Thus the local volume factor is
\[
\sqrt{g_{\mathrm{tube}}}
=
\sqrt\gamma\,(1+2Hy+K_Gy^2)
\]
within the tubular neighborhood where the normal coordinates remain nonsingular.

The condition
\[
|y k_i|<1
\]
keeps the local coordinate map regular. A controlled thin layer expansion requires
\[
d|H|\ll1,\qquad d^2|K_G|\ll1
\]
and control of tangential derivatives of curvature.

The transverse normalization itself becomes curvature dependent before a field redefinition is applied. Integrating out transverse modes can generate curvature potentials, modified kinetic coefficients, and couplings between transverse bands. A universal coefficient cannot be assigned without specifying the parent kinetic operator and confinement procedure.

This is the geometric reason the induced metric theory and the confinement derived theory need not coincide. Both can be legitimate effective descriptions, but they encode different microscopic assumptions.

For a layer with asymmetric confinement, odd normal moments such as
\[
\int y\,\chi_0^2dy
\]
need not vanish, so terms linear in mean curvature can appear when allowed by orientation and material symmetry.

## 108. A useful exact localized mode with a negative local mass region

Consider the one dimensional operator
\[
A=-\frac{d^2}{dx^2}+m_\infty^2-s(s+1)\kappa^2\operatorname{sech}^2(\kappa x),
\qquad s>0.
\]
The trial function
\[
u_0(x)=C\,\operatorname{sech}^s(\kappa x)
\]
is in fact an exact ground eigenfunction. Its logarithmic derivatives are
\[
\frac{u_0'}{u_0}=-s\kappa\tanh(\kappa x),
\]
\[
\frac{u_0''}{u_0}
=
s^2\kappa^2-s(s+1)\kappa^2\operatorname{sech}^2(\kappa x).
\]
Therefore
\[
\boxed{Au_0=(m_\infty^2-s^2\kappa^2)u_0.}
\]
Since \(u_0>0\), it is the ground state. The continuum begins at \(m_\infty^2\).

Choose
\[
s=1,\qquad\kappa=1,\qquad m_\infty^2=\frac32.
\]
The local coefficient reaches
\[
M^2(0)=\frac32-2=-\frac12,
\]
but the exact ground eigenvalue is
\[
\boxed{\nu_0=\frac12>0.}
\]
The linear system is stable despite a negative local mass squared region.

The instability threshold is \(m_\infty^2=1\), not the pointwise threshold \(m_\infty^2=2\). This explicit example demonstrates the difference between a local tachyonic tendency and a negative global mode without relying on a numerical approximation.

## 109. Exact normalization and nonlinear overlap for the localized example

For \(s=1\),
\[
\int_{-\infty}^{\infty}\operatorname{sech}^2(\kappa x)\,dx=\frac2\kappa.
\]
The normalized ground mode is
\[
u_0(x)=\sqrt{\frac\kappa2}\operatorname{sech}(\kappa x).
\]
Using
\[
\int_{-\infty}^{\infty}\operatorname{sech}^4(\kappa x)\,dx=\frac4{3\kappa},
\]
its quartic overlap is
\[
\boxed{C_4=\int u_0^4dx=\frac\kappa3.}
\]
The one mode quartic equation is therefore
\[
\ddot q+(m_\infty^2-\kappa^2)q+\frac{\lambda\kappa}{3}q^3=0.
\]
This supplies an exact spatial overlap for a nonlinear reduced model.

The reduction is still not an exact invariant subspace of the nonlinear PDE because
\[
u_0^3\not\propto u_0.
\]
The cubic source has components in other discrete modes or the continuum. The exact overlap determines the retained self interaction, while the complementary projection determines leakage.

In a higher dimensional separable geometry, transverse normalized modes multiply \(u_0\), and their quartic overlap factors multiply \(C_4\). The effective coupling then has the dimensions appropriate to the reduced theory. This prevents importing a one dimensional coefficient directly into a bulk action without normalization factors.

## 110. Ground state transformation and a general positivity proof

Suppose a positive function \(u_0\) satisfies
\[
Au_0=\nu_0u_0
\]
for the weighted scalar operator. Write \(u=u_0f\). The quadratic form can be expanded and integrated by parts using the equation for \(u_0\). The cross terms cancel, giving
\[
\boxed{
\mathfrak a[u,u]-\nu_0\|u\|_{\mathcal H}^2
=
\int_\Omega Nu_0^2|Df|_h^2\,dV_h
}
\]
when boundary terms vanish or match the declared ground state boundary conditions.

The right side is nonnegative. Consequently \(\nu_0\) is a lower spectral bound, and when \(u_0\) belongs to the operator domain it is the ground eigenvalue.

This identity proves the lapse circle result and the localized \(\operatorname{sech}\) example. It also provides a way to construct exactly solvable benchmark potentials: choose a positive \(u_0\), select \(\nu_0\), and solve its eigen equation for the coefficient \(M^2(x)\).

Such inverse construction is a mathematical benchmark design. It is not a derivation of a physical potential from an independently specified material. The direction of construction must be disclosed when interpreting the result.

The identity is also useful numerically: violations of the corresponding nonnegative discrete form can expose inconsistencies between the operator, measure, and boundary terms.

## 111. Unitary conversion of the lapse weighted Hilbert space

For a static spatial metric, the mode Hilbert space has measure \(dV_h/N\). Define
\[
u=\sqrt N\,v.
\]
Then
\[
\|u\|_{\mathcal H}^2=\int|v|^2dV_h.
\]
The unitarily transformed operator is
\[
\widetilde A=N^{-1/2}AN^{1/2}.
\]
Expanding derivatives yields
\[
\boxed{
\widetilde A
=
-D_i(N^2D^i)
+N^2M^2-\frac12N\Delta_hN-\frac14|DN|_h^2.
}
\]
This acts in the ordinary spatial \(L^2(dV_h)\) space.

The transformed expression is manifestly divergence form in its principal part, with an additional lapse dependent potential. It is not simply \(-\Delta_h+M^2\). The principal coefficient \(N^2\) still carries the local coordinate propagation speed.

The transformation is valid when \(N\) is positive and sufficiently regular, and when the operator domain and boundary conditions are transformed as well. For Robin data,
\[
s^iD_i(\sqrt N\,v)+\alpha\sqrt N\,v=0,
\]
so the transformed Robin coefficient includes
\[
\frac12s^iD_i\log N.
\]
Changing the Hilbert measure while leaving the boundary domain untouched can change the spectrum.

## 112. Generalized geometric perturbation inside a degenerate subspace

On the straight periodic surface cylinder, normalize Fourier modes with the unperturbed area measure. Let a degenerate multiplet have common squared frequency \(\nu_*\), and perturb the radius by \(\eta\).

The first order matrix is obtained from
\[
\delta\mathsf K-\nu_*\delta\mathsf M.
\]
Using the coefficient variations derived earlier gives
\[
\boxed{
B_{ij}
=
\frac{\widehat\eta_{k_i-k_j}}{R_0}
\left[
-\frac{\ell_i\ell_j}{R_0^2}
+\frac{p_ip_j}{a^2}
+m_\Sigma^2-\nu_*
\right].
}
\]
This expression assumes no additional curvature or external potential and a unit lapse. It is Hermitian because the bracket is symmetric in \(i,j\) and the radius perturbation is real.

For a uniform radius shift \(\eta=\eta_0\), the diagonal result is
\[
\delta\nu_{\ell p}=-\frac{2\ell^2}{R_0^3}\eta_0,
\]
which is exactly the derivative of \(\ell^2/R_0^2\). For the constant mode, \(\ell=p=0\) and \(\nu_*=m_\Sigma^2\), so every relevant first order coefficient vanishes, consistent with the exact constant mode theorem.

For a zero mean corrugation, isolated Fourier modes have zero diagonal first order shift. Degenerate pairs can still split through off diagonal entries. The coupling coefficient depends on both angular and axial indices, so an external potential matrix with the same harmonic support does not reproduce geometric mode mixing in general.

## 113. Resolvent projection and the error in a two mode model

Let \(P\) project onto a selected finite mode subspace and \(Q=I-P\). The eigenproblem
\[
Au=\nu u
\]
splits into
\[
(PAP-\nu)Pu+PAQ\,Qu=0,
\]
\[
QAP\,Pu+(QAQ-\nu)Qu=0.
\]
If \(QAQ-\nu\) is invertible,
\[
Qu=-(QAQ-\nu)^{-1}QAP\,Pu.
\]
Substitution gives the exact energy dependent reduced operator
\[
\boxed{
A_{\mathrm{eff}}(\nu)
=
PAP-PAQ(QAQ-\nu)^{-1}QAP.
}
\]
The second term is the effect of discarded modes. Neglecting it is the ordinary finite subspace truncation.

If the discarded spectrum stays at distance at least \(\Delta\) from \(\nu\),
\[
\|(QAQ-\nu)^{-1}\|\le\Delta^{-1},
\]
so
\[
\|A_{\mathrm{eff}}(\nu)-PAP\|
\le\frac{\|PAQ\|^2}{\Delta}.
\]
This supplies a quantitative condition for a two mode approximation:
\[
\|PAQ\|^2/\Delta
\]
must be small relative to the splitting or precision of interest.

Near another resonance, \(\Delta\) shrinks and the reduced subspace must be enlarged. The formal two by two avoided crossing expression remains algebraically correct for its own matrix, while its use as a full field prediction loses control.

## 114. Ray transport in a variable effective mass

In the massive Hamilton–Jacobi scaling, define
\[
\mathcal H(x,p)=\frac12\left(g^{\mu\nu}p_\mu p_\nu+M^2(x)\right).
\]
Hamilton's equations give
\[
\frac{dx^\mu}{d\lambda}=p^\mu,
\]
\[
\frac{Dp_\mu}{d\lambda}=-\frac12\nabla_\mu M^2.
\]
For \(M>0\), write
\[
p^\mu=Mu^\mu,\qquad u^\mu u_\mu=-1,
\qquad \frac{d\tau}{d\lambda}=M.
\]
Then
\[
\boxed{
u^\nu\nabla_\nu u^\mu
=
-(g^{\mu\nu}+u^\mu u^\nu)\nabla_\nu\log M.
}
\]
The force is orthogonal to the four velocity, as required by its normalization.

This trajectory law describes a semiclassical massive packet in a slowly varying effective mass background. It is not the characteristic equation for arbitrary high frequency wavefronts at fixed mass. The distinction follows from the different asymptotic scalings already stated.

At the next WKB order, the amplitude obeys a transport equation of the form
\[
\nabla_\mu(A^2p^\mu)=0
\]
for the conservative scalar problem. Caustics, turning points, and regions where \(M^2\) crosses zero require a different local approximation.

## 115. Restoring units without changing the field normalization silently

Take coordinates
\[
x^0=ct
\]
with all \(x^\mu\) carrying length units. Define a geometric scalar \(\phi_g\) of dimension \(L^{-1}\) and write
\[
\frac S\hbar
=
\int d^4x\sqrt{-g}
\left[
-\frac12(\nabla\phi_g)^2
-\frac12\mu_\phi^2\phi_g^2
-\frac{\lambda}{4}\phi_g^4
-U_g\phi_g^2
\right].
\]
Here
\[
\mu_\phi=\frac{m_{\mathrm{phys}}c}{\hbar},
\qquad [U_g]=L^{-2}.
\]
The flat equation in laboratory time is
\[
\boxed{
\frac1{c^2}\frac{\partial^2\phi_g}{\partial t^2}
-\nabla^2\phi_g
+\left(\frac{m_{\mathrm{phys}}^2c^2}{\hbar^2}+2U_g\right)\phi_g
+\lambda\phi_g^3=0.
}
\]
The physical energy is
\[
E_{\mathrm{SI}}
=
\hbar c
\int d^3x
\left[
\frac1{2c^2}\phi_{g,t}^2
+\frac12|\nabla\phi_g|^2
+\frac12\mu_\phi^2\phi_g^2
+\frac{\lambda}{4}\phi_g^4
+U_g\phi_g^2
\right].
\]
This fixes the field normalization rather than leaving its SI dimension implicit.

For gravity in these coordinates,
\[
F_g=\frac{c^3}{8\pi G\hbar}-\xi\phi_g^2.
\]
Multiplying the action by \(\hbar\) recovers the Einstein coefficient \(c^3/(16\pi G)\).

For a chosen length \(L_*\), use
\[
\tilde t=\frac{ct}{L_*},\qquad
\tilde r=\frac r{L_*},\qquad
\tilde z=\frac z{L_*},\qquad
\tilde\phi=L_*\phi_g,
\]
while \(\theta,\zeta\) remain dimensionless angles. Scaling an angular coordinate as though it were a length would change the metric components and is not the intended nondimensionalization.

---

# Part XIV. Observables, inference, and falsification

## 116. The observable map

A model becomes predictive when its parameters and inputs map to measured quantities. Let
\[
\mathbf p=(m_\phi^2,\lambda,U_0,U_1,\mu,R_0,A,a,n,m,\xi,\ldots)
\]
denote the parameters relevant to one selected realization. The forward map may include
\[
\mathcal F(\mathbf p)=
\{\omega_j,\ u_j,\ \text{response amplitudes},\ \text{growth rates},
\ \text{nonlinear frequency shifts},\ \text{shape displacements}\}.
\]
Discrete labels such as \(n,m\), continuous material coefficients, and boundary conditions should not all be treated as interchangeable fit parameters.

Eigenvalues alone do not determine every coefficient. Eigenfunctions sampled at several locations, driven response phases, mode overlaps, and nonlinear amplitude dependence can provide complementary information.

For a damped linear response model,
\[
\left[\mathsf K-\omega^2\mathsf M-i\omega\mathsf C\right]\mathbf q(\omega)
=\mathbf s(\omega).
\]
The sign of the damping term follows the convention \(e^{-i\omega t}\). Resonance linewidths depend on \(\mathsf C\), while resonance centers depend primarily on the conservative matrices when damping is weak. A static lossless action does not predict linewidths without an environment or radiation channel.

A measured waveform is also filtered by source and detector transfer functions. Those functions belong in the observation model rather than being absorbed without explanation into the field couplings.

## 117. Structural parameter degeneracies

For a constant external coefficient, the linear scalar equation contains only
\[
m_{\mathrm{eff}}^2=m_\phi^2+2U_c.
\]
A spectrum measured at one constant \(U_c\) cannot separate \(m_\phi^2\) from \(U_c\). It identifies their combination.

Likewise, if the only curvature invariant sampled is a fixed multiple of another,
\[
\mathcal R_\Sigma=2K_G,
\]
the corresponding coefficients are not independently identifiable from that data. A model with two labels for the same operator has a redundant parameterization.

For a single mode Duffing measurement, the nonlinear shift identifies
\[
g=\lambda C_4,
\]
not \(\lambda\) alone unless the normalized mode overlap and amplitude calibration are known. A rescaling of the field variable changes the apparent quartic coefficient and the source coupling together.

For a perfectly periodic isolated modulation, phase offsets are unidentifiable from eigenvalues because they are removable by translation. Relative phase becomes identifiable only with a registered second structure.

These degeneracies are exact features of the forward map. Collecting more measurements of the same invariant combination cannot remove them. The experimental design must vary geometry, coefficients, excitation, or observables in a way that changes the combinations being probed.

## 118. Sensitivity of generalized eigenvalues

For a simple eigenpair
\[
\mathsf K(\mathbf p)u_j=\nu_j\mathsf M(\mathbf p)u_j,
\qquad u_j^\dagger\mathsf M u_j=1,
\]
differentiate with respect to \(p_\alpha\):
\[
\boxed{
\frac{\partial\nu_j}{\partial p_\alpha}
=
u_j^\dagger
\left(
\frac{\partial\mathsf K}{\partial p_\alpha}
-\nu_j\frac{\partial\mathsf M}{\partial p_\alpha}
\right)u_j.
}
\]
For \(\nu_j>0\),
\[
\frac{\partial\omega_j}{\partial p_\alpha}
=
\frac1{2\omega_j}\frac{\partial\nu_j}{\partial p_\alpha}.
\]
Near a zero mode, frequency sensitivities can become large, while the squared frequency remains the regular quantity. Fitting \(\omega\) across an instability threshold is therefore less natural than fitting \(\nu=\omega^2\) and the associated growth rate.

At degeneracy, the derivative is a matrix in the degenerate eigenspace. A single scalar derivative assigned to one arbitrarily chosen eigenvector is not invariant. One diagonalizes the projected derivative matrix or tracks a symmetry resolved branch.

The same formula gives exact first order gradients for inverse design. A geometry optimization must include both stiffness and mass derivatives; changing the surface changes the integration measure as well as the differential operator.

## 119. Fisher information and its limitations

Let the observation vector be
\[
y=\mathcal F(\mathbf p)+\epsilon,
\]
with a declared covariance \(C\). In a local Gaussian approximation, define the Jacobian
\[
J_{i\alpha}=\frac{\partial\mathcal F_i}{\partial p_\alpha}.
\]
The Fisher information is
\[
\mathcal I=J^\mathsf T C^{-1}J.
\]
A null direction of \(\mathcal I\) indicates a locally unidentifiable parameter combination. A small eigenvalue indicates weak sensitivity relative to noise.

This calculation does not remove model discrepancy. If the actual system has an omitted curvature term, boundary loss, anisotropy, or nonlinear coupling, a precise fit within the restricted model can produce a biased parameter estimate.

A complete uncertainty model distinguishes
\[
y_{\mathrm{obs}}
=
\mathcal F_{\mathrm{continuum}}(\mathbf p)
+\delta_{\mathrm{model}}
+\delta_{\mathrm{num}}
+\epsilon_{\mathrm{meas}}.
\]
Numerical uncertainty should be made smaller than the effect under study and propagated when it is not negligible. Model discrepancy should not be silently interpreted as measurement noise.

Bayesian inference requires an explicit likelihood and priors. A posterior probability for a parameter within the selected model is not a posterior probability that the model is a new fundamental theory. Model comparison requires competing hypotheses and their predictive distributions.

## 120. A discriminating sequence of experiments

A practical test sequence can isolate the mechanisms in the action.

| Stage | Controlled change | Primary diagnostic |
|---|---|---|
| Straight reference | Set corrugation amplitude to zero | Baseline spectrum and boundary calibration |
| Metric deformation | Change shape while holding material coefficient model fixed | Geometric shifts and constant mode behavior |
| Potential modulation | Change constitutive coefficient on a fixed geometry | Quadratic mode mixing and ground shift |
| Harmonic change | Vary \(n,m\) independently | Angular and axial selection rules |
| Amplitude sweep | Vary excitation amplitude at fixed geometry | Quartic frequency shift and mode leakage |
| Phase registration | Shift corrugation relative to a fixed source or defect | Relative phase response |
| Time modulation | Drive geometry with measured mechanical work | Parametric resonance and energy balance |
| Released shape | Permit mechanical response | Scalar force induced deformation |
| Independent geometry | Predict a held out profile | Transferability of inferred coefficients |

The controls must be physically realizable. Changing the shape may also change thickness, tension, material composition, or confinement. Those changes should be measured or included in the constitutive model.

A strong test fixes parameters using one dataset and predicts a different geometry, mode family, or drive protocol without refitting every coefficient. Repeatedly choosing a new \(U(x)\) to fit each observation weakens the model's predictive content.

## 121. Distinguishing ordinary geometry effects from an additional interaction

Several effects in this monograph occur in established mathematical frameworks:

- A changed Laplacian produces changed eigenfrequencies.
- A periodic coefficient mixes Fourier modes.
- Degenerate perturbations produce avoided crossings.
- A quartic potential produces amplitude dependent frequency shifts.
- A curvature coupling changes an effective mass.
- A moving boundary can exchange energy with a field.

Observing one of these effects supports the corresponding effective model only after alternatives are controlled. It does not by itself establish an additional fundamental force or a new spacetime principle.

A stronger claim would require a quantitative deviation from the predictions of the applicable standard description, with systematic errors and model flexibility accounted for. The proposed action must then explain that deviation with a parameter structure that also predicts new observations.

A useful standard is predictive compression: one fixed, physically motivated action and a small set of independently constrained coefficients explain several distinct observables across multiple geometries. An arbitrary adjustable potential can fit many spectra but provides less explanatory constraint.

## 122. Stopping rules and falsifiable outcomes

Before running a parameter scan, specify a target observable and an acceptance criterion. Examples include:

1. A predicted selection rule has nonzero measured response in a forbidden sector exceeding calibrated leakage.
2. A predicted avoided crossing gap disagrees with a held out measurement beyond combined uncertainty.
3. The inferred quartic coefficient fails to transfer between modes after normalization.
4. A claimed stable configuration has a reproducible negative Hessian eigenvalue.
5. Energy balance requires an unmodeled source larger than the measured uncertainty.
6. A thin layer approximation fails as the excitation approaches the transverse gap.
7. A proposed gravitational solution violates a constraint or enters \(F\le0\).
8. A numerical effect disappears under refinement or changes with an unphysical coordinate origin.

Each outcome should trigger a declared response: reject the specific parameter choice, enlarge the model within a stated hierarchy, or reject the mechanism under the tested conditions. It should not trigger unrestricted post hoc adjustment while retaining the original claim.

A numerical stopping rule can require that the last two resolution changes are below a declared tolerance, that independent quadrature changes are smaller still, and that algebraic residuals are negligible relative to both. Such a rule provides operational reproducibility without claiming rigorous interval certification.

## 123. Research claims supported by the present work

The present construction supports the following statements at their stated levels:

| Statement | Status |
|---|---|
| The canonical real scalar action has the displayed Euler equation | Exact variational identity |
| The static lapse problem uses different temporal and spatial weights | Exact reduction |
| The radial graph has the displayed metric and curvature | Exact differential geometry |
| A unit lapse surface with constant mass retains its constant ground mode | Exact spectral result |
| A specific periodic lapse has ground eigenvalue \((1-\epsilon^2)/4\) | Exact benchmark proved here |
| A negative local mass region can coexist with a positive spectrum | Exact localized example |
| The selected Fourier implementation matches exact limits | Executed numerical verification |
| The quartic modal integrator converges at second order in the benchmark | Executed temporal verification |
| The selected geometry describes a real material system | Requires matching and experiment |
| The model is a new fundamental theory | Not established |
| A quantum ultraviolet completion exists | Not established |
| A fully nonlinear coupled gravity and surface simulation has been solved | Not performed in this document |

The separation between a mathematical result and a physical assertion is part of the model's rigor. It makes the successful results stronger because their hypotheses are visible and their limits are explicit.

## 124. Minimum complete model for each intended use

For a wave simulation on the corrugated surface, the minimum complete specification is
\[
X,\quad N_\Sigma,\quad V_\Sigma,\quad U_\Sigma,\quad
\varphi(0),\quad\partial_t\varphi(0),\quad\text{boundary data}.
\]
For a spectral calculation, replace the initial data with an operator domain and an eigenvalue target.

For a bulk scalar and fermion calculation, specify
\[
g,\quad U,\quad V,\quad M,\quad g_Y,\quad
\text{spin structure},\quad\text{scalar and spinor boundary data}.
\]
For dynamical gravity, add
\[
F,\quad Z,\quad\text{matter closure},\quad
h_{ij},K_{ij},\phi,p
\]
satisfying the gravitational constraints, together with coordinate gauge conditions.

For a dynamical membrane, specify the mass transport law, elastic energy, external pressure, boundary forces, scalar transport convention, and initial shape velocity. A static radius formula is insufficient.

For quantum predictions, add a state, regulator and renormalization conditions, boundary counterterms, and an effective theory validity range.

These lists are not alternative presentations of one automatically complete theory. They define different scientific problems. Selecting one makes the next calculation definite.

---

# Part XV. Detailed algebraic audits

## 125. Derivation of the nonminimal stress variation

Consider
\[
S_F=\frac12\int\sqrt{-g}\,F\mathcal R\,d^4x.
\]
At fixed scalar,
\[
\delta(F\mathcal R)=F\,\delta\mathcal R.
\]
The metric variation identity is
\[
\delta\mathcal R
=
R_{\mu\nu}\delta g^{\mu\nu}
+g_{\mu\nu}\Box\delta g^{\mu\nu}
-\nabla_\mu\nabla_\nu\delta g^{\mu\nu}
\]
up to the standard interpretation of the derivative terms before boundary integration.

Combining the determinant variation and integrating the derivative terms by parts gives
\[
\delta S_F
=
\frac12\int\sqrt{-g}
\left[
FG_{\mu\nu}
+g_{\mu\nu}\Box F-\nabla_\mu\nabla_\nu F
\right]\delta g^{\mu\nu}\,d^4x
+\text{boundary}.
\]
The matter variation is
\[
\delta S_m=-\frac12\int\sqrt{-g}\,T_{\mu\nu}\delta g^{\mu\nu}\,d^4x.
\]
Setting the total variation to zero yields
\[
FG_{\mu\nu}
=
T_{\mu\nu}+\nabla_\mu\nabla_\nu F-g_{\mu\nu}\Box F.
\]

For \(F=M_{\mathrm{Pl}}^2-\xi\phi^2\), the derivative term is
\[
\nabla_\mu\nabla_\nu F-g_{\mu\nu}\Box F
=
\xi(g_{\mu\nu}\Box-\nabla_\mu\nabla_\nu)\phi^2.
\]
This calculation fixes the sign of the improvement term directly. It also shows why replacing the curvature coupling by an algebraic potential during metric variation is insufficient.

## 126. Bianchi consistency of the scalar tensor equation

Take the divergence of
\[
FG_{\mu\nu}=T_{\mu\nu}+\nabla_\mu\nabla_\nu F-g_{\mu\nu}\Box F.
\]
The left side is
\[
(\nabla^\mu F)G_{\mu\nu}
\]
because \(\nabla^\mu G_{\mu\nu}=0\).

For a scalar \(F\),
\[
\nabla^\mu\nabla_\mu\nabla_\nu F-\nabla_\nu\Box F
=
R_{\nu\mu}\nabla^\mu F.
\]
Therefore
\[
(\nabla^\mu F)G_{\mu\nu}
=
\nabla^\mu T_{\mu\nu}+R_{\nu\mu}\nabla^\mu F,
\]
or
\[
\boxed{
\nabla^\mu T_{\mu\nu}
=
-\frac12\mathcal R\,\nabla_\nu F.
}
\]
For the canonical minimal scalar stress,
\[
\nabla^\mu T_{\mu\nu}^{\phi,\mathrm{min}}
=
(\Box\phi-V')\nabla_\nu\phi.
\]
The scalar equation is
\[
\Box\phi-V'=-\frac12F'\mathcal R
\]
when matter has no direct scalar coupling. Hence
\[
\nabla^\mu T_{\mu\nu}^{\phi,\mathrm{min}}
=
-\frac12\mathcal R\,F'\nabla_\nu\phi,
\]
which agrees exactly with the metric identity.

This is a stringent sign check. It uses both the scalar equation and the derivative terms in the metric equation. A metric equation assembled from a minimal stress tensor and an inserted curvature mass term without the corresponding improvement term would fail this identity.

## 127. Conformal covariance and the quartic interaction

In \(D\) spacetime dimensions, let
\[
\widetilde g_{\mu\nu}=\Omega^2g_{\mu\nu},
\qquad
\widetilde\phi=\Omega^{-(D-2)/2}\phi.
\]
The conformal wave operator satisfies
\[
\left(\widetilde\Box-\xi_D\widetilde{\mathcal R}\right)\widetilde\phi
=
\Omega^{-(D+2)/2}
\left(\Box-\xi_D\mathcal R\right)\phi,
\]
where
\[
\xi_D=\frac{D-2}{4(D-1)}.
\]
A potential
\[
V(\phi)=c\,\phi^{2D/(D-2)}
\]
has the corresponding classical conformal scaling when defined in a suitable real domain.

In four dimensions, the conformal interaction is quartic:
\[
V=\frac{\lambda}{4}\phi^4,
\qquad \xi=\frac16.
\]
Thus classical conformal symmetry does not require \(\lambda=0\). The mass term and a generic external \(U\) break the symmetry unless their transformation properties are supplied as spurions.

For the improved stress tensor,
\[
T_{\mu\nu}^{\mathrm{imp}}
=
T_{\mu\nu}^{\mathrm{min}}
+\xi\left[
G_{\mu\nu}\phi^2
+g_{\mu\nu}\Box\phi^2
-\nabla_\mu\nabla_\nu\phi^2
\right],
\]
the trace is
\[
T^{\mathrm{imp}}
=
-(\nabla\phi)^2-4V
+\xi\left[-\mathcal R\phi^2+3\Box\phi^2\right].
\]
At \(\xi=1/6\), use
\[
\Box\phi^2=2\phi\Box\phi+2(\nabla\phi)^2
\]
and
\[
\Box\phi=\frac16\mathcal R\phi+\lambda\phi^3.
\]
All terms cancel:
\[
T^{\mathrm{imp}}=0
\]
classically on shell. Quantum anomalies and running couplings alter this result.

## 128. Energy estimate for a bounded domain

For a static background with finite volume, bounded negative mass part, and \(\lambda>0\), write the energy as
\[
E=
\frac12\int Np^2dV_h
+\frac12\int N|D\phi|^2dV_h
+\frac12\int Nb\phi^2dV_h
+\frac{\lambda}{4}\int N\phi^4dV_h.
\]
Suppose \(|b_-|\le B\). For every real \(\phi\),
\[
\frac B2\phi^2
\le
\frac{\lambda}{8}\phi^4+\frac{B^2}{2\lambda}.
\]
Therefore
\[
E+\frac{B^2}{2\lambda}\int N\,dV_h
\ge
\frac12\int Np^2dV_h
+\frac12\int N|D\phi|^2dV_h
+\frac{\lambda}{8}\int N\phi^4dV_h.
\]
The conserved energy controls the normal velocity, gradient, and quartic field norm. On a finite volume domain, the \(L^2\) norm is controlled by the \(L^4\) norm:
\[
\|\phi\|_{L^2}^2
\le
\operatorname{Vol}(\Omega)^{1/2}\|\phi\|_{L^4}^2.
\]
Lapse bounds convert the weighted norms to ordinary norms.

These estimates explain why the defocusing quartic term can provide global energy control even if the quadratic coefficient is locally negative. They do not extend unchanged to infinite volume, focusing quartic coupling, time dependent sources, or a lapse approaching zero.

For a production theorem, one combines this bound with an appropriate local well posedness and continuation criterion. The estimate is the explicit analytical input, rather than a substitute for the functional analytic theorem.

## 129. Local versus global lower bounds on an infinite domain

On an infinite domain, the pointwise quartic lower bound
\[
W(\phi,x)\ge-\frac{b_-^2(x)}{4\lambda}
\]
is integrable only if
\[
\int N b_-^2\,dV_h<\infty
\]
or a suitable vacuum reference is subtracted. If \(b\) is a negative constant throughout infinite space, the broken vacuum has an extensive negative energy relative to \(\phi=0\).

Choose a reference vacuum \(v\) minimizing the homogeneous potential and define
\[
E_{\mathrm{rel}}
=
\int N\left[
\frac12p^2+\frac12|D\phi|^2+W(\phi)-W(v)
\right]dV_h.
\]
Finite relative energy requires approach to a vacuum at infinity, with a rate and topology appropriate to the dimension.

For an inhomogeneous coefficient, a pointwise minimum \(v(x)\) generally has gradient energy and is not an exact equilibrium. Subtracting its local potential value is a convenient lower bound but does not make it a dynamically stationary reference. A more precise relative energy can be defined around a true static solution.

In gravitational theory, subtracting a constant potential changes the cosmological term unless that change is accompanied by a corresponding redefinition of the gravitational vacuum parameter. Vacuum subtraction is therefore a convention for a prescribed background energy but a physical parameter choice in a dynamical spacetime action.

## 130. No net work from a static ground state

Let \(H\) be a time independent Hamiltonian bounded below by \(E_0\), and let \(|0\rangle\) be a ground state. Any cyclic external operation represented by a unitary \(U\), with the Hamiltonian returned to \(H\), gives final energy
\[
E_{\mathrm f}=\langle0|U^\dagger H U|0\rangle.
\]
Because \(H-E_0I\) is positive,
\[
E_{\mathrm f}-E_0
=
\langle0|U^\dagger(H-E_0I)U|0\rangle\ge0.
\]
The extracted work in a cycle, defined as initial minus final system energy, cannot be positive for this isolated initial ground state.

A geometry change can alter the Hamiltonian and its ground energy. The agent changing the geometry then performs work, and returning the geometry to its initial configuration closes the accounting. A nonequilibrium state, thermal gradient, externally driven boundary, or metastable configuration can supply extractable energy, but those are additional resources.

This elementary inequality is sufficient to delimit energy claims based on static geometric vacuum modifications. It does not deny Casimir forces, particle creation in time dependent backgrounds, or energy exchange between coupled sectors. It identifies the resources and boundary conditions those effects require.

## 131. A complete dependency chain for one canonical surface model

A concrete surface calculation can be written as the following chain of definitions:
\[
(R_0,A,a,n,m,\delta_\theta,\delta_\zeta)
\longrightarrow X
\longrightarrow(\gamma,b,H,K_G)
\]
\[
\longrightarrow
\left[
S_\Sigma,\ \mathcal H_\Sigma,\ \text{boundary domain}
\right]
\longrightarrow
\left[
\varphi,\ T_{AB},\ \nu_j,\ u_j
\right].
\]
If the shape is dynamical, add
\[
E_{\mathrm{mem}},\quad
\text{inertia and transport law},\quad
\frac{\delta S_{\mathrm{total}}}{\delta X}=0.
\]
If the coefficient is prescribed by curvature,
\[
U_\Sigma=\alpha_HH^2+\alpha_KK_G,
\]
the same geometry used to assemble the Laplacian must be used to assemble \(U_\Sigma\). If the coefficient is instead fitted phenomenologically, its fitted relation to the geometry must be recorded separately.

Every arrow in this chain is either an exact geometric construction, an explicit constitutive choice, a variational derivative, or a solved mathematical problem. An unspecified arrow is an unresolved part of the theory.

The executed surface benchmarks complete this chain for a linear scalar on a prescribed periodic geometry. The nonlinear, mechanical, gravitational, and quantum extensions are derived as separate equations with their additional requirements stated.

## 132. Compact canonical equation collection

For the prescribed bulk scalar:
\[
S_\phi=\int\sqrt{-g}\left[-\frac12(\nabla\phi)^2-V-U\phi^2\right],
\]
\[
\boxed{\Box\phi-V'-2U\phi=0,}
\]
\[
\boxed{\nabla_\mu T^\mu{}_\nu=-\phi^2\nabla_\nu U.}
\]

For a static background:
\[
\boxed{
-\partial_i(N\sqrt h\,h^{ij}\partial_ju)
+N\sqrt h\,M^2u
=\nu\frac{\sqrt h}{N}u.
}
\]

For the scalar and fermion, using \(\{\Gamma^\mu,\Gamma^\nu\}=-2g^{\mu\nu}\):
\[
\boxed{\Box\phi-V'-2U\phi-g_Y\bar\psi\psi=0,}
\]
\[
\boxed{(i\Gamma^\mu D_\mu-M-g_Y\phi)\psi=0,}
\]
\[
\boxed{\nabla_\mu(\bar\psi\Gamma^\mu\psi)=0.}
\]

For canonical scalar tensor gravity:
\[
\boxed{
FG_{\mu\nu}
=
T_{\mu\nu}^{\phi,\mathrm{min}}+T_{\mu\nu}^m
+\nabla_\mu\nabla_\nu F-g_{\mu\nu}\Box F,
}
\]
\[
\boxed{\Box\phi+\frac12F'\mathcal R-V'=0}
\]
when matter is scalar independent, with
\[
F=M_{\mathrm{Pl}}^2-\xi\phi^2.
\]

For the unit lapse prescribed surface:
\[
\boxed{
\varphi_{tt}-\Delta_\gamma\varphi
+V_\Sigma'(\varphi)+2U_\Sigma\varphi=0.
}
\]
For a static elastic surface with scalar:
\[
\boxed{
\frac{\delta(E_{\mathrm{mem}}+E_\varphi)}{\delta X_\perp}=0,
\qquad
-\Delta_\gamma\varphi+V_\Sigma'(\varphi)+2U_\Sigma\varphi=0.
}
\]

For every model, the action, boundary domain, initial data, and coefficient regularity remain part of the equation set. The compact formulas do not replace those specifications.

---

# Part XVI. Provenance and reusable computational record

## 133. Source document and revision scope

The source supplied for this revision was *Geometry_Coupled_Phase_Field_Field_Equations_Max_Rigor(2).md*. It contained the cylindrical scalar architecture, a phenomenological corrugation potential, optional Yukawa and gravitational sectors, and a surface interpretation. This revision reorganizes those ingredients into explicit model classes and develops their mathematical consequences.

The expansion adds full lapse weighted operator theory, exact surface curvature, explicit shape forces, consistent Clifford and current conventions, constrained gravitational closure, finite and infinite volume distinctions, rigorous spectral counterexamples, dimensional reduction, perturbative and nonperturbative benchmarks, numerical convergence records, and an inference framework.

The original diagram mentioned inside the source document was not separately available as an image in this task. All geometry used here is taken from the explicit radius and metric formulas in the supplied Markdown. No additional feature has been inferred from an unseen drawing.

The calculations are newly executed dimensionless verification examples. Their inputs are specified in the document and source code. They are not observations, historical experimental results, or numerical data supplied by the user.

## 134. Primary references and their role

The references below identify established frameworks used by the monograph. The detailed calculations specialized to the stated radius, lapse, normalization, and benchmark parameters are presented explicitly in the text.

1. Christian Bär, Nicolas Ginoux, and Frank Pfäffle, [Wave Equations on Lorentzian Manifolds and Quantization](https://arxiv.org/abs/0806.1036). Linear hyperbolic equations, Green operators, and quantization on globally hyperbolic backgrounds.

2. Eric Gourgoulhon, [3+1 Formalism and Bases of Numerical Relativity](https://arxiv.org/abs/gr-qc/0703035). Hypersurface geometry, gravitational constraints, and evolution formulations.

3. R. C. T. da Costa, [Quantum mechanics of a constrained particle](https://link.aps.org/doi/10.1103/PhysRevA.23.1982), Physical Review A 23, 1982 (1981). Thin confinement and the nonrelativistic extrinsic curvature potential.

4. Riccardo Capovilla and Jemal Guven, [Stresses in lipid membranes](https://arxiv.org/abs/cond-mat/0203148). Membrane stresses, shape equations, and geometric conservation structure.

5. Stefan Hollands and Robert M. Wald, [Quantum fields in curved spacetime](https://arxiv.org/abs/1401.2026). States, locality, covariance, and renormalized quantum fields on classical geometry.

6. D. V. Vassilevich, [Heat kernel expansion: user's manual](https://arxiv.org/abs/hep-th/0306138). Local heat coefficients and boundary contributions to quantum effective actions.

7. John F. Donoghue, [General relativity as an effective field theory: The leading quantum corrections](https://arxiv.org/abs/gr-qc/9405057). The low energy effective theory interpretation of gravitational quantum corrections.

8. Laur Järv, Piret Kuusk, and Margus Saal, [Scalar tensor cosmology at the general relativity limit: Jordan vs Einstein frame](https://arxiv.org/abs/0705.4644). Scalar tensor frame transformations and their potentially singular limits.

9. Stefan Hollands and Robert M. Wald, [On the Renormalization Group in Curved Spacetime](https://arxiv.org/abs/gr-qc/0209029). Renormalization flow for interacting fields under geometric scaling.

These references establish context and attribution. None is cited as experimental confirmation of the particular geometry coupled model defined here. A comprehensive priority or novelty review would require a separate systematic literature investigation targeted to a specific theorem or physical realization.

## 135. Exact provenance record

The supplied source file has SHA-256:

e4ee0f23124c106ffd9d0fb429b99954729383d4fc1815da831fc90f386ec8a3

The executable verification source embedded below has SHA-256:

2423e87af48e21258b1f42b7995e553fb2ae91c582b7add00977b51e96a0aefe

The complete JSON execution receipt embedded below has SHA-256:

c18e5355b6f1ccec623f6084409bf8f5f96804d953ee2ea8b9d894deabd7a503

These hashes identify the precise input, executable, and output bytes used for this revision. The Markdown document does not include a self hash, because inserting one would change its own bytes.

The computation ran with the dependency versions recorded in the receipt. Its implementation uses binary64 arithmetic. Exact rational benchmark values are retained in the analytical text. Arithmetic residuals and observed refinement changes are not interval certified bounds.

## 136. Complete executable verification source

Save the following block as verification.py. Run it with Python in an environment containing NumPy and SciPy. Setting OPENBLAS_NUM_THREADS=1 before execution limits BLAS thread variation. The program writes its complete JSON receipt to standard output. No notebook, network connection, hidden dataset, or GPU is required.

```python
"""Deterministic benchmarks for the geometry coupled scalar monograph.
All inputs below are dimensionless. No fitted or experimental data are used.
Run: OPENBLAS_NUM_THREADS=1 python verification.py > verification.json
"""
import json
import platform
from decimal import Decimal
import numpy as np
import scipy
from scipy.linalg import eigh
from scipy.special import jn_zeros, jv, ellipk, ellipj


def number(x):
    x = float(x)
    return {"float64_exact_decimal": str(Decimal.from_float(x)),
            "float64_hex": x.hex()}


def geometry(q, amplitude=0.1):
    theta, zeta = np.meshgrid(2*np.pi*np.arange(q)/q,
                              2*np.pi*np.arange(q)/q, indexing="ij")
    a, n, m = 1.5, 2, 1
    f = np.sin(n*theta)*np.cos(m*zeta)
    R = 1 + amplitude*f
    Rt = amplitude*n*np.cos(n*theta)*np.cos(m*zeta)
    Rz = -amplitude*m*np.sin(n*theta)*np.sin(m*zeta)
    Rtt = -amplitude*n*n*f
    Rzz = -amplitude*m*m*f
    Rtz = -amplitude*n*m*np.cos(n*theta)*np.sin(m*zeta)
    E, B, G = R*R+Rt*Rt, Rt*Rz, a*a+Rz*Rz
    determinant = E*G-B*B
    root = np.sqrt(determinant)
    # b_ab = -n dot X_ab: outward cylinder has H = +1/(2R).
    btt = a*(R*R + 2*Rt*Rt - R*Rtt)/root
    btz = a*(Rt*Rz-R*Rtz)/root
    bzz = -a*R*Rzz/root
    H = (G*btt - 2*B*btz + E*bzz)/(2*determinant)
    KG = (btt*bzz-btz*btz)/determinant
    invtt, invtz, invzz = G/determinant, -B/determinant, E/determinant
    return theta,zeta,root,invtt,invtz,invzz,H,KG,R


def fourier_matrix(values, modes):
    q = values.shape[0]
    coeff = np.fft.fft2(values)/(q*q)
    diff = modes[:,None,:]-modes[None,:,:]
    return coeff[diff[:,:,0] % q, diff[:,:,1] % q]


def surface_spectrum(cutoff, amplitude=0.1, potential=0.0, q=128):
    th,ze,s,itt,itz,izz,H,KG,R = geometry(q,amplitude)
    modes = np.array([(l,p) for l in range(-cutoff,cutoff+1)
                      for p in range(-cutoff,cutoff+1)])
    l,p = modes[:,0],modes[:,1]
    mass = fourier_matrix(s,modes)
    ctt = fourier_matrix(s*itt,modes)
    ctz = fourier_matrix(s*itz,modes)
    czz = fourier_matrix(s*izz,modes)
    stiffness = (l[:,None]*l[None,:]*ctt
       +(l[:,None]*p[None,:]+p[:,None]*l[None,:])*ctz
       +p[:,None]*p[None,:]*czz)
    potential_values = 0.25+2*potential*np.sin(2*th)*np.cos(ze)
    stiffness += fourier_matrix(s*potential_values,modes)
    hermiticity = np.max(np.abs(stiffness-stiffness.conj().T))
    vals,vec = eigh(stiffness,mass,subset_by_index=[0,8])
    res = stiffness@vec-mass@vec*vals[None,:]
    scaled = np.linalg.norm(res,axis=0)/(np.linalg.norm(stiffness,2)*np.linalg.norm(vec,axis=0)
                +np.abs(vals)*np.linalg.norm(mass,2)*np.linalg.norm(vec,axis=0))
    return {"cutoff":cutoff,"quadrature_each_axis":q,"dimension":len(modes),
            "omega_squared":[number(v) for v in vals],
            "max_scaled_residual":number(np.max(scaled)),
            "hermiticity_max":number(hermiticity)}


def lapse_spectrum(cutoff):
    q=2048
    x=2*np.pi*np.arange(q)/q
    N=1+0.2*np.cos(x)
    modes=np.arange(-cutoff,cutoff+1)
    diff=(modes[:,None]-modes[None,:]) % q
    C=(np.fft.fft(N)/q)[diff]
    W=(np.fft.fft(1/N)/q)[diff]
    K=(modes[:,None]*modes[None,:]+0.25)*C
    vals=eigh(K,W,subset_by_index=[0,5],eigvals_only=True)
    return {"cutoff":cutoff,"omega_squared":[number(v) for v in vals]}


def duffing():
    w2,g,A,T=1.25,0.75,0.5,20.0
    Om=np.sqrt(w2+g*A*A)
    parameter=g*A*A/(2*(w2+g*A*A))
    period=4*ellipk(parameter)/Om
    q_exact=A*ellipj(Om*T,parameter)[1]
    p_exact=-A*Om*ellipj(Om*T,parameter)[0]*ellipj(Om*T,parameter)[2]
    output=[]
    for steps in [1000,2000,4000]:
        h=T/steps; q=A; p=0.0
        e0=0.5*w2*q*q+g*q**4/4
        worst=0.0
        for _ in range(steps):
            p-=h*(w2*q+g*q**3)/2
            q+=h*p
            p-=h*(w2*q+g*q**3)/2
            energy=0.5*p*p+0.5*w2*q*q+g*q**4/4
            worst=max(worst,abs(energy-e0))
        output.append({"steps":steps,"dt":number(h),
           "q_error":number(abs(q-q_exact)),"p_error":number(abs(p-p_exact)),
           "max_energy_error":number(worst)})
    return {"omega_squared_exact":"5/4","g_exact":"3/4","amplitude_exact":"1/2",
            "elliptic_parameter_exact":"3/46","period":number(period),"runs":output}


def clifford_checks():
    I=np.eye(2,dtype=complex); O=np.zeros((2,2),dtype=complex)
    pauli=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
    gamma=[np.block([[I,O],[O,-I]])]+[np.block([[O,s],[-s,O]]) for s in pauli]
    metric=[-1,1,1,1]; errors=[]
    for a in range(4):
        for b in range(4):
            errors.append(np.max(np.abs(gamma[a]@gamma[b]+gamma[b]@gamma[a]
                      +(2*metric[a]*np.eye(4) if a==b else 0))))
    return {"anticommutator_minus_2g_max_error":number(max(errors)),
            "gamma0_squared_equals_identity":bool(np.array_equal(gamma[0]@gamma[0],np.eye(4)))}


def main():
    result={"environment":{"python":platform.python_version(),"numpy":np.__version__,
              "scipy":scipy.__version__,"arithmetic":"IEEE 754 binary64"},
            "clifford":clifford_checks()}
    result["bessel"]=[]
    for ell in [0,1,2]:
        roots=jn_zeros(ell,3)
        result["bessel"].append({"ell":ell,"roots":[number(v) for v in roots],
          "max_absolute_J_residual":number(np.max(np.abs(jv(ell,roots))))})
    result["geometry"]=[]
    for Q in [32,64,128,256]:
        th,ze,s,itt,itz,izz,H,KG,R=geometry(Q)
        cell=(2*np.pi)**2
        result["geometry"].append({"Q":Q,"area":number(np.mean(s)*cell),
          "integral_Gaussian_curvature":number(np.mean(KG*s)*cell),
          "integral_H_squared":number(np.mean(H*H*s)*cell),
          "minimum_radius_sampled":number(np.min(R)),
          "minimum_determinant_sampled":number(np.min(s*s)),
          "minimum_H_squared_minus_K_sampled":number(np.min(H*H-KG))})
    result["corrugated_surface"]=[surface_spectrum(k) for k in [3,5,7,9]]
    result["potential_on_cylinder"]=[surface_spectrum(k,amplitude=0,potential=0.1) for k in [3,5,7,9]]
    result["lapse_circle"]=[lapse_spectrum(k) for k in [8,16,24]]
    result["duffing"]=duffing()
    result["surface_quadrature_check"]=[surface_spectrum(7,q=q) for q in [64,96,128]]
    # Actual tests: independent analytic limits and convergence, not physical validation.
    flat=surface_spectrum(3,amplitude=0,potential=0)
    exact=sorted(l*l+p*p/2.25+0.25 for l in range(-3,4) for p in range(-3,4))[:9]
    flat_error=max(abs(float(a["float64_exact_decimal"])-b) for a,b in zip(flat["omega_squared"],exact))
    constant_error=abs(float(result["corrugated_surface"][-1]["omega_squared"][0]["float64_exact_decimal"])-0.25)
    errs=[float(r["q_error"]["float64_exact_decimal"]) for r in result["duffing"]["runs"]]
    result["checks"]={"flat_cylinder_max_error":number(flat_error),
      "corrugated_constant_mode_error":number(constant_error),
      "duffing_q_error_ratios":[number(errs[i]/errs[i+1]) for i in range(2)]}
    lapse_error=abs(float(result["lapse_circle"][-1]["omega_squared"][0]["float64_exact_decimal"])-0.24)
    result["checks"]["lapse_exact_ground_error"]=number(lapse_error)
    assert lapse_error < 1e-10
    assert flat_error < 1e-11
    assert constant_error < 1e-10
    assert all(3.8 < errs[i]/errs[i+1] < 4.2 for i in range(2))
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__ == "__main__":
    main()
```

## 137. Complete execution receipt

Every reported floating point quantity includes the exact decimal expansion of the stored binary64 value and its hexadecimal representation. The receipt is intentionally unabridged. Duplicate eigenvalues appear separately because multiplicity is part of the spectrum.

```json
{
  "environment": {
    "python": "3.12.14",
    "numpy": "2.3.5",
    "scipy": "1.17.0",
    "arithmetic": "IEEE 754 binary64"
  },
  "clifford": {
    "anticommutator_minus_2g_max_error": {
      "float64_exact_decimal": "0",
      "float64_hex": "0x0.0p+0"
    },
    "gamma0_squared_equals_identity": true
  },
  "bessel": [
    {
      "ell": 0,
      "roots": [
        {
          "float64_exact_decimal": "2.404825557695772442201587182353250682353973388671875",
          "float64_hex": "0x1.33d152e971b3fp+1"
        },
        {
          "float64_exact_decimal": "5.52007811028631056871063265134580433368682861328125",
          "float64_hex": "0x1.6148f5b2c2e45p+2"
        },
        {
          "float64_exact_decimal": "8.653727912911012509766806033439934253692626953125",
          "float64_hex": "0x1.14eb56cccdecap+3"
        }
      ],
      "max_absolute_J_residual": {
        "float64_exact_decimal": "1.040353654866447615182703286451465231599946379835615328790510147882741875946521759033203125E-16",
        "float64_hex": "0x1.dfc747df59b1dp-54"
      }
    },
    {
      "ell": 1,
      "roots": [
        {
          "float64_exact_decimal": "3.831705970207512468306276787188835442066192626953125",
          "float64_hex": "0x1.ea75575af6f09p+1"
        },
        {
          "float64_exact_decimal": "7.0155866698156188476787065155804157257080078125",
          "float64_hex": "0x1.c0ff5f3b47250p+2"
        },
        {
          "float64_exact_decimal": "10.1734681350627216289694842998869717121124267578125",
          "float64_hex": "0x1.458d0d0bdfc29p+3"
        }
      ],
      "max_absolute_J_residual": {
        "float64_exact_decimal": "2.43500876579685830365477449589424523738336969373718954301466510514728724956512451171875E-16",
        "float64_hex": "0x1.18bcc60cbc52cp-52"
      }
    },
    {
      "ell": 2,
      "roots": [
        {
          "float64_exact_decimal": "5.13562230184068280181008958606980741024017333984375",
          "float64_hex": "0x1.48ae0929c0e4fp+2"
        },
        {
          "float64_exact_decimal": "8.41724414039986612579014035873115062713623046875",
          "float64_hex": "0x1.0d5a10622ee1cp+3"
        },
        {
          "float64_exact_decimal": "11.6198411721490604264772628084756433963775634765625",
          "float64_hex": "0x1.73d5bd2763065p+3"
        }
      ],
      "max_absolute_J_residual": {
        "float64_exact_decimal": "2.58902878456593245018838810614093019051232670395268353757955992477945983409881591796875E-16",
        "float64_hex": "0x1.2a7ea4689e9ccp-52"
      }
    }
  ],
  "geometry": [
    {
      "Q": 32,
      "area": {
        "float64_exact_decimal": "59.545452879848568272791453637182712554931640625",
        "float64_hex": "0x1.dc5d166643ab4p+5"
      },
      "integral_Gaussian_curvature": {
        "float64_exact_decimal": "5.5277613874308684797925131406529344522092495051168725694878958165645599365234375E-13",
        "float64_hex": "0x1.372f6fec42caep-41"
      },
      "integral_H_squared": {
        "float64_exact_decimal": "15.1973861857146115283967446885071694850921630859375",
        "float64_hex": "0x1.e650fcd58a723p+3"
      },
      "minimum_radius_sampled": {
        "float64_exact_decimal": "0.90000000000000002220446049250313080847263336181640625",
        "float64_hex": "0x1.ccccccccccccdp-1"
      },
      "minimum_determinant_sampled": {
        "float64_exact_decimal": "1.822500000000000230926389122032560408115386962890625",
        "float64_hex": "0x1.d28f5c28f5c2ap+0"
      },
      "minimum_H_squared_minus_K_sampled": {
        "float64_exact_decimal": "0.1094711172077426908355590740029583685100078582763671875",
        "float64_hex": "0x1.c064c94438adep-4"
      }
    },
    {
      "Q": 64,
      "area": {
        "float64_exact_decimal": "59.545452879848568272791453637182712554931640625",
        "float64_hex": "0x1.dc5d166643ab4p+5"
      },
      "integral_Gaussian_curvature": {
        "float64_exact_decimal": "6.4203879199401465259081620305690930555048666350526076485039084218442440032958984375E-17",
        "float64_hex": "0x1.28168fd226180p-54"
      },
      "integral_H_squared": {
        "float64_exact_decimal": "15.1973861857030971833637522649951279163360595703125",
        "float64_hex": "0x1.e650fcd588dd1p+3"
      },
      "minimum_radius_sampled": {
        "float64_exact_decimal": "0.90000000000000002220446049250313080847263336181640625",
        "float64_hex": "0x1.ccccccccccccdp-1"
      },
      "minimum_determinant_sampled": {
        "float64_exact_decimal": "1.822500000000000230926389122032560408115386962890625",
        "float64_hex": "0x1.d28f5c28f5c2ap+0"
      },
      "minimum_H_squared_minus_K_sampled": {
        "float64_exact_decimal": "0.1094711172077426908355590740029583685100078582763671875",
        "float64_hex": "0x1.c064c94438adep-4"
      }
    },
    {
      "Q": 128,
      "area": {
        "float64_exact_decimal": "59.54545287984857537821881123818457126617431640625",
        "float64_hex": "0x1.dc5d166643ab5p+5"
      },
      "integral_Gaussian_curvature": {
        "float64_exact_decimal": "2.140129306646715714068581411494855344472602754076449860232145283589488826692104339599609375E-17",
        "float64_hex": "0x1.8ac8bfc2dd756p-56"
      },
      "integral_H_squared": {
        "float64_exact_decimal": "15.1973861857030971833637522649951279163360595703125",
        "float64_hex": "0x1.e650fcd588dd1p+3"
      },
      "minimum_radius_sampled": {
        "float64_exact_decimal": "0.90000000000000002220446049250313080847263336181640625",
        "float64_hex": "0x1.ccccccccccccdp-1"
      },
      "minimum_determinant_sampled": {
        "float64_exact_decimal": "1.822500000000000230926389122032560408115386962890625",
        "float64_hex": "0x1.d28f5c28f5c2ap+0"
      },
      "minimum_H_squared_minus_K_sampled": {
        "float64_exact_decimal": "0.1094711172077426908355590740029583685100078582763671875",
        "float64_hex": "0x1.c064c94438adep-4"
      }
    },
    {
      "Q": 256,
      "area": {
        "float64_exact_decimal": "59.54545287984857537821881123818457126617431640625",
        "float64_hex": "0x1.dc5d166643ab5p+5"
      },
      "integral_Gaussian_curvature": {
        "float64_exact_decimal": "1.712103445317372447995348688412789679995493877825811501747210741086746565997600555419921875E-17",
        "float64_hex": "0x1.3bd3cc9be45dep-56"
      },
      "integral_H_squared": {
        "float64_exact_decimal": "15.1973861857030971833637522649951279163360595703125",
        "float64_hex": "0x1.e650fcd588dd1p+3"
      },
      "minimum_radius_sampled": {
        "float64_exact_decimal": "0.90000000000000002220446049250313080847263336181640625",
        "float64_hex": "0x1.ccccccccccccdp-1"
      },
      "minimum_determinant_sampled": {
        "float64_exact_decimal": "1.822500000000000230926389122032560408115386962890625",
        "float64_hex": "0x1.d28f5c28f5c2ap+0"
      },
      "minimum_H_squared_minus_K_sampled": {
        "float64_exact_decimal": "0.1094711172077426908355590740029583685100078582763671875",
        "float64_hex": "0x1.c064c94438adep-4"
      }
    }
  ],
  "corrugated_surface": [
    {
      "cutoff": 3,
      "quadrature_each_axis": 128,
      "dimension": 49,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.25000000000000011102230246251565404236316680908203125",
          "float64_hex": "0x1.0000000000002p-2"
        },
        {
          "float64_exact_decimal": "0.6915788054956963915032019940554164350032806396484375",
          "float64_hex": "0x1.62169e006be8ep-1"
        },
        {
          "float64_exact_decimal": "0.6961106902018820985489355734898708760738372802734375",
          "float64_hex": "0x1.64689ed1a04aep-1"
        },
        {
          "float64_exact_decimal": "1.2402328261066752901342624682001769542694091796875",
          "float64_hex": "0x1.3d7fe6038dc78p+0"
        },
        {
          "float64_exact_decimal": "1.240232826106678398758731418638490140438079833984375",
          "float64_hex": "0x1.3d7fe6038dc86p+0"
        },
        {
          "float64_exact_decimal": "1.67710674469077591908217073068954050540924072265625",
          "float64_hex": "0x1.ad56de1c59104p+0"
        },
        {
          "float64_exact_decimal": "1.677106744690778583617429831065237522125244140625",
          "float64_hex": "0x1.ad56de1c59110p+0"
        },
        {
          "float64_exact_decimal": "1.691506153494959363570160348899662494659423828125",
          "float64_hex": "0x1.b1068c1a3e5d0p+0"
        },
        {
          "float64_exact_decimal": "1.691506153494962472194629299337975680828094482421875",
          "float64_hex": "0x1.b1068c1a3e5dep+0"
        }
      ],
      "max_scaled_residual": {
        "float64_exact_decimal": "4.8857379755354558629750410255440720903004152807225235477517344406805932521820068359375E-16",
        "float64_hex": "0x1.19a4c435327ccp-51"
      },
      "hermiticity_max": {
        "float64_exact_decimal": "1.9947301009923321357462866313814632706541599992447998113132001662961556576192378997802734375E-17",
        "float64_hex": "0x1.6ff67738f7277p-56"
      }
    },
    {
      "cutoff": 5,
      "quadrature_each_axis": 128,
      "dimension": 121,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.24999999999999611421941381195210851728916168212890625",
          "float64_hex": "0x1.fffffffffff74p-3"
        },
        {
          "float64_exact_decimal": "0.691577881656254334075129008851945400238037109375",
          "float64_hex": "0x1.62167f00b37e0p-1"
        },
        {
          "float64_exact_decimal": "0.6961102077555982869938588919467292726039886474609375",
          "float64_hex": "0x1.64688ea171b1ep-1"
        },
        {
          "float64_exact_decimal": "1.2402226406067102804087198819615878164768218994140625",
          "float64_hex": "0x1.3d7f3b212a221p+0"
        },
        {
          "float64_exact_decimal": "1.2402226406067204944605464334017597138881683349609375",
          "float64_hex": "0x1.3d7f3b212a24fp+0"
        },
        {
          "float64_exact_decimal": "1.6770936553525148671184297199943102896213531494140625",
          "float64_hex": "0x1.ad56028211721p+0"
        },
        {
          "float64_exact_decimal": "1.6770936553525250811702562714344821870326995849609375",
          "float64_hex": "0x1.ad5602821174fp+0"
        },
        {
          "float64_exact_decimal": "1.6914986552664494912079362620715983211994171142578125",
          "float64_hex": "0x1.b1060e4d98eddp+0"
        },
        {
          "float64_exact_decimal": "1.6914986552664494912079362620715983211994171142578125",
          "float64_hex": "0x1.b1060e4d98eddp+0"
        }
      ],
      "max_scaled_residual": {
        "float64_exact_decimal": "4.617455707296191945545762950919868719371435519978341677216349125956185162067413330078125E-16",
        "float64_hex": "0x1.0a2d9e7461c01p-51"
      },
      "hermiticity_max": {
        "float64_exact_decimal": "3.583561317026776129509378522892929870652852303238196374213231365501997061073780059814453125E-17",
        "float64_hex": "0x1.4a867302fa249p-55"
      }
    },
    {
      "cutoff": 7,
      "quadrature_each_axis": 128,
      "dimension": 225,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.2500000000000295319324550291639752686023712158203125",
          "float64_hex": "0x1.0000000000214p-2"
        },
        {
          "float64_exact_decimal": "0.69157788090181349094365259588812477886676788330078125",
          "float64_hex": "0x1.62167efa38759p-1"
        },
        {
          "float64_exact_decimal": "0.69611020724719996355389639575150795280933380126953125",
          "float64_hex": "0x1.64688e9d13b71p-1"
        },
        {
          "float64_exact_decimal": "1.240222636934619426796189145534299314022064208984375",
          "float64_hex": "0x1.3d7f3b1164a06p+0"
        },
        {
          "float64_exact_decimal": "1.240222636934619426796189145534299314022064208984375",
          "float64_hex": "0x1.3d7f3b1164a06p+0"
        },
        {
          "float64_exact_decimal": "1.677093650590919526877087264438159763813018798828125",
          "float64_hex": "0x1.ad56026d9e042p+0"
        },
        {
          "float64_exact_decimal": "1.677093650590919526877087264438159763813018798828125",
          "float64_hex": "0x1.ad56026d9e042p+0"
        },
        {
          "float64_exact_decimal": "1.69149865316625636069147731177508831024169921875",
          "float64_hex": "0x1.b1060e4493be0p+0"
        },
        {
          "float64_exact_decimal": "1.69149865316625636069147731177508831024169921875",
          "float64_hex": "0x1.b1060e4493be0p+0"
        }
      ],
      "max_scaled_residual": {
        "float64_exact_decimal": "5.291633310098403650577077671853971571819521212652615016480694976053200662136077880859375E-16",
        "float64_hex": "0x1.310ab96d3568bp-51"
      },
      "hermiticity_max": {
        "float64_exact_decimal": "1.8908140758317276149527186887368681329077020592498159512473421273170970380306243896484375E-16",
        "float64_hex": "0x1.b3fdf6745d2eep-53"
      }
    },
    {
      "cutoff": 9,
      "quadrature_each_axis": 128,
      "dimension": 361,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.25000000000002120525977034048992209136486053466796875",
          "float64_hex": "0x1.000000000017ep-2"
        },
        {
          "float64_exact_decimal": "0.69157788090143335058002094228868372738361358642578125",
          "float64_hex": "0x1.62167efa379f9p-1"
        },
        {
          "float64_exact_decimal": "0.69611020724447414398383671141345985233783721923828125",
          "float64_hex": "0x1.64688e9d0db89p-1"
        },
        {
          "float64_exact_decimal": "1.240222636882539308800232902285642921924591064453125",
          "float64_hex": "0x1.3d7f3b112b5d2p+0"
        },
        {
          "float64_exact_decimal": "1.240222636882613027609068012679927051067352294921875",
          "float64_hex": "0x1.3d7f3b112b71ep+0"
        },
        {
          "float64_exact_decimal": "1.677093650491118470569062992581166326999664306640625",
          "float64_hex": "0x1.ad56026d3048ap+0"
        },
        {
          "float64_exact_decimal": "1.67709365049113667822666684514842927455902099609375",
          "float64_hex": "0x1.ad56026d304dcp+0"
        },
        {
          "float64_exact_decimal": "1.691498653156310094658465459360741078853607177734375",
          "float64_hex": "0x1.b1060e4488ce6p+0"
        },
        {
          "float64_exact_decimal": "1.6914986531563283023160693119280040264129638671875",
          "float64_hex": "0x1.b1060e4488d38p+0"
        }
      ],
      "max_scaled_residual": {
        "float64_exact_decimal": "1.18478085407164929734618878569465855737314415215000185099825102952308952808380126953125E-15",
        "float64_hex": "0x1.557d65944a062p-50"
      },
      "hermiticity_max": {
        "float64_exact_decimal": "1.8908140758317276149527186887368681329077020592498159512473421273170970380306243896484375E-16",
        "float64_hex": "0x1.b3fdf6745d2eep-53"
      }
    }
  ],
  "potential_on_cylinder": [
    {
      "cutoff": 3,
      "quadrature_each_axis": 128,
      "dimension": 49,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.247749716642788830878174621830112300813198089599609375",
          "float64_hex": "0x1.fb64341497a4ep-3"
        },
        {
          "float64_exact_decimal": "0.69069781644021521760379300758359022438526153564453125",
          "float64_hex": "0x1.61a324ea0f051p-1"
        },
        {
          "float64_exact_decimal": "0.6935068621193927196344475305522792041301727294921875",
          "float64_hex": "0x1.631354d8b5706p-1"
        },
        {
          "float64_exact_decimal": "1.2383864197075329371955376700498163700103759765625",
          "float64_hex": "0x1.3d06e47474528p+0"
        },
        {
          "float64_exact_decimal": "1.2383864197075329371955376700498163700103759765625",
          "float64_hex": "0x1.3d06e47474528p+0"
        },
        {
          "float64_exact_decimal": "1.69230262578090684399967358331196010112762451171875",
          "float64_hex": "0x1.b13abeb0a9f6cp+0"
        },
        {
          "float64_exact_decimal": "1.6923026257809092864903277586563490331172943115234375",
          "float64_hex": "0x1.b13abeb0a9f77p+0"
        },
        {
          "float64_exact_decimal": "1.7026609352824806364878895692527294158935546875",
          "float64_hex": "0x1.b3e19649370c0p+0"
        },
        {
          "float64_exact_decimal": "1.702660935282485521469197919941507279872894287109375",
          "float64_hex": "0x1.b3e19649370d6p+0"
        }
      ],
      "max_scaled_residual": {
        "float64_exact_decimal": "4.267351663960705050554378113983782397766939789747475675341092937742359936237335205078125E-16",
        "float64_hex": "0x1.ebfdfd8cb3382p-52"
      },
      "hermiticity_max": {
        "float64_exact_decimal": "4.3178049498783581719085367314691604371986427722486696911818881972067174501717090606689453125E-18",
        "float64_hex": "0x1.3e99078d476e2p-58"
      }
    },
    {
      "cutoff": 5,
      "quadrature_each_axis": 128,
      "dimension": 121,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.24774948726337886473203298010048456490039825439453125",
          "float64_hex": "0x1.fb64154b2d044p-3"
        },
        {
          "float64_exact_decimal": "0.69069735578059410219253777540870942175388336181640625",
          "float64_hex": "0x1.61a3157505ccdp-1"
        },
        {
          "float64_exact_decimal": "0.69350681214280296416063720243982970714569091796875",
          "float64_hex": "0x1.6313532b69c18p-1"
        },
        {
          "float64_exact_decimal": "1.238386397900841817687478396692313253879547119140625",
          "float64_hex": "0x1.3d06e416cb9cap+0"
        },
        {
          "float64_exact_decimal": "1.238386397900841817687478396692313253879547119140625",
          "float64_hex": "0x1.3d06e416cb9cap+0"
        },
        {
          "float64_exact_decimal": "1.692302619891921100503395791747607290744781494140625",
          "float64_hex": "0x1.b13abe975ef4ap+0"
        },
        {
          "float64_exact_decimal": "1.692302619891928205930753392749466001987457275390625",
          "float64_hex": "0x1.b13abe975ef6ap+0"
        },
        {
          "float64_exact_decimal": "1.70266089689171717935778360697440803050994873046875",
          "float64_hex": "0x1.b3e195a453f4cp+0"
        },
        {
          "float64_exact_decimal": "1.70266089689171717935778360697440803050994873046875",
          "float64_hex": "0x1.b3e195a453f4cp+0"
        }
      ],
      "max_scaled_residual": {
        "float64_exact_decimal": "4.1040025414295491448736624254081641316870907444484817272467580551165156066417694091796875E-16",
        "float64_hex": "0x1.d928c679c1d6bp-52"
      },
      "hermiticity_max": {
        "float64_exact_decimal": "4.3178049498783581719085367314691604371986427722486696911818881972067174501717090606689453125E-18",
        "float64_hex": "0x1.3e99078d476e2p-58"
      }
    },
    {
      "cutoff": 7,
      "quadrature_each_axis": 128,
      "dimension": 225,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.247749487260288725476442550643696449697017669677734375",
          "float64_hex": "0x1.fb64154b11d5ep-3"
        },
        {
          "float64_exact_decimal": "0.6906973557740077040989490342326462268829345703125",
          "float64_hex": "0x1.61a31574f7510p-1"
        },
        {
          "float64_exact_decimal": "0.693506812142352213612639388884417712688446044921875",
          "float64_hex": "0x1.6313532b68c3cp-1"
        },
        {
          "float64_exact_decimal": "1.2383863979006901612223146003088913857936859130859375",
          "float64_hex": "0x1.3d06e416cb71fp+0"
        },
        {
          "float64_exact_decimal": "1.238386397900707702746103677782230079174041748046875",
          "float64_hex": "0x1.3d06e416cb76ep+0"
        },
        {
          "float64_exact_decimal": "1.6923026198918933449277801628340966999530792236328125",
          "float64_hex": "0x1.b13abe975eecdp+0"
        },
        {
          "float64_exact_decimal": "1.69230261989191088645156924030743539333343505859375",
          "float64_hex": "0x1.b13abe975ef1cp+0"
        },
        {
          "float64_exact_decimal": "1.7026608968914285213713810662738978862762451171875",
          "float64_hex": "0x1.b3e195a453a38p+0"
        },
        {
          "float64_exact_decimal": "1.702660896891445840850565218715928494930267333984375",
          "float64_hex": "0x1.b3e195a453a86p+0"
        }
      ],
      "max_scaled_residual": {
        "float64_exact_decimal": "5.96853331934107490874350955047958027966542061959476228594212443567812442779541015625E-16",
        "float64_hex": "0x1.5810015bfc3d0p-51"
      },
      "hermiticity_max": {
        "float64_exact_decimal": "4.3178049498783581719085367314691604371986427722486696911818881972067174501717090606689453125E-18",
        "float64_hex": "0x1.3e99078d476e2p-58"
      }
    },
    {
      "cutoff": 9,
      "quadrature_each_axis": 128,
      "dimension": 361,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.247749487260273404398702723483438603579998016357421875",
          "float64_hex": "0x1.fb64154b11b36p-3"
        },
        {
          "float64_exact_decimal": "0.69069735577400559467520224643521942198276519775390625",
          "float64_hex": "0x1.61a31574f74fdp-1"
        },
        {
          "float64_exact_decimal": "0.69350681214228415694122986678848974406719207763671875",
          "float64_hex": "0x1.6313532b689d7p-1"
        },
        {
          "float64_exact_decimal": "1.238386397900666846538797472021542489528656005859375",
          "float64_hex": "0x1.3d06e416cb6b6p+0"
        },
        {
          "float64_exact_decimal": "1.238386397900697044605067276279442012310028076171875",
          "float64_hex": "0x1.3d06e416cb73ep+0"
        },
        {
          "float64_exact_decimal": "1.69230261989189845195369343855418264865875244140625",
          "float64_hex": "0x1.b13abe975eee4p+0"
        },
        {
          "float64_exact_decimal": "1.69230261989189845195369343855418264865875244140625",
          "float64_hex": "0x1.b13abe975eee4p+0"
        },
        {
          "float64_exact_decimal": "1.702660896891451169921083419467322528362274169921875",
          "float64_hex": "0x1.b3e195a453a9ep+0"
        },
        {
          "float64_exact_decimal": "1.702660896891451169921083419467322528362274169921875",
          "float64_hex": "0x1.b3e195a453a9ep+0"
        }
      ],
      "max_scaled_residual": {
        "float64_exact_decimal": "1.275738677695655983694028057972657548191819550098546898198037524707615375518798828125E-15",
        "float64_hex": "0x1.6fb4e64a30708p-50"
      },
      "hermiticity_max": {
        "float64_exact_decimal": "4.3178049498783581719085367314691604371986427722486696911818881972067174501717090606689453125E-18",
        "float64_hex": "0x1.3e99078d476e2p-58"
      }
    }
  ],
  "lapse_circle": [
    {
      "cutoff": 8,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.24000000000000032418512319054570980370044708251953125",
          "float64_hex": "0x1.eb851eb851ec4p-3"
        },
        {
          "float64_exact_decimal": "1.19674769527484503583991681807674467563629150390625",
          "float64_hex": "0x1.325e0e94c4d24p+0"
        },
        {
          "float64_exact_decimal": "1.2163852121136553563474080874584615230560302734375",
          "float64_hex": "0x1.376505715dbd8p+0"
        },
        {
          "float64_exact_decimal": "4.08511486125284495329879064229317009449005126953125",
          "float64_hex": "0x1.0572859a5f02dp+2"
        },
        {
          "float64_exact_decimal": "4.08547219334599365225813016877509653568267822265625",
          "float64_hex": "0x1.0578605cc8dc1p+2"
        },
        {
          "float64_exact_decimal": "8.88509321549610575630140374414622783660888671875",
          "float64_hex": "0x1.1c52af01cef3cp+3"
        }
      ]
    },
    {
      "cutoff": 16,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.239999999999969571007341073709540069103240966796875",
          "float64_hex": "0x1.eb851eb851a70p-3"
        },
        {
          "float64_exact_decimal": "1.19674769527484681219675621832720935344696044921875",
          "float64_hex": "0x1.325e0e94c4d2cp+0"
        },
        {
          "float64_exact_decimal": "1.216385212113636260511384534765966236591339111328125",
          "float64_hex": "0x1.376505715db82p+0"
        },
        {
          "float64_exact_decimal": "4.0851148611835554902427247725427150726318359375",
          "float64_hex": "0x1.0572859a4bf70p+2"
        },
        {
          "float64_exact_decimal": "4.0854721932766633329947580932639539241790771484375",
          "float64_hex": "0x1.0578605cb5cd6p+2"
        },
        {
          "float64_exact_decimal": "8.8850931504608308131309968302957713603973388671875",
          "float64_hex": "0x1.1c52aedee4927p+3"
        }
      ]
    },
    {
      "cutoff": 24,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.240000000000036683989179664422408677637577056884765625",
          "float64_hex": "0x1.eb851eb8523e2p-3"
        },
        {
          "float64_exact_decimal": "1.1967476952747677643174029071815311908721923828125",
          "float64_hex": "0x1.325e0e94c4bc8p+0"
        },
        {
          "float64_exact_decimal": "1.21638521211359229567960937856696546077728271484375",
          "float64_hex": "0x1.376505715dabcp+0"
        },
        {
          "float64_exact_decimal": "4.0851148611835608193132429732941091060638427734375",
          "float64_hex": "0x1.0572859a4bf76p+2"
        },
        {
          "float64_exact_decimal": "4.0854721932767770198324797092936933040618896484375",
          "float64_hex": "0x1.0578605cb5d56p+2"
        },
        {
          "float64_exact_decimal": "8.88509315046086811662462423555552959442138671875",
          "float64_hex": "0x1.1c52aedee493cp+3"
        }
      ]
    }
  ],
  "duffing": {
    "omega_squared_exact": "5/4",
    "g_exact": "3/4",
    "amplitude_exact": "1/2",
    "elliptic_parameter_exact": "3/46",
    "period": {
      "float64_exact_decimal": "5.329266301866848465351722552441060543060302734375",
      "float64_hex": "0x1.5512b2f78c59cp+2"
    },
    "runs": [
      {
        "steps": 1000,
        "dt": {
          "float64_exact_decimal": "0.0200000000000000004163336342344337026588618755340576171875",
          "float64_hex": "0x1.47ae147ae147bp-6"
        },
        "q_error": {
          "float64_exact_decimal": "0.00026742056766544154700060431650854297913610935211181640625",
          "float64_hex": "0x1.1869297a794a0p-12"
        },
        "p_error": {
          "float64_exact_decimal": "0.0000441809950804117335110277053900063037872314453125",
          "float64_hex": "0x1.729df6e8a8000p-15"
        },
        "max_energy_error": {
          "float64_exact_decimal": "0.0000226074476152582359844700476969592273235321044921875",
          "float64_hex": "0x1.7b4a3f86fe000p-16"
        }
      },
      {
        "steps": 2000,
        "dt": {
          "float64_exact_decimal": "0.01000000000000000020816681711721685132943093776702880859375",
          "float64_hex": "0x1.47ae147ae147bp-7"
        },
        "q_error": {
          "float64_exact_decimal": "0.0000668526529534717306457736185620888136327266693115234375",
          "float64_hex": "0x1.18667d5147f00p-14"
        },
        "p_error": {
          "float64_exact_decimal": "0.00001103049525408295039596850983798503875732421875",
          "float64_hex": "0x1.721f3b9580000p-17"
        },
        "max_energy_error": {
          "float64_exact_decimal": "0.000005651857166333318360784687683917582035064697265625",
          "float64_hex": "0x1.7b4a2ab110000p-18"
        }
      },
      {
        "steps": 4000,
        "dt": {
          "float64_exact_decimal": "0.005000000000000000104083408558608425664715468883514404296875",
          "float64_hex": "0x1.47ae147ae147bp-8"
        },
        "q_error": {
          "float64_exact_decimal": "0.00001671300755205773480582820411655120551586151123046875",
          "float64_hex": "0x1.1865d2237b000p-16"
        },
        "p_error": {
          "float64_exact_decimal": "0.00000275670179672449222607610863633453845977783203125",
          "float64_hex": "0x1.71ff8d7040000p-19"
        },
        "max_energy_error": {
          "float64_exact_decimal": "0.000001412963962998947664573279325850307941436767578125",
          "float64_hex": "0x1.7b4a24e940000p-20"
        }
      }
    ]
  },
  "surface_quadrature_check": [
    {
      "cutoff": 7,
      "quadrature_each_axis": 64,
      "dimension": 225,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.2499999999999882316359389733406715095043182373046875",
          "float64_hex": "0x1.ffffffffffe58p-3"
        },
        {
          "float64_exact_decimal": "0.69157788090180272178031373186968266963958740234375",
          "float64_hex": "0x1.62167efa386f8p-1"
        },
        {
          "float64_exact_decimal": "0.696110207247190526658187081920914351940155029296875",
          "float64_hex": "0x1.64688e9d13b1cp-1"
        },
        {
          "float64_exact_decimal": "1.240222636934613209547251244657672941684722900390625",
          "float64_hex": "0x1.3d7f3b11649eap+0"
        },
        {
          "float64_exact_decimal": "1.240222636934627420401966446661390364170074462890625",
          "float64_hex": "0x1.3d7f3b1164a2ap+0"
        },
        {
          "float64_exact_decimal": "1.677093650590933737731802466441877186298370361328125",
          "float64_hex": "0x1.ad56026d9e082p+0"
        },
        {
          "float64_exact_decimal": "1.677093650590933737731802466441877186298370361328125",
          "float64_hex": "0x1.ad56026d9e082p+0"
        },
        {
          "float64_exact_decimal": "1.691498653166268351100143263465724885463714599609375",
          "float64_hex": "0x1.b1060e4493c16p+0"
        },
        {
          "float64_exact_decimal": "1.691498653166268351100143263465724885463714599609375",
          "float64_hex": "0x1.b1060e4493c16p+0"
        }
      ],
      "max_scaled_residual": {
        "float64_exact_decimal": "6.3088760531930833261648434491218777354023280849737442821378863300196826457977294921875E-16",
        "float64_hex": "0x1.6bae93dac349cp-51"
      },
      "hermiticity_max": {
        "float64_exact_decimal": "7.586088780763588561284530016690240793847919975601001851828186772763729095458984375E-17",
        "float64_hex": "0x1.5dd8ba7e0cf00p-54"
      }
    },
    {
      "cutoff": 7,
      "quadrature_each_axis": 96,
      "dimension": 225,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.249999999999984290344201554034953005611896514892578125",
          "float64_hex": "0x1.ffffffffffdcap-3"
        },
        {
          "float64_exact_decimal": "0.69157788090180949414076394532457925379276275634765625",
          "float64_hex": "0x1.62167efa38735p-1"
        },
        {
          "float64_exact_decimal": "0.69611020724717909136103344280854798853397369384765625",
          "float64_hex": "0x1.64688e9d13ab5p-1"
        },
        {
          "float64_exact_decimal": "1.240222636934608768655152744031511247158050537109375",
          "float64_hex": "0x1.3d7f3b11649d6p+0"
        },
        {
          "float64_exact_decimal": "1.240222636934621647242238395847380161285400390625",
          "float64_hex": "0x1.3d7f3b1164a10p+0"
        },
        {
          "float64_exact_decimal": "1.6770936505909190827878774143755435943603515625",
          "float64_hex": "0x1.ad56026d9e040p+0"
        },
        {
          "float64_exact_decimal": "1.6770936505909190827878774143755435943603515625",
          "float64_hex": "0x1.ad56026d9e040p+0"
        },
        {
          "float64_exact_decimal": "1.691498653166261245672785662463866174221038818359375",
          "float64_hex": "0x1.b1060e4493bf6p+0"
        },
        {
          "float64_exact_decimal": "1.691498653166261245672785662463866174221038818359375",
          "float64_hex": "0x1.b1060e4493bf6p+0"
        }
      ],
      "max_scaled_residual": {
        "float64_exact_decimal": "8.07778492082877528090165739010626187174019126845114779911227742559276521205902099609375E-16",
        "float64_hex": "0x1.d1a7109cddecep-51"
      },
      "hermiticity_max": {
        "float64_exact_decimal": "3.4265488115139595173535431120845482206707912557590300917098602440091781318187713623046875E-16",
        "float64_hex": "0x1.8b0dded0a78bbp-52"
      }
    },
    {
      "cutoff": 7,
      "quadrature_each_axis": 128,
      "dimension": 225,
      "omega_squared": [
        {
          "float64_exact_decimal": "0.2500000000000295319324550291639752686023712158203125",
          "float64_hex": "0x1.0000000000214p-2"
        },
        {
          "float64_exact_decimal": "0.69157788090181349094365259588812477886676788330078125",
          "float64_hex": "0x1.62167efa38759p-1"
        },
        {
          "float64_exact_decimal": "0.69611020724719996355389639575150795280933380126953125",
          "float64_hex": "0x1.64688e9d13b71p-1"
        },
        {
          "float64_exact_decimal": "1.240222636934619426796189145534299314022064208984375",
          "float64_hex": "0x1.3d7f3b1164a06p+0"
        },
        {
          "float64_exact_decimal": "1.240222636934619426796189145534299314022064208984375",
          "float64_hex": "0x1.3d7f3b1164a06p+0"
        },
        {
          "float64_exact_decimal": "1.677093650590919526877087264438159763813018798828125",
          "float64_hex": "0x1.ad56026d9e042p+0"
        },
        {
          "float64_exact_decimal": "1.677093650590919526877087264438159763813018798828125",
          "float64_hex": "0x1.ad56026d9e042p+0"
        },
        {
          "float64_exact_decimal": "1.69149865316625636069147731177508831024169921875",
          "float64_hex": "0x1.b1060e4493be0p+0"
        },
        {
          "float64_exact_decimal": "1.69149865316625636069147731177508831024169921875",
          "float64_hex": "0x1.b1060e4493be0p+0"
        }
      ],
      "max_scaled_residual": {
        "float64_exact_decimal": "5.291633310098403650577077671853971571819521212652615016480694976053200662136077880859375E-16",
        "float64_hex": "0x1.310ab96d3568bp-51"
      },
      "hermiticity_max": {
        "float64_exact_decimal": "1.8908140758317276149527186887368681329077020592498159512473421273170970380306243896484375E-16",
        "float64_hex": "0x1.b3fdf6745d2eep-53"
      }
    }
  ],
  "checks": {
    "flat_cylinder_max_error": {
      "float64_exact_decimal": "2.220446049250313080847263336181640625E-16",
      "float64_hex": "0x1.0000000000000p-52"
    },
    "corrugated_constant_mode_error": {
      "float64_exact_decimal": "2.120525977034048992209136486053466796875E-14",
      "float64_hex": "0x1.7e00000000000p-46"
    },
    "duffing_q_error_ratios": [
      {
        "float64_exact_decimal": "4.0001489223107054016281836084090173244476318359375",
        "float64_hex": "0x1.000270a01d106p+2"
      },
      {
        "float64_exact_decimal": "4.0000372611116734589131738175638020038604736328125",
        "float64_hex": "0x1.00009c48d0632p+2"
      }
    ],
    "lapse_exact_ground_error": {
      "float64_exact_decimal": "3.6692870963861423661001026630401611328125E-14",
      "float64_hex": "0x1.4a80000000000p-45"
    }
  }
}
```

## 138. Defined continuation points

The next mathematical problems are now concrete. A nonlinear surface simulation can use the derived weak action and verify field energy and mode leakage. A mechanical realization can solve the displayed shape equation with measured elastic parameters. A bulk realization can derive a thin layer effective action from an explicit confinement mechanism. A gravitational realization can solve constraint satisfying initial data in the declared scalar tensor model. A quantum calculation can select a state and renormalization conditions before evaluating the fluctuation determinants.

Each continuation starts from an explicit action, a declared domain, and a measurable or computable target. The present document supplies those definitions, exact limits, and reproducible verification records for the prescribed geometry scalar problem, while stating the additional inputs required by the broader extensions.
