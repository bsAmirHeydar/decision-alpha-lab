from .trace import TraceLedger
from .checkpoint import validate_checkpoint
from .contracts import *

def resume_from_checkpoint(manifest,fixture_id,all_events,checkpoint):
    val=validate_checkpoint(checkpoint,manifest,fixture_id)
    ledger=TraceLedger(manifest,fixture_id)
    if val.disposition==CheckpointDisposition.ACCEPTED:
        for e in checkpoint.events: ledger.append(e)
        for e in all_events:
            if e.sequence>checkpoint.processed_sequence: ledger.append(e)
    else:
        for e in all_events: ledger.append(e)
    return ledger.run(),val
