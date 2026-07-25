from .constants import RELATION_ORDER,CANONICAL_CONSUMPTION_POLICY
from .registry import REASON_CODES,CONTRACTS

def run_conformance():
    checks={
      "relation_order":RELATION_ORDER==("AL","AN","LN","NA","NL","NN","WW"),
      "consumption_unset":CANONICAL_CONSUMPTION_POLICY=="UNSET",
      "reason_codes_unique":len(REASON_CODES)==len(set(REASON_CODES)),
      "contracts_unique":len(CONTRACTS)==len(set(CONTRACTS)),
      "reason_registry_nonempty":len(REASON_CODES)>=20,
    }
    return checks
