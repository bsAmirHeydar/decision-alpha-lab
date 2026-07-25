from pathlib import Path
def test_lcm11a_python_has_no_authority_tokens(repo_root:Path):
    root=repo_root/'src/engine/tooling/strategy_factory/lcm/lcm_11a'
    text='\n'.join(p.read_text(encoding='utf-8') for p in root.glob('*.py'))
    for token in ('OrderSend(', 'OrderSendAsync(', 'trade.Buy(', 'trade.Sell('):assert token not in text
