from __future__ import annotations
from dataclasses import replace
from .contracts import DataInventory,ContextOccurrence
from .enums import DataMode
from .errors import TournamentError

def validate_inventory(inv:DataInventory,require_real:bool=False)->DataInventory:
 if require_real and inv.mode is DataMode.FIXTURE:raise TournamentError('fixture_not_real_data','fixture inventory cannot satisfy real-data gate')
 if inv.causal_cut_ms<inv.end_time_ms:raise TournamentError('causal_cut_before_end','causal cut invalid')
 return inv

def validate_occurrences(inv:DataInventory,rows:list[ContextOccurrence])->tuple[ContextOccurrence,...]:
 if len(rows)>inv.row_count:raise TournamentError('row_count_exceeded','occurrences exceed inventory row count')
 seen=set();out=[]
 for row in sorted(rows,key=lambda x:(x.known_time_ms,x.occurrence_id)):
  if row.occurrence_id in seen:raise TournamentError('duplicate_occurrence','duplicate occurrence')
  if row.known_time_ms>inv.causal_cut_ms:raise TournamentError('future_occurrence','occurrence beyond causal cut')
  if not set(row.symbol_scope).issubset(set(inv.symbols)):raise TournamentError('symbol_outside_inventory','occurrence symbol outside inventory')
  seen.add(row.occurrence_id);out.append(row)
 return tuple(out)

def future_suffix_invariant(prefix:list[ContextOccurrence],suffix:list[ContextOccurrence],cut_ms:int)->bool:
 left=[x.occurrence_hash for x in prefix if x.known_time_ms<=cut_ms]
 right=[x.occurrence_hash for x in prefix+suffix if x.known_time_ms<=cut_ms]
 return left==right
