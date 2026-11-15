---
course: "Statistical Inference by Simulation"
code: "DS-201"
version: "2027.1.0"
deck: "day3"
day: 3
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-201/slides/day3.html"
---

# Statistical Inference by Simulation

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
- Nobody need cheat: each choice seems reasonable in the light of the data.

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
