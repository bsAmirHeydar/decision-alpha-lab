"""UCE-I16 deterministic context onboarding and legacy migration factory."""
from .contracts import *
from .generator import ContextGenerator
from .adapters import LegacyAdapter,measure_parity
from .invariance import snapshot,compare
from .waves import build_wave
from .migration import execute_wave
__version__='1.0.0'
