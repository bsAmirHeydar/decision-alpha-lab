from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PLUG=ROOT/'mql5/Include/AlphaLab/StrategyFactory/Plugins'
HOST=ROOT/'mql5/Experts/StrategyFactory/SF04_StrategyHost.mq5'
errors=[]
required=['SF04_PluginDescriptor.mqh','SF04_DataRequirement.mqh','SF04_PluginRequirements.mqh','SF04_AnatomyEventQueue.mqh','ISF04_AnatomyPlugin.mqh','SF04_AnatomyPluginBase.mqh','SF04_PluginRegistry.mqh','SF04_PluginStartupValidator.mqh','SF04_AllPlugins.mqh']
for n in required:
 if not any(p.name==n for p in PLUG.rglob('*.mqh')):errors.append(f'missing {n}')
for p in list(PLUG.rglob('*.mqh'))+[HOST]:
 t=p.read_text(encoding='utf-8',errors='replace')
 for token in ('OrderSend(','OrderCheck(','CTrade','PositionOpen('):
  if token in t:errors.append(f'live authority token {token} in {p.relative_to(ROOT)}')
for p in PLUG.rglob('*.mqh'):
 if p.name!='SF04_FixturePulsePlugin.mqh':
  t=p.read_text(encoding='utf-8',errors='replace')
  for token in ('HookAfterF3','F3Locked','DivergenceStrength','ZoneInvalidation'):
   if token in t:errors.append(f'strategy-specific token {token} in {p.relative_to(ROOT)}')
if HOST.exists():
 t=HOST.read_text(encoding='utf-8',errors='replace')
 for token in ('HookAfterF3','F3Locked','DivergenceStrength','ZoneInvalidation'):
  if token in t:errors.append(f'host contains {token}')
# only phase03 terminal source may call terminal market APIs
allowed=ROOT/'mql5/Include/AlphaLab/StrategyFactory/Market/SF03_TerminalMarketSource.mqh'
for p in (ROOT/'mql5/Include/AlphaLab/StrategyFactory').rglob('*.mqh'):
 if p==allowed:continue
 t=p.read_text(encoding='utf-8',errors='replace')
 for pattern in (r'\bCopyRates\s*\(',r'\bSymbolInfoTick\s*\(',r'\bSymbolInfoDouble\s*\(',r'\bSymbolInfoInteger\s*\('):
  if re.search(pattern,t):errors.append(f'terminal market API outside owner: {p.relative_to(ROOT)}')
print(json.dumps({'phase':'SF04','errors':errors,'status':'PASS' if not errors else 'FAIL'},indent=2))
sys.exit(1 if errors else 0)
