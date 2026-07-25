from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__);s=json.loads((ROOT/'releases/history/strategy_factory/program/status/SAED_V4_23.json').read_text())
assert s['phase']=='SAED_V4_23' and s['status']=='accepted-reference' and s['real_alpha'] is False and s['production_authorization'] is False and s['promotion_authority'] is False and s['runtime_executable'] is False and s['metaeditor_compile']=='pending_local_windows'
print('V4-23 status validation passed')
