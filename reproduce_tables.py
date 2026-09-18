"""
Recomputes Table 1 and Table 2 of the manuscript from the deposited result tables.
Reproduces the published values exactly; no annotator queries are made.

    python reproduce_tables.py --data ./data --out .
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) or ".")
import numpy as np, pandas as pd
from precheck import cp_ci, c2_threshold, min_seed, split_conformal

LABELS = list(range(9))
ALPHAS = [0.05, 0.10, 0.20, 0.30]
RATIOS = [0.25, 0.50, 0.75]


def table1():
    rows = []
    for a in ALPHAS:
        for r in RATIOS:
            rows.append({"Target alpha": a, "True e0": round(a * r, 4), "e0 / alpha": r,
                         "Minimum seed images (80% power)": min_seed(a, a * r),
                         "Minimum n_cal (condition C1)": int(np.ceil(1 / a) - 1)})
    return pd.DataFrame(rows)


def table2(pf):
    y = pf.n_visible.values
    gap = (pf.n - pf.n_visible).values
    subsets = [("Fully rendered frames", gap == 0), ("Under-rendered frames", gap > 0),
               ("All frames", np.ones(len(pf), bool))]
    rows = []
    for scorer, pre in [("Repeated sampling", "rep"), ("Perturbation ensemble", "pert")]:
        P = pf[[f"{pre}_p{i}" for i in LABELS]].values
        for name, mask in subsets:
            k = int((P[mask, y[mask]] == 0).sum()); n = int(mask.sum())
            lo, hi = cp_ci(k, n)
            row = {"Scorer": scorer, "Frame subset": name, "n": n, "e0": round(k / n, 3),
                   "e0 95% CI low": round(lo, 3), "e0 95% CI high": round(hi, 3),
                   "Accuracy": round(float((pf[f"{pre}_majority"].values[mask] == y[mask]).mean()), 3)}
            for a in (0.20, 0.30):
                s, _cov, g = split_conformal(P[mask], y[mask], a)
                row[f"Set size a={a:.2f}"] = round(s, 2)
                row[f"Yield % a={a:.2f}"] = round(g * 100, 1)
            rows.append(row)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="./data")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    pf = pd.read_csv(os.path.join(a.data, "a3_pilot_per_frame.csv"))
    t1, t2 = table1(), table2(pf)
    t1.to_excel(os.path.join(a.out, "Table_1_seed_sizing.xlsx"), index=False)
    t2.to_excel(os.path.join(a.out, "Table_2_stratified_precheck.xlsx"), index=False)
    print(t1.to_string(index=False)); print(); print(t2.to_string(index=False))
