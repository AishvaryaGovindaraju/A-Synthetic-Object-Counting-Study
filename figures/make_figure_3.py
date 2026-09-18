import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) or '.')
from figstyle_shim import apply_figure_style, panel_letter, META_GREY
R = os.environ.get('PRECHECK_DATA', '../data') + '/'

import matplotlib as mpl, matplotlib.pyplot as plt
import pandas as pd, numpy as np, json

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



pf = pd.read_csv(R+"a3_pilot_per_frame.csv")
rv = pd.read_csv(R+"a3_precheck_rule_validation.csv")
summ = json.load(open(R+"a3_precheck_summary.json"))

labels = np.arange(9)
yv = pf.n_visible.values
pf["gap"] = pf.n - pf.n_visible

def cp_ci(k, n, conf=0.95):
    from scipy import stats
    a = (1-conf)/2
    lo = 0.0 if k==0 else stats.beta.ppf(a, k, n-k+1)
    hi = 1.0 if k==n else stats.beta.ppf(1-a, k+1, n-k)
    return lo, hi

def conformal(P, ytrue, alpha, n_splits=400, cal_frac=0.5, seed=0):
    rng = np.random.default_rng(seed); n = len(ytrue); ncal = max(2, int(round(cal_frac*n)))
    S, C, G = [], [], []
    for _ in range(n_splits):
        idx = rng.permutation(n); cal, test = idx[:ncal], idx[ncal:]
        if len(test) == 0: continue
        s = 1 - P[cal, ytrue[cal]]
        k = int(np.ceil((len(cal)+1)*(1-alpha)))
        qhat = 1.0 if k > len(cal) else np.sort(s)[k-1]
        sets = (1 - P[test]) <= qhat
        S.append(sets.sum(1).mean()); C.append(sets[np.arange(len(test)), ytrue[test]].mean()); G.append((sets.sum(1)==1).mean())
    return np.mean(S), np.mean(C), np.mean(G)

agrid = np.round(np.arange(0.02, 0.605, 0.02), 3)
rowsw = []
for s in ("rep","pert"):
    P = pf[[f"{s}_p{i}" for i in labels]].values
    for sub, mask in [("all", np.ones(30,bool)), ("gap0", (pf.gap==0).values), ("gap1", (pf.gap>0).values)]:
        for a_ in agrid:
            ms, cov, sing = conformal(P[mask], yv[mask], a_, n_splits=400)
            rowsw.append(dict(scorer=s, subset=sub, alpha=a_, mean_set=ms, coverage=cov, yield_pct=sing*100))
sweep = pd.DataFrame(rowsw)

out = []
for s in ("rep","pert"):
    P = pf[[f"{s}_p{i}" for i in labels]].values
    for subset, mask in [("all 30 frames", np.ones(30, bool)), ("gap=0 (n=17)", (pf.gap==0).values), ("gap>0 (n=13)", (pf.gap>0).values)]:
        e0 = float((P[mask, yv[mask]] == 0).mean()); k = int((P[mask, yv[mask]] == 0).sum()); nn = int(mask.sum())
        lo, hi = cp_ci(k, nn)
        row = dict(scorer=s, subset=subset, n=nn, e0=round(e0,3), e0_lo=round(lo,3), e0_hi=round(hi,3),
                   acc=round(float((pf[f"{s}_majority"].values[mask]==yv[mask]).mean()),3))
        for a in (0.10, 0.20, 0.30):
            ms, cov, sing = conformal(P[mask], yv[mask], a)
            row[f"set@{a:.2f}"] = round(ms,2); row[f"yield@{a:.2f}"] = round(sing*100,1)
        out.append(row)
strat = pd.DataFrame(out)

apply_figure_style()
BLUE, RED = "#3b6fb6", "#c0392b"

f3 = plt.figure(figsize=(7.4, 2.6))
g3 = f3.add_gridspec(1, 3, wspace=0.40, left=0.075, right=0.985, bottom=0.30, top=0.80)
# (a) e0 with Clopper-Pearson CIs
ax1 = f3.add_subplot(g3[0])
order = [("Fully\nrendered", "gap0"), ("Under-\nrendered", "gap1"), ("All\nframes", "all")]
xs = np.arange(3)
for j,(s, col, dx) in enumerate([("rep", BLUE, -0.13), ("pert", RED, +0.13)]):
    P = pf[[f"{s}_p{i}" for i in labels]].values
    for i,(lab, sub) in enumerate(order):
        mask = {"all": np.ones(30,bool), "gap0": (pf.gap==0).values, "gap1": (pf.gap>0).values}[sub]
        k = int((P[mask, yv[mask]]==0).sum()); nn = int(mask.sum()); p = k/nn; lo, hi = cp_ci(k, nn)
        ax1.errorbar(i+dx, p, yerr=[[p-lo],[hi-p]], fmt="o", ms=4, color=col, lw=1.1, capsize=2.2)
ax1.axhline(0.20, color=META_GREY, ls="--", lw=0.9)
ax1.text(2.42, 0.215, r"$\alpha$=0.20", fontsize=6, ha="right", color=META_GREY)
ax1.set_xticks(xs); ax1.set_xticklabels([l for l,_ in order]); ax1.set_xlim(-0.5, 2.5); ax1.set_ylim(0, 0.75)
ax1.set_ylabel(r"unanimous-error rate $\hat e_0$")
ax1.text(-0.42, 0.70, "repeated sampling", color=BLUE, fontsize=6)
ax1.text(-0.42, 0.645, "perturbation ensemble", color=RED, fontsize=6)
ax1.set_title("Under-rendered frames carry\nthe annotator's error rate", fontsize=8)
# (b) set size and (c) yield vs alpha by subset
for pi,(metric, ylab, ttl) in enumerate([("mean_set", "mean set size (of 9 labels)", "Sets are informative on frames\nthe generator rendered as intended"),
                                          ("yield_pct", "images with a single label (%)", "Usable auto-label yield recovers\nonly on rendered frames")]):
    axx = f3.add_subplot(g3[pi+1])
    for s, col in [("rep", BLUE), ("pert", RED)]:
        for sub, sty, lw in [("gap0","-",1.4), ("gap1","--",1.0)]:
            d = sweep[(sweep.scorer==s)&(sweep.subset==sub)].sort_values("alpha")
            axx.plot(d.alpha, d[metric], sty, color=col, lw=lw)
    axx.set_xlabel(r"target miscoverage $\alpha$"); axx.set_ylabel(ylab); axx.set_xlim(0, 0.62)
    axx.set_title(ttl, fontsize=8)
    if pi==0:
        axx.axhline(8.1, color=META_GREY, ls=":", lw=0.8); axx.text(0.60, 8.3, "trivial", fontsize=6, ha="right", color=META_GREY)
        axx.set_ylim(0, 9.8)
        axx.text(0.315, 7.3, "under-rendered\n(dashed, n=13)", fontsize=6, color="#4d4d4d")
        axx.text(0.34, 2.1, "fully rendered\n(solid, n=17)", fontsize=6, color="#4d4d4d")
    else:
        axx.set_ylim(-2, 100)
ax1.set_xlabel("frame subset")
for i, ax in enumerate(f3.axes): panel_letter(ax, "ABC"[i])
f3.savefig("Figure_4_worked_example.png", dpi=300, bbox_inches="tight")

axb3 = f3.axes[1]
for t in list(axb3.texts):
    s0 = t.get_text()
    if s0.startswith("under-rendered"): t.set_position((0.325, 5.7))
    elif s0.startswith("fully rendered"): t.set_position((0.03, 2.3))
    elif s0 == "trivial": t.set_position((0.60, 7.4))
for t in list(f3.axes[0].texts):
    if t.get_text().startswith(r"$\alpha$"): t.set_position((-0.45, 0.225)); t.set_ha("left")
f3.savefig("Figure_4_worked_example.png", dpi=300, bbox_inches="tight")