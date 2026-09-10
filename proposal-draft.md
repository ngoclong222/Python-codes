# Task proposal (draft for Terry to confirm): Searching for distant rings of Uranus and Neptune in AKARI far-infrared data

Prepared from the project document ("Project 2: Searching for New Rings of the Solar System's Gas Giants in AKARI Data"), a first look at the shared data, and Verbiscer, Skrutskie & Hamilton (2009, Nature 461, 1098). Everything marked **[Terry?]** needs your answer or correction; everything else is our reading of the material and should also be checked.

---

## 1. The work, as you would brief a colleague

Saturn has an enormous, very faint dust ring associated with its outer irregular moon Phoebe (128 to at least 207 Saturn radii, peak 0.4 MJy/sr at 24 um, normal optical depth ~2e-8). Verbiscer et al. found it by scanning regions far from Saturn with Spitzer/MIPS and looking for a diffuse band centred on Saturn's orbital plane, with off-target scans as controls. They closed the paper by predicting that "similar structures should also adorn the other gas giant planets". Uranus and Neptune both have irregular moons (Caliban, Sycorax; Nereid, Halimede, ...) that could feed such rings. Any ring of this kind would be optically invisible but should glow in the far infrared, with dust at roughly 50-60 K peaking near 50-90 um, right in the AKARI/FIS bands.

We have AKARI Far-Infrared Surveyor (FIS) all-sky-survey images, separated by survey season, around the positions of Uranus and Neptune at each epoch AKARI scanned them in 2006-2007. Because the planets move by degrees between seasons, each epoch has one season image containing the planet and one or two season images of the same sky without it. The job is: confirm where and when each planet appears in these images, characterise the planet's own far-infrared footprint (PSF, saturation, scan artefacts) so it can be separated from anything around it, estimate how bright a Phoebe-like ring around Uranus or Neptune would be at these wavelengths, compare that with what AKARI can actually detect, and then search the planet-subtracted, background-subtracted images for extended emission tied to the planet. The result is either a detection with a measured brightness profile, or a well-defended upper limit on the ring brightness and optical depth per band, with a clear statement of what AKARI can and cannot rule out.

**[Terry?]** Is this a fair summary of the scientific goal? The document says the rings "spread over a large area of the sky (a few degrees)"; our own scaling from the irregular-moon orbits gives a ring radius of 0.14-0.24 deg for Uranus (Caliban, Sycorax) and 0.07-0.2 deg for Neptune (Nereid, Halimede). Which size do you have in mind, and why?

## 2. The data: link + rights

- `akari_uranus_neptune` (Google Drive, images from Doi-san): 89 FITS cutouts, 41x41 pixels, 14.63"/pixel (10 arcmin on a side), TAN WCS, one file per planet epoch x band (N60, WideS, WideL, N160) x survey season (1-3), with WideS also in two processing "orders" (12, 13). Five files are empty (0 bytes) and three failed to download from Drive (Uranus_3 WideS season 2/3).
- `AKARI-FIS_Planets.csv`: 11 planet passages (5 Neptune, 6 Uranus) with date/time, RA/Dec, detector flags, reset interval, moon-ghost flags, and model flux densities in the four bands.
- Verbiscer et al. 2009 (Nature) as the method reference.

**[Terry?]**
- Rights: these are Doi-san's season-separated processed images, not the public IRSA all-sky maps. Can they be released publicly (e.g. CC BY 4.0 on a Hugging Face dataset), or at least redistributed inside a benchmark container? If not, the task has to be rebuilt on the public AKARI FIS all-sky maps (which merge all seasons and so lose the planet-on / planet-off pairing). This is the one hard requirement.
- Units and processing: are the pixel values MJy/sr from the standard all-sky map pipeline (Doi et al. 2015)? What is "order12" vs "order13"? Are seasons 1/2/3 the standard AKARI survey seasons?
- Field size: 10 arcmin is only +/-160 Uranus radii and +/-260 Neptune radii, i.e. inside the Caliban/Sycorax and Nereid orbits. Can Doi-san provide larger cutouts (1-2 deg on a side, same season separation) around each planet epoch? Without them the search can only set limits inside the orbits of the irregular moons.
- Epoch matching: the CSV lists 11 passages but there are only 3 Uranus and 3 Neptune image positions (several passages on the same day are 1.6 h apart and fall in the same cutout). Please confirm which CSV rows correspond to Uranus_1/2/3 and Neptune_1/2/3.
- Jupiter and Saturn images: the document says these come later. We propose to build the task on Uranus and Neptune first and keep Jupiter/Saturn for a follow-up (Saturn's Phoebe ring is known, which would make it a good calibration case rather than a search).

## 3. What "done well" looks like

Our proposal for the checks, in the style of a student review. **[Terry?]** please correct, add, or remove.

- Planet identification: for every planet epoch and band, the planet is found in exactly one season image, at the position predicted by the ephemeris for the scan time, within the FIS beam (the peak should agree with JPL Horizons to better than a pixel or two). The season images without the planet show only background at that position. Reported peak/integrated brightness of the planet should be consistent with the model flux densities in the CSV where the detector was not saturated.
- Recognising the planet's footprint: Uranus is saturated in most planet-season images (NaN holes and pixel values of 1e5-3e6 MJy/sr), Neptune in some. A good job identifies which epochs/bands are usable, states why, and does not treat saturation residue, the scan-direction tail, or the PSF wings as ring emission.
- Ring brightness estimate: an equilibrium dust temperature for Uranus (~60 K) and Neptune (~48 K) distances, the corresponding blackbody surface brightness for a "solid wall" of grains in each FIS band, and the brightness expected for a Phoebe-like optical depth (~2e-7 along the line of sight). We get ~0.5-0.6 MJy/sr for Uranus and ~0.3 MJy/sr for Neptune in WideS. This should be compared with the actual pixel noise measured in the planet-free season images (and with the published AKARI FIS all-sky-map sensitivities), giving the minimum detectable optical depth after averaging over the expected ring area.
- Search: planet-free season images subtracted from the planet season image (or an equivalent background model), the planet's PSF/saturation region masked or modelled, then a profile of residual brightness versus distance from the planet, and versus distance from the planet's orbital plane (the Phoebe-ring signature is a band centred on the planet's orbital plane, double-peaked for an inclined source moon).
- Result: per band and per planet, either a detection (brightness profile, extent, significance, and evidence that it is fixed on the sky and not a scan artefact) or an upper limit on surface brightness and optical depth at stated radii, with the limitations of the 10 arcmin field stated honestly.
- Classic subtle failures we expect: mistaking the saturated core's ringing/ghost for structure; using the season-combined public map, where the planet is smeared over all seasons; forgetting that the planet moves between the 1.6 h passages in one season; quoting an optical depth without a temperature or emissivity assumption; treating a positive residual in a single band as a detection without the planet-free control.

Independent checks available: JPL Horizons ephemerides for planet positions; the CSV model flux densities; the planet-free season images as a null control; published AKARI FIS sensitivities; the Verbiscer et al. Phoebe-ring numbers as the scaling anchor.

## 4. A reference result

**[Terry?]** Has anyone (you, Doi-san, a previous student) already done this search on these images? If yes, please share the numbers or plots (they are used only to calibrate the checks and are never shown to anyone doing the task). If not, we will produce a maintainer reference solution first and ask you to confirm it blind (we would send you only the object list, positions and epochs, and compare afterwards).

## 5. Two time estimates

**[Terry?]**
- You: ?
- A good graduate student seeing the data for the first time: ? (our guess: 2-4 weeks, most of it on the saturation/PSF handling and on deciding what the 10 arcmin field can and cannot constrain)

## 6. Why is this hard

Our reading; **[Terry?]** please add your own.

- There is no recipe: Verbiscer et al. designed dedicated scans far from Saturn; here the geometry is fixed by the all-sky survey, the planet sits in the middle of a small field and is saturated, so the searcher has to decide how much of the field is usable at all.
- The brightness estimate needs modelling (temperature, emissivity, optical depth, path length through the ring), and the comparison with the detection limit requires measuring the noise properly on the planet-free images, not reading a single-pixel number off a table.
- The tempting shortcut is to look at the planet-season image alone, see extended emission around the saturated planet (PSF wings, scan tail, saturation ghosts), and call it a ring. The control images and the ephemeris are what separate a real result from an artefact.
- The honest outcome is very likely an upper limit, and writing a correct upper limit (area-averaged noise, assumed ring geometry, stated temperature) is the expert-judgment part; a solver that only measures things without stating what it cannot rule out has not finished.

Field: planetary science / far-infrared survey data analysis.

---

## Summary of what we need from Terry

1. Permission/route to redistribute Doi-san's images (or confirmation to fall back to public maps).
2. Larger season-separated cutouts (1-2 deg) if possible, and the three missing/empty files.
3. Units, meaning of order12/13, season definition, and the CSV-row-to-image mapping.
4. Any existing reference result.
5. Your two time estimates and your own view of the hard part.
6. Whether this summary reads like the project you have in mind.
