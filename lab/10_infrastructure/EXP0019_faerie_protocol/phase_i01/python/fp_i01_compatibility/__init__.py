"""FP-I01 Shared-Core Compatibility Harness and Adapter Contracts."""
from .adapters import *
from .models import *
from .registry import CATALOG, default_registry
from .differential import run_all_fixtures
__version__='1.0.0'
