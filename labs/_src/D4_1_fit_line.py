# %% [markdown]
# # Lab 4.1 · Consumption on household size
#
# Day 4 · Session 1 (Least squares as a summary) · 25 min.
#
# Jamila Al-Shuraim is planning supply for a new housing scheme with large families. Her question: "How much more water does a household use for each additional person?" You answer with a fitted line on 2,000 metered households, say the slope in units she uses, and compare your line with the one the whole population gives.
#
# **AI policy.** Steps 1 to 3 are the day's first core computation: no assistant (AI-off). Steps 4, 5 and the stretch: AI-tutor.
#
# **Reference state.** `data/metered_2000.csv`: 2,000 households drawn at random from the 80,000. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Scatter and mean consumption by household size (5')
# - [ ] 2 · Fit the line by least squares (6')
# - [ ] 3 · The slope in litres a day and cubic metres a month (5')
# - [ ] 4 · Predict for 2 and 6 people; read the intercept (4')
# - [ ] 5 · Compare with the population line (5')
# - [ ] ✱ Stretch · Fit the same line with a statistics library and find the slope in its summary

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
m = U.metered()
x = m["household_size"].to_numpy(float)
y = m["consumption_l_day"].to_numpy(float)
print(m.head(3).to_string(index=False))

# %% [markdown]
# ## 1 · Scatter and mean consumption by household size (5')
#
# ✏️ **Exercise** · Return a table indexed by `household_size` with the columns `n` and `mean` of `consumption_l_day`.

# %%
def means_by_size(m):
    # BEGIN SOLUTION
    g = m.groupby("household_size")["consumption_l_day"]
    return pd.DataFrame({"n": g.size(), "mean": g.mean()})
    # END SOLUTION


# %%
try:
    tab = means_by_size(m)
except NotImplementedError:
    tab = pd.DataFrame(U.reference("d4_1", "tab"))
    tab.index = tab.index.astype(int)
U.keep("d4_1", "tab", tab.to_dict())
print(tab.round(1).to_string())
steps = tab["mean"].diff().iloc[1:6]
print(f"from one size to the next, among sizes 1 to 6, the mean rises by {steps.min():.0f} to {steps.max():.0f} litres")
U.check(int(tab["n"].sum()) == 2000 and tab["mean"].iloc[5] > tab["mean"].iloc[0] + 300, "mean consumption climbs steadily with household size")
plt = U.plt()
fig, ax = plt.subplots()
ax.scatter(x + U.rng(131).uniform(-0.2, 0.2, len(x)), y, s=5, alpha=0.3, color="#3a7ca5")
ax.plot(tab.index, tab["mean"], "o-", color="#e4572e", label="mean by household size")
ax.set(xlabel="people in the household", ylabel="consumption, litres a day", title="2,000 metered households")
ax.legend()
plt.show()

# %% [markdown]
# **Look at.** The red means climb in nearly equal steps: a straight line will summarise them well. And the cloud widens to the right: large households differ more from one another than small ones. Lab 4.2 comes back to that.

# %% [markdown]
# ## 2 · Fit the line by least squares (6')
#
# The least-squares line is the one that makes the sum of squared vertical distances to the points as small as possible. For one variable:
#
# slope = covariance(x, y) / variance(x), intercept = mean(y) - slope × mean(x).
#
# ✏️ **Exercise** · Write `fit_line(x, y)` returning `(intercept, slope)` from that formula.

# %%
def fit_line(x, y):
    # BEGIN SOLUTION
    slope = np.mean((x - x.mean()) * (y - y.mean())) / np.mean((x - x.mean()) ** 2)
    return float(y.mean() - slope * x.mean()), float(slope)
    # END SOLUTION


# %%
try:
    b0, b1 = fit_line(x, y)
except NotImplementedError:
    b0, b1 = U.reference("d4_1", "line")
U.keep("d4_1", "line", [b0, b1])
check = np.polyfit(x, y, 1)
print(f"fitted line: consumption = {b0:.1f} + {b1:.2f} × people")
U.check(abs(b1 - check[0]) < 1e-6 and abs(b0 - check[1]) < 1e-6, "the formula agrees with np.polyfit")

# %% [markdown]
# ## 3 · The slope in litres a day and cubic metres a month (5')
#
# Zulal bills in cubic metres a month. 1 cubic metre = 1,000 litres; take a month of 30 days.
#
# ✏️ **Exercise** · Write `manager_units(slope)` returning `(litres_per_day, cubic_metres_per_month)`, each for one additional person.

# %%
def manager_units(slope):
    # BEGIN SOLUTION
    return float(slope), float(slope * 30 / 1000)
    # END SOLUTION


# %%
try:
    lpd, m3 = manager_units(b1)
except NotImplementedError:
    lpd, m3 = U.reference("d4_1", "units")
U.keep("d4_1", "units", [lpd, m3])
print(f"\"Among these households, one more person goes with about {lpd:.0f} litres more a day, about {m3:.1f} cubic metres more a month.\"")
U.check(abs(m3 - b1 * 0.03) < 1e-9 and 2.5 < m3 < 3.3, "about 3 cubic metres a month for each additional person")

# %% [markdown]
# **Look at.** "Goes with", not "causes". The line compares different households of different sizes. It does not follow one household as a person moves in.

# %% [markdown]
# ## 4 · Predict for 2 and 6 people; read the intercept (4')
#
# ✏️ **Exercise** · Write `predict(b0, b1, people)`.

# %%
def predict(b0, b1, people):
    # BEGIN SOLUTION
    return b0 + b1 * people
    # END SOLUTION


# %%
try:
    p2, p6 = float(predict(b0, b1, 2)), float(predict(b0, b1, 6))
except NotImplementedError:
    p2, p6 = U.reference("d4_1", "pred")
U.keep("d4_1", "pred", [p2, p6])
print(f"line: 2 people {p2:.0f} litres, 6 people {p6:.0f} litres; observed means: {tab.loc[2, 'mean']:.0f} and {tab.loc[6, 'mean']:.0f}")
print(f"the intercept, {b0:.0f} litres, is the line's value for a household of zero people: no such household exists")
U.check(abs((p6 - p2) - 4 * b1) < 1e-6, "four more people, four slopes more")

# %% [markdown]
# **Look at.** The intercept is where the line crosses the axis, not a measurement. Read it only as "the part of consumption that does not scale with people" and do not predict outside the sizes you observed.

# %% [markdown]
# ## 5 · Compare with the population line (5')

# %%
pop = U.households()
B0, B1 = np.polyfit(pop["household_size"], pop["consumption_l_day"], 1)[::-1]
U.keep("d4_1", "population_line", [float(B0), float(B1)])
print(f"your sample of 2,000: {b0:.1f} + {b1:.2f} × people")
print(f"all 80,000:           {B0:.1f} + {B1:.2f} × people")
print(f"your slope misses the population slope by {b1 - B1:+.2f} litres per person")
U.check(abs(b1 - B1) < 6, "the sample slope lands within a few litres of the population slope")

# %% [markdown]
# **Look at.** The slope is a statistic like any other: another sample of 2,000 gives another slope. It needs an interval, and lab 4.2 builds it.

# %% [markdown]
# ## ✱ Stretch · The same line from a statistics library
#
# Fit `consumption_l_day ~ household_size` with statsmodels and find the slope, its standard error and R² in the summary.

# %%
def stretch():
    # BEGIN SOLUTION
    import statsmodels.formula.api as smf
    fit = smf.ols("consumption_l_day ~ household_size", data=m).fit()
    print(fit.summary().tables[1])
    print(f"R squared: {fit.rsquared:.3f}: household size accounts for {fit.rsquared:.0%} of the variation in consumption")
    return [float(fit.params["household_size"]), float(fit.bse["household_size"]), float(fit.rsquared)]
    # END SOLUTION


try:
    U.keep("d4_1", "library", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the truth: sample slope {b1:.2f}, population slope {B1:.2f} litres a day per person.",
       "Checked: the formula against np.polyfit.",
       "Not checked: whether household size is the reason. Session 3 shows that part of this slope belongs to temperature.")

# %% [markdown]
# ## Checkpoint
#
# 1. The slope is 98 litres a day per person. A household of 5 uses how much more than a household of 3, on average?
#    <details><summary>Answer</summary>About 196 litres a day more.</details>
# 2. Can you use the line for a compound of 40 people on one meter?
#    <details><summary>Answer</summary>No. The data stop at 12 people; beyond that the line is a guess.</details>
# 3. A new baby arrives in a household of 3. Does its consumption rise by 98 litres?
#    <details><summary>Answer</summary>The line does not say. It compares households of different sizes; it does not follow one household through a change.</details>
#
# ## Carry forward
#
# The slope, about 98 litres per person, is the estimate that lab 4.2 puts an interval around and lab 4.3 revises.
