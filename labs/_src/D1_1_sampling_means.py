# %% [markdown]
# # Lab 1.1 · One sample, then a thousand
#
# Day 1 · Session 1 (A sample is one draw of many) · 25 min.
#
# Jamila Al-Shuraim asks what an average household at Zulal uses in a day. You hold what no real analyst holds: the whole population of 80,000 households. You compute the true answer, then pretend you can only afford to read 50 meters, and watch how far one sample of 50 lands from the truth, and how 1,000 such samples scatter.
#
# **AI policy.** Steps 1 to 3 are the day's first core computation: no assistant (AI-off). From step 4 on, the tutor instruction `tutor_instruction.md` may give hints, never the code (AI-tutor).
#
# **Reference state.** `data/households.csv`, the population. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Load the population and compute the parameter (4')
# - [ ] 2 · One sample of 50: the statistic and its miss (5')
# - [ ] 3 · 1,000 samples: collect the means (7')
# - [ ] 4 · Plot the means and mark the truth (5')
# - [ ] 5 · Share of samples within 20 litres of the truth (4')
# - [ ] ✱ Stretch · Repeat with samples of 200 and compare the two spreads

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
# ## 1 · Load the population and compute the parameter (4')
#
# A **parameter** is a number that describes the population. Here it is the mean daily consumption of all 80,000 households. In real work you never see it; in this course you always can, which is how every method gets checked.

# %%
pop = U.households()
print(pop.head(3).to_string(index=False))
print(f"{len(pop):,} households in {pop['district'].nunique()} districts")
x = pop["consumption_l_day"].to_numpy(float)

# %% [markdown]
# ✏️ **Exercise** · Return the population mean of `x`.

# %%
def parameter(x):
    # BEGIN SOLUTION
    return float(x.mean())
    # END SOLUTION


# %%
try:
    MU = parameter(x)
except NotImplementedError:
    MU = U.reference("d1_1", "mu")
U.keep("d1_1", "mu", MU)
print(f"the parameter: mean consumption of the population = {MU:.1f} litres a day")
U.check(abs(MU - x.mean()) < 1e-9, "the parameter is the mean of all 80,000 households")

# %% [markdown]
# ## 2 · One sample of 50: the statistic and its miss (5')
#
# A **statistic** is the same number computed from a sample. `gen.choice(x, size=50, replace=False)` reads 50 meters at random.
#
# ✏️ **Exercise** · Write `sample_mean(x, n, gen)`: draw `n` households without replacement and return their mean.

# %%
def sample_mean(x, n, gen):
    # BEGIN SOLUTION
    return float(gen.choice(x, size=n, replace=False).mean())
    # END SOLUTION


# %%
gen = U.rng(11)
try:
    one = sample_mean(x, 50, gen)
except NotImplementedError:
    one = U.reference("d1_1", "one")
U.keep("d1_1", "one", one)
print(f"one sample of 50: mean = {one:.1f} litres a day; it misses the truth by {one - MU:+.1f}")
U.check(abs(one - MU) < 150, "one sample of 50 lands near the truth, not on it")

# %% [markdown]
# **Look at.** The miss is not a mistake. Read 50 other meters and you get another number. The question for the rest of the course is how large such misses typically are.

# %% [markdown]
# ## 3 · 1,000 samples: collect the means (7')
#
# ✏️ **Exercise** · Write `many_means(x, n, reps, gen)`: an array of `reps` sample means, each from a fresh sample of `n`.

# %%
def many_means(x, n, reps, gen):
    # BEGIN SOLUTION
    return np.array([gen.choice(x, size=n, replace=False).mean() for _ in range(reps)])
    # END SOLUTION


# %%
REPS = U.pick(1000, 300)
gen = U.rng(12)
try:
    means = many_means(x, 50, REPS, gen)
except NotImplementedError:
    means = U.reference("d1_1", "means")
U.keep("d1_1", "means", means)
print(f"{len(means)} sample means: lowest {means.min():.1f}, highest {means.max():.1f}")
print(f"their centre {means.mean():.1f} (truth {MU:.1f}); their spread (standard deviation) {means.std(ddof=1):.1f}")
U.check(abs(means.mean() - MU) < 5 and 20 < means.std(ddof=1) < 40, "the means centre on the truth and spread by about 29 litres")

# %% [markdown]
# ## 4 · Plot the means and mark the truth (5')
#
# This histogram is the **sampling distribution** of the mean for samples of 50: not households, but sample means.

# %%
plt = U.plt()
fig, ax = plt.subplots()
ax.hist(means, bins=30, color="#1f9e89")
ax.axvline(MU, color="black", linestyle="--", label=f"population mean {MU:.0f}")
ax.axvline(one, color="#e4572e", label=f"your one sample {one:.0f}")
ax.set(xlabel="mean consumption of a sample of 50, litres a day", ylabel="samples", title=f"{len(means)} samples of 50 households")
ax.legend()
plt.show()

# %% [markdown]
# **Look at.** The histogram is far narrower than the households themselves, whose consumption runs from under 100 to over 1,200 litres. And it is roughly bell-shaped although the households are not.

# %% [markdown]
# ## 5 · Share of samples within 20 litres of the truth (4')
#
# ✏️ **Exercise** · Return the share of the means that lie within `tol` litres of `mu`.

# %%
def share_within(means, mu, tol):
    # BEGIN SOLUTION
    return float(np.mean(np.abs(means - mu) <= tol))
    # END SOLUTION


# %%
try:
    shares = [share_within(means, MU, t) for t in (20, 57)]
except NotImplementedError:
    shares = U.reference("d1_1", "shares")
U.keep("d1_1", "shares", shares)
print(f"within 20 litres of the truth: {shares[0]:.0%} of samples; within 57 litres: {shares[1]:.0%}")
U.check(0.40 < shares[0] < 0.62 and shares[1] > 0.90, "about half the samples of 50 land within 20 litres; about 95% within 57")

# %% [markdown]
# ## ✱ Stretch · Samples of 200
#
# Collect the means of samples of 200 and compare their spread with the spread for 50. By what factor did it shrink?

# %%
def stretch():
    # BEGIN SOLUTION
    big = many_means(x, 200, U.pick(1000, 300), U.rng(13))
    print(f"spread for 50: {means.std(ddof=1):.1f}; for 200: {big.std(ddof=1):.1f}; ratio {means.std(ddof=1) / big.std(ddof=1):.2f}")
    # Four times the sample, about half the spread: session 2 gives the reason.
    return float(big.std(ddof=1))
    # END SOLUTION


try:
    U.keep("d1_1", "spread_200", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the truth: the 1,000 sample means centre on the population mean {MU:.1f} (their centre: {means.mean():.1f}).",
       "Not checked: nothing here says how to learn the spread from ONE sample. That is session 2.")

# %% [markdown]
# ## Checkpoint
#
# 1. Is 470.4 litres a parameter or a statistic? And the mean of your one sample?
#    <details><summary>Answer</summary>470.4 is the parameter: it describes all 80,000 households. The mean of one sample is a statistic: it changes with the sample.</details>
# 2. What does one bar of the histogram in step 4 count?
#    <details><summary>Answer</summary>Samples, not households: the number of samples of 50 whose mean fell in that range.</details>
# 3. A colleague reads 50 meters and reports "the average household uses 512 litres". What is missing?
#    <details><summary>Answer</summary>How far a sample of 50 typically lands from the truth: about 29 litres here. Without it the reader cannot tell 512 from 470.</details>
#
# ## Carry forward
#
# The spread of the sample means, about 29 litres for samples of 50, is the number session 2 names: the standard error.
