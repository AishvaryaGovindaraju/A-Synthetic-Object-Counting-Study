"""
Recomputes Table 1 and Table 2 of the manuscript from the deposited result tables.
Reproduces the published values exactly and incorporates the verified 195 benchmark frames.

    python reproduce_tables.py --data ./data --out .
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) or ".")
import numpy as np, pandas as pd
from precheck import cp_ci, c2_threshold, min_seed, split_conformal

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LABELS_9 = list(range(9))
LABELS_11 = list(range(11))
ALPHAS = [0.05, 0.10, 0.20, 0.30]
RATIOS = [0.25, 0.50, 0.75]


def table_1_stratified(pf, bench=None):
    """
    Table 1: Stratified precheck and calibration results.
    Computes precheck quantities on the 30-seed sample, and optionally adds the 195 benchmark.
    """
    y = pf.n_visible.values
    gap = (pf.n - pf.n_visible).values
    subsets = [
        ("Seed: Fully rendered", gap == 0),
        ("Seed: Under-rendered", gap > 0),
        ("Seed: All frames (n=30)", np.ones(len(pf), bool))
    ]
    rows = []
    for scorer, pre in [("Repeated sampling", "rep"), ("Perturbation ensemble", "pert")]:
        P = pf[[f"{pre}_p{i}" for i in LABELS_9]].values
        for name, mask in subsets:
            k = int((P[mask, y[mask]] == 0).sum())
            n = int(mask.sum())
            lo, hi = cp_ci(k, n)
            acc = float((pf[f"{pre}_majority"].values[mask] == y[mask]).mean())
            row = {
                "Scorer": scorer,
                "Frame subset": name,
                "n": n,
                "e0": round(k / n, 3),
                "e0 95% CI low": round(lo, 3),
                "e0 95% CI high": round(hi, 3),
                "Accuracy": round(acc, 3)
            }
            for a in (0.20, 0.30):
                s, _cov, g = split_conformal(P[mask], y[mask], a, n_splits=400, seed=0)
                row[f"Set size α={a:.2f}"] = round(s, 2)
                row[f"Yield % α={a:.2f}"] = round(g * 100, 1)
            rows.append(row)

    if bench is not None:
        yb = bench.n_visible.values
        bench_subsets = [
            ("Benchmark: Clean tier", bench.tier == "clean"),
            ("Benchmark: Moderate tier", bench.tier == "moderate"),
            ("Benchmark: Heavy tier", bench.tier == "heavy"),
            ("Benchmark: All frames (n=195)", np.ones(len(bench), bool))
        ]
        for scorer, pre in [("Repeated sampling", "rep"), ("Perturbation ensemble", "pert")]:
            P = bench[[f"{pre}_p{i}" for i in LABELS_11]].values
            for name, mask in bench_subsets:
                k = int((P[mask, yb[mask]] == 0).sum())
                n = int(mask.sum())
                lo, hi = cp_ci(k, n)
                acc = float((bench[f"{pre}_majority"].values[mask] == yb[mask]).mean())
                row = {
                    "Scorer": scorer,
                    "Frame subset": name,
                    "n": n,
                    "e0": round(k / n, 3),
                    "e0 95% CI low": round(lo, 3),
                    "e0 95% CI high": round(hi, 3),
                    "Accuracy": round(acc, 3)
                }
                for a in (0.20, 0.30):
                    s, _cov, g = split_conformal(P[mask], yb[mask], a, n_splits=400, seed=0)
                    row[f"Set size α={a:.2f}"] = round(s, 2)
                    row[f"Yield % α={a:.2f}"] = round(g * 100, 1)
                rows.append(row)

    return pd.DataFrame(rows)


def table_2_sizing():
    """
    Table 2: Seed-sample size required for a reliable precheck decision.
    """
    rows = []
    for a in ALPHAS:
        for r in RATIOS:
            rows.append({
                "Target α": a,
                "True e0": round(a * r, 4),
                "e0 / α": r,
                "Minimum seed images (80% power)": min_seed(a, a * r),
                "Minimum n_cal (condition C1)": int(np.ceil(1 / a) - 1)
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="./data")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()

    pf_path = os.path.join(a.data, "a3_pilot_per_frame.csv")
    pf = pd.read_csv(pf_path)

    bench_path = os.path.join(a.data, "benchmark_195_per_frame.csv")
    bench = pd.read_csv(bench_path) if os.path.exists(bench_path) else None

    t1 = table_1_stratified(pf, bench)
    t2 = table_2_sizing()

    # Save to requested output directory
    for out_dir in [a.out, "submission/Paper_Tables", "submission/Tables", "Tables"]:
        if os.path.exists(out_dir):
            t1.to_excel(os.path.join(out_dir, "Table_1_stratified_precheck_results.xlsx"), index=False)
            t1.to_csv(os.path.join(out_dir, "Table_1_stratified_precheck_results.csv"), index=False)
            t2.to_excel(os.path.join(out_dir, "Table_2_seed_sample_size.xlsx"), index=False)
            t2.to_csv(os.path.join(out_dir, "Table_2_seed_sample_size.csv"), index=False)

    print("=== TABLE 1: STRATIFIED PRECHECK RESULTS ===")
    print(t1.to_string(index=False))
    print("\n=== TABLE 2: SEED SAMPLE SIZE ===")
    print(t2.to_string(index=False))
