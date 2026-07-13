from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[5]
for rel in ('lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02/python','lab/10_infrastructure/EXP0019_faerie_protocol/phase_i03/python','lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/python','lab/10_infrastructure/EXP0019_faerie_protocol/phase_i05/python','lab/10_infrastructure/EXP0019_faerie_protocol/phase_i06/python','lab/10_infrastructure/EXP0019_faerie_protocol/phase_i07/python','lab/10_infrastructure/EXP0019_faerie_protocol/phase_i08/python'):
    p=str(ROOT/rel)
    if p not in sys.path:sys.path.insert(0,p)
