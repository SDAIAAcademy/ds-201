<!-- academy:title -->
# Statistical Inference by Simulation

الاستدلال الإحصائي بالمحاكاة

Data Science Track · SDAIA Academy · DS-201 · Level 200

REPLACE: one line under the title: what participants can do after the course

Participants learn inference by computing it. On synthetic data from a fictional water utility whose true population is known, they draw repeated samples, build bootstrap intervals, run permutation tests beside classical ones, and report effect sizes with intervals instead of bare p-values. They see how testing 30 districts at once produces false findings and correct for it, then fit and read a first linear regression.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

**Course page:** https://sdaiaacademy.github.io/ds-201/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Explain what a sampling distribution, a standard error, a confidence interval and a p-value describe, and identify common misreadings, given eight statements from utility reports | Awareness | a marked sheet with reasons, at least six of eight correct |
| LO2 | Compute bootstrap intervals for a mean, a median and a group difference, resampling the correct unit, given skewed repair times with the population known | Applied | each interval with its coverage over 1,000 simulated samples |
| LO3 | Implement a permutation test, compare it with the matching classical test and report an effect size with an interval, given satisfaction scores for two contractors | Applied | a script reporting both p-values and the effect size |
| LO4 | Apply family-wise and false discovery rate corrections to many tests and measure the false findings without them, given 30 districts of unequal size, five with a planted difference | Applied | true and false discoveries under no correction, Holm and Benjamini-Hochberg |
| LO5 | Analyse a linear regression of water consumption on household size and temperature, with slope intervals and residual checks, given 2,000 synthetic metered households | Applied | a regression summary, a residual plot and a two-sentence interpretation |
| LO6 | Deliver an inference brief that answers a manager's question with an estimate, an interval, a test, an effect size and stated limits, given a question and a dataset not seen in class | Performance | a two-page brief and a notebook that reruns from raw data, defended live |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Day 1 | Variation | A sample is one draw of many; Standard error by simulation and by formula; Skew, outliers and the median; Describing a sample honestly | [`slides/day1.html`](slides/day1.html) |
| Day 2 | Intervals | The bootstrap idea; Coverage is a testable claim; Resample the right unit; Intervals for differences and ratios | [`slides/day2.html`](slides/day2.html) |
| Day 3 | Tests | A test is a shuffling rule; p-values and their misreadings; Effect size and practical significance; Thirty districts, many false alarms | [`slides/day3.html`](slides/day3.html) |
| Day 4 | Regression and reporting | Least squares as a summary; Slopes with intervals; Residuals and confounding; Writing an inference brief | [`slides/day4.html`](slides/day4.html) |
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Draw 1,000 samples of 50 households and plot their means | [`D1_1_draw_1_000.ipynb`](labs/D1_1_draw_1_000.ipynb) |
| 1.2 | Day 1 · Session 2 | Compare simulated and formula standard errors at three sample sizes | [`D1_2_compare_simulated_formula.ipynb`](labs/D1_2_compare_simulated_formula.ipynb) |
| 1.3 | Day 1 · Session 3 | Measure how one extreme repair time moves mean and median | [`D1_3_measure_how_one.ipynb`](labs/D1_3_measure_how_one.ipynb) |
| 1.4 | Day 1 · Session 4 | Summarise repair times in five numbers and a histogram | [`D1_4_summarise_repair_times.ipynb`](labs/D1_4_summarise_repair_times.ipynb) |
| 2.1 | Day 2 · Session 1 | Bootstrap the median repair time and compare with the truth | [`D2_1_bootstrap_median_repair.ipynb`](labs/D2_1_bootstrap_median_repair.ipynb) |
| 2.2 | Day 2 · Session 2 | Count how often two interval methods cover the truth in 500 studies | [`D2_2_count_how_often.ipynb`](labs/D2_2_count_how_often.ipynb) |
| 2.3 | Day 2 · Session 3 | Bootstrap satisfaction by household and by district; explain the difference | [`D2_3_bootstrap_satisfaction_household.ipynb`](labs/D2_3_bootstrap_satisfaction_household.ipynb) |
| 2.4 | Day 2 · Session 4 | Build intervals for the difference and ratio of contractor medians | [`D2_4_build_intervals_difference.ipynb`](labs/D2_4_build_intervals_difference.ipynb) |
| 3.1 | Day 3 · Session 1 | Run a permutation test and compare its p-value with a t-test | [`D3_1_run_permutation_test.ipynb`](labs/D3_1_run_permutation_test.ipynb) |
| 3.2 | Day 3 · Session 2 | Mark eight report sentences about p-values right or wrong, with reasons | [`D3_2_mark_eight_report.ipynb`](labs/D3_2_mark_eight_report.ipynb) |
| 3.3 | Day 3 · Session 3 | Report the contractor effect with an interval against the utility's threshold | [`D3_3_report_contractor_effect.ipynb`](labs/D3_3_report_contractor_effect.ipynb) |
| 3.4 | Day 3 · Session 4 | Test 30 districts with and without correction; note where small districts land | [`D3_4_test_30_districts.ipynb`](labs/D3_4_test_30_districts.ipynb) |
| 4.1 | Day 4 · Session 1 | Fit consumption on household size; state the slope in a manager's units | [`D4_1_fit_consumption_household.ipynb`](labs/D4_1_fit_consumption_household.ipynb) |
| 4.2 | Day 4 · Session 2 | Bootstrap the slope and compare with the reported standard error | [`D4_2_bootstrap_slope_compare.ipynb`](labs/D4_2_bootstrap_slope_compare.ipynb) |
| 4.3 | Day 4 · Session 3 | Add temperature, plot residuals and explain why the slope moved | [`D4_3_add_temperature_plot.ipynb`](labs/D4_3_add_temperature_plot.ipynb) |
| 4.4 | Day 4 · Session 4 | Draft an estimate, interval and limits paragraph; choose the capstone question | [`D4_4_draft_estimate_interval.ipynb`](labs/D4_4_draft_estimate_interval.ipynb) |
<!-- /academy:labs -->

## Capstone

An inference brief on one of three synthetic questions or an approved public dataset, in a public repository whose README reports estimates, intervals, tests, effect sizes and a coverage check; eight-minute defence plus questions

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

## Prerequisites

- FN-101 Python for Data and AI Work
- FN-103 Mathematics for Machine Learning: Vectors, Gradients and Probability
- Filters and groups a table with a dataframe library
- Computes a mean, a standard deviation and a simple probability

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Analysis environment and notebooks:** Python with uv and JupyterLab or marimo, R with Quarto
- **Arrays, statistics and resampling:** NumPy, SciPy and statsmodels, R with the infer package
- **Plotting:** Matplotlib, Vega-Altair, ggplot2
- **Hint-only course tutor:** a locally served open-weight model with a tutor instruction, an approved assistant in a study mode
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->

### National references

- Personal Data Protection Law and its implementing regulations: REPLACE: the address of the official text
- NDMO Open Data Policy: REPLACE: the address of the official text
