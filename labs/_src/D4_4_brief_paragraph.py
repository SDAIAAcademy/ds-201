# %% [markdown]
# # Lab 4.4 · One paragraph of a brief
#
# Day 4 · Session 4 (Writing an inference brief) · 25 min.
#
# A question you have not seen this week. Zulal's service standard says a leak is repaired within 24 hours. Jamila Al-Shuraim asks: "What share of repairs meet the standard, and is one contractor better at it?" You have a sample of 400 repairs. You produce the estimate, the interval and the comparison, write the one paragraph a manager reads, and check it against your own numbers. Then you choose your capstone question.
#
# **AI policy.** AI-tutor for the computation. Write the paragraph yourself: the capstone is defended live, and this is the rehearsal.
#
# **Reference state.** `data/repairs.csv`; the sample of 400 is drawn here with a seed. `capstone/questions.json` holds the three capstone questions. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · A new question: the share inside the 24-hour standard (5')
# - [ ] 2 · An interval and a contractor comparison (7')
# - [ ] 3 · Draft the estimate, interval and limits paragraph (6')
# - [ ] 4 · Check the paragraph against the numbers (3')
# - [ ] 5 · Choose the capstone question and write its estimand (4')
# - [ ] ✱ Stretch · Count the coverage of your interval method over 500 studies

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-201.git"
    if not Path("/content/ds-201").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-201"], check=True)
    os.chdir("/content/ds-201/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("zulal.py").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd
import zulal as U
np.set_printoptions(precision=3, suppress=True)
print("mode:", U.MODE)

# %%
def percentile_interval(boot, level=0.95):
    a = (1 - level) / 2 * 100
    low, high = np.percentile(boot, [a, 100 - a])
    return float(low), float(high)


repairs = U.repairs()
sample = repairs.sample(400, random_state=U.SEED + 161).reset_index(drop=True)
met = (sample["repair_hours"] <= U.SERVICE_STANDARD_HOURS).to_numpy(float)
is_a = (sample["contractor"] == "A").to_numpy()
print(f"{len(sample)} repairs sampled; {int(is_a.sum())} by contractor A, {int((~is_a).sum())} by contractor B")

# %% [markdown]
# ## 1 · A new question: the share inside the 24-hour standard (5')
#
# First the **estimand**: the number in the population that the question is about. Here: the share of all of this year's 12,000 repairs that took 24 hours or less. A share is the mean of a column of 0s and 1s, so everything you know about means applies.
#
# ✏️ **Exercise** · Return the estimate: the share of the sample that met the standard.

# %%
def estimate(met):
    # BEGIN SOLUTION
    return float(met.mean())
    # END SOLUTION


# %%
try:
    share = estimate(met)
except NotImplementedError:
    share = U.reference("d4_4", "share")
U.keep("d4_4", "share", share)
print(f"estimate: {share:.1%} of repairs met the 24-hour standard ({int(met.sum())} of {len(met)})")
U.check(0.85 < share < 0.99, "about 19 repairs in 20 meet the standard")

# %% [markdown]
# ## 2 · An interval and a contractor comparison (7')
#
# ✏️ **Exercise** · Write `analyse(met, is_a, B, gen)` returning a dictionary with:
# - `interval`: the 95% bootstrap percentile interval for the share;
# - `gap`: share of A minus share of B;
# - `gap_interval`: the 95% bootstrap interval for the gap, each contractor resampled on its own;
# - `p`: the two-sided permutation p-value for the gap (shuffle the contractor labels `B` times; `(count + 1) / (B + 1)`).

# %%
def analyse(met, is_a, B, gen):
    # BEGIN SOLUTION
    n = len(met)
    interval = percentile_interval(met[gen.integers(0, n, size=(B, n))].mean(axis=1))
    a, b = met[is_a], met[~is_a]
    gap = a.mean() - b.mean()
    boot = a[gen.integers(0, len(a), size=(B, len(a)))].mean(axis=1) - b[gen.integers(0, len(b), size=(B, len(b)))].mean(axis=1)
    null = np.empty(B)
    for i in range(B):
        lab = gen.permutation(is_a)
        null[i] = met[lab].mean() - met[~lab].mean()
    p = (np.sum(np.abs(null) >= abs(gap) - 1e-12) + 1) / (B + 1)
    return {"interval": interval, "gap": float(gap), "gap_interval": percentile_interval(boot), "p": float(p)}
    # END SOLUTION


# %%
B = U.pick(4000, 1000)
try:
    res = analyse(met, is_a, B, U.rng(162))
except NotImplementedError:
    res = U.reference("d4_4", "res")
U.keep("d4_4", "res", res)
lo, hi = res["interval"]
glo, ghi = res["gap_interval"]
print(f"share meeting the standard: {share:.1%}, 95% interval {lo:.1%} to {hi:.1%}")
print(f"contractor A minus contractor B: {res['gap'] * 100:+.1f} percentage points, 95% interval {glo * 100:+.1f} to {ghi * 100:+.1f}; permutation p = {res['p']:.2f}")
U.check(lo < share < hi and glo < res["gap"] < ghi and 0 < res["p"] <= 1, "both intervals contain their estimates and the p-value is a share")

# %% [markdown]
# **Look at.** The gap interval includes zero and the p-value is large: this sample does not show that either contractor meets the standard more often. It also does not show that they are equal. Read the width of the gap interval: that is what is still possible.

# %% [markdown]
# ## 3 · Draft the estimate, interval and limits paragraph (6')
#
# The numbers to quote, formatted as the check expects them:

# %%
NUM = {"sample size": "400", "estimate": f"{share:.1%}", "interval low": f"{lo:.1%}", "interval high": f"{hi:.1%}",
       "gap": f"{abs(res['gap']) * 100:.1f}", "p-value": f"{res['p']:.2f}"}
for k, v in NUM.items():
    print(f"{k:>14}: {v}")

# %% [markdown]
# ✏️ **Exercise** · Write the paragraph: four or five sentences. It must quote the six numbers above exactly as printed, name the **population** the conclusion applies to, and state at least one **limit**: something the analysis cannot tell. Use the words "population" and "cannot".

# %%
def my_paragraph():
    # BEGIN SOLUTION
    return (f"In a random sample of {NUM['sample size']} of this year's 12,000 leak repairs, {NUM['estimate']} were completed within the 24-hour standard "
            f"(95% interval {NUM['interval low']} to {NUM['interval high']}). "
            f"Contractor A met the standard {'more' if res['gap'] > 0 else 'less'} often than contractor B by {NUM['gap']} percentage points, "
            f"a gap that could easily arise by chance (permutation p = {NUM['p-value']}; 95% interval {glo * 100:+.1f} to {ghi * 100:+.1f} points). "
            f"The population these numbers describe is the repairs logged this year at Zulal, including tickets that were closed late in the system. "
            f"The sample cannot tell whether a late ticket was a late repair or a late entry, and it cannot show that the two contractors are equal: a gap of a few points either way remains possible.")
    # END SOLUTION


# %%
try:
    paragraph = my_paragraph()
except NotImplementedError:
    paragraph = U.reference("d4_4", "paragraph")
U.keep("d4_4", "paragraph", paragraph)
print(paragraph)

# %% [markdown]
# ## 4 · Check the paragraph against the numbers (3')

# %%
ok = U.brief_check(paragraph, NUM, ["population", "cannot", "95%"])
TRUE = float((repairs["repair_hours"] <= U.SERVICE_STANDARD_HOURS).mean())
print(f"and against the truth: {TRUE:.1%} of all 12,000 repairs met the standard; your interval {'contains' if lo <= TRUE <= hi else 'MISSES'} it")

# %% [markdown]
# **Look at.** The check is mechanical: it finds numbers and words. It cannot tell whether the paragraph is honest. Swap paragraphs with a neighbour and ask one question each: "which sentence would you challenge?"

# %% [markdown]
# ## 5 · Choose the capstone question and write its estimand (4')

# %%
questions = U.js("../capstone/questions.json")
for q in questions:
    print(f"{q['id']} · {q['title']} ({q['from']})\n   {q['question']}\n   data: {q['file']}: {q['columns']}\n   think about: {q['think_about']}\n")

# %% [markdown]
# ✏️ **Exercise** · Return your choice: the question id (`"q1"`, `"q2"`, `"q3"`, or `"own"` for a public dataset your trainer has approved), the estimand in one sentence of at least ten words, and the unit you will resample.

# %%
def my_choice():
    # BEGIN SOLUTION
    return {"question": "q2",
            "estimand": "The difference between message and control neighbourhoods in the mean change of daily consumption per household, in litres a day.",
            "unit": "neighbourhood"}
    # END SOLUTION


# %%
try:
    choice = my_choice()
except NotImplementedError:
    choice = U.reference("d4_4", "choice")
U.keep("d4_4", "choice", choice)
print(choice)
U.check(choice["question"] in {"q1", "q2", "q3", "own"} and len(choice["estimand"].split()) >= 10 and choice["unit"], "a question, an estimand of at least ten words, a resampling unit")

# %% [markdown]
# ## ✱ Stretch · Is your interval method honest for a share near 100%?
#
# Draw 500 samples of 400 repairs and count how often the bootstrap interval for the share contains the truth.

# %%
def stretch():
    # BEGIN SOLUTION
    gen, hits, studies = U.rng(163), 0, U.pick(500, 100)
    all_met = (repairs["repair_hours"] <= U.SERVICE_STANDARD_HOURS).to_numpy(float)
    for _ in range(studies):
        s = gen.choice(all_met, size=400, replace=False)
        l, h = percentile_interval(s[gen.integers(0, 400, size=(1000, 400))].mean(axis=1))
        hits += l <= TRUE <= h
    print(f"coverage over {studies} studies: {hits / studies:.1%}")
    return hits / studies
    # END SOLUTION


try:
    U.keep("d4_4", "coverage", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the truth: {TRUE:.1%} of all repairs met the standard; the interval {lo:.1%} to {hi:.1%} {'contains' if lo <= TRUE <= hi else 'misses'} it.",
       "Checked mechanically: the paragraph quotes its six numbers and names the population and a limit.",
       "Not checked: whether a colleague would sign the paragraph. Swap and read.")

# %% [markdown]
# ## Checkpoint
#
# 1. What is the estimand of "is one contractor better at meeting the standard"?
#    <details><summary>Answer</summary>The difference between the two contractors in the share of all their repairs this year that took 24 hours or less.</details>
# 2. The gap interval runs from -3 to +5 points. Can you write "the contractors perform equally"?
#    <details><summary>Answer</summary>No. Write that no difference was shown and that a gap of up to about 5 points either way is still possible.</details>
# 3. Name the five parts the capstone brief must contain.
#    <details><summary>Answer</summary>An estimate, an interval, a test, an effect size and the stated limits, for a question turned into an estimand.</details>
#
# ## Carry forward
#
# Your choice goes into the first lines of your capstone README: the question, the estimand, the unit. Start from `capstone/README.md`.
