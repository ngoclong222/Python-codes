# Suggestions for improving the Keplerian orbit fit

## 1. What is `N_RESTARTS_MAIN` and why does it matter?

The fitting uses the **Nelder–Mead** algorithm (`scipy.optimize.minimize` with `method="Nelder-Mead"`).
Nelder–Mead is a derivative-free optimizer: it walks a simplex of `N+1` points through parameter space, shrinking or expanding the simplex until it finds a minimum.

The catch: Nelder–Mead is **local**. If the objective landscape has many valleys (local minima), the solver stops at whichever valley contained its starting simplex. It cannot jump out to a better valley on its own.

`N_RESTARTS_MAIN` is the number of independent Nelder–Mead runs, each starting from a different random initial simplex. The code keeps the result with the lowest objective value.

- **Why more restarts help:** each restart is a new lottery ticket. If your objective has 10 plausible minima and you only start 30 times, you may miss the deepest one. With 100–200 starts you are far more likely to find it.
- **Cost:** runtime grows roughly linearly with `N_RESTARTS_MAIN`. If one restart takes time `T`, then 200 restarts take about `200T`.
- **Diminishing returns:** once the best result stops changing as you add restarts, you have probably found the minimum that is reachable from your initial-guess distribution.

In short: `N_RESTARTS_MAIN` is not part of the physics; it is a search-budget knob. With a degenerate problem like this one, it is one of the cheapest ways to reduce the chance of being trapped in a poor local minimum.

---

## 2. Why the current fit is hard

The code fits a 6-parameter Keplerian orbit to only three astrometric detections (IRAS, AKARI_1, AKARI_2). Each detection gives an RA and a Dec, so there are 6 measurements for 6 parameters. In a perfect world this would be just enough. In practice:

- The three points span only ~2° on the sky and ~24 years in time.
- The assumed 5 arcsec astrometric noise is tiny compared with the ~740 arcsec residuals, so the model is not a good description of the data.
- `a` (semimajor axis) and `e` (eccentricity) are strongly correlated: you can raise `a` and also raise `e` so that perihelion distance `q = a(1-e)` and the observed distances stay roughly the same.

Because of this degeneracy, the objective landscape has a long, shallow valley rather than a single sharp minimum. Different starting guesses can slide to very different points along that valley.

---

## 3. Suggested improvements and the reasons behind them

### 3.1 Warm-start from a fixed-`a` grid

**What to do:**
1. Run fixed-`a` fits for a dense grid, e.g. `a = 200, 350, 700, 1000, 1500, 2000, 3000, 5000 AU`.
2. Record the best-fit `(e, i, Ω, ω, M)` for each `a`.
3. Pick the `a` with the lowest RMS residual.
4. Use that full 6-element vector as the initial guess for the free-`a` fit.

**Why it helps:**
Instead of starting the free-`a` optimizer from a random point, you start it from the best known point on the `a`–residual curve. This is much better than hoping 30 random starts find the same valley.

---

### 3.2 Tighten the allowed range for `a`

**What to do:**
Change the random initial `log a` from

```python
log_a_init = rng.uniform(np.log(50.0), np.log(10000.0))
```

to something like

```python
log_a_init = rng.uniform(np.log(300.0), np.log(3000.0))
```

**Why it helps:**
A broad range sounds safe, but it mostly wastes restarts on physically implausible regions (e.g., `a < 100 AU` or `a > 10,000 AU`). A tighter range focuses the search where Planet Nine-like objects are expected and reduces the chance of the optimizer chasing spurious high-`a`, near-parabolic orbits.

---

### 3.3 Increase `N_RESTARTS_MAIN`

**What to do:**
Set `N_RESTARTS_MAIN = 100` or `200` instead of `30`.

**Why it helps:**
With only 30 random starts in a 6-dimensional degenerate space, it is easy to miss the deepest minimum. More restarts improve the chance that at least one start lands near the true global minimum. This is the simplest change and does not require rewriting the model.

---

### 3.4 Use a grid of initial `a` values plus random angles

**What to do:**
Instead of drawing `log a` completely at random, create a regular grid of `log a` values (say 15 values from `log(300)` to `log(3000)`). For each grid value, generate a few random initial guesses for the other five parameters.

**Why it helps:**
The biggest degeneracy is along the `a` direction. A grid guarantees that every plausible `a` is explored. Randomizing the angles then explores the other directions for each `a`. This is more efficient than pure random sampling in a space where one parameter matters more than the others.

---

### 3.5 Add a global optimization stage

**What to do:**
Before Nelder–Mead, run `scipy.optimize.differential_evolution` or `scipy.optimize.basinhopping` with wide bounds. Then polish the best candidate with Nelder–Mead.

**Why it helps:**
Differential evolution and basin hopping are designed to escape local minima. They are more expensive than Nelder–Mead, but they are far better at finding a good starting point in a rugged landscape. Nelder–Mead then acts as a fast polisher.

---

### 3.6 Fit more data points

**What to do:**
Include additional reliable positions from the ephemeris file, not just the three special detections. Each extra RA/Dec pair adds two more constraints.

**Why it helps:**
The fundamental problem is too few constraints for too many free parameters. More data breaks the `a`–`e` degeneracy and forces the orbit to follow the actual observed track over many years. This is the single most effective way to get a unique, accurate orbit, provided the extra points are real and correctly matched to the object.

---

### 3.7 Apply a tighter upper bound on eccentricity

**What to do:**
Change

```python
0.99 * sigmoid(optimizer_params[1])
```

to

```python
0.90 * sigmoid(optimizer_params[1])
```

or another physically motivated upper limit.

**Why it helps:**
Without a tighter bound, the optimizer can wander into extremely eccentric orbits (`e ≈ 0.95`) that are mathematically allowed but physically unlikely for a distant solar-system object. A reasonable bound keeps the fit in the regime where the Keplerian model is meaningful.

---

### 3.8 Run the free-`a` fit from multiple fixed-`a` warm starts and compare

**What to do:**
Take the best-fit parameters from several fixed-`a` cases (e.g., `a = 700`, `a = 1000`, `a = 1500`, `a = 2000`) and use each as a warm start for an independent free-`a` run. Keep the result with the lowest RMS residual.

**Why it helps:**
This directly tests whether the current free-`a` best fit (`a ≈ 2383 AU`) is just a local minimum. If the `a = 5000 AU` warm start produces a much lower residual, then the previous result was closer to the global minimum.

---

## 4. What to expect

Even with all of these improvements, the fit may still be uncertain because:

- The three detections may not all belong to the same object.
- The astrometric uncertainty may be much larger than 5 arcsec.
- A purely Keplerian model may not be adequate (e.g., perturbations from the known giant planets).

The most honest interpretation is: **the current data do not uniquely determine a Keplerian orbit.** Improving the optimizer helps you find the best possible Keplerian orbit, but it cannot create information that is not in the data.
