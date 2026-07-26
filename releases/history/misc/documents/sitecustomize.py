"""Compatibility bootstrap for the relocated historical documents tree.

The historical tree is intentionally retained as an archive.  When Python
loads this module from that tree, expose the repository root so archived tools
which use repository-relative imports remain importable without changing the
active package topology.
"""
from __future__ import annotations

import sys
from pathlib import Path


_REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))
