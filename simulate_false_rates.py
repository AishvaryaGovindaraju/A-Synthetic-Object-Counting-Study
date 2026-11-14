"""
Monte Carlo false-go / false-no-go rates of the three-condition precheck decision rule
(Supplemental File 1, precheck.py), added in response to Reviewer #2's request to evaluate
the decision rule's false-go and false-no-go behavior.

For a hypothesized true unanimous-error rate e0, this simulates n_sims draws of a seed
sample of size n, applies the exact C1/C2/C3 decision rule, and reports:
  - false-go rate  = P(decision == GO   | true e0 is ABOVE the C2/C3 threshold)  -> incorrectly optimistic
  - false-no-go rate = P(decision == NO-GO | true e0 is AT OR BELOW the threshold) -> incorrectly conservative

Usage:
    python simulate_false_rates.py --out Table_3_false_go_no_go_rates.csv
"""
import argparse
import numpy as np
from scipy import stats
from precheck import c2_threshold


def simulate_decision_rate(n, n_cal, alpha, true_e0, n_sims=30000, seed=0):
    """Monte Carlo P(decision == GO) when the TRUE unanimous-error rate is true_e0."""
    rng = np.random.default_rng(seed)
    thr = c2_threshold(alpha, n_cal)
    c1 = n_cal >= int(np.ceil(1 / alpha) - 1)
    if not c1 or not np.isfinite(thr):
        return 0.0, thr
    ks = rng.binomial(n, true_e0, size=n_sims)
    e0_hats = ks / n
    his = np.where(ks == n, 1.0, stats.beta.ppf(0.975, ks + 1, n - ks))
    go = (e0_hats <= thr) & (his <= thr)
    return float(go.mean()), thr


CONFIGS = [("Preliminary seed sample", 30, 15), ("Full confirmatory benchmark", 195, 98)]
ALPHAS = [0.20, 0.30]
RATIOS = [0.50, 0.75, 1.00, 1.25, 1.50]


def table3(n_sims=30000):
    import pandas as pd
    rows = []
    for label, n, n_cal in CONFIGS:
        for a in ALPHAS:
            for r in RATIOS:
                true_e0 = r * a
                p_go, thr = simulate_decision_rate(n, n_cal, a, true_e0, n_sims=n_sims,
                                                     seed=hash((label, a, r)) % 2**32)
                feasible = bool(true_e0 <= thr) if np.isfinite(thr) else False
                rows.append({
                    "Seed sample": label, "n": n, "n_cal": n_cal, "Target alpha": a,
                    "True e0 / alpha": r, "True e0": round(true_e0, 4),
                    "Decision threshold (C2/C3)": round(thr, 4) if np.isfinite(thr) else "C1 fails",
                    "Truly feasible (true e0 <= threshold)": feasible,
                    "Simulated P(GO)": round(p_go, 4),
                    "False-go rate": round(p_go, 4) if not feasible else None,
                    "False-no-go rate": round(1 - p_go, 4) if feasible else None,
                })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="Table_3_false_go_no_go_rates.csv")
    ap.add_argument("--n-sims", type=int, default=30000)
    a = ap.parse_args()
    t3 = table3(a.n_sims)
    t3.to_csv(a.out, index=False)
    print(t3.to_string(index=False))
