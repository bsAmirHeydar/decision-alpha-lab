def test_mql5_reference(repo_root):
 root=repo_root/"mql5/Include/StrategyFactory/LCM/V11B";text="\n".join(p.read_text(encoding="utf-8") for p in root.glob("*.mqh"));assert "ALV1::" in text;assert "RuntimeAuthority()const{return false;}" in text;assert "OrderSend(" not in text
