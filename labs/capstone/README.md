# Capstone: an inference brief

You answer one manager's question with an estimate, an interval, a test, an effect size and
stated limits, on a dataset you have not seen in class, and you defend one result live.

## Choose one question

The three questions and their files are in `questions.json` (lab 4.4 prints them):

| | Question | File |
|---|---|---|
| q1 | The meter-replacement programme: did smart meters reduce estimated bills, and by how much? | `data/q1_meter_replacement.csv` |
| q2 | The conservation-message pilot: did the message reduce consumption, and does the saving reach 10 litres a day? | `data/q2_conservation_message.csv` |
| q3 | The call-back change: did complaints get resolved faster, for which types, and by how much? | `data/q3_call_back.csv` |

All three are synthetic and seeded. Or bring a public dataset: agree the table and the question
with your trainer before the capstone day, state its licence in your README, and use no personal
data that is not already public and lawful to use.

## What you submit

A link to a **public GitHub repository** with:

1. `brief.md` or `brief.pdf`: at most two pages. The question, the estimand, a description of the
   data (count, middle, spread, exclusions, population), then the estimate with its interval, the
   test, the effect size against the threshold that matters, a regression if the question has a
   second variable, and the limits.
2. `analysis.ipynb`: reruns from the raw file to every number of the brief, with a fixed seed.
3. `README.md` reporting the estimates, intervals, tests, effect sizes and **a coverage check**
   (below), and how many comparisons you ran, including the ones you did not report.
4. `run_log.txt`: the printed output of one complete seeded run.

The commit history is part of the evidence: commit as you work.

## The coverage check

You do not know the truth of your dataset. Check your interval method on a case where you do:
treat your data as the population, draw 1,000 samples from it of a realistic size, **with the
same sampling unit as your study**, build your interval in each, and count how often it contains
the "population" value. Report the count next to the interval.

```python
hits = 0
for _ in range(1000):
    study = draw_sample(units, gen)          # resample the units you chose: households, districts, ...
    low, high = my_interval(study, gen)
    hits += low <= value_in_full_data <= high
print(hits / 1000)
```

## The defence

Eight minutes on one result, then four minutes of questions. During the questions the assessor
names a **different resampling unit** ("resample households, not neighbourhoods"). You predict
what will happen to the interval and why, then run it and show the effect.

## Rubric

| Criterion | Weight | Full marks look like |
|---|---|---|
| Question and estimand | 15 | The manager's question restated as one number in a named population, with the unit of analysis |
| Intervals and coverage | 25 | The right resampling unit, an interval for every headline number, a coverage count for the method |
| Tests and effect sizes | 25 | A test whose null is stated as a shuffling rule, the effect in the manager's units against a threshold, a count of comparisons and a correction if there are several |
| Regression and limits | 20 | A slope with an interval that does not rest on equal spread, a residual plot, a named confounder, and the population the conclusion applies to |
| Reproducibility | 15 | One command reruns everything from the raw file with a seed; the run log matches the brief |

Assistant policy: open (AI-full) for the work. The defence is yours alone.
