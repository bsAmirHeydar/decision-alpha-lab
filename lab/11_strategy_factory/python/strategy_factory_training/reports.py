from __future__ import annotations
from dataclasses import asdict
from enum import IntEnum
from pathlib import Path
import json,csv

def _plain(value):
    if isinstance(value,IntEnum):return int(value)
    if isinstance(value,tuple):return [_plain(v) for v in value]
    if isinstance(value,list):return [_plain(v) for v in value]
    if isinstance(value,dict):return {k:_plain(v) for k,v in value.items()}
    return value

def write_training_bundle(path,bundle,dataset_manifest,training_plan)->dict[str,str]:
    root=Path(path);root.mkdir(parents=True,exist_ok=True)
    artifacts={
      "dataset_manifest.json":dataset_manifest,
      "training_plan.json":training_plan,
      "transform_state.json":bundle.transform,
      "model_artifact.json":bundle.model,
      "calibration_artifact.json":bundle.calibration,
      "model_card.json":bundle.card,
      "training_report_manifest.json":bundle.report,
    }
    for name,value in artifacts.items():
        (root/name).write_text(json.dumps(_plain(asdict(value)),indent=2,sort_keys=True)+"\n",encoding="utf-8")
    with (root/"predictions.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(asdict(bundle.predictions[0]).keys()));writer.writeheader()
        for prediction in bundle.predictions:writer.writerow(_plain(asdict(prediction)))
    return {name:str(root/name) for name in (*artifacts,"predictions.csv")}
