"""ACL-00 Constitution and Unified Authority reference implementation.

The package is intentionally free of trading and capital activation authority.  It
only evaluates lifecycle governance decisions and emits tamper-evident evidence.
"""
from .service import ACL00ControlPlane, EvaluationBundle
from .types import Decision, LifecycleState

__all__ = ["ACL00ControlPlane", "EvaluationBundle", "Decision", "LifecycleState"]
__version__ = "1.0.0"
