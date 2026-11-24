---
course: "Statistical Inference by Simulation"
code: "DS-201"
version: "2027.2.0"
scope: "course"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-201/"
---

# Statistical Inference by Simulation

Answer a manager's question with an estimate, an interval, a test and an effect size, each computed by simulation and checked against a known truth

Participants learn inference by computing it. On synthetic data from a fictional water utility whose true population is known, they draw repeated samples, build bootstrap intervals, run permutation tests beside classical ones, and report effect sizes with intervals instead of bare p-values. They see how testing 30 districts at once produces false findings and correct for it, then fit and read a first linear regression.

- **Audience:** Practitioners. Graduates and early-career analysts who have completed the FN courses or passed the placement test, and analysts moving into data science.
- **Prerequisites:** FN-101 Python for Data and AI Work; FN-103 Mathematics for Machine Learning: Vectors, Gradients and Probability; Filters and groups a table with a dataframe library; Computes a mean, a standard deviation and a simple probability; Pre-work: about two hours on sampling and plotting, labs/P0_prework_sampling_plotting.ipynb, before the supervised entry quiz; Setup: a laptop with uv, or Google Colab. Nothing calls or downloads a model. Run 00_setup_check before Day 1; see labs/README.md.
- **Case study:** Zulal Water Utility: Zulal Water Utility (مرفق زلال للمياه) is a fictional regional water utility whose whole population is on file: 80,000 metered households, 12,000 leak repairs by two contractors, 9,000 survey responses and 30 districts of unequal size, all synthetic and generated with a fixed seed. Because the truth is known, every interval and test in the labs is checked against it: repair times are skewed and hold twelve tickets left open for weeks, the survey has a district effect, five districts truly differ in repair time, and larger households live in hotter districts. Participants work as Shadin Al-Qaisi, a junior analyst answering questions from Jamila Al-Shuraim, head of customer operations; household keys are pseudonyms and results are reported by district only.

## Outcomes

- LO1 (Awareness): Explain what a sampling distribution, a standard error, a confidence interval and a p-value describe, and identify common misreadings, given eight statements from utility reports
- LO2 (Applied): Compute bootstrap intervals for a mean, a median and a group difference, resampling the correct unit, given skewed repair times with the population known
- LO3 (Applied): Implement a permutation test, compare it with the matching classical test and report an effect size with an interval, given satisfaction scores for two contractors
- LO4 (Applied): Apply family-wise and false discovery rate corrections to many tests and measure the false findings without them, given 30 districts of unequal size, five with a planted difference
- LO5 (Applied): Analyse a linear regression of water consumption on household size and temperature, with slope intervals and residual checks, given 2,000 synthetic metered households
- LO6 (Performance): Deliver an inference brief that answers a manager's question with an estimate, an interval, a test, an effect size and stated limits, given a question and a dataset not seen in class

## Day 1: Variation

Before any interval or test: a sample is one draw of many, and its statistics move from draw to draw

#### [day1#title] Variation

*SDAIA Academy · Statistical Inference by Simulation*

Day 1: Before any interval or test: a sample is one draw of many, and its statistics move from draw to draw

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-201

#### [day1#agenda] Variation

*Today*

- **Session 1 · A sample is one draw of many**: Population and sample, parameter and statistic, and the distribution of a statistic over many samples
- **Session 2 · Standard error by simulation and by formula**: The standard error is the spread of a sampling distribution; one sample is enough to estimate it
- **Session 3 · Skew, outliers and the median**: Repair times are skewed: the mean follows the tail and the median stays with the typical repair
- **Session 4 · Describing a sample honestly**: A description a reader can trust: five numbers, a histogram with its choices stated, the count and what was left out

#### [day1#the-utility] Zulal Water Utility: a population you can see whole

*The case study*

- **80,000** metered households
- **12,000** leak repairs, two contractors
- **9,000** survey responses, scored 1 to 10
- **30** districts, from 700 to 10,079 households

You work as **Shadin Al-Qaisi**, junior analyst. **Jamila Al-Shuraim**, head of customer operations, asks the questions. Nizar Al-Khayyat owns the two repair contracts, Ilyas Al-Tuwaijri writes the district report, Wafa Al-Enezi is the data protection officer. The utility, its people and every record are fictional and generated with a fixed seed.

#### [day1#method] Compute the inference, then check it against the truth

*The method of this course*

1. **1 · Draw** a sample from the population, with a seed
2. **2 · Infer** an estimate, an interval or a test, from the sample alone
3. **3 · Check** against the population, over hundreds of repeats

| Part of the course | Assistant |
| --- | --- |
| Quizzes and each day's first core computation (labs 1.1, 2.1, 3.1, 4.1, and the marking in 3.2) | Off |
| The other lab steps and the stretch items | A tutor that hints one step at a time and never writes the simulation |
| The capstone | Free; the result is defended live |

#### [day1#setup-and-keys] One check proves the setup; two rules govern the data

*Before the first lab*

- **Setup check.** Open `00_setup_check.ipynb` in Colab or locally and run all cells. It imports the libraries, reads the four population files and prints their row counts.
  ```text
  uv sync
  uv run jupyter lab
  ```
- **Treated as personal data.** The survey is synthetic, and the course still handles it as personal data under the Personal Data Protection Law:
  - households appear only as pseudonymised keys
  - results are reported by district or contractor, never by household
  - every conclusion names the population it applies to

### Session 1: A sample is one draw of many

#### [day1#s1] A sample is one draw of many

*Session 1*

- Distinguish a parameter of the population from a statistic of one sample
- Draw repeated samples with a seed and collect a statistic from each
- Describe a sampling distribution by its centre and its spread

#### [day1#four-words] Four words separate what is true from what you saw

*The vocabulary*

|  | All of it | What you measured |
| --- | --- | --- |
| **The units** | **Population**: 80,000 households | **Sample**: the 50 whose meters you read |
| **The number** | **Parameter**: their mean, 470.4 litres a day | **Statistic**: the sample's mean, 458.8 |
| **How many values it has** | One, fixed, usually unknown | One per sample: it varies |

> **Inference** is a statement about the left column made from the right column, with a measure of how wrong it may be.

#### [day1#one-sample-misses] One sample of 50 lands near the truth, never on it

*Lab 1.1, step 2*

- **470.4** the parameter: mean litres a day, all households
- **458.8** the statistic: mean of one sample of 50
- **-11.5** the miss, which a real analyst cannot see

- The miss is not an error of method. Read 50 other meters and the number changes.
- The useful question is not "is 458.8 right?" but "how far do samples of 50 typically land?"

#### [day1#sampling-distribution] Do it 1,000 times and the misses form a distribution

*Lab 1.1, steps 3 and 4*

Figure: 1,000 samples of 50 households each. One bar counts samples, not households.

- This is the **sampling distribution** of the mean for n = 50.
- Centre 471.1: on the truth.
- Spread 29.6 litres, from 387.5 to 571.1.
- 49% of samples within 20 litres of the truth; 94% within 57.

#### [day1#three-distributions] Three distributions carry three different spreads

*Do not mix them up*

- **The population.** 80,000 households, from 30 to 1,536 litres a day. Standard deviation 206 litres. Skewed to the right.
- **One sample.** 50 households. Looks like a rough copy of the population. Its standard deviation is near 206 too.
- **The sampling distribution.** Means of many samples. Standard deviation 29.6 litres. Bell-shaped. You never see it in real work.

> **What goes wrong.** A report quotes the narrow third spread as if it described households, or the wide first one as if it described the estimate.

#### [day1#seeded-draws] A seeded generator makes every simulation repeatable

*The tool*

```python
gen = np.random.default_rng(201)

def sample_mean(x, n, gen):
    s = gen.choice(x, size=n, replace=False)
    return s.mean()

means = np.array([sample_mean(x, 50, gen)
                  for _ in range(1000)])
```

- **One generator, passed along**: the 1,000 samples differ, and the whole run repeats exactly.
- `replace=False`: no meter is read twice within a sample.
- The capstone asks for a seeded run log. The habit starts here.

#### [day1#bigger-sample] Four times the sample halves the spread of the means

*Lab 1.1, stretch*

| Item | Value |
| --- | --- |
| samples of 50 | 29.6 litres |
| samples of 200 | 14.8 litres |

- The population did not change. Only the precision of the estimate did.
- The ratio is 2.00: session 2 gives the rule behind it.

#### [day1#check-sampling-distribution] Which sentence describes a sampling distribution?

*Checkpoint*

**Question:** Ilyas reads 50 meters each month and reports the mean. Over the year his twelve means ran from 430 to 515 litres. Which statement explains the range best?

- A. Households use between 430 and 515 litres a day
- B. Consumption rose and fell during the year
- C. Means of samples of 50 scatter by about 30 litres around the truth
- D. Some of the monthly samples were drawn incorrectly

#### [day1#lab-1-1] One sample, then a thousand

Lab 1.1 · 25 min

Draw one sample of 50 households, then 1,000 of them, and plot the 1,000 mean consumptions around the population mean you can compute.

[D1_1_sampling_means.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D1_1_sampling_means.ipynb)

- [ ] Load the population and compute the parameter (4 min)
- [ ] One sample of 50: the statistic and its miss (5 min)
- [ ] 1,000 samples: collect the means (7 min)
- [ ] Plot the means and mark the truth (5 min)
- [ ] Share of samples within 20 litres of the truth (4 min)
- [ ] ✱ Stretch: Repeat with samples of 200 and compare the two spreads

### Session 2: Standard error by simulation and by formula

#### [day1#s2] Standard error by simulation and by formula

*Session 2*

- Measure a standard error by simulation at several sample sizes
- Compute the standard error of a mean from one sample
- Separate the standard deviation of households from the standard error of a mean

#### [day1#se-is-a-spread] The standard error is the standard deviation of a statistic

*A name for the spread*

- It is the spread of the sampling distribution: 29.6 litres for the mean of 50 households.
- It says how far an estimate typically lands from the truth.
- Every statistic has one: a mean, a median, a difference, a slope.

- **You met a cousin in FN-103.** The Monte Carlo error of a simulated average was a spread divided by √N. The standard error of a sample mean is the same idea, with households in place of simulated months.

#### [day1#se-by-simulation] By simulation: draw 2,000 samples at each size and measure

*Lab 1.2, step 1*

```python
def simulated_se(x, n, reps, gen):
    means = np.array([
        gen.choice(x, size=n, replace=False).mean()
        for _ in range(reps)])
    return means.std(ddof=1)
```

| households n | simulated standard error |
| --- | --- |
| 25 | 41.45 |
| 100 | 20.76 |
| 400 | 10.14 |

#### [day1#se-by-formula] By formula: the spread of households divided by √n

*Lab 1.2, steps 2 and 3*

| n | simulated | σ / √n, population known | s / √n, from one sample |
| --- | --- | --- | --- |
| 25 | 41.45 | 41.29 | 46.72 |
| 100 | 20.76 | 20.64 | 20.03 |
| 400 | 10.14 | 10.32 | 10.31 |

- σ is the population's standard deviation, 206.4 litres. Nobody has it in real work.
- **s** is the sample's own standard deviation. One sample estimates its own standard error.
- At n = 25 the one-sample value is 13% off: small samples know little about their own spread.

#### [day1#sd-versus-se] The standard deviation describes households; the standard error describes your estimate

*The most common mix-up*

- **Standard deviation: 200 litres.** "Households differ a lot: a typical household is about 200 litres away from the sample mean of 490." **Does not shrink** when you read more meters.
- **Standard error: 20 litres.** "Our estimate of the average, 490 litres, is typically within about 20 litres of the true average." **Shrinks** with √n.

> **What goes wrong.** "490 ± 20" printed without a word on which of the two the 20 is. Always name it.

#### [day1#sqrt-law-samples] Half the error costs four times the sample

*Lab 1.2, step 4*

| n | standard error | × √n |
| --- | --- | --- |
| 25 | 41.45 | 207.3 |
| 100 | 20.76 | 207.6 |
| 400 | 10.14 | 202.8 |

- The last column is nearly constant: it is σ, 206.4.
- From 25 to 400 households, 16 times the work, the error fell 4.1 times.
- Precision has a price list. A manager can read it before the survey is commissioned.

#### [day1#estimate-plus-minus] Estimate ± 2 standard errors is the first interval

*Where this leads*

- In lab 1.1, 94% of sample means lay within 57 litres of the truth: about 2 standard errors.
- Turn it around: the truth lies within 2 standard errors of most sample means.
- For the sample of 100: 490 ± 2 × 20, from 450 to 530 litres. The truth, 470.4, is inside.

- **Not every statistic has a formula.** The median's standard error at n = 100 is 25.5 litres by simulation (lab 1.2, stretch). No σ/√n gives it. Day 2 gets it from one sample by resampling.

#### [day1#check-sd-or-se] Which number answers the manager?

*Checkpoint*

**Question:** From 400 households: mean 468 litres, standard deviation 204, standard error 10. Jamila asks: "How sure are we about the 468?" Which reply is right?

- A. The true average is very likely within about 20 litres of 468
- B. The true average could be anywhere within 204 litres of 468
- C. Nearly all households use between 448 and 488 litres
- D. With 400 households the 468 is exact

#### [day1#lab-1-2] Standard error twice

Lab 1.2 · 25 min

Measure the standard error of mean consumption by simulation at 25, 100 and 400 households, then get nearly the same numbers from the formula and from a single sample.

[D1_2_standard_error.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D1_2_standard_error.ipynb)

- [ ] Simulated standard error at n = 25, 100 and 400 (8 min)
- [ ] The formula with the population standard deviation (4 min)
- [ ] The formula from one sample only (6 min)
- [ ] One table and the square-root law (4 min)
- [ ] SD or SE: two sentences for the manager (3 min)
- [ ] ✱ Stretch: Do the same for the sample median, which has no simple formula

### Session 3: Skew, outliers and the median

#### [day1#s3] Skew, outliers and the median

*Session 3*

- Recognise skew from a histogram and from mean against median
- Measure the effect of one extreme value on the mean, the median and a trimmed mean
- Choose the summary that answers the question asked, and say why

#### [day1#repairs-are-skewed] Repair times are skewed: most are short, a few are very long

*A different kind of data*

Figure: All 12,000 leak repairs of the year.

- Median 6.5 hours, mean 9.9 hours.
- 70% of repairs are shorter than the mean.
- Durations, costs, waiting times and consumption in litres are usually skewed like this.

#### [day1#mean-follows-tail] The mean is a balance point; the median is the middle ticket

*Two meanings of "the middle"*

- **Mean.** Add all hours, divide by the count. Every hour of every ticket counts, so one long ticket moves it. Mean × count = total hours.
- **Median.** Sort the tickets, take the middle one. Only the order counts, so a ticket of 50 hours and one of 2,000 hours pull equally.

Sample of 200 regular repairs (lab 1.3): mean 8.11 hours, median 6.40 hours, 63% of repairs shorter than the mean, longest 48.4 hours.

#### [day1#one-open-ticket] One ticket left open for two months nearly doubles the mean

*Lab 1.3, step 2*

|  | mean, hours | median, hours |
| --- | --- | --- |
| 200 regular repairs | 8.11 | 6.40 |
| plus one ticket of 1,450 hours | 15.28 | 6.50 |
| the move | +7.17 | +0.10 |

- The crew finished in an afternoon. Nobody closed the ticket.
- Twelve such tickets sit among Zulal's 12,000 repairs, from 598 to 2,090 hours.
- In the whole population they lift the mean from 8.86 to 9.86 hours and leave the median at 6.5.

#### [day1#sweep-extreme] The mean follows the extreme value without limit; the median stops caring

*Lab 1.3, step 3*

| the extra ticket, hours | 10 | 50 | 100 | 500 | 1,000 | 2,000 |
| --- | --- | --- | --- | --- | --- | --- |
| mean of the 201 repairs | 8.12 | 8.32 | 8.56 | 10.55 | 13.04 | 18.02 |
| median of the 201 repairs | 6.50 | 6.50 | 6.50 | 6.50 | 6.50 | 6.50 |

- Each extra hour on the one ticket adds 1/201 of an hour to the mean.
- It takes 27 such tickets, 12% of the sample, to move the median by one hour (stretch).

#### [day1#which-summary] The question decides the summary

*Lab 1.3, steps 4 and 5*

| The question | The summary | Why |
| --- | --- | --- |
| How long does a typical repair take? | **Median** | Half the repairs are shorter, half longer |
| How many crew hours do we pay for? | **Mean** | A total is the mean times the count |
| A stable mean when a few records are suspect? | **Trimmed mean** | Drops the top and bottom 5%: 7.29 hours, and 7.37 with the open ticket |

> **What goes wrong.** Deleting the long tickets in silence. An extreme value is reported and explained, then kept or set aside in the open.

#### [day1#skew-and-inference] Skew makes the mean a harder target for inference too

*Why this matters tomorrow*

- A sample of 40 repairs usually contains none of the rare long tickets, so its mean runs low and its standard error looks small.
- Intervals for the mean then miss the truth more often than they promise. Lab 2.2 counts how often.
- The median has no σ/√n formula. Lab 2.1 gets its interval by resampling.

#### [day1#check-which-summary] Which summary goes in the monthly report?

*Checkpoint*

**Question:** The contract promises customers that "a typical leak is repaired within 8 hours". This month: mean 15.3 hours, median 6.5 hours, one ticket of 1,450 hours. What should Nizar report against the promise?

- A. The mean, 15.3 hours: the promise was broken
- B. The mean after deleting the long ticket, with no note
- C. The midpoint of mean and median, 10.9 hours
- D. The median, 6.5 hours, and the long ticket named separately

#### [day1#lab-1-3] One ticket left open

Lab 1.3 · 25 min

Add one repair ticket left open for weeks to a sample of 200 repairs and measure how far the mean, the median and a trimmed mean move.

[D1_3_extreme_repair.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D1_3_extreme_repair.ipynb)

- [ ] Look at the skew: mean against median (5 min)
- [ ] Add one ticket left open and recompute (6 min)
- [ ] Sweep the extreme value from 10 to 2,000 hours (6 min)
- [ ] A trimmed mean as a middle road (4 min)
- [ ] Decide what to report, and why (4 min)
- [ ] ✱ Stretch: Count how many open tickets it takes to move the median by one hour

### Session 4: Describing a sample honestly

#### [day1#s4] Describing a sample honestly

*Session 4*

- Summarise a skewed sample in five numbers and an interquartile range
- Draw a histogram and state the bin width and the axis
- Write a description that gives the count, the exclusions and the population

#### [day1#five-numbers] Five numbers describe a skewed sample without pretending it is a bell

*Lab 1.4, step 1*

| 300 repairs | hours |
| --- | --- |
| minimum | 1.0 |
| first quartile | 3.7 |
| median | 6.2 |
| third quartile | 10.4 |
| maximum | 663.5 |

- The **interquartile range**, 6.7 hours, is the width of the middle half.
- The same sample as "mean ± SD": 10.4 ± 38.4 hours, a range that starts below zero.
- The maximum is one late-entry ticket. The five numbers show it without being bent by it.

#### [day1#histogram-choices] A histogram is a set of choices: state them

*Lab 1.4, steps 2 and 3*

- **Bin width.** 2 hours here. Too wide hides the peak; too narrow draws noise. Write the width on the axis.
- **Where the axis ends.** The plot stops at 40 hours. The title says "4 longer than 40 hours not shown".
- **Plain or log axis.** On a log axis all 300 fit. Skewness falls from 16.5 to 0.8, and the late ticket stands apart as its own group.

> **Rule.** A reader should be able to redraw your picture from its caption: count, bin width, axis, what is left out.

#### [day1#groups-with-counts] A group summary always carries its count

*Lab 1.4, step 4*

| contractor | n | median | quartiles |
| --- | --- | --- | --- |
| A | 150 | 5.2 | 3.4 to 8.9 |
| B | 150 | 7.5 | 4.7 to 11.6 |

- B's median is 2.3 hours higher in this sample.
- A description shows the gap. It does not say whether the gap is more than the luck of 300 tickets.
- That judgement needs an interval (Day 2) and a test (Day 3).

#### [day1#small-counts] By district only, and not when the count is small

*Lab 1.4, stretch*

- Zulal reports by district or contractor, never by household.
- A district's number is withheld when it rests on fewer than 20 repairs.
- In the sample of 300, that withholds 24 of the 29 districts that appear.

- **Two reasons, one rule.** **Statistics:** a median of 8 tickets jumps with every new ticket. **Protection:** in a small district a number can point at single households.

#### [day1#honest-description] An honest description can be checked line by line

*Lab 1.4, step 5*

- "We looked at **300** leak repairs drawn at random from Zulal's **12,000** repairs of the year. The median repair took **6.2** hours; the middle half took between **3.7** and **10.4** hours. **One** ticket in the sample was closed in the system weeks late and is reported separately; the longest regular repair took 42.8 hours. These numbers describe the 300 sampled repairs, by contractor and never by household."

- **Count.** 300 of 12,000
- **Middle and spread.** median, quartiles
- **Exclusions.** named, not hidden
- **Population.** what the sample stands for

#### [day1#description-is-not-inference] A description is about the sample; an inference is about the population

*The line between today and tomorrow*

- **Description, today.** "In these 300 repairs the median was 6.2 hours." True by arithmetic. No uncertainty needed.
- **Inference, from tomorrow.** "The median of all 12,000 repairs is between two stated values." A claim that can be wrong, and whose error rate can be measured.

The true median is 6.5 hours. The sample said 6.2. Tomorrow's interval has to be wide enough to admit 6.5, and you will count how often it is.

#### [day1#check-honest-description] Which description would you sign?

*Checkpoint*

**Question:** Four drafts describe the same 300 repairs, one of which is a late-entry ticket of 663.5 hours. Which one can a reader check and rely on?

- A. Repairs took 10.4 ± 38.4 hours on average
- B. Of 300 sampled repairs the median was 6.2 hours (quartiles 3.7 and 10.4); one late-entry ticket is listed apart
- C. Repairs typically take about six hours
- D. All of Zulal's repairs have a median of exactly 6.2 hours

#### [day1#lab-1-4] Five numbers and a histogram

Lab 1.4 · 25 min

Summarise 300 repair times in five numbers, draw the histogram on a plain and a log axis, split by contractor with counts, and write the description a reader can check.

[D1_4_five_numbers.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D1_4_five_numbers.ipynb)

- [ ] Five numbers and the interquartile range (6 min)
- [ ] A histogram with a stated bin width (5 min)
- [ ] The same data on a log axis (4 min)
- [ ] The summary by contractor, with counts (5 min)
- [ ] Write the honest description (5 min)
- [ ] ✱ Stretch: Build the district table and withhold every district with fewer than 20 repairs

#### [day1#wrap-up] What to keep

*Day 1 in three lines*

- **A statistic varies.** One sample is one draw of many. The sampling distribution shows all the draws you did not get.
- **The standard error measures it.** The spread of a statistic, s / √n for a mean, from one sample. Not the standard deviation of households.
- **Describe before you infer.** Median and quartiles for skewed data, the count, the exclusions, the population.

#### [day1#next] Day 2: Intervals

*Next*

From "samples land near the truth" to an interval built from one sample, and a count of how often it holds.

- Keep your environment as it is: tomorrow's labs use the same four files.
- Think about it tonight: with one sample and no population, how could you see a sampling distribution?

## Day 2: Intervals

An interval is a method with a promise, and on a known population the promise can be counted

#### [day2#title] Intervals

*SDAIA Academy · Statistical Inference by Simulation*

Day 2: An interval is a method with a promise, and on a known population the promise can be counted

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-201

#### [day2#agenda] Intervals

*Today*

- **Session 1 · The bootstrap idea**: The sample stands in for the population: resample it with replacement and watch the statistic move
- **Session 2 · Coverage is a testable claim**: A 95% interval is a claim about the method over many studies, and the claim can fail
- **Session 3 · Resample the right unit**: Rows that share a district are not independent: the unit you resample must be the unit that was sampled
- **Session 4 · Intervals for differences and ratios**: Managers ask about gaps and ratios: resample each group, recompute the comparison, read the interval against 0 or 1

#### [day2#review-day1] Which number shrinks when you read more meters?

*Review of Day 1*

**Question:** From 100 households: mean 490 litres, standard deviation 200, standard error 20. Zulal reads 400 households next time. What do you expect?

- A. Standard deviation about 100, standard error about 20
- B. Standard deviation about 200, standard error about 10
- C. Standard deviation about 200, standard error about 5
- D. Standard deviation about 100, standard error about 10

### Session 1: The bootstrap idea

#### [day2#s1] The bootstrap idea

*Session 1*

- Explain why resampling the sample imitates sampling the population
- Compute a percentile bootstrap interval for a median
- Compare a bootstrap distribution with the real sampling distribution

#### [day2#one-sample-only] A real analyst has one sample and no population to resample

*The problem*

- Yesterday's sampling distributions came from drawing 1,000 samples from the population.
- In real work you can afford one sample. The other 999 do not exist.
- For a mean, a formula fills the gap: s / √n. For a median, a ratio or a slope there is often none.

- **Nizar's question.** "What is the typical repair time, with an honest range around it?" You hold 150 tickets. Median 6.15 hours. How far could that be from the truth?

#### [day2#bootstrap-idea] Treat the sample as the population and sample from it

*The bootstrap idea*

1. **1 · One sample** 150 repair times, the best picture of the population you have
2. **2 · Resample** draw 150 from the 150, with replacement
3. **3 · Recompute** the median of the resample
4. **4 · Repeat** 2,000 times: an imitation of the sampling distribution

> **With replacement** is the whole trick. Without it, every resample is the sample itself.

#### [day2#one-resample] One resample repeats some tickets and leaves others out

*Lab 2.1, step 2*

```python
def resample(v, gen):
    return gen.choice(v, size=len(v),
                      replace=True)

one = resample(sample, gen)
len(np.unique(one))   # 77 distinct values
np.median(one)        # 6.40 hours
```

- 150 values drawn, 77 distinct values. Many tickets appear twice or more; many do not appear.
- Its median is 6.40 hours; the sample's was 6.15.
- That difference imitates the difference between two real samples.

#### [day2#bootstrap-distribution] The middle 95% of the resampled medians is the interval

*Lab 2.1, steps 3 and 4*

Figure: 2,000 bootstrap medians from one sample of 150 repairs.

- **Percentile interval**: from the 2.5th to the 97.5th percentile, 5.00 to 7.50 hours.
- The true median, 6.50 hours, is inside.
- The histogram is lumpy: a median of 150 tickets can only take values in the sample, or halfway between two of them.

#### [day2#width-not-centre] The bootstrap gets the width right, not the centre

*Lab 2.1, step 5*

- **0.553** standard error of the median by bootstrap, from one sample
- **0.513** the real one, from 2,000 samples of the population
- **6.15** where the bootstrap is centred: the sample median, not the truth, 6.50

- The bootstrap cannot repair a sample that landed low. It can tell you how far samples land.
- That is exactly what an interval needs.

#### [day2#b-is-not-n] More resamples smooth the picture; only more data narrow the interval

*Two numbers people confuse*

|  | n, the sample size | B, the number of resamples |
| --- | --- | --- |
| What it is | 150 tickets you collected | 2,000 loops your laptop ran |
| What it costs | Field work | Seconds |
| What more of it buys | A narrower interval | A steadier estimate of the same interval |

> **What goes wrong.** "We ran a million resamples, so the result is very precise." The interval for 150 tickets is 2.5 hours wide at any B.

#### [day2#check-resample] Which procedure is a bootstrap resample?

*Checkpoint*

**Question:** You have 80 survey scores and want an interval for their median. Which step, repeated 2,000 times, gives the bootstrap distribution?

- A. Shuffle the 80 scores and take their median
- B. Draw 40 of the 80 scores at random and take their median
- C. Draw 80 new scores from all customers and take their median
- D. Draw 80 scores from the 80 with replacement and take their median

#### [day2#lab-2-1] Bootstrap a median

Lab 2.1 · 25 min

Bootstrap the median repair time from one sample of 150 repairs, read the percentile interval, and compare both the interval and the bootstrap spread with the truth.

[D2_1_bootstrap_median.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D2_1_bootstrap_median.ipynb)

- [ ] One sample of 150 repairs and its median (4 min)
- [ ] One resample, by hand (4 min)
- [ ] 2,000 resamples: the bootstrap distribution (7 min)
- [ ] The percentile interval beside the truth (5 min)
- [ ] Bootstrap spread against the real sampling spread (5 min)
- [ ] ✱ Stretch: Count the coverage of the median's interval over 1,000 studies

### Session 2: Coverage is a testable claim

#### [day2#s2] Coverage is a testable claim

*Session 2*

- State what 95% coverage promises
- Measure the coverage of two interval methods over simulated studies
- Name two situations in which the bootstrap fails

#### [day2#what-95-promises] 95% is a promise about the method, not about one interval

*What the number means*

- **The promise.** "Use this method on many studies and about 95 in 100 of the intervals it produces will contain the true value." That share is the **coverage**.
- **Not the promise.** "There is a 95% chance that the truth is between 5.0 and 7.5." The truth is a fixed number. This one interval contains it or it does not.

> **At Zulal the promise can be checked.** Draw 500 studies, build 500 intervals, count how many contain the truth.

#### [day2#two-methods] Two ways to an interval for a mean

*Lab 2.2, step 1*

- **The t interval.** mean ± t × s / √n, with t about 2.02 for 40 tickets. Symmetric by construction. One study of 40: **5.83 to 10.76** hours.
- **The bootstrap interval.** Percentiles of 1,000 resampled means. Follows the skew of the sample. The same study: **6.16 to 10.91** hours.

Mean of the 40 tickets: 8.29 hours. True mean of tickets closed on time: 8.86 hours. Both intervals contain it, in this study.

#### [day2#coverage-loop] Coverage is measured by a loop and a count

*Lab 2.2, step 2*

```python
hits = 0
for _ in range(500):
    study = gen.choice(pool, size=40,
                       replace=False)
    low, high = t_interval(study)
    hits += low <= truth <= high
coverage = hits / 500
```

- Each pass is one imaginary study, analysed the way you would analyse a real one.
- The count has its own error: with 500 studies, a true 95% shows as 95% give or take 1.9 points.
- The capstone asks for this loop on your own method.

#### [day2#coverage-results] The promise holds for ordinary skew and collapses with rare extremes

*Lab 2.2, steps 2 to 4*

| The population sampled | tickets per study | t interval | bootstrap |
| --- | --- | --- | --- |
| tickets closed on time | 40 | 93.4% | 93.2% |
| tickets closed on time | 200 | 94.2% | 93.6% |
| all tickets, with the 12 late entries | 40 | 81.4% | 81.8% |
| all tickets, with the 12 late entries | 200 | 62.4% | 63.0% |

Share of 500 studies whose 95% interval for the mean contained the true mean.

#### [day2#when-bootstrap-fails] The bootstrap fails where the sample cannot stand in for the population

*Know the limits*

- **Rare extreme values.** The sample usually misses them. Coverage for the mean fell to 62% (lab 2.2).
- **Statistics at the edge.** A resample never exceeds the sample's maximum. Coverage for the maximum repair time: 1.3% (stretch).
- **Very small samples.** Ten tickets hold too few distinct values to imitate a population. Intervals come out too short.

> **And one more, next session:** resampling rows that were not sampled independently.

#### [day2#what-to-do-about-it] When coverage fails, change the question or say so

*In a brief*

- **Change the target:** the median repair time, or the mean of tickets closed on time, with the late entries reported apart.
- **Say what the sample cannot know:** "this sample contains no late-entry ticket; the mean over all tickets may be an hour higher."
- **Check your own method:** a coverage count on data like yours, reported next to the interval.

#### [day2#check-reading-95] What may Ilyas write about his interval?

*Checkpoint*

**Question:** From 150 repairs Ilyas computes a 95% interval for the median repair time: 5.0 to 7.5 hours. Which sentence is correct?

- A. The method that gave this interval catches the true median in about 95 of 100 studies
- B. About 95% of repairs take between 5.0 and 7.5 hours
- C. The true median has a 95% chance of lying between 5.0 and 7.5 hours
- D. In 95% of future samples the median will be between 5.0 and 7.5 hours

#### [day2#lab-2-2] Count the coverage

Lab 2.2 · 25 min

Run 500 studies of 40 repairs, count how often a t interval and a percentile bootstrap interval for the mean contain the true mean, then repeat with 200 repairs and with the late-entry tickets left in.

[D2_2_coverage.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D2_2_coverage.ipynb)

- [ ] Two intervals for the mean from one study of 40 (6 min)
- [ ] 500 studies: count the coverage of each method (8 min)
- [ ] The same count with 200 repairs (4 min)
- [ ] Leave the late-entry tickets in and count again (4 min)
- [ ] State what 95% promised and what it delivered (3 min)
- [ ] ✱ Stretch: Bootstrap the maximum repair time and count its coverage

### Session 3: Resample the right unit

#### [day2#s3] Resample the right unit

*Session 3*

- Identify the sampling unit of a two-stage sample
- Bootstrap by household and by district and compare the intervals
- Show by coverage which unit keeps the promise

#### [day2#two-stage-sample] The survey team drew districts first, then households

*How the data were collected*

1. **Stage 1** 6 of the 30 districts, chosen at random
2. **Stage 2** 60 households phoned in each chosen district
3. **The file** 360 rows of satisfaction scores

| district | responses | mean score |
| --- | --- | --- |
| D05 | 60 | 7.58 |
| D09 | 60 | 6.53 |
| D10 | 60 | 6.67 |
| D11 | 60 | 5.92 |
| D17 | 60 | 6.70 |
| D28 | 60 | 6.22 |

#### [day2#rows-not-independent] 360 rows are not 360 independent pieces of information

*The hidden assumption*

- Households of one district share the same pipes, crews and service office.
- Another survey would have visited six **other districts**. That is the largest source of variation, and the rows alone do not show it.

- **The estimate.** 6.60 from this sample. Truth, all 9,000 responses: 6.67. The question is the width of the interval.

#### [day2#two-bootstraps] Same data, two resampling units, two different intervals

*Lab 2.3, steps 2 and 3*

Figure: 95% bootstrap intervals for mean satisfaction from the same 360 responses.

- **By household:** resample the 360 rows. Width 0.38 points.
- **By district:** resample the 6 districts, each with all its rows. Width 0.79 points.
- Both contain the truth this time. Which width is honest?

#### [day2#unit-coverage] Counted over 300 surveys, only the district bootstrap keeps the promise

*Lab 2.3, step 4*

| Item | Value |
| --- | --- |
| resampling households | 72.3% |
| resampling districts | 93.7% |
| promised | 95% |

- The household interval misses the truth in more than one survey in four.
- Six districts are few, so even the right unit falls a little short. It is honest about the size of the uncertainty.

#### [day2#find-the-unit] Resample the unit that was drawn at random

*The question to ask of every dataset*

| The data | Rows | Unit to resample |
| --- | --- | --- |
| 360 households phoned at random across the region | households | household |
| 60 households in each of 6 districts chosen at random | households | **district** |
| Five pressure readings on each of 40 pumps | readings | **pump** |
| Twelve monthly bills for each of 500 customers | bills | **customer** |

> **Design beats arithmetic.** The same 360 calls spread over 12 districts of 30 give a narrower honest interval: 0.64 against 0.79 points (stretch).

#### [day2#unit-in-the-file] In code the change is one line: what you index

*Lab 2.3, step 3*

```python
# by household: index the rows
idx = gen.integers(0, 360, size=(B, 360))
boot = scores[idx].mean(axis=1)
```

```python
# by district: index the districts
dm = df.groupby("district")["satisfaction"].mean()
idx = gen.integers(0, 6, size=(B, 6))
boot = dm.to_numpy()[idx].mean(axis=1)
```

With 60 responses in every district, the mean of a resample of districts is the mean of their district means. With unequal counts, carry each drawn district's rows along.

#### [day2#oversample-rare-group] Oversample a rare group, and every row stands for a different number of households

*Another design: a rare group drawn more often*

| group, n drawn | N | N / n | mean |
| --- | --- | --- | --- |
| 9+ people, 150 | 1,809 | 12.1 | 970.5 |
| 1 to 8, 250 | 78,191 | 312.8 | 460.7 |

N: households on file. n: households drawn. N / n: the design weight. Mean: sample mean consumption, litres a day.

- Planners need a figure for the largest households, which are 2.3% of the region: a plain random 400 would hold about 9 of them.
- So the design draws 150 of them on purpose. Good design for the group; a trap for the regional mean.

#### [day2#design-weights] Weight each row by N / n and the regional mean comes back

*Restoring the population*

| Item | Value |
| --- | --- |
| plain mean of the 400 | 651.9 |
| weighted mean | 472.2 |
| truth, all 80,000 | 470.4 |

- **The weighted mean.** (12.1 × 150 × 970.5 + 312.8 × 250 × 460.7) ÷ (12.1 × 150 + 312.8 × 250): each group counts as many households as it has on file. Over 1,000 such samples the plain mean averages 653.6 and the weighted 470.1.

> **Not more data, a different question.** The plain mean answers "the average of the rows I happened to draw"; the weighted mean answers the regional question. Weights go with every row into every resample.

#### [day2#check-unit] What is the unit to resample?

*Checkpoint*

**Question:** To estimate mean water pressure, Zulal picks 25 streets at random and measures the pressure at 8 houses on each: 200 readings. Which bootstrap gives an honest interval for the mean?

- A. Resample the 200 readings
- B. Resample 8 readings within each street
- C. Resample the 25 streets, each with its 8 readings
- D. Resample 100 of the 200 readings

#### [day2#lab-2-3] Household or district

Lab 2.3 · 25 min

Bootstrap mean satisfaction from a two-stage survey sample by household and by district, then count the coverage of both over 300 studies and explain the difference.

[D2_3_resampling_unit.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D2_3_resampling_unit.ipynb)

- [ ] Draw the two-stage sample and estimate (4 min)
- [ ] Bootstrap by household (5 min)
- [ ] Bootstrap by district (6 min)
- [ ] Coverage of both over 300 studies (6 min)
- [ ] Explain the difference in two sentences (4 min)
- [ ] ✱ Stretch: Redraw with 12 districts of 30 responses and compare the widths

### Session 4: Intervals for differences and ratios

#### [day2#s4] Intervals for differences and ratios

*Session 4*

- Compute a bootstrap interval for a difference between two groups
- Compute a bootstrap interval for a ratio
- Read an interval for a comparison against no difference

#### [day2#managers-ask-gaps] Managers rarely ask for a level; they ask for a gap

*The question behind most questions*

- "Is contractor B slower than A, and by how much?"
- A gap can be said two ways: a **difference** (hours) or a **ratio** (percent).
- Either way it is a statistic, computed from two samples, with its own sampling distribution.

| 200 repairs each | median, hours |
| --- | --- |
| contractor A | 6.00 |
| contractor B | 6.90 |
| difference B - A | 0.90 |
| ratio B / A | 1.15 |

#### [day2#resample-each-group] Resample each group on its own, then recompute the comparison

*Lab 2.4, step 2*

```python
ia = gen.integers(0, len(a), size=(B, len(a)))
ib = gen.integers(0, len(b), size=(B, len(b)))
ma = np.median(a[ia], axis=1)
mb = np.median(b[ib], axis=1)

diff_boot  = mb - ma      # difference
ratio_boot = mb / ma      # ratio
```

- The study fixed 200 repairs per contractor. Each resample keeps that.
- One set of resamples serves both comparisons.
- The interval is the percentile interval of the 2,000 differences, or ratios.

#### [day2#difference-and-ratio] Two intervals, one story, in two units

*Lab 2.4, steps 2 to 4*

|  | estimate | 95% interval | "no gap" is | truth |
| --- | --- | --- | --- | --- |
| difference of medians, B - A | 0.90 h | -0.25 to 2.50 h | 0 | 1.40 h |
| ratio of medians, B / A | 1.15 | 0.96 to 1.44 | 1 | 1.24 |

- Both intervals contain the truth, and both include "no gap".
- In words: B's typical repair takes between 0.96 and 1.44 times as long as A's.
- Hours suit the crew planner; a percentage suits the contract.

#### [day2#reading-zero-and-one] An interval that includes "no gap" shows what is still possible, not that nothing is there

*Reading a comparison*

- **Wrong.** "The interval includes 1, so the contractors are equally fast."
- **Right.** "The study cannot tell B from A. It is consistent with B being 4% faster and with B being 44% slower."

> **And do not compare two separate intervals by eye.** Whether the interval for A and the interval for B overlap is not a test. Build the interval for the difference itself.

#### [day2#ratio-coverage] Counted against the truth, both intervals keep their promise

*Lab 2.4, step 5 and stretch*

- **95.0%** coverage of the ratio of medians, over 300 studies of 200 repairs per contractor
- **94.3%** coverage of the difference of means on tickets closed on time, over 1,000 studies

- A ratio of medians has no textbook formula. The bootstrap needs none.
- The second figure is the course's evidence standard: an interval with its coverage over 1,000 simulated samples.

#### [day2#day2-method] An interval for almost anything, in four questions

*Day 2 as one recipe*

1. **What is the statistic?** A median, a difference, a ratio: whatever answers the manager.
2. **What unit was drawn at random?** Resample that unit, within each group.
3. **Where do the middle 95% of the resampled statistics lie?** That is the interval.
4. **Does the method keep its promise on data like mine?** Count the coverage.

#### [day2#check-ratio] How do you read this ratio interval?

*Checkpoint*

**Question:** A study compares the median time to answer a call at two desks. Ratio North / South: 1.30, 95% interval 1.08 to 1.57. What may the analyst report?

- A. No gap is shown, because the interval does not include 0
- B. North is slower: between 8% and 57% longer than South
- C. North is slower by exactly 30%
- D. North takes between 1.08 and 1.57 hours longer than South

#### [day2#lab-2-4] Difference and ratio of medians

Lab 2.4 · 25 min

Build bootstrap intervals for the difference and the ratio of the two contractors' median repair times, compare them with the truth and count the coverage of the ratio interval.

[D2_4_difference_ratio.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D2_4_difference_ratio.ipynb)

- [ ] Sample 200 repairs for each contractor (4 min)
- [ ] Bootstrap the difference of medians (7 min)
- [ ] Bootstrap the ratio of medians (5 min)
- [ ] Compare with the truth; read 0 and 1 (4 min)
- [ ] Coverage of the ratio interval over 300 studies (5 min)
- [ ] ✱ Stretch: Do the difference of means on closed tickets with coverage over 1,000 studies

#### [day2#wrap-up] What to keep

*Day 2 in three lines*

- **Resample the sample.** With replacement, same size, many times. The middle 95% of the recomputed statistic is the interval.
- **Count the coverage.** 95% is a promise about the method. On a known population you can count whether it is kept: 93%, or 62%.
- **Resample the right unit.** The unit that was drawn at random. Rows that share a district are not independent: 72% against 94%.

#### [day2#next] Day 3: Tests

*Next*

"Could this gap be luck?" A test answers by building the world in which it is luck.

- Tomorrow starts with a shuffle, not a formula.
- Bring one sentence about a p-value from a report you have read. Lab 3.2 marks eight of them.

## Day 3: Tests

A test asks one narrow question; the answer needs an effect size beside it and a count of how many questions were asked

#### [day3#title] Tests

*SDAIA Academy · Statistical Inference by Simulation*

Day 3: A test asks one narrow question; the answer needs an effect size beside it and a count of how many questions were asked

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-201

#### [day3#agenda] Tests

*Today*

- **Session 1 · A test is a shuffling rule**: The null hypothesis is a rule for shuffling labels; the p-value counts how often the rule beats your result
- **Session 2 · p-values and their misreadings**: What a p-value says, the misreadings found in reports, and how a simulation with the truth known settles them
- **Session 3 · Effect size and practical significance**: How big, and does it matter: an effect with its interval set against the threshold the business named
- **Session 4 · Thirty districts, many false alarms**: Test 30 districts and some will cross 0.05 by chance: family-wise error, false discovery rate and where small districts land

#### [day3#review-day2] Which interval would you report?

*Review of Day 2*

**Question:** A survey phoned 50 households in each of 8 districts chosen at random. Bootstrapping the 400 rows gives a 95% interval of 6.5 to 6.8; bootstrapping the 8 districts gives 6.3 to 7.0. Which do you report, and why?

- A. 6.5 to 6.8, because it is more precise
- B. 6.5 to 6.8, because it uses 400 observations and not 8
- C. 6.3 to 7.0, because districts were the unit drawn at random
- D. Something in between, to be safe

### Session 1: A test is a shuffling rule

#### [day3#s1] A test is a shuffling rule

*Session 1*

- State a null hypothesis as a shuffling rule
- Implement a permutation test for a difference in means
- Compare the permutation p-value with the matching classical test

#### [day3#could-it-be-luck] Contractor A scores higher. Could that be luck?

*Nizar's question*

| contractor | responses | mean score, 1 to 10 |
| --- | --- | --- |
| A | 400 | 6.748 |
| B | 400 | 6.452 |
| difference A - B |  | +0.295 |

- Two samples of 400 never give exactly equal means, even from identical contractors.
- So 0.295 could be a real gap, or the noise of sampling.
- A test asks one narrow question: **how surprising is 0.295 if there is no gap at all?**

#### [day3#null-as-shuffle] If the contractor makes no difference, the labels are arbitrary

*The null hypothesis*

1. **1 · Assume** the contractor has nothing to do with the score
2. **2 · Shuffle** the 800 labels: any 400 could have been "A"
3. **3 · Recompute** the difference in means under the shuffled labels
4. **4 · Repeat** 5,000 times and see where 0.295 falls

> **The null hypothesis is a rule for generating data.** Here the rule is: shuffle the labels. No formula is needed to state it.

#### [day3#null-distribution] Under shuffled labels a gap of 0.295 is rare

*Lab 3.1, steps 3 and 4*

Figure: 5,000 shuffles of the contractor labels.

- Centred on zero, spread 0.135.
- The largest shuffled gap in 5,000: 0.525.
- Gaps of 0.295 or more, in either direction: about 31 in every 1,000 shuffles.
- That share is the **p-value**: 0.031.

#### [day3#classical-approximation] The t-test is a formula for the histogram you just drew

*Lab 3.1, step 5*

|  | by shuffling | by formula (Welch) |
| --- | --- | --- |
| spread of the difference under the null | 0.1346 | 0.1353 |
| p-value | 0.0314 | 0.0295 |

- t = difference / standard error = 0.295 / 0.1353 = 2.18.
- The t distribution is the bell curve that the shuffles trace out.
- With 400 per group the approximation is excellent.

#### [day3#when-they-differ] Shuffle when the formula is doubtful or does not exist

*Which one to use*

| Situation | Classical test | Permutation test |
| --- | --- | --- |
| Two means, hundreds per group | Fine: agrees to two decimals | Fine |
| Two means, 15 per group, skewed scores | Approximation is rough | Still exact for the shuffling rule |
| Two medians, a ratio, a custom metric | Often none at hand | Same four steps |

> **What goes wrong.** Shuffling the wrong thing. If districts were assigned to a programme, shuffle district labels, not household labels.

#### [day3#test-says-little] The test was right, and it said very little

*Checked against the truth*

- **0.295** the gap in the study of 800 responses
- **0.462** the gap in all 9,000 responses
- **0.031** the p-value: "a gap exists", nothing about its size

- Rejecting "no difference" was the right call: the true gap is not zero.
- The study's estimate is well below the truth. The p-value gave no hint of that.

#### [day3#check-shuffle] What does one shuffle assume?

*Checkpoint*

**Question:** A pilot gave 60 customers a new bill layout and 60 the old one, by lot. To test the difference in mean hold time, the analyst shuffles the 120 layout labels. What does each shuffle take for granted?

- A. That the layout has no effect, so any 60 customers could carry the new label
- B. That the new layout shortens hold time for every customer
- C. That hold times follow a normal distribution
- D. That the 120 customers are replaced by new ones each time

#### [day3#lab-3-1] Shuffle the contractor labels

Lab 3.1 · 25 min

Test the difference in mean satisfaction between the two contractors by shuffling their labels 5,000 times, then run Welch's t-test on the same study and compare the two p-values.

[D3_1_permutation_test.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D3_1_permutation_test.ipynb)

- [ ] The observed difference in mean satisfaction (4 min)
- [ ] One shuffle of the contractor labels (4 min)
- [ ] 5,000 shuffles: the null distribution (7 min)
- [ ] The two-sided permutation p-value (4 min)
- [ ] Welch's t-test beside it (6 min)
- [ ] ✱ Stretch: Test the difference in medians, for which no classical test is at hand

### Session 2: p-values and their misreadings

#### [day3#s2] p-values and their misreadings

*Session 2*

- Explain what a p-value describes and what it does not
- Identify five common misreadings of p-values and intervals
- Check a claim about p-values by simulating studies with the truth known

#### [day3#p-value-definition] A p-value is the share of null worlds at least as extreme as yours

*One sentence to keep*

- "**If** the two contractors were really the same, a difference at least as large as the one we observed would turn up in about 3 studies in 100."

- **It starts with "if".** The null is assumed, not assessed.
- **It is about data.** How unusual this result is, not how likely a hypothesis is.
- **It knows nothing of size.** Small gap, huge sample: tiny p-value.

#### [day3#five-misreadings] Five misreadings turn up again and again

*What reports get wrong*

| The misreading | Why it is wrong |
| --- | --- |
| "p = 0.03: a 3% chance of no effect" | The 3% is computed assuming no effect |
| "p = 0.40: proves no effect" | A small study gives a large p-value too |
| "p = 0.001: a large effect" | A p-value mixes effect size with sample size |
| "The 95% interval for the mean holds 95% of the repairs" | The interval is about the mean, not about single repairs |
| "30 tests, 2 significant: each has a 5% chance of being false" | With 30 tests, one or two false alarms are expected |

#### [day3#simulate-the-truth] Settle the argument by simulating studies whose truth you know

*Lab 3.2, step 2*

1. **2,000 studies, null true** both groups of 100 drawn from contractor A
2. **2,000 studies, null false** one group from A, one from B: true gap 0.46
3. **4,000 p-values** each with a label: was the null true?

| p < 0.05 in | share of studies |
| --- | --- |
| studies whose null is true | 4.7% |
| studies whose null is false | 42.2% |

#### [day3#p-is-not-prob-null] Near p = 0.03, the null was true in 13% of studies, not 3%

*Lab 3.2, step 3*

**13%** of the 248 studies with p between 0.02 and 0.04 had two identical groups

- The share depends on what the p-value cannot know: how many tested hypotheses are true to begin with (here half), and how well the study detects a real gap.
- If only one hypothesis in ten were false, the share would be far higher.
- A p-value alone can never be "the chance that the null is true".

#### [day3#uniform-under-null] When nothing is going on, every p-value is equally likely

*Lab 3.2, step 4 and stretch*

- The 2,000 p-values under a true null fall evenly between 0 and 1: about 200 in each tenth.
- So 5% fall below 0.05, by construction. That is all "significant at 0.05" guarantees.
- In batches of 30 such tests: 1.38 flagged on average; at least one flag in 80% of batches.

- **Sentence 7, counted.** "30 districts tested, two significant, each with a 5% chance of being a false alarm." In batches where nothing differs, two or more flags appeared 41% of the time, and every one of them was false.

#### [day3#what-to-write] Write what the p-value says, then give the reader what it cannot

*In a report*

- **Before.** "The difference between the contractors gave p = 0.03, so there is a 3% chance that the two contractors are really the same."
- **After.** "Contractor A was rated 0.29 points higher (95% interval 0.03 to 0.55). If the contractors were the same, a gap this large would turn up in about 3 studies in 100."

> **Order of information:** the estimate, its interval, then the test. The p-value is the last thing a manager needs, not the first.

#### [day3#check-misreading] Which reading of the result is sound?

*Checkpoint*

**Question:** A trial of a new valve schedule in one district compares 40 days with it and 40 days without. Mean daily bursts fell from 3.1 to 2.8; p = 0.38. Which sentence may go in the report?

- A. The schedule has no effect on bursts
- B. There is a 38% chance that the schedule does nothing
- C. The schedule cut bursts by 10%
- D. The trial does not show an effect; a fall of this size is common by chance at this sample size

#### [day3#lab-3-2] Mark eight report sentences

Lab 3.2 · 25 min

Mark eight sentences from Zulal's district report right or wrong with a reason each, then check two of them by counting over 4,000 simulated studies whose truth is known.

[D3_2_report_sentences.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D3_2_report_sentences.ipynb)

- [ ] Mark the eight sentences with reasons, assistant off (10 min)
- [ ] Simulate 4,000 studies with the truth known (5 min)
- [ ] Check sentence 1 by counting (4 min)
- [ ] Check sentence 7 by counting (3 min)
- [ ] Score the sheet and rewrite one sentence (3 min)
- [ ] ✱ Stretch: Plot the p-values of the studies whose null is true

### Session 3: Effect size and practical significance

#### [day3#s3] Effect size and practical significance

*Session 3*

- Report a raw and a standardised effect size with an interval
- Place an interval against zero and against a practical threshold
- Estimate Type I error and power by simulation

#### [day3#how-big] The useful question is how big, and whether that matters

*After "is there a gap?"*

- The test said the contractors differ. Nizar's contract says a gap of **0.5 points or more** is material and triggers a review.
- So the decision hangs on the size of the gap, with its uncertainty.
- An **effect size** is the gap in units someone can judge.

- **Statistical significance.** The gap is unlikely to be exactly zero.
  ##### Practical significance
  The gap is large enough to act on. The threshold comes from the business, never from the data.

#### [day3#raw-and-standardised] Report the raw effect for the decision, the standardised one for comparison

*Lab 3.3, step 1*

- **Raw effect: 0.295 points.** In the units of the scale. This is what the contract's 0.5 is written in.
- **Standardised effect: d = 0.154.** The gap divided by the standard deviation of the scores, 1.91. "About a sixth of the spread of single households' scores."

- d = 0.15 means the two score distributions overlap almost completely.
- d helps compare across scales and studies. It does not say whether the gap matters.

#### [day3#interval-vs-threshold] Place the interval against zero and against the threshold

*Lab 3.3, steps 2 and 3*

Figure: Bootstrap interval for the satisfaction gap, 400 responses per contractor.

- Excludes 0: the gap is real.
- Includes 0.5: material or not is **not settled**.
- The estimate, 0.29, is below the threshold.

#### [day3#four-positions] An interval can sit in four positions, and each has its own sentence

*A reading rule*

| The interval | The sentence |
| --- | --- |
| includes 0, lies below the threshold | No gap shown; a material gap is ruled out |
| excludes 0, lies wholly below the threshold | A real gap, and not a material one |
| excludes 0, includes the threshold | A real gap; material or not is not settled |
| lies wholly above the threshold | A real and material gap |

A fifth case, an interval that includes both 0 and the threshold, settles nothing: the study was too small for the question.

#### [day3#two-errors] A test can err in two directions

*What can go wrong*

|  | The test says "gap" | The test says "no gap shown" |
| --- | --- | --- |
| **In truth, no gap** | *Type I error*: a false alarm. Rate set by the threshold, 5% | Correct |
| **In truth, a gap** | Correct. Its rate is the **power** | *Type II error*: a miss. Rate = 1 - power |

- The 5% is chosen. The power is not: it depends on the size of the true gap and on the sample size.
- In lab 3.2, groups of 100 detected the true gap of 0.46 in 42% of studies: they missed it more often than not.

#### [day3#power-for-a-question] A study is powered for a question, not in general

*Lab 3.3, step 4*

| responses per contractor | detects that a gap exists | can show the gap is below 0.5 |
| --- | --- | --- |
| 100 | 41.3% | 4.0% |
| 400 | 93.7% | 5.2% |
| 1,600 | 100.0% | 7.6% |

- The true gap, 0.46, sits just under the threshold. Detecting it is easy; placing it on one side of 0.5 is very hard.
- For an interval narrower than 0.3 points: about 1,170 responses per contractor (stretch).

#### [day3#three-sentence-report] Three sentences: the estimate, the test, what is settled

*Lab 3.3, step 5*

- "In a study of 400 responses per contractor, households rated contractor A **0.29** points higher than contractor B on the 10-point scale (95% interval **0.03 to 0.55**). A gap of this size would be unusual if the contractors were the same, so we conclude that A is rated higher. Whether the gap reaches the contract's threshold of **0.5** points is **not settled**: the interval includes 0.5, the estimate is below it, and the study covers surveyed households of this year only."

#### [day3#check-significant-important] What do you tell the manager?

*Checkpoint*

**Question:** A bill redesign was compared on 60,000 customers before and 60,000 after. Mean time to pay fell by 0.2 days (95% interval 0.1 to 0.3; p < 0.001). Finance says only a fall of 2 days or more matters. What is the right summary?

- A. Highly significant: roll it out for the cash-flow benefit
- B. A real fall, far too small to matter: the whole interval is below 2 days
- C. No effect was found, since 0.2 days is negligible
- D. The study is inconclusive and needs a larger sample

#### [day3#lab-3-3] The effect against the threshold

Lab 3.3 · 25 min

Report the contractors' satisfaction gap as a raw and a standardised effect with a bootstrap interval, place it against the contract's threshold of 0.5 points, and measure the power of a study this size.

[D3_3_effect_threshold.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D3_3_effect_threshold.ipynb)

- [ ] Raw effect and standardised effect (5 min)
- [ ] Bootstrap interval for the difference (6 min)
- [ ] Place the interval against 0 and against 0.5 (4 min)
- [ ] Power of a study this size, by simulation (6 min)
- [ ] Write the three-sentence report (4 min)
- [ ] ✱ Stretch: Find the sample size at which the interval is narrower than 0.3 points

### Session 4: Thirty districts, many false alarms

#### [day3#s4] Thirty districts, many false alarms

*Session 4*

- Measure the false findings of 30 uncorrected tests
- Apply the Holm and Benjamini-Hochberg corrections
- Explain why the smallest districts give the most extreme estimates

#### [day3#thirty-tests] Ilyas tests all 30 districts every quarter

*The quarterly audit*

- An audit sample of 4,000 repairs. For each district: is its repair time different from the others?
- Repair times are skewed, so the test compares log hours: the estimate is a **ratio** of typical repair times.
- Districts flagged at p < 0.05 get an inspection visit.

- **The truth, on file.** Five districts truly differ: three slower by about 20%, two faster by about 14%. Twenty-five do not. You open the list after testing, not before.

#### [day3#false-alarms-expected] One audit flags seven districts, and three of them are false alarms

*Lab 3.4, steps 1 and 2*

| district | repairs | ratio | p | truth |
| --- | --- | --- | --- | --- |
| D21 | 245 | 1.25 | < 0.0001 | differs |
| D05 | 426 | 0.85 | 0.0001 | differs |
| D29 | 91 | 0.74 | 0.0009 | differs |
| D19 | 37 | 1.43 | 0.0030 | differs |
| D23 | 44 | 0.76 | 0.0091 | no difference |
| D04 | 52 | 1.32 | 0.0169 | no difference |
| D28 | 153 | 0.87 | 0.0355 | no difference |

- 4 true discoveries, 3 false, and one planted district (D16) missed.
- With 25 districts that do not differ and a 5% threshold, 1.25 false flags per audit are expected.
- Each test is working exactly as designed. Thirty of them are the problem.

#### [day3#forking-paths] Every choice made after seeing the data is another test

*The same problem without a list of tests*

- Mean or median? All tickets or closed ones? This quarter or the last two? Districts or zones?
- An analyst who tries a few and reports the one that "works" has run many tests and shown one.

- **The remedy: a plan before the data.** Write down the question, the estimand, the unit, the test and the list of comparisons first. Report every comparison on the list, and mark anything added later as exploration.

#### [day3#two-promises] Two corrections make two different promises

*Lab 3.4, step 3*

- **Holm: family-wise error.** "The chance of **even one** false flag among the 30 stays below 5%." Sort the p-values. Compare the smallest with 0.05/30, the next with 0.05/29, and so on. Stop at the first that fails.
- **Benjamini-Hochberg: false discovery rate.** "Among the districts flagged, the expected **share** of false ones stays below 5%." Compare the k-th smallest p-value with 0.05 × k/30. Flag everything up to the last one that passes.

```python
from statsmodels.stats.multitest import multipletests
reject = multipletests(p, alpha=0.05, method="holm")[0]      # or method="fdr_bh"
```

#### [day3#count-discoveries] Counted over 200 audits against the planted truth

*Lab 3.4, step 4*

| method | true discoveries per audit, of 5 | false discoveries per audit | audits with a false flag | false share of all flags |
| --- | --- | --- | --- | --- |
| no correction | 3.81 | 1.08 | 67% | 20% |
| Holm | 2.31 | 0.04 | 4% | 2% |
| Benjamini-Hochberg | 2.80 | 0.13 | 12% | 3% |

- Holm kept its promise: a false flag in 4% of audits. It pays with missed districts.
- Benjamini-Hochberg kept its own: 3% of its flags were false. It finds more.

#### [day3#small-districts-funnel] The smallest districts give the most extreme estimates by chance

*Lab 3.4, step 5*

Figure: One audit: estimated ratio of repair time, district against the others.

- Districts with no true difference and under 60 audited repairs are off by 11% on average; those with 150 or more by 6%.
- A league table sorted by estimate puts small districts at both ends, different ones each quarter.
- Before ranking units of unequal size, plot the estimate against the size.

#### [day3#worst-five-recover] Pick the worst districts and they improve next time, with nothing done

*The lowest five, measured again*

| district | wave 1 | wave 2 | all responses |
| --- | --- | --- | --- |
| D25 (13 replies) | 5.08 | 6.57 | 5.73 |
| D03 (12) | 5.33 | 5.67 | 6.43 |
| D01 (160) | 5.73 | 5.71 | 5.79 |
| D09 (47) | 5.74 | 6.49 | 6.29 |
| D19 (14) | 5.79 | 6.75 | 6.35 |
| **average** | **5.53** | **6.24** |  |

- Two survey waves of 1,500 replies each, drawn from the same 9,000. Nothing changed between them.
- The five lowest in wave 1 rose by 0.70 points. Over 1,000 pairs of waves they rise by 0.37 on average, in 92% of pairs.
- D01 is large and truly low, and stays put. The small ones were low partly by luck, and luck does not repeat.

#### [day3#extremes-need-a-control] Among equally extreme districts, treat half by lot and compare the changes

*Designing the comparison*

- **Before and after on the treated five.** A call-back programme with a true effect of +0.30 points reads as **+0.53**: the rise of the mean is credited to the programme.
- **The ten lowest, five treated by lot.** Change in the treated five minus change in the other five: **+0.29** on average. Both halves regress alike, so the rise cancels.

> **If a lot is impossible,** measure the baseline again before starting, on a fresh sample, and judge the change from that second baseline.

#### [day3#which-correction] The cost of a false flag decides the correction

*Choosing*

| The situation | Use | Because |
| --- | --- | --- |
| Each flag triggers a costly or embarrassing action: an inspection, a penalty | **Holm** | Even one false flag is expensive |
| Flags are a first screen; each gets a cheap second look | **Benjamini-Hochberg** | A few false leads are acceptable; misses are not |
| One question, one test, planned before the data | No correction | There is one test |

> **Where this continues.** Many segments and many metrics in live experiments are the subject of DS-302.

#### [day3#check-correction] Which correction fits the audit?

*Checkpoint*

**Question:** Zulal tests 40 pumping stations for abnormal energy use each month. A flagged station is shut for a two-day inspection that leaves its district on reduced pressure. Which rule should the plan name?

- A. Flag every station with p below 0.05
- B. Benjamini-Hochberg at 5%
- C. Holm at 5%
- D. Test only the stations that look abnormal on the chart

#### [day3#lab-3-4] Thirty districts at once

Lab 3.4 · 25 min

Test each of 30 districts against the others on an audit sample of repairs, count true and false discoveries with no correction, Holm and Benjamini-Hochberg over 200 audits, and plot the estimates against district size.

[D3_4_thirty_districts.ipynb](https://sdaiaacademy.github.io/ds-201/labs/D3_4_thirty_districts.ipynb)

- [ ] One audit sample: test each district against the others (6 min)
- [ ] Count discoveries at 0.05, then open the planted five (4 min)
- [ ] Holm and Benjamini-Hochberg on the same p-values (5 min)
- [ ] 200 audits: true and false discoveries by method (6 min)
- [ ] Plot each estimate against its district's size (4 min)
- [ ] ✱ Stretch: Shuffle the district labels and count how often at least one district is flagged

#### [day3#wrap-up] What to keep

*Day 3 in three lines*

- **A test is a shuffling rule.** The p-value is the share of null worlds at least as extreme as yours. It starts with "if".
- **Size against a threshold.** Report the effect with its interval and place it against zero and against what matters.
- **Count your tests.** Thirty tests give one false flag per audit. Plan the comparisons, then correct for their number.

#### [day3#next] Day 4: Regression and reporting

*Next*

How consumption moves with household size, what a slope means, and the paragraph a manager can act on.

- Tomorrow's last lab ends with your choice of capstone question. Read the three questions in `labs/capstone/README.md` tonight.
- The supervised exit check follows the teaching days: items like today's marked sheet, without an assistant.

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

#### [day4#balanced-test-precision] A leak flag checked on 300 leaks and 300 sound households reports a precision the field will not see

*A share from a sample drawn by class*

| test set | households | flagged |
| --- | --- | --- |
| confirmed leak | 300 | 243 |
| no leak | 300 | 28 |
| **precision on the set** |  | **243 / 271 = 89.7%** |

- The night-flow flag catches 81.0% of leaks and wrongly flags 9.3% of sound households. Those two rates belong to each class and carry over.
- The set is half leaks; the region is 3.0% leaks, 2,400 of 80,000 households.
- Precision and prevalence depend on the mix, so they do not carry over.

#### [day4#precision-reweighted] Weight each class back to its count on file, then recompute the share

*Put the population mix back*

| class, n = 300 each | N | N / n | flagged × N / n |
| --- | --- | --- | --- |
| leak | 2,400 | 8.0 | 1,944 |
| no leak | 77,600 | 258.7 | 7,243 |

N: households on file. n: households in the test set. N / n: the weight of each household in the set.

- **Precision in the region.** 1,944 / (1,944 + 7,243) = **21.2%**. True value, all 80,000: 19.8%. About one visit in five finds a leak, not nine in ten.
- **The same as a formula.** sensitivity × prevalence ÷ (sensitivity × prevalence + false-alarm rate × (1 − prevalence))

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

## Capstone: Capstone: the inference brief and its defence

Each participant defends one result of a brief on an unseen question in eight minutes, then answers questions for four

#### [capstone#title] Capstone: the inference brief and its defence

*SDAIA Academy · Statistical Inference by Simulation*

Capstone: Each participant defends one result of a brief on an unseen question in eight minutes, then answers questions for four

Data Science Track · 4 teaching days + capstone day · 8 min talk and demo · 4 min Q&A · DS-201

#### [capstone#agenda] How the defences run

*Capstone*

- **Expectations and final prep**: the rubric, a last rerun from the raw file, then the first defences
- **Defences**: eight minutes on one result, then four minutes of questions
- **Review and closing**: peer feedback, the trainer's review, what next

#### [capstone#rubric] The rubric

*How the capstone is scored*

| Item | Value |
| --- | --- |
| Question and estimand | 15% |
| Intervals and coverage | 25% |
| Tests and effect sizes | 25% |
| Regression and limits | 20% |
| Reproducibility | 15% |

> **Every number comes with its interval and its unit.** An estimate without an interval is a guess, and an interval without a stated resampling unit cannot be checked.

#### [capstone#format] 8 minutes for the defence, then 4 minutes of questions

*Format*

- **1 · The question.** The manager's words, then the estimand in one sentence. One slide or one cell.
- **2 · One result.** The estimate, its interval, the test and the effect size against the threshold. Rerun it live with the seed.
- **3 · Limits.** The population, the resampling unit and why, the coverage check, what the data cannot tell.

> **In the questions,** the assessor names a different resampling unit. You predict what happens to your interval, then run it and show it.

#### [capstone#running-order] Who presents when

*Running order*

| # | Presenter | Question |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |

#### [capstone#final-prep] Final prep · 20 minutes

*Before the first defence*

Rerun the notebook from the raw file, check that the numbers match the brief, and choose the one result you will defend.

#### [capstone#now-presenting] Defence

*Now presenting*

##### Questions

#### [capstone#review] What the defences showed

*Trainer review*

- **Strongest patterns.** What several briefs got right.
- **Common gaps.** What most briefs would fix next.
- **One surprise.** Something nobody expected.

#### [capstone#what-next] Keep going

*After the course*

- **Your brief stays yours:** keep the repository reproducible, and add the limit a colleague named today.
- **Follow-up task, within two weeks:** an inference brief on a table of the national Open Data Platform (`labs/followup`).
- **Next Academy course:** DS-302, Online Experiments and A/B Testing, for comparisons that are designed, not found.

#### [capstone#thanks] Thank you

*SDAIA Academy*

Statistical Inference by Simulation
