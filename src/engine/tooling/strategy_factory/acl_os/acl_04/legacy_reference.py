from __future__ import annotations
from pathlib import Path
from src.engine.tooling.strategy_factory.lcm.lcm_09b.factory_bridge import SetupFactoryReferencePort

def open_legacy_reference_port(registration_path:Path)->SetupFactoryReferencePort:
    """Open a read-only reference registry. No candidate compilation is performed."""
    return SetupFactoryReferencePort(registration_path)
