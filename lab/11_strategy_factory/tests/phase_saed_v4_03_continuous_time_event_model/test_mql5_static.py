from pathlib import Path

def test_mql5_static(root):
    files=list((root/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4EventModel').glob('*.mqh'))+list((root/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics').glob('EXP_SAED_V4_03_*.mq5'));assert len(files)==13
    text="\n".join(p.read_text(errors='ignore') for p in files)
    for token in ['OrderSend','CTrade','WebRequest','SocketCreate','PositionOpen']:assert token not in text
    for required in ['SAED_EVENT_ORDER_AUTHORITY false','SAED_EVENT_BROKER_AUTHORITY false','SAED_EVENT_NETWORK_AUTHORITY false']:assert required in text
