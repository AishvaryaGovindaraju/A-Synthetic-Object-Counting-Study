"""Minimal stand-ins for the plotting helpers used when these figures were produced."""
import matplotlib as mpl, matplotlib.pyplot as plt

META_GREY = "#6b6b6b"

def apply_figure_style():
    mpl.rcParams.update({
        "figure.dpi": 150, "savefig.dpi": 300, "font.size": 7,
        "axes.titlesize": 8, "axes.labelsize": 7, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": 0.7, "xtick.major.width": 0.7, "ytick.major.width": 0.7,
        "legend.frameon": False, "figure.facecolor": "white", "axes.facecolor": "white",
    })

def panel_letter(ax, letter):
    ax.text(-0.16, 1.06, letter, transform=ax.transAxes, fontsize=9, fontweight="bold", va="top", ha="left")
