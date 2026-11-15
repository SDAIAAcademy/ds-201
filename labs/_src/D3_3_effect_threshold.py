# %% [markdown]
# # Lab 3.3 · The effect against the threshold
#
# Day 3 · Session 3 (Effect size and practical significance) · 25 min.
#
# The test of lab 3.1 said the gap between the contractors is unlikely to be luck. Nizar Al-Khayyat's contract has a clause: a satisfaction gap of **0.5 points or more** between the contractors is "material" and triggers a review. So the question is no longer "is there a gap?" but "how large is it, and does it reach 0.5?" You report the effect with an interval, place it against the threshold, and measure what a study of this size can and cannot show.
#
# **AI policy.** AI-tutor: hints one step at a time, never the code.
#
# **Reference state.** `data/study_satisfaction.csv`, the same study as lab 3.1, loaded fresh; `data/survey.csv` for the power simulation. Nothing from lab 3.1 is needed.
#
# **Tasks**
# - [ ] 1 · Raw effect and standardised effect (5')
# - [ ] 2 · Bootstrap interval for the difference (6')
# - [ ] 3 · Place the interval against 0 and against 0.5 (4')
# - [ ] 4 · Power of a study this size, by simulation (6')
# - [ ] 5 · Write the three-sentence report (4')
# - [ ] ✱ Stretch · Find the sample size at which the interval is narrower than 0.3 points

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
def percentile_interval(boot, level=0.95):
    a = (1 - level) / 2 * 100
    low, high = np.percentile(boot, [a, 100 - a])
    return float(low), float(high)


study = U.study_satisfaction()
a = study.loc[study["contractor"] == "A", "satisfaction"].to_numpy(float)
b = study.loc[study["contractor"] == "B", "satisfaction"].to_numpy(float)
print(f"threshold in the contract: {U.THRESHOLD} points")

# %% [markdown]
# ## 1 · Raw effect and standardised effect (5')
#
# The **raw effect** is the gap in the units of the scale: points. The **standardised effect** (Cohen's d) divides it by the pooled standard deviation of the scores: the gap measured in "how much households differ from one another".
#
# ✏️ **Exercise** · Write `effects(a, b)` returning `(raw, d)`. Pooled SD for equal group sizes: `sqrt((sa² + sb²) / 2)` with `ddof=1`.

# %%
def effects(a, b):
    # BEGIN SOLUTION
    raw = a.mean() - b.mean()
    pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    return float(raw), float(raw / pooled)
    # END SOLUTION


# %%
try:
    raw, d = effects(a, b)
except NotImplementedError:
    raw, d = U.reference("d3_3", "effects")
U.keep("d3_3", "effects", [raw, d])
print(f"raw effect: {raw:.3f} points; standardised effect d = {d:.3f}")
U.check(abs(raw - 0.295) < 0.001 and 0.12 < d < 0.19, "0.295 points, about 0.15 standard deviations: a small effect")

# %% [markdown]
# **Look at.** d = 0.15 means the two score distributions overlap almost completely. Whether a small effect matters is not a statistical question: the contract answers it with 0.5 points. Report the raw effect for the decision, d for comparing across scales.

# %% [markdown]
# ## 2 · Bootstrap interval for the difference (6')
#
# ✏️ **Exercise** · Write `boot_diff(a, b, B, gen)`: `B` differences in means, each group resampled on its own.

# %%
def boot_diff(a, b, B, gen):
    # BEGIN SOLUTION
    ra = a[gen.integers(0, len(a), size=(B, len(a)))].mean(axis=1)
    rb = b[gen.integers(0, len(b), size=(B, len(b)))].mean(axis=1)
    return ra - rb
    # END SOLUTION


# %%
B = U.pick(5000, 1000)
try:
    boot = np.asarray(boot_diff(a, b, B, U.rng(111)))
except NotImplementedError:
    boot = U.reference("d3_3", "boot")
U.keep("d3_3", "boot", boot)
low, high = percentile_interval(boot)
print(f"difference A - B: {raw:.2f} points, 95% interval {low:.2f} to {high:.2f}")
U.check(0.0 < low < 0.1 and 0.5 < high < 0.62, "the interval runs from just above 0 to just above 0.5")

# %% [markdown]
# ## 3 · Place the interval against 0 and against 0.5 (4')
#
# Four positions are possible. Which one is this?
#
# | The interval | Reading |
# |---|---|
# | includes 0 and lies below the threshold | no gap shown; a material gap ruled out |
# | excludes 0, lies wholly below the threshold | a real gap, and not a material one |
# | excludes 0, includes the threshold | a real gap; material or not is **not settled** |
# | lies wholly above the threshold | a real and material gap |
#
# ✏️ **Exercise** · Write `position(low, high, threshold)` returning one of `"no gap shown"`, `"real, not material"`, `"real, not settled"`, `"real and material"`, or `"nothing settled"` when the interval includes both 0 and the threshold.

# %%
def position(low, high, threshold):
    # BEGIN SOLUTION
    has_zero, has_thr = low <= 0 <= high, low <= threshold <= high
    if has_zero and has_thr:
        return "nothing settled"
    if has_zero:
        return "no gap shown"
    if has_thr:
        return "real, not settled"
    return "real and material" if low > threshold else "real, not material"
    # END SOLUTION


# %%
try:
    pos = position(low, high, U.THRESHOLD)
except NotImplementedError:
    pos = U.reference("d3_3", "position")
U.keep("d3_3", "position", pos)
print("position:", pos)
U.check(pos == "real, not settled", "the gap is real; whether it reaches 0.5 points is not settled by this study")
try:
    others = [position(-0.1, 0.3, 0.5), position(0.1, 0.4, 0.5), position(0.6, 0.9, 0.5)]
    U.check(others == ["no gap shown", "real, not material", "real and material"], "the function also handles the three other positions")
except NotImplementedError:
    pass

# %% [markdown]
# ## 4 · Power of a study this size, by simulation (6')
#
# **Power** is the share of studies that detect a real effect. Zulal's survey holds the real effect, so draw the study again and again: 400 responses per contractor from the 9,000, a Welch test each time. Count two things: how often p < 0.05 (the gap is detected), and how often the whole interval lies below 0.5 (the study can say "not material").
#
# ✏️ **Exercise** · Write `power(pool_a, pool_b, n, studies, gen)` returning `(detected, shown_not_material)`. Use the t interval for speed: `diff ± 1.96 × se` with `se = sqrt(sa²/n + sb²/n)`, computed for all studies at once.

# %%
def power(pool_a, pool_b, n, studies, gen):
    # BEGIN SOLUTION
    x = gen.choice(pool_a, size=(studies, n))
    y = gen.choice(pool_b, size=(studies, n))
    p = stats.ttest_ind(x, y, axis=1, equal_var=False).pvalue
    diff = x.mean(axis=1) - y.mean(axis=1)
    se = np.sqrt(x.var(axis=1, ddof=1) / n + y.var(axis=1, ddof=1) / n)
    return float(np.mean(p < 0.05)), float(np.mean(diff + 1.96 * se < U.THRESHOLD))
    # END SOLUTION


# %%
survey = U.survey()
pool_a = survey.loc[survey["contractor"] == "A", "satisfaction"].to_numpy(float)
pool_b = survey.loc[survey["contractor"] == "B", "satisfaction"].to_numpy(float)
TRUE = float(pool_a.mean() - pool_b.mean())
STUDIES = U.pick(2000, 500)
try:
    res = {n: power(pool_a, pool_b, n, STUDIES, U.rng(112 + n)) for n in (100, 400, 1600)}
except NotImplementedError:
    res = {int(k): tuple(v) for k, v in U.reference("d3_3", "power").items()}
U.keep("d3_3", "power", {k: list(v) for k, v in res.items()})
print(f"the true gap in all 9,000 responses: {TRUE:.3f} points (below the threshold)")
U.table(["responses per contractor", "gap detected (power)", "shown to be below 0.5"], [[n, r[0], r[1]] for n, r in res.items()], fmt="{:.1%}")
U.check(res[400][0] > 0.85 and res[400][1] < 0.2 and res[100][0] < 0.6, "400 per contractor almost always detect the gap, and almost never can show it is below 0.5")

# %% [markdown]
# **Look at.** The true gap, 0.46, sits just under the threshold. Detecting that a gap exists is easy at 400 per group. Showing on which side of 0.5 it lies is a far harder question, and even 1,600 per group rarely answers it. A study is powered for a question, not in general.

# %% [markdown]
# ## 5 · Write the three-sentence report (4')
#
# ✏️ **Exercise** · Three sentences for Nizar: the estimate with its interval; what the test says; what is and is not settled about the threshold.

# %%
def my_report():
    # BEGIN SOLUTION
    return (f"In a study of 400 responses per contractor, households rated contractor A {raw:.2f} points higher than contractor B on the 10-point scale (95% interval {low:.2f} to {high:.2f}). "
            f"A gap of this size would be unusual if the contractors were the same, so we conclude that A is rated higher. "
            f"Whether the gap reaches the contract's threshold of 0.5 points is not settled: the interval includes 0.5, the estimate is below it, and the study covers surveyed households of this year only.")
    # END SOLUTION


# %%
try:
    report = my_report()
except NotImplementedError:
    report = U.reference("d3_3", "report")
U.keep("d3_3", "report", report)
print(report)
U.brief_check(report, {"estimate": f"{raw:.2f}", "interval low": f"{low:.2f}", "interval high": f"{high:.2f}", "threshold": "0.5"}, ["not settled"])

# %% [markdown]
# ## ✱ Stretch · How many responses for a useful interval?
#
# Find the number of responses per contractor at which the 95% interval for the gap is narrower than 0.3 points in total.

# %%
def stretch():
    # BEGIN SOLUTION
    sd = np.sqrt((pool_a.var() + pool_b.var()) / 2)
    n = int(np.ceil(2 * (2 * 1.96 * sd / 0.3) ** 2))
    print(f"width = 2 × 1.96 × sd × sqrt(2/n) < 0.3 with sd = {sd:.2f} gives n of about {n:,} per contractor")
    print(f"the survey holds {len(pool_a):,} and {len(pool_b):,} responses per contractor in all")
    return n
    # END SOLUTION


try:
    U.keep("d3_3", "n_for_width", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the truth: the true gap is {TRUE:.3f} points; the interval {low:.2f} to {high:.2f} contains it.",
       f"Checked by simulation: power {res[400][0]:.0%} to detect the gap at 400 per contractor; {res[400][1]:.0%} of such studies can show it is below 0.5.",
       "Not checked: whether 0.5 points is the right threshold. That is the contract's choice, not a statistical result.")

# %% [markdown]
# ## Checkpoint
#
# 1. A study with 50,000 responses per group finds a gap of 0.03 points, p < 0.001. What do you report?
#    <details><summary>Answer</summary>A real and negligible gap: the interval lies far below 0.5. Statistical significance is not importance.</details>
# 2. Which error is a missed real gap?
#    <details><summary>Answer</summary>A Type II error. Its rate is 1 minus the power.</details>
# 3. Why report the raw gap in points and not only d?
#    <details><summary>Answer</summary>The decision rule is written in points. d helps to compare with other scales and studies.</details>
#
# ## Carry forward
#
# "Estimate, interval, test, effect size, limits" is the skeleton of the capstone brief. This report is its first draft.
