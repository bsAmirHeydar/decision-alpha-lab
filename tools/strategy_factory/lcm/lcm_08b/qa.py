from __future__ import annotations
import ast,json,re
from pathlib import Path
from .verify import verify_package
from .errors import VerificationError

FORBIDDEN=("OrderSend","CTrade",".Buy(",".Sell(","PositionOpen","PositionModify","PositionClose","ObjectCreate","ObjectSet","ChartRedraw")

def run(repo_root:Path,pilot_root:Path):
    result=verify_package(pilot_root)
    module_root=repo_root/'tools/strategy_factory/lcm/lcm_08b'
    py_files=sorted(module_root.glob('*.py'))
    for p in py_files:ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    adapter=(module_root/'legacy_adapter.py').read_text(encoding='utf-8')
    hits=[x for x in FORBIDDEN if x in adapter]
    if hits:raise VerificationError(f'forbidden adapter APIs: {hits}')
    phase_doc=repo_root/'docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/05_PHASES/LCM_08B_PILOT_CONTEXT_MIGRATION_COMPATIBILITY_ADAPTER_AND_BEHAVIORAL_PARITY.md'
    if 'status: accepted-reference' not in phase_doc.read_text(encoding='utf-8'):raise VerificationError('phase status not accepted-reference')
    return {**result,"python_file_count":len(py_files),"forbidden_adapter_api_hits":0,"qa_passed":True}
