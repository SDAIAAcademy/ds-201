# %% [markdown]
# # Lab 3.4 · Thirty districts at once
#
# Day 3 · Session 4 (Thirty districts, many false alarms) · 25 min.
#
# Each quarter Ilyas Al-Tuwaijri audits a sample of 4,000 repairs and tests every one of the 30 districts: is its repair time different from the rest? The districts he flags get a visit from Nizar Al-Khayyat's inspectors. In this population five districts truly differ and 25 do not, and the list is on file. You count how many of Ilyas's flags are true and how many are false, with no correction, with Holm's and with Benjamini-Hochberg's.
#
# **AI policy.** AI-tutor: hints one step at a time, never the simulation.
#
# **Reference state.** `data/repairs.csv` and `data/planted_districts.json`, which you open in step 2 and not before. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · One audit sample: test each district against the others (6')
# - [ ] 2 · Count discoveries at 0.05, then open the planted five (4')
# - [ ] 3 · Holm and Benjamini-Hochberg on the same p-values (5')
# - [ ] 4 · 200 audits: true and false discoveries by method (6')
# - [ ] 5 · Plot each estimate against its district's size (4')
# - [ ] ✱ Stretch · Shuffle the district labels and count how often at least one district is flagged
# - [ ] ✱ Stretch 2 · Audit the five slowest districts again, with nothing changed

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
from scipy import stats
from statsmodels.stats.multitest import multipletests
np.set_printoptions(precision=3, suppress=True)
print("mode:", U.MODE)

# %%
repairs = U.repairs()
LOG_HOURS = np.log(repairs["repair_hours"].to_numpy())
DISTRICT = repairs["district"].to_numpy()
CODES = np.array(sorted(set(DISTRICT)))
AUDIT = 4000


def draw_audit(gen):
    """Row numbers of one audit sample of 4,000 repairs."""
    return gen.choice(len(repairs), size=AUDIT, replace=False)


# %% [markdown]
# ## 1 · One audit sample: test each district against the others (6')
#
# Repair times are skewed, so the test is done on their logarithms: a difference of log-means is a **ratio** of typical repair times. For each district: Welch's t-test of its log hours against the log hours of all other districts in the audit.
#
# ✏️ **Exercise** · Write `test_districts(rows)`. Return a table with one row per district and the columns `district`, `n` (repairs of the district in the audit), `ratio` (`exp` of the difference in log-means, district against the others) and `p`.

# %%
def test_districts(rows):
    # BEGIN SOLUTION
    y, d = LOG_HOURS[rows], DISTRICT[rows]
    out = []
    for code in CODES:
        inside = d == code
        r = stats.ttest_ind(y[inside], y[~inside], equal_var=False)
        out.append((str(code), int(inside.sum()), float(np.exp(y[inside].mean() - y[~inside].mean())), float(r.pvalue)))
    return pd.DataFrame(out, columns=["district", "n", "ratio", "p"])
    # END SOLUTION


# %%
audit_rows = draw_audit(U.rng(121))
try:
    tests = test_districts(audit_rows)
except NotImplementedError:
    tests = pd.DataFrame(U.reference("d3_4", "tests"))
U.keep("d3_4", "tests", tests.to_dict(orient="list"))
print(tests.sort_values("p").head(8).round(4).to_string(index=False))
U.check(len(tests) == 30 and int(tests["n"].sum()) == AUDIT, "30 tests, one per district, on the 4,000 audited repairs")

# %% [markdown]
# ## 2 · Count discoveries at 0.05, then open the planted five (4')
#
# ✏️ **Exercise** · Write `count_true_false(flagged, planted)`: `flagged` is a list of district codes, `planted` the set of districts that truly differ. Return `(true_discoveries, false_discoveries)`.

# %%
def count_true_false(flagged, planted):
    # BEGIN SOLUTION
    flagged = set(flagged)
    return len(flagged & set(planted)), len(flagged - set(planted))
    # END SOLUTION


# %%
flag_none = tests.loc[tests["p"] < 0.05, "district"].to_list()
print(f"flagged at p < 0.05, no correction: {len(flag_none)} districts: {flag_none}")
PLANTED = U.js("planted_districts.json")
print("the planted truth, district: ratio of typical repair time:", PLANTED)
try:
    tf_none = count_true_false(flag_none, PLANTED)
except NotImplementedError:
    tf_none = U.reference("d3_4", "tf_none")
U.keep("d3_4", "tf_none", list(tf_none))
print(f"no correction: {tf_none[0]} true discoveries, {tf_none[1]} false discoveries, {5 - tf_none[0]} of the five missed")
U.check(tf_none[0] + tf_none[1] == len(flag_none) and tf_none[1] >= 1, "at least one flagged district is a false alarm in this audit")

# %% [markdown]
# **Look at.** The inspectors would visit a district where nothing is wrong. With 25 districts that do not differ and a 5% threshold, about 1.25 false flags per audit are expected: the test is working exactly as designed, 30 times.

# %% [markdown]
# ## 3 · Holm and Benjamini-Hochberg on the same p-values (5')
#
# - **Holm** controls the **family-wise error rate**: the chance of even one false flag among the 30 stays below 5%.
# - **Benjamini-Hochberg** controls the **false discovery rate**: among the districts flagged, the expected share of false ones stays below 5%.
#
# Holm by hand: sort the p-values; compare the smallest with 0.05/30, the next with 0.05/29, and so on; stop at the first that fails.
#
# ✏️ **Exercise** · Write `flag(tests, method)`: the list of districts flagged at 0.05 under `"holm"` or `"fdr_bh"`. Use `multipletests(p, alpha=0.05, method=method)[0]`, which returns a boolean array.

# %%
def flag(tests, method):
    # BEGIN SOLUTION
    reject = multipletests(tests["p"].to_numpy(), alpha=0.05, method=method)[0]
    return tests.loc[reject, "district"].to_list()
    # END SOLUTION


# %%
try:
    flags = {m: flag(tests, m) for m in ("holm", "fdr_bh")}
except NotImplementedError:
    flags = U.reference("d3_4", "flags")
U.keep("d3_4", "flags", flags)
try:
    one_audit = {"none": tuple(tf_none), "holm": count_true_false(flags["holm"], PLANTED), "fdr_bh": count_true_false(flags["fdr_bh"], PLANTED)}
except NotImplementedError:
    one_audit = {m: tuple(v) for m, v in U.reference("d3_4", "one_audit").items()}
U.keep("d3_4", "one_audit", {m: list(v) for m, v in one_audit.items()})
U.table(["method", "true discoveries", "false discoveries"], [[m, t, f] for m, (t, f) in one_audit.items()])
smallest = np.sort(tests["p"].to_numpy())[:4]
print("Holm by hand, the four smallest p-values against 0.05/30, 0.05/29, ...:", [f"{p:.5f} < {0.05 / (30 - i):.5f}: {p < 0.05 / (30 - i)}" for i, p in enumerate(smallest)])
U.check(one_audit["holm"][1] == 0 and one_audit["holm"][0] <= one_audit["fdr_bh"][0] <= tf_none[0], "Holm flags no false district here and finds fewest; Benjamini-Hochberg sits between")

# %% [markdown]
# ## 4 · 200 audits: true and false discoveries by method (6')
#
# One audit is one draw. Repeat the audit 200 times and average.
#
# ✏️ **Exercise** · Write `many_audits(audits, gen)`. For each audit: `draw_audit(gen)`, `test_districts`, then for each of `"none"`, `"holm"`, `"fdr_bh"` the true and false discoveries. Return a dictionary `method -> array of shape (audits, 2)`.

# %%
def many_audits(audits, gen):
    # BEGIN SOLUTION
    out = {m: [] for m in ("none", "holm", "fdr_bh")}
    for _ in range(audits):
        t = test_districts(draw_audit(gen))
        out["none"].append(count_true_false(t.loc[t["p"] < 0.05, "district"], PLANTED))
        for m in ("holm", "fdr_bh"):
            out[m].append(count_true_false(flag(t, m), PLANTED))
    return {m: np.array(v) for m, v in out.items()}
    # END SOLUTION


# %%
AUDITS = U.pick(200, 40)
try:
    runs = many_audits(AUDITS, U.rng(122))
except NotImplementedError:
    runs = U.reference("d3_4", "runs")
runs = {m: np.asarray(v) for m, v in runs.items()}
U.keep("d3_4", "runs", runs)
rows = []
for m, v in runs.items():
    total = v.sum(axis=1)
    fdp = np.where(total > 0, v[:, 1] / np.maximum(total, 1), 0.0)
    rows.append([m, v[:, 0].mean(), v[:, 1].mean(), float(np.mean(v[:, 1] >= 1)), float(fdp.mean())])
U.table(["method", "true per audit", "false per audit", "audits with a false flag", "false share of flags"], rows, fmt="{:.2f}")
summary = {r[0]: r[1:] for r in rows}
U.keep("d3_4", "summary", summary)
U.check(summary["none"][1] > 0.8 and summary["holm"][2] < 0.12 and summary["fdr_bh"][0] > summary["holm"][0],
        "uncorrected: about one false flag per audit; Holm: a false flag in few audits; Benjamini-Hochberg: more true discoveries than Holm")

# %% [markdown]
# **Look at.** Read the two right-hand columns against the two promises. Holm promises "a false flag in fewer than 5% of audits" and pays with missed districts. Benjamini-Hochberg promises "fewer than 5% of the flags are false" and finds more. Which promise fits depends on the cost of a wasted inspection against the cost of a missed slow district: that choice is Nizar's, and it is written down before the audit, not after.

# %% [markdown]
# ## 5 · Plot each estimate against its district's size (4')

# %%
plt = U.plt()
fig, ax = plt.subplots()
is_planted = tests["district"].isin(PLANTED).to_numpy()
ax.scatter(tests["n"][~is_planted], tests["ratio"][~is_planted], color="#3a7ca5", label="no true difference (25)")
ax.scatter(tests["n"][is_planted], tests["ratio"][is_planted], color="#e4572e", marker="D", label="planted difference (5)")
ax.axhline(1.0, color="black", linewidth=1)
ax.set_xscale("log")
ax.set(xlabel="repairs of the district in the audit (log axis)", ylabel="ratio of typical repair time, district / others", title="One audit: estimates fan out as districts get small")
ax.legend()
plt.show()
null_tests = tests[~is_planted]
small, large = null_tests[null_tests["n"] < 60], null_tests[null_tests["n"] >= 150]
spread_small, spread_large = float(np.abs(np.log(small["ratio"])).mean()), float(np.abs(np.log(large["ratio"])).mean())
U.keep("d3_4", "spread", [spread_small, spread_large, len(small), len(large)])
print(f"districts with no true difference: the {len(small)} with fewer than 60 audited repairs are off by {np.expm1(spread_small):.0%} on average, the {len(large)} with 150 or more by {np.expm1(spread_large):.0%}")
U.check(spread_small > spread_large, "small districts give the most extreme estimates, by chance alone")

# %% [markdown]
# **Look at.** A league table of districts sorted by estimated ratio would put small districts at both ends, best and worst, every quarter, and different ones each time. The smallest planted district sits among them and cannot be told apart. Before ranking units of unequal size, plot the estimate against the size.

# %% [markdown]
# ## ✱ Stretch · The global null by shuffling
#
# Shuffle the district labels of the audit, so that no district differs, and test all 30 again. Over 200 shuffles, how often is at least one district flagged without correction, and with Holm?

# %%
def stretch():
    # BEGIN SOLUTION
    gen, y, d = U.rng(123), LOG_HOURS[audit_rows], DISTRICT[audit_rows]
    any_none = any_holm = 0
    reps = U.pick(200, 40)
    for _ in range(reps):
        ds = gen.permutation(d)
        p = np.array([stats.ttest_ind(y[ds == c], y[ds != c], equal_var=False).pvalue for c in CODES])
        any_none += (p < 0.05).any()
        any_holm += multipletests(p, 0.05, "holm")[0].any()
    print(f"labels shuffled, nothing differs: at least one flag in {any_none / reps:.0%} of audits without correction, {any_holm / reps:.0%} with Holm")
    return [any_none / reps, any_holm / reps]
    # END SOLUTION


try:
    U.keep("d3_4", "global_null", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## ✱ Stretch 2 · The five slowest districts, audited again
#
# Nizar proposes to send a coaching team to the five districts with the **highest** estimated ratio in this audit, and to judge the coaching by the next audit. Before any coaching happens, look at what the next audit shows when **nothing changes**: draw a second, independent audit of 4,000 repairs from the same population and estimate the same five districts again.
#
# ✏️ **Exercise** · Write `audit_again(tests, gen)`: take the five districts with the highest `ratio` in `tests`, draw a new audit with `draw_audit(gen)`, test it, and return a table with the columns `district`, `ratio_first`, `ratio_again`.

# %%
def audit_again(tests, gen):
    # BEGIN SOLUTION
    top5 = tests.nlargest(5, "ratio")[["district", "ratio"]].rename(columns={"ratio": "ratio_first"})
    again = test_districts(draw_audit(gen))[["district", "ratio"]].rename(columns={"ratio": "ratio_again"})
    return top5.merge(again, on="district")
    # END SOLUTION


try:
    again = audit_again(tests, U.rng(124))
    again["planted"] = again["district"].isin(PLANTED)
    print(again.round(3).to_string(index=False))
    excess_first = float(np.exp(np.log(again["ratio_first"]).mean()) - 1)
    excess_again = float(np.exp(np.log(again["ratio_again"]).mean()) - 1)
    print(f"the five slowest: {excess_first:+.0%} slower than the others in the first audit, {excess_again:+.0%} in the second, with nothing changed")
    U.check(excess_again < excess_first, "the five most extreme districts look less extreme in an independent audit, with no coaching at all")
    U.keep("d3_4", "audit_again", [excess_first, excess_again])
except NotImplementedError:
    print("✱ stretch 2 not done")

# %% [markdown]
# **Look at.** The five were picked **because** they were extreme, and part of being extreme was luck in that audit; the luck does not repeat, so the next audit pulls them back towards the rest. That is regression to the mean, and a before-and-after comparison would credit it to the coaching. The comparison that removes it: take the ten slowest districts, coach five of them **chosen by lot**, and compare the change in the coached five with the change in the other five, which regress just as much.

# %%
U.note(f"Checked against the planted truth over {AUDITS} audits: false flags per audit {summary['none'][1]:.2f} (none), {summary['holm'][1]:.2f} (Holm), {summary['fdr_bh'][1]:.2f} (Benjamini-Hochberg); true discoveries {summary['none'][0]:.2f}, {summary['holm'][0]:.2f}, {summary['fdr_bh'][0]:.2f} of 5.",
       "The 25 other districts differ slightly from one another in the finite population, as real districts would; they count as 'no true difference' because none was planted.",
       "Tests of each district against 'the others' are not independent. Holm's promise holds regardless; Benjamini-Hochberg's is proven for independent or positively related tests, and the count above is the check that it held here.")

# %% [markdown]
# ## Checkpoint
#
# 1. 30 tests at 0.05, nothing truly differs. How many flags do you expect?
#    <details><summary>Answer</summary>30 × 0.05 = 1.5 on average, and at least one flag in about 4 audits of 5.</details>
# 2. An inspection visit is expensive and embarrassing when the district turns out fine. Which correction?
#    <details><summary>Answer</summary>Holm: it keeps the chance of even one false flag in the audit below 5%.</details>
# 3. The audit is a first screen and every flag gets a cheap second look. Which correction?
#    <details><summary>Answer</summary>Benjamini-Hochberg: it allows a few false flags among many, and misses fewer true ones.</details>
#
# ## Carry forward
#
# The capstone rubric asks what you did about many comparisons. The answer starts with a count: how many tests did you run, including the ones you did not report?
