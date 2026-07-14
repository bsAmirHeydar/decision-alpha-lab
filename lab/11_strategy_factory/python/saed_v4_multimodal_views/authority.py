from .models import ViewAuthorityBoundary
from .errors import AuthorityError
FORBIDDEN={'mutate_ucee_truth','mutate_twin_manifest','mutate_event_journal','fit_adaptive_normalizer','impute_silently','train_model','select_treatment','allocate_risk','activate_runtime','send_order','network_access'}
def default_boundary():return ViewAuthorityBoundary()
def assert_safe_boundary(boundary:ViewAuthorityBoundary)->None:
    bad=[k for k,v in boundary.to_dict().items() if k in FORBIDDEN and v]
    if bad:raise AuthorityError('forbidden authority enabled: '+','.join(sorted(bad)))
