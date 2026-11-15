# %% [markdown]
# # Lab 3.2 · Mark eight report sentences
#
# Day 3 · Session 2 (p-values and their misreadings) · 25 min.
#
# Ilyas Al-Tuwaijri's district performance report is going to Jamila Al-Shuraim tomorrow. Eight of its sentences interpret a p-value, an interval or a standard error. You mark each one right or wrong, with a reason. Then you check two of them the way this course checks everything: by simulating studies whose truth you know, and counting.
#
# **AI policy.** Step 1 is AI-off: the marking is the evidence for the first outcome of the course, and the exit check asks the same without an assistant. Steps 2 to 5: AI-tutor.
#
# **Reference state.** `data/report_sentences.json` (the eight sentences) and `data/survey.csv`. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Mark the eight sentences with reasons, assistant off (10')
# - [ ] 2 · Simulate 4,000 studies with the truth known (5')
# - [ ] 3 · Check sentence 1 by counting (4')
# - [ ] 4 · Check sentence 7 by counting (3')
# - [ ] 5 · Score the sheet and rewrite one sentence (3')
# - [ ] ✱ Stretch · Plot the p-values of the studies whose null is true

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

# %% [markdown]
# ## 1 · Mark the eight sentences with reasons, assistant off (10')

# %%
sentences = U.js("report_sentences.json")
for s in sentences:
    print(f"{s['id']}. {s['text']}\n")

# %% [markdown]
# ✏️ **Exercise** · Fill in the sheet: for each sentence `"right"` or `"wrong"`, and a reason of at least six words. Do not run step 5 before you have written all eight.

# %%
def my_sheet():
    # BEGIN SOLUTION
    return {
        1: ("wrong", "The 3% is computed assuming no difference; it is not the chance of no difference."),
        2: ("wrong", "A large p-value does not prove zero effect; the sample may be too small."),
        3: ("right", "This is the definition: how often the null rule gives a gap this large."),
        4: ("wrong", "A small p-value says nothing about size; a huge sample makes tiny effects significant."),
        5: ("wrong", "The interval is about the mean; single repairs spread far wider than that."),
        6: ("right", "Coverage describes the method over many studies, which is what the sentence says."),
        7: ("wrong", "With 30 tests one or two false alarms are expected even if nothing differs."),
        8: ("right", "The standard error is the typical distance of the sample mean from the truth."),
    }
    # END SOLUTION


# %%
try:
    sheet = my_sheet()
except NotImplementedError:
    sheet = None
print("sheet written" if sheet else "✏️ sheet not written yet: steps 2 to 4 run without it")

# %% [markdown]
# ## 2 · Simulate 4,000 studies with the truth known (5')
#
# A world in which you know which null hypotheses are true. Each simulated study compares two groups of 100 survey responses.
# - In half the studies the null is **true**: both groups are drawn from contractor A's responses.
# - In the other half it is **false**: one group from A, one from B (true gap 0.46 points).
#
# ✏️ **Exercise** · Write `simulate(pool_a, pool_b, studies, n, gen)`. Return `(null_true, p)`: a boolean array, `True` for the first half of the studies, and the Welch p-value of every study. Draw all groups at once: `gen.choice(pool, size=(k, n))` gives `k` groups; `stats.ttest_ind(x, y, axis=1, equal_var=False).pvalue` tests them row by row.

# %%
def simulate(pool_a, pool_b, studies, n, gen):
    # BEGIN SOLUTION
    half = studies // 2
    x = gen.choice(pool_a, size=(studies, n))
    y = np.vstack([gen.choice(pool_a, size=(half, n)), gen.choice(pool_b, size=(studies - half, n))])
    null_true = np.arange(studies) < half
    return null_true, stats.ttest_ind(x, y, axis=1, equal_var=False).pvalue
    # END SOLUTION


# %%
survey = U.survey()
pool_a = survey.loc[survey["contractor"] == "A", "satisfaction"].to_numpy(float)
pool_b = survey.loc[survey["contractor"] == "B", "satisfaction"].to_numpy(float)
STUDIES = U.pick(4000, 1200)
try:
    null_true, p = simulate(pool_a, pool_b, STUDIES, 100, U.rng(101))
except NotImplementedError:
    null_true, p = U.reference("d3_2", "sim")
null_true, p = np.asarray(null_true, dtype=bool), np.asarray(p)
U.keep("d3_2", "sim", [null_true, p])
alpha_hat, power_hat = float(np.mean(p[null_true] < 0.05)), float(np.mean(p[~null_true] < 0.05))
print(f"{len(p)} studies. Null true: {np.mean(p[null_true] < 0.05):.1%} have p < 0.05. Null false: {power_hat:.1%} have p < 0.05.")
U.check(0.03 < alpha_hat < 0.075 and 0.25 < power_hat < 0.6, "about 5% false alarms when the null is true; a real gap of 0.46 is detected in about 4 studies of 10")

# %% [markdown]
# **Look at.** Two error rates in one line. When nothing is going on, 5% of studies raise a false alarm: the **Type I** error rate, set by the 0.05 threshold. When the gap is real, more than half of the studies of this size miss it: **Type II** errors. Session 3 names the share that does detect it: power.

# %% [markdown]
# ## 3 · Check sentence 1 by counting (4')
#
# Sentence 1 claims: p = 0.03 means a 3% chance that the contractors are the same. In this simulated world you can count: among the studies whose p-value came out near 0.03 (between 0.02 and 0.04), in what share was the null actually true?
#
# ✏️ **Exercise** · Write `share_null_true(null_true, p, low, high)`.

# %%
def share_null_true(null_true, p, low, high):
    # BEGIN SOLUTION
    near = (p >= low) & (p <= high)
    return float(np.mean(null_true[near]))
    # END SOLUTION


# %%
try:
    s1 = share_null_true(null_true, p, 0.02, 0.04)
except NotImplementedError:
    s1 = U.reference("d3_2", "s1")
U.keep("d3_2", "s1", s1)
print(f"studies with p between 0.02 and 0.04: {int(np.sum((p >= 0.02) & (p <= 0.04)))}; in {s1:.0%} of them the two groups really were the same")
U.check(s1 > 0.10, "far more than 3%: the p-value is not the probability that the null is true")

# %% [markdown]
# **Look at.** The share depends on things the p-value does not know: how many of the hypotheses tested are true to begin with (here half), and how well the study detects a real gap. Change either and the share changes. A p-value alone can never deliver it.

# %% [markdown]
# ## 4 · Check sentence 7 by counting (3')
#
# Sentence 7: 30 districts tested, two below 0.05, "each has only a 5% chance of being a false alarm". Take the studies whose null is true, in batches of 30, as 30 districts where nothing differs.
#
# ✏️ **Exercise** · Write `flags_per_batch(p_null, size=30)`: cut `p_null` into full batches of `size` and return the number of p-values below 0.05 in each batch.

# %%
def flags_per_batch(p_null, size=30):
    # BEGIN SOLUTION
    k = len(p_null) // size
    return (p_null[: k * size].reshape(k, size) < 0.05).sum(axis=1)
    # END SOLUTION


# %%
try:
    flags = np.asarray(flags_per_batch(p[null_true]))
except NotImplementedError:
    flags = U.reference("d3_2", "flags")
U.keep("d3_2", "flags", flags)
print(f"{len(flags)} batches of 30 districts with no true difference: {flags.mean():.2f} districts flagged per batch on average;")
print(f"at least one flagged in {np.mean(flags >= 1):.0%} of batches, two or more in {np.mean(flags >= 2):.0%}. Every one of these flags is a false alarm.")
U.check(1.0 < flags.mean() < 2.1 and np.mean(flags >= 1) > 0.6, "about 1.5 false alarms per 30 tests; most batches have at least one")

# %% [markdown]
# ## 5 · Score the sheet and rewrite one sentence (3')

# %%
if sheet is None:
    sheet = {int(k): tuple(v) for k, v in U.reference("d3_2", "sheet").items()}
U.keep("d3_2", "sheet", {k: list(v) for k, v in sheet.items()})
score = U.mark_sheet(sheet)
U.check(score >= 6, "at least six of eight correct with reasons: the evidence for the first outcome of the course")

# %% [markdown]
# ✏️ **Exercise** · Rewrite sentence 1 so that it is right. Keep the 3%.

# %%
def my_rewrite():
    # BEGIN SOLUTION
    return ("The difference between the contractors gave p = 0.03: if the two contractors were really the same, "
            "a difference at least this large would turn up in about 3 studies in 100.")
    # END SOLUTION


# %%
try:
    rewrite = my_rewrite()
except NotImplementedError:
    rewrite = U.reference("d3_2", "rewrite")
U.keep("d3_2", "rewrite", rewrite)
print(rewrite)
U.check("if" in rewrite.lower() and "chance that the two contractors are" not in rewrite, "the rewrite states the condition: IF the contractors were the same")

# %% [markdown]
# ## ✱ Stretch · What p-values look like when nothing is going on
#
# Plot a histogram of the p-values of the studies whose null is true. What shape did you expect?

# %%
def stretch():
    # BEGIN SOLUTION
    counts = np.histogram(p[null_true], bins=10, range=(0, 1))[0]
    print("p-values under a true null, counts in ten equal bins:", counts.tolist())
    plt = U.plt()
    plt.hist(p[null_true], bins=20, range=(0, 1))
    plt.show()
    # Flat: under a true null every p-value is equally likely, so 5% fall below 0.05 and 1% below 0.01.
    return counts.tolist()
    # END SOLUTION


try:
    U.keep("d3_2", "null_p_hist", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked by simulation with the truth known: sentence 1 (the share of true nulls near p = 0.03 was {s1:.0%}, not 3%) and sentence 7 ({flags.mean():.1f} false alarms per 30 null tests).",
       "Checked against the key: the eight verdicts.",
       "Not checked: your reasons. The key compares verdicts and asks for a reason of six words; a trainer or a colleague reads the reasons.")

# %% [markdown]
# ## Checkpoint
#
# 1. In your simulation half the nulls were true. If only one hypothesis in ten were false, would the share in step 3 go up or down?
#    <details><summary>Answer</summary>Up, sharply: most small p-values would then come from the many true nulls.</details>
# 2. A study finds p = 0.40. Name two different worlds that produce it.
#    <details><summary>Answer</summary>No effect at all; or a real effect and a study too small to see it.</details>
# 3. What is the one sentence that is always a correct reading of p = 0.03?
#    <details><summary>Answer</summary>If the null hypothesis were true, a result at least this extreme would occur in about 3 studies of 100.</details>
#
# ## Carry forward
#
# The count of false alarms in 30 null tests, about 1.5, is the starting point of lab 3.4.
