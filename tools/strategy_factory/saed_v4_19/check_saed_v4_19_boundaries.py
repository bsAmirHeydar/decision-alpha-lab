from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[3]
bases=[ROOT/'lab/11_strategy_factory/python/saed_v4_neurosymbolic_setup_reasoning',ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_19',ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_19']
text='\n'.join(f.read_text(encoding='utf-8') for b in bases for f in b.rglob('*') if f.is_file() and f.name!='check_saed_v4_19_boundaries.py' and f.suffix.lower() in {'.py','.mqh','.mq5'})
for token in ['eval(','exec(','compile(','__import__("subprocess")','OrderSend(','CTrade','PositionOpen(','WebRequest(','SocketCreate(']:assert token not in text,token
print('SAED V4-19 authority and dynamic-code boundary passed')
