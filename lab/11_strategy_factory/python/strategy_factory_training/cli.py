from __future__ import annotations
import argparse,json
from dataclasses import asdict
from .examples import build_reference_training_bundle

def main()->int:
    parser=argparse.ArgumentParser(description="Decision Alpha Lab Phase 13 reference trainer")
    parser.add_argument("--demo",action="store_true",help="run deterministic in-memory reference training")
    args=parser.parse_args()
    if not args.demo:parser.error("use --demo for the reference workflow")
    result=build_reference_training_bundle()
    print(json.dumps({"dataset_hash":result[0].manifest.dataset_hash,"model_hash":result[3].model.artifact_hash,
                      "report_hash":result[3].report.report_hash,"prediction_count":len(result[3].predictions)},indent=2,sort_keys=True))
    return 0

if __name__=="__main__":raise SystemExit(main())
