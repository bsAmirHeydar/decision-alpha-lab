from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
required=['mql5/Include/AlphaLab/StrategyFactory/Economics/UCEI05_All.mqh','src/engine/packages/strategy_factory_economics_v3/solver.py','tests/fixtures/legacy/strategy_factory/v3/uce_i05_economic_vectors.json','docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i05/00_UCE_I05_DELIVERY_MOC.md','releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I05.json']
missing=[x for x in required if not (root/x).exists()]
if missing: print('missing:',*missing,sep='\n'); raise SystemExit(1)
status=json.loads((root/required[-1]).read_text()); assert status['phase_id']=='UCE-I05' and status['status']=='implemented'
print('UCE-I05 delivery validation PASS')
