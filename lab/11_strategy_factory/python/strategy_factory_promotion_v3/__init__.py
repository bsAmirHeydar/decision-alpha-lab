"""UCE-I12 statistical, anti-overfit and promotion governance pack."""
from .calibration import *
from .canonical import canonical_json, canonical_sha256, stable_id
from .contracts import *
from .evidence import *
from .gate import decide
from .multiplicity import *
from .nulls import *
from .registry import registry, registry_snapshot
from .scorecard import build_scorecard
from .stress import *
from .uncertainty import *
from .winner_overfit import *
__version__="1.0.0"
