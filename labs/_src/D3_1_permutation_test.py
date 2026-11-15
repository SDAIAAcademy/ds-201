# %% [markdown]
# # Lab 3.1 · Shuffle the contractor labels
#
# Day 3 · Session 1 (A test is a shuffling rule) · 25 min.
#
# Households rate the repair they received from 1 to 10. In a study of 400 responses for each contractor, A scores higher than B. Nizar Al-Khayyat asks: "Could that be luck?" You answer by building the world in which it is luck: shuffle the contractor labels, recompute the difference, 5,000 times. Then you run the classical test on the same data and compare.
#
# **AI policy.** Steps 1 to 4 are the day's first core computation: no assistant (AI-off). Step 5 and the stretch: AI-tutor.
#
# **Reference state.** `data/study_satisfaction.csv`: 400 responses for each contractor, drawn at random from the survey. Jobs go to the contractors by rota, so the contractor does not depend on the district. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · The observed difference in mean satisfaction (4')
# - [ ] 2 · One shuffle of the contractor labels (4')
# - [ ] 3 · 5,000 shuffles: the null distribution (7')
# - [ ] 4 · The two-sided permutation p-value (4')
# - [ ] 5 · Welch's t-test beside it (6')
# - [ ] ✱ Stretch · Test the difference in medians, for which no classical test is at hand

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
study = U.study_satisfaction()
score = study["satisfaction"].to_numpy(float)
is_a = (study["contractor"] == "A").to_numpy()
print(study.groupby("contractor")["satisfaction"].agg(["size", "mean", "std"]).round(3).to_string())

# %% [markdown]
# ## 1 · The observed difference in mean satisfaction (4')
#
# ✏️ **Exercise** · Write `diff_means(score, is_a)`: mean of A minus mean of B.

# %%
def diff_means(score, is_a):
    # BEGIN SOLUTION
    return float(score[is_a].mean() - score[~is_a].mean())
    # END SOLUTION


# %%
try:
    OBS = diff_means(score, is_a)
except NotImplementedError:
    OBS = U.reference("d3_1", "obs")
U.keep("d3_1", "obs", OBS)
print(f"observed difference, A - B: {OBS:+.3f} points on the 10-point scale")
U.check(abs(OBS - 0.295) < 0.001, "A is ahead by 0.295 points in this study")

# %% [markdown]
# ## 2 · One shuffle of the contractor labels (4')
#
# The **null hypothesis**: the contractor makes no difference to the score. If that is true, the label "A" or "B" on a response is arbitrary, and shuffling the labels changes nothing that matters.
#
# ✏️ **Exercise** · Write `one_shuffle(score, is_a, gen)`: shuffle the labels with `gen.permutation(is_a)` and return the difference in means under the shuffled labels.

# %%
def one_shuffle(score, is_a, gen):
    # BEGIN SOLUTION
    return diff_means(score, gen.permutation(is_a))
    # END SOLUTION


# %%
gen = U.rng(91)
try:
    few = [one_shuffle(score, is_a, gen) for _ in range(5)]
except NotImplementedError:
    few = U.reference("d3_1", "few")
U.keep("d3_1", "few", few)
print("five shuffled differences:", [round(v, 3) for v in few])
U.check(len(set(few)) > 1 and max(abs(v) for v in few) < 0.6, "shuffled differences are small and of either sign")

# %% [markdown]
# ## 3 · 5,000 shuffles: the null distribution (7')
#
# ✏️ **Exercise** · Write `null_distribution(score, is_a, B, gen)`: an array of `B` shuffled differences.

# %%
def null_distribution(score, is_a, B, gen):
    # BEGIN SOLUTION
    return np.array([one_shuffle(score, is_a, gen) for _ in range(B)])
    # END SOLUTION


# %%
B = U.pick(5000, 1000)
try:
    null = np.asarray(null_distribution(score, is_a, B, U.rng(92)))
except NotImplementedError:
    null = U.reference("d3_1", "null")
U.keep("d3_1", "null", null)
print(f"{len(null)} shuffles: centre {null.mean():+.4f}, standard deviation {null.std(ddof=1):.4f}, largest {np.abs(null).max():.3f}")
U.check(abs(null.mean()) < 0.02 and 0.11 < null.std(ddof=1) < 0.16, "the null distribution is centred on zero with a spread of about 0.135")
plt = U.plt()
fig, ax = plt.subplots()
ax.hist(null, bins=40, color="#3a7ca5")
for v in (OBS, -OBS):
    ax.axvline(v, color="#e4572e")
ax.set(xlabel="difference in means under shuffled labels, A - B", ylabel="shuffles", title=f"{len(null)} shuffles; red: the observed ±{OBS:.3f}")
plt.show()

# %% [markdown]
# ## 4 · The two-sided permutation p-value (4')
#
# The **p-value**: the share of shuffles whose difference is at least as far from zero as the observed one. Two-sided, because a gap in B's favour would have interested Nizar just as much. Count the observed arrangement as one of the shuffles: `(count + 1) / (B + 1)`.
#
# ✏️ **Exercise** · Write `p_value(null, obs)`.

# %%
def p_value(null, obs):
    # BEGIN SOLUTION
    return float((np.sum(np.abs(null) >= abs(obs)) + 1) / (len(null) + 1))
    # END SOLUTION


# %%
try:
    p_perm = p_value(null, OBS)
except NotImplementedError:
    p_perm = U.reference("d3_1", "p_perm")
U.keep("d3_1", "p_perm", p_perm)
print(f"permutation p-value: {p_perm:.4f}: under shuffled labels, a gap of {abs(OBS):.3f} or more turns up in about {p_perm * 1000:.0f} shuffles of 1,000")
U.check(0.012 < p_perm < 0.05, "a gap this large is rare under the shuffling rule, about 3 in 100")

# %% [markdown]
# ## 5 · Welch's t-test beside it (6')
#
# The classical route does not shuffle. It computes `t = difference / standard error` and looks the value up in a t distribution, which is a formula for the histogram you just drew.
#
# ✏️ **Exercise** · Write `welch(score, is_a)` returning `(t, p)`. By hand: the standard error is `sqrt(sa²/na + sb²/nb)` with sample standard deviations (`ddof=1`). Or call `stats.ttest_ind(a, b, equal_var=False)`.

# %%
def welch(score, is_a):
    # BEGIN SOLUTION
    r = stats.ttest_ind(score[is_a], score[~is_a], equal_var=False)
    return float(r.statistic), float(r.pvalue)
    # END SOLUTION


# %%
try:
    t, p_t = welch(score, is_a)
except NotImplementedError:
    t, p_t = U.reference("d3_1", "welch")
U.keep("d3_1", "welch", [t, p_t])
a, b = score[is_a], score[~is_a]
se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
print(f"standard error of the difference by formula: {se:.4f}; spread of the shuffled differences: {null.std(ddof=1):.4f}")
print(f"Welch's t-test: t = {t:.3f}, p = {p_t:.4f}; permutation test: p = {p_perm:.4f}")
U.check(abs(p_t - p_perm) < 0.012 and abs(t - OBS / se) < 1e-6, "the two p-values agree to about one hundredth: the t-test approximates the shuffle")

# %% [markdown]
# **Look at.** The formula's standard error and the spread of your shuffles are the same number to three decimals. With 400 responses per group the approximation is excellent. The shuffle needs no formula and no bell curve, which is why it still works when the classical test has none to offer.

# %% [markdown]
# ## ✱ Stretch · A statistic without a classical test
#
# Run the permutation test for the difference in **median** satisfaction.

# %%
def stretch():
    # BEGIN SOLUTION
    gen = U.rng(93)
    obs = np.median(score[is_a]) - np.median(score[~is_a])
    sh = np.empty(U.pick(5000, 1000))
    for i in range(len(sh)):
        lab = gen.permutation(is_a)
        sh[i] = np.median(score[lab]) - np.median(score[~lab])
    p = (np.sum(np.abs(sh) >= abs(obs)) + 1) / (len(sh) + 1)
    print(f"difference in medians: {obs:+.1f}; permutation p-value {p:.3f}")
    # Scores are whole numbers, so the median moves in steps and often shows no gap at all.
    return float(p)
    # END SOLUTION


try:
    U.keep("d3_1", "median_p", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
s = U.survey()
true_gap = s.loc[s.contractor == "A", "satisfaction"].mean() - s.loc[s.contractor == "B", "satisfaction"].mean()
U.note(f"Checked against the truth: in all 9,000 responses A is ahead by {true_gap:.3f} points, so rejecting 'no difference' was the right call here.",
       f"The study's estimate, {OBS:.3f}, is below the truth: a test says a gap exists, not how large it is. That is session 3.",
       "Not checked: a test on a sample drawn by district would need the district as the unit to shuffle.")

# %% [markdown]
# ## Checkpoint
#
# 1. What does one shuffle assume?
#    <details><summary>Answer</summary>That the contractor label has nothing to do with the score, so any assignment of the 400 A labels is as likely as the real one.</details>
# 2. The p-value is 0.03. Under which condition was that 3% computed?
#    <details><summary>Answer</summary>Under the null hypothesis. It is the chance of such a gap IF labels do not matter, not the chance that labels do not matter.</details>
# 3. With 15 responses per contractor, which p-value would you trust more?
#    <details><summary>Answer</summary>The permutation p-value: it does not lean on the bell-curve approximation, which is rough for small groups of whole-number scores.</details>
#
# ## Carry forward
#
# The observed gap, 0.295 points, and its p-value return in lab 3.3, where the question changes from "is there a gap?" to "does it matter?"
