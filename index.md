---
course: "Statistical Inference by Simulation"
code: "DS-201"
version: "2027.1.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-201/index.html"
---

# Statistical Inference by Simulation

الاستدلال الإحصائي بالمحاكاة

Data Science Track · 4 teaching days + capstone day · 26 hours · Level 200

Answer a manager's question with an estimate, an interval, a test and an effect size, each computed by simulation and checked against a known truth

Participants learn inference by computing it. On synthetic data from a fictional water utility whose true population is known, they draw repeated samples, build bootstrap intervals, run permutation tests beside classical ones, and report effect sizes with intervals instead of bare p-values. They see how testing 30 districts at once produces false findings and correct for it, then fit and read a first linear regression.

**Who it is for:** Practitioners. Graduates and early-career analysts who have completed the FN courses or passed the placement test, and analysts moving into data science.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**Zulal Water Utility.** Zulal Water Utility (مرفق زلال للمياه) is a fictional regional water utility whose whole population is on file: 80,000 metered households, 12,000 leak repairs by two contractors, 9,000 survey responses and 30 districts of unequal size, all synthetic and generated with a fixed seed. Because the truth is known, every interval and test in the labs is checked against it: repair times are skewed and hold twelve tickets left open for weeks, the survey has a district effect, five districts truly differ in repair time, and larger households live in hotter districts. Participants work as Shadin Al-Qaisi, a junior analyst answering questions from Jamila Al-Shuraim, head of customer operations; household keys are pseudonyms and results are reported by district only.

## The course

### Day 1: Variation

Slides: https://sdaiaacademy.github.io/ds-201/slides/day1.md

- **Session 1: A sample is one draw of many**
  - Distinguish a parameter of the population from a statistic of one sample
  - Draw repeated samples with a seed and collect a statistic from each
  - Describe a sampling distribution by its centre and its spread
  - [Lab 1.1: One sample, then a thousand (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D1_1_sampling_means.ipynb)
- **Session 2: Standard error by simulation and by formula**
  - Measure a standard error by simulation at several sample sizes
  - Compute the standard error of a mean from one sample
  - Separate the standard deviation of households from the standard error of a mean
  - [Lab 1.2: Standard error twice (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D1_2_standard_error.ipynb)
- **Session 3: Skew, outliers and the median**
  - Recognise skew from a histogram and from mean against median
  - Measure the effect of one extreme value on the mean, the median and a trimmed mean
  - Choose the summary that answers the question asked, and say why
  - [Lab 1.3: One ticket left open (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D1_3_extreme_repair.ipynb)
- **Session 4: Describing a sample honestly**
  - Summarise a skewed sample in five numbers and an interquartile range
  - Draw a histogram and state the bin width and the axis
  - Write a description that gives the count, the exclusions and the population
  - [Lab 1.4: Five numbers and a histogram (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D1_4_five_numbers.ipynb)

### Day 2: Intervals

Slides: https://sdaiaacademy.github.io/ds-201/slides/day2.md

- **Session 1: The bootstrap idea**
  - Explain why resampling the sample imitates sampling the population
  - Compute a percentile bootstrap interval for a median
  - Compare a bootstrap distribution with the real sampling distribution
  - [Lab 2.1: Bootstrap a median (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D2_1_bootstrap_median.ipynb)
- **Session 2: Coverage is a testable claim**
  - State what 95% coverage promises
  - Measure the coverage of two interval methods over simulated studies
  - Name two situations in which the bootstrap fails
  - [Lab 2.2: Count the coverage (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D2_2_coverage.ipynb)
- **Session 3: Resample the right unit**
  - Identify the sampling unit of a two-stage sample
  - Bootstrap by household and by district and compare the intervals
  - Show by coverage which unit keeps the promise
  - [Lab 2.3: Household or district (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D2_3_resampling_unit.ipynb)
- **Session 4: Intervals for differences and ratios**
  - Compute a bootstrap interval for a difference between two groups
  - Compute a bootstrap interval for a ratio
  - Read an interval for a comparison against no difference
  - [Lab 2.4: Difference and ratio of medians (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D2_4_difference_ratio.ipynb)

### Day 3: Tests

Slides: https://sdaiaacademy.github.io/ds-201/slides/day3.md

- **Session 1: A test is a shuffling rule**
  - State a null hypothesis as a shuffling rule
  - Implement a permutation test for a difference in means
  - Compare the permutation p-value with the matching classical test
  - [Lab 3.1: Shuffle the contractor labels (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D3_1_permutation_test.ipynb)
- **Session 2: p-values and their misreadings**
  - Explain what a p-value describes and what it does not
  - Identify five common misreadings of p-values and intervals
  - Check a claim about p-values by simulating studies with the truth known
  - [Lab 3.2: Mark eight report sentences (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D3_2_report_sentences.ipynb)
- **Session 3: Effect size and practical significance**
  - Report a raw and a standardised effect size with an interval
  - Place an interval against zero and against a practical threshold
  - Estimate Type I error and power by simulation
  - [Lab 3.3: The effect against the threshold (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D3_3_effect_threshold.ipynb)
- **Session 4: Thirty districts, many false alarms**
  - Measure the false findings of 30 uncorrected tests
  - Apply the Holm and Benjamini-Hochberg corrections
  - Explain why the smallest districts give the most extreme estimates
  - [Lab 3.4: Thirty districts at once (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D3_4_thirty_districts.ipynb)

### Day 4: Regression and reporting

Slides: https://sdaiaacademy.github.io/ds-201/slides/day4.md

- **Session 1: Least squares as a summary**
  - Fit a line by least squares and read its slope and intercept
  - Translate a slope into the units a manager uses
  - Separate a description of a pattern from a claim about cause
  - [Lab 4.1: Consumption on household size (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D4_1_fit_line.ipynb)
- **Session 2: Slopes with intervals**
  - Bootstrap a regression slope by resampling households
  - Compare a bootstrap standard error with the one a library reports
  - Explain which assumption makes the two differ
  - [Lab 4.2: An interval for the slope (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D4_2_slope_interval.ipynb)
- **Session 3: Residuals and confounding**
  - Read a residual plot for curvature and unequal spread
  - Add a second variable and explain why the first slope moved
  - State what a regression on observed data cannot settle
  - [Lab 4.3: Add temperature (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D4_3_residuals_confounding.ipynb)
- **Session 4: Writing an inference brief**
  - Turn a manager's question into an estimand
  - Write an estimate, an interval and the limits in one paragraph
  - State the population a conclusion applies to
  - [Lab 4.4: One paragraph of a brief (25 min)](https://sdaiaacademy.github.io/ds-201/labs/D4_4_brief_paragraph.ipynb)

### Capstone: Capstone: the inference brief and its defence

Slides: https://sdaiaacademy.github.io/ds-201/slides/capstone.md

## Capstone

An inference brief on one of three synthetic questions or an approved public dataset, in a public repository whose README reports estimates, intervals, tests, effect sizes and a coverage check; eight-minute defence plus questions

**What you submit:** A link to a public GitHub repository with a two-page brief, a notebook that reruns from the raw data with a fixed seed, and a README that reports the estimates, intervals, tests, effect sizes and a coverage check, with the commit history and the seeded run log. Then an eight-minute live defence of one result and four minutes of questions, in which the assessor names a different resampling unit and the participant predicts, then shows, the effect.

**Rubric:**

- Question and estimand: 15%
- Intervals and coverage: 25%
- Tests and effect sizes: 25%
- Regression and limits: 20%
- Reproducibility: 15%

## Outcomes

- **LO1** Explain what a sampling distribution, a standard error, a confidence interval and a p-value describe, and identify common misreadings, given eight statements from utility reports (Awareness) Evidence: a marked sheet with reasons, at least six of eight correct
- **LO2** Compute bootstrap intervals for a mean, a median and a group difference, resampling the correct unit, given skewed repair times with the population known (Applied) Evidence: each interval with its coverage over 1,000 simulated samples
- **LO3** Implement a permutation test, compare it with the matching classical test and report an effect size with an interval, given satisfaction scores for two contractors (Applied) Evidence: a script reporting both p-values and the effect size
- **LO4** Apply family-wise and false discovery rate corrections to many tests and measure the false findings without them, given 30 districts of unequal size, five with a planted difference (Applied) Evidence: true and false discoveries under no correction, Holm and Benjamini-Hochberg
- **LO5** Analyse a linear regression of water consumption on household size and temperature, with slope intervals and residual checks, given 2,000 synthetic metered households (Applied) Evidence: a regression summary, a residual plot and a two-sentence interpretation
- **LO6** Deliver an inference brief that answers a manager's question with an estimate, an interval, a test, an effect size and stated limits, given a question and a dataset not seen in class (Performance) Evidence: a two-page brief and a notebook that reruns from raw data, defended live

## Tools

- **Analysis environment and notebooks:** Python with uv and JupyterLab or marimo, R with Quarto
- **Arrays, statistics and resampling:** NumPy, SciPy and statsmodels, R with the infer package
- **Plotting:** Matplotlib, Vega-Altair, ggplot2
- **Hint-only course tutor:** a locally served open-weight model with a tutor instruction, an approved assistant in a study mode

## Prerequisites

- FN-101 Python for Data and AI Work
- FN-103 Mathematics for Machine Learning: Vectors, Gradients and Probability
- Filters and groups a table with a dataframe library
- Computes a mean, a standard deviation and a simple probability
- Pre-work: about two hours on sampling and plotting, labs/P0_prework_sampling_plotting.ipynb, before the supervised entry quiz
- Setup: a laptop with uv, or Google Colab. Nothing calls or downloads a model. Run 00_setup_check before Day 1; see labs/README.md.

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

---

SDAIA Academy · Data Science Track · Statistical Inference by Simulation

Course version 2027.1.0 · engine 1.0.0 · built 2026-11-15 · commit 705e303
