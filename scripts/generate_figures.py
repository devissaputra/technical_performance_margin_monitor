#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,html
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]

def t(x,y,s,z=16,w="400",a="start"):return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{z}" font-weight="{w}" text-anchor="{a}">{html.escape(str(s))}</text>'
def o(w,h):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="white"/>'
def checkpoints():
    with (ROOT/"data/derived/checkpoint_results.csv").open() as f:return list(csv.DictReader(f))
def aggregates():
    with (ROOT/"data/derived/checkpoint_aggregate.csv").open() as f:return list(csv.DictReader(f))

def architecture():
    p=[o(1200,420),t(45,50,"Technical Performance Margin — Forecast Maturity",28,"700"),t(45,82,"Official NASA source → fixed checkpoints → threshold projection → revision/error → decision boundary",15)]
    labs=[("NASA cells","B0005/6/7/18"),("Checkpoint","40 / 60 / 80"),("Forecast","linear crossing"),("Maturity","revision + error"),("Decision","bounded warning")]
    for i,(a,b) in enumerate(labs):
        x=35+i*232;p+=[f'<rect x="{x}" y="145" width="185" height="120" rx="12" fill="#f7f7f7" stroke="#333"/>',t(x+92,y=185,s=a,z=17,w="700",a="middle"),t(x+92,y=218,s=b,z=14,a="middle")]
        if i<4:p.append(f'<line x1="{x+185}" y1="205" x2="{x+222}" y2="205" stroke="#222" stroke-width="2"/>')
    return "".join(p+["</svg>"])

def method():
    steps=["Observe capacity only through a fixed cycle checkpoint.","Compute current margin to NASA's 1.4 Ah EOL boundary.","Fit a transparent linear trend using available cycles only.","Project threshold timing; track error and revision as evidence accumulates."]
    p=[o(1200,520),t(45,50,"Fixed-checkpoint monitoring method",28,"700")]
    for i,s in enumerate(steps,1):
        y=105+(i-1)*95;p+=[f'<circle cx="75" cy="{y+30}" r="23" fill="#f0f0f0" stroke="#333"/>',t(75,y+36,i,16,"700","middle"),f'<rect x="120" y="{y}" width="1020" height="62" rx="10" fill="#fafafa" stroke="#444"/>',t(145,y+38,s,15)]
    return "".join(p+["</svg>"])

def checkpoint_error():
    rows=aggregates();p=[o(1050,560),t(40,45,"Threshold-cycle error falls as evidence accumulates",26,"700"),t(40,72,"MAE across B0005, B0006, and B0018; B0007 has no observed 1.4 Ah crossing.",14)]
    maxv=max(float(r["mae_cycles_crossing_cells"]) for r in rows);base=455
    for i,r in enumerate(rows):
        v=float(r["mae_cycles_crossing_cells"]);x=150+i*280;h=330*v/maxv;y=base-h
        p+=[f'<rect x="{x}" y="{y}" width="150" height="{h}" fill="#555" fill-opacity="0.72"/>',t(x+75,y-12,f"{v:.1f}",16,"700","middle"),t(x+75,base+28,f'Cycle {r["checkpoint_cycle"]}',14,"700","middle")]
    return "".join(p+["</svg>"])

def revision():
    rows=[r for r in aggregates() if r["mean_forecast_revision_cycles"]];p=[o(1050,520),t(40,45,"Forecast revision remains a material monitoring signal",26,"700"),t(40,72,"Mean absolute change in projected threshold cycle across four cells.",14)]
    for i,r in enumerate(rows):
        v=float(r["mean_forecast_revision_cycles"]);x=190+i*390;w=v*5.5
        label="40→60" if r["checkpoint_cycle"]=="60" else "60→80"
        p+=[t(80,185+i*150,label,16,"700"),f'<rect x="190" y="{155+i*150}" width="{w}" height="55" fill="#666" fill-opacity="{0.75-i*0.12}"/>',t(200+w,190+i*150,f"{v:.1f} cycles",15,"700")]
    return "".join(p+["</svg>"])

def evaluation():
    p=[o(1200,500),t(45,50,"Evidence boundary",28,"700")]
    blocks=[("What improves","Fixed checkpoints remove dependence on eventual recorded lifetime."),("What remains hard","Individual linear forecasts can still revise by tens or hundreds of cycles."),("Concrete warning","B0007 projects 158.2 cycles at checkpoint 80 but stays above 1.4 Ah through cycle 168."),("Claim limit","Transparent baseline on four lab cells; not production BMS or general RUL validation.")]
    for i,(a,b) in enumerate(blocks):
        y=90+i*92;p+=[f'<rect x="55" y="{y}" width="1090" height="68" rx="10" fill="#f8f8f8" stroke="#444"/>',t(80,y+27,a,16,"700"),t(80,y+51,b,14)]
    return "".join(p+["</svg>"])

def render(out):
    out.mkdir(parents=True,exist_ok=True);fs={"architecture.svg":architecture(),"method.svg":method(),"checkpoint_error.svg":checkpoint_error(),"forecast_revision.svg":revision(),"evaluation.svg":evaluation()}
    for n,c in fs.items():ET.fromstring(c);(out/n).write_text(c,encoding="utf-8")
    return fs
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out-dir",default=str(ROOT/"assets"));a=ap.parse_args();print("generated_figures:",len(render(Path(a.out_dir))))
if __name__=="__main__":main()
