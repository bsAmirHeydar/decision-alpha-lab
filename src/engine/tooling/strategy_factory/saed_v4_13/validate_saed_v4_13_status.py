from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__);s=json.loads((ROOT/'releases/history/strategy_factory/program/status/SAED_V4_13.json').read_text());assert s['implementation_status']=='implemented_reference_synthetic';assert s['authority']['decision_authority'] is False and s['authority']['execution_authority'] is False;assert s['external_evidence']['metaeditor_compile']=='pending_local_windows';print('SAED V4-13 status boundary passed')
