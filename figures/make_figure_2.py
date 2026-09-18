import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) or '.')
from figstyle_shim import apply_figure_style, panel_letter, META_GREY
R = os.environ.get('PRECHECK_DATA', '../data') + '/'

import pandas as pd, numpy as np, json, re
import matplotlib as mpl, matplotlib.pyplot as plt
from scipy import stats


pf = pd.read_csv(R+"a3_pilot_per_frame.csv")
rv = pd.read_csv(R+"a3_precheck_rule_validation.csv")
summ = json.load(open(R+"a3_precheck_summary.json"))

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


def pred_trivial(alpha, e0, n_cal):
    k = int(np.ceil((n_cal+1)*(1-alpha)))
    if k > n_cal: return True
    return (e0*n_cal) > (n_cal - k)


def cp_ci(k, n, conf=0.95):
    a = (1-conf)/2
    lo = 0.0 if k==0 else stats.beta.ppf(a, k, n-k+1)
    hi = 1.0 if k==n else stats.beta.ppf(1-a, k+1, n-k)
    return lo, hi


def crit_k(n, alpha_t, sig=0.05):
    cdf = stats.binom.cdf(np.arange(n+1), n, alpha_t)
    ok = np.where(cdf <= sig)[0]
    return int(ok.max()) if len(ok) else -1


def min_seed(alpha_t, true_e0, power=0.80, nmax=4000):
    for n in range(5, nmax+1):
        kk = crit_k(n, alpha_t)
        if kk < 0: continue
        if stats.binom.cdf(kk, n, true_e0) >= power: return n
    return None


apply_figure_style()
BLUE, RED = "#3b6fb6", "#c0392b"
NCAL = 15

fig = plt.figure(figsize=(7.4, 2.5))
gs = fig.add_gridspec(1, 3, wspace=0.42, left=0.075, right=0.985, bottom=0.21, top=0.80)
# (a) condition 1 — calibration-size floor
axa = fig.add_subplot(gs[0])
aa = np.linspace(0.02, 0.60, 400); floor = np.ceil(1/aa) - 1
axa.plot(aa, floor, color="k", lw=1.4)
axa.fill_between(aa, 1, floor, color="#bdbdbd", alpha=0.35, lw=0)
axa.set_yscale("log"); axa.set_yticks([1,10,100]); axa.set_yticklabels(["1","10","100"])
axa.set_xlabel(r"target miscoverage $\alpha$"); axa.set_ylabel(r"calibration images $n_{cal}$")
axa.text(0.30, 2.2, "full label space\nreturned regardless\nof annotator", fontsize=6, ha="center", color="#4d4d4d")
axa.axhline(NCAL, color=META_GREY, ls=":", lw=0.9)
axa.annotate("this study, $n_{cal}$=15", xy=(0.30, NCAL), xytext=(0.20, 30), fontsize=6, color=META_GREY,
             arrowprops=dict(arrowstyle="-", lw=0.6, color=META_GREY))
axa.set_title("Condition 1: below this line, no\nprediction set can be informative", fontsize=8)
axa.set_xlim(0.0, 0.62); axa.set_ylim(1, 200)
# (b) condition 2 — exact boundary beats the asymptotic rule
axb = fig.add_subplot(gs[1])
for (nm, e0, mset, obs, col) in [("repeated sampling", 0.2333, rv.mean_set_repeat.values, rv.observed_trivial_repeat.values, BLUE),
                                 ("perturbation ensemble", 0.2000, rv.mean_set_perturb.values, rv.observed_trivial_perturb.values, RED)]:
    axb.plot(rv.alpha, mset, "-o", color=col, ms=2.6, lw=1.2)
    ex = np.array([pred_trivial(x, e0, NCAL) for x in rv.alpha]); b = rv.alpha[ex].values[-1] + 0.01
    axb.axvline(e0, color=col, ls=":", lw=1.0); axb.axvline(b, color=col, ls="-", lw=0.9, alpha=0.55)
axb.axhline(8.1, color=META_GREY, ls="--", lw=0.8)
axb.text(0.60, 8.3, "trivial", fontsize=6, ha="right", color=META_GREY)
axb.annotate(r"$\hat e_0$ (asymptotic)", xy=(0.20, 3.2), xytext=(0.015, 2.0), fontsize=6,
             arrowprops=dict(arrowstyle="-", lw=0.6))
axb.annotate("exact finite-$n$", xy=(0.31, 5.6), xytext=(0.345, 6.6), fontsize=6,
             arrowprops=dict(arrowstyle="-", lw=0.6))
axb.text(0.60, 1.0, "repeated sampling", color=BLUE, fontsize=6, ha="right")
axb.text(0.60, 0.1, "perturbation ensemble", color=RED, fontsize=6, ha="right")
axb.set_xlabel(r"target miscoverage $\alpha$"); axb.set_ylabel("mean set size (of 9 labels)")
axb.set_title("Condition 2: the exact boundary\ntracks collapse, 4 misses → 2", fontsize=8)
axb.set_xlim(0.0, 0.62); axb.set_ylim(0, 9.8)
# (c) condition 3 — seed size for a reliable GO decision
axc = fig.add_subplot(gs[2])
al = np.array([0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
for ratio, sty, lab in [(0.25, "-", "0.25"), (0.50, "--", "0.50"), (0.75, ":", "0.75")]:
    ns = [min_seed(x, x*ratio) for x in al]
    axc.plot(al, ns, sty, color="k", lw=1.3, marker="o", ms=2.6)
    axc.text(al[-1]+0.012, ns[-1], lab, fontsize=6, va="center")
axc.text(0.335, 320, r"$\hat e_0/\alpha$", fontsize=6)
axc.set_yscale("log"); axc.set_yticks([10,100,1000]); axc.set_yticklabels(["10","100","1k"])
axc.set_xlabel(r"target miscoverage $\alpha$"); axc.set_ylabel("seed images needed")
axc.axhline(30, color=META_GREY, ls=":", lw=0.9)
axc.annotate("this study, n=30", xy=(0.055, 30), xytext=(0.06, 11), fontsize=6, color=META_GREY)
axc.set_title("Condition 3: deciding the precheck\nnear the boundary is expensive", fontsize=8)
axc.set_xlim(0.03, 0.40); axc.set_ylim(8, 3000)
for i, ax in enumerate(fig.axes): panel_letter(ax, "ABC"[i])

for t in axa.texts:
    if t.get_text().startswith("full label space"):
        t.set_text("full label space regardless\nof how good the annotator is"); t.set_position((0.36, 1.18)); t.set_fontsize(6)

fig.savefig("Figure_2_feasibility_conditions.png", dpi=300, bbox_inches="tight")