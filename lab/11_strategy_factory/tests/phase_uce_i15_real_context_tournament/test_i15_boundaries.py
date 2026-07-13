from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];PKG=ROOT/'lab/11_strategy_factory/python/strategy_factory_tournament_v3'
FORBIDDEN=('OrderSend(', 'CTrade', 'PositionOpen(', 'WebRequest(', 'requests.get(', 'requests.post(', 'urllib.request', 'socket.socket', 'subprocess.Popen', 'os.system(', 'eval(', 'exec(')
def test_no_execution_or_network_authority():
 for p in PKG.glob('*.py'):
  text=p.read_text()
  for token in FORBIDDEN:assert token not in text,f'{p.name}: {token}'
def test_fixture_cannot_be_real_evidence_token_present():
 assert 'fixture_not_real_data' in (PKG/'inventory.py').read_text();assert 'reference_fixture_not_confirmatory_real_data' in (PKG/'confirmatory.py').read_text()
