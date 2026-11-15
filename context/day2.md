---
course: "Statistical Inference by Simulation"
code: "DS-201"
version: "2027.1.0"
deck: "day2"
day: 2
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-201/slides/day2.html"
---

# Statistical Inference by Simulation

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
- The 60th household of D05 tells you little that the first 59 did not.
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
