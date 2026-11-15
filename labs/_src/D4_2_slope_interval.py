# %% [markdown]
# # Lab 4.2 · An interval for the slope
#
# Day 4 · Session 2 (Slopes with intervals) · 25 min.
#
# A regression summary prints a standard error next to every slope. It rests on an assumption: the points scatter around the line equally widely everywhere. You bootstrap the slope, which assumes nothing of the kind, compare the two standard errors, find out why they differ, and count which interval keeps its promise.
#
# **AI policy.** AI-tutor: hints one step at a time, never the code.
#
# **Reference state.** `data/metered_2000.csv`, loaded fresh. Nothing from lab 4.1 is needed.
#
# **Tasks**
# - [ ] 1 · Read the reported standard error of the slope (4')
# - [ ] 2 · Bootstrap the pairs: 2,000 slopes (8')
# - [ ] 3 · Compare the two standard errors and intervals (5')
# - [ ] 4 · Why they differ: the spread by household size (4')
# - [ ] 5 · Coverage of both intervals over 300 samples (4')
# - [ ] ✱ Stretch · Ask the library for a robust standard error and compare

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-201.git"
    if not Path("/content/ds-201").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-201"], check=True)
    os.chdir("/content/ds-201/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("zulal.py").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd
import zulal as U
import statsmodels.api as sm
np.set_printoptions(precision=3, suppress=True)
print("mode:", U.MODE)

# %%
def percentile_interval(boot, level=0.95):
    a = (1 - level) / 2 * 100
    low, high = np.percentile(boot, [a, 100 - a])
    return float(low), float(high)


m = U.metered()
x = m["household_size"].to_numpy(float)
y = m["consumption_l_day"].to_numpy(float)

# %% [markdown]
# ## 1 · Read the reported standard error of the slope (4')
#
# ✏️ **Exercise** · Fit the line with `sm.OLS(y, sm.add_constant(x)).fit()` and return `(slope, reported_se)`: `fit.params[1]` and `fit.bse[1]`.

# %%
def reported(x, y):
    # BEGIN SOLUTION
    fit = sm.OLS(y, sm.add_constant(x)).fit()
    return float(fit.params[1]), float(fit.bse[1])
    # END SOLUTION


# %%
try:
    slope, se_rep = reported(x, y)
except NotImplementedError:
    slope, se_rep = U.reference("d4_2", "reported")
U.keep("d4_2", "reported", [slope, se_rep])
int_rep = (slope - 1.96 * se_rep, slope + 1.96 * se_rep)
print(f"slope {slope:.2f} litres a day per person; reported standard error {se_rep:.3f}; reported 95% interval {int_rep[0]:.2f} to {int_rep[1]:.2f}")
U.check(abs(slope - np.polyfit(x, y, 1)[0]) < 1e-6 and 0.9 < se_rep < 1.4, "the library reports the same slope and a standard error of about 1.1")

# %% [markdown]
# ## 2 · Bootstrap the pairs: 2,000 slopes (8')
#
# The unit that was sampled is the household. A household is a **pair**: its size and its consumption stay together. Resample households with replacement and refit the slope each time.
#
# ✏️ **Exercise** · Write `boot_slopes(x, y, B, gen)`. Draw `idx = gen.integers(0, n, size=(B, n))`, take `xs = x[idx]`, `ys = y[idx]`, and compute all `B` slopes at once: covariance over variance along `axis=1`.

# %%
def boot_slopes(x, y, B, gen):
    # BEGIN SOLUTION
    idx = gen.integers(0, len(x), size=(B, len(x)))
    xs, ys = x[idx], y[idx]
    xc = xs - xs.mean(axis=1, keepdims=True)
    return (xc * (ys - ys.mean(axis=1, keepdims=True))).mean(axis=1) / (xc ** 2).mean(axis=1)
    # END SOLUTION


# %%
B = U.pick(2000, 500)
try:
    boot = np.asarray(boot_slopes(x, y, B, U.rng(141)))
except NotImplementedError:
    boot = U.reference("d4_2", "boot")
U.keep("d4_2", "boot", boot)
se_boot = float(boot.std(ddof=1))
int_boot = percentile_interval(boot)
print(f"{len(boot)} bootstrap slopes: standard deviation {se_boot:.3f}; 95% interval {int_boot[0]:.2f} to {int_boot[1]:.2f}")
U.check(abs(boot.mean() - slope) < 0.3 and 1.1 < se_boot < 1.8, "the bootstrap slopes centre on the fitted slope with a spread of about 1.4")

# %% [markdown]
# ## 3 · Compare the two standard errors and intervals (5')

# %%
ratio = se_boot / se_rep
U.keep("d4_2", "ratio", ratio)
U.table(["method", "standard error", "low", "high", "width"],
        [["reported by the library", se_rep, int_rep[0], int_rep[1], int_rep[1] - int_rep[0]],
         ["bootstrap of households", se_boot, int_boot[0], int_boot[1], int_boot[1] - int_boot[0]]], fmt="{:.2f}")
print(f"the bootstrap standard error is {ratio - 1:.0%} larger than the reported one")
U.check(1.1 < ratio < 1.5, "the bootstrap standard error is about a quarter larger")

# %% [markdown]
# ## 4 · Why they differ: the spread by household size (4')
#
# The reported standard error assumes one common spread of the points around the line. Look at the residuals: the distance of each household from the line.
#
# ✏️ **Exercise** · Write `residual_sd_by_size(x, y)`: fit the line, compute the residuals, and return a Series: the standard deviation of the residuals for each household size from 1 to 8.

# %%
def residual_sd_by_size(x, y):
    # BEGIN SOLUTION
    b1, b0 = np.polyfit(x, y, 1)
    res = pd.Series(y - (b0 + b1 * x))
    return res.groupby(x.astype(int)).std().loc[1:8]
    # END SOLUTION


# %%
try:
    sds = residual_sd_by_size(x, y)
except NotImplementedError:
    sds = pd.Series(U.reference("d4_2", "sds"))
    sds.index = sds.index.astype(int)
U.keep("d4_2", "sds", sds.to_dict())
print(sds.round(1).to_string())
U.check(sds.iloc[-1] > 1.7 * sds.iloc[0], "households of 8 scatter about twice as widely around the line as households of 1")

# %% [markdown]
# **Look at.** The spread grows with household size. The large households sit at the far end of the line, where a point has most leverage on the slope, and they are the noisiest. The formula averages the noise over all households and so understates how much the slope can swing. The bootstrap carries each household's own noise with it.

# %% [markdown]
# ## 5 · Coverage of both intervals over 300 samples (4')
#
# Which interval is honest? Draw 300 fresh samples of 2,000 from the population and count how often each interval contains the population slope.

# %%
pop = U.households()
PX, PY = pop["household_size"].to_numpy(float), pop["consumption_l_day"].to_numpy(float)
TRUE = float(np.polyfit(PX, PY, 1)[0])


def coverage(studies, gen):
    hit_rep = hit_boot = 0
    for _ in range(studies):
        rows = gen.choice(len(PX), size=2000, replace=False)
        sx, sy = PX[rows], PY[rows]
        s, se = reported(sx, sy)
        hit_rep += s - 1.96 * se <= TRUE <= s + 1.96 * se
        lo, hi = percentile_interval(boot_slopes(sx, sy, 500, gen))
        hit_boot += lo <= TRUE <= hi
    return hit_rep / studies, hit_boot / studies


STUDIES = U.pick(300, 60)
try:
    cov = coverage(STUDIES, U.rng(142))
except NotImplementedError:
    cov = U.reference("d4_2", "cov")
U.keep("d4_2", "cov", list(cov))
print(f"population slope {TRUE:.2f}. Over {STUDIES} samples: reported interval covers {cov[0]:.1%}, bootstrap interval covers {cov[1]:.1%} (promised: 95%)")
U.check(cov[1] > cov[0] and cov[1] > 0.9, "the bootstrap interval comes close to 95%; the reported one falls short")

# %% [markdown]
# ## ✱ Stretch · A robust standard error from the library
#
# Libraries can drop the equal-spread assumption too. Ask statsmodels for the `HC3` standard error and compare it with your bootstrap.

# %%
def stretch():
    # BEGIN SOLUTION
    fit = sm.OLS(y, sm.add_constant(x)).fit()
    robust = float(fit.get_robustcov_results("HC3").bse[1])
    print(f"reported {se_rep:.3f}, robust (HC3) {robust:.3f}, bootstrap {se_boot:.3f}")
    return robust
    # END SOLUTION


try:
    U.keep("d4_2", "hc3", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the truth: population slope {TRUE:.2f}; coverage over {STUDIES} samples: reported {cov[0]:.0%}, bootstrap {cov[1]:.0%}.",
       f"This sample: reported interval {int_rep[0]:.2f} to {int_rep[1]:.2f}, bootstrap interval {int_boot[0]:.2f} to {int_boot[1]:.2f}.",
       "Not checked: the slope's meaning. Both intervals are about the slope of size alone, which lab 4.3 shows to be partly temperature.")

# %% [markdown]
# ## Checkpoint
#
# 1. Why resample pairs and not x and y separately?
#    <details><summary>Answer</summary>A household's size and its consumption belong together. Resampling them separately destroys the relation and every slope comes out near zero.</details>
# 2. The reported standard error is smaller. Is it therefore better?
#    <details><summary>Answer</summary>No. It is smaller because it assumes equal spread, which is false here; its interval misses the truth more often than promised.</details>
# 3. If the spread were the same at every household size, how would the two standard errors compare?
#    <details><summary>Answer</summary>They would agree closely. A gap between them is itself a sign that the assumption fails.</details>
#
# ## Carry forward
#
# When a library's standard error and a bootstrap disagree, say so in the brief and report the wider one.
