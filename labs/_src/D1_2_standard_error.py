# %% [markdown]
# # Lab 1.2 · Standard error twice
#
# Day 1 · Session 2 (Standard error by simulation and by formula) · 25 min.
#
# The spread of a sampling distribution has a name: the **standard error**. You measure it by brute force at three sample sizes, then get nearly the same numbers from a formula, and finally from a single sample, which is all a real analyst ever has.
#
# **AI policy.** AI-tutor: hints one step at a time, never the simulation itself.
#
# **Reference state.** `data/households.csv`, the population. Nothing from lab 1.1 is needed.
#
# **Tasks**
# - [ ] 1 · Simulated standard error at n = 25, 100 and 400 (8')
# - [ ] 2 · The formula with the population standard deviation (4')
# - [ ] 3 · The formula from one sample only (6')
# - [ ] 4 · One table and the square-root law (4')
# - [ ] 5 · SD or SE: two sentences for the manager (3')
# - [ ] ✱ Stretch · Do the same for the sample median, which has no simple formula

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
x = U.households()["consumption_l_day"].to_numpy(float)
MU, SIGMA = x.mean(), x.std()
SIZES = [25, 100, 400]
REPS = U.pick(2000, 400)
print(f"population: mean {MU:.1f}, standard deviation {SIGMA:.1f} litres a day")

# %% [markdown]
# ## 1 · Simulated standard error at n = 25, 100 and 400 (8')
#
# ✏️ **Exercise** · Write `simulated_se(x, n, reps, gen)`: draw `reps` samples of `n` without replacement, take the mean of each, and return the standard deviation of those means (`ddof=1`).

# %%
def simulated_se(x, n, reps, gen):
    # BEGIN SOLUTION
    means = np.array([gen.choice(x, size=n, replace=False).mean() for _ in range(reps)])
    return float(means.std(ddof=1))
    # END SOLUTION


# %%
gen = U.rng(21)
try:
    sim = [simulated_se(x, n, REPS, gen) for n in SIZES]
except NotImplementedError:
    sim = U.reference("d1_2", "sim")
U.keep("d1_2", "sim", sim)
for n, s in zip(SIZES, sim):
    print(f"n = {n:>3}: simulated standard error {s:.2f} litres")
U.check(sim[0] > sim[1] > sim[2] and 35 < sim[0] < 48, "the standard error shrinks as the sample grows: about 41, 21 and 10")

# %% [markdown]
# ## 2 · The formula with the population standard deviation (4')
#
# For a mean, the standard error is the standard deviation of the households divided by the square root of the sample size: σ / √n.
#
# ✏️ **Exercise** · Return σ / √n.

# %%
def formula_se(sigma, n):
    # BEGIN SOLUTION
    return float(sigma / np.sqrt(n))
    # END SOLUTION


# %%
try:
    form = [formula_se(SIGMA, n) for n in SIZES]
except NotImplementedError:
    form = U.reference("d1_2", "form")
U.keep("d1_2", "form", form)
print("formula:", [round(v, 2) for v in form])
U.check(all(abs(a - b) / b < 0.12 for a, b in zip(sim, form)), "simulation and formula agree within a few percent")

# %% [markdown]
# ## 3 · The formula from one sample only (6')
#
# The formula above needs σ, which only the whole population gives. A real analyst replaces it with the standard deviation **of the sample**, `s` (`ddof=1`): the estimated standard error is s / √n.
#
# ✏️ **Exercise** · Write `one_sample_se(sample)`.

# %%
def one_sample_se(sample):
    # BEGIN SOLUTION
    return float(sample.std(ddof=1) / np.sqrt(len(sample)))
    # END SOLUTION


# %%
gen = U.rng(22)
samples = {n: gen.choice(x, size=n, replace=False) for n in SIZES}
try:
    est = [one_sample_se(samples[n]) for n in SIZES]
except NotImplementedError:
    est = U.reference("d1_2", "est")
U.keep("d1_2", "est", est)
print("from one sample each:", [round(v, 2) for v in est])
U.check(all(abs(a - b) / b < 0.30 for a, b in zip(est, form)), "one sample estimates its own standard error within about a quarter")

# %% [markdown]
# ## 4 · One table and the square-root law (4')

# %%
rows = [[n, a, b, c, a * np.sqrt(n)] for n, a, b, c in zip(SIZES, sim, form, est)]
U.table(["n", "simulated", "σ/√n", "s/√n, one sample", "simulated × √n"], rows, fmt="{:.2f}")
ratio = sim[0] / sim[2]
U.keep("d1_2", "ratio", ratio)
print(f"16 times the sample (25 to 400) made the standard error {ratio:.1f} times smaller")
U.check(3.3 < ratio < 4.8, "sixteen times the sample, about four times less error")

# %% [markdown]
# **Look at.** The last column is nearly constant and equals the standard deviation of the households, about 206 litres. Half the error costs four times the meters read. The third column came from a single sample, without the population: this is why a standard error can be reported in real work at all.

# %% [markdown]
# ## 5 · SD or SE: two sentences for the manager (3')
#
# From the sample of 100, write one sentence that uses the standard deviation and one that uses the standard error. They answer different questions.
#
# ✏️ **Exercise** · Return the two numbers, rounded to a whole litre: `(sd, se)` of `samples[100]`.

# %%
def sd_and_se(sample):
    # BEGIN SOLUTION
    return round(float(sample.std(ddof=1))), round(float(sample.std(ddof=1) / np.sqrt(len(sample))))
    # END SOLUTION


# %%
try:
    sd, se = sd_and_se(samples[100])
except NotImplementedError:
    sd, se = U.reference("d1_2", "sd_se")
U.keep("d1_2", "sd_se", [sd, se])
m = samples[100].mean()
print(f"SD sentence: households differ a lot from one another: a typical household is about {sd} litres away from the sample mean of {m:.0f}.")
print(f"SE sentence: our estimate of the average, {m:.0f} litres, is typically within about {se} litres of the true average.")
U.check(sd > 5 * se, "the standard deviation describes households, the standard error describes the estimate")

# %% [markdown]
# ## ✱ Stretch · The median has a standard error too
#
# Simulate the standard error of the sample **median** at the three sizes. There is no σ/√n for it, yet the simulation does not care.

# %%
def stretch():
    # BEGIN SOLUTION
    gen = U.rng(23)
    out = []
    for n in SIZES:
        meds = np.array([np.median(gen.choice(x, size=n, replace=False)) for _ in range(U.pick(2000, 400))])
        out.append(float(meds.std(ddof=1)))
    print("simulated standard error of the median:", [round(v, 2) for v in out])
    return out
    # END SOLUTION


try:
    U.keep("d1_2", "median_se", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the truth: simulated standard errors {[round(v, 1) for v in sim]} against σ/√n {[round(v, 1) for v in form]}.",
       "Checked: one sample's own estimate s/√n lands near both.",
       "Not checked: whether the mean is the right summary for skewed data. That is session 3.")

# %% [markdown]
# ## Checkpoint
#
# 1. A sample of 100 households has s = 210 litres. What is the estimated standard error of its mean?
#    <details><summary>Answer</summary>210 / √100 = 21 litres.</details>
# 2. How many households for a standard error of 7 litres?
#    <details><summary>Answer</summary>Nine times as many, 900: three times less error costs nine times the sample.</details>
# 3. Does the standard deviation of the households shrink when you read more meters?
#    <details><summary>Answer</summary>No. Households differ as much as they differ. Only the uncertainty of the estimate shrinks.</details>
#
# ## Carry forward
#
# Estimate ± 2 standard errors is the first interval of the course. Day 2 builds intervals without any formula.
