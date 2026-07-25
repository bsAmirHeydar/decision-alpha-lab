"""LCM-08B pilot context migration package."""
from .context_core import ContextConfig, detect_occurrences
from .legacy_adapter import run_legacy_compatible
__all__=["ContextConfig","detect_occurrences","run_legacy_compatible"]
