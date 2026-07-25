from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT = find_repository_root(__file__)
status = json.loads((ROOT / 'releases/history/strategy_factory/program/status/SAED_V4_24.json').read_text())
assert status['phase'] == 'SAED_V4_24' and status['status'] == 'accepted_reference' and status['qa_passed']
assert not any((status['real_alpha'], status['promotion_authority'], status['runtime_executable'], status['risk_allocation_authority'], status['execution_authority'], status['production_authorization']))
assert status['metaeditor_compile'] == 'pending_local_windows'
print('V4-24 status validation passed')
