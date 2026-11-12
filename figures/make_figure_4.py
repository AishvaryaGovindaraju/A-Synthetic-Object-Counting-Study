"""Figure 4 - The three feasibility conditions.
Produces: Figure_4_feasibility_conditions.png and .pdf
"""
import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__)) or "."
repo_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, script_dir)

from figstyle_shim import apply_figure_style, panel_letter, META_GREY
import pandas as pd, numpy as np, json
import matplotlib as mpl, matplotlib.pyplot as plt
from scipy import stats

data_dir = os.environ.get("PRECHECK_DATA") or os.path.join(repo_root, "data")
pf = pd.read_csv(os.path.join(data_dir, "a3_pilot_per_frame.csv"))
rv = pd.read_csv(os.path.join(data_dir, "a3_precheck_rule_validation.csv"))
summ = json.load(open(os.path.join(data_dir, "a3_precheck_summary.json")))

def pred_trivial(alpha, e0, n_cal):
    k = int(np.ceil((n_cal + 1) * (1 - alpha)))
    if k > n_cal:
        return True
    return (e0 * n_cal) > (n_cal - k)

def crit_k(n, alpha_t, sig=0.05):
    cdf = stats.binom.cdf(np.arange(n + 1), n, alpha_t)
    ok = np.where(cdf <= sig)[0]
    return int(ok.max()) if len(ok) else -1

def min_seed(alpha_t, true_e0, power=0.80, nmax=4000):
    for n in range(5, nmax + 1):
        kk = crit_k(n, alpha_t)
        if kk < 0:
            continue
        if stats.binom.cdf(kk, n, true_e0) >= power:
            return n
    return None

apply_figure_style()
BLUE, RED = "#3b6fb6", "#c0392b"
NCAL = 15  # 50/50 split of the 30-frame seed sample

fig = plt.figure(figsize=(7.4, 2.6))
gs = fig.add_gridspec(1, 3, wspace=0.60, left=0.075, right=0.985, bottom=0.25, top=0.76)

# (A) Condition 1 — Calibration-size floor
axa = fig.add_subplot(gs[0])
aa = np.linspace(0.02, 0.60, 400)
floor = np.ceil(1 / aa) - 1
axa.plot(aa, floor, color="k", lw=1.4)
axa.fill_between(aa, 1, floor, color="#bdbdbd", alpha=0.35, lw=0)
axa.set_yscale("log")
axa.set_yticks([1, 10, 100])
axa.set_yticklabels(["1", "10", "100"])
axa.set_xlabel(r"target miscoverage $\alpha$")
axa.set_ylabel(r"calibration images $n_{cal}$")
axa.text(0.16, 1.8, "full label space\nregardless of\nannotator quality",
         fontsize=5.0, ha="center", color="#4d4d4d")
axa.axhline(NCAL, color=META_GREY, ls=":", lw=0.9)
axa.annotate(r"this study, $n_{cal}$=15", xy=(0.18, NCAL), xytext=(0.04, 30), fontsize=5.5, color=META_GREY,
             arrowprops=dict(arrowstyle="-", lw=0.6, color=META_GREY))
axa.set_title("Condition 1: below this line, no\nprediction set can be informative", fontsize=8, pad=10)
axa.set_xlim(0.0, 0.62)
axa.set_ylim(1, 200)

# (B) Condition 2 — Exact finite-sample boundary vs asymptotic rule
axb = fig.add_subplot(gs[1])
for (nm, e0, mset, obs, col) in [
    ("repeated sampling", 0.2333, rv.mean_set_repeat.values, rv.observed_trivial_repeat.values, BLUE),
    ("perturbation ensemble", 0.2000, rv.mean_set_perturb.values, rv.observed_trivial_perturb.values, RED)
]:
    axb.plot(rv.alpha, mset, "-o", color=col, ms=2.6, lw=1.2)
    ex = np.array([pred_trivial(x, e0, NCAL) for x in rv.alpha])
    b = rv.alpha[ex].values[-1] + 0.01
    axb.axvline(e0, color=col, ls=":", lw=1.0)
    axb.axvline(b, color=col, ls="-", lw=0.9, alpha=0.55)

axb.axhline(8.1, color=META_GREY, ls="--", lw=0.8)
axb.text(0.60, 8.3, "trivial", fontsize=5.8, ha="right", color=META_GREY)
axb.annotate(r"$\hat e_0$ (asymptotic)", xy=(0.20, 3.2), xytext=(0.02, 2.0), fontsize=5.8,
             arrowprops=dict(arrowstyle="-", lw=0.6))
axb.annotate(r"exact ($n_{cal}$=15)", xy=(0.31, 5.6), xytext=(0.32, 6.6), fontsize=5.8,
             arrowprops=dict(arrowstyle="-", lw=0.6))
axb.text(0.60, 1.4, "repeated sampling", color=BLUE, fontsize=5.5, ha="right")
axb.text(0.60, 0.5, "perturbation ensemble", color=RED, fontsize=5.5, ha="right")
axb.set_xlabel(r"target miscoverage $\alpha$")
axb.set_ylabel("mean set size (of 9 labels)")
axb.set_yticks([0, 2, 4, 6, 8])
axb.set_title("Condition 2: exact boundary tracks\ncollapse, 4 misses \u2192 2", fontsize=8, pad=10)
axb.set_xlim(0.0, 0.62)
axb.set_ylim(0, 9.5)

# (C) Condition 3 — Seed size for a reliable GO decision
axc = fig.add_subplot(gs[2])
al = np.array([0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
for ratio, sty, lab in [(0.25, "-", "0.25"), (0.50, "--", "0.50"), (0.75, ":", "0.75")]:
    ns = [min_seed(x, x * ratio) for x in al]
    axc.plot(al, ns, sty, color="k", lw=1.3, marker="o", ms=2.6)
    axc.text(al[-1] + 0.012, ns[-1], lab, fontsize=5.8, va="center")

axc.text(0.335, 320, r"$\hat e_0/\alpha$", fontsize=5.8)
axc.set_yscale("log")
axc.set_yticks([10, 100, 1000])
axc.set_yticklabels(["10", "100", "1k"])
axc.set_xlabel(r"target miscoverage $\alpha$")
axc.set_ylabel("seed images needed")
axc.axhline(30, color=META_GREY, ls=":", lw=0.9)
axc.annotate("this study, n=30", xy=(0.055, 30), xytext=(0.06, 11), fontsize=5.8, color=META_GREY)
axc.set_title("Condition 3: deciding precheck\nnear boundary is expensive", fontsize=8, pad=10)
axc.set_xlim(0.03, 0.40)
axc.set_ylim(8, 3000)

for i, ax in enumerate(fig.axes):
    panel_letter(ax, "ABC"[i], dx=-0.22, dy=1.12)

os.makedirs("figures", exist_ok=True)
os.makedirs("submission/Figures", exist_ok=True)
fig.savefig("figures/Figure_4_feasibility_conditions.png", dpi=300, bbox_inches="tight")
fig.savefig("figures/Figure_4_feasibility_conditions.pdf", bbox_inches="tight")
fig.savefig("submission/Figures/Figure_4_feasibility_conditions.png", dpi=300, bbox_inches="tight")
fig.savefig("submission/Figures/Figure_4_feasibility_conditions.pdf", bbox_inches="tight")

fig.canvas.draw()
rr = fig.canvas.get_renderer()
tx = [(t.get_text(), t.get_window_extent(rr)) for t in fig.findobj(mpl.text.Text) if t.get_text().strip() and t.get_visible()]
overlaps = [(x[0][:16], y[0][:16]) for i, x in enumerate(tx) for y in tx[i+1:] if x[1].overlaps(y[1])]
print("Figure 4 successfully generated! Overlaps:", overlaps)
