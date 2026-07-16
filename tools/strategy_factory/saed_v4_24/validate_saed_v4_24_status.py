from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[3]
status = json.loads((ROOT / 'lab/11_strategy_factory/phase_status/SAED_V4_24.json').read_text())
assert status['phase'] == 'SAED_V4_24' and status['status'] == 'accepted_reference' and status['qa_passed']
assert not any((status['real_alpha'], status['promotion_authority'], status['runtime_executable'], status['risk_allocation_authority'], status['execution_authority'], status['production_authorization']))
assert status['metaeditor_compile'] == 'pending_local_windows'
print('V4-24 status validation passed')
