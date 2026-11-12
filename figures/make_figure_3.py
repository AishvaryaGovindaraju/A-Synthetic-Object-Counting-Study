"""Figure 3 - Worked example on the synthetic counting task.
Produces: Figure_3_worked_example.png and .pdf
"""
import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__)) or "."
repo_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, script_dir)

from figstyle_shim import apply_figure_style, panel_letter, META_GREY
import matplotlib as mpl, matplotlib.pyplot as plt
import pandas as pd, numpy as np, json
from scipy import stats

data_dir = os.environ.get("PRECHECK_DATA") or os.path.join(repo_root, "data")
pf = pd.read_csv(os.path.join(data_dir, "a3_pilot_per_frame.csv"))
rv = pd.read_csv(os.path.join(data_dir, "a3_precheck_rule_validation.csv"))
summ = json.load(open(os.path.join(data_dir, "a3_precheck_summary.json")))

labels = np.arange(9)
yv = pf.n_visible.values
pf["gap"] = pf.n - pf.n_visible

def cp_ci(k, n, conf=0.95):
    a = (1 - conf) / 2
    lo = 0.0 if k == 0 else stats.beta.ppf(a, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a, k + 1, n - k)
    return lo, hi

def conformal(P, ytrue, alpha, n_splits=400, cal_frac=0.5, seed=0):
    rng = np.random.default_rng(seed)
    n = len(ytrue)
    ncal = max(2, int(round(cal_frac * n)))
    S, C, G = [], [], []
    for _ in range(n_splits):
        idx = rng.permutation(n)
        cal, test = idx[:ncal], idx[ncal:]
        if len(test) == 0:
            continue
        s = 1 - P[cal, ytrue[cal]]
        k = int(np.ceil((len(cal) + 1) * (1 - alpha)))
        qhat = 1.0 if k > len(cal) else np.sort(s)[k - 1]
        sets = (1 - P[test]) <= qhat
        S.append(sets.sum(1).mean())
        C.append(sets[np.arange(len(test)), ytrue[test]].mean())
        G.append((sets.sum(1) == 1).mean())
    return np.mean(S), np.mean(C), np.mean(G)

agrid = np.round(np.arange(0.02, 0.605, 0.02), 3)
rowsw = []
for s in ("rep", "pert"):
    P = pf[[f"{s}_p{i}" for i in labels]].values
    for sub, mask in [("all", np.ones(30, bool)), ("gap0", (pf.gap == 0).values), ("gap1", (pf.gap > 0).values)]:
        for a_ in agrid:
            ms, cov, sing = conformal(P[mask], yv[mask], a_, n_splits=400)
            rowsw.append(dict(scorer=s, subset=sub, alpha=a_, mean_set=ms, coverage=cov, yield_pct=sing * 100))
sweep = pd.DataFrame(rowsw)

apply_figure_style()
BLUE, RED = "#3b6fb6", "#c0392b"

f3 = plt.figure(figsize=(7.4, 2.6))
g3 = f3.add_gridspec(1, 3, wspace=0.52, left=0.075, right=0.985, bottom=0.25, top=0.76)

# (A) e0 with Clopper-Pearson CIs
ax1 = f3.add_subplot(g3[0])
order = [("Fully\nrendered", "gap0"), ("Under-\nrendered", "gap1"), ("All\nframes", "all")]
xs = np.arange(3)
for j, (s, col, dx) in enumerate([("rep", BLUE, -0.13), ("pert", RED, +0.13)]):
    P = pf[[f"{s}_p{i}" for i in labels]].values
    for i, (lab, sub) in enumerate(order):
        mask = {"all": np.ones(30, bool), "gap0": (pf.gap == 0).values, "gap1": (pf.gap > 0).values}[sub]
        k = int((P[mask, yv[mask]] == 0).sum())
        nn = int(mask.sum())
        p = k / nn
        lo, hi = cp_ci(k, nn)
        ax1.errorbar(i + dx, p, yerr=[[p - lo], [hi - p]], fmt="o", ms=4, color=col, lw=1.1, capsize=2.2)

ax1.axhline(0.20, color=META_GREY, ls="--", lw=0.9)
ax1.text(2.42, 0.22, r"$\alpha$=0.20", fontsize=5.8, ha="right", color=META_GREY)
ax1.set_xticks(xs)
ax1.set_xticklabels([l for l, _ in order])
ax1.set_xlim(-0.5, 2.5)
ax1.set_ylim(0, 0.75)
ax1.set_ylabel(r"unanimous-error rate $\hat e_0$")
ax1.set_xlabel("frame subset")
ax1.text(0.04, 0.93, "repeated sampling", transform=ax1.transAxes, color=BLUE, fontsize=5.4)
ax1.text(0.04, 0.86, "perturbation ensemble", transform=ax1.transAxes, color=RED, fontsize=5.4)
ax1.set_title("Under-rendered frames carry\nthe annotator's error rate", fontsize=8, pad=10)

# (B) Mean set size & (C) Yield pct
for pi, (metric, ylab, ttl) in enumerate([
    ("mean_set", "mean set size (of 9 labels)", "Sets are informative on frames\nthe generator rendered as intended"),
    ("yield_pct", "images with a single label (%)", "Usable auto-label yield recovers\nonly on rendered frames")
]):
    axx = f3.add_subplot(g3[pi + 1])
    for s, col in [("rep", BLUE), ("pert", RED)]:
        for sub, sty, lw in [("gap0", "-", 1.4), ("gap1", "--", 1.0)]:
            d = sweep[(sweep.scorer == s) & (sweep.subset == sub)].sort_values("alpha")
            axx.plot(d.alpha, d[metric], sty, color=col, lw=lw)
    axx.set_xlabel(r"target miscoverage $\alpha$")
    axx.set_ylabel(ylab)
    axx.set_xlim(0, 0.62)
    axx.set_title(ttl, fontsize=8, pad=10)
    if pi == 0:
        axx.axhline(8.1, color=META_GREY, ls=":", lw=0.8)
        axx.text(0.60, 8.3, "trivial", fontsize=5.8, ha="right", color=META_GREY)
        axx.set_ylim(0, 9.5)
        axx.set_yticks([0, 2, 4, 6, 8])
        axx.text(0.325, 5.7, "under-rendered\n(dashed, n=13)", fontsize=5.5, color="#4d4d4d")
        axx.text(0.04, 2.3, "fully rendered\n(solid, n=17)", fontsize=5.5, color="#4d4d4d")
    else:
        axx.set_ylim(-2, 100)

for i, ax in enumerate(f3.axes):
    panel_letter(ax, "ABC"[i], dx=-0.22, dy=1.12)

os.makedirs("figures", exist_ok=True)
os.makedirs("submission/Figures", exist_ok=True)
f3.savefig("figures/Figure_3_worked_example.png", dpi=300, bbox_inches="tight")
f3.savefig("figures/Figure_3_worked_example.pdf", bbox_inches="tight")
f3.savefig("submission/Figures/Figure_3_worked_example.png", dpi=300, bbox_inches="tight")
f3.savefig("submission/Figures/Figure_3_worked_example.pdf", bbox_inches="tight")

f3.canvas.draw()
rr = f3.canvas.get_renderer()
tx = [(t.get_text(), t.get_window_extent(rr)) for t in f3.findobj(mpl.text.Text) if t.get_text().strip() and t.get_visible()]
overlaps = [(x[0][:16], y[0][:16]) for i, x in enumerate(tx) for y in tx[i+1:] if x[1].overlaps(y[1])]
print("Figure 3 successfully generated! Overlaps:", overlaps)
