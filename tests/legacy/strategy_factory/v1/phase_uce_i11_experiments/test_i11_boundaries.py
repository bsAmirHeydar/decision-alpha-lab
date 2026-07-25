from tools.repository_paths import find_repository_root
from pathlib import Path

ROOT = find_repository_root(__file__)
PACKAGE = ROOT / "lab" / "11_strategy_factory" / "python" / "strategy_factory_experiments_v3"


def test_experiment_package_has_no_order_broker_or_network_authority():
    forbidden = (
        "OrderSend(",
        "trade.Buy(",
        "trade.Sell(",
        "requests.get(",
        "requests.post(",
        "urllib.request",
        "socket.socket",
        "subprocess.Popen",
        "os.system(",
    )
    text = "\n".join(path.read_text(encoding="utf-8") for path in PACKAGE.glob("*.py"))
    for token in forbidden:
        assert token not in text


def test_hidden_test_role_is_not_hardcoded_into_search_or_scheduler_modules():
    for name in ("search.py", "scheduler.py", "budget.py", "cache.py"):
        text = (PACKAGE / name).read_text(encoding="utf-8")
        assert "final_test" not in text
        assert "hidden_test" not in text
