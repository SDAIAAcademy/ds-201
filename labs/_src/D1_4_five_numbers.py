# %% [markdown]
# # Lab 1.4 · Five numbers and a histogram
#
# Day 1 · Session 4 (Describing a sample honestly) · 25 min.
#
# Before any interval or test, a reader needs an honest description of the sample: where the middle is, how wide the spread, how many repairs, what was left out. You describe 300 repairs so that a colleague could check every number.
#
# **AI policy.** AI-tutor: hints one step at a time, never the code.
#
# **Reference state.** `data/repairs.csv`. The sample of 300 is drawn here with a seed from all 12,000 repairs, late-entry tickets included. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Five numbers and the interquartile range (6')
# - [ ] 2 · A histogram with a stated bin width (5')
# - [ ] 3 · The same data on a log axis (4')
# - [ ] 4 · The summary by contractor, with counts (5')
# - [ ] 5 · Write the honest description (5')
# - [ ] ✱ Stretch · Build the district table and withhold every district with fewer than 20 repairs

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
repairs = U.repairs()
sample = repairs.sample(300, random_state=U.SEED + 52).reset_index(drop=True)
hours = sample["repair_hours"].to_numpy()
print(sample.head(3).to_string(index=False))
print("late-entry tickets in this sample:", int((sample["status"] != "closed").sum()))

# %% [markdown]
# ## 1 · Five numbers and the interquartile range (6')
#
# The five numbers: minimum, first quartile, median, third quartile, maximum. The **interquartile range** (IQR) is the width of the middle half.
#
# ✏️ **Exercise** · Return a dictionary with the keys `min`, `q1`, `median`, `q3`, `max`, `iqr`. Use `np.percentile`.

# %%
def five_numbers(v):
    # BEGIN SOLUTION
    q1, med, q3 = np.percentile(v, [25, 50, 75])
    return {"min": float(np.min(v)), "q1": float(q1), "median": float(med), "q3": float(q3),
            "max": float(np.max(v)), "iqr": float(q3 - q1)}
    # END SOLUTION


# %%
try:
    five = five_numbers(hours)
except NotImplementedError:
    five = U.reference("d1_4", "five")
U.keep("d1_4", "five", five)
print({k: round(v, 2) for k, v in five.items()})
print(f"for comparison: mean {hours.mean():.2f}, standard deviation {hours.std(ddof=1):.2f}")
U.check(five["q1"] < five["median"] < five["q3"] and abs(five["iqr"] - (five["q3"] - five["q1"])) < 1e-9, "the five numbers are in order and the IQR is q3 - q1")

# %% [markdown]
# **Look at.** The standard deviation is larger than the mean. For skewed data "mean ± SD" describes nothing: it would reach below zero hours.

# %% [markdown]
# ## 2 · A histogram with a stated bin width (5')
#
# A histogram is a choice: where it ends and how wide the bins are. State both.
#
# ✏️ **Exercise** · Return the bin edges for bins 2 hours wide from 0 to 40 hours (`np.arange`). Repairs longer than 40 hours are counted and named in the title, not dropped in silence.

# %%
def bin_edges():
    # BEGIN SOLUTION
    return np.arange(0, 42, 2)
    # END SOLUTION


# %%
try:
    edges = np.asarray(bin_edges())
except NotImplementedError:
    edges = U.reference("d1_4", "edges")
U.keep("d1_4", "edges", edges)
beyond = int((hours > edges[-1]).sum())
plt = U.plt()
fig, ax = plt.subplots()
ax.hist(hours[hours <= edges[-1]], bins=edges, color="#1f9e89")
ax.axvline(five["median"], color="black", linestyle="--", label=f"median {five['median']:.1f} h")
ax.set(xlabel="repair time, hours (bins of 2 hours)", ylabel="repairs",
       title=f"{len(hours)} repairs; {beyond} longer than {edges[-1]:.0f} h not shown")
ax.legend()
plt.show()
print(f"{beyond} repairs are longer than {edges[-1]:.0f} hours and are named in the title")
U.check(len(edges) == 21 and edges[1] - edges[0] == 2, "20 bins of 2 hours")

# %% [markdown]
# ## 3 · The same data on a log axis (4')
#
# On a log axis each step multiplies: 1, 10, 100, 1,000 hours. Every repair fits, the late-entry tickets too.

# %%
fig, ax = plt.subplots()
ax.hist(hours, bins=np.logspace(np.log10(hours.min()), np.log10(hours.max()), 35), color="#3a7ca5")
ax.set_xscale("log")
ax.set(xlabel="repair time, hours (log axis)", ylabel="repairs", title=f"all {len(hours)} repairs")
plt.show()
log_skew = float(pd.Series(np.log(hours)).skew())
raw_skew = float(pd.Series(hours).skew())
U.keep("d1_4", "skew", [raw_skew, log_skew])
print(f"skewness of the hours: {raw_skew:.1f}; of their logarithms: {log_skew:.1f}")

# %% [markdown]
# **Look at.** On the log axis the bulk is nearly symmetric and the late-entry tickets stand apart on the right as a separate little group: a different process, not the tail of the same one.

# %% [markdown]
# ## 4 · The summary by contractor, with counts (5')
#
# ✏️ **Exercise** · Return a table indexed by `contractor` with the columns `n`, `median`, `q1`, `q3` of `repair_hours`.

# %%
def by_contractor(df):
    # BEGIN SOLUTION
    g = df.groupby("contractor")["repair_hours"]
    return pd.DataFrame({"n": g.size(), "median": g.median(), "q1": g.quantile(0.25), "q3": g.quantile(0.75)})
    # END SOLUTION


# %%
try:
    tab = by_contractor(sample)
except NotImplementedError:
    tab = pd.DataFrame(U.reference("d1_4", "tab"))
U.keep("d1_4", "tab", tab.to_dict())
print(tab.round(2).to_string())
U.check(int(tab["n"].sum()) == 300 and set(tab.index) == {"A", "B"}, "both contractors, counts adding up to 300")

# %% [markdown]
# **Look at.** Contractor B's median is higher in this sample. Whether that gap is more than the luck of 300 tickets is a question for Day 2 and Day 3. A description shows the gap; it does not judge it.

# %% [markdown]
# ## 5 · Write the honest description (5')
#
# ✏️ **Exercise** · Write three or four sentences. They must give: the number of repairs, the median and the quartiles, the longest repair or the count of late-entry tickets, and the population the sample came from.

# %%
def my_description():
    # BEGIN SOLUTION
    return (f"We looked at 300 leak repairs drawn at random from Zulal's 12,000 repairs of the year. "
            f"The median repair took {five['median']:.1f} hours; the middle half took between {five['q1']:.1f} and {five['q3']:.1f} hours. "
            f"{int((sample['status'] != 'closed').sum())} ticket in the sample was closed in the system weeks late and is reported separately; "
            f"the longest regular repair took {sample.loc[sample['status'] == 'closed', 'repair_hours'].max():.1f} hours. "
            f"These numbers describe the 300 sampled repairs, by contractor and never by household.")
    # END SOLUTION


# %%
try:
    text = my_description()
except NotImplementedError:
    text = U.reference("d1_4", "text")
U.keep("d1_4", "text", text)
print(text)
U.brief_check(text, {"count": "300", "median": f"{five['median']:.1f}", "first quartile": f"{five['q1']:.1f}", "third quartile": f"{five['q3']:.1f}"}, ["12,000"])

# %% [markdown]
# ## ✱ Stretch · A district table that protects small counts
#
# Zulal reports results by district only, and withholds a district's number when it rests on fewer than 20 repairs. Build the table of medians by district for the sample and blank the small ones.

# %%
def stretch():
    # BEGIN SOLUTION
    g = sample.groupby("district")["repair_hours"]
    t = pd.DataFrame({"n": g.size(), "median": g.median()})
    t.loc[t["n"] < 20, "median"] = np.nan
    print(t.sort_values("n", ascending=False).head(8).to_string())
    print(f"{int(t['median'].isna().sum())} of {len(t)} districts withheld (fewer than 20 repairs in the sample)")
    return int(t["median"].isna().sum())
    # END SOLUTION


try:
    U.keep("d1_4", "withheld", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the truth: the sample median {five['median']:.1f} h against the population median {repairs['repair_hours'].median():.1f} h.",
       "Checked: the description quotes the count, the median and the quartiles exactly as computed.",
       "Not checked: no statement about uncertainty yet. A description is not an inference.")

# %% [markdown]
# ## Checkpoint
#
# 1. Why is "mean ± SD" a poor description of these repair times?
#    <details><summary>Answer</summary>The SD exceeds the mean, so the range runs below zero, and one late-entry ticket inflates both. Median and quartiles describe the data as it is.</details>
# 2. What must a histogram's caption say?
#    <details><summary>Answer</summary>The bin width, the axis (plain or log), the count, and what is not shown.</details>
# 3. Why does Zulal withhold districts with fewer than 20 repairs?
#    <details><summary>Answer</summary>A number resting on a handful of tickets is unstable, and in a small district it can point at single households.</details>
#
# ## Carry forward
#
# Every brief in this course starts with such a description. Lab 4.4 and the capstone reuse the pattern: count, middle, spread, exclusions, population.
