"""Build the approved Problem 12 Figure 1 concept in a white publication style."""

from collections import deque
from pathlib import Path
import json

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
RESULTS = ROOT / "results" / "frozen_results.json"
OUTFIELD_ROLES = ("CB", "FB", "WB", "DM", "CM", "AM", "W", "ST")
TAXONOMY_B_EDGES = (
    ("CB", "FB"), ("CB", "DM"), ("FB", "WB"), ("WB", "W"),
    ("DM", "CM"), ("CM", "AM"), ("AM", "W"), ("AM", "ST"),
    ("W", "ST"),
)

POSITIONS = {
    "CB": (50, 81), "FB": (22, 73), "WB": (16, 55), "DM": (50, 65),
    "CM": (50, 50), "AM": (50, 34), "W": (20, 26), "ST": (50, 16),
}

# Restrained accents chosen to sit beside the existing Figure 2 palette.
CHARCOAL = "#202124"
MID_GREY = "#62676d"
LIGHT_GREY = "#d6d9dc"
PITCH_GREY = "#c9cdd1"
EDGE_GREY = "#aeb5bb"
BLUE = "#377eb8"
ORANGE = "#c9782b"
PALE_BLUE = "#f4f8fb"
WHITE = "#ffffff"


def graph_distances(nodes, edges):
    graph = {node: set() for node in nodes}
    for left, right in edges:
        graph[left].add(right); graph[right].add(left)
    distances = {}
    for start in nodes:
        queue = deque([(start, 0)]); seen = {start}
        while queue:
            node, distance = queue.popleft(); distances[(start, node)] = distance
            for neighbor in graph[node] - seen:
                seen.add(neighbor); queue.append((neighbor, distance + 1))
    return graph, distances


def draw_pitch(ax):
    ax.set_facecolor(WHITE)
    ax.add_patch(Rectangle((5, 5), 90, 90, fill=False, edgecolor=PITCH_GREY, lw=1.7))
    ax.plot([5, 95], [50, 50], color=PITCH_GREY, lw=1.35)
    ax.add_patch(Circle((50, 50), 9.15, fill=False, edgecolor=PITCH_GREY, lw=1.35))
    ax.add_patch(Circle((50, 50), .65, color=PITCH_GREY))
    for y in (5, 78.5): ax.add_patch(Rectangle((25, y), 50, 16.5, fill=False, edgecolor=PITCH_GREY, lw=1.35))
    for y in (5, 89.5): ax.add_patch(Rectangle((39, y), 22, 5.5, fill=False, edgecolor=PITCH_GREY, lw=1.35))
    ax.add_patch(Arc((50, 16), 18.3, 18.3, theta1=35, theta2=145, color=PITCH_GREY, lw=1.2))
    ax.add_patch(Arc((50, 84), 18.3, 18.3, theta1=215, theta2=325, color=PITCH_GREY, lw=1.2))
    ax.set_xlim(0, 100); ax.set_ylim(100, 0); ax.set_aspect("equal"); ax.axis("off")


def main():
    # Deterministic white styling regardless of local Matplotlib theme.
    mpl.rcParams.update({
        "figure.facecolor": WHITE,
        "axes.facecolor": WHITE,
        "savefig.facecolor": WHITE,
        "savefig.edgecolor": WHITE,
        "font.family": "DejaVu Sans",
        "text.color": CHARCOAL,
    })

    nodes = list(OUTFIELD_ROLES)
    edges = list(TAXONOMY_B_EDGES)
    assert nodes == ["CB", "FB", "WB", "DM", "CM", "AM", "W", "ST"]
    assert set(nodes) == set(POSITIONS)
    _, distances = graph_distances(nodes, edges)
    assert set(distances.values()) == {0, 1, 2, 3, 4}
    assert distances[("DM", "CM")] == 1
    assert distances[("FB", "ST")] == 3

    frozen = json.loads(RESULTS.read_text(encoding="utf-8"))
    assert [list(edge) for edge in edges] == frozen["role_graph"]["conservative_edges"]
    row = frozen["distance_only"]
    rho, p_value = float(row["spearman_rho"]), float(row["permutation_p"])
    assert round(rho, 4) == 0.1547 and round(p_value, 4) == 0.0488

    OUT.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(14, 7.15), facecolor=WHITE)
    pitch = fig.add_axes([.035, .075, .555, .80]); draw_pitch(pitch)

    for left, right in edges:
        x1, y1 = POSITIONS[left]; x2, y2 = POSITIONS[right]
        pitch.plot([x1, x2], [y1, y2], color=EDGE_GREY, lw=2.5, alpha=.95, zorder=2)

    pitch.plot([50, 50], [65, 50], color=BLUE, lw=7.2, solid_capstyle="round", zorder=3)
    for left, right in [("FB", "WB"), ("WB", "W"), ("W", "ST")]:
        x1, y1 = POSITIONS[left]; x2, y2 = POSITIONS[right]
        pitch.plot([x1, x2], [y1, y2], color=ORANGE, lw=7.2, solid_capstyle="round", zorder=3)

    for role in nodes:
        x, y = POSITIONS[role]
        pitch.scatter([x], [y], s=1020, color=WHITE, edgecolor=CHARCOAL, linewidth=2.2, zorder=4)
        pitch.text(x, y+.25, role, ha="center", va="center", fontsize=14, fontweight="bold", color=CHARCOAL, zorder=5)

    fig.text(.045, .947, "Position is a variable, not just a label", fontsize=23, fontweight="bold", color=CHARCOAL)
    fig.text(.045, .897, "Tactical distance links role changes to changes in the same player’s performance profile", fontsize=13.2, color=MID_GREY)

    side = fig.add_axes([.615, .095, .355, .72], facecolor=WHITE); side.axis("off")
    side.add_patch(FancyBboxPatch((0, .70), 1, .28, boxstyle="round,pad=.018,rounding_size=.02", facecolor=WHITE, edgecolor=LIGHT_GREY, linewidth=1.4))
    side.text(.06, .92, "TACTICAL DISTANCE", fontsize=11.8, fontweight="bold", color=CHARCOAL)
    side.plot([.07, .27], [.84, .84], color=BLUE, lw=7, solid_capstyle="round")
    side.text(.32, .84, "1 edge  •  adjacent", va="center", fontsize=13.0, fontweight="bold", color=CHARCOAL)
    side.text(.07, .78, "2 edges  •  two graph steps", va="center", fontsize=12.2, color=CHARCOAL)
    side.plot([.07, .27], [.725, .725], color=ORANGE, lw=7, solid_capstyle="round")
    side.text(.32, .725, "3–4 edges  •  more distant", va="center", fontsize=12.5, fontweight="bold", color=CHARCOAL)

    side.add_patch(FancyBboxPatch((0, .31), 1, .31, boxstyle="round,pad=.018,rounding_size=.02", facecolor=PALE_BLUE, edgecolor=LIGHT_GREY, linewidth=1.2))
    side.text(.06, .55, "GREATER TACTICAL DISTANCE", fontsize=11.2, fontweight="bold", color=CHARCOAL)
    side.text(.06, .505, "was associated with greater profile divergence", fontsize=11.0, color=MID_GREY)
    side.text(.06, .425, f"ρ = {rho:.4f}", fontsize=24, fontweight="bold", color=CHARCOAL)
    side.text(.06, .365, f"permutation p = {p_value:.4f}", fontsize=13.5, color=MID_GREY)
    side.text(.06, .325, "Association, not a causal effect", fontsize=9.8, color=MID_GREY)

    side.text(.01, .245, "PERFORMANCE PROFILE", fontsize=11.2, fontweight="bold", color=CHARCOAL)
    side.text(.01, .195, "Attack  •  Progression  •  Possession  •  Defense", fontsize=11.3, color=MID_GREY)
    side.plot([.01, .99], [.15, .15], color=LIGHT_GREY, lw=1)
    side.text(.01, .105, "Pitch locations are schematic.", fontsize=10.8, fontweight="bold", color=CHARCOAL)
    side.text(.01, .06, "Tactical distance = shortest-path distance in the frozen role graph.", fontsize=10.3, color=MID_GREY)
    side.text(.01, .015, "It does not represent physical distance in metres.", fontsize=10.3, color=MID_GREY)
    side.set_xlim(-.03, 1.03); side.set_ylim(0, 1)

    outputs = {
        "png": OUT / "figure1_tactical_role_distance.png",
        "pdf": OUT / "figure1_tactical_role_distance.pdf",
        "svg": OUT / "figure1_tactical_role_distance.svg",
    }
    for kind, path in outputs.items():
        fig.savefig(path, dpi=240 if kind == "png" else None, facecolor=WHITE, edgecolor=WHITE, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
