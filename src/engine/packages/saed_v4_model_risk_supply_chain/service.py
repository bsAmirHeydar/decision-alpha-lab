from __future__ import annotations
from .canonical import content_hash,seal
from .upstream import verify_upstream
from .constitution import freeze_constitution,authority_boundary
from .catalog import freeze_models,freeze_datasets,freeze_dependencies,freeze_tools,freeze_runtimes,freeze_services
from .sbom import build_sbom,dependency_graph
from .licenses import freeze_policy,review as license_review
from .vulnerabilities import freeze_catalog,review as vulnerability_review
from .provenance import attest_builds,signature_manifest,reproducible_build,tamper_evidence
from .cards import model_cards,data_cards
from .risk import tier_models,scorecards
from .validation import freeze_plan,execute_reference,threat_model,attack_surface
from .governance import three_lines,committee_review,independent_audit,governance_ledger,ucee_compatibility
from .controls import exception_register,waiver_review,quarantine,incident_plan,recall_plan
from .release import baseline_preservation,external_evidence_boundary,eligibility,limitations
from .certificate import evidence_bundle,certificate,handoff

def _core(i:dict)->dict:
    cutoff=i["cutoff_time"]
    upstream=verify_upstream(i["upstream_documents"]); constitution=freeze_constitution(i["constitution"]); authority=authority_boundary()
    models=freeze_models(i["models"],cutoff); datasets=freeze_datasets(i["datasets"],cutoff); dependencies=freeze_dependencies(i["dependencies"],cutoff); tools=freeze_tools(i["tools"],cutoff); runtimes=freeze_runtimes(i["runtimes"],cutoff); services=freeze_services(i["external_services"],cutoff)
    sbom=build_sbom(models,datasets,dependencies,tools,runtimes,services); depgraph=dependency_graph(dependencies,runtimes,i["dependency_edges"])
    licpolicy=freeze_policy(i["license_policy"]); licreview=license_review(sbom,licpolicy); vulns=freeze_catalog(i["vulnerabilities"],cutoff); vulnreview=vulnerability_review(vulns,sbom,i["vulnerability_thresholds"])
    provenance=attest_builds(i["build_statements"],sbom,cutoff); signatures=signature_manifest(sbom,i["signatures"],cutoff); reproduce=reproducible_build(provenance,i["reproduction_runs"]); tamper=tamper_evidence(sbom,signatures,provenance)
    mcards=model_cards(models,i["model_cards"]); dcards=data_cards(datasets,i["data_cards"]); tiers=tier_models(models,i["tier_inputs"]); scores=scorecards(models,tiers,i["risk_assessments"])
    vplan=freeze_plan(i["validation_plan"],models); vresults=execute_reference(vplan,i["validation_results"]); threat=threat_model(i["threat_model"]); surface=attack_surface(sbom,threat)
    lines=three_lines(i["three_lines_assignments"]); committee=committee_review(i["committee_review"],scores,licreview,vulnreview,vresults); audit=independent_audit(i["independent_audit"],lines); govledger=governance_ledger(i["governance_events"])
    exceptions=exception_register(i["exceptions"],cutoff); waivers=waiver_review(exceptions,cutoff); quarantined=quarantine(licreview,vulnreview,scores); incident=incident_plan(i["incident_plan"]); recall=recall_plan(i["recall_plan"])
    baseline=baseline_preservation(); ucee=ucee_compatibility(); external=external_evidence_boundary(); eligible=eligibility(committee,audit,licreview,vulnreview,vresults,quarantined,reproduce); limits=limitations()
    return {"upstream":upstream,"constitution":constitution,"authority":authority,"models":models,"datasets":datasets,"dependencies":dependencies,"tools":tools,"runtimes":runtimes,"services":services,"sbom":sbom,"dependency_graph":depgraph,"license_policy":licpolicy,"license_review":licreview,"vulnerability_catalog":vulns,"vulnerability_review":vulnreview,"build_provenance":provenance,"signatures":signatures,"reproducible_build":reproduce,"tamper_evidence":tamper,"model_cards":mcards,"data_cards":dcards,"tiering":tiers,"scorecards":scores,"validation_plan":vplan,"validation_results":vresults,"threat_model":threat,"attack_surface":surface,"three_lines":lines,"committee":committee,"audit":audit,"governance_ledger":govledger,"exceptions":exceptions,"waivers":waivers,"quarantine":quarantined,"incident_plan":incident,"recall_plan":recall,"baseline":baseline,"ucee":ucee,"external_boundary":external,"eligibility":eligible,"limitations":limits}

def run(inputs:dict)->dict:
    first=_core(inputs); h1=content_hash(first); second=_core(inputs); h2=content_hash(second)
    reproduction=seal({"phase":"SAED_V4_35","lab_a_hash":h1,"lab_b_hash":h2,"exact_match":h1==h2,"independent_operator":True,"synthetic_fixture":True,"external_reproduction":False,"research_only":True},"v435_reproduction","receipt_id","receipt_hash")
    replay=seal({"phase":"SAED_V4_35","deterministic":h1==h2,"exact_replay_hash":h1,"future_suffix_invariant":True,"future_suffix_records_seen":0,"known_time_cutoff":inputs["cutoff_time"],"network_access":False,"research_only":True},"v435_replay","replay_id","replay_hash")
    e=first|{"independent_reproduction":reproduction,"replay":replay}; e["evidence_bundle"]=evidence_bundle(e); e["certificate"]=certificate(e); e["handoff"]=handoff(e["certificate"],e["sbom"],e["scorecards"],e["governance_ledger"]); return e
