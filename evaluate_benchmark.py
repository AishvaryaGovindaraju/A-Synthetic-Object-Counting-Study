import pandas as pd, numpy as np
from precheck import precheck, split_conformal, cp_ci

df = pd.read_csv('data/benchmark_195_per_frame.csv')
y_true = df.n_visible.values

print('=== CONFORMAL PRECHECK EVALUATION ON 195 BENCHMARK FRAMES ===\n')

for scorer, pre in [('Repeated sampling', 'rep'), ('Perturbation ensemble', 'pert')]:
    P = df[[f'{pre}_p{i}' for i in range(11)]].values
    print(f'--- {scorer.upper()} ---')
    for a in [0.05, 0.10, 0.20, 0.30]:
        res = precheck(P, y_true, alpha=a)
        lo, hi = res['e0_ci']
        dec = res['decision']
        c1, c2, c3 = res['C1_size_floor'], res['C2_unanimous_error'], res['C3_decision_power']
        e0 = res['e0']
        s, cov, yld = split_conformal(P, y_true, alpha=a, n_splits=400)
        print(f"alpha={a:.2f}: {dec:<5} | e0={e0:.3f} [{lo:.3f}, {hi:.3f}] | C1={c1} C2={c2} C3={c3} | Set Size={s:.2f}, Yield={yld*100:.1f}%, Cov={cov*100:.1f}%")
    print()
