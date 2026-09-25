from research.model import BATTERIES,CHECKPOINTS,THRESHOLD_AH,analyze_series,linear_threshold_projection,load_cycle_evidence,load_checkpoint_results,recompute_from_packaged,validate_bundle

def test_fixed_checkpoint_fixture():
    s=[(i,2.0-.005*i) for i in range(1,121)]
    z=linear_threshold_projection(s,40,1.4)
    assert z["checkpoint"]==40
    assert abs(z["projected_threshold_cycle"]-120)<1e-8

def test_complete_cycle_evidence():
    rows=load_cycle_evidence()
    assert len(rows)==636
    counts={b:sum(r["battery"]==b for r in rows) for b in BATTERIES}
    assert counts=={"B0005":168,"B0006":168,"B0007":168,"B0018":132}

def test_checkpoints_are_future_independent_and_before_observed_eol():
    rows=load_checkpoint_results()
    assert sorted({int(r["checkpoint_cycle"]) for r in rows})==list(CHECKPOINTS)
    for r in rows:
        if r["observed_threshold_cycle"]:
            assert int(r["checkpoint_cycle"])<int(r["observed_threshold_cycle"])

def test_exact_checkpoint_80_results():
    rows={(r["battery"],int(r["checkpoint_cycle"])):r for r in load_checkpoint_results()}
    expected={"B0005":145.025,"B0006":93.434,"B0007":158.219,"B0018":96.764}
    for b,p in expected.items():assert abs(float(rows[(b,80)]["projected_threshold_cycle"])-p)<0.002

def test_b0007_false_early_warning_only_at_80():
    rows={(r["battery"],int(r["checkpoint_cycle"])):r for r in load_checkpoint_results()}
    assert rows[("B0007",40)]["false_early_warning"]=="false"
    assert rows[("B0007",60)]["false_early_warning"]=="false"
    assert rows[("B0007",80)]["false_early_warning"]=="true"

def test_packaged_recomputation_and_bundle():
    assert len(recompute_from_packaged())==12
    assert validate_bundle()
