# Project 2 reference solution — search for Phoebe-ring-like debris around Uranus and Neptune in AKARI FIS data

Status: exploratory reference solution (not benchmark-frozen). All numbers below are reproducible
from `geometry.py -> profile.py -> limits.py -> widths.py`, `stack2d.py [INJ] -> analyze2d.py -> variants.py`,
`nearfield.py` in this directory, run on the private data archive
`yehyu2004/astroagentbench-akari-rings` (commit 27eb5f9).

## Verdict

**No planet-bound diffuse emission is detected around Uranus or Neptune in any of the four FIS bands,
by any of the methods tried.** The strongest apparent midplane excess in any configuration is < 2.6 sigma
against the empirical null and in every such case the same feature is present in the off-target control.
The data do exclude a Phoebe-ring-like ring around **Uranus** at 3–7x below the scaled prediction in all
four bands; for **Neptune** the sensitivity only reaches the scaled prediction (UL/prediction 0.7–2.2),
so nothing can be said beyond "not brighter than a Phoebe analogue".

## Data

| Data | Use | Caveat |
|---|---|---|
| IRSA public AKARI FIS 6x6 deg all-sky tiles (fixstripe/sigma/nscan), l=315..350, b=0 | far-field (0.35–3 deg) ring search | 2–3 seasons averaged; moving sources (the planets) removed; a planet-bound ring exists in only one season -> intrinsic dilution x2–3 |
| Doi-san season-separated 41x41 (10') cutouts | epoch/position check, near-field (<5') search | 10 of 90 files are 0 bytes at the source; planet saturated (garbage 1e5–1e6 values, NaNs) in most Uranus frames |
| JPL Horizons (899/799, 399) | planet position, orbital-plane projection | epochs from CSV dates; Neptune_3 (2007-05) is **not in the CSV** |

## Geometry (geometry.py)

Horizons state vectors give the planet's heliocentric orbital plane normal n = r x v. Projected on the sky
the ring is **exactly edge-on** (axis ratio ~0.001) because the Earth lies in the planet's orbital plane to
within the Earth's own inclination — the ring is a straight line through the planet at PA = -1.76 deg
(Neptune) / ~0 deg (Uranus) w.r.t. the ecliptic. Uranus at elat -0.77 deg, Neptune at -0.19 to -0.25 deg.
The earlier "axis_ratio 0.00" was physical, not a bug. 1 AU at the planet = 2.86 deg (Uranus) / 1.91 deg (Neptune).

## Method A — orbital-plane vertical profiles (profile.py; Verbiscer+2009 logic)

Strip 0.35 < |s| < 1.2 deg along the plane (outside PSF, inside the Hill sphere), median profile in t
(perpendicular) with 0.04-deg bins, quadratic baseline fitted at |t| > 0.5 deg, midplane |t| < 0.12 deg.
Masks: NaN, nscan < 2, compact sources > 5 sigma above a 15-pixel median filter. Controls: identical
measurement shifted +-2.4 deg along the ecliptic. Stacks: per planet (N=3) and all six epochs.

3-sigma upper limits (MJy/sr, midplane, |t|<0.12 deg):

| band | Uranus UL | Neptune UL | Phoebe-like prediction U / N |
|---|---|---|---|
| N60 | 0.18 | 0.49 | 0.59 / 0.23 |
| WideS | 0.09 | 0.24 | 0.65 / 0.32 |
| WideL | 0.14 | 0.61 | 0.51 / 0.31 |
| N160 | 0.17 | 0.50 | 0.45 / 0.28 |

Prediction (limits.py): Phoebe ring 0.4 MJy/sr at 24 um, T=85 K -> edge-on tau_los = 1.6e-7, kept fixed;
grain temperature scaled as T = 85 K sqrt(9.5 AU / a) -> 60 K (Uranus), 48 K (Neptune).

Findings: (i) the midplane stack is consistent with the control stack everywhere; (ii) the noise does NOT
depend on the assumed ring thickness (widths.py, 0.04–0.3 deg) and does not fall as 1/sqrt(N) between
epochs -> it is systematic, large-scale background (zodiacal bands, cirrus), not pixel noise; (iii) the
Neptune WideL/N160 "+0.5 MJy/sr bump at t~+0.4 deg" seen in earlier exploratory runs is present in the
controls too -> background structure, not ring.

## Method B — planet-frame 2D coadd (stack2d.py; WISE-style)

Each epoch resampled onto a 6x6 deg (s,t) grid at 45"/pix, 2D polynomial background (order 3 in t,
2 in s) fitted outside the ring zone (|t|<0.3, |s|<2.5) and the 0.35-deg core, epochs coadded with
inverse-variance weights from the control scatter. Statistic: midplane excess E = <B(|t|<0.08)> -
<B(0.3<|t|<0.6)> in radial |s| bins 0.35–2.5 deg. Null: E evaluated with the trial midplane slid to
|t0| = 0.5–2.0 deg in the same image (where no planet-bound ring can be) -> robust sigma.

Result (analyze2d.py): all 60 (band x planet x radius) cells |S/N| < 2.6. The best cell, Neptune WideL
1.0–1.6 deg (+0.33, 2.5 sigma), has +0.17 in the control at the same place. Ring-zone (0.5–1.6 deg) limits
for a thin ring: Uranus WideS sigma = 0.055 -> 3-sigma UL 0.17 MJy/sr (peak brightness of a sigma_t=0.05
deg ring: /0.62 -> 0.27), Neptune WideS sigma = 0.11.

Variants (variants.py; 96 configurations: thickness 0.04–0.30 deg, reference bands, two backgrounds):
no configuration exceeds 2.6 sigma in the ring zone. The "running median along s" background is an
anti-detection filter (it removes any structure extended along the plane) and is listed only as a trap.
The one recurring negative feature (Uranus WideS, 0.35–0.6 deg, -0.09 MJy/sr) is a near-planet artefact
of the moving-source removal / destriping around the planet track, not a ring.

Injection test (stack2d.py 0.3): an edge-on ring of 0.3 MJy/sr peak, sigma_t = 0.05 deg, |s| = 0.5–1.5 deg
added to the raw on-target pixels is recovered at the expected window-diluted level (0.18–0.23 MJy/sr) with
S/N 3.4 (Uranus WideS), 2.5 (Neptune WideS), 3.2 (all six). So a full-brightness Phoebe analogue at Uranus
(0.65 MJy/sr) would have been a ~7-sigma line even in the season-averaged public map, and ~3 sigma after the
x2–3 season dilution. Neptune's analogue (0.32) would be marginal (~1.5–3 sigma).

## Method C — near field, Doi-san season-separated cutouts (nearfield.py)

Planet-on season minus mean of planet-off seasons, then radial profile and along-ecliptic vs
perpendicular sector means at 1.5–5' (20–160 R_p). Clean (unsaturated) cases only: Neptune_1 all bands,
Uranus_2 N60/WideL/WideS-order13.
- Normalised PSF-wing profiles of Uranus and Neptune agree (e.g. WideS 1->0.36->0.17->0.10 vs
  1->0.52->0.25->0.15 per 0.5' step); no epoch shows an extra shelf.
- Sector means at 2.5–5' are +5..+30 MJy/sr along the ecliptic and -5..-13 perpendicular: the
  perpendicular (scan-direction) deficit is the destriper/transient over-subtraction along the scan track,
  the along-ecliptic surplus is PSF wings + the same artefact's complement. Both are 10–50x larger than
  any plausible ring (<0.6 MJy/sr) -> the 10' cutouts have **no sensitivity** to a diffuse ring; they only
  serve to confirm planet positions/epochs and to show the known narrow rings (<8") are unresolved.
- Data quality: 10/90 files empty; saturation garbage (1e5–1e6 MJy/sr) not flagged as NaN in several
  frames (WideS Uranus_2 order12 season 1, N160 Uranus_2, Neptune_2 order13); "order12/order13" pairs of
  the same frame differ by factors of 2–400 in peak value -> processing versions, need Doi-san's definition.

## What would improve the search

1. Season-separated **large** (>=3x3 deg) images from Doi-san: removes the x2–3 dilution and allows the
   planet-off season to be used as a true same-sky background (kills the zodiacal/cirrus systematics that
   dominate now). This is the single largest gain (factor ~3–5 in sensitivity).
2. Saturn/Jupiter data as positive controls (Phoebe ring 0.4 MJy/sr at 24 um; expected ~1–2 MJy/sr in
   WideS if T~85 K) to demonstrate the pipeline recovers a known ring under AKARI systematics.
3. A zodiacal-light model (e.g. Kelsall-type fitted to the AKARI maps) instead of a polynomial baseline.

## Traps documented (for the benchmark)

- Planets are removed from the public maps as moving sources; "planet not found" is not "not observed".
- The ring is edge-on: a radial (azimuthally averaged) profile dilutes it by the ratio of the ring
  thickness to the circumference — use plane-aligned strips.
- Noise is systematic: 1/sqrt(N) stacking assumptions overstate sensitivity by ~2x here.
- Any background filter that operates along the plane direction (running median in s) removes the signal.
- Off-target controls at the same ecliptic latitude are mandatory; the largest apparent "excesses" in these
  fields (Neptune WideL/N160 bumps, Uranus near-planet deficit) are present in the controls.
- Season-averaged maps dilute a planet-bound ring by the number of seasons.
- The 10' cutouts cannot constrain a diffuse ring: PSF wings and destriping artefacts are 10–50x larger
  than the expected signal.
