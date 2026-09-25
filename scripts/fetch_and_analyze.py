#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,io,json,sys,urllib.request,zipfile
from pathlib import Path
import numpy as np
from scipy.io import loadmat

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from research.model import BATTERIES,CHECKPOINTS,THRESHOLD_AH,analyze_series

NASA_URL="https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip"
EXPECTED_ARCHIVE_SHA256="82302a7db4fc1b34e0b6676326610438d43b816bdf11a69d1d012a464ef2f92e"

def nested_mats(blob):
    wanted={f"{b}.mat" for b in BATTERIES};found={}
    def visit(zbytes):
        with zipfile.ZipFile(io.BytesIO(zbytes)) as z:
            for name in z.namelist():
                base=Path(name).name
                if base in wanted and base not in found:found[base]=z.read(name)
                elif name.lower().endswith(".zip"):
                    try:visit(z.read(name))
                    except zipfile.BadZipFile:pass
    visit(blob)
    missing=wanted-set(found)
    if missing:raise RuntimeError(f"Missing NASA MAT files: {sorted(missing)}")
    return found

def extract_capacity(mat_bytes,battery):
    data=loadmat(io.BytesIO(mat_bytes),squeeze_me=True,struct_as_record=False)
    obj=data[battery];out=[];idx=0
    for cycle in np.atleast_1d(obj.cycle):
        if str(cycle.type).strip().lower()!="discharge":continue
        d=cycle.data
        if not hasattr(d,"Capacity"):continue
        idx+=1;cap=float(np.asarray(d.Capacity).squeeze())
        out.append((idx,cap))
    return out

def packaged_cycles():
    with (ROOT/"data/derived/cycle_capacity_evidence.csv").open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def packaged_checkpoints():
    with (ROOT/"data/derived/checkpoint_results.csv").open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true");args=ap.parse_args()
    payload=urllib.request.urlopen(NASA_URL,timeout=120).read();sha=hashlib.sha256(payload).hexdigest()
    print("NASA archive sha256:",sha)
    if EXPECTED_ARCHIVE_SHA256 and sha!=EXPECTED_ARCHIVE_SHA256:raise SystemExit("FAIL: NASA archive SHA-256 changed")
    mats=nested_mats(payload);rebuilt={}
    for b in BATTERIES:rebuilt[b]=extract_capacity(mats[f"{b}.mat"],b)
    print("cycles:",{b:len(v) for b,v in rebuilt.items()})
    if args.check:
        packaged=packaged_cycles()
        for b in BATTERIES:
            expected=[r for r in packaged if r["battery"]==b]
            got=rebuilt[b]
            if len(expected)!=len(got):raise SystemExit(f"FAIL: cycle count mismatch for {b}")
            for r,(idx,cap) in zip(expected,got):
                if int(r["discharge_cycle"])!=idx or abs(float(r["capacity_ah"])-cap)>1e-9:raise SystemExit(f"FAIL: NASA capacity mismatch for {b} cycle {idx}")
        cp={(r["battery"],int(r["checkpoint_cycle"])):r for r in packaged_checkpoints()}
        for b in BATTERIES:
            for z in analyze_series(rebuilt[b]):
                r=cp[(b,z["checkpoint"])]
                if abs(float(r["projected_threshold_cycle"])-z["projected_threshold_cycle"])>0.0015:raise SystemExit(f"FAIL: checkpoint projection mismatch {b}/{z['checkpoint']}")
        print("official_nasa_rebuild: PASS")
    else:
        for b in BATTERIES:print(b,analyze_series(rebuilt[b]))

if __name__=="__main__":main()
