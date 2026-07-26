#!/usr/bin/env python3
"""Validate UCE-I02 delivery structure, English documentation, schemas and package conformance."""
from __future__ import annotations
import argparse,hashlib,json,re,sys
from pathlib import Path
PERSIAN_ARABIC=re.compile(r"[\u0600-\u06ff]")
REQUIRED_HEADERS={"UCE02_Enums.mqh","UCE02_Manifest.mqh","UCE02_Observation.mqh","UCE02_Lifecycle.mqh","UCE02_Feature.mqh","UCE02_Representation.mqh","UCE02_Cluster.mqh","UCE02_ContextPackage.mqh","UCE02_Registry.mqh","UCE02_ReferenceSynthetic.mqh","UCE02_EXP0017Reference.mqh","UCE02_Conformance.mqh","UCE02_All.mqh"}
REQUIRED_SCHEMAS={"context_source_requirement","context_package_manifest","context_observation","context_transition","feature_descriptor_v3","feature_value_v3","feature_frame_v3","representation_view_descriptor","representation_view_instance","cluster_rule","cluster_assignment","manual_policy_reference","context_task_reference","context_conformance_report","context_package_release_manifest"}

def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("root",nargs="?",default=".");args=parser.parse_args();root=Path(args.root).resolve();errors=[]
    headers=root/"mql5/Include/AlphaLab/StrategyFactory/ContextPackage";found={p.name for p in headers.glob("UCE02_*.mqh")}
    for name in sorted(REQUIRED_HEADERS-found): errors.append(f"missing MQL5 header: {name}")
    schemas=root/"schemas/legacy/strategy_factory/v3"
    for name in sorted(REQUIRED_SCHEMAS):
        p=schemas/f"{name}.schema.json"
        if not p.is_file(): errors.append(f"missing schema: {p.relative_to(root)}");continue
        try:data=json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc: errors.append(f"invalid JSON {p.name}: {exc}");continue
        if data.get("$schema")!="https://json-schema.org/draft/2020-12/schema": errors.append(f"wrong schema draft: {p.name}")
        if data.get("additionalProperties") is not False: errors.append(f"open top-level schema: {p.name}")
    docs=root/"docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i02";notes=list(docs.rglob("*.md"))
    if len(notes)<36: errors.append(f"expected at least 36 English notes including ADRs, found {len(notes)}")
    for p in notes:
        text=p.read_text(encoding="utf-8")
        if not text.startswith("---\n"): errors.append(f"missing frontmatter: {p.relative_to(root)}")
        if PERSIAN_ARABIC.search(text): errors.append(f"non-English script: {p.relative_to(root)}")
    required=[
      "tests/fixtures/legacy/strategy_factory/v3/uce_i02_context_package_vectors.json","tests/fixtures/legacy/strategy_factory/v3/uce_i02_negative_vectors.json",
      "releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I02.json",
      "releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I02_HANDOFF_TO_UCE_I03.json",
      "releases/history/ucee/manifests/UCEE_I02_PATCH_MANIFEST.json","releases/history/ucee/reports/UCEE_I02_QA_REPORT.json","releases/history/ucee/indexes/UCEE_I02_FILE_INDEX.txt","releases/history/ucee/hashes/UCEE_I02_FILE_HASHES.sha256"]
    for rel in required:
        if not (root/rel).is_file(): errors.append(f"missing delivery artifact: {rel}")
    for cache in list(root.rglob("__pycache__"))+list(root.rglob(".pytest_cache")):
        if str(cache).startswith(str(root/".pytest_cache")): continue
        if "phase_uce_i02" in str(cache) or "strategy_factory_contexts_v3" in str(cache): errors.append(f"generated cache included: {cache.relative_to(root)}")
    sys.path.insert(0,str(root/"src/engine/packages"))
    try:
        from strategy_factory_contexts_v3 import SyntheticBreakContextPackage,EXP0017ContextPackage,ContextConformanceHarness
        from strategy_factory_contexts_v3.fixtures import synthetic_records,synthetic_future_mutations,exp0017_records
        a=ContextConformanceHarness().run(SyntheticBreakContextPackage(),synthetic_records(),synthetic_future_mutations())
        b=ContextConformanceHarness().run(EXP0017ContextPackage(),exp0017_records(),[])
        if not a.passed: errors.append("synthetic reference conformance failed")
        if not b.passed: errors.append("EXP0017 reference conformance failed")
    except Exception as exc: errors.append(f"conformance execution failed: {type(exc).__name__}: {exc}")
    hf=root/"releases/history/ucee/hashes/UCEE_I02_FILE_HASHES.sha256"
    if hf.is_file():
        for n,line in enumerate(hf.read_text(encoding="utf-8").splitlines(),1):
            if not line.strip(): continue
            parts=line.split("  ",1)
            if len(parts)!=2: errors.append(f"invalid hash line {n}");continue
            expected,rel=parts;p=root/rel
            if not p.is_file(): errors.append(f"hash target missing: {rel}");continue
            if hashlib.sha256(p.read_bytes()).hexdigest()!=expected: errors.append(f"hash mismatch: {rel}")
    if errors:
        print("UCE-I02 delivery validation: FAIL");[print("ERROR:",x) for x in errors];return 1
    print(f"UCE-I02 delivery validation: PASS ({len(found)} headers, {len(notes)} English notes, {len(REQUIRED_SCHEMAS)} schemas)");return 0
if __name__=="__main__": raise SystemExit(main())
