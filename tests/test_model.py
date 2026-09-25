from research.model import linear_threshold_projection,validate_bundle,load_packaged
def test_projection_fixture():
    series=[(i,2.0-.01*i) for i in range(1,101)]; z=linear_threshold_projection(series,1.4,.6); assert z['last_train_cycle']==60; assert abs(z['projected_eol']-60)<1e-8
def test_no_eol_leakage_in_packaged_cells():
    for r in load_packaged():
        if r['observed_first_cycle_le_1_4']: assert int(r['training_last_cycle_first_60pct']) < int(r['observed_first_cycle_le_1_4'])
def test_b0007_false_early_prediction_and_bundle(): assert validate_bundle()
