"""Repository-local launcher for the Strategy Factory CLI."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
PYTHON_ROOT = ROOT / "python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

from strategy_factory.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
