"""
make_figures.py -- builds every Python graph in the report into figures/.

Run from the repository root:
    python code/make_figures.py

Hebrew note: recent matplotlib versions (3.10+) lay out right-to-left text
correctly by themselves. Older versions draw Hebrew backwards; he() detects
the version and reverses the label only when needed. Keep Hebrew labels free
of numbers and brackets; put those in separate English text.
Font: DejaVu Sans ships with matplotlib and includes Hebrew, so this runs
the same on every computer.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

OURS = "המחקר המוצע"

# One palette for the whole report. Change it here (and in template.cls).
ACCENT = "#8B2E2E"   # deep Roman red: our solution
GREY = "#8A8A8A"     # existing tools
LIGHT = "#F4E9E1"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": "#444444",
    "axes.linewidth": 0.8,
    "savefig.bbox": "tight",
})


_MPL = tuple(int(p) for p in matplotlib.__version__.split(".")[:2])


def he(text: str) -> str:
    """Return a Hebrew label that matplotlib will show right-to-left."""
    return text if _MPL >= (3, 10) else text[::-1]


# ------------------------------------------------------------------
# Chapter 4 data: the team's assessment of each tool, scale 1-5.
# These are illustrative scores, explained in chapter 4 -- not measurements.
# ------------------------------------------------------------------
AXES = [
    "כיסוי התקופה",
    "מידע על כנסייה ומדינה",
    "נתונים מובנים",
    "גישה פתוחה",
    "קריאה במחשב",
    "ניתוח טקסט",
]
TOOLS = {
    "Seshat":           [3, 2, 5, 4, 5, 1],
    "Perseus / Scaife": [3, 2, 2, 5, 4, 2],
    "dMGH / openMGH":   [3, 4, 2, 5, 4, 1],
    "Pleiades":         [4, 1, 4, 5, 5, 1],
    OURS:   [5, 5, 5, 4, 5, 5],
}

# x = how much of our question the tool answers, y = effort to use it (1-5)
SCATTER = {
    he("קריאה ידנית"):   (4.0, 5.0),
    "Seshat":           (2.0, 2.0),
    "Perseus / Scaife": (2.0, 4.0),
    "dMGH / openMGH":   (3.0, 4.5),
    "Pleiades":         (1.0, 1.5),
    "ORBIS":            (1.0, 1.0),
    "Ithaca":           (1.5, 3.0),
    OURS:   (5.0, 2.5),
}


def radar():
    n = len(AXES)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6.2, 5.2), subplot_kw={"polar": True})
    styles = iter(["--", ":", "-.", (0, (6, 2, 1, 2))])
    for name, vals in TOOLS.items():
        v = vals + vals[:1]
        ours = name == OURS
        ax.plot(angles, v, color=ACCENT if ours else GREY,
                linewidth=2.4 if ours else 1.3,
                linestyle="-" if ours else next(styles), label=he(name) if name == OURS else name)
        if ours:
            ax.fill(angles, v, color=ACCENT, alpha=0.15)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([he(a) for a in AXES], fontsize=9)
    ax.tick_params(axis="x", pad=10)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=7, color="#666666")
    # push side labels away from the circle so they never touch it
    for lbl, ang in zip(ax.get_xticklabels(), angles[:-1]):
        x = np.cos(np.pi / 2 - ang)
        lbl.set_horizontalalignment("left" if x > 0.1 else "right" if x < -0.1 else "center")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=3,
              frameon=False, fontsize=8)
    fig.savefig(FIG / "ch4-radar.pdf")
    fig.savefig(FIG / "ch4-radar.png", dpi=150)
    plt.close(fig)


def scatter():
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    for name, (x, y) in SCATTER.items():
        ours = name == OURS
        ax.scatter(x, y, s=140 if ours else 60,
                   color=ACCENT if ours else GREY, zorder=3,
                   edgecolor="white", linewidth=1)
        ax.annotate(he(name) if name in (OURS,) else name, (x, y), textcoords="offset points", xytext=(7, 5),
                    fontsize=8.5, color=ACCENT if ours else "#333333",
                    fontweight="bold" if ours else "normal")
    ax.set_xlim(0, 5.8)
    ax.set_ylim(0, 5.8)
    ax.set_xlabel(he("כמה מהשאלה שלנו הכלי עונה") + "  (1-5)")
    ax.set_ylabel(he("מאמץ השימוש") + "  (1-5)")
    ax.axvspan(3.5, 5.8, ymin=0, ymax=3.25 / 5.8, color=LIGHT, zorder=0)
    ax.text(4.65, 0.35, he("האזור הרצוי"), ha="center", fontsize=8.5, color=ACCENT)
    ax.grid(color="#DDDDDD", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(FIG / "ch4-scatter.pdf")
    fig.savefig(FIG / "ch4-scatter.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    radar()
    scatter()
    print("figures written to", FIG)
