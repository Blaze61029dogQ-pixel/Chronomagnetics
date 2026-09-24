# Executed validation record

Release 1.0.0. This record is generated from the delivered result files, not from predicted outcomes.

**30 tests run; 0 failures; 0 errors.**

This is implementation verification on specified problems. It does not constitute physical validation or a certified bound on continuum error.

## Execution environment

| Item | Recorded value |
|---|---|
| python | 3.12.14 |
| numpy | 2.3.5 |
| scipy | 1.17.0 |
| platform | Linux-6.18.44-x86_64-with-glibc2.39 |
| solver_version | 1.0.0 |
| solver_sha256 | c938afe9938ddbe034121d2483771ef4fbb4d3d229c49030d9e5928be9cd436e |
| arithmetic | IEEE-754 binary64 |
| threads | {"OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": null} |

## Test inventory

| Test | Outcome |
|---|---|
| test_01_flat_geometry | passed |
| test_02_curvature_against_embedding | passed |
| test_03_gauss_bonnet | passed |
| test_04_flat_spectrum | passed |
| test_05_constant_mode_curved | passed |
| test_06_lapse_exact_ground | passed |
| test_07_independent_complex_assembly | passed |
| test_08_phase_translation_invariance | passed |
| test_09_mass_shift_and_lapse_scaling | passed |
| test_10_eigen_residual_and_orthogonality | passed |
| test_11_potential_second_order | passed |
| test_12_energy_gradient | passed |
| test_13_hessian_directional_derivative | passed |
| test_14_cubic_projection_dealiasing | passed |
| test_15_full_field_duffing | passed |
| test_16_corrugated_nonlinear_energy_order | passed |
| test_17_manufactured_nonlinear_forcing | passed |
| test_18_exact_damping_loss | passed |
| test_19_negative_mode_is_retained | passed |
| test_20_broken_vacuum_equilibrium | passed |
| test_21_zero_stationary_is_classified_unstable | passed |
| test_22_nonuniform_equilibrium | passed |
| test_23_restart_exact_same_environment | passed |
| test_24_checkpoint_tamper_rejected | passed |
| test_25_checkpoint_wrong_operator_rejected | passed |
| test_26_bad_geometry_and_nonfinite_rejected | passed |
| test_27_timestep_guard_preserves_state | passed |
| test_28_basis_and_quadrature_convergence | passed |
| test_29_real_field_contract | passed |
| test_30_finite_resource_budget | passed |

## Exact stored metrics

Each decimal below is the exact value of the stored binary64 result. This formatting adds no accuracy beyond the original computation. The hexadecimal form provides a compact exact representation. Test thresholds, initial data, and resolutions are executable in verify_solver.py.

| Metric | Exact binary64 decimal | Binary64 hexadecimal |
|---|---|---|
| gauss_bonnet_absolute_residual | 1.1818864095956486527919425808107906368296636211157046858488683938048779964447021484375E-15 | 0x1.54a7d311a5b1cp-50 |
| flat_spectrum_max_error | 9.76996261670137755572795867919921875E-15 | 0x1.6000000000000p-47 |
| curved_constant_mode_error | 8.8817841970012523233890533447265625E-16 | 0x1.0000000000000p-50 |
| lapse_ground_error | 1.609823385706476983614265918731689453125E-15 | 0x1.d000000000000p-50 |
| independent_complex_spectrum_error | 1.95399252334027551114559173583984375E-14 | 0x1.6000000000000p-46 |
| eigen_max_scaled_residual | 1.17057540523412412565154391133392735935602870585466039887734268631902523338794708251953125E-16 | 0x1.0dea9363d1a01p-53 |
| potential_fourth_order_remainder_ratio_0 | 15.9667559428828642609232701943255960941314697265625 | 0x1.feefaa28bca85p+3 |
| potential_fourth_order_remainder_ratio_1 | 15.991687650112449858852414763532578945159912109375 | 0x1.ffbbe7bd228fep+3 |
| duffing_field_error_ratio_0 | 4.000054058081463637108754483051598072052001953125 | 0x1.0000e2bc6c494p+2 |
| duffing_field_error_ratio_1 | 4.00001351874818400489175473921932280063629150390625 | 0x1.000038b3a5349p+2 |
| nonlinear_energy_error_ratio_0 | 4.000010017175480214746130513958632946014404296875 | 0x1.00002a03dc3acp+2 |
| nonlinear_energy_error_ratio_1 | 4.000002506915055988656604313291609287261962890625 | 0x1.00000a83c7904p+2 |
| manufactured_finest_max_field_error | 3.425262609935142421591081074438989162445068359375E-7 | 0x1.6fc8e6d580000p-22 |
| damping_balance_absolute_error | 4.44089209850062616169452667236328125E-16 | 0x1.0000000000000p-51 |
| broken_vacuum_dual_residual | 8.35368145791205895423125561362424125144113436214343693109185551293194293975830078125E-15 | 0x1.2cf91ca9a726ap-47 |
| nonuniform_equilibrium_dual_residual | 2.85397061829670848883514607823688934709754363126810172701652845717035233974456787109375E-15 | 0x1.9b4cee61c2c63p-49 |
| basis_refinement_change_0 | 0.004146539998824749773120856843888759613037109375 | 0x1.0fbf65afbf000p-8 |
| basis_refinement_change_1 | 0.000109932969141635084042718517594039440155029296875 | 0x1.cd17a07638000p-14 |

The Duffing field error and varying nonlinear energy error ratios approach four when the timestep is halved, supporting second order convergence for those fixed spatial problems. The potential remainder ratios approach sixteen when potential amplitude is halved, supporting the expected fourth order remainder after the second order perturbative term. Neither observation is a universal error bound.

## Executed example jobs

### corrugated_spectrum

Result: results/corrugated_spectrum/report.json. Task: spectrum. Solver source hash matches this release.

| Sorted index | Exact squared frequency |
|---|---|
| 0 | 0.2499999999999999722444243843710864894092082977294921875 |
| 1 | 0.6915778816683679774968140918645076453685760498046875 |
| 2 | 0.6961102077675003219070504201226867735385894775390625 |
| 3 | 1.2402328259644814778539512190036475658416748046875 |
| 4 | 1.2402328259644814778539512190036475658416748046875 |
| 5 | 1.6771067430650337115594084025360643863677978515625 |
| 6 | 1.67710674306503815245150690316222608089447021484375 |
| 7 | 1.6915061519621144014990932191722095012664794921875 |
| 8 | 1.69150615196211884239119171979837119579315185546875 |

### lapse_spectrum

Result: results/lapse_spectrum/report.json. Task: spectrum. Solver source hash matches this release.

| Sorted index | Exact squared frequency |
|---|---|
| 0 | 0.24000000000000787370169064161018468439579010009765625 |
| 1 | 1.1967476952748310470298065411043353378772735595703125 |
| 2 | 1.2163852121136662365330494139925576746463775634765625 |
| 3 | 4.08511486125286182868876494467258453369140625 |
| 4 | 4.0854721933460016458639074699021875858306884765625 |
| 5 | 8.885093215496024043886791332624852657318115234375 |

### nonlinear_wave

Result: results/nonlinear_wave/report.json. Task: evolve. Solver source hash matches this release.

Stored samples: 101. Initial global step: 0. Final global step: 1000.

| Diagnostic | Exact binary64 decimal |
|---|---|
| Final step | 1000 |
| Final time | 5 |
| Final energy | 0.5031715672944037098801572938100434839725494384765625 |
| Final work | 0 |
| Final dissipated | 0 |
| Final balance_defect | -2.605429880730980585212819278240203857421875E-7 |
| Final max_abs_field | 0.1954887691417796780068982798184151761233806610107421875 |
| Final mass_norm | 0.75554165837669085004080216094735078513622283935546875 |
| Maximum sampled absolute balance defect | 0.0000053419174166347005439092754386365413665771484375 |

The maximum is computed over stored samples only. The resumed run retains the original energy reference and cumulative work and dissipation.

### nonuniform_equilibrium

Result: results/nonuniform_equilibrium/report.json. Task: equilibrium. Solver source hash matches this release.

| Diagnostic | Value |
|---|---|
| Converged | True |
| Reason | residual_tolerance |
| residual | 6.5048849337534230684421514683876543854522509109650219016884875600226223468780517578125E-15 |
| tolerance | 1.1782551004832177300008987664019406704785097872445476241409778594970703125E-10 |
| energy | -3.68431409590940717180274077691137790679931640625 |
| Smallest discrete Hessian eigenvalue | 0.996480041242840730575380803202278912067413330078125 |
| Stationary classification | positive |

### driven_wave

Result: results/driven_wave/report.json. Task: evolve. Solver source hash matches this release.

Stored samples: 21. Initial global step: 0. Final global step: 400.

| Diagnostic | Exact binary64 decimal |
|---|---|
| Final step | 400 |
| Final time | 2 |
| Final energy | 0.1077628379424848958922922292913426645100116729736328125 |
| Final work | -0.00765088500338407216661007481661727069877088069915771484375 |
| Final dissipated | 0.010063221197366210846180223370538442395627498626708984375 |
| Final balance_defect | -6.6331197137899089444346145683084614574909210205078125E-7 |
| Final max_abs_field | 0.076474601979028722364972736613708548247814178466796875 |
| Final mass_norm | 0.27353192249445001937857568918843753635883331298828125 |
| Maximum sampled absolute balance defect | 0.000001299617410333540890032821835120557807385921478271484375 |

The maximum is computed over stored samples only. The resumed run retains the original energy reference and cumulative work and dissipation.

### driven_resumed

Result: results/driven_resumed/report.json. Task: evolve. Solver source hash matches this release.

Stored samples: 11. Initial global step: 400. Final global step: 600.

| Diagnostic | Exact binary64 decimal |
|---|---|
| Final step | 600 |
| Final time | 3 |
| Final energy | 0.1091329390909357155425851715335738845169544219970703125 |
| Final work | -0.005179697348723218304489268604129392770119011402130126953125 |
| Final dissipated | 0.011164546875299934114433852982983808033168315887451171875 |
| Final balance_defect | -4.241402476908018304158076716703362762928009033203125E-7 |
| Final max_abs_field | 0.09278357741610911146867834986551315523684024810791015625 |
| Final mass_norm | 0.322633109919202076820710090032662265002727508544921875 |
| Maximum sampled absolute balance defect | 6.6331197137899089444346145683084614574909210205078125E-7 |

The maximum is computed over stored samples only. The resumed run retains the original energy reference and cumulative work and dissipation.

### refinement

Result: results/refinement/report.json. Task: convergence. Solver source hash matches this release.

| Sequence | Setting | Maximum absolute change from previous in the same sequence |
|---|---|---|
| basis | 2 | First run; no preceding comparison |
| basis | 3 | 0.0040153162756109139763793791644275188446044921875 |
| basis | 4 | 9.238273286360509928272222168743610382080078125E-7 |
| basis | 5 | 0.000013087712516846039534357259981334209442138671875 |
| quadrature | 32 | First run; no preceding comparison |
| quadrature | 48 | 7.3274719625260331667959690093994140625E-15 |
| quadrature | 64 | 4.6629367034256574697792530059814453125E-15 |

Basis refinement holds the configured 48 by 48 quadrature fixed; quadrature refinement holds the configured cutoff four fixed. These are observed changes, not interval enclosures.

### potential_sweep

Result: results/potential_sweep/report.json. Task: sweep. Solver source hash matches this release.

| Exact parameter | Exact lowest squared frequency |
|---|---|
| 0 | 0.250000000000000055511151231257827021181583404541015625 |
| 0.025000000000000001387778780781445675529539585113525390625 | 0.2498593729919111883219784431275911629199981689453125 |
| 0.05000000000000000277555756156289135105907917022705078125 | 0.2494374678872419703878904329030774533748626708984375 |
| 0.1000000000000000055511151231257827021181583404541015625 | 0.2477494872633846656473366465434082783758640289306640625 |
| 0.200000000000000011102230246251565404236316680908203125 | 0.240991864412079370705299652399844489991664886474609375 |

## Reproduction and limits

Run python verify_solver.py --out my_verification.json for a fresh local receipt. Run python run_examples.py --out my_runs for verification and all example jobs. The runner uses the current Python interpreter and preserves explicitly configured BLAS thread environment variables.

The provided tests are targeted checks of mathematical behavior and failure handling. They are not an exhaustive proof of every parameter combination, convergence for every solution, or every operating system. In particular, native Windows was not executed in this environment; the delivered scripts use portable Python, NumPy, and SciPy interfaces.

The original verification and examples use the solver hash shown above. If phasefield.py is edited, rerun verification and regenerate examples before associating these numerical claims with the changed solver. Existing checkpoints intentionally reject a changed solver source.
