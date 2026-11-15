# %% [markdown]
# # Lab 1.3 · One ticket left open
#
# Day 1 · Session 3 (Skew, outliers and the median) · 25 min.
#
# Nizar Al-Khayyat reports the "average repair time" of the leak crews every month. Repair times are skewed: most leaks are fixed in a few hours, a few take days. You measure what a single ticket that was left open in the system for weeks does to the mean, the median and a trimmed mean of 200 repairs.
#
# **AI policy.** AI-tutor: hints one step at a time, never the code.
#
# **Reference state.** `data/repairs.csv`, the population of 12,000 repairs. The sample of 200 is drawn here with a seed from the tickets closed on time. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Look at the skew: mean against median (5')
# - [ ] 2 · Add one ticket left open and recompute (6')
# - [ ] 3 · Sweep the extreme value from 10 to 2,000 hours (6')
# - [ ] 4 · A trimmed mean as a middle road (4')
# - [ ] 5 · Decide what to report, and why (4')
# - [ ] ✱ Stretch · Count how many open tickets it takes to move the median by one hour

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
repairs = U.repairs()
late = repairs[repairs["status"] == "closed_late_entry"]
print(f"{len(repairs):,} repairs; {len(late)} were closed in the system weeks after the crew left:")
print(late["repair_hours"].sort_values().to_list())
closed = repairs.loc[repairs["status"] == "closed", "repair_hours"].to_numpy()
sample = U.rng(31).choice(closed, size=200, replace=False)

# %% [markdown]
# ## 1 · Look at the skew: mean against median (5')
#
# ✏️ **Exercise** · Return `(mean, median)` of the sample.

# %%
def mean_median(v):
    # BEGIN SOLUTION
    return float(np.mean(v)), float(np.median(v))
    # END SOLUTION


# %%
try:
    m0, med0 = mean_median(sample)
except NotImplementedError:
    m0, med0 = U.reference("d1_3", "base")
U.keep("d1_3", "base", [m0, med0])
print(f"200 repairs: mean {m0:.2f} h, median {med0:.2f} h; the longest took {sample.max():.1f} h")
print(f"share of repairs shorter than the mean: {np.mean(sample < m0):.0%}")
U.check(m0 > med0 * 1.15, "the mean sits well above the median: the sign of a long right tail")
plt = U.plt()
fig, ax = plt.subplots()
ax.hist(sample, bins=40, color="#1f9e89")
ax.axvline(m0, color="#e4572e", label=f"mean {m0:.1f}")
ax.axvline(med0, color="black", linestyle="--", label=f"median {med0:.1f}")
ax.set(xlabel="repair time, hours", ylabel="repairs", title="200 leak repairs")
ax.legend()
plt.show()

# %% [markdown]
# ## 2 · Add one ticket left open and recompute (6')
#
# One of the twelve late-entry tickets shows 1,450 hours: the crew finished in an afternoon, nobody closed the ticket for two months.
#
# ✏️ **Exercise** · Write `with_extra(v, value)`: the `(mean, median)` of the sample with one more value appended.

# %%
def with_extra(v, value):
    # BEGIN SOLUTION
    w = np.append(v, value)
    return float(w.mean()), float(np.median(w))
    # END SOLUTION


# %%
try:
    m1, med1 = with_extra(sample, 1450.0)
except NotImplementedError:
    m1, med1 = U.reference("d1_3", "extra")
U.keep("d1_3", "extra", [m1, med1])
print(f"with the open ticket: mean {m1:.2f} h (was {m0:.2f}), median {med1:.2f} h (was {med0:.2f})")
print(f"one ticket in 201 moved the mean by {m1 - m0:+.2f} h, the median by {med1 - med0:+.2f} h")
U.check(m1 - m0 > 5 and abs(med1 - med0) < 0.3, "one ticket nearly doubles the mean and leaves the median where it was")

# %% [markdown]
# ## 3 · Sweep the extreme value from 10 to 2,000 hours (6')
#
# ✏️ **Exercise** · For each value in `values`, compute `with_extra(sample, value)`. Return two lists: the means and the medians.

# %%
VALUES = [10, 50, 100, 500, 1000, 2000]


def sweep(v, values):
    # BEGIN SOLUTION
    pairs = [with_extra(v, float(x)) for x in values]
    return [p[0] for p in pairs], [p[1] for p in pairs]
    # END SOLUTION


# %%
try:
    means, medians = sweep(sample, VALUES)
except NotImplementedError:
    means, medians = U.reference("d1_3", "sweep")
U.keep("d1_3", "sweep", [means, medians])
U.table(["the extra ticket, hours", "mean", "median"], [[v, a, b] for v, a, b in zip(VALUES, means, medians)], fmt="{:.2f}")
U.check(means[-1] - means[0] > 8 and max(medians) - min(medians) < 0.3, "the mean follows the extra ticket without limit; the median does not")

# %% [markdown]
# **Look at.** The mean rises in a straight line with the extreme value: each extra hour on that one ticket adds 1/201 of an hour to the mean, for ever. The median only asks on which side of the middle the ticket falls.

# %% [markdown]
# ## 4 · A trimmed mean as a middle road (4')
#
# A 5% trimmed mean drops the lowest 5% and the highest 5% of the values, then averages the rest: `stats.trim_mean(values, 0.05)`.
#
# ✏️ **Exercise** · Return the 5% trimmed mean of the sample with the 1,450-hour ticket appended.

# %%
def trimmed(v, value):
    # BEGIN SOLUTION
    return float(stats.trim_mean(np.append(v, value), 0.05))
    # END SOLUTION


# %%
try:
    t1 = trimmed(sample, 1450.0)
except NotImplementedError:
    t1 = U.reference("d1_3", "trim")
U.keep("d1_3", "trim", t1)
t0 = float(stats.trim_mean(sample, 0.05))
print(f"5% trimmed mean: {t0:.2f} h without the ticket, {t1:.2f} h with it")
U.check(abs(t1 - t0) < 0.3, "the trimmed mean barely notices the ticket")

# %% [markdown]
# ## 5 · Decide what to report, and why (4')
#
# Nizar's question is "how long does a typical repair take?" His finance colleague asks "how many crew hours do we pay for?"
#
# ✏️ **Exercise** · Return a dictionary with the summary you would report for each question: `{"typical": "mean" or "median", "total_hours": "mean" or "median"}`.

# %%
def my_choice():
    # BEGIN SOLUTION
    return {"typical": "median", "total_hours": "mean"}
    # END SOLUTION


# %%
try:
    choice = my_choice()
except NotImplementedError:
    choice = U.reference("d1_3", "choice")
U.keep("d1_3", "choice", choice)
U.check(choice == {"typical": "median", "total_hours": "mean"}, "the typical repair is the median; a total needs the mean (total = mean × count)")
print("And the 1,450-hour ticket is not deleted in silence: it is a data-entry fact to report (\"12 tickets closed late, shown separately\").")

# %% [markdown]
# ## ✱ Stretch · How robust is the median?
#
# Append 1,450-hour tickets one at a time. How many does it take to move the median by one hour?

# %%
def stretch():
    # BEGIN SOLUTION
    w, k = sample.copy(), 0
    while np.median(w) - med0 < 1.0:
        w, k = np.append(w, 1450.0), k + 1
    print(f"{k} open tickets among {len(w)} repairs ({k / len(w):.0%}) move the median by one hour")
    return k
    # END SOLUTION


try:
    U.keep("d1_3", "tickets_for_one_hour", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
pop_all = repairs["repair_hours"]
U.note(f"Checked against the truth: in the whole population the 12 late-entry tickets lift the mean from {closed.mean():.2f} to {pop_all.mean():.2f} h; the median stays at {np.median(closed):.1f} against {pop_all.median():.1f}.",
       "Not checked: whether a ticket is an error or a real long repair. That needs the crew log, not statistics.")

# %% [markdown]
# ## Checkpoint
#
# 1. In a right-skewed sample, which is larger, the mean or the median?
#    <details><summary>Answer</summary>The mean: the long tail pulls it up. Here about two thirds of repairs are shorter than the mean.</details>
# 2. A report says "average repair time rose from 8.5 to 15.7 hours this month". What do you check first?
#    <details><summary>Answer</summary>Whether one or two extreme tickets explain it: compare the medians, and list the longest tickets.</details>
# 3. When is the mean the right summary even for skewed data?
#    <details><summary>Answer</summary>When the question is about a total: crew hours paid, water lost. A total is the mean times the count.</details>
#
# ## Carry forward
#
# Day 2 bootstraps the median repair time, because the median is the summary that answers "typical".
