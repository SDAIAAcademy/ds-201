# %% [markdown]
# # Lab 2.1 · Bootstrap a median
#
# Day 2 · Session 1 (The bootstrap idea) · 25 min.
#
# Nizar Al-Khayyat wants the typical repair time with an honest range around it. The median has no σ/√n. You hold one sample of 150 repairs and nothing else, resample it with replacement 2,000 times, and read an interval off the resampled medians. Then, because this is Zulal, you open the population and see whether the interval caught the truth.
#
# **AI policy.** Steps 1 to 3 are the day's first core computation: no assistant (AI-off). From step 4 on, the tutor may give hints (AI-tutor).
#
# **Reference state.** `data/repairs.csv`. The sample of 150 is drawn here with a seed. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · One sample of 150 repairs and its median (4')
# - [ ] 2 · One resample, by hand (4')
# - [ ] 3 · 2,000 resamples: the bootstrap distribution (7')
# - [ ] 4 · The percentile interval beside the truth (5')
# - [ ] 5 · Bootstrap spread against the real sampling spread (5')
# - [ ] ✱ Stretch · Count the coverage of the median's interval over 1,000 studies

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
np.set_printoptions(precision=3, suppress=True)
print("mode:", U.MODE)

# %% [markdown]
# ## 1 · One sample of 150 repairs and its median (4')

# %%
population = U.repairs()["repair_hours"].to_numpy()
sample = U.rng(51).choice(population, size=150, replace=False)
med = float(np.median(sample))
print(f"sample of {len(sample)} repairs: median {med:.2f} hours (mean {sample.mean():.2f})")

# %% [markdown]
# ## 2 · One resample, by hand (4')
#
# A **bootstrap resample** draws 150 values from the 150 you have, **with replacement**: some tickets appear twice or more, some not at all.
#
# ✏️ **Exercise** · Write `resample(v, gen)`: an array of `len(v)` values drawn from `v` with replacement.

# %%
def resample(v, gen):
    # BEGIN SOLUTION
    return gen.choice(v, size=len(v), replace=True)
    # END SOLUTION


# %%
gen = U.rng(52)
try:
    one = resample(sample, gen)
except NotImplementedError:
    one = U.reference("d2_1", "one")
U.keep("d2_1", "one", one)
distinct = len(np.unique(one))
print(f"one resample: {len(one)} values, {distinct} distinct; its median {np.median(one):.2f} hours")
U.check(len(one) == 150 and 70 < distinct < 115 and set(one) <= set(sample), "same size, drawn from the sample, with repeats (about 63% of the tickets appear)")

# %% [markdown]
# ## 3 · 2,000 resamples: the bootstrap distribution (7')
#
# ✏️ **Exercise** · Write `bootstrap(v, stat, B, gen)`: an array of `B` values of `stat`, one per resample. A fast way: `idx = gen.integers(0, len(v), size=(B, len(v)))`, then `stat(v[idx], axis=1)`.

# %%
def bootstrap(v, stat, B, gen):
    # BEGIN SOLUTION
    idx = gen.integers(0, len(v), size=(B, len(v)))
    return stat(v[idx], axis=1)
    # END SOLUTION


# %%
B = U.pick(2000, 500)
gen = U.rng(53)
try:
    boot = np.asarray(bootstrap(sample, np.median, B, gen))
except NotImplementedError:
    boot = U.reference("d2_1", "boot")
U.keep("d2_1", "boot", boot)
print(f"{len(boot)} bootstrap medians: from {boot.min():.2f} to {boot.max():.2f}; their standard deviation {boot.std(ddof=1):.3f}")
U.check(len(boot) == B and 0.2 < boot.std(ddof=1) < 1.2, "the resampled medians scatter around the sample median by about half an hour")

# %% [markdown]
# ## 4 · The percentile interval beside the truth (5')
#
# The 95% **percentile interval** runs from the 2.5th to the 97.5th percentile of the bootstrap values.
#
# ✏️ **Exercise** · Write `percentile_interval(boot, level=0.95)` returning `(low, high)`.

# %%
def percentile_interval(boot, level=0.95):
    # BEGIN SOLUTION
    a = (1 - level) / 2 * 100
    low, high = np.percentile(boot, [a, 100 - a])
    return float(low), float(high)
    # END SOLUTION


# %%
try:
    low, high = percentile_interval(boot)
except NotImplementedError:
    low, high = U.reference("d2_1", "interval")
U.keep("d2_1", "interval", [low, high])
TRUE = float(np.median(population))
print(f"sample median {med:.2f} h; 95% bootstrap interval {low:.2f} to {high:.2f} h; true median {TRUE:.2f} h")
U.check(low < med < high, "the interval contains the sample median")
print("the interval contains the truth" if low <= TRUE <= high else "the interval MISSES the truth: about 1 study in 20 does")
plt = U.plt()
fig, ax = plt.subplots()
ax.hist(boot, bins=30, color="#1f9e89")
for v, c, lab in ((low, "#e4572e", "interval"), (high, "#e4572e", None), (TRUE, "black", f"truth {TRUE:.1f}")):
    ax.axvline(v, color=c, linestyle="--" if c == "black" else "-", label=lab)
ax.set(xlabel="median of a resample, hours", ylabel="resamples", title=f"{len(boot)} bootstrap medians from one sample of 150")
ax.legend()
plt.show()

# %% [markdown]
# **Look at.** The histogram is lumpy: a median of 150 tickets can only take values that are in the sample, or halfway between two of them. That is normal for a bootstrapped median.

# %% [markdown]
# ## 5 · Bootstrap spread against the real sampling spread (5')
#
# The bootstrap imitates sampling from the population. Here you can do the real thing and compare.
#
# ✏️ **Exercise** · Write `real_spread(population, n, reps, gen)`: the standard deviation (`ddof=1`) of the medians of `reps` fresh samples of `n` drawn without replacement.

# %%
def real_spread(population, n, reps, gen):
    # BEGIN SOLUTION
    meds = np.array([np.median(gen.choice(population, size=n, replace=False)) for _ in range(reps)])
    return float(meds.std(ddof=1))
    # END SOLUTION


# %%
gen = U.rng(54)
try:
    real = real_spread(population, 150, U.pick(2000, 400), gen)
except NotImplementedError:
    real = U.reference("d2_1", "real")
U.keep("d2_1", "real", real)
print(f"standard error of the median: bootstrap, from one sample: {boot.std(ddof=1):.3f} h; real, from the population: {real:.3f} h")
U.check(0.5 < boot.std(ddof=1) / real < 2.0, "the bootstrap standard error is of the right size, from one sample alone")

# %% [markdown]
# **Look at.** The bootstrap is centred on the **sample** median, not on the truth: it cannot repair a sample that landed low or high. What it gets right is the **width**.

# %% [markdown]
# ## ✱ Stretch · Does the method keep its promise?
#
# One interval caught the truth, or did not. Count how often the method does: draw 1,000 fresh samples of 150 repairs from the population, build the 95% percentile interval for the median in each (1,000 resamples are enough), and count how often it contains the true median.

# %%
def stretch():
    # BEGIN SOLUTION
    gen = U.rng(55)
    studies = U.pick(1000, 150)
    hits = 0
    for _ in range(studies):
        s = gen.choice(population, size=150, replace=False)
        lo, hi = percentile_interval(bootstrap(s, np.median, 1000, gen))
        hits += lo <= TRUE <= hi
    print(f"coverage of the 95% percentile interval for the median: {hits} of {studies} studies, {hits / studies:.1%}")
    return hits / studies
    # END SOLUTION


try:
    U.keep("d2_1", "median_coverage", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the truth: interval {low:.2f} to {high:.2f} h; true median {TRUE:.2f} h ({'inside' if low <= TRUE <= high else 'outside'}).",
       f"Checked: bootstrap standard error {boot.std(ddof=1):.3f} against the real one {real:.3f}.",
       "Not checked in steps 1 to 5: one interval says nothing about how often the method is right. The stretch counts it for the median, lab 2.2 for the mean.")

# %% [markdown]
# ## Checkpoint
#
# 1. Why with replacement?
#    <details><summary>Answer</summary>Without replacement a resample of 150 from 150 is the sample itself, every time. Replacement is what makes resamples differ, the way real samples differ.</details>
# 2. You raise B from 2,000 to 200,000. Does the interval get narrower?
#    <details><summary>Answer</summary>No. B only smooths the picture. The width is set by the 150 tickets; only more tickets narrow it.</details>
# 3. The sample median is 0.4 hours below the truth. Is the bootstrap distribution centred on the truth?
#    <details><summary>Answer</summary>No, on the sample median. The bootstrap estimates the spread, not the miss.</details>
#
# ## Carry forward
#
# `bootstrap` and `percentile_interval` are the two functions of the week. Every later lab defines them again in a cell of its own, so nothing has to be carried.
