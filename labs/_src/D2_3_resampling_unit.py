# %% [markdown]
# # Lab 2.3 · Household or district
#
# Day 2 · Session 3 (Resample the right unit) · 25 min.
#
# To save travel, Zulal's survey team did not phone households all over the region. It picked 6 districts and phoned 60 households in each. Jamila Al-Shuraim wants mean satisfaction with an interval. You bootstrap the 360 responses the obvious way, then the right way, and count which of the two keeps the 95% promise.
#
# **AI policy.** AI-tutor: hints one step at a time, never the simulation.
#
# **Reference state.** `data/survey.csv`, the 9,000 responses, and `U.two_stage_sample(gen, 6, 60)`, which draws the two-stage sample. Districts are chosen with probability proportional to their size, so the plain mean of the sample is a fair estimate. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Draw the two-stage sample and estimate (4')
# - [ ] 2 · Bootstrap by household (5')
# - [ ] 3 · Bootstrap by district (6')
# - [ ] 4 · Coverage of both over 300 studies (6')
# - [ ] 5 · Explain the difference in two sentences (4')
# - [ ] ✱ Stretch · Redraw with 12 districts of 30 responses and compare the widths
# - [ ] ✱ Stretch 2 · Oversample the six smallest districts and restore the regional mean with design weights

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


survey = U.survey()
TRUE = float(survey["satisfaction"].mean())
print(f"all 9,000 responses: mean satisfaction {TRUE:.3f} on the 10-point scale")

# %% [markdown]
# ## 1 · Draw the two-stage sample and estimate (4')

# %%
sample = U.two_stage_sample(U.rng(71), 6, 60)
est = float(sample["satisfaction"].mean())
by_district = sample.groupby("district")["satisfaction"].agg(["size", "mean"]).round(2)
print(by_district.to_string())
print(f"estimate from {len(sample)} responses in {sample['district'].nunique()} districts: {est:.3f}")

# %% [markdown]
# **Look at.** The six district means differ by more than a point. Two households of one district resemble each other more than two households picked anywhere: the rows are not 360 independent pieces of information.

# %% [markdown]
# ## 2 · Bootstrap by household (5')
#
# The obvious way: treat the 360 rows as the units.
#
# ✏️ **Exercise** · Write `boot_households(values, B, gen)`: `B` means of resamples of the rows.

# %%
def boot_households(values, B, gen):
    # BEGIN SOLUTION
    idx = gen.integers(0, len(values), size=(B, len(values)))
    return values[idx].mean(axis=1)
    # END SOLUTION


# %%
B = U.pick(2000, 500)
v = sample["satisfaction"].to_numpy(float)
try:
    bh = np.asarray(boot_households(v, B, U.rng(72)))
except NotImplementedError:
    bh = U.reference("d2_3", "bh")
U.keep("d2_3", "bh", bh)
ih = percentile_interval(bh)
print(f"household bootstrap: {ih[0]:.2f} to {ih[1]:.2f} (width {ih[1] - ih[0]:.2f})")
U.check(0.25 < ih[1] - ih[0] < 0.6, "resampling rows gives a narrow interval, about 0.4 points wide")

# %% [markdown]
# ## 3 · Bootstrap by district (6')
#
# The survey team drew **districts** first. So the unit to resample is the district: draw 6 districts with replacement from the 6, and take each drawn district with all its responses. With equal numbers per district, that is the mean of the resampled district means.
#
# ✏️ **Exercise** · Write `boot_districts(df, B, gen)`: compute the district means, resample them with replacement `B` times, return the `B` means.

# %%
def boot_districts(df, B, gen):
    # BEGIN SOLUTION
    dm = df.groupby("district")["satisfaction"].mean().to_numpy()
    idx = gen.integers(0, len(dm), size=(B, len(dm)))
    return dm[idx].mean(axis=1)
    # END SOLUTION


# %%
try:
    bd = np.asarray(boot_districts(sample, B, U.rng(73)))
except NotImplementedError:
    bd = U.reference("d2_3", "bd")
U.keep("d2_3", "bd", bd)
idist = percentile_interval(bd)
print(f"district bootstrap:  {idist[0]:.2f} to {idist[1]:.2f} (width {idist[1] - idist[0]:.2f})")
print(f"the truth: {TRUE:.2f}; household interval {'contains' if ih[0] <= TRUE <= ih[1] else 'MISSES'} it, district interval {'contains' if idist[0] <= TRUE <= idist[1] else 'MISSES'} it")
U.check(idist[1] - idist[0] > 1.5 * (ih[1] - ih[0]), "resampling districts gives an interval about twice as wide")

# %% [markdown]
# ## 4 · Coverage of both over 300 studies (6')
#
# Which width is the honest one? Count.
#
# ✏️ **Exercise** · Write `coverage(studies, gen)`: for each study draw `U.two_stage_sample(gen, 6, 60)`, build both intervals with 1,000 resamples, and return the two shares that contain `TRUE`: `(household_share, district_share)`.

# %%
def coverage(studies, gen):
    # BEGIN SOLUTION
    hit_h = hit_d = 0
    for _ in range(studies):
        s = U.two_stage_sample(gen, 6, 60)
        lo, hi = percentile_interval(boot_households(s["satisfaction"].to_numpy(float), 1000, gen))
        hit_h += lo <= TRUE <= hi
        lo, hi = percentile_interval(boot_districts(s, 1000, gen))
        hit_d += lo <= TRUE <= hi
    return hit_h / studies, hit_d / studies
    # END SOLUTION


# %%
STUDIES = U.pick(300, 80)
try:
    cov = coverage(STUDIES, U.rng(74))
except NotImplementedError:
    cov = U.reference("d2_3", "cov")
U.keep("d2_3", "cov", list(cov))
print(f"{STUDIES} two-stage studies: the household interval covers {cov[0]:.1%}, the district interval {cov[1]:.1%} (promised: 95%)")
U.check(cov[0] < 0.80 and cov[1] > 0.84, "the household bootstrap misses the truth in more than a quarter of studies; the district bootstrap comes close to its promise")

# %% [markdown]
# **Look at.** The district interval still falls a little short of 95%: six districts are few, and a bootstrap of six values is rough. It is honest about the size of the uncertainty all the same; the household interval is not.

# %% [markdown]
# ## 5 · Explain the difference in two sentences (4')
#
# ✏️ **Exercise** · Return your two sentences. The first names the unit that was sampled; the second says what resampling rows gets wrong.

# %%
def my_explanation():
    # BEGIN SOLUTION
    return ("The survey sampled 6 districts first and households inside them, so the district is the unit that was drawn at random and the unit to resample. "
            "Resampling households keeps the same 6 districts in every resample and so ignores that another survey would have visited other districts, which makes the interval about half as wide as it should be.")
    # END SOLUTION


# %%
try:
    text = my_explanation()
except NotImplementedError:
    text = U.reference("d2_3", "text")
U.keep("d2_3", "text", text)
print(text)
U.check("district" in text.lower() and len(text.split()) >= 20, "the explanation names the district as the sampled unit")

# %% [markdown]
# ## ✱ Stretch · More districts, fewer calls in each
#
# The same 360 calls spent on 12 districts of 30. Compare the width of the district interval.

# %%
def stretch():
    # BEGIN SOLUTION
    s = U.two_stage_sample(U.rng(75), 12, 30)
    lo, hi = percentile_interval(boot_districts(s, U.pick(2000, 500), U.rng(76)))
    print(f"12 districts of 30: {lo:.2f} to {hi:.2f} (width {hi - lo:.2f}); 6 districts of 60 gave width {idist[1] - idist[0]:.2f}")
    # More districts narrow the interval far more than more households per district.
    return hi - lo
    # END SOLUTION


try:
    U.keep("d2_3", "width_12", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## ✱ Stretch 2 · Oversample the small districts, then weight them back
#
# Jamila also wants a number for each of the six smallest districts, and a handful of calls in each would be useless. So another survey design phones **40** households in each of the six smallest districts and **120** households at random from the other 24: 360 calls again, but two thirds of them in districts that hold under 5% of the responses.
#
# Each response then stands for a different number of responses in the population: its **design weight** is `N / n` of its group (responses on file in the group divided by responses drawn from it). The plain mean of the sample answers the wrong question; the weighted mean answers the regional one.
#
# ✏️ **Exercise** · Write `oversampled_estimates(gen)`: draw the sample above, and return `(plain_mean, weighted_mean)`.

# %%
COUNTS = survey["district"].value_counts()
SMALL6 = sorted(COUNTS.nsmallest(6).index)
SCORE = survey["satisfaction"].to_numpy(dtype=float)
IS_SMALL = survey["district"].isin(SMALL6).to_numpy()
ROWS_BY_DISTRICT = {d: np.flatnonzero(survey["district"].to_numpy() == d) for d in SMALL6}
OTHER_ROWS = np.flatnonzero(~IS_SMALL)


def oversampled_estimates(gen):
    # BEGIN SOLUTION
    values, weights = [], []
    for d in SMALL6:
        rows = ROWS_BY_DISTRICT[d]
        values.append(SCORE[gen.choice(rows, 40, replace=False)])
        weights.append(np.full(40, len(rows) / 40))
    values.append(SCORE[gen.choice(OTHER_ROWS, 120, replace=False)])
    weights.append(np.full(120, len(OTHER_ROWS) / 120))
    y, w = np.concatenate(values), np.concatenate(weights)
    return float(y.mean()), float(np.sum(w * y) / np.sum(w))
    # END SOLUTION


try:
    one_over = oversampled_estimates(U.rng(77))
    gen = U.rng(78)
    many_over = np.array([oversampled_estimates(gen) for _ in range(U.pick(500, 100))])
    print(f"six smallest districts {SMALL6}: {IS_SMALL.sum()} of {len(survey):,} responses ({IS_SMALL.mean():.1%}), mean {SCORE[IS_SMALL].mean():.2f}; the other 24: {SCORE[~IS_SMALL].mean():.2f}")
    print(f"one oversampled survey: plain mean {one_over[0]:.2f}, weighted mean {one_over[1]:.2f}, truth {TRUE:.2f}")
    print(f"over {len(many_over)} surveys: plain mean {many_over[:, 0].mean():.2f} on average, weighted {many_over[:, 1].mean():.2f}, truth {TRUE:.2f}")
    U.check(abs(many_over[:, 1].mean() - TRUE) < 0.05 < abs(many_over[:, 0].mean() - TRUE),
            "the plain mean of the oversampled survey misses the regional mean; the weighted mean lands on it")
    U.keep("d2_3", "oversampled", [one_over[0], one_over[1], float(many_over[:, 0].mean()), float(many_over[:, 1].mean())])
except NotImplementedError:
    print("✱ stretch 2 not done")

# %% [markdown]
# **Look at.** Oversampling a small group is good design when the group must be reported on its own; it only becomes an error when the regional number is computed as if every row counted the same. Keep the weight beside every row, and say in the brief that the regional estimate is weighted. A bootstrap of such a sample resamples within each group and carries the weights along.

# %%
U.note(f"Checked against the truth: coverage of the mean of all 9,000 responses ({TRUE:.2f}) over {STUDIES} two-stage studies: household {cov[0]:.0%}, district {cov[1]:.0%}.",
       "Not checked: a district bootstrap with unequal numbers of responses per district, which needs the full rows of each drawn district.")

# %% [markdown]
# ## Checkpoint
#
# 1. A study measures 5 pressure readings on each of 40 pumps. What is the resampling unit for the mean pressure?
#    <details><summary>Answer</summary>The pump: readings of one pump move together. Resample pumps, each with its 5 readings.</details>
# 2. The survey had phoned 360 households picked at random across the whole region. Which bootstrap then?
#    <details><summary>Answer</summary>By household: the household was the unit drawn at random.</details>
# 3. In the capstone defence the assessor names another resampling unit. What do you predict before running it?
#    <details><summary>Answer</summary>Whether the interval widens (a larger unit that groups similar rows) or stays about the same (rows inside the unit are no more alike than rows anywhere).</details>
#
# ## Carry forward
#
# "What was the unit that was drawn at random?" is the first question of every interval and every test from here on.
