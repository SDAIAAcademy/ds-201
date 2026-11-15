<!-- academy:title -->
# Statistical Inference by Simulation

الاستدلال الإحصائي بالمحاكاة

Data Science Track · SDAIA Academy · DS-201 · Level 200

Answer a manager's question with an estimate, an interval, a test and an effect size, each computed by simulation and checked against a known truth

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
| Capstone | Capstone: the inference brief and its defence |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**Zulal Water Utility (مرفق زلال للمياه).** Zulal Water Utility (مرفق زلال للمياه) is a fictional regional water utility whose whole population is on file: 80,000 metered households, 12,000 leak repairs by two contractors, 9,000 survey responses and 30 districts of unequal size, all synthetic and generated with a fixed seed. Because the truth is known, every interval and test in the labs is checked against it: repair times are skewed and hold twelve tickets left open for weeks, the survey has a district effect, five districts truly differ in repair time, and larger households live in hotter districts. Participants work as Shadin Al-Qaisi, a junior analyst answering questions from Jamila Al-Shuraim, head of customer operations; household keys are pseudonyms and results are reported by district only.

| Planted in the data | Found in |
|---|---|
| Skewed repair times and twelve tickets closed weeks late | Labs 1.3, 1.4 and 2.2 |
| A two-stage survey sample whose rows are not independent | Lab 2.3 |
| Contractor B slower than A by a known ratio | Lab 2.4 |
| A satisfaction gap between the contractors that is real and just under the contract's threshold | Labs 3.1 and 3.3 |
| Eight report sentences, five of them misreadings | Lab 3.2 |
| Five of 30 districts with a true difference in repair time, 25 without | Lab 3.4 |
| Consumption that rises with household size and temperature, with larger households in hotter districts and a spread that grows with size | Labs 4.1 to 4.3 |

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | One sample, then a thousand | [`D1_1_sampling_means.ipynb`](labs/D1_1_sampling_means.ipynb) |
| 1.2 | Day 1 · Session 2 | Standard error twice | [`D1_2_standard_error.ipynb`](labs/D1_2_standard_error.ipynb) |
| 1.3 | Day 1 · Session 3 | One ticket left open | [`D1_3_extreme_repair.ipynb`](labs/D1_3_extreme_repair.ipynb) |
| 1.4 | Day 1 · Session 4 | Five numbers and a histogram | [`D1_4_five_numbers.ipynb`](labs/D1_4_five_numbers.ipynb) |
| 2.1 | Day 2 · Session 1 | Bootstrap a median | [`D2_1_bootstrap_median.ipynb`](labs/D2_1_bootstrap_median.ipynb) |
| 2.2 | Day 2 · Session 2 | Count the coverage | [`D2_2_coverage.ipynb`](labs/D2_2_coverage.ipynb) |
| 2.3 | Day 2 · Session 3 | Household or district | [`D2_3_resampling_unit.ipynb`](labs/D2_3_resampling_unit.ipynb) |
| 2.4 | Day 2 · Session 4 | Difference and ratio of medians | [`D2_4_difference_ratio.ipynb`](labs/D2_4_difference_ratio.ipynb) |
| 3.1 | Day 3 · Session 1 | Shuffle the contractor labels | [`D3_1_permutation_test.ipynb`](labs/D3_1_permutation_test.ipynb) |
| 3.2 | Day 3 · Session 2 | Mark eight report sentences | [`D3_2_report_sentences.ipynb`](labs/D3_2_report_sentences.ipynb) |
| 3.3 | Day 3 · Session 3 | The effect against the threshold | [`D3_3_effect_threshold.ipynb`](labs/D3_3_effect_threshold.ipynb) |
| 3.4 | Day 3 · Session 4 | Thirty districts at once | [`D3_4_thirty_districts.ipynb`](labs/D3_4_thirty_districts.ipynb) |
| 4.1 | Day 4 · Session 1 | Consumption on household size | [`D4_1_fit_line.ipynb`](labs/D4_1_fit_line.ipynb) |
| 4.2 | Day 4 · Session 2 | An interval for the slope | [`D4_2_slope_interval.ipynb`](labs/D4_2_slope_interval.ipynb) |
| 4.3 | Day 4 · Session 3 | Add temperature | [`D4_3_residuals_confounding.ipynb`](labs/D4_3_residuals_confounding.ipynb) |
| 4.4 | Day 4 · Session 4 | One paragraph of a brief | [`D4_4_brief_paragraph.ipynb`](labs/D4_4_brief_paragraph.ipynb) |
<!-- /academy:labs -->

## Capstone

An inference brief on one of three synthetic questions or an approved public dataset, in a public repository whose README reports estimates, intervals, tests, effect sizes and a coverage check; eight-minute defence plus questions.

The three synthetic questions are a meter-replacement programme rolled out by district, a conservation-message pilot randomised by neighbourhood, and a change to complaint call-backs across six complaint types. Their data are in `labs/capstone/` and are not used in class.

**Submission:** A link to a public GitHub repository with a two-page brief, a notebook that reruns from the raw data with a fixed seed, and a README that reports the estimates, intervals, tests, effect sizes and a coverage check, with the commit history and the seeded run log. Then an eight-minute live defence of one result and four minutes of questions, in which the assessor names a different resampling unit and the participant predicts, then shows, the effect.

| Criterion | Weight |
|---|---|
| Question and estimand | 15 |
| Intervals and coverage | 25 |
| Tests and effect sizes | 25 |
| Regression and limits | 20 |
| Reproducibility | 15 |

## How the course is organised

- **Pre-work:** about two hours on sampling and plotting (`labs/P0_prework_sampling_plotting.ipynb`), then a supervised entry quiz without an assistant.
- **Four teaching days:** four sessions each; every session has about 25 minutes of concepts, one checkpoint and a 25-minute lab. Every lab draws a seeded sample from a population whose truth is known and ends with a verification note.
- **Capstone day:** an eight-minute defence of one result and four minutes of questions for each participant.
- **Follow-up:** an inference brief on a table of the national Open Data Platform within two weeks (`labs/followup/README.md`).
- **Assessment:** supervised entry quiz and exit check without an assistant (20%); the capstone repository on the rubric above (60%); the live defence of one result (20%). Passing needs 70% overall and at least 60% on both the capstone rubric and the supervised check. The items of the supervised checks are not in this repository; `assessments/bank.json` holds practice questions only.
- **Assistant policy:** off for quizzes and each day's first core computation; a hint-only tutor (`labs/tutor_instruction.md`) in the other lab steps; open in the capstone, which is defended live.
- **Responsible use:** the survey responses are synthetic and are handled as personal data: pseudonymised household keys, results by district or contractor only, and every brief states the population its conclusions apply to.

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

### National references

- [Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf)
- [Implementing Regulation of the Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf)
- [Open Data Policy (National Data Management Office, SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/OpenDataPolicy.pdf)
- [Open Data Platform (the follow-up task takes one of its tables)](https://open.data.gov.sa/en/home)

### Libraries used in the labs

- [NumPy: random generators and seeds](https://numpy.org/doc/stable/reference/random/generator.html)
- [SciPy: scipy.stats.bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)
- [SciPy: scipy.stats.permutation_test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html)
- [SciPy: scipy.stats.ttest_ind (Welch's t-test)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html)
- [statsmodels: multipletests (Holm, Benjamini-Hochberg)](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html)
- [statsmodels: linear regression](https://www.statsmodels.org/stable/regression.html)
- [statsmodels: robust covariance of a fitted regression](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLSResults.get_robustcov_results.html)
- [uv: Python projects and environments](https://docs.astral.sh/uv/)

### Reading on inference

- [Greenland and others (2016): Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations](https://link.springer.com/article/10.1007/s10654-016-0149-3)
- [Gelman and Loken (2013): The garden of forking paths](http://www.stat.columbia.edu/~gelman/research/unpublished/p_hacking.pdf)
- [Ismay, Kim and Valdivia: Statistical Inference via Data Science (ModernDive)](https://moderndive.com/)
- [Çetinkaya-Rundel and Hardin: Introduction to Modern Statistics](https://openintro-ims.netlify.app/)
<!-- /academy:sources -->

### The national references this course names

- Personal Data Protection Law and its implementing regulations: https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf and https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf
- NDMO Open Data Policy: https://sdaia.gov.sa/en/SDAIA/about/Documents/OpenDataPolicy.pdf
