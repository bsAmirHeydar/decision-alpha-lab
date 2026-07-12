"""Executable package linting, causality perturbation, replay and chaos conformance."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Any, Iterable
from strategy_factory_contracts_v3 import canonical_sha256
from .enums import ConformanceSeverity, ContextLifecycleState
from .package import ContextPackage
from .lifecycle import ContextLifecycleEngine
from .representation import RepresentationViewRegistry
from .cluster import ClusterCompiler
from .errors import ConformanceError
from .utils import contract_safe

@dataclass(frozen=True, slots=True)
class ConformanceFinding:
    code: str; severity: ConformanceSeverity; message: str; evidence: Mapping[str,Any]
@dataclass(frozen=True, slots=True)
class ConformanceReport:
    package_id: str; package_version: str; passed: bool; findings: tuple[ConformanceFinding,...]; replay_hash: str; tested_records: int
    def material(self): return {"findings":[{"code":x.code,"evidence":contract_safe(x.evidence),"message":x.message,"severity":x.severity.value} for x in self.findings],"package_id":self.package_id,"package_version":self.package_version,"passed":self.passed,"replay_hash":self.replay_hash,"tested_records":self.tested_records}

class ContextPackageLinter:
    def lint(self,package:ContextPackage)->tuple[ConformanceFinding,...]:
        findings=[]; manifest=package.manifest
        feature_ids=[x.feature_id for x in package.feature_descriptors()]
        view_ids=[x.view_id for x in package.view_descriptors()]
        cluster_ids=[x.rule_id for x in package.cluster_rules()]
        if not feature_ids: findings.append(ConformanceFinding("no_features",ConformanceSeverity.FATAL,"package exposes no feature descriptors",{}))
        if not view_ids: findings.append(ConformanceFinding("no_views",ConformanceSeverity.FATAL,"package exposes no representation views",{}))
        if not cluster_ids: findings.append(ConformanceFinding("no_cluster_rules",ConformanceSeverity.ERROR,"package exposes no dependence clusters",{}))
        for view in package.view_descriptors():
            missing=sorted(set(view.feature_ids)-set(feature_ids))
            if missing: findings.append(ConformanceFinding("view_unknown_feature",ConformanceSeverity.FATAL,"view references unknown features",{"view_id":view.view_id,"missing":missing}))
            if view.runtime_exportable and not all(next(f for f in package.feature_descriptors() if f.feature_id==fid).runtime_exportable for fid in view.feature_ids): findings.append(ConformanceFinding("runtime_view_offline_feature",ConformanceSeverity.FATAL,"runtime-exportable view consumes an offline-only feature",{"view_id":view.view_id}))
        manifest_view_ids={x.component_id for x in manifest.representation_views}
        if manifest_view_ids!=set(view_ids): findings.append(ConformanceFinding("manifest_view_mismatch",ConformanceSeverity.FATAL,"manifest and package view descriptors disagree",{"manifest":sorted(manifest_view_ids),"actual":sorted(view_ids)}))
        return tuple(findings)

class ContextConformanceHarness:
    def __init__(self)->None: self.views=RepresentationViewRegistry(); self.clusters=ClusterCompiler()
    def run(self,package:ContextPackage,records:Iterable[Mapping[str,Any]],future_mutations:Iterable[Mapping[str,Any]] | None=None)->ConformanceReport:
        findings=list(ContextPackageLinter().lint(package)); ledger=[]; lifecycle=ContextLifecycleEngine()
        records=list(records); mutations=list(future_mutations or [])
        for index,record in enumerate(records):
            try:
                observations=package.observe(record)
                for observation in observations:
                    current,is_new=lifecycle.register(observation)
                    if not is_new: continue
                    frame=package.build_feature_frame(current,record)
                    views=[]
                    for descriptor in package.view_descriptors():
                        if descriptor.kind.value=="sequence": continue
                        if descriptor.kind.value=="intermarket": continue
                        views.append(self.views.compile(descriptor,frame,record.get("auxiliary",{})).view_hash)
                    ledger.append({"frame_hash":frame.frame_hash,"observation_hash":current.observation_hash,"observation_id":current.observation_id,"view_hashes":views})
            except Exception as exc:
                findings.append(ConformanceFinding("record_failure",ConformanceSeverity.ERROR,str(exc),{"index":index,"type":type(exc).__name__}))
        baseline_hash=canonical_sha256(ledger)
        # Future perturbation: past outputs must be invariant when only data strictly after observation_cut changes.
        for mutation in mutations:
            base_index=int(mutation.get("base_record_index",0))
            if base_index<0 or base_index>=len(records):
                findings.append(ConformanceFinding("invalid_mutation_index",ConformanceSeverity.ERROR,"future mutation references invalid record",{"index":base_index})); continue
            original=dict(records[base_index]); changed=dict(original); changed.update(dict(mutation.get("changes",{})))
            cutoff=int(original.get("observation_cut_ms",original.get("confirmation_time_ms",original.get("known_time_ms",original.get("event_time_ms",0)))))
            mutation_time=int(mutation.get("mutation_time_ms",cutoff+1))
            if mutation_time<=cutoff:
                findings.append(ConformanceFinding("non_future_mutation",ConformanceSeverity.ERROR,"future perturbation timestamp is not after observation cut",{"cutoff":cutoff,"mutation_time_ms":mutation_time})); continue
            a=package.observe(original); b=package.observe(changed)
            if [x.observation_hash for x in a] != [x.observation_hash for x in b]: findings.append(ConformanceFinding("future_perturbation_changed_past",ConformanceSeverity.FATAL,"future-only mutation changed historical observation hash",{"record_index":base_index}))
        # Deterministic replay.
        replay=[]; replay_seen=set()
        for record in records:
            for observation in package.observe(record):
                if observation.observation_id in replay_seen: continue
                replay_seen.add(observation.observation_id)
                frame=package.build_feature_frame(observation,record); replay.append({"frame_hash":frame.frame_hash,"observation_hash":observation.observation_hash,"observation_id":observation.observation_id,"view_hashes":[self.views.compile(d,frame,record.get("auxiliary",{})).view_hash for d in package.view_descriptors() if d.kind.value not in ("sequence","intermarket")]})
        if canonical_sha256(replay)!=baseline_hash: findings.append(ConformanceFinding("replay_hash_mismatch",ConformanceSeverity.FATAL,"repeat replay did not reproduce ledger hash",{}))
        passed=not any(x.severity in (ConformanceSeverity.ERROR,ConformanceSeverity.FATAL) for x in findings)
        return ConformanceReport(package.manifest.package_id,package.manifest.version,passed,tuple(findings),baseline_hash,len(records))
