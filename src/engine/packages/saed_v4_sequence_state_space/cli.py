from pathlib import Path
import argparse,json
from .service import build_reference_bundle

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--root',default='.');p.add_argument('--out',required=True);a=p.parse_args(argv);r=Path(a.root)
    load=lambda x:json.loads((r/x).read_text(encoding='utf-8'))
    bundle,seq=build_reference_bundle(load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKEN_STREAMS.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKENIZER_SPEC.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON'),load('examples/legacy/strategy_factory/saed_v4_12/reference_sequence_spec.json'),load('examples/legacy/strategy_factory/saed_v4_12/reference_candidate_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_12/reference_reset_policy.json'))
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);(out/'bundle.json').write_text(json.dumps(bundle,indent=2,sort_keys=True)+'\n');(out/'sequences.json').write_text(json.dumps(seq,indent=2,sort_keys=True)+'\n');return 0
if __name__=='__main__':raise SystemExit(main())
