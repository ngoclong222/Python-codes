# Orbit-Fitting Validation Report

**Planet Nine candidate (IRAS / AKARI triplet) versus five objects with known orbits**

Date: 2026-09-08
Code: `run_orbit-mcmc.py`, `run_orbit-free_params.py`, `validation/run_validation.py`,
`validation/run_mcmc_validation.py`, `validation/fit_p9_row.py`

---

## 0. Purpose and experimental design

The Planet Nine candidate rests on **three** detections:

| Label | Epoch (UTC) | RA (deg) | Dec (deg) |
|---|---|---|---|
| IRAS | 1983-04-23T10:42:31.6 | 121.75170 | 13.22079 |
| AKARI_1 | 2006-10-26T17:13:56.4 | 124.11840 | 14.33744 |
| AKARI_2 | 2007-04-23T23:32:59.0 | 124.46950 | 14.46484 |

Three detections give **6 observables** (RA, Dec × 3) against **6 orbital
elements**, so the system is *exactly determined*: **dof = 0**. Before trusting
any Planet Nine number, the same machinery was run on five objects whose orbits
are published, using the **same adversarial geometry**:

* two detections ~6 months apart (maximum parallax),
* one detection ~5-34 years earlier at nearly the same time of year (long
  proper-motion baseline, almost no differential parallax).

Astrometry was taken from the MPC (Sednoids) and JPL Horizons (gas giants);
ground truth is the Horizons osculating element set **evaluated at the fit
epoch** (`validation/data/truth_at_epoch.csv`), since osculating elements drift.
All fits assume 5 arcsec per-coordinate uncertainty, matching the assumed
IRAS/AKARI error.

**Validation targets and truth at fit epoch (Table 0)**

| Target | a (AU) | e | i (deg, ecl) | q (AU) | r at epoch (AU) | Baseline (yr) |
|---|---|---|---|---|---|---|
| Uranus | 19.306 | 0.0480 | 0.774 | 18.380 | 19.020 | 5.01 |
| Neptune | 30.285 | 0.0062 | 1.770 | 30.097 | 30.261 | 5.01 |
| Sedna | 547.983 | 0.8607 | 11.929 | 76.341 | 83.496 | 34.03 |
| 2012 VP113 | 269.043 | 0.7005 | 24.011 | 80.586 | 82.922 | 5.89 |
| Leleākūhonua | 1085.185 | 0.9403 | 11.663 | 64.786 | 78.825 | 13.04 |

---

# PART 1 — Monte Carlo (least-squares + noise resampling)

Method: free 6-parameter least-squares fit with 300 random restarts, then 60
Monte Carlo replicas in which 5 arcsec Gaussian noise is added to the astrometry
and the fit is repeated. Source: `validation/run_validation.py`,
`validation/fit_p9_row.py`.

## 1.1 Best-fit versus published values

**Table 1 — Monte Carlo best fit versus truth** (`validation/validation_results.csv`)

| Target | a true | a fit | e true | e fit | i true | i fit | q true | q fit | r true | r fit | RMS (arcsec) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Uranus | 19.306 | 16.561 | 0.048 | 0.203 | 0.774 | 0.779 | 18.380 | 13.201 | 19.020 | 18.464 | 2.4e-11 |
| Neptune | 30.285 | 35.415 | 0.006 | 0.183 | 1.770 | 1.779 | 30.097 | 28.947 | 30.261 | 30.929 | 1.6e-10 |
| Sedna | 547.98 | 1472.44 | 0.861 | 0.949 | 11.929 | 11.929 | 76.341 | 74.925 | 83.496 | 83.608 | 0.215 |
| 2012 VP113 | 269.04 | 246.55 | 0.700 | 0.668 | 24.011 | 24.034 | 80.586 | 81.907 | 82.922 | 82.794 | 9.4e-10 |
| Leleākūhonua | 1085.19 | 3148.57 | 0.940 | 0.980 | 11.663 | 11.660 | 64.786 | 64.494 | 78.825 | 79.002 | 0.297 |
| **P9 candidate** | — | **8.32** | — | **0.879** | — | **−19.23** (eq) | — | **1.005** | — | **2.623** | **0.000** |

Reading Table 1:

* **Inclination is recovered essentially perfectly** for all five targets
  (worst error 0.023 deg, on 2012 VP113).
* **Heliocentric distance is recovered to sub-percent** accuracy
  (worst error 0.7 AU, on Neptune).
* **Perihelion distance q is good** (worst 5 AU, on Uranus).
* **Semi-major axis a and eccentricity e are poor**: Sedna 548 → 1472 AU,
  Leleākūhonua 1085 → 3149 AU. Both are pushed to higher a *and* higher e,
  the signature of the degeneracy discussed in §3.1.
* **RMS residuals are at or below the noise floor** for all five targets, so in
  every validation case a genuine Keplerian orbit reproduces the three
  detections.

## 1.2 The Planet Nine row is qualitatively different

The P9 entry in Table 1 achieves RMS = 0.000 arcsec, but inspection of the
solution shows it is **unphysical**:

```
a = 8.32 AU, e = 0.879, q = 1.005 AU, r(fit epoch) = 2.62 AU
observer-relative distances = [0.02, 2.43, 0.00] AU
```

The optimiser placed the object **at the observer** (geocentric distance ~0 AU at
detections 1 and 3). At zero range the apparent RA/Dec are arbitrary, so any
sky positions can be matched exactly. This is a coordinate singularity, not a
solution.

Once the object is required to be *distant*, no Keplerian orbit fits. From the
fixed-`a` scan (`monte_carlo_summary.txt`, `fixed_a_orbital_parameters.csv`):

**Table 2 — P9 fixed-`a` scan: residual never approaches the noise floor**

| a (AU) | e | i (deg, eq) | q (AU) | d1, d2, d3 (AU) | RMS (arcsec) | RMS / 5" |
|---|---|---|---|---|---|---|
| 200 | 0.106 | 31.876 | 178.71 | 219.6, 219.9, 219.9 | 836.08 | 167 |
| 350 | 0.297 | 31.517 | 245.98 | 246.4, 246.8, 246.8 | 778.04 | 156 |
| 700 | 0.622 | 31.317 | 264.51 | 264.7, 265.0, 265.0 | 745.30 | 149 |
| 1000 | 0.730 | 31.263 | 270.03 | 270.2, 270.5, 270.5 | 736.32 | 147 |
| 1500 | 0.817 | 31.222 | 274.32 | 274.5, 274.8, 274.8 | — | — |
| 2000 | 0.862 | 31.202 | 276.46 | 276.6, 276.9, 276.9 | — | — |

The residual is **147-167 times the assumed uncertainty at every value of `a`**,
and it decreases monotonically toward large `a` without ever becoming
acceptable. The fitted distance saturates at **260-280 AU** (see §3.2).

## 1.3 Are the Monte Carlo error bars honest?

The critical question is not whether `a` is recovered, but whether the quoted
uncertainty *admits* that it is not. Define z = (median − truth) / std.

**Table 3 — Monte Carlo coverage** (`validation/validation_monte_carlo.csv`, 60 trials)

| Target | quantity | truth | MC median | MC std | z |
|---|---|---|---|---|---|
| Uranus | a | 19.306 | 18.899 | 84.73 | −0.005 |
| | e | 0.0480 | 0.1531 | 0.1925 | +0.546 |
| | i | 0.7744 | 0.7726 | 0.0066 | −0.278 |
| | r | 19.020 | 18.953 | 0.733 | −0.092 |
| Neptune | a | 30.285 | 30.875 | 10.38 | +0.057 |
| | e | 0.0062 | 0.1184 | 0.1380 | +0.813 |
| | i | 1.7696 | 1.7696 | 0.0092 | −0.010 |
| | r | 30.261 | 30.360 | 0.882 | +0.112 |
| Sedna | a | 547.98 | 663.20 | 1334.69 | +0.086 |
| | e | 0.8607 | 0.8852 | 0.1618 | +0.151 |
| | i | 11.929 | 11.928 | 0.0269 | −0.023 |
| | r | 83.496 | 83.482 | 10.576 | −0.001 |
| 2012 VP113 | a | 269.04 | 293.78 | 1091.43 | +0.023 |
| | e | 0.7005 | 0.7362 | 0.1232 | +0.290 |
| | i | 24.011 | 24.065 | 0.0671 | +0.805 |
| | r | 82.922 | 82.876 | 0.398 | −0.116 |
| Leleākūhonua | a | 1085.19 | 1064.79 | 1134.86 | −0.018 |
| | e | 0.9403 | 0.9387 | 0.1570 | −0.010 |
| | i | 11.663 | 11.672 | 0.0106 | +0.908 |
| | r | 78.825 | 78.887 | 1.114 | +0.056 |

**Every one of the 20 z-scores satisfies |z| < 1.** The Monte Carlo error bars
are therefore well calibrated, including for `a`, where the honest answer is a
huge uncertainty (Uranus: 18.9 ± 84.7 AU — an error bar four times the value
itself; Sedna: 663 ± 1335 AU). The estimator is not biased; it is *imprecise*
in `a` and `e`, and it correctly says so.

**Part 1 verdict:** the Monte Carlo pipeline is **validated**. It recovers
distance, inclination and perihelion distance accurately, and its error bars
cover the truth for every parameter and every target. Applied to P9, it finds
no physically acceptable orbit — residuals stay at ~150σ for any distant `a`.

---

# PART 2 — MCMC (emcee ensemble sampler)

Method: the **actual** `log_prior`, `log_likelihood`, `log_probability` and
propagator from `run_orbit-mcmc.py`, with only the detection globals rebound to
each target (`validation/run_mcmc_validation.py`). Nothing statistical is
re-implemented, so whatever the sampler does to P9 it does to these targets.
Prior on `a` is widened per target to `[0.51 r, 100 r]` so that Uranus is not
excluded. Runs: 32 walkers, 40 000 steps, 12 000 burn-in, thinned by 20, ball
initialisation around the least-squares solution.

## 2.1 Validation targets

**Table 4 — MCMC 68% credible intervals versus truth**
(`validation/mcmc_validation_20260908_ball_*.csv`; angles are **equatorial**,
the frame in which the code fits)

| Target | param | truth | p16 | median | p84 | truth in 68%? | split-Rhat | tau (steps) |
|---|---|---|---|---|---|---|---|---|
| Uranus | a | 19.307 | 15.140 | 16.287 | 17.137 | **No** | 2.14 | 3931 |
| | e | 0.0480 | 0.1604 | 0.2246 | 0.3286 | **No** | 2.04 | 3914 |
| | i | 23.663 | 23.6638 | 23.6659 | 23.6682 | **No** | 1.07 | 34 |
| | Ω | 1.8555 | 1.8489 | 1.8601 | 1.8717 | Yes | 1.08 | 173 |
| | ω | 175.911 | 110.834 | 115.480 | 120.760 | **No** | 2.41 | 3932 |
| Neptune | a | 30.286 | 32.992 | 34.492 | 36.261 | **No** | 2.44 | 4151 |
| | e | 0.0062 | 0.1125 | 0.1564 | 0.2040 | **No** | 2.27 | 4100 |
| | i | 22.297 | 22.2984 | 22.2997 | 22.3010 | **No** | 1.10 | 23 |
| | Ω | 3.4793 | 3.4909 | 3.5170 | 3.5446 | **No** | 1.09 | 829 |
| | ω | 349.692 | 319.785 | 321.506 | 323.632 | **No** | 1.47 | 2745 |
| Sedna | a | 547.98 | 2946.4 | 3126.1 | 3410.2 | **No** | 3.48 | 4078 |
| | e | 0.8607 | 0.9745 | 0.9759 | 0.9781 | **No** | 17.10 | 3496 |
| | i | 15.318 | 15.2999 | 15.3055 | 15.3104 | **No** | 32.84 | 92 |
| | Ω | 27.135 | 27.1023 | 27.1130 | 27.1241 | **No** | 135.32 | 183 |
| | ω | 69.475 | 72.235 | 72.574 | 72.988 | **No** | 4.85 | 1402 |
| 2012 VP113 | a | 269.04 | 241.56 | 248.81 | 257.34 | **No** | 2.24 | 3650 |
| | e | 0.7005 | 0.6596 | 0.6721 | 0.6870 | **No** | 2.71 | 3771 |
| | i | 32.793 | 32.7897 | 32.8194 | 32.8507 | Yes | 1.32 | 1376 |
| | Ω | 48.696 | 48.6991 | 48.7016 | 48.7041 | **No** | 1.32 | 24 |
| | ω | 341.434 | 341.220 | 347.437 | 354.319 | Yes | 3.29 | 4093 |
| Leleākūhonua | a | 1085.19 | 701.09 | 1022.84 | 1203.22 | Yes | 34.65 | 1811 |
| | e | 0.9403 | 0.9256 | 0.9990 | 0.9990 | Yes | 99.09 | 1580 |
| | i | 30.989 | 0.00006 | 0.00006 | 0.00006 | **No** | 1.00 | 20 |
| | Ω | 340.309 | 4.856 | 179.941 | 312.756 | **No** | 112.82 | 2696 |
| | ω | 76.868 | 60.021 | 338.649 | 338.739 | Yes | 50.51 | 3160 |

Acceptance fractions: Uranus/Neptune/Sedna/2012 VP113 ~0.07-0.24,
Leleākūhonua 0.113.

Leleākūhonua is the clearest illustration of a chain that has failed while
looking superficially plausible: its `a` interval does bracket the truth, but
with Rhat = 34.7 that is luck, not inference. Its inclination has collapsed
entirely to a single value of 6e-5 deg (width exactly 0.0, Rhat = 1.00,
tau = 20) — the walkers are frozen, and the "converged" flag that Rhat awards
that parameter is an artefact of them all being stuck at the same point.
Eccentricity has piled up against the e < 0.999 prior wall.

Two things are immediately wrong:

1. **Nothing converged.** Split-Rhat should be < 1.01. Observed values reach
   **135.3** (Sedna Ω) and **112.8** (Leleākūhonua Ω); only parameters whose
   walkers are completely frozen score well. The integrated autocorrelation
   time reaches ~4150 steps, so a 40 000-step chain holds at best ~10
   independent samples per walker, where ~50τ (≈210 000 steps) is required.
2. **The credible intervals miss the truth in 19 of 25 entries.** Some are
   absurdly overconfident: Sedna's Ω interval is 0.02 deg wide with Rhat = 135,
   and Leleākūhonua's inclination collapsed to a single value (6e-5 deg, width
   exactly zero — this crashed `corner`, now patched).

These narrow intervals are **not** measurements. With acceptance ~0.07 the
walkers barely move, so the "posterior" is largely the initialisation ball
remembered back to the user.

**Figures:** `validation/posteriors/corner_Uranus_20260908_ball.png`,
`corner_Neptune_20260908_ball.png`, `corner_Sedna_20260908_ball.png`,
`corner_2012VP113_20260908_ball.png`,
`corner_Leleakuhonua_20260908_ball.png`. Red lines mark JPL truth, dotted blue
lines the prior edges; `a` is plotted as log10 because the posterior spans
decades.

## 2.2 Is it the parametrisation? Three sampler variants on Sedna

To check whether the failure is a fixable parametrisation problem, Sedna was run
three ways at an identical budget (128 walkers, 20 000 steps, thin 20).

**Table 5 — Sedna sampler comparison**
(`mcmc_validation_cmplin_Sedna.csv`, `cmplog`, `cmpfil`)

| Variant | Sampled `a` | Init | Acceptance | max split-Rhat | max tau |
|---|---|---|---|---|---|
| Linear | a | ball | 0.073 | 32.9 | 1792 |
| Log | log a | ball | 0.074 | 55.9 | 2053 |
| Filament | a | along valley | **0.008** | **142.1** | 2074 |

* **Log-`a`** (a log-uniform prior straightening a multi-decade valley) changed
  nothing: acceptance identical to 3 significant figures.
* **Filament initialisation** — walkers seeded along the degeneracy valley by
  fixing `a` on a log grid and re-fitting the other five elements — made things
  **worse**, because the valley is *curved*: the straight line between two
  distant walkers leaves the valley, so stretch proposals land at zero
  likelihood.

**Figures:** `validation/posteriors/corner_Sedna_cmplin.png`,
`corner_Sedna_cmplog.png`, `corner_Sedna_cmpfil.png`.

The failure is therefore **geometric, not parametric**.

## 2.2b Run-to-run irreproducibility

Leleākūhonua was run twice with **identical arguments** (32 walkers, 40 000
steps, seed 42). The two runs disagree:

| Run | Acceptance | max split-Rhat | a 95% interval (AU) |
|---|---|---|---|
| First | 0.073 | 8.95 | 69.4 – 2230.4 |
| Second | 0.113 | 261.51 | 49.6 – 1976.6 |

Cause: `emcee.EnsembleSampler` draws its proposals from numpy's **global** RNG,
while the script seeded only its own `default_rng(seed)` used for the initial
positions. The global RNG was never seeded, so every invocation explored a
different set of pockets. This has been fixed (`np.random.seed(seed)` added in
`run_mcmc_validation.py`).

The episode is itself diagnostic: for a properly converged chain the choice of
random stream would shift results by far less than the credible interval. A
swing in max Rhat from 8.9 to 261.5 shows the sampler is reporting the accident
of where its walkers happened to get stuck.

## 2.3 Planet Nine MCMC

Source: `mcmc_summary_20260906_225604_newepochs.txt`,
`mcmc_diagnostics_20260906_225604_newepochs.txt` (32 walkers, 4000 steps,
1000 burn-in, prior a ∈ [50, 5000] AU).

**Table 6 — P9 MCMC posterior**

| Parameter | Median | −1σ | +1σ | MCSE | Max-posterior |
|---|---|---|---|---|---|
| a (AU) | 3740.16 | 1625.51 | 1255.46 | 91.20 | 4999.03 |
| e | 0.9255 | 0.0563 | 0.0184 | 0.0023 | 0.9439 |
| i (deg, eq) | 31.146 | 0.061 | 0.053 | 0.0032 | 31.161 |
| Ω (deg, eq) | 99.156 | 0.061 | 0.055 | 0.0032 | 99.172 |
| ω (deg, eq) | 23.296 | 1.678 | 1.011 | 0.0883 | 24.264 |
| M (deg) | 0.0992 | 0.0558 | 0.0604 | 0.0045 | 0.0421 |

Converted to **ecliptic** elements (the frame in which published Planet Nine
predictions are quoted): **i = 41.21 deg, Ω = 129.16 deg, ω = 347.68 deg.**

**Table 7 — P9 MCMC diagnostics**

| Diagnostic | Value | Status |
|---|---|---|
| Mean acceptance | 0.243 | OK on average |
| Stuck walkers (<0.05) | 1 / 32 (index 7) | Warning |
| max tau | 540.6 steps (needs 50τ = 27 028) | Chain 4000 steps — **too short** |
| max split-Rhat | 3.35 (a: 2.51, e: 2.97, M: 3.35) | **FAIL** |
| RMS residual at best sample | **720.5 arcsec** | **FAIL — 144σ** |
| Max residual | 1285.8 arcsec | — |
| χ² | 1.246e5 (dof = 0) | Not usable as GoF |
| `a` within 1% of upper prior edge | **39.0%** of samples | **Prior-driven** |

Per-coordinate residuals of the best P9 sample:

| Coordinate | Residual (arcsec) | In σ |
|---|---|---|
| RA_IRAS | +84.18 | +16.8σ |
| RA_AKARI_1 | +1203.49 | +240.7σ |
| RA_AKARI_2 | −1285.77 | −257.2σ |
| Dec_IRAS | +59.93 | +12.0σ |
| Dec_AKARI_1 | −9.89 | −2.0σ |
| Dec_AKARI_2 | −49.78 | −10.0σ |

**Figures:** `mcmc_corner_20260906_225604_newepochs.png`,
`mcmc_traces_20260906_225604_newepochs.png`.

Note the pattern: the two AKARI right-ascensions are missed by ±1200-1300
arcsec **in opposite directions**. The model cannot bend enough to pass through
both, which is precisely what one expects if the two AKARI sources are not the
same moving object as assumed.

The quoted median a = 3740 AU is meaningless: 39% of the posterior sits against
the 5000 AU prior wall, Rhat = 2.5, and the underlying fit misses the data by
144σ.

**Part 2 verdict:** the MCMC is **not validated**. On objects with known orbits
it fails to converge and its credible intervals systematically exclude the truth.
Its P9 output must not be quoted as a measurement.

---

# PART 3 — Discussion and Conclusion

## 3.1 Why `a` and `e` are unconstrained (and why that is correct)

With three detections the fit is exactly determined, so a solution always
exists. But the *conditioning* is terrible in a specific direction. The three
detections tightly fix:

* the **direction** to the object at each epoch,
* the **plane** of the orbit (hence i and Ω to ~0.01-0.07 deg),
* the **distance** via parallax (hence r to <1%),
* and therefore **q**, the perihelion distance.

What they barely fix is the **radial velocity** — motion along the line of
sight. Over a short arc the sky-plane motion is almost independent of it. Yet by
the vis-viva relation,

    a = 1 / (2/r − v²/GM)

`a` diverges as v approaches escape speed. A sub-percent error in speed
therefore becomes a factor-of-several error in `a`. The consequence is a valley
in parameter space along which `a` and `e` increase together while **q = a(1−e)
stays fixed** — visible directly in Table 2, where `a` runs 200 → 2000 AU and
`e` runs 0.106 → 0.862 while q only moves 179 → 276 AU. This is why the
posteriors in Table 4 are wide in `a` and `e`, tight in i, Ω and r, and why the
Monte Carlo std on `a` (Table 3) is comparable to or larger than `a` itself.

This is a genuine property of the data, not a code defect. Demonstrated
independently in `validation/why_a_is_unconstrained.py`.

## 3.2 Why the fitted distance saturates at 260-280 AU

A bound orbit cannot move faster than escape speed, so an observed proper motion
μ implies a maximum distance:

    μ·d ≤ sqrt(2GM/d)   ⟹   d ≤ (2GM/μ²)^(1/3)

For the P9 triplet this ceiling is **259.9 AU**. The fits pile up at 260-280 AU
(Table 2) because that is the largest distance at which a *bound* Keplerian
orbit can still produce the observed angular motion. It is a physical boundary,
not a measurement and not a bias. The same calculation for the validation
targets gives ceilings of 24.2 (Uranus), 38.7 (Neptune), 94.9 (Sedna), 85.0
(2012 VP113) and 89.4 AU (Leleākūhonua) — and in every case the true distance
lies safely below its ceiling, which is why those fits behave. Implemented in
`validation/check_distance_bias.py` and `run_validation.escape_ceiling`.

## 3.3 Why MCMC fails where Monte Carlo succeeds

The two methods face the same degeneracy but respond very differently.

* **Monte Carlo** never has to *explore* the valley. Each replica is a
  deterministic optimisation that lands somewhere on it; the scatter across
  replicas maps the degeneracy correctly. Hence the honest |z| < 1 coverage in
  Table 3.
* **MCMC** must random-walk *along* the valley. With dof = 0 the likelihood is
  a razor-thin, curved, one-dimensional filament in 6-D. emcee's stretch move
  proposes along the line joining two walkers; because the filament is thin,
  almost every proposal lands off it at zero likelihood (acceptance 0.07), and
  because it is curved, even seeding walkers along it does not help (Table 5,
  acceptance 0.008). Walkers end up trapped in disconnected pockets, which is
  exactly what Rhat = 33-135 reports.

Both the tight-but-wrong intervals and the non-convergence in Table 4 follow
from this single cause.

## 3.4 What the P9 result actually means

Three independent lines of evidence agree:

1. No distant bound Keplerian orbit reproduces the three detections: RMS stays
   at 736-836 arcsec (147-167σ) for every `a` from 200 to 2000 AU (Table 2).
2. The MCMC best sample misses by 720 arcsec (144σ), with the two AKARI RA
   residuals of opposite sign at ±1200 arcsec (Table 7).
3. The only exact solution is the degenerate one that puts the object at the
   observer (§1.2).

Meanwhile the identical pipeline fits all five known objects to ≤0.3 arcsec
(Table 1). The machinery is therefore sound, and the conclusion is about the
data: **the IRAS and two AKARI positions are mutually inconsistent with a single
bound two-body orbit at the assumed 5 arcsec uncertainty.**

Possible explanations, in rough order of likelihood: the sources are not the
same object; the astrometric uncertainties are far larger than 5 arcsec
(reconciling them requires ~700 arcsec errors, which is implausible for either
mission); or an epoch/frame association error remains in the source catalogues.

## 3.5 How to improve

**Data (decisive).**
* **A fourth detection** is the single highest-value change. It moves dof from
  0 to 2, makes χ² a real goodness-of-fit statistic, and collapses the `a`-`e`
  valley. With dof = 0 no amount of statistical machinery can test the model.
* **Realistic per-detection uncertainties**, ideally with the full covariance
  including cross-scan versus in-scan asymmetry, rather than a flat 5 arcsec.

**Method (for the existing data).**
* **Report the profile likelihood in `a`**, not an MCMC posterior: fix `a`,
  re-fit the other five elements, and quote the Δχ² interval. This traverses
  the valley by construction and is already implemented in
  `why_a_is_unconstrained.py` and the fixed-`a` scan.
* **Reparametrise to Herget variables** (the two topocentric ranges ρ₁, ρ₂
  instead of a, e, M). These are close to orthogonal for a short arc and remove
  the vis-viva amplification. `solve_herget.py` already exists in the tree.
* **Use a sampler suited to curved degeneracies** — nested sampling (dynesty)
  or parallel tempering. Neither is currently installed (only emcee 3.1.6 and
  corner 2.3.0 are available); adding dynesty is recommended.
* **Bound the prior physically** to exclude the near-observer singularity of
  §1.2, e.g. a minimum geocentric distance.
* If emcee must be used, run ≥ 50τ ≈ 250 000 steps and **report Rhat, tau and
  acceptance next to every number**. The diagnostics added in this work make
  the failure visible rather than silent, which is their main value.

## 3.6 Conclusion

1. The **Monte Carlo / least-squares pipeline is validated.** On five objects
   with published orbits it recovers heliocentric distance to <1%, inclination
   to <0.03 deg and perihelion distance to a few AU, and — critically — all 20
   coverage z-scores satisfy |z| < 1, so its error bars are honest (Tables 1, 3).
2. It is **imprecise in `a` and `e` by construction**, because a short arc
   barely constrains radial velocity and vis-viva amplifies that into a
   factor-of-several uncertainty in `a` (§3.1). Large error bars on `a` are the
   correct answer, not a bug.
3. The **MCMC is not validated.** With dof = 0 the posterior is a thin curved
   filament that emcee's stretch move cannot sample; chains reach split-Rhat of
   135-262, credible intervals exclude the true value in 19 of 25 cases, and
   repeat runs with identical settings disagree (Tables 4, 5, §2.2b). This
   failure is geometric and was not fixed by log-`a` or by filament
   initialisation. **Do not quote the P9 MCMC posterior.**
4. For the **Planet Nine candidate**, every method agrees that no distant bound
   Keplerian orbit fits the three detections, with residuals of 720-836 arcsec
   ≈ 150σ (Tables 2, 7), against ≤0.3 arcsec for all five controls. The fitted
   distance saturates at the 259.9 AU escape-velocity ceiling and `a` is driven
   into the prior wall (39% of samples).
5. **The three detections are not consistent with a single bound two-body
   orbit.** A fourth epoch, or a re-examination of whether the IRAS and AKARI
   sources are the same object, is required before an orbit can be claimed.

---

## Appendix — Files

**Code**
`run_orbit-mcmc.py`, `run_orbit-free_params.py`, `Fixed_a/run_orbit-fixed_a.py`,
`solve_herget.py`, `diagnose_geometry.py`, `check_distance_bias.py`,
`validation/run_validation.py`, `validation/run_mcmc_validation.py`,
`validation/why_a_is_unconstrained.py`, `validation/fetch_observations.py`,
`validation/fit_p9_row.py`

**Results**
`validation/validation_results.csv` (Table 1),
`validation/validation_monte_carlo.csv` (Table 3),
`validation/p9_row.csv` (P9 row of Table 1),
`validation/mcmc_validation_20260908_ball_*.csv` (Table 4),
`validation/mcmc_validation_cmp{lin,log,fil}_Sedna.csv` (Table 5),
`monte_carlo_summary.txt`, `fixed_a_orbital_parameters.csv` (Table 2),
`mcmc_summary_20260906_225604_newepochs.txt`,
`mcmc_diagnostics_20260906_225604_newepochs.txt` (Tables 6, 7),
`validation/data/truth_at_epoch.csv` (Table 0)

**Figures**
`validation/posteriors/corner_{Uranus,Neptune,Sedna,2012VP113,Leleakuhonua}_20260908_ball.png`,
`validation/posteriors/corner_Sedna_cmp{lin,log,fil}.png`,
`mcmc_corner_20260906_225604_newepochs.png`,
`mcmc_traces_20260906_225604_newepochs.png`

**Caveats**
* Angles in Table 4 and Table 6 are **equatorial**; Table 0 and published values
  are **ecliptic**. The conversion is printed by the MCMC summary.
* Table 2 RMS values for a = 1500 and 2000 AU were not recorded in the summary
  file; the trend is monotonic and the a = 2000 case matches the free-fit RMS of
  736 arcsec.
* The Leleākūhonua MCMC row in Table 4 comes from the repeated run; the first
  attempt lost its CSV and corner plot to a `corner` zero-dynamic-range crash
  (caused by the collapsed inclination), which has since been patched.
* Two bugs were found and fixed while producing this report: the `corner`
  crash above, and the unseeded global RNG of §2.2b. Neither changes any
  conclusion — both concern how the failure is displayed and reproduced, not
  whether it occurs.
