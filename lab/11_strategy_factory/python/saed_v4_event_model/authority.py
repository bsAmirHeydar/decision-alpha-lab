from .models import EventAuthorityBoundary
from .errors import AuthorityError

def default_boundary():return EventAuthorityBoundary()
def assert_safe_boundary(boundary:EventAuthorityBoundary)->None:
    forbidden={k:v for k,v in boundary.to_dict().items() if k in {'mutate_ucee_truth','mutate_twin_manifest','select_treatment','allocate_risk','activate_runtime','send_order','network_access'} and v}
    if forbidden:raise AuthorityError('forbidden authority enabled: '+','.join(sorted(forbidden)))
