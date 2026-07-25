from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from .canonical import digest_object


def _version(command: list[str]) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return "UNAVAILABLE"
    text = (result.stdout or result.stderr).strip().splitlines()
    return text[0] if text else "UNKNOWN"


def capture_environment() -> dict:
    value = {
        "schema_version": "1.0.0",
        "python_version": sys.version.split()[0],
        "python_implementation": platform.python_implementation(),
        "operating_system": platform.system(),
        "os_release": platform.release(),
        "machine": platform.machine(),
        "filesystem_encoding": sys.getfilesystemencoding(),
        "preferred_encoding": __import__("locale").getpreferredencoding(False),
        "git_version": _version(["git", "--version"]),
        "powershell_version": _version(["pwsh", "--version"]) if shutil.which("pwsh") else "UNAVAILABLE",
        "metaeditor_available": bool(shutil.which("metaeditor64") or shutil.which("metaeditor")),
        "mt5_runtime_available": False,
        "network_used": False,
        "secret_accessed": False,
        "environment_digest": "",
    }
    value["environment_digest"] = digest_object(value, "environment_digest")
    return value
