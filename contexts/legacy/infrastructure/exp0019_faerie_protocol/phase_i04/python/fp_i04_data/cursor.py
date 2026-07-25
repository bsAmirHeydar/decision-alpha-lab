from __future__ import annotations
from .contracts import IncrementalCursor,SynchronizationResult
from .enums import CursorState
from .errors import FPI04Error

def empty_cursor(pair_id:str)->IncrementalCursor:
    return IncrementalCursor(pair_id,None,-1,-1,'NONE',CursorState.EMPTY)

def advance_cursor(cursor:IncrementalCursor,result:SynchronizationResult)->IncrementalCursor:
    if cursor.pair_id!=result.pair_id: raise FPI04Error('FP_DRC_CURSOR_PAIR_MISMATCH','cursor pair differs')
    last=result.rows[-1].open_utc_ms if result.rows else cursor.last_emitted_open_utc_ms
    left=max((r.left.bar.source_sequence for r in result.rows if r.left.bar),default=cursor.left_last_source_sequence)
    right=max((r.right.bar.source_sequence for r in result.rows if r.right.bar),default=cursor.right_last_source_sequence)
    return IncrementalCursor(cursor.pair_id,last,left,right,result.revision.revision_id,CursorState.ACTIVE if result.rows else CursorState.EXHAUSTED)

def validate_resume(cursor:IncrementalCursor,parent_revision_id:str):
    if cursor.state is CursorState.INVALIDATED: raise FPI04Error('FP_DRC_CURSOR_INVALIDATED','cursor invalidated')
    if cursor.data_revision_id not in ('NONE',parent_revision_id): raise FPI04Error('FP_DRC_CURSOR_REVISION_MISMATCH','cursor revision differs')
    return True
