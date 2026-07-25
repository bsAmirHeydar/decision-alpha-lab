from tools.repository_paths import find_repository_root
from pathlib import Path
import pytest
ROOT=find_repository_root(__file__)
raise SystemExit(pytest.main(["-q",str(ROOT/"tests/legacy/strategy_factory/v1/phase_saed_v4_27_complete_search_exposure_ledger")]))
