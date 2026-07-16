from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[3];pkg=ROOT/'lab/11_strategy_factory/python/saed_v4_generative_path_stress_lab';forbidden=[r'OrderSend\s*\(',r'from\s+MetaTrader',r'import\s+MetaTrader',r'production_authority\s*[=:]\s*True',r'runtime_executable\s*[=:]\s*True']
for p in pkg.glob('*.py'):
    t=p.read_text(encoding='utf-8')
    for pat in forbidden:assert not re.search(pat,t,re.I),(p.name,pat)
print(json.dumps({'passed':True,'authority_boundary':'research_only','central_engine_mutation':False},sort_keys=True))
