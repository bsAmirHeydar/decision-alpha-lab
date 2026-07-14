from pathlib import Path
from dataclasses import asdict
import json, sys
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_context_twin.compiler import compile_twin
from saed_v4_context_twin.state import build_snapshot
from saed_v4_context_twin.integrity import build_receipt
from saed_v4_context_twin.handoff import build_v4_03_handoff

example_root = ROOT/'lab/11_strategy_factory/examples/saed_v4_02'
context_spec = json.loads((example_root/'golden_context_specification.json').read_text())
seed = json.loads((example_root/'golden_twin_seed.json').read_text())
manifest = compile_twin(context_spec, seed)
snapshot = build_snapshot(
    manifest, seed['known_as_of'], manifest.initial_lifecycle_state,
    (), (), None, (), (), (), 1,
)
receipt = build_receipt(manifest, snapshot)
out = ROOT/'lab/11_strategy_factory/artifacts/saed_v4_02'
out.mkdir(parents=True, exist_ok=True)

def dump(name, payload):
    (out/name).write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n', encoding='utf-8')

dump('GOLDEN_TWIN_MANIFEST.json', {**manifest.semantic_payload(), 'semantic_hash': manifest.semantic_hash})
dump('GOLDEN_TWIN_SNAPSHOT.json', {
    **asdict(snapshot),
    'twin_state': snapshot.twin_state.value,
    'hypothesis_states': [],
})
dump('GOLDEN_TWIN_RECEIPT.json', {**asdict(receipt), 'receipt_id': receipt.receipt_id})
dump('V4_02_TO_V4_03_HANDOFF.json', build_v4_03_handoff(manifest, snapshot, receipt, ['No event model yet']))
print(manifest.twin_id, manifest.semantic_hash, snapshot.snapshot_hash)
