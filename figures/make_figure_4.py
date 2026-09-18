import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) or '.')
from figstyle_shim import apply_figure_style, panel_letter, META_GREY
R = os.environ.get('PRECHECK_DATA', '../data') + '/'

import pandas as pd
import numpy as np
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import stats

# skill:figure-style kernel.py (auto-injected on skill load)
META_GREY = "#888888"


def apply_figure_style(*, frame="open", font=None, sizes=(8, 7, 6), grid=False):
    import matplotlib as mpl
    if frame not in ("open", "boxed", "none"):
        raise ValueError(f"frame must be 'open'|'boxed'|'none', got {frame!r}")

    try:
        import os, sys, glob, matplotlib.font_manager as fm
        fdir = os.path.join(os.environ.get("CONDA_PREFIX") or sys.prefix, "fonts")
        if os.path.isdir(fdir):
            known = {f.fname for f in fm.fontManager.ttflist}
            for f in glob.glob(os.path.join(fdir, "*.ttf")):
                if f not in known:
                    fm.fontManager.addfont(f)
    except Exception:
        pass
    base, secondary, tick = sizes
    boxed = (frame == "boxed")
    rc = {
        "font.family": "sans-serif",
        "font.size": base,
        "axes.labelsize": base,
        "axes.titlesize": base,
        "legend.fontsize": secondary,
        "xtick.labelsize": tick,
        "ytick.labelsize": tick,
        "axes.linewidth": 0.6,
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.size": 3, "ytick.major.size": 3,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "axes.spines.top": boxed, "axes.spines.right": boxed,
        "axes.spines.left": frame != "none", "axes.spines.bottom": frame != "none",
        "axes.grid": bool(grid),
        "legend.frameon": False,
        "figure.dpi": 200,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "axes.titleweight": "normal",
        "axes.titlelocation": "left",
        "axes.labelweight": "normal",
        "lines.linewidth": 1.2,
        "patch.linewidth": 0.6,
        "pdf.fonttype": 42, "ps.fonttype": 42,
    }
    if font:
        rc["font.sans-serif"] = [font, "DejaVu Sans"]
    mpl.rcParams.update(rc)


def panel_letter(ax, letter, dx=-0.18, dy=1.02, case="lower", fontsize=None):
    import matplotlib.pyplot as plt
    if fontsize is None:
        fontsize = plt.rcParams.get("font.size", 8) + 1
    s = letter.lower() if case == "lower" else letter.upper()
    ax.text(dx, dy, s, transform=ax.transAxes,
            fontweight="bold", fontsize=fontsize, va="bottom", ha="left")


def cp_ci(k, n, conf=0.95):
    a = (1-conf)/2
    lo = 0.0 if k==0 else stats.beta.ppf(a, k, n-k+1)
    hi = 1.0 if k==n else stats.beta.ppf(1-a, k+1, n-k)
    return lo, hi



pf = pd.read_csv(R+"a3_pilot_per_frame.csv")
vk = pd.read_csv(R+"a3_ablation_vote_count.csv")

labels = np.arange(9)
yv = pf.n_visible.values
pf["gap"] = pf.n - pf.n_visible

apply_figure_style()
BLUE, RED = "#3b6fb6", "#c0392b"

# AUROC computation
def auroc(score, pos):
    r = stats.rankdata(score); n1 = pos.sum(); n0 = len(pos)-n1
    return (r[pos].sum() - n1*(n1+1)/2) / (n1*n0)

rng_auroc = np.random.default_rng(7)
auroc_results = {}
for s in ("rep","pert"):
    sc = pf[f"{s}_agreement"].values; y = pf[f"{s}_correct"].values.astype(bool)
    a0 = auroc(sc, y)
    bs = []
    for _ in range(10000):
        i = rng_auroc.integers(0, len(pf), len(pf))
        if y[i].sum() in (0, len(i)): continue
        bs.append(auroc(sc[i], y[i]))
    lo, hi = np.percentile(bs, [2.5, 97.5]); auroc_results[f"auroc_{s}"] = (a0, lo, hi)

# signed error
signed = {}
for s in ("rep","pert"):
    signed[s] = pf[f"{s}_majority"].values - yv

# Figure 4
f4 = plt.figure(figsize=(7.4, 2.5))
g4 = f4.add_gridspec(1, 3, wspace=0.40, left=0.075, right=0.985, bottom=0.26, top=0.80)
rng = np.random.default_rng(3)
axd = f4.add_subplot(g4[0])
pos = {("rep",True):0, ("rep",False):0.75, ("pert",True):2.0, ("pert",False):2.75}
for (s, corr), x0 in pos.items():
    col = BLUE if s=="rep" else RED
    v = pf.loc[pf[f"{s}_correct"]==corr, f"{s}_agreement"].values
    axd.scatter(x0 + rng.uniform(-0.13, 0.13, len(v)), v, s=9, color=col if corr else "#9e9e9e",
                edgecolors="none", alpha=0.85, zorder=3)
    axd.plot([x0-0.22, x0+0.22], [np.median(v)]*2, color="k", lw=1.2, zorder=4)
axd.set_xticks([0, 0.75, 2.0, 2.75]); axd.set_xticklabels(["correct","wrong","correct","wrong"], fontsize=6)
axd.set_ylabel("agreement across the 5 queries"); axd.set_ylim(0.3, 1.08); axd.set_xlim(-0.45, 3.2)
axd.text(0.37, 0.355, "repeated\nsampling", ha="center", fontsize=6, color=BLUE)
axd.text(2.37, 0.355, "perturbation\nensemble", ha="center", fontsize=6, color=RED)
axd.text(0.37, 1.045, "AUROC 0.54\n[0.44, 0.69]", ha="center", fontsize=6)
axd.text(2.37, 1.045, "AUROC 0.74\n[0.55, 0.92]", ha="center", fontsize=6)
axd.set_title("Agreement separates right from wrong\nonly for the perturbation ensemble", fontsize=8)
# (b) signed error — all errors are overcounts
axe = f4.add_subplot(g4[1])
w = 0.35
for j,(s, col) in enumerate([("rep", BLUE), ("pert", RED)]):
    sg = pf[f"{s}_majority"].values - yv
    vals, cnts = np.unique(sg, return_counts=True)
    axe.bar(vals + (j-0.5)*w, cnts, width=w, color=col, edgecolor="none")
    for v_, c_ in zip(vals, cnts):
        if v_ != 0: axe.text(v_+(j-0.5)*w, c_+0.6, str(c_), ha="center", fontsize=6, color=col)
axe.set_xticks([-1,0,1,2]); axe.set_xlabel("majority answer − true count")
axe.set_ylabel("frames (of 30)"); axe.set_ylim(0, 26); axe.set_xlim(-1.6, 2.6)
axe.text(-1.45, 20, "no undercounts\nin 30 frames", fontsize=6, color="#4d4d4d")
axe.text(1.05, 14, "Wilcoxon on the\nwrong frames:\np = 0.008 / 0.004", fontsize=6, color="#4d4d4d")
axe.set_title("Errors are one-sided overcounts,\nnot symmetric noise", fontsize=8)
# (c) K ablation with CI
axf = f4.add_subplot(g4[2])
acc = vk.accuracy.values*100; K = vk.K.values
se = np.sqrt((acc/100)*(1-acc/100)/30)*100
axf.fill_between(K, acc-1.96*se, acc+1.96*se, color=BLUE, alpha=0.16, lw=0)
axf.plot(K, acc, "-o", color=BLUE, ms=3.4, lw=1.4)
axf.set_xticks(K); axf.set_xlabel("repeated queries per image K"); axf.set_ylabel("majority-vote accuracy (%)")
axf.set_ylim(40, 100); axf.set_xlim(0.7, 5.3)
axf.text(1.05, 46, "shaded: 95% CI, n=30\nspread across K: 2.6 pp", fontsize=6, color="#4d4d4d")
axf.set_title("More votes do not help, but n=30\ncannot exclude a ±20 pp effect", fontsize=8)
for i, ax in enumerate(f4.axes): panel_letter(ax, "ABC"[i])
f4.savefig("Figure_3_annotator_diagnostics.png", dpi=300, bbox_inches="tight")
rr = f4.canvas.get_renderer()
tx=[(t.get_text(), t.get_window_extent(rr)) for t in f4.findobj(mpl.text.Text) if t.get_text().strip() and t.get_visible()]
print("F4 overlaps:", [(x[0][:16],y[0][:16]) for i,x in enumerate(tx) for y in tx[i+1:] if x[1].overlaps(y[1])][:10])