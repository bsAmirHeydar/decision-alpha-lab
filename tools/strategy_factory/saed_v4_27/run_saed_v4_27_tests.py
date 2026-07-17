from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[3]
raise SystemExit(pytest.main(["-q",str(ROOT/"lab/11_strategy_factory/tests/phase_saed_v4_27_complete_search_exposure_ledger")]))
