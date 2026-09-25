#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

COLORS = {
    "B0005": "#2563eb",
    "B0006": "#7c3aed",
    "B0007": "#f97316",
    "B0018": "#16a34a",
}
RED = "#dc2626"
GOLD = "#f59e0b"
GRAY = "#64748b"
INK = "#172033"
SOFT = "#475569"
GRID = "#e2e8f0"


def esc(value):
    return html.escape(str(value))


def open_svg(width, height):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="#ffffff"/>'
    )


def text(x, y, value, size=16, weight="400", anchor="start", fill=INK):
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">'
        f'{esc(value)}</text>'
    )


def line(x1, y1, x2, y2, stroke=GRID, width=1, dash=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{stroke}" stroke-width="{width}"{extra}/>'
    )


def box(x, y, width, height, title, lines, fill, stroke, title_fill=INK):
    out = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="15" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>',
        text(x + 18, y + 31, title, 16, "700", "start", title_fill),
    ]
    for i, item in enumerate(lines):
        out.append(text(x + 18, y + 57 + i * 21, item, 12.5, "400", "start", SOFT))
    return "".join(out)


def arrow(x1, y1, x2, y2, color=GRAY):
    return (
        line(x1, y1, x2 - 12, y2, color, 2)
        + f'<polygon points="{x2-12},{y2-6} {x2},{y2} {x2-12},{y2+6}" fill="{color}"/>'
    )


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cycles():
    return read_csv(ROOT / "data/derived/cycle_capacity_evidence.csv")


def checkpoints():
    return read_csv(ROOT / "data/derived/checkpoint_results.csv")


def aggregates():
    return read_csv(ROOT / "data/derived/checkpoint_aggregate.csv")


def architecture():
    rows = cycles()
    width, height = 1200, 720
    left, right, top, bottom = 90, 865, 125, 600
    xmin, xmax, ymin, ymax = 1, 168, 1.15, 2.08

    def sx(value):
        return left + (value - xmin) / (xmax - xmin) * (right - left)

    def sy(value):
        return bottom - (value - ymin) / (ymax - ymin) * (bottom - top)

    out = [
        open_svg(width, height),
        text(55, 52, "NASA battery capacity trajectories and monitoring checkpoints", 30, "700"),
        text(
            55,
            82,
            "Four cells • fixed checkpoints at cycles 40, 60, and 80 • NASA end of life boundary at 1.4 Ah",
            15,
            "400",
            "start",
            SOFT,
        ),
    ]

    for x in [20, 40, 60, 80, 100, 120, 140, 160]:
        xx = sx(x)
        out += [
            line(xx, top, xx, bottom, GRID),
            text(xx, bottom + 27, x, 12, "400", "middle", GRAY),
        ]

    for y in [1.2, 1.4, 1.6, 1.8, 2.0]:
        yy = sy(y)
        out += [
            line(left, yy, right, yy, GRID),
            text(left - 14, yy + 5, f"{y:.1f}", 12, "400", "end", GRAY),
        ]

    out += [
        line(left, bottom, right, bottom, "#334155", 1.7),
        line(left, top, left, bottom, "#334155", 1.7),
        line(left, sy(1.4), right, sy(1.4), RED, 2.4, "8 6"),
        text(right - 5, sy(1.4) - 9, "1.4 Ah NASA EOL", 12, "700", "end", RED),
    ]

    for checkpoint in [40, 60, 80]:
        xx = sx(checkpoint)
        out += [
            line(xx, top, xx, bottom, "#94a3b8", 1.4, "4 5"),
            f'<rect x="{xx-24}" y="{top+8}" width="48" height="24" rx="7" fill="#f8fafc" stroke="#94a3b8"/>',
            text(xx, top + 25, f"C{checkpoint}", 11, "700", "middle", SOFT),
        ]

    by_battery = {
        battery: [r for r in rows if r["battery"] == battery]
        for battery in COLORS
    }
    observed = {"B0005": 125, "B0006": 109, "B0007": None, "B0018": 97}

    for battery, color in COLORS.items():
        points = " ".join(
            f'{sx(int(r["discharge_cycle"])):.2f},{sy(float(r["capacity_ah"])):.2f}'
            for r in by_battery[battery]
        )
        out.append(
            f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.4" '
            'stroke-opacity="0.9" stroke-linejoin="round" stroke-linecap="round"/>'
        )

        crossing = observed[battery]
        if crossing is not None:
            row = next(r for r in by_battery[battery] if int(r["discharge_cycle"]) == crossing)
            out.append(
                f'<circle cx="{sx(crossing)}" cy="{sy(float(row["capacity_ah"]))}" r="6" '
                f'fill="#fff" stroke="{RED}" stroke-width="3"/>'
            )

    out += [
        text((left + right) / 2, 668, "Discharge cycle", 14, "600", "middle"),
        f'<text x="28" y="{(top+bottom)/2}" transform="rotate(-90 28 {(top+bottom)/2})" '
        'font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="600" '
        f'text-anchor="middle" fill="{INK}">Measured discharge capacity (Ah)</text>',
        '<rect x="900" y="125" width="250" height="250" rx="16" fill="#f8fafc" stroke="#cbd5e1"/>',
        text(925, 158, "Cell trajectories", 17, "700"),
    ]

    legend_y = 193
    for battery in ["B0005", "B0006", "B0007", "B0018"]:
        out += [
            line(925, legend_y, 965, legend_y, COLORS[battery], 4),
            text(980, legend_y + 5, battery, 13, "700"),
        ]
        legend_y += 36

    out += [
        line(925, legend_y, 965, legend_y, RED, 2.5, "8 6"),
        text(980, legend_y + 5, "1.4 Ah boundary", 12.5, "600"),
    ]
    legend_y += 36
    out += [
        f'<circle cx="945" cy="{legend_y}" r="6" fill="#fff" stroke="{RED}" stroke-width="3"/>',
        text(980, legend_y + 5, "Observed crossing", 12.5, "600"),
        '<rect x="900" y="402" width="250" height="198" rx="16" fill="#fff7ed" stroke="#fdba74"/>',
        text(925, 435, "What the plot shows", 15, "700", "start", "#9a3412"),
        text(925, 464, "B0005 crossing: cycle 125", 12.5, "600", "start", "#7c2d12"),
        text(925, 488, "B0006 crossing: cycle 109", 12.5, "600", "start", "#7c2d12"),
        text(925, 512, "B0018 crossing: cycle 97", 12.5, "600", "start", "#7c2d12"),
        text(925, 536, "B0007: no crossing through 168", 12.5, "600", "start", "#7c2d12"),
        text(925, 568, "Checkpoints occur before every", 12, "400", "start", "#7c2d12"),
        text(925, 588, "observed crossing in the release.", 12, "400", "start", "#7c2d12"),
        text(
            55,
            706,
            "Red circles mark first observed cycle at or below 1.4 Ah. B0007 remains above the boundary within the recorded horizon.",
            12,
            "400",
            "start",
            GRAY,
        ),
        "</svg>",
    ]
    return "".join(out)


def method():
    out = [
        open_svg(1200, 720),
        text(55, 52, "Fixed checkpoint performance margin forecasting pipeline", 30, "700"),
        text(
            55,
            82,
            "The forecast at each checkpoint sees only evidence available up to that cycle; later observations are reserved for evaluation.",
            15,
            "400",
            "start",
            SOFT,
        ),
        box(45, 135, 210, 125, "1 • NASA evidence", ["B0005 / B0006", "B0007 / B0018", "636 discharge cycles"], "#eff6ff", "#3b82f6", "#1d4ed8"),
        box(295, 135, 210, 125, "2 • Censor at checkpoint", ["Cycle 40", "Cycle 60", "Cycle 80"], "#f5f3ff", "#8b5cf6", "#6d28d9"),
        box(545, 135, 210, 125, "3 • Current margin", ["Capacity - 1.4 Ah", "State at decision time"], "#f0fdf4", "#22c55e", "#15803d"),
        box(795, 135, 210, 125, "4 • OLS trend", ["Fit available history", "No future observations"], "#fffbeb", GOLD, "#92400e"),
        arrow(255, 198, 295, 198),
        arrow(505, 198, 545, 198),
        arrow(755, 198, 795, 198),
        box(795, 330, 210, 135, "5 • Project boundary", ["Solve fitted line", "for capacity = 1.4 Ah", "Point forecast only"], "#fff7ed", "#f97316", "#9a3412"),
        arrow(900, 260, 900, 330, "#f97316"),
        box(520, 330, 225, 135, "6 • Compare later outcome", ["Observed crossing", "or no crossing horizon", "Signed + absolute error"], "#fef2f2", "#ef4444", "#991b1b"),
        arrow(795, 397, 745, 397, "#ef4444"),
        box(235, 330, 235, 135, "7 • Forecast maturity", ["Revision from prior", "checkpoint projection", "Track stability"], "#eef2ff", "#6366f1", "#4338ca"),
        arrow(520, 397, 470, 397, "#6366f1"),
        box(235, 530, 770, 115, "8 • Decision evidence", ["Current margin + projected crossing + revision history + realized error / warning status", "Interpret aggregate trends together with cell-level heterogeneity"], "#f8fafc", "#94a3b8", "#334155"),
        arrow(352, 465, 352, 530, "#6366f1"),
        arrow(632, 465, 632, 530, "#ef4444"),
        arrow(900, 465, 900, 530, "#f97316"),
        text(55, 695, "Key safeguard: checkpoints are fixed in advance and never depend on each battery's eventual lifetime or crossing cycle.", 13, "700", "start", "#334155"),
        "</svg>",
    ]
    return "".join(out)


def checkpoint_error():
    rows = checkpoints()
    width, height = 1200, 690
    left, right, top, bottom = 105, 1135, 130, 570
    log_min, log_max = -1, 3

    def y(value):
        return bottom - (math.log10(value) - log_min) / (log_max - log_min) * (bottom - top)

    x = {40: 280, 60: 600, 80: 920}
    out = [
        open_svg(width, height),
        text(55, 52, "Cell-level threshold forecast error across checkpoints", 30, "700"),
        text(55, 82, "Absolute crossing-cycle error shown on a logarithmic scale so both large and small errors remain visible.", 15, "400", "start", SOFT),
    ]

    for value in [0.1, 1, 10, 100, 1000]:
        yy = y(value)
        out += [
            line(left, yy, right, yy, GRID),
            text(left - 14, yy + 5, value, 12, "400", "end", GRAY),
        ]

    for checkpoint in [40, 60, 80]:
        out += [
            line(x[checkpoint], top, x[checkpoint], bottom, "#f1f5f9"),
            text(x[checkpoint], bottom + 32, f"Cycle {checkpoint}", 13, "700", "middle", "#334155"),
        ]

    for battery in ["B0005", "B0006", "B0018"]:
        values = sorted(
            [r for r in rows if r["battery"] == battery],
            key=lambda r: int(r["checkpoint_cycle"]),
        )
        points = " ".join(
            f'{x[int(r["checkpoint_cycle"])]},{y(abs(float(r["projection_error_cycles"]))):.2f}'
            for r in values
        )
        out.append(
            f'<polyline points="{points}" fill="none" stroke="{COLORS[battery]}" '
            'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        for row in values:
            value = abs(float(row["projection_error_cycles"]))
            xx = x[int(row["checkpoint_cycle"])]
            yy = y(value)
            out += [
                f'<circle cx="{xx}" cy="{yy}" r="7" fill="#fff" stroke="{COLORS[battery]}" stroke-width="3"/>',
                text(xx + 12, yy - 10, f"{value:.3f}", 11.5, "700", "start", COLORS[battery]),
            ]

    out += [
        line(left, bottom, right, bottom, "#334155", 1.7),
        line(left, top, left, bottom, "#334155", 1.7),
        f'<text x="28" y="{(top+bottom)/2}" transform="rotate(-90 28 {(top+bottom)/2})" '
        'font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="600" '
        f'text-anchor="middle" fill="{INK}">Absolute threshold-cycle error (log scale)</text>',
        '<rect x="810" y="105" width="325" height="92" rx="12" fill="#f8fafc" stroke="#cbd5e1"/>',
    ]

    legend_x = 835
    for battery in ["B0005", "B0006", "B0018"]:
        out += [
            line(legend_x, 135, legend_x + 35, 135, COLORS[battery], 4),
            text(legend_x + 45, 140, battery, 12.5, "700"),
        ]
        legend_x += 95

    out += [
        text(835, 172, "B0006 is the key counterexample:", 11.5, "600", "start", SOFT),
        text(835, 190, "0.346 → 6.025 → 15.566 cycles", 11.5, "700", "start", COLORS["B0006"]),
        text(55, 666, "Aggregate MAE improves, but later checkpoints do not improve every battery. B0007 is excluded because no observed 1.4 Ah crossing occurs.", 12, "400", "start", GRAY),
        "</svg>",
    ]
    return "".join(out)


def forecast_revision():
    rows = checkpoints()
    width, height = 1200, 700
    left, right, top, bottom = 110, 1120, 135, 570
    max_revision = 200

    def y(value):
        return bottom - (value / max_revision) * (bottom - top)

    x = {"40→60": 390, "60→80": 800}
    offsets = {"B0005": -54, "B0006": -18, "B0007": 18, "B0018": 54}

    out = [
        open_svg(width, height),
        text(55, 52, "Forecast revision by battery and checkpoint transition", 30, "700"),
        text(55, 82, "Absolute change in projected threshold cycle; smaller values indicate a more stable point forecast, not calibrated certainty.", 15, "400", "start", SOFT),
    ]

    for value in [0, 50, 100, 150, 200]:
        yy = y(value)
        out += [
            line(left, yy, right, yy, GRID),
            text(left - 14, yy + 5, value, 12, "400", "end", GRAY),
        ]

    for label, xx in x.items():
        out.append(text(xx, bottom + 34, label, 14, "700", "middle", "#334155"))

    for battery in ["B0005", "B0006", "B0007", "B0018"]:
        r60 = next(r for r in rows if r["battery"] == battery and r["checkpoint_cycle"] == "60")
        r80 = next(r for r in rows if r["battery"] == battery and r["checkpoint_cycle"] == "80")
        v60, v80 = float(r60["forecast_revision_cycles"]), float(r80["forecast_revision_cycles"])
        x60, x80 = x["40→60"] + offsets[battery], x["60→80"] + offsets[battery]
        y60, y80 = y(v60), y(v80)
        out += [
            line(x60, y60, x80, y80, COLORS[battery], 2.2),
            f'<circle cx="{x60}" cy="{y60}" r="8" fill="{COLORS[battery]}" fill-opacity="0.85" stroke="#fff" stroke-width="1.5"/>',
            f'<circle cx="{x80}" cy="{y80}" r="8" fill="{COLORS[battery]}" fill-opacity="0.85" stroke="#fff" stroke-width="1.5"/>',
            text(x60, y60 - 13, f"{v60:.1f}", 10.5, "700", "middle", COLORS[battery]),
            text(x80, y80 - 13, f"{v80:.1f}", 10.5, "700", "middle", COLORS[battery]),
        ]

    out += [
        line(left, bottom, right, bottom, "#334155", 1.7),
        line(left, top, left, bottom, "#334155", 1.7),
        f'<text x="28" y="{(top+bottom)/2}" transform="rotate(-90 28 {(top+bottom)/2})" '
        'font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="600" '
        f'text-anchor="middle" fill="{INK}">Absolute forecast revision (cycles)</text>',
        '<rect x="835" y="110" width="285" height="125" rx="12" fill="#f8fafc" stroke="#cbd5e1"/>',
    ]

    legend_y = 138
    for battery in ["B0005", "B0006", "B0007", "B0018"]:
        out += [
            f'<circle cx="858" cy="{legend_y}" r="6" fill="{COLORS[battery]}"/>',
            text(875, legend_y + 5, battery, 12.5, "700"),
        ]
        legend_y += 24

    out += [
        text(55, 676, "Mean revision falls from 100.046 cycles (40→60) to 38.012 cycles (60→80), while substantial cell-level movement remains.", 12, "400", "start", GRAY),
        "</svg>",
    ]
    return "".join(out)


def evaluation():
    out = [
        open_svg(1200, 650),
        text(55, 52, "Evidence boundary and released findings", 30, "700"),
        box(55, 100, 1090, 96, "Design correction", ["Fixed 40 / 60 / 80 checkpoints remove dependence on each cell's eventual recorded lifetime."], "#eff6ff", "#3b82f6", "#1d4ed8"),
        box(55, 220, 1090, 96, "Aggregate finding", ["MAE across crossing cells falls 102.399 → 35.852 → 11.942 cycles as checkpoint evidence accumulates."], "#f0fdf4", "#22c55e", "#15803d"),
        box(55, 340, 1090, 96, "Heterogeneity warning", ["B0006 gets less accurate across checkpoints even while the aggregate improves; B0005 drives much of the early MAE."], "#fff7ed", "#f97316", "#9a3412"),
        box(55, 460, 1090, 96, "False warning and claim limit", ["B0007 projects 158.219 at cycle 80 but never crosses 1.4 Ah through 168. Four-cell baseline only; no calibrated uncertainty or production BMS claim."], "#fef2f2", "#ef4444", "#991b1b"),
        text(55, 625, "Interpretation: forecast revision and cell-level behavior should accompany a point estimate of margin exhaustion.", 13, "700", "start", "#334155"),
        "</svg>",
    ]
    return "".join(out)


def render(out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    figures = {
        "architecture.svg": architecture(),
        "method.svg": method(),
        "checkpoint_error.svg": checkpoint_error(),
        "forecast_revision.svg": forecast_revision(),
        "evaluation.svg": evaluation(),
    }
    for name, content in figures.items():
        ET.fromstring(content)
        (out_dir / name).write_text(content, encoding="utf-8")
    return figures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default=str(ROOT / "assets"))
    args = parser.parse_args()
    figures = render(Path(args.out_dir))
    print("generated_figures:", len(figures))


if __name__ == "__main__":
    main()
