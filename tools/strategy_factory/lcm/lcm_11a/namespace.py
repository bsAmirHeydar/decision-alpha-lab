from __future__ import annotations
from .canonical import stable_id, token
from .constants import CANONICAL_NAMESPACE_VERSION
from .models import NamespaceContract, VisualSite

def _observed_scope(site: VisualSite) -> tuple[str,str]:
    expr=(site.observed_name_expression+" "+site.chart_scope_expression).lower()
    if site.surface_kind in {"INDICATOR_BUFFER","REPORT_PROJECTION"}: return "PLATFORM_OR_OUTPUT_SCOPED","LOW"
    scoped_tokens=("prefix","instance","chart_id","chartid","symbol","timeframe","context_id","object_namespace","m_prefix")
    if any(x in expr for x in scoped_tokens): return "PARTIALLY_SCOPED","MEDIUM"
    if '"' in site.observed_name_expression and "+" not in site.observed_name_expression: return "STATIC_OR_GLOBAL_NAME","HIGH"
    return "UNPROVEN_SCOPE","HIGH"

def build_namespace_contract(site: VisualSite) -> NamespaceContract:
    observed_status,risk=_observed_scope(site)
    owner=token(site.owner); subsystem=token(site.subsystem); role=token(site.object_type); visual=site.visual_object_id.split("_",1)[-1][:12]
    template=f"{CANONICAL_NAMESPACE_VERSION}::{owner}::{subsystem}::{{INSTANCE_ID}}::{{CHART_ID}}::{{SYMBOL}}::{{TIMEFRAME}}::{{EVENT_ID}}::{role}::{visual}"
    cleanup=f"{CANONICAL_NAMESPACE_VERSION}::{owner}::{subsystem}::{{INSTANCE_ID}}::{{CHART_ID}}::"
    return NamespaceContract(stable_id("VISNS",site.visual_object_id,template),site.visual_object_id,template,cleanup,site.observed_name_expression,observed_status,risk,True,True,True)

def simulate_namespace_collisions(contracts: list[NamespaceContract]) -> dict:
    scenarios=[]; seen=set(); collisions=[]
    for contract in contracts:
        for scenario,vals in (
            ("SAME_CHART_DIFFERENT_INSTANCE",("I1","C1","EURUSD","M5","E1")),
            ("SAME_CHART_SECOND_INSTANCE",("I2","C1","EURUSD","M5","E1")),
            ("DIFFERENT_CHART_SAME_INSTANCE",("I1","C2","EURUSD","M5","E1")),
            ("SAME_SYMBOL_DIFFERENT_TIMEFRAME",("I1","C1","EURUSD","H1","E1")),
            ("SAME_SCOPE_DIFFERENT_EVENT",("I1","C1","EURUSD","M5","E2")),
        ):
            value=contract.canonical_object_id_template.replace("{INSTANCE_ID}",vals[0]).replace("{CHART_ID}",vals[1]).replace("{SYMBOL}",vals[2]).replace("{TIMEFRAME}",vals[3]).replace("{EVENT_ID}",vals[4])
            key=(scenario,value)
            if value in seen: collisions.append({"scenario":scenario,"canonical_object_id":value,"namespace_id":contract.namespace_id})
            seen.add(value); scenarios.append({"scenario":scenario,"namespace_id":contract.namespace_id,"canonical_object_id":value,"result":"PASS"})
    return {"scenario_count":len(scenarios),"collision_count":len(collisions),"collisions":collisions,"scenarios":scenarios,"result":"PASS" if not collisions else "FAIL"}
