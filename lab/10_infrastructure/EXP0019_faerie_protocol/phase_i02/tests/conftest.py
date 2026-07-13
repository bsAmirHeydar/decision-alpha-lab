from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
PYROOT = ROOT / "lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02/python"
if str(PYROOT) not in sys.path:
    sys.path.insert(0, str(PYROOT))
