# Answer key for the trainer

Everything here comes from `prepare_data.py` (seed 201) and from the full-size runs of the solution
notebooks. The numbers a participant sees in class match these when the notebook runs at full
size; with `DS201_QUICK=1` they differ a little, and the stored quick references are used instead.
The population truths are also in `truth.json`.

## What is planted, and which lab finds it

| Planted in the data | Where | Found in |
|---|---|---|
| Consumption is skewed to the right: mean 470.4 litres a day, standard deviation 206.4 | `households.csv` | Lab 1.1 |
| 12 repair tickets were closed weeks late; the mean repair time is 9.86 hours with them and 8.86 without, the median 6.5 either way | `repairs.csv`, column `status` | Labs 1.3 and 1.4 |
| Households of one district resemble each other, so a two-stage sample holds less information than its row count suggests | `households.csv`, column `district` | Lab 2.3 |
| Contractor B is slower: median 7.3 hours against 5.9 for A (ratio 1.237 on closed tickets) | `repairs.csv` | Lab 2.4 |
| Contractor A is rated higher: true difference in mean satisfaction 0.462 points; the threshold that matters is 0.5 | `survey.csv` | Labs 3.1 and 3.3 |
| Five districts with a real difference in repair time: D05 (0.87), D29 (0.85) faster; D16 (1.22), D19 (1.22), D21 (1.20) slower. The other 25 do not differ | `planted_districts.json` | Lab 3.4 |
| Spread around the regression line grows with household size | `metered_2000.csv` | Lab 4.2 |
| Hot districts have larger households, and heat raises consumption: the generator uses 85 litres per person and 20 per degree | `households.csv`, `metered_2000.csv` | Lab 4.3 |
| Eight report sentences, some correct and some misread | `report_sentences.json`, key in `report_sentences_key.json` | Lab 3.2 |

## Expected results, full-size solution runs

**Day 1**
- 1.1: population mean 470.4; the first sample of 50 gives 458.8; the means of samples of 200 have a standard deviation of 14.8; of samples of 50, 49% land within 20 litres of the truth and 94% within 57 litres.
- 1.2: standard error of the mean at n = 25, 100, 400: simulated 41.5, 20.8, 10.1; by formula 41.3, 20.6, 10.3. Four times the sample halves the error. The median's standard error is larger at each size (51.4, 25.5, 13.0).
- 1.3: one ticket left open moves the mean of a sample of 200 repairs from 8.11 to 15.28 hours and the median from 6.40 to 6.50; 27 open tickets are needed to move the median by one hour.
- 1.4: the participant's five-number summary lists the late tickets apart; cells under the small-count threshold are withheld, not deleted.

**Day 2**
- 2.1: bootstrap 95% interval for the median repair time of the sample: 5.0 to 7.5 hours (truth 6.5); bootstrap standard error 0.553 against the real 0.513. Stretch: the percentile interval for the median covers the truth in 958 of 1,000 fresh samples of 150 (95.8%).
- 2.2: on closed tickets, coverage of the bootstrap interval is a little under 95% (93% to 94% at n = 40 and n = 200). With all tickets the interval for the mean covers far less often: most samples hold no late ticket.
- 2.3: 6 districts of 60 households. Resampling rows covers the truth in 72.3% of studies, resampling districts in 93.7%.
- 2.4: ratio of medians B to A, interval 0.96 to 1.44 for the lab's sample; coverage of the ratio interval 95.0% over 300 studies. Stretch: coverage of the interval for the difference of means on closed tickets 94.3% over 1,000 studies.

**Day 3**
- 3.1: observed difference in mean satisfaction 0.295; permutation p = 0.031, Welch t = 2.18 with p = 0.029; for the difference of medians the permutation p is 0.038.
- 3.2: the marked sheet is checked against `report_sentences_key.json`; six of eight is the pass mark.
- 3.3: effect 0.295 points (95% interval 0.03 to 0.55), standardised 0.154; the interval excludes zero and includes the threshold of 0.5: "real, not settled". A sample of about 1,170 per group would be needed for the planned interval width.
- 3.4: with no correction the audit flags 4 of the 5 planted districts and 3 that do not differ; Holm flags 3 and 0; Benjamini-Hochberg 4 and 0. When no district differs, 75% of audits flag at least one district without correction and 3% with Holm.

**Day 4**
- 4.1: line 63.7 + 98.48 × people; 98 litres a day is 3.0 cubic metres a month; predictions 261 and 655 for 2 and 6 people; population line 71.4 + 96.21.
- 4.2: reported standard error 1.128, bootstrap 1.409 (25% larger; the reported one is 20% smaller), robust (HC3) 1.402; coverage over 300 samples 92.0% reported and 95.0% bootstrap.
- 4.3: residual trend 17.0 litres per degree; with temperature in the model 86.19 litres per person and 19.84 per degree, new trend 0.0; correlation of size and temperature 0.38; predicted move 0.619 × 19.84 = 12.3.
- 4.4: 94.5% of 400 sampled repairs within 24 hours, interval 92.0% to 96.5% (truth 95.2%); contractor gap +1.6 points, interval -2.9 to +6.1, permutation p = 0.51.

## The capstone questions

The data are in `../capstone/data`. Each has one main trap, taught in class on other data.

| | Planted truth | The trap | A sound brief |
|---|---|---|---|
| q1 Meter replacement | Estimated bills per household occur at a rate ratio of 0.638, smart to old meters (observed means 1.199 and 1.806) | The rollout was by district, 8 smart and 12 old: the district is the unit, and households are not independent | Resamples districts; says that districts were not chosen by lot, so other differences between them may be mixed in |
| q2 Conservation message | The message lowers consumption by 18 litres a day; every neighbourhood drifts by its own amount (observed change -24.7 with the message, -5.0 without) | 40 neighbourhoods randomised 20 and 20: the neighbourhood is the unit; the question carries a threshold of 10 litres | Works on neighbourhood means of the change; reports the difference with its interval set against 10 litres |
| q3 Call-back change | Resolution time falls to 0.72 of its earlier median for billing and meter complaints; the four other types do not change | Six types tested at once; the overall ratio (medians 24.15 before, 21.4 after) mixes two real changes with four none; before-and-after is not a designed comparison | Corrects for six comparisons, reports by type, and states that anything else that changed between the periods is mixed in |

## In the defence

Name a resampling unit different from the one the participant used and ask for a prediction before
the run. Rows in place of districts or neighbourhoods: the interval narrows and is too narrow
(lab 2.3). Groups in place of rows, where rows were sampled one by one: the interval widens without
reason and becomes unstable when the groups are few.
