from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3];s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_23.json').read_text())
assert s['phase']=='SAED_V4_23' and s['status']=='accepted-reference' and s['real_alpha'] is False and s['production_authorization'] is False and s['promotion_authority'] is False and s['runtime_executable'] is False and s['metaeditor_compile']=='pending_local_windows'
print('V4-23 status validation passed')
