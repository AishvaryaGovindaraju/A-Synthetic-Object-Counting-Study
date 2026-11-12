"""Figure 1 - the precheck protocol schematic. Produces artwork only; no data input."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) or ".")
from figstyle_shim import apply_figure_style, META_GREY
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

apply_figure_style()
BLUE, ORANGE, GREY = "#3b6fb6", "#b4761f", "#4d4d4d"
fig, ax = plt.subplots(figsize=(7.4, 3.6))
ax.set_axis_off(); ax.set_xlim(0, 100); ax.set_ylim(0, 100)

def panel(x, y, w, h, fc, ec, lw=0.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.45,rounding_size=1.4",
                                fc=fc, ec=ec, lw=lw, zorder=2))

def arrow(x0, y0, x1, y1, col=GREY, lw=0.9):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=7,
                                 lw=lw, color=col, shrinkA=0, shrinkB=0, zorder=3))

# Top row: Steps 1, 2, 3, 4
W, H, Y, GAP = 21.0, 21.0, 74.0, 4.0
xs = [1.0 + i * (W + GAP) for i in range(4)]
steps = [("1  SEED & VERIFY", "generate seed sample;\nverify ground truth;\nsize from Table 2", BLUE),
         ("2  QUERY", "query annotator K times\nper image: repeats or\nperturbed views", BLUE),
         ("3  MEASURE", "count zero-vote images\n$\\rightarrow\\ \\hat e_0$ and exact\nClopper-Pearson 95% CI", BLUE),
         ("4  DECIDE", "evaluate feasibility\nconditions C1--C3 below\nat target miscoverage $\\alpha$", ORANGE)]
for (hdr, txt, col), x in zip(steps, xs):
    panel(x, Y, W, H, "#fdf3e7" if col == ORANGE else "#eef2f8", col)
    ax.text(x + W/2, Y + H - 4.4, hdr, ha="center", va="center", fontsize=6.4, fontweight="bold", color=col, zorder=4)
    ax.text(x + W/2, Y + H/2 - 2.6, txt, ha="center", va="center", fontsize=5.9, linespacing=1.45, zorder=4)
for x in xs[:3]:
    arrow(x + W + 0.5, Y + H/2, x + W + GAP - 0.5, Y + H/2)

# Middle box: Feasibility conditions C1, C2, C3
CX, CW, CY, CH = 1.0, 95.0, 32.5, 30.5
panel(CX, CY, CW, CH, "#f5f5f5", GREY)
ax.text(CX + CW/2, CY + CH + 3.6, "FEASIBILITY CONDITIONS (STEP 4 EVALUATION)",
        ha="center", va="center", fontsize=6.6, fontweight="bold", color=GREY)
conds = [("C1", r"$n_{cal} \geq \lceil 1/\alpha \rceil - 1$",
          "below this floor every prediction set is the full\nlabel space, whatever the annotator does"),
         ("C2", r"$\hat e_0 \leq 1 - \lceil (n_{cal}{+}1)(1{-}\alpha) \rceil / n_{cal}$",
          r"exact finite-sample form of $\hat e_0 < \alpha$; if violated," + "\ncalibration is pinned at the trivial full set"),
         ("C3", r"upper 95% bound of $\hat e_0$ also satisfies C2",
          "otherwise seed sample is too small to decide;\nenlarge seed size using Table 2")]
for i, (c, formula, why) in enumerate(conds):
    yy = CY + CH - 6.0 - i * 9.2
    ax.text(CX + 2.8, yy, c, fontsize=6.6, fontweight="bold", va="center", color=ORANGE, zorder=4)
    ax.text(CX + 7.5, yy, formula, fontsize=6.6, va="center", zorder=4)
    ax.text(CX + 51.0, yy, why, fontsize=5.9, va="center", color=GREY, linespacing=1.4, zorder=4)

arrow(xs[3] + W/2, Y - 0.5, xs[3] + W/2, CY + CH + 7.0, col=ORANGE)

# Bottom row: Decisions -> Step 5 or No-Go
OY, OH = 2.5, 21.0
gx, gw, nx, nw = 4.0, 42.0, 50.0, 46.0

# GO -> Step 5 CONFIRM
panel(gx, OY, gw, OH, "#eaf3ec", "#2e7d32")
ax.text(gx + gw/2, OY + OH - 4.4, "ALL THREE PASS  \u2192  GO (STEP 5: CONFIRM)", ha="center", va="center",
        fontsize=6.4, fontweight="bold", color="#2e7d32", zorder=4)
ax.text(gx + gw/2, OY + OH/2 - 2.8, "run split conformal calibration on full dataset;\nassess empirical coverage, set size, and yield;\nproceed with auto-annotation",
        ha="center", va="center", fontsize=5.8, linespacing=1.4, zorder=4)

# NO-GO
panel(nx, OY, nw, OH, "#fdecea", "#b3261e")
ax.text(nx + nw/2, OY + OH - 4.4, "ANY ONE FAILS  \u2192  NO-GO", ha="center", va="center",
        fontsize=6.4, fontweight="bold", color="#b3261e", zorder=4)
ax.text(nx + nw/2, OY + OH/2 - 2.8, "stop before annotating at scale; do not commit full budget;\nimprove annotator (prompt, model, ensemble), raise $\\alpha$,\nor enlarge seed sample / $n_{cal}$ using Table 2",
        ha="center", va="center", fontsize=5.8, linespacing=1.4, zorder=4)

arrow(gx + gw/2, CY - 0.5, gx + gw/2, OY + OH + 0.6, col="#2e7d32")
arrow(nx + nw/2, CY - 0.5, nx + nw/2, OY + OH + 0.6, col="#b3261e")

fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
os.makedirs("submission/Figures", exist_ok=True)
fig.savefig("figures/Figure_1_protocol_schematic.png", dpi=300, bbox_inches="tight")
fig.savefig("figures/Figure_1_protocol_schematic.pdf", bbox_inches="tight")
fig.savefig("submission/Figures/Figure_1_protocol_schematic.png", dpi=300, bbox_inches="tight")
fig.savefig("submission/Figures/Figure_1_protocol_schematic.pdf", bbox_inches="tight")
print("Figure 1 successfully generated!")
