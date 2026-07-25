from tools.repository_paths import find_repository_root
from pathlib import Path
import sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_self_supervised_pretraining.cli import main
raise SystemExit(main())
