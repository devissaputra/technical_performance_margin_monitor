#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.model import (
    BATTERIES,
    CHECKPOINTS,
    THRESHOLD_AH,
    aggregate_recomputed,
    analyze_series,
    first_crossing,
)

NASA_URL = "https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip"
EXPECTED_ARCHIVE_SHA256 = "82302a7db4fc1b34e0b6676326610438d43b816bdf11a69d1d012a464ef2f92e"


def nested_mats(blob):
    wanted = {f"{battery}.mat" for battery in BATTERIES}
    found = {}

    def visit(zip_bytes):
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
            for name in archive.namelist():
                base = Path(name).name
                if base in wanted and base not in found:
                    found[base] = archive.read(name)
                elif name.lower().endswith(".zip"):
                    try:
                        visit(archive.read(name))
                    except zipfile.BadZipFile:
                        pass

    visit(blob)
    missing = wanted - set(found)
    if missing:
        raise RuntimeError(f"Missing NASA MAT files: {sorted(missing)}")
    return found


def extract_capacity(mat_bytes, battery):
    data = loadmat(io.BytesIO(mat_bytes), squeeze_me=True, struct_as_record=False)
    obj = data[battery]
    output = []
    index = 0

    for cycle in np.atleast_1d(obj.cycle):
        if str(cycle.type).strip().lower() != "discharge":
            continue
        discharge_data = cycle.data
        if not hasattr(discharge_data, "Capacity"):
            continue
        index += 1
        capacity = float(np.asarray(discharge_data.Capacity).squeeze())
        output.append((index, capacity))

    return output


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def packaged_cycles():
    return read_csv(ROOT / "data/derived/cycle_capacity_evidence.csv")


def packaged_battery_summary():
    return read_csv(ROOT / "data/derived/battery_summary.csv")


def packaged_checkpoints():
    return read_csv(ROOT / "data/derived/checkpoint_results.csv")


def packaged_aggregate():
    return read_csv(ROOT / "data/derived/checkpoint_aggregate.csv")


def packaged_summary():
    return json.loads(
        (ROOT / "results/empirical_summary.json").read_text(encoding="utf-8")
    )


def close(a, b, tolerance=1e-9):
    return abs(float(a) - float(b)) <= tolerance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    payload = urllib.request.urlopen(NASA_URL, timeout=120).read()
    archive_sha = hashlib.sha256(payload).hexdigest()
    print("NASA archive sha256:", archive_sha)

    if archive_sha != EXPECTED_ARCHIVE_SHA256:
        raise SystemExit("FAIL: NASA archive SHA-256 changed")

    mats = nested_mats(payload)
    rebuilt = {
        battery: extract_capacity(mats[f"{battery}.mat"], battery)
        for battery in BATTERIES
    }
    print("cycles:", {battery: len(values) for battery, values in rebuilt.items()})

    if not args.check:
        for battery in BATTERIES:
            print(battery, analyze_series(rebuilt[battery]))
        return

    packaged_cycle_rows = packaged_cycles()
    for battery in BATTERIES:
        expected = [r for r in packaged_cycle_rows if r["battery"] == battery]
        got = rebuilt[battery]

        if len(expected) != len(got):
            raise SystemExit(f"FAIL: cycle count mismatch for {battery}")

        for row, (index, capacity) in zip(expected, got):
            if int(row["discharge_cycle"]) != index:
                raise SystemExit(f"FAIL: cycle index mismatch for {battery}/{index}")
            if not close(row["capacity_ah"], capacity):
                raise SystemExit(f"FAIL: NASA capacity mismatch for {battery} cycle {index}")
            if not close(row["margin_to_1_4_ah"], capacity - THRESHOLD_AH):
                raise SystemExit(f"FAIL: margin mismatch for {battery} cycle {index}")

    packaged_batteries = {
        row["battery"]: row for row in packaged_battery_summary()
    }
    expected_crossings = {}

    for battery in BATTERIES:
        series = rebuilt[battery]
        crossing = first_crossing(series)
        expected_crossings[battery] = crossing
        row = packaged_batteries[battery]

        if int(row["n_cycles"]) != len(series):
            raise SystemExit(f"FAIL: battery summary cycle count mismatch for {battery}")
        if not close(row["first_capacity_ah"], series[0][1]):
            raise SystemExit(f"FAIL: first capacity mismatch for {battery}")
        if not close(row["last_capacity_ah"], series[-1][1]):
            raise SystemExit(f"FAIL: final capacity mismatch for {battery}")
        if not close(row["final_margin_ah"], series[-1][1] - THRESHOLD_AH):
            raise SystemExit(f"FAIL: final margin mismatch for {battery}")

        packaged_crossing = (
            int(row["observed_first_cycle_le_1_4"])
            if row["observed_first_cycle_le_1_4"]
            else None
        )
        if packaged_crossing != crossing:
            raise SystemExit(f"FAIL: observed crossing mismatch for {battery}")

    packaged_checkpoint_rows = {
        (row["battery"], int(row["checkpoint_cycle"])): row
        for row in packaged_checkpoints()
    }
    recomputed = []

    for battery in BATTERIES:
        for result in analyze_series(rebuilt[battery]):
            recomputed.append((battery, result))
            row = packaged_checkpoint_rows[(battery, result["checkpoint"])]

            numeric_pairs = {
                "last_observed_capacity_ah": result["last_observed_capacity"],
                "slope_ah_per_cycle": result["slope"],
                "projected_threshold_cycle": result["projected_threshold_cycle"],
            }
            for key, value in numeric_pairs.items():
                if not close(row[key], value, tolerance=0.0015 if key == "projected_threshold_cycle" else 1e-9):
                    raise SystemExit(
                        f"FAIL: {key} mismatch for {battery}/{result['checkpoint']}"
                    )

            if not close(
                row["margin_to_1_4_ah"],
                result["last_observed_capacity"] - THRESHOLD_AH,
            ):
                raise SystemExit(
                    f"FAIL: checkpoint margin mismatch for {battery}/{result['checkpoint']}"
                )

            packaged_observed = (
                int(row["observed_threshold_cycle"])
                if row["observed_threshold_cycle"]
                else None
            )
            if packaged_observed != result["observed_threshold_cycle"]:
                raise SystemExit(
                    f"FAIL: observed threshold mismatch for {battery}/{result['checkpoint']}"
                )

            if result["projection_error_cycles"] is None:
                if row["projection_error_cycles"]:
                    raise SystemExit(
                        f"FAIL: unexpected packaged error for {battery}/{result['checkpoint']}"
                    )
            elif not close(
                row["projection_error_cycles"],
                result["projection_error_cycles"],
                tolerance=0.0015,
            ):
                raise SystemExit(
                    f"FAIL: projection error mismatch for {battery}/{result['checkpoint']}"
                )

            if result["forecast_revision_cycles"] is None:
                if row["forecast_revision_cycles"]:
                    raise SystemExit(
                        f"FAIL: unexpected packaged revision for {battery}/{result['checkpoint']}"
                    )
            elif not close(
                row["forecast_revision_cycles"],
                result["forecast_revision_cycles"],
                tolerance=0.0015,
            ):
                raise SystemExit(
                    f"FAIL: forecast revision mismatch for {battery}/{result['checkpoint']}"
                )

            if (
                row["projection_within_observed_horizon"].lower() == "true"
            ) != result["projection_within_observed_horizon"]:
                raise SystemExit(
                    f"FAIL: horizon flag mismatch for {battery}/{result['checkpoint']}"
                )

            if (
                row["false_early_warning"].lower() == "true"
            ) != result["false_early_warning"]:
                raise SystemExit(
                    f"FAIL: false warning mismatch for {battery}/{result['checkpoint']}"
                )

    recalculated_aggregate = {
        result["checkpoint_cycle"]: result
        for result in aggregate_recomputed(recomputed)
    }
    packaged_aggregate_rows = {
        int(row["checkpoint_cycle"]): row
        for row in packaged_aggregate()
    }

    for checkpoint in CHECKPOINTS:
        calculated = recalculated_aggregate[checkpoint]
        row = packaged_aggregate_rows[checkpoint]

        for key in (
            "mae_cycles_crossing_cells",
            "median_abs_error_cycles_crossing_cells",
        ):
            if not close(row[key], calculated[key]):
                raise SystemExit(f"FAIL: aggregate {key} mismatch at checkpoint {checkpoint}")

        packaged_revision = (
            float(row["mean_forecast_revision_cycles"])
            if row["mean_forecast_revision_cycles"]
            else None
        )
        if packaged_revision != calculated["mean_forecast_revision_cycles"]:
            raise SystemExit(
                f"FAIL: aggregate revision mismatch at checkpoint {checkpoint}"
            )

        if int(row["false_early_warnings"]) != calculated["false_early_warnings"]:
            raise SystemExit(
                f"FAIL: aggregate warning count mismatch at checkpoint {checkpoint}"
            )

    summary = packaged_summary()["headline_metrics"]
    if summary["observed_eol_cycles"] != expected_crossings:
        raise SystemExit("FAIL: summary observed crossing map differs from NASA rebuild")
    if summary["checkpoint_80_mae_cycles_crossing_cells"] != recalculated_aggregate[80]["mae_cycles_crossing_cells"]:
        raise SystemExit("FAIL: summary checkpoint 80 MAE differs from NASA rebuild")
    if summary["b0007_false_early_warning_at_80"] is not True:
        raise SystemExit("FAIL: summary B0007 warning flag is inconsistent")

    print("official_nasa_rebuild: PASS")


if __name__ == "__main__":
    main()
