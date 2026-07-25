"""Capture a sanitized, reproducible environment and toolchain manifest."""
from __future__ import annotations

import importlib.metadata
import os
import platform
import shutil
import sys
from pathlib import Path

from .git_utils import git_metadata, run_command


_COMMANDS = {
    "git": ("git", "--version"),
    "git_lfs": ("git", "lfs", "version"),
    "python": (sys.executable, "--version"),
    "pytest": (sys.executable, "-m", "pytest", "--version"),
    "pip": (sys.executable, "-m", "pip", "--version"),
}


def capture_environment(repo_root: Path) -> dict:
    commands = {}
    for name, command in _COMMANDS.items():
        result = run_command(command, repo_root, timeout=30)
        commands[name] = {
            "command": list(command),
            "returncode": result.returncode,
            "output": result.stdout.strip()[:4000],
        }
    packages = []
    try:
        for dist in importlib.metadata.distributions():
            name = dist.metadata.get("Name") or dist.metadata.get("Summary") or "unknown"
            packages.append({"name": str(name), "version": dist.version})
    except Exception:
        packages = []
    packages.sort(key=lambda x: (x["name"].lower(), x["version"]))
    executables = {}
    for name in ("metaeditor64.exe", "terminal64.exe", "MetaEditor64.exe", "Terminal64.exe"):
        resolved = shutil.which(name)
        if resolved:
            executables[name] = str(Path(resolved).resolve())
    safe_env_names = (
        "OS", "PROCESSOR_ARCHITECTURE", "NUMBER_OF_PROCESSORS", "COMSPEC", "SHELL",
        "LANG", "LC_ALL", "TZ", "VIRTUAL_ENV", "CONDA_DEFAULT_ENV", "PYTHONHASHSEED",
    )
    return {
        "python": {
            "version": sys.version,
            "executable": sys.executable,
            "implementation": platform.python_implementation(),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "commands": commands,
        "packages": packages,
        "git": git_metadata(repo_root),
        "safe_environment": {name: os.environ.get(name) for name in safe_env_names if os.environ.get(name) is not None},
        "detected_terminal_executables": executables,
        "secrets_copied": False,
    }
