from __future__ import annotations
from .upstream import verify_upstream
from .constitution import freeze_constitution,authority_boundary
from .instruments import freeze_instrument_master
from .fx import freeze_fx_snapshot
from .costs import freeze_cost_schedules
from .liquidity import freeze_liquidity_profiles
from .dependence import freeze_dependence,covariance
from .constraints import freeze_constraints
from .portfolio import freeze_opportunities
from .capacity import compute_capacity
from .economics import opportunity_economics
from .allocator import allocate
from .scheduler import build_non_executable_schedule
from .stress import run_stress
from .ledger import build_reservation_ledger
from .reconciliation import reconcile
from .governance import freeze_reviews,preserve_baseline,evidence_bundle,certificate,handoff

def run_reference(f:dict)->dict:
    cutoff=f["cutoff_time"]
    out={}
    out["upstream_receipt"]=verify_upstream(f["upstream"])
    out["constitution"]=freeze_constitution(f["constitution"])
    out["authority_boundary"]=authority_boundary()
    out["instrument_master"]=freeze_instrument_master(f["instruments"],cutoff)
    out["fx_snapshot"]=freeze_fx_snapshot(f["base_currency"],f["fx_rates"],cutoff)
    out["cost_registry"]=freeze_cost_schedules(f["cost_schedules"],cutoff)
    out["liquidity_registry"]=freeze_liquidity_profiles(f["liquidity_profiles"],cutoff)
    out["dependence_model"]=freeze_dependence(f["dependence"],cutoff)
    out["covariance_matrix"]={"phase":"SAED_V4_37","instrument_ids":out["dependence_model"]["instrument_ids"],"matrix":covariance(out["dependence_model"]),"research_only":True}
    out["constraints"]=freeze_constraints(f["constraints"],cutoff)
    out["opportunity_registry"]=freeze_opportunities(f["opportunities"],cutoff)
    out["capacity_surface"]=compute_capacity(out["opportunity_registry"],out["liquidity_registry"],out["instrument_master"],f["prices"],out["constraints"])
    out["opportunity_economics"]=opportunity_economics(out["opportunity_registry"],out["capacity_surface"],out["instrument_master"],out["liquidity_registry"],out["cost_registry"],f["prices"],out["constraints"])
    out["allocation_plan"]=allocate(out["opportunity_economics"],out["opportunity_registry"],out["dependence_model"],out["constraints"])
    out["non_executable_schedule"]=build_non_executable_schedule(out["allocation_plan"],out["opportunity_registry"],out["instrument_master"],out["liquidity_registry"],f["prices"],out["constraints"])
    out["stress_suite"]=run_stress(out["allocation_plan"],out["opportunity_economics"],f["stress_scenarios"],out["constraints"])
    out["reservation_ledger"]=build_reservation_ledger(out["allocation_plan"],out["constraints"])
    out["synthetic_reconciliation"]=reconcile(out["non_executable_schedule"],f["synthetic_fills"],out["opportunity_economics"])
    out["baseline_receipt"]=preserve_baseline(out["allocation_plan"],out["non_executable_schedule"])
    out["review_bundle"]=freeze_reviews(f["reviews"],out["allocation_plan"]["plan_hash"])
    bundle_input={k:v for k,v in out.items() if k not in {"review_bundle"}}
    out["evidence_bundle"]=evidence_bundle(bundle_input)
    out["certificate"]=certificate(out["evidence_bundle"],out["review_bundle"],out["stress_suite"],out["baseline_receipt"])
    out["handoff"]=handoff(out["certificate"],out["allocation_plan"],out["opportunity_economics"],out["non_executable_schedule"])
    return out
