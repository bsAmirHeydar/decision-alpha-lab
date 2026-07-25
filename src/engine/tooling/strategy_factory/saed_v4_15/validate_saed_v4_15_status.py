from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__);s=json.loads((ROOT/'releases/history/strategy_factory/program/status/SAED_V4_15.json').read_text());assert s['phase']=='SAED_V4_15' and s['implementation_status']=='implemented_reference_synthetic';assert s['qa']['passed'];assert s['claims']['multimodal_fusion_boundary_implemented'] and not s['claims']['production_authorization'];assert s['external_evidence']['metaeditor_compile']=='pending_local_windows';print('SAED V4-15 phase status validated')
