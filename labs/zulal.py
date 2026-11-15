"""Helpers for the DS-201 labs: the population of Zulal Water Utility, checks and safety nets.

    import zulal as U

Plain NumPy, pandas and the standard library. Nothing calls a model.

Environment variables
    DS201_QUICK=1      fewer simulated studies and resamples, for a fast run
    DS201_STRICT=1     solution runs: a failed check stops the run
    DS201_WRITE_REF=1  the trainer's run that writes data/reference/ (the safety nets read it)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

for _stream in (sys.stdout, sys.stderr):  # a Windows console or a redirected run may not default to UTF-8
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
REF = DATA / "reference"

QUICK = os.environ.get("DS201_QUICK", "0") == "1"
STRICT = os.environ.get("DS201_STRICT", "0") == "1"
WRITE_REF = os.environ.get("DS201_WRITE_REF", "0") == "1"
MODE = "quick" if QUICK else "full"
SEED = 201

THRESHOLD = 0.5  # points on the 10-point scale: the difference Zulal's contract clause calls material
SERVICE_STANDARD_HOURS = 24.0


def pick(full, quick):
    """The full value, or the small one in quick mode."""
    return quick if QUICK else full


def rng(offset: int = 0) -> np.random.Generator:
    """A seeded generator. The same offset gives the same draws on every run."""
    return np.random.default_rng(SEED + offset)


# ---------------------------------------------------------------- checks and safety nets

def check(ok, what: str) -> bool:
    """Print a tick or a cross. In a solution run (DS201_STRICT=1) a cross stops the run."""
    ok = bool(ok)
    print(("✅ " if ok else "❌ ") + what)
    if STRICT and not ok:
        raise AssertionError(what)
    return ok


def _jsonable(v):
    if isinstance(v, np.ndarray):
        return {"__array__": v.tolist()}
    if isinstance(v, (np.floating, np.integer, np.bool_)):
        return v.item()
    if isinstance(v, dict):
        return {str(k): _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    return v


def _unjson(v):
    if isinstance(v, dict):
        if "__array__" in v:
            return np.array(v["__array__"])
        return {k: _unjson(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_unjson(x) for x in v]
    return v


def keep(lab: str, name: str, value):
    """Return value. In the trainer's run, also store it as the reference of this exercise."""
    if WRITE_REF:
        REF.mkdir(parents=True, exist_ok=True)
        path = REF / f"{lab}.{MODE}.json"
        store = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        store[name] = _jsonable(value)
        path.write_text(json.dumps(store, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return value


def reference(lab: str, name: str):
    """The reference result of an exercise, so the cells after it run when it is not done yet."""
    if STRICT:
        raise AssertionError(f"the solution run reached the safety net of {lab}/{name}")
    print(f"↪ exercise not done yet: using the reference result for {name}")
    store = json.loads((REF / f"{lab}.{MODE}.json").read_text(encoding="utf-8"))
    return _unjson(store[name])


# ---------------------------------------------------------------- the population and the study files

def districts() -> pd.DataFrame:
    """30 districts: district, households, summer_temp_c."""
    return pd.read_csv(DATA / "districts.csv")


def households() -> pd.DataFrame:
    """The population: 80,000 metered households. household_key is a pseudonym, never a name or an address."""
    return pd.read_csv(DATA / "households.csv")


def repairs() -> pd.DataFrame:
    """The population: 12,000 leak repairs. repair_hours is skewed; contractor is A or B."""
    return pd.read_csv(DATA / "repairs.csv")


def survey() -> pd.DataFrame:
    """The population: 9,000 survey responses, satisfaction 1 to 10."""
    return pd.read_csv(DATA / "survey.csv")


def study_satisfaction() -> pd.DataFrame:
    """One study: 400 responses for each contractor, drawn at random from the survey."""
    return pd.read_csv(DATA / "study_satisfaction.csv")


def metered() -> pd.DataFrame:
    """One study: 2,000 households drawn at random from the 80,000."""
    return pd.read_csv(DATA / "metered_2000.csv")


def js(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def two_stage_sample(gen: np.random.Generator, n_districts: int = 12, per_district: int = 40) -> pd.DataFrame:
    """A two-stage survey sample: districts first, then responses inside each chosen district.

    Districts are chosen with probability proportional to their number of responses, so the plain
    mean of the sample is a fair estimate of the mean of all 9,000 responses.
    """
    s = _survey_cache()
    counts = s["district"].value_counts().sort_index()
    chosen = gen.choice(counts.index.to_numpy(), size=n_districts, replace=False, p=(counts / counts.sum()).to_numpy())
    parts = []
    for d in chosen:
        rows = _SURVEY_ROWS[d]
        parts.append(s.iloc[gen.choice(rows, size=per_district, replace=False)])
    return pd.concat(parts, ignore_index=True)


_SURVEY = None
_SURVEY_ROWS: dict = {}


def _survey_cache() -> pd.DataFrame:
    global _SURVEY
    if _SURVEY is None:
        _SURVEY = survey()
        for d, idx in _SURVEY.groupby("district").indices.items():
            _SURVEY_ROWS[d] = idx
    return _SURVEY


# ---------------------------------------------------------------- the marked sheet of lab 3.2 and the brief of lab 4.4

def mark_sheet(sheet: dict) -> int:
    """Score a sheet {sentence id: (verdict, reason)} against the key. A verdict without a reason does not count."""
    key = {x["id"]: x for x in js("report_sentences_key.json")}
    score = 0
    for i in sorted(key):
        verdict, reason = sheet.get(i, ("", ""))
        has_reason = len(str(reason).split()) >= 6
        ok = verdict == key[i]["verdict"] and has_reason
        score += ok
        mark = "✅" if ok else "❌"
        why = "" if has_reason else "  (a reason of at least six words is part of the answer)"
        print(f"{mark} sentence {i}: you said {verdict or 'nothing'}; the key says {key[i]['verdict']}{why}")
        print(f"   key: {key[i]['reason']}")
    print(f"score: {score} of {len(key)} (the outcome asks for at least 6 with reasons)")
    return score


def brief_check(paragraph: str, numbers: dict, words: list[str]) -> bool:
    """Does the paragraph quote every number (as formatted) and use every required word?"""
    ok = True
    for name, shown in numbers.items():
        found = str(shown) in paragraph
        ok &= found
        print(f"{'✅' if found else '❌'} quotes the {name}: {shown}")
    low = paragraph.lower()
    for w in words:
        found = w.lower() in low
        ok &= found
        print(f"{'✅' if found else '❌'} says: {w}")
    print(f"length: {len(paragraph.split())} words")
    if STRICT and not ok:
        raise AssertionError("the brief paragraph misses a number or a required statement")
    return ok


# ---------------------------------------------------------------- plotting and tables

def plt():
    """matplotlib.pyplot with the course defaults; draws to nothing when run as a script."""
    import matplotlib
    if "ipykernel" not in sys.modules:
        import warnings
        matplotlib.use("Agg")
        warnings.filterwarnings("ignore", message=".*non-interactive.*")
    import matplotlib.pyplot as p
    p.rcParams.update({"figure.figsize": (7, 4), "axes.spines.top": False, "axes.spines.right": False,
                       "axes.grid": True, "grid.alpha": 0.25, "font.size": 11})
    return p


def table(header: list[str], rows: list[list], fmt: str = "{:.4g}") -> None:
    """Print a small aligned table."""
    cells = [[fmt.format(v) if isinstance(v, (float, np.floating)) else str(v) for v in r] for r in rows]
    widths = [max(len(h), *(len(r[i]) for r in cells)) for i, h in enumerate(header)]
    print("  ".join(h.ljust(w) for h, w in zip(header, widths)))
    for r in cells:
        print("  ".join(c.rjust(w) for c, w in zip(r, widths)))


def note(*lines: str) -> None:
    """The verification note that closes every lab: what was checked against the truth, and what was not."""
    print("VERIFICATION NOTE")
    for line in lines:
        print(" ·", line)
