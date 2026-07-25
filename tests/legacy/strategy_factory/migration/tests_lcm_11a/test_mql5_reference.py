def test_mql5_reference_is_namespace_only(repo_root):
    root=repo_root/'mql5/Include/StrategyFactory/LCM/V11A'
    files=list(root.glob('*.mqh'));assert len(files)>=4
    text='\n'.join(p.read_text(encoding='utf-8') for p in files)
    assert 'ALV1::' in text
    assert 'OrderSend(' not in text
    assert 'ObjectCreate(' not in text
