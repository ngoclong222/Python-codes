# Task proposal (draft for Terry to confirm): A search for Planet Y in IRAS and AKARI data

Prepared from the project document ("Project 1: A Search for Planet Y with IRAS and AKARI Data"), Siraj, Chyba & Tremaine (2025, arXiv:2508.14156, "Planet Y"), Phan et al. (2025, PASA, "A Search for Planet Nine with IRAS and AKARI Data") and a quick look at the catalogue access. Items marked **[Terry?]** need your answer.

---

## 1. The work, as you would brief a colleague

Siraj et al. (2025) measure a warp of the mean plane of the distant Kuiper belt (a = 80-400 AU) and show with n-body simulations that the most likely cause is an unseen planet of Mercury-to-Earth mass at a ~ 100-200 AU with inclination >~ 10 deg ("Planet Y"). This is a very different object from Planet Nine (5-10 M_earth, 400-800 AU): closer, much smaller, colder and faster-moving on the sky.

Phan et al. (2025) searched for Planet Nine by pairing sources in the IRAS Point/Faint Source Catalogues (1983) with sources in the AKARI Monthly Unconfirmed Source List (2006) that are consistent with the expected 23-year orbital motion and flux of Planet Nine (hourly confirmation but no monthly confirmation in AKARI, flux/colour consistency, galactic-plane and known-source rejection), then inspected images of the surviving pairs.

The assignment: redo this for Planet Y. Starting from the Siraj et al. mass, distance and inclination ranges, derive the expected far-infrared flux of Planet Y in the IRAS 60/100 um and AKARI 65/90/140/160 um bands as a function of mass and distance (including the assumptions about radius, albedo/temperature and any internal heat), derive the expected sky motion between 1983 and 2006 (orbital motion, parallax and their range over the inclination range), decide in what part of the (mass, distance) plane Planet Y is detectable by both surveys at all, and then build the IRAS x AKARI-MUSL pair search with selection criteria appropriate to those numbers. Deliver the candidate list with the criteria and their per-step counts, an image-inspection tool (auto-download IRIS and AKARI cutouts by coordinate), and an honest statement of what part of Planet Y parameter space the search does and does not cover.

**[Terry?]** Is this the scope you intend? In particular: is the main deliverable the candidate list, or the detectability analysis + candidate list?

## 2. The data: link + rights

- IRAS PSC v2 and FSC v2 (public, IRSA/VizieR). Fine to redistribute.
- AKARI-MUSL: Phan et al. write it "will be made available upon reasonable request"; it is not on the public DARTS/ISAS catalogue pages. **[Terry?]** Can the MUSL (or the subset the task needs, e.g. all sources with hourly-but-no-monthly confirmation plus the columns used) be redistributed publicly for the task, e.g. on Hugging Face under an open licence? Without this the task cannot be built on MUSL and would have to fall back to the public AKARI FIS Bright Source Catalogue, which excludes movers and so defeats the method.
- IRIS (IRAS) and AKARI FIS all-sky map cutouts (public, IRSA) for image inspection.

## 3. What "done well" looks like

Our proposal; **[Terry?]** please correct, add, or remove.

- Detectability: the expected fluxes and motions as a table over the Siraj et al. ranges. Our own quick numbers (blackbody, equilibrium temperature 278 K/sqrt(d), no internal heat, A=0): at 150 AU an Earth-mass body is ~23 K and gives ~12 mJy at 90 um and ~50 mJy at 160 um; a Mercury-mass body ~2-7 mJy; only at <~100 AU, >~1 M_earth, or with substantial internal heat (T >~ 35-40 K) does the flux reach the ~0.2 Jy limits of IRAS-FSC and AKARI-MUSL. A good result states this clearly and defines the searchable corner of parameter space instead of pretending the whole Siraj et al. range is covered.
- Motion: at 100/150/200 AU the 23-year orbital motion is ~8.3/4.5/2.9 deg and the parallax amplitude ~34/23/17 arcmin, so the pair-search window and the "hourly yes / monthly no" logic differ from the Planet Nine case (42-70 arcmin). Copying the Phan et al. window silently misses Planet Y.
- Pair search: explicit criteria (flux quality, detection limits, known-source rejection, galactic plane/bulge cut, flux upper limits appropriate to Planet Y, flux-ratio and colour consistency, angular-separation window), the number of sources surviving each step, and the final pair list with positions, fluxes, separations and implied distances.
- Controls: the Phan et al. Planet Nine candidate (their 13 pairs / 1 good candidate) should be recoverable when the Planet Nine parameters are plugged into the same pipeline; this is a positive control that shows the pipeline works. Known moving objects (bright asteroids, comets) in MUSL should be rejected or flagged.
- Image inspection tool: takes coordinates, fetches IRIS and AKARI cutouts, displays both epochs with the two catalogue positions marked; run on every final candidate.
- Honest interpretation: for each surviving pair, the implied distance/mass from flux and motion, and why it is or is not a viable Planet Y.

## 4. A reference result

**[Terry?]** Has anyone in the group already run a Planet Y (or <500 AU) version of the Phan et al. search? The Planet Nine paper mentions the <500 AU search as a follow-up study. If numbers exist (counts per criterion, final pairs) they would be the calibration for the checks; otherwise we build a reference solution and ask you to confirm it blind.

## 5. Two time estimates

**[Terry?]**
- You: ?
- A good graduate student seeing the data for the first time: ? (our guess: 2-4 weeks; the physics of the flux/motion estimate is fast, the catalogue handling and image tool take most of the time)

## 6. Why is this hard

Our reading; **[Terry?]** please add your own.

- The obvious approach (reuse the Planet Nine criteria) gives a confident but wrong answer: the separation window, flux upper limit and colour expectation are all set by the Planet Nine mass/distance, and Planet Y is ~4-10x closer, ~10-100x fainter and moves ~5-10x faster.
- The detectability question has a negative-looking answer for most of the parameter space; it takes judgment to turn that into a well-defined, defensible search of the reachable corner rather than either giving up or overclaiming.
- Cross-catalogue reasoning across two surveys with different bands, beams, epochs and confirmation logic; MUSL is large (~1e6 sources) and dominated by artefacts and real movers.
- The candidate list has no ground truth; quality is judged by the internal consistency of the criteria, the recovered positive control, and the per-pair physical interpretation.

Field: planetary science / outer solar system / far-infrared survey catalogues.

---

## Summary of what we need from Terry

1. Whether AKARI-MUSL (or a subset) can be redistributed for the task. This is the hard blocker.
2. Scope: detectability analysis + candidate list, or candidate list only.
3. Any existing <500 AU / Planet Y search results in the group.
4. Time estimates and your view of the hard part.
5. Whether this reads like the project you have in mind.
