from __future__ import annotations
import json
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
rules_path = repo / "lab/11_strategy_factory/phase03_market/config/dependency_rules_v3.json"
rules = json.loads(rules_path.read_text(encoding="utf-8"))

market = repo / "mql5/Include/AlphaLab/StrategyFactory/Market"
allowed_terminal = market / "SF03_TerminalMarketSource.mqh"
violations: list[str] = []

terminal_tokens = tuple(rules["terminal_api_boundary"]["tokens"])
for path in market.glob("*.mqh"):
    text = path.read_text(encoding="utf-8")
    if path != allowed_terminal and any(token in text for token in terminal_tokens):
        violations.append(f"{path.relative_to(repo)}: terminal API outside terminal source")

phase_roots = [
    market,
    repo / "mql5/Experts/StrategyFactory/SF03_MarketServicesDiagnostic.mq5",
    repo / "mql5/Experts/StrategyFactoryTests/SF03_MarketServicesSelfTest.mq5",
]
for root in phase_roots:
    paths = [root] if root.is_file() else list(root.rglob("*"))
    for path in paths:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for token in rules["forbidden_authority_tokens"]:
            if token in text:
                violations.append(f"{path.relative_to(repo)}: forbidden authority token {token}")

strategy_words = ("Hook", "F3", "Divergence", "Hunter", "CleanSymbol", "Daye", "Astro", "ICT")
for path in market.glob("*.mqh"):
    text = path.read_text(encoding="utf-8")
    for word in strategy_words:
        if word in text:
            violations.append(f"{path.relative_to(repo)}: strategy-specific vocabulary {word}")

for item in violations:
    print(item)
if violations:
    raise SystemExit(1)
print("SF03 boundary guard: PASS")
