# %% [markdown]
# # Lab 2.4 · Difference and ratio of medians
#
# Day 2 · Session 4 (Intervals for differences and ratios) · 25 min.
#
# Nizar Al-Khayyat asks the question behind the contract renewal: "Is contractor B slower than A, and by how much?" You answer twice, as a difference in hours and as a ratio, each with a bootstrap interval, and you check both against the truth.
#
# **AI policy.** AI-tutor: hints one step at a time, never the code.
#
# **Reference state.** `data/repairs.csv`. The study draws 200 repairs for each contractor with a seed from the tickets closed on time. Nothing from another lab is needed: the percentile interval is given.
#
# **Tasks**
# - [ ] 1 · Sample 200 repairs for each contractor (4')
# - [ ] 2 · Bootstrap the difference of medians (7')
# - [ ] 3 · Bootstrap the ratio of medians (5')
# - [ ] 4 · Compare with the truth; read 0 and 1 (4')
# - [ ] 5 · Coverage of the ratio interval over 300 studies (5')
# - [ ] ✱ Stretch · Do the difference of means on closed tickets with coverage over 1,000 studies

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

# %%
def percentile_interval(boot, level=0.95):
    a = (1 - level) / 2 * 100
    low, high = np.percentile(boot, [a, 100 - a])
    return float(low), float(high)


repairs = U.repairs()
closed = repairs[repairs["status"] == "closed"]
POOL = {c: closed.loc[closed["contractor"] == c, "repair_hours"].to_numpy() for c in ("A", "B")}
TRUE_DIFF = float(np.median(POOL["B"]) - np.median(POOL["A"]))
TRUE_RATIO = float(np.median(POOL["B"]) / np.median(POOL["A"]))

# %% [markdown]
# ## 1 · Sample 200 repairs for each contractor (4')

# %%
def draw_study(gen, n=200):
    return gen.choice(POOL["A"], size=n, replace=False), gen.choice(POOL["B"], size=n, replace=False)


a, b = draw_study(U.rng(81))
print(f"contractor A: n = {len(a)}, median {np.median(a):.2f} h")
print(f"contractor B: n = {len(b)}, median {np.median(b):.2f} h")
print(f"difference B - A: {np.median(b) - np.median(a):.2f} h; ratio B / A: {np.median(b) / np.median(a):.3f}")

# %% [markdown]
# ## 2 · Bootstrap the difference of medians (7')
#
# Two groups, two samples: resample **each group on its own**, compute both medians, take the difference. Repeat.
#
# ✏️ **Exercise** · Write `boot_medians(a, b, B, gen)` returning two arrays of length `B`: the resampled medians of `a` and of `b`.

# %%
def boot_medians(a, b, B, gen):
    # BEGIN SOLUTION
    ma = np.median(a[gen.integers(0, len(a), size=(B, len(a)))], axis=1)
    mb = np.median(b[gen.integers(0, len(b), size=(B, len(b)))], axis=1)
    return ma, mb
    # END SOLUTION


# %%
B = U.pick(2000, 500)
try:
    ma, mb = boot_medians(a, b, B, U.rng(82))
except NotImplementedError:
    ma, mb = U.reference("d2_4", "medians")
ma, mb = np.asarray(ma), np.asarray(mb)
U.keep("d2_4", "medians", [ma, mb])
diff_int = percentile_interval(mb - ma)
print(f"difference of medians, B - A: {np.median(b) - np.median(a):.2f} h, 95% interval {diff_int[0]:.2f} to {diff_int[1]:.2f}")
U.check(len(ma) == B and diff_int[0] < np.median(b) - np.median(a) < diff_int[1], "the interval contains the observed difference")

# %% [markdown]
# ## 3 · Bootstrap the ratio of medians (5')
#
# The same resamples, another comparison: divide instead of subtracting.
#
# ✏️ **Exercise** · Write `ratio_interval(ma, mb)`: the percentile interval of `mb / ma`.

# %%
def ratio_interval(ma, mb):
    # BEGIN SOLUTION
    return percentile_interval(mb / ma)
    # END SOLUTION


# %%
try:
    ratio_int = ratio_interval(ma, mb)
except NotImplementedError:
    ratio_int = U.reference("d2_4", "ratio_int")
U.keep("d2_4", "ratio_int", list(ratio_int))
print(f"ratio of medians, B / A: {np.median(b) / np.median(a):.3f}, 95% interval {ratio_int[0]:.3f} to {ratio_int[1]:.3f}")
print(f"in words: contractor B's typical repair takes between {ratio_int[0]:.2f} and {ratio_int[1]:.2f} times as long as contractor A's")
U.check(ratio_int[0] < np.median(b) / np.median(a) < ratio_int[1], "the interval contains the observed ratio")

# %% [markdown]
# ## 4 · Compare with the truth; read 0 and 1 (4')
#
# "No difference" is **0** for a difference and **1** for a ratio.
#
# ✏️ **Exercise** · Return two booleans: does the difference interval exclude 0, and does the ratio interval exclude 1?

# %%
def excludes_no_difference(diff_int, ratio_int):
    # BEGIN SOLUTION
    return not (diff_int[0] <= 0 <= diff_int[1]), not (ratio_int[0] <= 1 <= ratio_int[1])
    # END SOLUTION


# %%
try:
    ex = excludes_no_difference(diff_int, ratio_int)
except NotImplementedError:
    ex = U.reference("d2_4", "excludes")
U.keep("d2_4", "excludes", list(ex))
print(f"truth: difference {TRUE_DIFF:.2f} h, ratio {TRUE_RATIO:.3f}")
print(f"difference interval excludes 0: {ex[0]}; contains the truth: {diff_int[0] <= TRUE_DIFF <= diff_int[1]}")
print(f"ratio interval excludes 1: {ex[1]}; contains the truth: {ratio_int[0] <= TRUE_RATIO <= ratio_int[1]}")
U.check(ex[0] == ex[1], "the two readings agree: a difference of 0 and a ratio of 1 are the same statement")

# %% [markdown]
# **Look at.** The two intervals tell one story in two units. Hours suit the crew planner; a percentage suits the contract. Give the one the reader will act on.

# %% [markdown]
# ## 5 · Coverage of the ratio interval over 300 studies (5')
#
# ✏️ **Exercise** · Write `ratio_coverage(studies, gen)`: for each study, `draw_study(gen)`, `boot_medians` with 1,000 resamples, `ratio_interval`; return the share of intervals that contain `TRUE_RATIO`.

# %%
def ratio_coverage(studies, gen):
    # BEGIN SOLUTION
    hits = 0
    for _ in range(studies):
        x, y = draw_study(gen)
        lo, hi = ratio_interval(*boot_medians(x, y, 1000, gen))
        hits += lo <= TRUE_RATIO <= hi
    return hits / studies
    # END SOLUTION


# %%
STUDIES = U.pick(300, 80)
try:
    cov = ratio_coverage(STUDIES, U.rng(83))
except NotImplementedError:
    cov = U.reference("d2_4", "cov")
U.keep("d2_4", "cov", cov)
print(f"{STUDIES} studies: the ratio interval contains the true ratio {TRUE_RATIO:.3f} in {cov:.1%}")
U.check(cov > 0.90, "the bootstrap interval for a ratio of medians keeps its promise here")

# %% [markdown]
# ## ✱ Stretch · The difference of means, with 1,000 studies
#
# The outcome of the course asks for a coverage figure over 1,000 simulated samples. Do it for the difference of **mean** repair times, B - A, on tickets closed on time.

# %%
def stretch():
    # BEGIN SOLUTION
    gen, hits, studies = U.rng(84), 0, U.pick(1000, 100)
    truth = POOL["B"].mean() - POOL["A"].mean()
    for _ in range(studies):
        x, y = draw_study(gen)
        dx = y[gen.integers(0, 200, size=(1000, 200))].mean(axis=1) - x[gen.integers(0, 200, size=(1000, 200))].mean(axis=1)
        lo, hi = percentile_interval(dx)
        hits += lo <= truth <= hi
    print(f"difference of means: truth {truth:.2f} h; coverage over {studies} studies {hits / studies:.1%}")
    return hits / studies
    # END SOLUTION


try:
    U.keep("d2_4", "mean_diff_coverage", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the truth: difference {TRUE_DIFF:.2f} h and ratio {TRUE_RATIO:.3f}; ratio coverage {cov:.0%} over {STUDIES} studies.",
       "Not checked: whether B gets the harder jobs. Jobs are assigned by rota at Zulal, which is why the comparison is fair; in real data that must be argued, not assumed.")

# %% [markdown]
# ## Checkpoint
#
# 1. A ratio interval runs from 0.96 to 1.31. What do you tell Nizar?
#    <details><summary>Answer</summary>B may be anywhere from slightly faster to 31% slower. The data do not settle the direction; the estimate leans towards slower.</details>
# 2. The interval for A is 5.2 to 6.6 hours and for B 6.4 to 8.3. They overlap. Is there no difference?
#    <details><summary>Answer</summary>Overlap of two separate intervals is not a test. Build the interval for the difference itself.</details>
# 3. Why resample each contractor separately?
#    <details><summary>Answer</summary>The study fixed 200 repairs per contractor. Resampling the pooled 400 would let the group sizes vary, which the study did not.</details>
#
# ## Carry forward
#
# Day 3 asks the same question as a test and adds a threshold: how large a gap matters.
