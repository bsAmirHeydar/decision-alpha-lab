from tools.repository_paths import find_repository_root
from pathlib import Path
import sys

ROOT = find_repository_root(__file__)
for relative in (
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i02/python",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i03/python",
):
    path = ROOT / relative
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
