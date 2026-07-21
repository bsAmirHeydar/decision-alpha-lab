"""LCM-09B canonical Setup migration and research-only Factory binding.

This package is intentionally fail-closed.  It never imports or executes legacy
Setup sources and it creates no promotion, runtime, order or capital authority.
"""
from .service import LCM09BSetupMigrationService
from .evaluator import CanonicalSetupEvaluator
from .factory_bridge import SetupFactoryReferencePort
__all__=["LCM09BSetupMigrationService","CanonicalSetupEvaluator","SetupFactoryReferencePort"]
