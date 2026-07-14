from .checkpoint import validate_checkpoint
from .contracts import *
from .ledger import ReconciliationLedger
def restore_checkpoint(cp,config_hash,policy):
    v=validate_checkpoint(cp,config_hash,policy)
    if v.disposition!=CheckpointDisposition.ACCEPTED: return v,None
    ledger=ReconciliationLedger(cp.ledger)
    return v,{"ledger":ledger,"quota_records":cp.quota_records,"orders":cp.orders,"fills":cp.fills,"positions":cp.positions}
