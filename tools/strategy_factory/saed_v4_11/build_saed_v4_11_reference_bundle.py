from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_self_supervised_pretraining.cli import main
raise SystemExit(main())
