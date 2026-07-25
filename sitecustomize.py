"""Temporary UC-03 compatibility bootstrap.

This file is removed during UC-07 after every consumer uses canonical paths.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_PATHS = (
    _ROOT / "src/engine/packages",
    _ROOT / "src/engine/legacy/core",
    _ROOT / "src/engine/legacy/infrastructure/utils",
)
for _path in reversed(_PATHS):
    if _path.is_dir():
        _value = str(_path)
        if _value not in sys.path:
            sys.path.insert(0, _value)
