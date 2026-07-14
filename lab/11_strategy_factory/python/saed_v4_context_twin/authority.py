from __future__ import annotations
from .models import TwinAuthorityBoundary
from .errors import AuthorityError

def default_boundary()->TwinAuthorityBoundary:return TwinAuthorityBoundary()
def assert_safe_boundary(boundary:TwinAuthorityBoundary)->None:
    forbidden={'mutate_ucee_truth':boundary.mutate_ucee_truth,'select_treatment':boundary.select_treatment,'allocate_risk':boundary.allocate_risk,'activate_runtime':boundary.activate_runtime,'send_order':boundary.send_order,'network_access':boundary.network_access}
    enabled=[k for k,v in forbidden.items() if v]
    if enabled:raise AuthorityError('forbidden authority enabled: '+','.join(sorted(enabled)))
