---
course: "Statistical Inference by Simulation"
code: "DS-201"
version: "2027.1.0"
deck: "day1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-201/slides/day1.html"
---

# Statistical Inference by Simulation

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
