from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

THRESHOLD_AH = 1.4
CHECKPOINTS = (40, 60, 80)
BATTERIES = ("B0005", "B0006", "B0007", "B0018")


def linear_threshold_projection(series, checkpoint, threshold=THRESHOLD_AH):
    series = sorted((int(x), float(y)) for x, y in series)
    if checkpoint < 2 or checkpoint > len(series):
        raise ValueError("invalid checkpoint")

    training = series[:checkpoint]
    n = len(training)
    mean_x = sum(x for x, _ in training) / n
    mean_y = sum(y for _, y in training) / n
    denominator = sum((x - mean_x) ** 2 for x, _ in training)
    slope = sum((x - mean_x) * (y - mean_y) for x, y in training) / denominator
    intercept = mean_y - slope * mean_x
    projected = (threshold - intercept) / slope if slope < 0 else None

    return {
        "checkpoint": checkpoint,
        "slope": slope,
        "intercept": intercept,
        "projected_threshold_cycle": projected,
        "last_observed_capacity": training[-1][1],
    }


def first_crossing(series, threshold=THRESHOLD_AH):
    return next(
        (int(cycle) for cycle, capacity in sorted(series) if float(capacity) <= threshold),
        None,
    )


def analyze_series(series, checkpoints=CHECKPOINTS, threshold=THRESHOLD_AH):
    series = sorted((int(x), float(y)) for x, y in series)
    observed = first_crossing(series, threshold)
    last_cycle = series[-1][0]
    results = []
    previous_projection = None

    for checkpoint in checkpoints:
        projection = linear_threshold_projection(series, checkpoint, threshold)
        projected_cycle = projection["projected_threshold_cycle"]

        signed_error = (
            None
            if observed is None or projected_cycle is None
            else projected_cycle - observed
        )
        revision = (
            None
            if previous_projection is None or projected_cycle is None
            else abs(projected_cycle - previous_projection)
        )
        within_horizon = (
            projected_cycle is not None
            and checkpoint < projected_cycle <= last_cycle
        )

        results.append(
            {
                **projection,
                "observed_threshold_cycle": observed,
                "projection_error_cycles": signed_error,
                "forecast_revision_cycles": revision,
                "projection_within_observed_horizon": within_horizon,
                "false_early_warning": bool(observed is None and within_horizon),
            }
        )
        previous_projection = projected_cycle

    return results


def load_cycle_evidence():
    with (ROOT / "data/derived/cycle_capacity_evidence.csv").open(
        newline="", encoding="utf-8"
    ) as f:
        return list(csv.DictReader(f))


def load_battery_summary():
    with (ROOT / "data/derived/battery_summary.csv").open(
        newline="", encoding="utf-8"
    ) as f:
        return list(csv.DictReader(f))


def load_checkpoint_results():
    with (ROOT / "data/derived/checkpoint_results.csv").open(
        newline="", encoding="utf-8"
    ) as f:
        return list(csv.DictReader(f))


def load_checkpoint_aggregate():
    with (ROOT / "data/derived/checkpoint_aggregate.csv").open(
        newline="", encoding="utf-8"
    ) as f:
        return list(csv.DictReader(f))


def load_summary():
    return json.loads(
        (ROOT / "results/empirical_summary.json").read_text(encoding="utf-8")
    )


def recompute_from_packaged():
    rows = load_cycle_evidence()
    by_battery = {}
    for battery in BATTERIES:
        by_battery[battery] = [
            (int(r["discharge_cycle"]), float(r["capacity_ah"]))
            for r in rows
            if r["battery"] == battery
        ]

    output = []
    for battery in BATTERIES:
        for result in analyze_series(by_battery[battery]):
            output.append((battery, result))
    return output


def aggregate_recomputed(recomputed):
    output = []
    for checkpoint in CHECKPOINTS:
        checkpoint_rows = [
            result
            for _, result in recomputed
            if result["checkpoint"] == checkpoint
        ]
        abs_errors = [
            abs(result["projection_error_cycles"])
            for result in checkpoint_rows
            if result["projection_error_cycles"] is not None
        ]
        revisions = [
            result["forecast_revision_cycles"]
            for result in checkpoint_rows
            if result["forecast_revision_cycles"] is not None
        ]
        output.append(
            {
                "checkpoint_cycle": checkpoint,
                "mae_cycles_crossing_cells": round(statistics.mean(abs_errors), 3),
                "median_abs_error_cycles_crossing_cells": round(
                    statistics.median(abs_errors), 3
                ),
                "mean_forecast_revision_cycles": (
                    None if not revisions else round(statistics.mean(revisions), 3)
                ),
                "false_early_warnings": sum(
                    result["false_early_warning"] for result in checkpoint_rows
                ),
            }
        )
    return output


def validate_bundle():
    cycle_rows = load_cycle_evidence()
    if len(cycle_rows) != 636:
        return False

    cycle_counts = {
        battery: sum(r["battery"] == battery for r in cycle_rows)
        for battery in BATTERIES
    }
    if cycle_counts != {
        "B0005": 168,
        "B0006": 168,
        "B0007": 168,
        "B0018": 132,
    }:
        return False

    battery_summary = {r["battery"]: r for r in load_battery_summary()}
    expected_crossings = {
        "B0005": 125,
        "B0006": 109,
        "B0007": None,
        "B0018": 97,
    }
    for battery, expected in expected_crossings.items():
        raw = battery_summary[battery]["observed_first_cycle_le_1_4"]
        packaged = int(raw) if raw else None
        if packaged != expected:
            return False

    recomputed = recompute_from_packaged()
    packaged_checkpoints = {
        (r["battery"], int(r["checkpoint_cycle"])): r
        for r in load_checkpoint_results()
    }

    if len(packaged_checkpoints) != 12:
        return False

    for battery, result in recomputed:
        row = packaged_checkpoints[(battery, result["checkpoint"])]
        if abs(
            float(row["projected_threshold_cycle"])
            - result["projected_threshold_cycle"]
        ) > 0.0015:
            return False

        packaged_observed = (
            int(row["observed_threshold_cycle"])
            if row["observed_threshold_cycle"]
            else None
        )
        if packaged_observed != result["observed_threshold_cycle"]:
            return False

        if packaged_observed is not None and int(row["checkpoint_cycle"]) >= packaged_observed:
            return False

        if (
            row["projection_within_observed_horizon"].lower() == "true"
        ) != result["projection_within_observed_horizon"]:
            return False

        if (
            row["false_early_warning"].lower() == "true"
        ) != result["false_early_warning"]:
            return False

    recalculated_aggregate = aggregate_recomputed(recomputed)
    packaged_aggregate = {
        int(r["checkpoint_cycle"]): r for r in load_checkpoint_aggregate()
    }

    for result in recalculated_aggregate:
        row = packaged_aggregate[result["checkpoint_cycle"]]
        for key in (
            "mae_cycles_crossing_cells",
            "median_abs_error_cycles_crossing_cells",
        ):
            if abs(float(row[key]) - float(result[key])) > 1e-9:
                return False

        packaged_revision = (
            float(row["mean_forecast_revision_cycles"])
            if row["mean_forecast_revision_cycles"]
            else None
        )
        if packaged_revision != result["mean_forecast_revision_cycles"]:
            return False

        if int(row["false_early_warnings"]) != result["false_early_warnings"]:
            return False

    summary = load_summary()["headline_metrics"]
    expected_summary = {
        "n_discharge_cycles": 636,
        "eol_threshold_ah": 1.4,
        "monitoring_checkpoints_cycles": [40, 60, 80],
        "checkpoint_80_mae_cycles_crossing_cells": 11.942,
        "mean_forecast_revision_40_to_60_cycles": 100.046,
        "mean_forecast_revision_60_to_80_cycles": 38.012,
        "b0005_projection_cycle_40": 413.782,
        "b0005_projection_cycle_60": 216.817,
        "b0005_projection_cycle_80": 145.025,
        "b0007_projection_cycle_80": 158.219,
        "b0007_false_early_warning_at_80": True,
    }
    for key, value in expected_summary.items():
        if summary[key] != value:
            return False

    return summary["observed_eol_cycles"] == {
        "B0005": 125,
        "B0006": 109,
        "B0007": None,
        "B0018": 97,
    }


# GitHub Actions verifies both offline and official-source rebuild paths.
