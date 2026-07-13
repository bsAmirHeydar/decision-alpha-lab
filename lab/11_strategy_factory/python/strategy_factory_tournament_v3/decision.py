from __future__ import annotations
from .contracts import *
from .enums import DecisionStatus,DataMode
from .canonical import stable_id

def decide_champion(tournament:TournamentReport,paper:ProspectivePaperReport,promotion_bundle_hash:str|None=None,max_challengers:int=3)->ChampionDecision:
 gates={
  'tournament_not_reference_only':not tournament.reference_only,
  'bounded_challenger_exists':bool(tournament.candidate_ids),
  'paper_mode_prospective':paper.mode is DataMode.PROSPECTIVE_PAPER,
  'paper_completed':paper.completed,
  'paper_untouched':paper.untouched,
  'paper_no_critical_findings':not paper.critical_findings,
  'paper_zero_reconciliation_mismatch':paper.mismatch_count==0,
 }
 reasons=[]
 for k,v in gates.items():
  if not v:reasons.append(k)
 champion=tournament.candidate_ids[0] if tournament.candidate_ids else 'none'
 status=DecisionStatus.PROMOTE if all(gates.values()) and promotion_bundle_hash else DecisionStatus.REJECT
 if all(gates.values()) and not promotion_bundle_hash:status=DecisionStatus.PENDING;reasons.append('promotion_bundle_missing')
 return ChampionDecision(stable_id('uce15_champion_decision',{'t':tournament.report_hash,'p':paper.report_hash}),'1.0.0',tournament.report_hash,paper.report_hash,status,champion,tournament.candidate_ids[:max_challengers],tuple(reasons),gates,promotion_bundle_hash if status is DecisionStatus.PROMOTE else None)
