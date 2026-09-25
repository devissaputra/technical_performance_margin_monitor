from __future__ import annotations
import csv,json,statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
THRESHOLD_AH=1.4
CHECKPOINTS=(40,60,80)
BATTERIES=("B0005","B0006","B0007","B0018")

def linear_threshold_projection(series,checkpoint,threshold=THRESHOLD_AH):
    series=sorted((int(x),float(y)) for x,y in series)
    if checkpoint<2 or checkpoint>len(series):raise ValueError("invalid checkpoint")
    tr=series[:checkpoint];n=len(tr)
    mx=sum(x for x,_ in tr)/n;my=sum(y for _,y in tr)/n
    den=sum((x-mx)**2 for x,_ in tr)
    slope=sum((x-mx)*(y-my) for x,y in tr)/den
    intercept=my-slope*mx
    projected=(threshold-intercept)/slope if slope<0 else None
    return {"checkpoint":checkpoint,"slope":slope,"intercept":intercept,"projected_threshold_cycle":projected,"last_observed_capacity":tr[-1][1]}

def first_crossing(series,threshold=THRESHOLD_AH):
    return next((int(x) for x,y in sorted(series) if float(y)<=threshold),None)

def analyze_series(series,checkpoints=CHECKPOINTS,threshold=THRESHOLD_AH):
    series=sorted((int(x),float(y)) for x,y in series)
    observed=first_crossing(series,threshold);last_cycle=series[-1][0];out=[];prev=None
    for cp in checkpoints:
        z=linear_threshold_projection(series,cp,threshold);p=z["projected_threshold_cycle"]
        error=None if observed is None or p is None else p-observed
        revision=None if prev is None or p is None else abs(p-prev)
        within=p is not None and p<=last_cycle
        out.append({**z,"observed_threshold_cycle":observed,"projection_error_cycles":error,"forecast_revision_cycles":revision,"projection_within_observed_horizon":within,"false_early_warning":bool(observed is None and within)})
        prev=p
    return out

def load_cycle_evidence():
    with (ROOT/"data/derived/cycle_capacity_evidence.csv").open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def load_checkpoint_results():
    with (ROOT/"data/derived/checkpoint_results.csv").open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def load_summary():
    return json.loads((ROOT/"results/empirical_summary.json").read_text(encoding="utf-8"))

def recompute_from_packaged():
    rows=load_cycle_evidence();by={}
    for b in BATTERIES:
        by[b]=[(int(r["discharge_cycle"]),float(r["capacity_ah"])) for r in rows if r["battery"]==b]
    out=[]
    for b in BATTERIES:
        for z in analyze_series(by[b]):
            out.append((b,z))
    return out

def validate_bundle():
    rows=load_cycle_evidence()
    if len(rows)!=636:return False
    recomputed=recompute_from_packaged()
    packaged={(r["battery"],int(r["checkpoint_cycle"])):r for r in load_checkpoint_results()}
    for b,z in recomputed:
        r=packaged[(b,z["checkpoint"])]
        if abs(float(r["projected_threshold_cycle"])-z["projected_threshold_cycle"])>0.0015:return False
        if r["observed_threshold_cycle"]:
            if int(r["observed_threshold_cycle"])!=z["observed_threshold_cycle"]:return False
            if int(r["checkpoint_cycle"])>=z["observed_threshold_cycle"]:return False
        if (r["false_early_warning"].lower()=="true")!=z["false_early_warning"]:return False
    s=load_summary()["headline_metrics"]
    return s["n_discharge_cycles"]==636 and s["eol_threshold_ah"]==1.4 and s["b0007_false_early_warning_at_80"] is True
