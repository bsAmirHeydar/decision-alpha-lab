#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);INC=ROOT/'mql5/Include/AlphaLab/StrategyFactory/Portfolio';EXP=ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics';files=sorted(INC.glob('*.mqh'))+sorted(EXP.glob('EXP_UCE_I17_*.mq5'));errors=[]
if len(files)<16:errors.append(f'expected at least 16 MQL5 files, found {len(files)}')
for p in files:
 text=p.read_text(errors='ignore')
 for token in ('OrderSend(', 'CTrade ', '.Buy(', '.Sell(', 'WebRequest(', 'PositionOpen('):
  if token in text:errors.append(f'{p.relative_to(ROOT)} contains forbidden {token}')
 if p.suffix=='.mq5' and '#property strict' not in text:errors.append(f'{p.relative_to(ROOT)} missing #property strict')
cat=(INC/'PortfolioCatalog.mqh').read_text();gate=(INC/'PortfolioAllocator.mqh').read_text()
for token in ('AL_PORTFOLIO_ORDER_AUTHORITY false','AL_PORTFOLIO_BROKER_AUTHORITY false','AL_PORTFOLIO_NETWORK_AUTHORITY false'):
 if token not in cat:errors.append(f'catalog missing {token}')
if 'selected_risk-reserved_risk' not in gate:errors.append('allocator mirror missing reservation parity gate')
if errors:print('\n'.join(errors));raise SystemExit(1)
print(f'UCE-I17 MQL5 static checks: PASS ({len(files)} files; MetaEditor compile not asserted)')
