---
course: "Statistical Inference by Simulation"
code: "DS-201"
version: "2027.1.0"
deck: "day4"
day: 4
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-201/slides/day4.html"
---

# Statistical Inference by Simulation

## Day 4: Regression and reporting

A line summarises how one quantity moves with another; its slope needs an interval, its residuals a look, and its reader a brief

#### [day4#title] Regression and reporting

*SDAIA Academy · Statistical Inference by Simulation*

Day 4: A line summarises how one quantity moves with another; its slope needs an interval, its residuals a look, and its reader a brief

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-201

#### [day4#agenda] Regression and reporting

*Today*

- **Session 1 · Least squares as a summary**: A fitted line is a summary of group averages, and its slope is a number in the manager's units
- **Session 2 · Slopes with intervals**: A slope is a statistic: it has a sampling distribution, a bootstrap interval and a reported standard error that rests on an assumption
- **Session 3 · Residuals and confounding**: Residuals show what the line missed; a second variable can move the first slope, and that is confounding
- **Session 4 · Writing an inference brief**: The brief a manager can act on: the question, the estimate, the interval, the test, the effect size and the limits

#### [day4#review-day3] How many of these flags can you trust?

*Review of Day 3*

**Question:** A monthly report tests 20 service counters against the average at the 0.05 level and flags one. No correction is applied. What is the fair reading of the single flag?

- A. It may well be a false alarm: 20 tests of counters that do not differ give one flag on average
- B. It has a 5% chance of being a false alarm
- C. The counter certainly differs from the others
- D. It must be ignored, since uncorrected tests mean nothing

### Session 1: Least squares as a summary

#### [day4#s1] Least squares as a summary

*Session 1*

- Fit a line by least squares and read its slope and intercept
- Translate a slope into the units a manager uses
- Separate a description of a pattern from a claim about cause

#### [day4#planning-question] "How much more water for each additional person?"

*Jamila's question*

- A new housing scheme for large families needs a supply estimate.
- Until now every question was about one variable, or one variable in two groups.
- This one is about how one quantity **moves with** another: consumption with household size.

- **The data.** 2,000 metered households drawn at random from the 80,000: household size, summer temperature of the area, litres a day.

#### [day4#line-through-means] A fitted line is a summary of the group averages

*Lab 4.1, steps 1 and 2*

Figure: 2,000 households: mean consumption at each household size, and the least-squares line.

- From one size to the next, the mean rises by 88 to 107 litres.
- One line replaces twelve means with two numbers: where it starts and how steeply it climbs.
- consumption = 63.7 + 98.48 × people.

#### [day4#least-squares] Least squares picks the line with the smallest squared misses

*How the line is chosen*

```python
def fit_line(x, y):
    dx, dy = x - x.mean(), y - y.mean()
    slope = (dx * dy).mean() / (dx ** 2).mean()
    intercept = y.mean() - slope * x.mean()
    return intercept, slope
```

- slope = covariance(x, y) / variance(x).
- The line always passes through the point of the two means.
- The same line as `np.polyfit(x, y, 1)`, and as the projection of FN-103.

#### [day4#slope-in-units] A slope is only useful in the manager's units

*Lab 4.1, step 3*

- **98.48** the coefficient in the output
- **98 litres** more a day for each additional person
- **3.0 m³** more a month: what a bill is counted in

> **The sentence.** "Among these households, one more person goes with about 98 litres more a day, about 3.0 cubic metres more a month."

#### [day4#intercept-and-range] Predict inside the range you observed; read the intercept with care

*Lab 4.1, step 4*

| household of | line | observed mean |
| --- | --- | --- |
| 2 people | 261 | 252 |
| 6 people | 655 | 659 |
| 0 people | 64 | none exists |
| 40 people | 4,003 | none observed |

- The **intercept**, 64 litres, is where the line meets the axis, not a measurement.
- The data stop at 12 people. Beyond that the line is a guess with a formula.

#### [day4#goes-with-not-causes] "Goes with" is not "causes"

*What the line does not say*

- **What was compared.** Different households of different sizes, at one moment.
- **What was not observed.** One household before and after a person moved in.

- Households of different sizes may differ in other ways too: where they live, the kind of home, a garden.
- Whatever travels with household size is folded into the 98 litres. Session 3 finds one such thing.

#### [day4#sample-and-population-line] The slope is a statistic: another sample gives another slope

*Lab 4.1, step 5*

|  | intercept | slope, litres per person |
| --- | --- | --- |
| your sample of 2,000 | 63.7 | 98.48 |
| all 80,000 households | 71.4 | 96.21 |
| the miss |  | +2.27 |

- Household size accounts for 79% of the variation in consumption (R² = 0.792).
- The slope needs an interval, like every estimate this week.

#### [day4#check-reading-slope] What does this slope tell the planner?

*Checkpoint*

**Question:** For 1,500 shops, monthly water use in cubic metres is regressed on floor area in square metres: use = 4.0 + 0.12 × area. The shops range from 20 to 400 square metres. Which statement is supported?

- A. Extending a shop by 100 square metres will raise its use by 12 cubic metres
- B. A warehouse of 5,000 square metres uses about 604 cubic metres
- C. A shop with no floor area uses 4 cubic metres
- D. Among these shops, one that is 100 square metres larger uses about 12 cubic metres more on average

#### [day4#lab-4-1] Consumption on household size

Lab 4.1 · 25 min

Fit daily consumption on household size for 2,000 metered households, state the slope in litres a day and cubic metres a month, and compare the line with the one the whole population gives.

[D4_1_fit_line.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D4_1_fit_line.ipynb)

- [ ] Scatter and mean consumption by household size (5 min)
- [ ] Fit the line by least squares (6 min)
- [ ] The slope in litres a day and cubic metres a month (5 min)
- [ ] Predict for 2 and 6 people; read the intercept (4 min)
- [ ] Compare with the population line (5 min)
- [ ] ✱ Stretch: Fit the same line with a statistics library and find the slope in its summary

### Session 2: Slopes with intervals

#### [day4#s2] Slopes with intervals

*Session 2*

- Bootstrap a regression slope by resampling households
- Compare a bootstrap standard error with the one a library reports
- Explain which assumption makes the two differ

#### [day4#slope-varies] A slope has a sampling distribution and a standard error

*Day 1, for a slope*

- Your sample says 98.48 litres per person. The population says 96.21.
- Everything from Days 1 and 2 applies: the slope's spread over samples is its standard error, and an interval is built from it.
- Two routes again: a formula in the library, and a bootstrap.

```text
             coef  std err      t  [0.025  0.975]
Intercept  63.739    5.160  12.35  53.620  73.858
size       98.479    1.128  87.27  96.266 100.692
```

#### [day4#pairs-bootstrap] Bootstrap the households: each one keeps its pair of values

*Lab 4.2, step 2*

```python
idx = gen.integers(0, n, size=(B, n))
xs, ys = x[idx], y[idx]   # pairs stay together
xc = xs - xs.mean(axis=1, keepdims=True)
yc = ys - ys.mean(axis=1, keepdims=True)
num = (xc * yc).mean(axis=1)
slopes = num / (xc ** 2).mean(axis=1)
```

- The unit drawn at random is the household, so the household is resampled: its size and its consumption together.
- Resample x and y separately and the relation is destroyed: every slope comes out near zero.
- 2,000 slopes: standard deviation 1.409.

#### [day4#two-standard-errors] The library's standard error is a fifth too small

*Lab 4.2, step 3*

| method | standard error | 95% interval | width |
| --- | --- | --- | --- |
| reported by the library | 1.13 | 96.27 to 100.69 | 4.42 |
| bootstrap of households | 1.41 | 95.66 to 101.23 | 5.57 |

- The bootstrap standard error is 25% larger; put the other way, the library's is 20% smaller.
- The population slope, 96.21, is inside the bootstrap interval and just outside the reported one.
- They disagree for a reason you can see in the data.

#### [day4#equal-spread-assumption] The formula assumes equal spread around the line; the data do not have it

*Lab 4.2, step 4*

Figure: Standard deviation of the residuals at each household size.

- Households of 8 scatter twice as widely around the line as households of 1: 133 against 67 litres.
- Large households sit at the end of the line, where a point has most pull on the slope, and they are the noisiest.
- The formula averages the noise over everyone and understates the swing.

#### [day4#slope-coverage] Counted over 300 samples, the bootstrap interval keeps the promise

*Lab 4.2, step 5*

| Item | Value |
| --- | --- |
| reported interval | 92.0% |
| bootstrap interval | 95.0% |
| promised | 95% |

- Libraries can drop the assumption too: the robust standard error (HC3) is 1.402, the bootstrap's 1.409.
- When the reported and the robust standard errors differ, report the robust one and say why.

#### [day4#reading-regression-output] Read a regression table in this order

*In practice*

1. **The coefficient, with units:** 98 litres a day per person.
2. **Its interval:** 95.7 to 101.2 by bootstrap. Is the whole interval large enough, or small enough, to matter?
3. **Where the standard error comes from:** the default formula, a robust one, or a bootstrap.
4. **The p-value last:** it tests "slope is exactly zero", which is rarely the question.

#### [day4#check-which-se] Which standard error goes in the brief?

*Checkpoint*

**Question:** A regression of monthly bill on meter size gives a slope of 41 riyals per size step. The library reports a standard error of 2.0; a bootstrap of customers gives 3.1. A plot shows bills scattering far more widely for large meters. What should the analyst report?

- A. 2.0, because the library's formula is the standard method
- B. 3.1, because the spread is unequal and the bootstrap does not assume otherwise
- C. About 2.5, the middle of the two
- D. Neither: the slope cannot be trusted when spreads differ

#### [day4#lab-4-2] An interval for the slope

Lab 4.2 · 25 min

Bootstrap the slope of consumption on household size 2,000 times, compare its standard error and interval with the ones the regression summary reports, and find out from the residual spread why they differ.

[D4_2_slope_interval.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D4_2_slope_interval.ipynb)

- [ ] Read the reported standard error of the slope (4 min)
- [ ] Bootstrap the pairs: 2,000 slopes (8 min)
- [ ] Compare the two standard errors and intervals (5 min)
- [ ] Why they differ: the spread by household size (4 min)
- [ ] Coverage of both intervals over 300 samples (4 min)
- [ ] ✱ Stretch: Ask the library for a robust standard error and compare

### Session 3: Residuals and confounding

#### [day4#s3] Residuals and confounding

*Session 3*

- Read a residual plot for curvature and unequal spread
- Add a second variable and explain why the first slope moved
- State what a regression on observed data cannot settle

#### [day4#residuals-are-evidence] A residual is what the model missed, and patterns in residuals are evidence

*What the line left behind*

- **No pattern.** A level band around zero: the model has captured what is systematic.
- **A trend or a curve.** Against some variable the residuals rise, fall or bend: something systematic is missing.
- **A funnel.** The band widens: unequal spread. The slopes stand, the default standard errors do not.

residual = observed - fitted. Plot the residuals against the fitted values, against each variable in the model, and against variables you left out.

#### [day4#residuals-vs-temperature] The residuals of the one-variable line rise with temperature

*Lab 4.3, step 1*

**17.0** litres of residual for each degree of summer temperature

- In hot areas the line is too low; in mild areas too high.
- Hot districts use more water per household: cooling, gardens, evaporation.
- Temperature was in the file all along. The model never asked.

#### [day4#slope-moved] Add temperature, and the slope on household size drops by 12 litres

*Lab 4.3, step 2*

| model | litres per person | litres per degree | R² |
| --- | --- | --- | --- |
| household size alone | 98.48 |  | 0.792 |
| household size and temperature | 86.19 | 19.84 | 0.865 |

- The move, 12.3 litres, is about nine times the slope's standard error (1.32, robust).
- No interval around 98 warned of it: an interval measures sampling error, and this is not sampling error.
- It is a different question getting a different answer.

#### [day4#confounding] Household size and temperature travel together: that is confounding

*Lab 4.3, step 4*

1. **Summer temperature** hot areas have larger households (5.19 people against 3.37 in mild areas)
2. **Household size** the variable you looked at
3. **Consumption** pushed up by both

- Correlation of household size with temperature: 0.38.
- Comparing households by size alone compares, in part, hot areas with mild ones.
- The one-variable slope credited people with litres that belong to the heat.
- The move is predictable: 19.84 litres per degree × 0.619 degrees per additional person = 12.3.

#### [day4#held-fixed] Both slopes are right, for different questions

*Which slope is right?*

| The question | The slope | Why |
| --- | --- | --- |
| How much more water for a family of 6 than of 4 **in the coastal scheme**? | 86 per person: about 172 litres a day | One area, so temperature is held fixed |
| How much more do Zulal's large households use than its small ones, **wherever they live**? | 98 per person | That comparison includes where large households live |

> **"Holding temperature fixed"** is what the second variable does: 86 litres compares households of different sizes in areas equally hot.

#### [day4#what-regression-cannot] The new residuals are flat; the list of confounders is never known to be complete

*Lab 4.3, steps 3 and 5*

- Trend of the new residuals in temperature: 0.0 litres per degree.
- The funnel remains: hence the robust standard error.
- A variable nobody measured may still be mixed in.

- "Among households in areas of the same summer temperature, one more person goes with about **86** litres more a day (95% interval **84 to 89**), and each degree with about 20 litres more. These are comparisons between different households, not the effect of adding a person to a home, and differences between areas that we did not measure may still be mixed into both numbers."

#### [day4#check-why-slope-moves] Why did the slope move?

*Checkpoint*

**Question:** Across 900 branches, sales are regressed on the number of staff: 12,000 riyals per staff member. When the size of the branch's town is added, the slope on staff falls to 7,000. Which explanation fits?

- A. The first slope was imprecise because the sample was too small
- B. Adding a variable always shrinks the other slopes
- C. Branches in larger towns have more staff and sell more for other reasons too
- D. The second model is wrong, since staff clearly drive sales

#### [day4#lab-4-3] Add temperature

Lab 4.3 · 25 min

Plot the residuals of the one-variable fit against temperature, add temperature to the model, plot the residuals again and explain why the slope on household size moved.

[D4_3_residuals_confounding.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D4_3_residuals_confounding.ipynb)

- [ ] Residuals of the one-variable fit against temperature (5 min)
- [ ] Add temperature and refit (6 min)
- [ ] The residual plot of the new model (5 min)
- [ ] Why the slope moved: size and temperature travel together (5 min)
- [ ] The two-sentence interpretation (4 min)
- [ ] ✱ Stretch: Predict the size of the move from the two fits and check it

### Session 4: Writing an inference brief

#### [day4#s4] Writing an inference brief

*Session 4*

- Turn a manager's question into an estimand
- Write an estimate, an interval and the limits in one paragraph
- State the population a conclusion applies to

#### [day4#what-a-brief-is] An inference brief answers one question on two pages

*The product of this course*

1. **Question** in the manager's words, then as an estimand
2. **Estimate** with its interval
3. **Test** and the effect size against a threshold
4. **Limits** the population, the unit, what the data cannot tell

Behind it: a notebook that reruns from the raw file with a seed, and a README with a coverage check of the interval method.

#### [day4#question-to-estimand] Turn the question into an estimand: one number in a named population

*Before any computing*

| The manager says | The estimand |
| --- | --- |
| "What share of repairs meet the 24-hour standard?" | The share of this year's 12,000 repairs that took 24 hours or less |
| "Is one contractor better at it?" | The difference between the contractors in that share |
| "Did the message reduce consumption?" | The difference between message and control neighbourhoods in the mean change of litres a day per household |

> **Write it before you open the data.** With the unit you will resample and the comparisons you will make: that is the analysis plan of Day 3.

#### [day4#share-is-a-mean] A new question needs no new method: a share is a mean of zeros and ones

*Lab 4.4, steps 1 and 2*

| 400 sampled repairs | estimate | 95% interval |
| --- | --- | --- |
| share within 24 hours | 94.5% | 92.0% to 96.5% |
| gap, contractor A minus B | +1.6 points | -2.9 to +6.1 |

- Bootstrap for both intervals; a permutation test for the gap: p = 0.51.
- Truth, all 12,000 repairs: 95.2%. Inside the interval.
- Coverage of this interval method over 500 studies: 93.6%.

#### [day4#brief-paragraph] One paragraph: estimate, interval, comparison, population, limits

*Lab 4.4, step 3*

- "In a random sample of **400** of this year's 12,000 leak repairs, **94.5%** were completed within the 24-hour standard (95% interval **92.0% to 96.5%**). Contractor A met the standard more often than contractor B by **1.6** percentage points, a gap that could easily arise by chance (permutation p = **0.51**; 95% interval -2.9 to +6.1 points). The **population** is the repairs logged this year at Zulal, including tickets closed late in the system. The sample **cannot** tell a late repair from a late entry, and it cannot show that the contractors are equal: a gap of a few points either way remains possible."

#### [day4#limits-worth-stating] Limits worth stating fall into four kinds

*The part most briefs leave out*

- **Population.** Who the conclusion applies to: this year, these districts, surveyed households.
- **Sampling.** How units were drawn, the unit resampled, what a sample this size cannot detect.
- **Measurement.** What the recorded number is: a ticket closed late is not always a repair done late.
- **Comparison.** Was assignment by lot or by rota, or are the groups different in other ways?

> **What goes wrong.** A ritual sentence, "results should be interpreted with caution". A limit names what could be wrong and in which direction.

#### [day4#capstone-questions] Three questions you have not seen, each with a trap you have

*Lab 4.4, step 5*

- **q1 · Meter replacement.** Did smart meters reduce estimated bills? Rolled out in 8 of the 20 districts of the first phase.
- **q2 · Conservation message.** Did a monthly message cut consumption by at least 10 litres a day? 40 neighbourhoods, 20 by lot.
- **q3 · Call-back change.** Did complaints get resolved faster after the new rule, and for which of six types?

Or an approved public dataset. In the defence the assessor names a different resampling unit: you predict the effect on your interval, then show it.

#### [day4#check-brief] Which draft is an inference brief?

*Checkpoint*

**Question:** A trial sent a reminder letter to 3,000 customers chosen by lot; 3,000 others got none. Which draft could a manager act on?

- A. The letter worked: late payment differed significantly between the two groups of 3,000 (p = 0.004)
- B. Late payment was 2.1 points lower among the customers who got the letter than among the others
- C. We compared the groups with a permutation test and a bootstrap interval, both run with a fixed seed
- D. Late payment fell 2.1 points (95% interval 0.7 to 3.5; p = 0.004) among customers billed in March

#### [day4#lab-4-4] One paragraph of a brief

Lab 4.4 · 25 min

Answer a new question, the share of repairs finished inside the 24-hour standard, with an estimate, an interval and a contractor comparison, draft the paragraph with its limits, then choose a capstone question and write its estimand.

[D4_4_brief_paragraph.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D4_4_brief_paragraph.ipynb)

- [ ] A new question: the share inside the 24-hour standard (5 min)
- [ ] An interval and a contractor comparison (7 min)
- [ ] Draft the estimate, interval and limits paragraph (6 min)
- [ ] Check the paragraph against the numbers (3 min)
- [ ] Choose the capstone question and write its estimand (4 min)
- [ ] ✱ Stretch: Count the coverage of your interval method over 500 studies

#### [day4#wrap-up] What to keep

*Day 4 in three lines*

- **A slope in units.** "One more person goes with 98 litres more a day." A comparison between households, inside the range observed.
- **An honest interval.** Bootstrap the households or use a robust standard error. Then look at the residuals.
- **Name what is held fixed.** A second variable moved the slope to 86. State the question each slope answers, and the limits.

#### [day4#next] Capstone day

*Next*

A two-page brief on your question, a notebook that reruns from the raw file, and an eight-minute defence of one result.

- Start from `labs/capstone/README.md`: what the repository must hold, the coverage check, the rubric.
- Commit as you work: the history and the seeded run log are part of the evidence.
- After the course: an inference brief on a table of the national Open Data Platform within two weeks (`labs/followup`).
