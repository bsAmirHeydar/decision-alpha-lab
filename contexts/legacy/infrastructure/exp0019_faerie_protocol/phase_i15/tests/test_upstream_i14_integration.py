from tools.repository_paths import find_repository_root
from pathlib import Path
def test_i14_acceptance_artifact_exists():
 root=find_repository_root(__file__);p=root/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i14/artifacts/FP_I14_DIAGNOSTIC_ACCEPTANCE.json';assert p.exists()
def test_i09_file_index_exists():
 root=find_repository_root(__file__);assert (root/'releases/history/exp0019/indexes/EXP0019_FP_I09_FILE_INDEX.txt').exists()
