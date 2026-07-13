from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[5]
for rel in (
 'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02/python',
 'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i03/python',
 'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/python',
):
    p=ROOT/rel
    if str(p) not in sys.path:sys.path.insert(0,str(p))
