import json
from saed_v4_context_twin.cli import main

def test_cli_compile(tmp_path,root):
    out=tmp_path/'manifest.json'
    rc=main(['compile','--context-spec',str(root/'lab/11_strategy_factory/examples/saed_v4_02/golden_context_specification.json'),'--seed',str(root/'lab/11_strategy_factory/examples/saed_v4_02/golden_twin_seed.json'),'--output',str(out)])
    assert rc==0 and len(json.loads(out.read_text())['semantic_hash'])==64

def test_cli_deterministic(tmp_path,root):
    args=['compile','--context-spec',str(root/'lab/11_strategy_factory/examples/saed_v4_02/golden_context_specification.json'),'--seed',str(root/'lab/11_strategy_factory/examples/saed_v4_02/golden_twin_seed.json')]
    a=tmp_path/'a';b=tmp_path/'b';main(args+['--output',str(a)]);main(args+['--output',str(b)]);assert a.read_bytes()==b.read_bytes()
