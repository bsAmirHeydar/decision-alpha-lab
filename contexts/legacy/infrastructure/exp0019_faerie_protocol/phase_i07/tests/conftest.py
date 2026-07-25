from tools.repository_paths import find_repository_root
from pathlib import Path
import sys
ROOT=find_repository_root(__file__)
for rel in ('contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i02/python','contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i03/python','contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i04/python','contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i05/python','contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i06/python','contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i07/python'):
    p=str(ROOT/rel)
    if p not in sys.path:sys.path.insert(0,p)
