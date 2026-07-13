from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[5]
PKG=ROOT/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/python'
if str(PKG) not in sys.path:sys.path.insert(0,str(PKG))
