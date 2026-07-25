"""Nested-selection and multiplicity accounting over the complete I11 universe."""
from __future__ import annotations
from dataclasses import asdict
from math import fsum
from typing import Mapping, Sequence
import numpy as np
from .canonical import canonical_sha256, canonical_json, stable_id
from .contracts import FamilyDefinition, MultiplicityReport, SelectionUniverse
from .enums import CorrectionMethod, DecisionRole
from .errors import PromotionError

def adjust_p_values(p_values:Sequence[float], method:CorrectionMethod)->np.ndarray:
    p=np.asarray(p_values,dtype=float)
    if p.ndim!=1 or np.any(~np.isfinite(p)) or np.any((p<0)|(p>1)): raise PromotionError("invalid_p_values","p-values must be finite in [0,1]")
    m=len(p)
    if m==0: return np.asarray([],dtype=float)
    order=np.argsort(p,kind="mergesort"); ranked=p[order]
    if method is CorrectionMethod.BONFERRONI: adjusted=np.minimum(1.0,p*m); return adjusted
    if method is CorrectionMethod.HOLM:
        raw=(m-np.arange(m))*ranked; mono=np.maximum.accumulate(raw); ranked_adj=np.minimum(1.0,mono)
    else:
        factor=m if method is CorrectionMethod.BENJAMINI_HOCHBERG else m*fsum(1.0/i for i in range(1,m+1))
        raw=ranked*factor/np.arange(1,m+1); ranked_adj=np.minimum(1.0,np.minimum.accumulate(raw[::-1])[::-1])
    adjusted=np.empty(m,dtype=float); adjusted[order]=ranked_adj; return adjusted

def family_key(trial, definition:FamilyDefinition)->str:
    return canonical_json({dim:getattr(trial,dim) for dim in definition.dimensions})

def multiplicity_report(universe:SelectionUniverse, definition:FamilyDefinition)->MultiplicityReport:
    grouped:dict[str,list]= {}
    for trial in universe.trials: grouped.setdefault(family_key(trial,definition),[]).append(trial)
    adjusted:dict[str,float]={}; rejected=[]; missing=0
    for key,trials in sorted(grouped.items()):
        observed=[t for t in trials if t.p_value is not None]
        missing += len(trials)-len(observed)
        if not observed: continue
        denominator=len(trials) if definition.include_missing_p_values else len(observed)
        p=[t.p_value for t in observed]
        # Pad absent choices with p=1 so every declared choice increases family multiplicity.
        padded=p+[1.0]*(denominator-len(p))
        corrected=adjust_p_values(padded,definition.correction)[:len(p)]
        for trial,value in zip(observed,corrected):
            adjusted[trial.trial_id]=float(value)
            if value<=definition.alpha: rejected.append(trial.trial_id)
    payload={"universe_hash":universe.universe_hash,"definition":asdict(definition),"adjusted":adjusted,"families":{k:len(v) for k,v in grouped.items()},"missing":missing}
    return MultiplicityReport(report_id=stable_id("multiplicity",payload),universe_hash=universe.universe_hash,family_definition_hash=canonical_sha256(asdict(definition)),total_choice_count=len(universe.trials),tested_choice_count=len(universe.trials)-missing,missing_p_value_count=missing,rejected_trial_ids=tuple(sorted(rejected)),adjusted_p_values=adjusted,family_counts={k:len(v) for k,v in sorted(grouped.items())},evidence_hash=canonical_sha256(payload))

def reconcile_trial_universe(universe:SelectionUniverse, ledger_trial_ids:Sequence[str], manifest_trial_ids:Sequence[str])->Mapping[str,object]:
    u={t.trial_id for t in universe.trials}; l=set(ledger_trial_ids); m=set(manifest_trial_ids)
    return {"complete":u==l==m,"universe_count":len(u),"ledger_count":len(l),"manifest_count":len(m),"missing_from_universe":sorted((l|m)-u),"missing_from_ledger":sorted((u|m)-l),"missing_from_manifest":sorted((u|l)-m),"evidence_hash":canonical_sha256({"u":sorted(u),"l":sorted(l),"m":sorted(m)})}

def audit_nested_selection(inner_train_ids:Sequence[str], inner_validation_ids:Sequence[str], outer_confirmation_ids:Sequence[str], *, declaration_frozen:bool, confirmation_role:DecisionRole)->Mapping[str,object]:
    train=set(inner_train_ids); val=set(inner_validation_ids); outer=set(outer_confirmation_ids)
    overlaps={"train_validation":sorted(train&val),"train_outer":sorted(train&outer),"validation_outer":sorted(val&outer)}
    blockers=[]
    if any(overlaps.values()): blockers.append("nested_selection_overlap")
    if not declaration_frozen: blockers.append("confirmatory_declaration_not_frozen")
    if confirmation_role not in (DecisionRole.CONFIRMATION,DecisionRole.PROSPECTIVE_CHALLENGE): blockers.append("invalid_confirmation_role")
    return {"passed":not blockers,"blockers":blockers,"overlaps":overlaps,"inner_train_count":len(train),"inner_validation_count":len(val),"outer_count":len(outer),"evidence_hash":canonical_sha256({"overlaps":overlaps,"frozen":declaration_frozen,"role":confirmation_role})}
