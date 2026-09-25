from research.model import (
    BATTERIES,
    CHECKPOINTS,
    THRESHOLD_AH,
    aggregate_recomputed,
    analyze_series,
    linear_threshold_projection,
    load_battery_summary,
    load_checkpoint_aggregate,
    load_checkpoint_results,
    load_cycle_evidence,
    recompute_from_packaged,
    validate_bundle,
)


def test_fixed_checkpoint_fixture():
    series = [(i, 2.0 - 0.005 * i) for i in range(1, 121)]
    result = linear_threshold_projection(series, 40, 1.4)
    assert result["checkpoint"] == 40
    assert abs(result["projected_threshold_cycle"] - 120) < 1e-8


def test_complete_cycle_evidence():
    rows = load_cycle_evidence()
    assert len(rows) == 636
    counts = {
        battery: sum(r["battery"] == battery for r in rows)
        for battery in BATTERIES
    }
    assert counts == {
        "B0005": 168,
        "B0006": 168,
        "B0007": 168,
        "B0018": 132,
    }


def test_observed_crossings_are_exact():
    rows = {r["battery"]: r for r in load_battery_summary()}
    assert rows["B0005"]["observed_first_cycle_le_1_4"] == "125"
    assert rows["B0006"]["observed_first_cycle_le_1_4"] == "109"
    assert rows["B0018"]["observed_first_cycle_le_1_4"] == "97"
    assert rows["B0007"]["observed_first_cycle_le_1_4"] == ""


def test_checkpoints_are_future_independent_and_before_observed_eol():
    rows = load_checkpoint_results()
    assert sorted({int(r["checkpoint_cycle"]) for r in rows}) == list(CHECKPOINTS)
    for row in rows:
        if row["observed_threshold_cycle"]:
            assert int(row["checkpoint_cycle"]) < int(row["observed_threshold_cycle"])


def test_exact_checkpoint_80_results():
    rows = {
        (r["battery"], int(r["checkpoint_cycle"])): r
        for r in load_checkpoint_results()
    }
    expected = {
        "B0005": 145.025,
        "B0006": 93.434,
        "B0007": 158.219,
        "B0018": 96.764,
    }
    for battery, projection in expected.items():
        assert abs(
            float(rows[(battery, 80)]["projected_threshold_cycle"]) - projection
        ) < 0.002


def test_b0006_is_counterexample_to_monotonic_accuracy_improvement():
    rows = {
        (r["battery"], int(r["checkpoint_cycle"])): r
        for r in load_checkpoint_results()
    }
    errors = [
        abs(float(rows[("B0006", checkpoint)]["projection_error_cycles"]))
        for checkpoint in CHECKPOINTS
    ]
    assert errors == [0.346, 6.025, 15.566]


def test_b0007_false_early_warning_only_at_80():
    rows = {
        (r["battery"], int(r["checkpoint_cycle"])): r
        for r in load_checkpoint_results()
    }
    assert rows[("B0007", 40)]["false_early_warning"] == "false"
    assert rows[("B0007", 60)]["false_early_warning"] == "false"
    assert rows[("B0007", 80)]["false_early_warning"] == "true"


def test_aggregate_results_recompute_exactly():
    calculated = {
        r["checkpoint_cycle"]: r
        for r in aggregate_recomputed(recompute_from_packaged())
    }
    packaged = {
        int(r["checkpoint_cycle"]): r for r in load_checkpoint_aggregate()
    }
    assert calculated[40]["mae_cycles_crossing_cells"] == 102.399
    assert calculated[60]["mae_cycles_crossing_cells"] == 35.852
    assert calculated[80]["mae_cycles_crossing_cells"] == 11.942
    assert calculated[60]["mean_forecast_revision_cycles"] == 100.046
    assert calculated[80]["mean_forecast_revision_cycles"] == 38.012
    for checkpoint in CHECKPOINTS:
        assert float(packaged[checkpoint]["mae_cycles_crossing_cells"]) == calculated[checkpoint]["mae_cycles_crossing_cells"]


def test_projection_inside_horizon_requires_future_cycle():
    series = [(i, 2.0 - 0.004 * i) for i in range(1, 101)]
    results = analyze_series(series, checkpoints=(40,), threshold=1.4)
    assert results[0]["projected_threshold_cycle"] > 40


def test_packaged_recomputation_and_bundle():
    assert len(recompute_from_packaged()) == 12
    assert validate_bundle()
