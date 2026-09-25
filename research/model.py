from __future__ import annotations
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def linear_threshold_projection(series, threshold=1.4, fraction=.60):
    series=sorted((int(x),float(y)) for x,y in series); n=max(10,int(len(series)*fraction)); tr=series[:n]
    mx=sum(x for x,_ in tr)/n; my=sum(y for _,y in tr)/n; den=sum((x-mx)**2 for x,_ in tr)
    slope=sum((x-mx)*(y-my) for x,y in tr)/den; intercept=my-slope*mx
    projected=(threshold-intercept)/slope; observed=next((x for x,y in series if y<=threshold),None)
    return {'train_n':n,'last_train_cycle':tr[-1][0],'slope':slope,'intercept':intercept,'projected_eol':projected,'observed_eol':observed}
def load_packaged():
    with (ROOT/'data/derived/primary_results.csv').open() as f:return list(csv.DictReader(f))
def load_summary():return json.loads((ROOT/'results/empirical_summary.json').read_text())
def validate_bundle():
    rows=load_packaged()
    for r in rows:
        if r['observed_first_cycle_le_1_4'] and int(r['training_last_cycle_first_60pct'])>=int(r['observed_first_cycle_le_1_4']): return False
    b7=next(r for r in rows if r['battery']=='B0007')
    return float(b7['last_capacity_ah'])>1.4 and float(b7['projected_eol_cycle_from_first_60pct'])<int(b7['n_cycles'])
