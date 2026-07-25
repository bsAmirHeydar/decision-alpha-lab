from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_mql5_static_boundary():
 files=list((ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4MultimodalViews').glob('*.mqh'))+list((ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics').glob('EXP_SAED_V4_04_*.mq5'))
 assert len(files)==14
 text='\n'.join(p.read_text() for p in files)
 for forbidden in ['OrderSend(','CTrade','WebRequest(','SocketCreate(','PositionOpen(']:assert forbidden not in text
 for required in ['SAED_VIEW_ORDER_AUTHORITY false','SAED_VIEW_BROKER_AUTHORITY false','SAED_VIEW_NETWORK_AUTHORITY false','SAED_VIEW_TRAIN_MODEL_AUTHORITY false']:assert required in text
