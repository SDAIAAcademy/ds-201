"""Write the synthetic population of Zulal Water Utility into labs/data/.

    uv run python prepare_data.py

Fixed seed, the same bytes on every run. Zulal is fictional: no real utility, household,
contractor or district is described. The files are committed; run this only to rebuild them.

What is planted, and which lab finds it, is listed in solutions/answer_key.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 201
LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
CAP = LABS / "capstone" / "data"

N_HOUSEHOLDS, N_REPAIRS, N_SURVEY, N_DISTRICTS = 80_000, 12_000, 9_000, 30

# The five districts with a planted, true difference in repair time (lab 3.4): code -> multiplier.
# Ranks by size, largest first. Three are slower and two faster, so the utility-wide level barely moves.
PLANTED_RANKS = {2: 0.87, 4: 1.20, 13: 1.22, 17: 0.85, 26: 1.22}


def keys(rng, n: int, prefix: str) -> list[str]:
    """Pseudonymised keys: a prefix and eight hexadecimal digits, unique, in no meaningful order."""
    out = set()
    while len(out) < n:
        out.update(f"{prefix}{v:08x}" for v in rng.integers(0, 16 ** 8, size=n - len(out)))
    out = sorted(out)
    rng.shuffle(out)
    return out


def write(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, lineterminator="\n")


def districts(rng) -> pd.DataFrame:
    w = rng.lognormal(0.0, 0.85, N_DISTRICTS)
    size = np.maximum(700, np.round(w / w.sum() * N_HOUSEHOLDS)).astype(int)
    size[np.argmax(size)] += N_HOUSEHOLDS - size.sum()
    temp = np.round(rng.uniform(33.0, 45.0, N_DISTRICTS), 1)
    d = pd.DataFrame({"district": [f"D{i + 1:02d}" for i in range(N_DISTRICTS)],
                      "households": size, "summer_temp_c": temp})
    return d


def households(rng, d: pd.DataFrame) -> pd.DataFrame:
    district = np.repeat(d["district"].to_numpy(), d["households"].to_numpy())
    temp_d = np.repeat(d["summer_temp_c"].to_numpy(), d["households"].to_numpy())
    temp = np.round(temp_d + rng.normal(0, 0.8, N_HOUSEHOLDS), 1)
    lam = np.clip(3.4 + 0.22 * (temp - 39.0), 1.2, None)
    size = np.minimum(1 + rng.poisson(lam), 12)
    noise = rng.normal(0, 1, N_HOUSEHOLDS) * (15 + 14 * size)
    litres = np.maximum(30, np.round(140 + 85 * size + 20 * (temp - 39.0) + noise)).astype(int)
    h = pd.DataFrame({"household_key": keys(rng, N_HOUSEHOLDS, "HK"), "district": district,
                      "household_size": size, "temperature_c": temp, "consumption_l_day": litres})
    return h.sample(frac=1, random_state=SEED).reset_index(drop=True)


def repairs(rng, d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    p = d["households"].to_numpy() / d["households"].sum()
    district = rng.choice(d["district"].to_numpy(), size=N_REPAIRS, p=p)
    contractor = rng.choice(["A", "B"], size=N_REPAIRS)
    order = d.sort_values("households", ascending=False)["district"].to_list()
    planted = {order[rank]: mult for rank, mult in PLANTED_RANKS.items()}
    mult = np.array([planted.get(x, 1.0) for x in district])
    median = np.where(contractor == "A", 6.0, 7.2) * mult
    hours = np.round(median * rng.lognormal(0, 0.75, N_REPAIRS), 1)
    hours = np.maximum(hours, 0.3)
    left_open = rng.choice(N_REPAIRS, size=12, replace=False)
    hours[left_open] = np.round(rng.uniform(500, 2400, 12), 1)
    status = np.full(N_REPAIRS, "closed", dtype=object)
    status[left_open] = "closed_late_entry"
    r = pd.DataFrame({"repair_key": keys(rng, N_REPAIRS, "RP"), "district": district,
                      "contractor": contractor, "repair_hours": hours, "status": status})
    return r, planted


def survey(rng, h: pd.DataFrame, d: pd.DataFrame) -> pd.DataFrame:
    rows = h.sample(N_SURVEY, random_state=SEED + 1)
    effect = dict(zip(d["district"], rng.normal(0, 0.6, N_DISTRICTS)))
    contractor = rng.choice(["A", "B"], size=N_SURVEY)
    latent = (6.55 + rows["district"].map(effect).to_numpy() + 0.42 * (contractor == "A")
              + rng.normal(0, 1.8, N_SURVEY))
    score = np.clip(np.round(latent), 1, 10).astype(int)
    s = pd.DataFrame({"response_key": keys(rng, N_SURVEY, "SV"),
                      "household_key": rows["household_key"].to_numpy(),
                      "district": rows["district"].to_numpy(), "contractor": contractor,
                      "satisfaction": score})
    return s.reset_index(drop=True)


SENTENCES = [
    {"id": 1, "text": "The difference between the contractors gave p = 0.03, so there is a 3% chance that the two contractors are really the same.",
     "verdict": "wrong", "reason": "A p-value is computed assuming no difference; it is not the probability that the assumption is true."},
    {"id": 2, "text": "District D07 showed no significant change (p = 0.40), which proves that the new valve schedule has no effect there.",
     "verdict": "wrong", "reason": "A large p-value is absence of evidence: a small sample or a small effect gives it too. The interval shows what is still possible."},
    {"id": 3, "text": "If the two contractors truly had the same satisfaction, a difference at least as large as the one we observed would turn up in about 3 studies in 100.",
     "verdict": "right", "reason": "This is the definition: how often the null rule produces a result at least this extreme."},
    {"id": 4, "text": "With p = 0.001 the effect of the reminder message is large and worth rolling out.",
     "verdict": "wrong", "reason": "A p-value mixes effect size and sample size. A tiny effect in a huge sample gives a tiny p-value. Size needs an estimate with an interval."},
    {"id": 5, "text": "The 95% interval for the mean repair time is 8.1 to 9.6 hours, so 95% of repairs take between 8.1 and 9.6 hours.",
     "verdict": "wrong", "reason": "The interval is about the mean, not about single repairs. Single repairs spread far wider: that is the standard deviation, not the standard error."},
    {"id": 6, "text": "We used a 95% method: across many studies run this way, about 95 in 100 of the intervals it produces would contain the true mean.",
     "verdict": "right", "reason": "Coverage is a property of the method over repeated studies."},
    {"id": 7, "text": "We tested all 30 districts at the 0.05 level and found two significant ones, so each of the two findings has only a 5% chance of being a false alarm.",
     "verdict": "wrong", "reason": "With 30 tests and no true differences, one or two results below 0.05 are expected. The chance that a flagged district is a false alarm can be far above 5%."},
    {"id": 8, "text": "The standard error of the mean consumption, 4.1 litres, describes how far a sample mean of this size typically lands from the population mean.",
     "verdict": "right", "reason": "The standard error is the spread of the sampling distribution of the statistic."},
]


def capstone(rng) -> dict:
    """Three datasets not used in class, each with its truth for the trainer."""
    truth = {}

    # Q1: smart meters rolled out by district; outcome: estimated bills in 12 months
    dcodes = [f"M{i + 1:02d}" for i in range(20)]
    smart_d = set(rng.choice(dcodes, size=8, replace=False))
    d_eff = dict(zip(dcodes, rng.normal(0, 0.25, 20)))
    rows = []
    for dc in dcodes:
        n = int(rng.integers(90, 240))
        size = np.minimum(1 + rng.poisson(3.3, n), 12)
        smart = dc in smart_d
        rate = np.exp(0.55 + d_eff[dc] - (0.45 if smart else 0.0) + 0.04 * (size - 4))
        bills = np.minimum(rng.poisson(rate * rng.gamma(2.0, 0.5, n)), 12)
        rows.append(pd.DataFrame({"district": dc, "meter": "smart" if smart else "old",
                                  "household_size": size, "estimated_bills_12m": bills}))
    q1 = pd.concat(rows, ignore_index=True)
    q1.insert(0, "household_key", keys(rng, len(q1), "HK"))
    write(q1, CAP / "q1_meter_replacement.csv")
    truth["q1"] = {"planted_rate_ratio_smart_to_old": round(float(np.exp(-0.45)), 3),
                   "unit": "district (8 smart, 12 old): the rollout was by district, so households are not independent",
                   "observed_means": q1.groupby("meter")["estimated_bills_12m"].mean().round(3).to_dict()}

    # Q2: conservation message, 40 neighbourhoods randomised 20 and 20
    rows = []
    arm = rng.permutation(["message"] * 20 + ["control"] * 20)
    for i in range(40):
        n = int(rng.integers(35, 70))
        size = np.minimum(1 + rng.poisson(3.5, n), 12)
        before = np.maximum(60, 150 + 84 * size + rng.normal(0, 20) + rng.normal(0, 1, n) * (20 + 12 * size))
        drift = rng.normal(-4, 9)  # the neighbourhood's own change between the two months
        effect = -18.0 if arm[i] == "message" else 0.0
        after = np.maximum(40, before + drift + effect + rng.normal(0, 28, n))
        rows.append(pd.DataFrame({"neighbourhood": f"N{i + 1:02d}", "arm": arm[i], "household_size": size,
                                  "litres_day_before": np.round(before).astype(int),
                                  "litres_day_after": np.round(after).astype(int)}))
    q2 = pd.concat(rows, ignore_index=True)
    q2.insert(0, "household_key", keys(rng, len(q2), "HK"))
    write(q2, CAP / "q2_conservation_message.csv")
    truth["q2"] = {"planted_effect_litres_day": -18.0,
                   "unit": "neighbourhood (40, randomised 20 and 20); every neighbourhood drifts by its own amount",
                   "observed_change_by_arm": (q2.assign(change=q2["litres_day_after"] - q2["litres_day_before"])
                                              .groupby("arm")["change"].mean().round(2).to_dict())}

    # Q3: call-back within one working day, before and after, two centres, six complaint types
    n = 2400
    period = rng.choice(["before", "after"], size=n)
    centre = rng.choice(["North", "South"], size=n, p=[0.55, 0.45])
    kinds = ["billing", "low pressure", "leak", "water quality", "meter", "other"]
    kind = rng.choice(kinds, size=n, p=[0.3, 0.2, 0.18, 0.1, 0.12, 0.1])
    complexity = rng.integers(1, 6, size=n)
    base = {"billing": 20, "low pressure": 30, "leak": 26, "water quality": 40, "meter": 22, "other": 18}
    ratio = np.where(period == "after", np.where(np.isin(kind, ["billing", "meter"]), 0.72, 1.0), 1.0)
    med = np.array([base[k] for k in kind]) * (1 + 0.18 * (complexity - 3)) * np.where(centre == "South", 1.1, 1.0) * ratio
    hours = np.round(med * rng.lognormal(0, 0.8, n), 1)
    q3 = pd.DataFrame({"complaint_key": keys(rng, n, "CP"), "period": period, "centre": centre, "type": kind,
                       "complexity": complexity, "resolution_hours": hours})
    write(q3, CAP / "q3_call_back.csv")
    truth["q3"] = {"planted_median_ratio_after_to_before": {"billing": 0.72, "meter": 0.72, "the four other types": 1.0},
                   "note": "six types tested at once: two true differences, four none; the overall ratio mixes them",
                   "observed_medians": q3.groupby("period")["resolution_hours"].median().round(2).to_dict()}
    return truth


def main() -> None:
    rng = np.random.default_rng(SEED)
    d = districts(rng)
    h = households(rng, d)
    r, planted = repairs(rng, d)
    s = survey(rng, h, d)
    write(d, DATA / "districts.csv")
    write(h, DATA / "households.csv")
    write(r, DATA / "repairs.csv")
    write(s, DATA / "survey.csv")

    # Supplied study samples: the reference states of the labs that analyse one study
    study = np.random.default_rng(SEED + 2)
    a = s[s["contractor"] == "A"].sample(400, random_state=int(study.integers(1 << 30)))
    b = s[s["contractor"] == "B"].sample(400, random_state=int(study.integers(1 << 30)))
    write(pd.concat([a, b]).sample(frac=1, random_state=SEED).reset_index(drop=True), DATA / "study_satisfaction.csv")
    write(h.sample(2000, random_state=int(study.integers(1 << 30))).reset_index(drop=True), DATA / "metered_2000.csv")

    public = [{"id": x["id"], "text": x["text"]} for x in SENTENCES]
    (DATA / "report_sentences.json").write_text(json.dumps(public, indent=1) + "\n", encoding="utf-8", newline="\n")
    (DATA / "report_sentences_key.json").write_text(json.dumps(SENTENCES, indent=1) + "\n", encoding="utf-8", newline="\n")
    (DATA / "planted_districts.json").write_text(json.dumps(planted, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    X = np.column_stack([np.ones(len(h)), h["household_size"], h["temperature_c"]])
    y = h["consumption_l_day"].to_numpy(float)
    truth = {
        "consumption_mean": float(y.mean()), "consumption_sd": float(y.std()),
        "repair_mean": float(r["repair_hours"].mean()), "repair_median": float(r["repair_hours"].median()),
        "repair_median_A": float(r.loc[r.contractor == "A", "repair_hours"].median()),
        "repair_median_B": float(r.loc[r.contractor == "B", "repair_hours"].median()),
        "satisfaction_mean": float(s["satisfaction"].mean()),
        "satisfaction_A_minus_B": float(s.loc[s.contractor == "A", "satisfaction"].mean() - s.loc[s.contractor == "B", "satisfaction"].mean()),
        "slope_size_alone": float(np.polyfit(h["household_size"], y, 1)[0]),
        "slope_size_with_temperature": float(np.linalg.lstsq(X, y, rcond=None)[0][1]),
        "slope_temperature": float(np.linalg.lstsq(X, y, rcond=None)[0][2]),
        "planted_districts": planted,
        "capstone": capstone(np.random.default_rng(SEED + 3)),
    }
    (LABS / "solutions").mkdir(exist_ok=True)
    (LABS / "solutions" / "truth.json").write_text(json.dumps(truth, indent=1) + "\n", encoding="utf-8", newline="\n")
    for k, v in truth.items():
        if k != "capstone":
            print(f"{k:32} {v}")
    print("districts by size:", d.sort_values("households")["households"].to_list())


if __name__ == "__main__":
    main()
