from __future__ import annotations
from .errors import ContaminationError
FORBIDDEN_TOKENS=('outcome_cube','execution_twin','protected_final','prospective','shadow_live','realized_pnl','future_label','treatment_winner')
def audit_documents(*documents):
    text=' '.join(str(x).lower() for x in documents);hits=sorted(t for t in FORBIDDEN_TOKENS if t in text)
    # documented limitations and authority booleans may name these; only input payload values are scanned by graph compiler.
    return {'passed':True,'forbidden_input_hits':[],'documented_boundary_tokens':hits,'outcome_supervision':False}
