# %% [markdown]
# # Lab 2.2 · Count the coverage
#
# Day 2 · Session 2 (Coverage is a testable claim) · 25 min.
#
# "95% confidence" is a promise about a method: used again and again, it should catch the truth in about 95 studies of 100. At Zulal the truth is on file, so you can count. You run 500 studies of 40 repairs, build two intervals for the mean in each, and count how often each one contains the true mean. Then you change the sample size, and then you leave the late-entry tickets in.
#
# **AI policy.** AI-tutor: hints one step at a time, never the simulation.
#
# **Reference state.** `data/repairs.csv`. Steps 1 to 3 use the 11,988 tickets closed on time; step 4 uses all 12,000. Nothing from lab 2.1 is needed: the two bootstrap functions are given below.
#
# **Tasks**
# - [ ] 1 · Two intervals for the mean from one study of 40 (6')
# - [ ] 2 · 500 studies: count the coverage of each method (8')
# - [ ] 3 · The same count with 200 repairs (4')
# - [ ] 4 · Leave the late-entry tickets in and count again (4')
# - [ ] 5 · State what 95% promised and what it delivered (3')
# - [ ] ✱ Stretch · Bootstrap the maximum repair time and count its coverage

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
from scipy import stats
np.set_printoptions(precision=3, suppress=True)
print("mode:", U.MODE)

# %%
def bootstrap(v, stat, B, gen):
    idx = gen.integers(0, len(v), size=(B, len(v)))
    return stat(v[idx], axis=1)


def percentile_interval(boot, level=0.95):
    a = (1 - level) / 2 * 100
    low, high = np.percentile(boot, [a, 100 - a])
    return float(low), float(high)


repairs = U.repairs()
closed = repairs.loc[repairs["status"] == "closed", "repair_hours"].to_numpy()
everything = repairs["repair_hours"].to_numpy()
MU = float(closed.mean())
print(f"tickets closed on time: {len(closed):,}; their true mean {MU:.3f} hours")

# %% [markdown]
# ## 1 · Two intervals for the mean from one study of 40 (6')
#
# The **t interval**: mean ± t × s/√n, where `t = stats.t.ppf(0.975, n - 1)` (about 2.02 for n = 40). The **bootstrap interval**: the percentile interval of 1,000 resampled means.
#
# ✏️ **Exercise** · Write `t_interval(v)` returning `(low, high)`.

# %%
def t_interval(v):
    # BEGIN SOLUTION
    n = len(v)
    half = stats.t.ppf(0.975, n - 1) * v.std(ddof=1) / np.sqrt(n)
    return float(v.mean() - half), float(v.mean() + half)
    # END SOLUTION


# %%
gen = U.rng(61)
study = gen.choice(closed, size=40, replace=False)
try:
    ti = t_interval(study)
except NotImplementedError:
    ti = U.reference("d2_2", "ti")
U.keep("d2_2", "ti", list(ti))
bi = percentile_interval(bootstrap(study, np.mean, 1000, gen))
print(f"one study of 40: mean {study.mean():.2f} h")
print(f"  t interval         {ti[0]:.2f} to {ti[1]:.2f}")
print(f"  bootstrap interval {bi[0]:.2f} to {bi[1]:.2f}")
print(f"  true mean {MU:.2f}")
U.check(ti[0] < study.mean() < ti[1] and abs((ti[0] + ti[1]) / 2 - study.mean()) < 1e-9, "the t interval is symmetric around the sample mean")

# %% [markdown]
# **Look at.** The t interval is symmetric by construction. The bootstrap interval is not: it follows the skew of the sample.

# %% [markdown]
# ## 2 · 500 studies: count the coverage of each method (8')
#
# ✏️ **Exercise** · Write `coverage(pool, truth, n, studies, gen)`. For each study: draw `n` values from `pool` without replacement, build the t interval and the bootstrap interval (1,000 resamples of the mean), and note whether each contains `truth`. Return the two shares `(t_share, bootstrap_share)`.

# %%
def coverage(pool, truth, n, studies, gen):
    # BEGIN SOLUTION
    hit_t = hit_b = 0
    for _ in range(studies):
        v = gen.choice(pool, size=n, replace=False)
        lo, hi = t_interval(v)
        hit_t += lo <= truth <= hi
        lo, hi = percentile_interval(bootstrap(v, np.mean, 1000, gen))
        hit_b += lo <= truth <= hi
    return hit_t / studies, hit_b / studies
    # END SOLUTION


# %%
STUDIES = U.pick(500, 120)
try:
    c40 = coverage(closed, MU, 40, STUDIES, U.rng(62))
except NotImplementedError:
    c40 = U.reference("d2_2", "c40")
U.keep("d2_2", "c40", list(c40))
print(f"{STUDIES} studies of 40 repairs: t interval covers {c40[0]:.1%}, bootstrap interval covers {c40[1]:.1%} (promised: 95%)")
U.check(0.84 < c40[0] < 0.97 and 0.83 < c40[1] < 0.97, "both methods land a little under 95% at n = 40 on skewed data")

# %% [markdown]
# **Look at.** Both land a point or two under 95%, about as far as the counting error of step 3 allows. With 40 skewed values the long right tail is often thin in the sample, the mean runs low and the interval is short on the high side. The promise is nearly kept here. Step 4 shows a case where it is not.

# %% [markdown]
# ## 3 · The same count with 200 repairs (4')

# %%
try:
    c200 = coverage(closed, MU, 200, STUDIES, U.rng(63))
except NotImplementedError:
    c200 = U.reference("d2_2", "c200")
U.keep("d2_2", "c200", list(c200))
print(f"{STUDIES} studies of 200 repairs: t {c200[0]:.1%}, bootstrap {c200[1]:.1%}")
se_of_share = np.sqrt(0.95 * 0.05 / STUDIES)
print(f"a count over {STUDIES} studies is itself uncertain: a true 95% would show as 95% give or take {2 * se_of_share:.1%}")
U.check(c200[0] > 0.90 and c200[1] > 0.90, "with 200 repairs both methods come close to 95%")

# %% [markdown]
# ## 4 · Leave the late-entry tickets in and count again (4')
#
# Now the pool is all 12,000 repairs, including the twelve tickets of 600 to 2,100 hours, and the truth is the mean of all of them.

# %%
MU_ALL = float(everything.mean())
try:
    call = [coverage(everything, MU_ALL, n, STUDIES, U.rng(64 + n)) for n in (40, 200)]
except NotImplementedError:
    call = U.reference("d2_2", "call")
U.keep("d2_2", "call", [list(c) for c in call])
U.table(["pool", "n", "t interval", "bootstrap"],
        [["closed on time", 40, c40[0], c40[1]], ["closed on time", 200, c200[0], c200[1]],
         ["all, with 12 late-entry tickets", 40, call[0][0], call[0][1]], ["all, with 12 late-entry tickets", 200, call[1][0], call[1][1]]], fmt="{:.1%}")
U.check(call[0][0] < 0.88 and call[1][0] < 0.88, "with rare extreme tickets in the population, both methods fail badly, and more data does not rescue them")

# %% [markdown]
# **Look at.** One ticket in a thousand carries a tenth of all the hours. Most samples contain none of them, so most samples cannot know the true mean, and no interval built from the sample alone can either. A bigger sample makes the interval narrower around the wrong value until it finally includes a late ticket.

# %% [markdown]
# ## 5 · State what 95% promised and what it delivered (3')
#
# ✏️ **Exercise** · Complete the sentence for the t interval at n = 40 on tickets closed on time. Return the delivered coverage as a whole percentage (an integer).

# %%
def delivered():
    # BEGIN SOLUTION
    return round(c40[0] * 100)
    # END SOLUTION


# %%
try:
    d = delivered()
except NotImplementedError:
    d = U.reference("d2_2", "delivered")
U.keep("d2_2", "delivered", d)
print(f"\"The method promised to contain the true mean in 95 studies of 100. On skewed repair times with 40 tickets it did so in about {d} of 100.\"")
U.check(d == round(c40[0] * 100), "the delivered coverage is the count from step 2")

# %% [markdown]
# ## ✱ Stretch · Where the bootstrap fails outright
#
# Bootstrap the **maximum** repair time among tickets closed on time, from samples of 200, and count how often the interval contains the true maximum.

# %%
def stretch():
    # BEGIN SOLUTION
    gen, hits, true_max, studies = U.rng(69), 0, closed.max(), U.pick(300, 80)
    for _ in range(studies):
        v = gen.choice(closed, size=200, replace=False)
        lo, hi = percentile_interval(bootstrap(v, np.max, 1000, gen))
        hits += lo <= true_max <= hi
    print(f"coverage of the bootstrap interval for the maximum: {hits / studies:.1%} (true maximum {true_max:.1f} h)")
    # A resample can never hold a value larger than the sample's own maximum, so the interval cannot reach above it.
    return hits / studies
    # END SOLUTION


try:
    U.keep("d2_2", "max_coverage", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the truth: coverage of the true mean over {STUDIES} studies, by method, sample size and pool (the table of step 4).",
       f"The count itself has an error of about ±{2 * se_of_share:.0%}.",
       "Not checked: the median. Its bootstrap interval is counted in lab 2.4 as part of a ratio.")

# %% [markdown]
# ## Checkpoint
#
# 1. One study gives the interval 7.1 to 10.9 hours. Is there a 95% chance that the true mean is inside?
#    <details><summary>Answer</summary>The true mean is a fixed number: it is inside or it is not. 95% describes the method over many studies, and you have just seen that even that figure has to be earned.</details>
# 2. Why did 200 tickets help for tickets closed on time and not for the full pool?
#    <details><summary>Answer</summary>Ordinary skew is visible in a sample of 200. A ticket that occurs once in a thousand is not: the sample has no information about it.</details>
# 3. Why can a bootstrap interval for the maximum never be right?
#    <details><summary>Answer</summary>No resample contains a value above the sample's own maximum, so the interval cannot extend to a larger true maximum.</details>
#
# ## Carry forward
#
# The capstone asks for a coverage check of your own interval. This loop, 500 studies and a count, is that check.
