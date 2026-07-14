from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
INC=ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4DataFoundation';EXP=ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics'
FILES=sorted(INC.glob('*.mqh'))+sorted(EXP.glob('EXP_SAED_V4_01_*.mq5'))
def test_expected_mql5_file_count(): assert len(FILES)==13
def test_no_execution_or_network_tokens():
 forbidden=['OrderSend','CTrade','WebRequest','SocketCreate','PositionOpen','trade.Buy','trade.Sell']
 for p in FILES:
  text=p.read_text(encoding='utf-8')
  for token in forbidden: assert token not in text,(p,token)
def test_authority_constants_false():
 text=(INC/'DataFoundationCatalog.mqh').read_text()
 for name in ['ORDER','BROKER','NETWORK','CONTEXT_MUTATION','RUNTIME_ACTIVATION','RISK','PORTFOLIO']: assert f'AL_SAED_V4_DATA_{name}_AUTHORITY false' in text
def test_all_include_references_modules():
 text=(INC/'DataFoundationAll.mqh').read_text()
 for name in ['Catalog','Enums','Contracts','Temporal','RoleGate','Revision','Snapshot','Integrity','TwinSeed']: assert f'DataFoundation{name}.mqh' in text
