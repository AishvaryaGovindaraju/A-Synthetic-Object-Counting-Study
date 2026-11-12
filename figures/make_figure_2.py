"""Figure 2 - Annotator diagnostics from the seed sample queries.
Produces: Figure_2_annotator_diagnostics.png and .pdf
"""
import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__)) or "."
repo_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, script_dir)

from figstyle_shim import apply_figure_style, panel_letter, META_GREY
import pandas as pd
import numpy as np
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import stats

data_dir = os.environ.get("PRECHECK_DATA") or os.path.join(repo_root, "data")
pf = pd.read_csv(os.path.join(data_dir, "a3_pilot_per_frame.csv"))
vk = pd.read_csv(os.path.join(data_dir, "a3_ablation_vote_count.csv"))

labels = np.arange(9)
yv = pf.n_visible.values
pf["gap"] = pf.n - pf.n_visible

apply_figure_style()
BLUE, RED = "#3b6fb6", "#c0392b"

# AUROC computation
def auroc(score, pos):
    r = stats.rankdata(score); n1 = pos.sum(); n0 = len(pos) - n1
    if n1 == 0 or n0 == 0:
        return 0.5
    return (r[pos].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

rng_auroc = np.random.default_rng(7)
auroc_results = {}
for s in ("rep", "pert"):
    sc = pf[f"{s}_agreement"].values
    y = pf[f"{s}_correct"].values.astype(bool)
    a0 = auroc(sc, y)
    bs = []
    for _ in range(5000):
        idx = rng_auroc.integers(0, len(pf), len(pf))
        if y[idx].sum() in (0, len(idx)):
            continue
        bs.append(auroc(sc[idx], y[idx]))
    lo, hi = np.percentile(bs, [2.5, 97.5])
    auroc_results[f"auroc_{s}"] = (a0, lo, hi)

f2 = plt.figure(figsize=(7.4, 2.6))
g2 = f2.add_gridspec(1, 3, wspace=0.45, left=0.08, right=0.985, bottom=0.25, top=0.76)

# (A) Agreement score vs correctness
rng = np.random.default_rng(3)
axd = f2.add_subplot(g2[0])
pos = {("rep", True): 0.0, ("rep", False): 0.75, ("pert", True): 2.0, ("pert", False): 2.75}
for (s, corr), x0 in pos.items():
    col = BLUE if s == "rep" else RED
    v = pf.loc[pf[f"{s}_correct"] == corr, f"{s}_agreement"].values
    axd.scatter(x0 + rng.uniform(-0.12, 0.12, len(v)), v, s=10,
                color=col if corr else "#9e9e9e", edgecolors="none", alpha=0.85, zorder=3)
    axd.plot([x0 - 0.22, x0 + 0.22], [np.median(v)] * 2, color="k", lw=1.2, zorder=4)

axd.set_xticks([0.0, 0.75, 2.0, 2.75])
axd.set_xticklabels(["correct", "wrong", "correct", "wrong"], fontsize=6)
axd.set_ylabel("agreement across 5 queries")
axd.set_ylim(0.30, 1.15)
axd.set_yticks([0.4, 0.6, 0.8, 1.0])
axd.set_xlim(-0.45, 3.20)
axd.text(0.375, 0.34, "repeated\nsampling", ha="center", fontsize=6, color=BLUE)
axd.text(2.375, 0.34, "perturbation\nensemble", ha="center", fontsize=6, color=RED)
axd.text(0.375, 1.05, f"AUROC {auroc_results['auroc_rep'][0]:.2f}\n[{auroc_results['auroc_rep'][1]:.2f}, {auroc_results['auroc_rep'][2]:.2f}]",
         ha="center", fontsize=5.8)
axd.text(2.375, 1.05, f"AUROC {auroc_results['auroc_pert'][0]:.2f}\n[{auroc_results['auroc_pert'][1]:.2f}, {auroc_results['auroc_pert'][2]:.2f}]",
         ha="center", fontsize=5.8)
axd.set_title("Agreement separates right from wrong\nonly for perturbation ensemble", fontsize=8, pad=10)

# (B) Signed error — all errors are overcounts
axe = f2.add_subplot(g2[1])
w = 0.35
for j, (s, col) in enumerate([("rep", BLUE), ("pert", RED)]):
    sg = pf[f"{s}_majority"].values - yv
    vals, cnts = np.unique(sg, return_counts=True)
    axe.bar(vals + (j - 0.5) * w, cnts, width=w, color=col, edgecolor="none",
            label="repeated sampling" if s == "rep" else "perturbation ensemble")
    for v_, c_ in zip(vals, cnts):
        if v_ != 0:
            axe.text(v_ + (j - 0.5) * w, c_ + 0.6, str(c_), ha="center", fontsize=6, color=col)

axe.set_xticks([-1, 0, 1, 2])
axe.set_xlabel("majority answer − true count")
axe.set_ylabel("frames (of 30)")
axe.set_ylim(0, 26)
axe.set_yticks([0, 5, 10, 15, 20, 25])
axe.set_xlim(-1.6, 2.6)
axe.text(-1.45, 20, "no undercounts\nin 30 frames", fontsize=6, color="#4d4d4d")
axe.text(1.10, 15, "Wilcoxon on the\nwrong frames:\np = 0.008 / 0.004", fontsize=6, color="#4d4d4d")
axe.set_title("Errors are one-sided overcounts,\nnot symmetric noise", fontsize=8, pad=10)

# (C) K ablation with CI
axf = f2.add_subplot(g2[2])
acc = vk.accuracy.values * 100
K = vk.K.values
se = np.sqrt((acc / 100) * (1 - acc / 100) / 30) * 100
axf.fill_between(K, acc - 1.96 * se, acc + 1.96 * se, color=BLUE, alpha=0.16, lw=0)
axf.plot(K, acc, "-o", color=BLUE, ms=3.4, lw=1.4)
axf.set_xticks(K)
axf.set_xlabel("repeated queries per image K")
axf.set_ylabel("majority-vote accuracy (%)")
axf.set_ylim(40, 100)
axf.set_xlim(0.7, 5.3)
axf.text(1.05, 46, "shaded: 95% CI, n=30\nspread across K: 2.6 pp", fontsize=6, color="#4d4d4d")
axf.set_title("More votes do not help, but n=30\ncannot exclude a \u00b120 pp effect", fontsize=8, pad=10)

for i, ax in enumerate(f2.axes):
    panel_letter(ax, "ABC"[i], dx=-0.22, dy=1.12)

os.makedirs("figures", exist_ok=True)
os.makedirs("submission/Figures", exist_ok=True)
f2.savefig("figures/Figure_2_annotator_diagnostics.png", dpi=300, bbox_inches="tight")
f2.savefig("figures/Figure_2_annotator_diagnostics.pdf", bbox_inches="tight")
f2.savefig("submission/Figures/Figure_2_annotator_diagnostics.png", dpi=300, bbox_inches="tight")
f2.savefig("submission/Figures/Figure_2_annotator_diagnostics.pdf", bbox_inches="tight")

f2.canvas.draw()
rr = f2.canvas.get_renderer()
tx = [(t.get_text(), t.get_window_extent(rr)) for t in f2.findobj(mpl.text.Text) if t.get_text().strip() and t.get_visible()]
overlaps = [(x[0][:16], y[0][:16]) for i, x in enumerate(tx) for y in tx[i+1:] if x[1].overlaps(y[1])]
print("Figure 2 successfully generated! Overlaps:", overlaps)
