# %% [markdown]
# # Pre-work · Sampling and plotting
#
# Before Day 1 · about two hours with the reading at the end.
#
# The course assumes you can filter and group a table, draw a random sample with a seed and plot a histogram. This notebook lets you check that on the data of the course: Zulal Water Utility, a fictional utility with a synthetic population. If a part is hard, that is the part to practise before the supervised entry quiz, which is held without an assistant.
#
# **Tasks**
# - [ ] 1 · Filter and group a table (20')
# - [ ] 2 · A mean, a standard deviation and a simple probability (20')
# - [ ] 3 · A random sample with a seed (20')
# - [ ] 4 · A histogram and a bar chart (30')
# - [ ] 5 · Self-check: five questions (15')
# - [ ] Reading: one chapter on sampling (15')

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
# ## 1 · Filter and group a table (20')

# %%
h = U.households()
print(h.head().to_string(index=False))

# %% [markdown]
# ✏️ **Exercise** · Return the number of households with six people or more in district `D01`.

# %%
def large_in_d01(h):
    # BEGIN SOLUTION
    return int(((h["district"] == "D01") & (h["household_size"] >= 6)).sum())
    # END SOLUTION


# %%
try:
    n_large = large_in_d01(h)
except NotImplementedError:
    n_large = U.reference("p0", "n_large")
U.keep("p0", "n_large", n_large)
print("households of six or more in D01:", n_large)
U.check(n_large == int(((h["district"] == "D01") & (h["household_size"] >= 6)).sum()), "the filter combines two conditions with &")

# %% [markdown]
# ✏️ **Exercise** · Return a Series: mean consumption by district, sorted from highest to lowest.

# %%
def mean_by_district(h):
    # BEGIN SOLUTION
    return h.groupby("district")["consumption_l_day"].mean().sort_values(ascending=False)
    # END SOLUTION


# %%
try:
    by_d = mean_by_district(h)
except NotImplementedError:
    by_d = pd.Series(U.reference("p0", "by_d"))
U.keep("p0", "by_d", by_d.to_dict())
print(by_d.head(5).round(1).to_string())
U.check(len(by_d) == 30 and by_d.iloc[0] >= by_d.iloc[-1], "30 districts, highest first")

# %% [markdown]
# ## 2 · A mean, a standard deviation and a simple probability (20')
#
# ✏️ **Exercise** · Return `(mean, sd, share)`: the mean and the standard deviation of `consumption_l_day`, and the probability that a household picked at random uses more than 700 litres a day.

# %%
def basics(h):
    # BEGIN SOLUTION
    x = h["consumption_l_day"]
    return float(x.mean()), float(x.std()), float((x > 700).mean())
    # END SOLUTION


# %%
try:
    mean, sd, share = basics(h)
except NotImplementedError:
    mean, sd, share = U.reference("p0", "basics")
U.keep("p0", "basics", [mean, sd, share])
print(f"mean {mean:.1f} litres, standard deviation {sd:.1f}, P(more than 700 litres) = {share:.3f}")
U.check(abs(mean - 470.35) < 0.1 and 0.1 < share < 0.2, "the mean is 470.4 litres; about one household in seven uses more than 700")

# %% [markdown]
# ## 3 · A random sample with a seed (20')
#
# A **seed** makes a random draw repeatable. `np.random.default_rng(7)` creates a generator; `gen.choice(values, size=20, replace=False)` draws 20 values without taking any twice.
#
# ✏️ **Exercise** · Write `seeded_sample(values, n, seed)`: create a generator from `seed` and return `n` values drawn without replacement.

# %%
def seeded_sample(values, n, seed):
    # BEGIN SOLUTION
    return np.random.default_rng(seed).choice(values, size=n, replace=False)
    # END SOLUTION


# %%
x = h["consumption_l_day"].to_numpy()
try:
    s1, s2, s3 = seeded_sample(x, 20, 7), seeded_sample(x, 20, 7), seeded_sample(x, 20, 8)
except NotImplementedError:
    s1 = s2 = np.asarray(U.reference("p0", "sample"))
    s3 = s1[::-1] + 1
U.keep("p0", "sample", s1)
print("seed 7:", s1[:8], "... mean", s1.mean())
print("seed 8:", s3[:8], "... mean", s3.mean())
U.check((s1 == s2).all() and not (s1 == s3).all(), "the same seed gives the same sample; another seed gives another")

# %% [markdown]
# **Look at.** Two samples of 20, two different means, neither equal to 470.4. Day 1 starts exactly here.

# %% [markdown]
# ## 4 · A histogram and a bar chart (30')
#
# ✏️ **Exercise** · Complete `plots(h, plt)`: draw a histogram of `consumption_l_day` with 40 bins on the first axis and a bar chart of the number of households by `household_size` on the second. Label both x axes. Return the two axes.

# %%
def plots(h, plt):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    # BEGIN SOLUTION
    ax1.hist(h["consumption_l_day"], bins=40)
    ax1.set(xlabel="consumption, litres a day", ylabel="households")
    counts = h["household_size"].value_counts().sort_index()
    ax2.bar(counts.index, counts.to_numpy())
    ax2.set(xlabel="people in the household", ylabel="households")
    # END SOLUTION
    return ax1, ax2


# %%
plt = U.plt()
try:
    ax1, ax2 = plots(h, plt)
    U.check(ax1.get_xlabel() != "" and ax2.get_xlabel() != "" and len(ax1.patches) == 40, "two labelled plots, 40 bins in the histogram")
except NotImplementedError:
    print("↪ plots not drawn yet")
plt.show()

# %% [markdown]
# ## 5 · Self-check (15')
#
# Answer on paper first, then open each answer.
#
# 1. You draw 20 households twice with the same seed. Are the two samples the same?
#    <details><summary>Answer</summary>Yes: a seed fixes the draws.</details>
# 2. The mean consumption is 470 litres and the median 449. Which way is the distribution skewed?
#    <details><summary>Answer</summary>To the right: a tail of large values pulls the mean above the median.</details>
# 3. In a histogram, what does the height of a bar show?
#    <details><summary>Answer</summary>How many observations fall into that bin.</details>
# 4. 12 of 200 sampled households use more than 900 litres. Estimate the probability for a random household.
#    <details><summary>Answer</summary>12 / 200 = 0.06.</details>
# 5. Why does `replace=False` matter when you sample households?
#    <details><summary>Answer</summary>No household is drawn twice, as in a real survey.</details>
#
# ## Reading (15')
#
# One chapter on sampling from either open textbook listed in the course sources: "Statistical Inference via Data Science" (the chapter on sampling) or "Introduction to Modern Statistics" (the chapter on foundations of inference). Read for the words population, sample, parameter and statistic.
#
# The supervised entry quiz follows this pre-work. It is held without an assistant and its items are not in this repository.
