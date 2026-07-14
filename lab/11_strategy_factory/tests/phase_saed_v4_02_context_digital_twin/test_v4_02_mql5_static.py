from pathlib import Path

def test_mql5_files(root):
    files = list((root/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4ContextTwin').glob('*.mqh'))
    files += list((root/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics').glob('EXP_SAED_V4_02_*.mq5'))
    assert len(files) >= 12
    text = '\n'.join(p.read_text(errors='ignore') for p in files).lower()
    for token in ['ordersend','ctrade','webrequest','socketcreate','positionopen']:
        assert token not in text
    for token in ['twin','context','authority']:
        assert token in text
