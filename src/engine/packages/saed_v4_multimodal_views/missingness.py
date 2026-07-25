from .enums import MissingnessPolicy
from .errors import MissingnessError

def resolve_missing(defn):
    if defn.missingness==MissingnessPolicy.PROHIBIT:raise MissingnessError('missing prohibited feature: '+defn.feature_id)
    if defn.missingness in {MissingnessPolicy.MASK,MissingnessPolicy.UNKNOWN}:return None,1,('missing_source',)
    if defn.missingness==MissingnessPolicy.EXPLICIT_DEFAULT:
        if defn.explicit_default is None:raise MissingnessError('explicit default not declared')
        return defn.explicit_default,1,('explicit_default_used',)
    raise MissingnessError('unknown missingness policy')
