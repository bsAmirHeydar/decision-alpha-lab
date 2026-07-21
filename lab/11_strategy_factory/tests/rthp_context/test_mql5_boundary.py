from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]/'mql5/Include/AlphaLab/StrategyFactory/ContextPackage/RTHP'
def test_no_order_api():
 text="\n".join(p.read_text(errors="ignore") for p in ROOT.glob("*.mqh"));assert "OrderSend(" not in text and "CTrade" not in text


def test_acl03_static_mirror_is_non_trading():
 p=ROOT/'RTHP_ACL03_StaticMirror.mqh';text=p.read_text(errors='ignore');assert 'PENDING_GENERATION' not in text;assert 'OrderSend(' not in text and 'CTrade' not in text;assert 'CONTEXT_COMPILATION_REFERENCE_ONLY' in text
