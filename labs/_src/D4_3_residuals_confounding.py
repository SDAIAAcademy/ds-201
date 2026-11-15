# %% [markdown]
# # Lab 4.3 · Add temperature
#
# Day 4 · Session 3 (Residuals and confounding) · 25 min.
#
# Jamila Al-Shuraim's new housing scheme is in a mild coastal district. Your line says 98 litres a day for each additional person. But Zulal's districts differ in summer temperature, and hot districts use more water for cooling and gardens. You look at what the line left unexplained, add temperature, and find that part of the "98 litres per person" was never about people.
#
# **AI policy.** AI-tutor: hints one step at a time, never the code.
#
# **Reference state.** `data/metered_2000.csv`, loaded fresh. Nothing from labs 4.1 or 4.2 is needed.
#
# **Tasks**
# - [ ] 1 · Residuals of the one-variable fit against temperature (5')
# - [ ] 2 · Add temperature and refit (6')
# - [ ] 3 · The residual plot of the new model (5')
# - [ ] 4 · Why the slope moved: size and temperature travel together (5')
# - [ ] 5 · The two-sentence interpretation (4')
# - [ ] ✱ Stretch · Predict the size of the move from the two fits and check it

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
import statsmodels.formula.api as smf
np.set_printoptions(precision=3, suppress=True)
print("mode:", U.MODE)

# %%
m = U.metered()
fit1 = smf.ols("consumption_l_day ~ household_size", data=m).fit()
S1 = float(fit1.params["household_size"])
print(f"one variable: consumption = {fit1.params['Intercept']:.1f} + {S1:.2f} × people")

# %% [markdown]
# ## 1 · Residuals of the one-variable fit against temperature (5')
#
# A **residual** is what the line missed: observed minus fitted. If the line had captured everything systematic, the residuals would show no pattern against anything.
#
# ✏️ **Exercise** · Write `residual_trend(residuals, other)`: the slope of the least-squares line of the residuals on another variable (`np.polyfit(other, residuals, 1)[0]`).

# %%
def residual_trend(residuals, other):
    # BEGIN SOLUTION
    return float(np.polyfit(other, residuals, 1)[0])
    # END SOLUTION


# %%
res1 = fit1.resid.to_numpy()
temp = m["temperature_c"].to_numpy()
try:
    trend1 = residual_trend(res1, temp)
except NotImplementedError:
    trend1 = U.reference("d4_3", "trend1")
U.keep("d4_3", "trend1", trend1)
plt = U.plt()
fig, ax = plt.subplots()
ax.scatter(temp, res1, s=5, alpha=0.3, color="#3a7ca5")
grid = np.array([temp.min(), temp.max()])
ax.plot(grid, np.polyval(np.polyfit(temp, res1, 1), grid), color="#e4572e")
ax.axhline(0, color="black", linewidth=1)
ax.set(xlabel="summer temperature of the household's area, °C", ylabel="residual, litres a day", title="What the one-variable line missed")
plt.show()
print(f"the residuals rise by {trend1:.1f} litres for each degree: the line is too low in hot areas and too high in mild ones")
U.check(trend1 > 10, "the residuals of the one-variable fit carry a clear trend in temperature")

# %% [markdown]
# ## 2 · Add temperature and refit (6')
#
# ✏️ **Exercise** · Fit `consumption_l_day ~ household_size + temperature_c` with `smf.ols(...).fit()` and return the fitted model.

# %%
def fit_two(m):
    # BEGIN SOLUTION
    return smf.ols("consumption_l_day ~ household_size + temperature_c", data=m).fit()
    # END SOLUTION


# %%
try:
    fit2 = fit_two(m)
    S2, T2 = float(fit2.params["household_size"]), float(fit2.params["temperature_c"])
    se2 = float(fit2.get_robustcov_results("HC3").bse[1])
    res2 = fit2.resid.to_numpy()
    r2 = [float(fit1.rsquared), float(fit2.rsquared)]
except NotImplementedError:
    S2, T2, se2, r2 = U.reference("d4_3", "two")
    res2 = res1 - T2 * (temp - temp.mean())
U.keep("d4_3", "two", [S2, T2, se2, r2])
print(f"two variables: {S2:.2f} litres per person (robust standard error {se2:.2f}), {T2:.2f} litres per degree")
print(f"the slope on household size moved from {S1:.2f} to {S2:.2f}: {S1 - S2:.1f} litres less per person")
print(f"R squared: {r2[0]:.3f} with size alone, {r2[1]:.3f} with temperature added")
U.check(8 < S1 - S2 < 16 and 17 < T2 < 23, "with temperature in the model, the slope per person drops by about 12 litres")

# %% [markdown]
# **Look at.** The move, about 12 litres, is many times the slope's standard error. No interval around 98 would have warned you: an interval measures sampling error, and this is not sampling error. It is a different question getting a different answer.

# %% [markdown]
# ## 3 · The residual plot of the new model (5')
#
# Two things to look for in a residual plot: a **trend or curve** (the model misses something systematic) and a **funnel** (the spread changes).

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].scatter(temp, res2, s=5, alpha=0.3, color="#3a7ca5")
axes[0].axhline(0, color="black", linewidth=1)
axes[0].set(xlabel="temperature, °C", ylabel="residual, litres a day", title="Against temperature: flat")
axes[1].scatter(m["household_size"] + U.rng(151).uniform(-0.2, 0.2, len(m)), res2, s=5, alpha=0.3, color="#3a7ca5")
axes[1].axhline(0, color="black", linewidth=1)
axes[1].set(xlabel="people in the household", title="Against household size: a funnel")
plt.show()
try:
    trend2 = residual_trend(res2, temp)
except NotImplementedError:
    trend2 = U.reference("d4_3", "trend2")
U.keep("d4_3", "trend2", trend2)
size = m["household_size"].to_numpy()
funnel = [float(res2[size <= 2].std()), float(res2[size >= 6].std())]
U.keep("d4_3", "funnel", funnel)
print(f"trend of the new residuals in temperature: {trend2:.2f} litres per degree (was {trend1:.1f})")
print(f"spread of the residuals: {funnel[0]:.0f} litres for households of 1 or 2, {funnel[1]:.0f} for households of 6 or more")
U.check(abs(trend2) < 1 and funnel[1] > 1.8 * funnel[0], "the trend is gone; the funnel remains, which is why the standard error above is the robust one")

# %% [markdown]
# ## 4 · Why the slope moved: size and temperature travel together (5')
#
# ✏️ **Exercise** · Write `link(m)`: return the correlation between `household_size` and `temperature_c`, and the mean household size in the mild areas (below 37 °C) and the hot areas (41 °C and above), as `(corr, mean_mild, mean_hot)`.

# %%
def link(m):
    # BEGIN SOLUTION
    corr = m["household_size"].corr(m["temperature_c"])
    mild = m.loc[m["temperature_c"] < 37, "household_size"].mean()
    hot = m.loc[m["temperature_c"] >= 41, "household_size"].mean()
    return float(corr), float(mild), float(hot)
    # END SOLUTION


# %%
try:
    corr, mild, hot = link(m)
except NotImplementedError:
    corr, mild, hot = U.reference("d4_3", "link")
U.keep("d4_3", "link", [corr, mild, hot])
print(f"correlation of household size with temperature: {corr:.2f}")
print(f"mean household size: {mild:.2f} people in mild areas, {hot:.2f} in hot areas")
U.check(corr > 0.25 and hot > mild + 0.8, "larger households live in hotter areas")

# %% [markdown]
# **Look at.** Hot areas have larger households **and** use more water per household for reasons of their own. Compare households by size alone and you compare, in part, hot areas with mild ones. The one-variable slope credited people with litres that belong to the heat. That is **confounding**: a third variable tied to both.

# %% [markdown]
# ## 5 · The two-sentence interpretation (4')
#
# ✏️ **Exercise** · Two sentences for Jamila. The first gives the slope per person with temperature held fixed, with its interval (slope ± 1.96 robust standard errors). The second says what the model cannot settle.

# %%
def my_interpretation():
    # BEGIN SOLUTION
    lo, hi = S2 - 1.96 * se2, S2 + 1.96 * se2
    return (f"Among households in areas of the same summer temperature, one more person goes with about {S2:.0f} litres more a day (95% interval {lo:.0f} to {hi:.0f}), "
            f"and each degree of summer temperature with about {T2:.0f} litres more. "
            f"These are comparisons between different households in 2,000 metered homes, not the effect of adding a person to a home, and other differences between areas that we did not measure may still be mixed into both numbers.")
    # END SOLUTION


# %%
try:
    text = my_interpretation()
except NotImplementedError:
    text = U.reference("d4_3", "text")
U.keep("d4_3", "text", text)
print(text)
U.brief_check(text, {"slope per person": f"{S2:.0f}", "low": f"{S2 - 1.96 * se2:.0f}", "high": f"{S2 + 1.96 * se2:.0f}"}, ["temperature"])

# %% [markdown]
# ## ✱ Stretch · Predict the move
#
# The move of the slope has a formula: (litres per degree) × (degrees of temperature per additional person). Fit `temperature_c ~ household_size`, take its slope, multiply by the temperature coefficient and compare with the move you saw.

# %%
def stretch():
    # BEGIN SOLUTION
    delta = float(smf.ols("temperature_c ~ household_size", data=m).fit().params["household_size"])
    print(f"each additional person goes with {delta:.3f} °C; {T2:.2f} × {delta:.3f} = {T2 * delta:.2f}; the slope moved by {S1 - S2:.2f}")
    return [delta, T2 * delta]
    # END SOLUTION


try:
    U.keep("d4_3", "predicted_move", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
pop = U.households()
pt = smf.ols("consumption_l_day ~ household_size + temperature_c", data=pop).fit().params
U.note(f"Checked against the truth: in all 80,000 households the two-variable slopes are {pt['household_size']:.1f} litres per person and {pt['temperature_c']:.1f} per degree; yours: {S2:.1f} and {T2:.1f}.",
       "The generator used 85 litres per person and 20 per degree: the two-variable model recovers what was planted, the one-variable model did not.",
       "Not checked, and not checkable from data alone: in real data you never know that the list of confounders is complete.")

# %% [markdown]
# ## Checkpoint
#
# 1. The slope fell from 98 to 86 when temperature was added. Which number answers "how much more water for a family of 6 than of 4 in the coastal scheme"?
#    <details><summary>Answer</summary>86 per person: the scheme is in one area, so temperature is held fixed. About 172 litres a day.</details>
# 2. And "how much more water do Zulal's large households use than its small ones, wherever they live"?
#    <details><summary>Answer</summary>98 per person: that comparison includes the fact that large households live in hotter areas. Both slopes are right for their question.</details>
# 3. The residuals fan out with household size. Which part of the regression output does that put in doubt?
#    <details><summary>Answer</summary>The reported standard errors, not the slopes. Use a robust standard error or a bootstrap.</details>
#
# ## Carry forward
#
# A capstone brief with a regression states which variables were held fixed, and names one that could not be.
