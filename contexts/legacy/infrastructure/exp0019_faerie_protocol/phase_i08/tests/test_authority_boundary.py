from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_python_has_no_broker_order_network_authority():
 forbidden=('OrderSend','CTrade','requests.','urllib.request','socket.','WebRequest(','ObjectCreate(','PositionSelect(')
 text='\n'.join(p.read_text(errors='ignore') for p in (ROOT/'python').rglob('*.py'))
 assert not [x for x in forbidden if x in text]
