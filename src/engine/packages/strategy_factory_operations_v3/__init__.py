"""UCE-I19 fail-closed production deployment and live-operations reference layer.

The package consumes an exact UCE-I18 release manifest. It does not connect to a
broker, send orders, raise capital automatically, or create production authority.
"""

from .authorization import authorize_cycle
from .change_control import classify_change
from .evidence import build_operations_evidence_bundle
from .health import evaluate_health
from .lease import issue_runtime_lease, revoke_runtime_lease
from .orchestrator import evaluate_operating_cycle
from .ramp import evaluate_ramp
from .release_binding import compile_deployment_plan

__all__ = [
    "authorize_cycle",
    "build_operations_evidence_bundle",
    "classify_change",
    "compile_deployment_plan",
    "evaluate_health",
    "evaluate_operating_cycle",
    "evaluate_ramp",
    "issue_runtime_lease",
    "revoke_runtime_lease",
]
