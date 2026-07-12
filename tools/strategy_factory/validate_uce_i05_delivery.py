from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
required=['mql5/Include/AlphaLab/StrategyFactory/Economics/UCEI05_All.mqh','lab/11_strategy_factory/python/strategy_factory_economics_v3/solver.py','lab/11_strategy_factory/test_vectors/v3/uce_i05_economic_vectors.json','docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i05/00_UCE_I05_DELIVERY_MOC.md','lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I05.json']
missing=[x for x in required if not (root/x).exists()]
if missing: print('missing:',*missing,sep='\n'); raise SystemExit(1)
status=json.loads((root/required[-1]).read_text()); assert status['phase_id']=='UCE-I05' and status['status']=='implemented'
print('UCE-I05 delivery validation PASS')
