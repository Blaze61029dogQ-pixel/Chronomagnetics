# Complete configuration reference

Configuration files are JSON objects. Unknown keys are rejected. Omitted sections and fields receive the defaults below. Physical real parameters accept finite JSON numbers or quoted rational strings such as "1/10". Integer counts must be JSON integers, not quoted strings. A fraction is converted to binary64 after parsing; it does not enable exact rational evolution.

## model

| Key | Default | Meaning |
|---|---|---|
| radius | 1.0 | Mean tube radius R0; strictly greater than abs(amplitude). |
| amplitude | 0.1 | Corrugation amplitude A; may have either sign. |
| axial_scale | 1.5 | Axial length scale a; period is 2 pi a; strictly positive. |
| n | 2 | Positive integer theta corrugation harmonic. |
| m | 1 | Positive integer zeta corrugation harmonic. |
| phase_theta | 0.0 | Theta corrugation phase in radians. |
| phase_zeta | 0.0 | Zeta corrugation phase in radians. |
| mass2 | 0.25 | Signed bare quadratic coefficient m0 squared. |
| quartic | 0.5 | Nonnegative lambda; energy has lambda phi^4/4. |
| potential_constant | 0.0 | Constant part Uc of U; stiffness uses mass2 + 2U. |
| potential_amplitude | 0.0 | Sin(theta harmonic) times cos(zeta harmonic) amplitude in U. |
| potential_n | 2 | Nonnegative integer theta potential harmonic. |
| potential_m | 1 | Nonnegative integer zeta potential harmonic. |
| potential_phase_theta | 0.0 | Theta potential phase in radians. |
| potential_phase_zeta | 0.0 | Zeta potential phase in radians. |
| curvature_h2 | 0.0 | Coefficient multiplying mean curvature squared inside U. |
| curvature_k | 0.0 | Coefficient multiplying Gaussian curvature inside U. |
| lapse_scale | 1.0 | Positive lapse scale N0. |
| lapse_amplitude | 0.0 | Relative cosine product lapse amplitude; absolute value below one. |
| lapse_n | 1 | Nonnegative integer theta lapse harmonic. |
| lapse_m | 0 | Nonnegative integer zeta lapse harmonic. |
| lapse_phase_theta | 0.0 | Theta lapse phase in radians. |
| lapse_phase_zeta | 0.0 | Zeta lapse phase in radians. |

## resolution

| Key | Default | Meaning |
|---|---|---|
| theta_cutoff | 4 | Nonnegative maximum theta Fourier harmonic. |
| zeta_cutoff | 4 | Nonnegative maximum zeta Fourier harmonic. |
| theta_points | 48 | Uniform quadrature points; strictly above four times theta_cutoff. |
| zeta_points | 48 | Uniform quadrature points; strictly above four times zeta_cutoff. |
| memory_limit_mib | 1024 | Positive integer estimate budget, in units of 2^20 bytes. |

## initial

| Key | Default | Meaning |
|---|---|---|
| kind | cosine | constant, cosine, or eigenmode. |
| amplitude | 1/10 | Physical profile amplitude for constant/cosine; modal coefficient for eigenmode. |
| offset | 0 | Constant position offset for constant/cosine only. |
| theta_mode | 1 | Nonnegative cosine profile harmonic; must lie within the theta basis for cosine initial data. |
| zeta_mode | 1 | Nonnegative cosine profile harmonic; must lie within the zeta basis for cosine initial data. |
| velocity_amplitude | 0 | Velocity profile amplitude, with the same normalization as position amplitude. |
| phase_theta | 0 | Theta cosine phase in radians; cosine kind only. |
| phase_zeta | 0 | Zeta cosine phase in radians; cosine kind only. |
| mode_index | 1 | Zero based sorted eigenvector index; eigenmode kind only. |

## drive

| Key | Default | Meaning |
|---|---|---|
| amplitude | 0 | Physical source amplitude; zero disables drive. |
| frequency | 1 | Angular frequency in coordinate time. |
| theta_mode | 1 | Nonnegative integer theta cosine source harmonic. |
| zeta_mode | 1 | Nonnegative integer zeta cosine source harmonic. |
| phase_time | 0 | Time cosine phase in radians. |
| phase_theta | 0 | Theta cosine phase in radians. |
| phase_zeta | 0 | Zeta cosine phase in radians. |

The source is s = amplitude cos(frequency t + phase_time) cos(theta_mode theta + phase_theta) cos(zeta_mode zeta + phase_zeta). It appears on the right side of the positive time equation specified in NUMERICAL_METHOD.md. The configured drive is ignored by spectrum, converge, and sweep, and must vanish for equilibrium.

## damping

The top level damping key is a nonnegative real scalar, default zero. The finite equation includes damping times M times velocity. It measures decay per unit coordinate time.

## Resolution and input checks

Geometry, lapse, and potential harmonics must be sampled below the Nyquist limit. A nonzero drive must also be resolved by the quadrature. These conditions do not certify product quadrature with variable geometry. Cutoff and quadrature refinement remain separate requirements.

The supported scalar field is real. Complex arrays are rejected by the field and coefficient interfaces rather than silently discarding their imaginary parts. Parameters cannot be NaN or infinity. A valid nondegenerate geometry does not by itself imply a well conditioned numerical problem.

## API arguments beyond JSON

Time stepping accepts dt, steps, sample_every, guard, and an optional callback through integrate. The command line exposes dt, steps, and sample_every and uses guard = 1.8. The API stationary solver accepts max_iter, atol, and rtol; the command line exposes max_iter and uses the documented tolerance defaults. Resume preserves its checkpoint timestep and model; there is no command line override for those quantities.

## Minimal configuration

The empty object {} selects all defaults. For experiments, retain an explicit configuration file and copy its normalized form from the result report to avoid relying on future defaults. The six files under examples provide more useful starting points than a completely implicit configuration.
