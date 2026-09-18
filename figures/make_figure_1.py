"""Figure 1 - the precheck protocol schematic. Produces artwork only; no data input."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) or ".")
from figstyle_shim import apply_figure_style, META_GREY
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

apply_figure_style()
BLUE, ORANGE, GREY = "#3b6fb6", "#b4761f", "#4d4d4d"
fig, ax = plt.subplots(figsize=(7.4, 3.5))
ax.set_axis_off(); ax.set_xlim(0, 100); ax.set_ylim(0, 100)

def panel(x, y, w, h, fc, ec, lw=0.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.45,rounding_size=1.4",
                                fc=fc, ec=ec, lw=lw, zorder=2))

def arrow(x0, y0, x1, y1, col=GREY, lw=0.9):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=7,
                                 lw=lw, color=col, shrinkA=0, shrinkB=0, zorder=3))

W, H, Y, GAP = 21.0, 21.0, 74.0, 4.0
xs = [1.0 + i * (W + GAP) for i in range(4)]
steps = [("1  SEED", "generate or collect a\nlabeled seed sample,\nsized from Table 1", BLUE),
         ("2  QUERY", "query the annotator\nK times per image:\nrepeats or perturbed views", BLUE),
         ("3  MEASURE", "count images whose true\nlabel received zero votes\n$\\rightarrow\\ \\hat e_0$ and its exact 95% CI", BLUE),
         ("4  DECIDE", "evaluate the three\nconditions below at the\ntarget miscoverage $\\alpha$", ORANGE)]
for (hdr, txt, col), x in zip(steps, xs):
    panel(x, Y, W, H, "#fdf3e7" if col == ORANGE else "#eef2f8", col)
    ax.text(x + W/2, Y + H - 4.4, hdr, ha="center", va="center", fontsize=6.6, fontweight="bold", color=col, zorder=4)
    ax.text(x + W/2, Y + H/2 - 2.6, txt, ha="center", va="center", fontsize=6.1, linespacing=1.5, zorder=4)
for x in xs[:3]:
    arrow(x + W + 0.5, Y + H/2, x + W + GAP - 0.5, Y + H/2)

CX, CW, CY, CH = 1.0, 95.0, 33.0, 30.0
panel(CX, CY, CW, CH, "#f5f5f5", GREY)
ax.text(CX + CW/2, CY + CH + 3.6, "THE THREE FEASIBILITY CONDITIONS",
        ha="center", va="center", fontsize=6.6, fontweight="bold", color=GREY)
conds = [("C1", r"$n_{cal} \geq \lceil 1/\alpha \rceil - 1$",
          "below this floor every prediction set is the full\nlabel space, whatever the annotator does"),
         ("C2", r"$\hat e_0 \leq 1 - \lceil (n_{cal}{+}1)(1{-}\alpha) \rceil / n_{cal}$",
          "the exact finite-sample form of $\\hat e_0 < \\alpha$; if violated,\ncalibration is pinned at the trivial set"),
         ("C3", r"upper 95% bound of $\hat e_0$ also satisfies C2",
          "otherwise the seed sample is too small to\ndecide; enlarge it using Table 1")]
for i, (c, formula, why) in enumerate(conds):
    yy = CY + CH - 6.2 - i * 9.2
    ax.text(CX + 3.0, yy, c, fontsize=6.6, fontweight="bold", va="center", color=ORANGE, zorder=4)
    ax.text(CX + 7.5, yy, formula, fontsize=6.6, va="center", zorder=4)
    ax.text(CX + 51.0, yy, why, fontsize=6.0, va="center", color=GREY, linespacing=1.45, zorder=4)
arrow(xs[3] + W/2, Y - 0.5, xs[3] + W/2, CY + CH + 7.4, ORANGE)

OY, OH = 3.0, 21.0
gx, gw, nx, nw = 6.0, 38.0, 51.0, 43.0
panel(gx, OY, gw, OH, "#eaf3ec", "#2e7d32")
ax.text(gx + gw/2, OY + OH - 4.6, "ALL THREE PASS  \u2192  GO", ha="center", va="center",
        fontsize=6.6, fontweight="bold", color="#2e7d32", zorder=4)
ax.text(gx + gw/2, OY + OH/2 - 3.2, "run the full calibration set:\nprediction sets can be\ninformative at this $\\alpha$",
        ha="center", va="center", fontsize=6.1, linespacing=1.5, zorder=4)
panel(nx, OY, nw, OH, "#fdecea", "#b3261e")
ax.text(nx + nw/2, OY + OH - 4.6, "ANY ONE FAILS  \u2192  NO-GO", ha="center", va="center",
        fontsize=6.6, fontweight="bold", color="#b3261e", zorder=4)
ax.text(nx + nw/2, OY + OH/2 - 3.2, "improve the annotator, raise $\\alpha$, or enlarge\n$n_{cal}$ \u2014 do not commit the full annotation budget",
        ha="center", va="center", fontsize=6.1, linespacing=1.5, zorder=4)
arrow(gx + gw/2, CY - 0.5, gx + gw/2, OY + OH + 0.6)
arrow(nx + nw/2, CY - 0.5, nx + nw/2, OY + OH + 0.6)

fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
fig.savefig("Figure_1_protocol_schematic.png", dpi=300, bbox_inches="tight")
fig.savefig("Figure_1_protocol_schematic.pdf", bbox_inches="tight")
