"""Numbers quoted on three slide segments, computed from the Zulal population with fixed seeds.

    uv run python _tools/weights_and_extremes.py      (from labs/)

1. Day 2, `oversample-rare-group` and `design-weights`: a sample that oversamples households of
   nine or more people, the unweighted mean against the weighted one and the truth.
2. Day 3, `worst-five-recover` and `extremes-need-a-control`: the five districts with the lowest
   satisfaction in one survey wave, measured again in a second wave with nothing changed, and a
   randomised comparison among the ten lowest that removes the rise.
3. Day 4, `balanced-test-precision` and `precision-reweighted`: a leak flag checked on a test set
   of 300 leaks and 300 sound households, its precision there and in the population.

Nothing here is a lab answer: the labs use other groups, other waves and other seeds.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import zulal as U  # noqa: E402

REPS = 1000


def weights() -> None:
    h = U.households()
    y = h["consumption_l_day"].to_numpy(dtype=float)
    large = h["household_size"].to_numpy() >= 9
    N = {"9 or more people": int(large.sum()), "1 to 8 people": int((~large).sum())}
    n = {"9 or more people": 150, "1 to 8 people": 250}
    truth = y.mean()

    def one(gen):
        a = gen.choice(np.flatnonzero(large), n["9 or more people"], replace=False)
        b = gen.choice(np.flatnonzero(~large), n["1 to 8 people"], replace=False)
        ya, yb = y[a], y[b]
        unweighted = np.concatenate([ya, yb]).mean()
        wa, wb = N["9 or more people"] / len(a), N["1 to 8 people"] / len(b)
        weighted = (wa * ya.sum() + wb * yb.sum()) / (wa * len(a) + wb * len(b))
        return ya.mean(), yb.mean(), unweighted, weighted

    ma, mb, unw, wtd = one(U.rng(211))
    print("== 1. Design weights (day 2)")
    print(f"population: {N}, share of large households {N['9 or more people'] / sum(N.values()):.1%}")
    print(f"true mean consumption, all 80,000: {truth:.1f} l/day; large stratum {y[large].mean():.1f}, others {y[~large].mean():.1f}")
    for k, m in (("9 or more people", ma), ("1 to 8 people", mb)):
        print(f"  {k}: N = {N[k]:,}, n = {n[k]}, weight = {N[k] / n[k]:.1f}, sample mean = {m:.1f}")
    print(f"one sample of 400: unweighted mean {unw:.1f}, weighted mean {wtd:.1f}, truth {truth:.1f}")
    gen = U.rng(212)
    runs = np.array([one(gen)[2:] for _ in range(REPS)])
    print(f"over {REPS} samples: average unweighted {runs[:, 0].mean():.1f}, average weighted {runs[:, 1].mean():.1f}, truth {truth:.1f}")
    print(f"  weighted estimate: sd over samples {runs[:, 1].std(ddof=1):.1f}; unweighted misses by {runs[:, 0].mean() - truth:+.1f} on average")


def extremes() -> None:
    s = U.survey()
    score = s["satisfaction"].to_numpy(dtype=float)
    dist = s["district"].to_numpy()
    codes = np.array(sorted(set(dist)))
    wave_size = 1500
    effect = 0.3  # the call-back programme's planted effect, in points

    def wave_means(rows):
        d, y = dist[rows], score[rows]
        return np.array([y[d == c].mean() for c in codes]), np.array([(d == c).sum() for c in codes])

    def two_waves(gen):
        rows = gen.choice(len(s), 2 * wave_size, replace=False)
        return wave_means(rows[:wave_size]), wave_means(rows[wave_size:])

    print("\n== 2. Regression to the mean (day 3)")
    true_means = np.array([score[dist == c].mean() for c in codes])
    (m1, n1), (m2, n2) = two_waves(U.rng(221))
    bottom = np.argsort(m1)[:5]
    print("one pair of waves, nothing changed between them; the five lowest districts in wave 1:")
    for i in bottom:
        print(f"  {codes[i]}: wave 1 {m1[i]:.2f} (n = {n1[i]}), wave 2 {m2[i]:.2f} (n = {n2[i]}), all responses {true_means[i]:.2f}")
    print(f"  average of the five: wave 1 {m1[bottom].mean():.2f}, wave 2 {m2[bottom].mean():.2f}, rise {m2[bottom].mean() - m1[bottom].mean():+.2f}; region mean {score.mean():.2f}")

    gen = U.rng(222)
    rise_none, naive, randomised = [], [], []
    for _ in range(REPS):
        (a1, _), (a2, _) = two_waves(gen)
        low5 = np.argsort(a1)[:5]
        rise_none.append(a2[low5].mean() - a1[low5].mean())
        low10 = np.argsort(a1)[:10]
        treated = gen.choice(low10, 5, replace=False)
        control = np.setdiff1d(low10, treated)
        change_t = (a2[treated] + effect).mean() - a1[treated].mean()
        change_c = a2[control].mean() - a1[control].mean()
        naive.append(change_t)
        randomised.append(change_t - change_c)
    rise_none, naive, randomised = map(np.array, (rise_none, naive, randomised))
    print(f"over {REPS} pairs of waves with no programme: the five lowest rise by {rise_none.mean():+.2f} on average; they rise in {np.mean(rise_none > 0):.0%} of pairs")
    print(f"programme with a planted effect of +{effect}: before-and-after on the 5 treated {naive.mean():+.2f} on average;"
          f" treated minus untreated among the 10 lowest, 5 drawn by lot: {randomised.mean():+.2f} (sd {randomised.std(ddof=1):.2f})")


def precision() -> None:
    gen = U.rng(231)
    N = 80_000
    prevalence, sensitivity, false_alarm = 0.03, 0.80, 0.10
    leak = np.zeros(N, dtype=bool)
    leak[gen.choice(N, int(round(prevalence * N)), replace=False)] = True
    flag = np.where(leak, gen.random(N) < sensitivity, gen.random(N) < false_alarm)
    pop_precision = leak[flag].mean()
    print("\n== 3. Precision after sampling by class (day 4)")
    print(f"population: {N:,} households, {leak.sum():,} with a leak ({leak.mean():.1%}); flagged {flag.sum():,}; true precision {pop_precision:.1%}")
    t = gen.choice(np.flatnonzero(leak), 300, replace=False)
    f = gen.choice(np.flatnonzero(~leak), 300, replace=False)
    tp, fp = int(flag[t].sum()), int(flag[f].sum())
    print(f"test set: 300 leaks, {tp} flagged (sensitivity {tp / 300:.1%}); 300 sound, {fp} flagged (false alarms {fp / 300:.1%})")
    print(f"precision on the test set {tp / (tp + fp):.1%}; share of leaks in the test set 50%")
    w_leak, w_sound = leak.sum() / 300, (~leak).sum() / 300
    wtp, wfp = tp * w_leak, fp * w_sound
    print(f"weights: leak {w_leak:.1f}, sound {w_sound:.1f}; weighted flagged leaks {wtp:,.0f}, weighted flagged sound {wfp:,.0f}")
    print(f"reweighted precision {wtp / (wtp + wfp):.1%}; true precision {pop_precision:.1%}")
    print(f"formula: {tp / 300:.3f} x {leak.mean():.3f} / ({tp / 300:.3f} x {leak.mean():.3f} + {fp / 300:.3f} x {1 - leak.mean():.3f})")
    # The parallel case in the notes: the same flag in a district where 1% of households leak
    p1 = 0.01
    print(f"same test set, a district where 1% leak: precision {tp / 300 * p1 / (tp / 300 * p1 + fp / 300 * (1 - p1)):.1%}")


if __name__ == "__main__":
    weights()
    extremes()
    precision()
