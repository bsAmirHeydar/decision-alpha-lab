from tools.repository_paths import find_repository_root
def test_artifact_set(load):
 import pathlib
 root=pathlib.find_repository_root(__file__);files=list((root/'releases/history/strategy_factory/artifacts/saed_v4_11').glob('*.JSON'));assert len(files)>=28
def test_checkpoint_card_prohibitions(load):assert 'order placement' in load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_CHECKPOINT_CARD.JSON')['prohibited_uses']
def test_sbom_no_network(load):assert not load('releases/history/strategy_factory/artifacts/saed_v4_11/SBOM.JSON')['external_network_required']
def test_rejected_ledger(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_11/REJECTED_CHECKPOINT_LEDGER.JSON')['entry_count']==2
def test_telemetry_admission(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_TELEMETRY.JSON')['reference_checkpoint_admitted']
