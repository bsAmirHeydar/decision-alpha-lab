from __future__ import annotations
from .contracts import OnboardingEvidenceBundle,ScaffoldManifest,DifferentialParityReport,MigrationWaveReport,EngineInvarianceReport
from .canonical import canonical_sha256,stable_id
def build_evidence(manifest:ScaffoldManifest,parity:tuple[DifferentialParityReport,...],migrations:tuple[MigrationWaveReport,...],invariance:EngineInvarianceReport,test_summary:dict,limitations:tuple[str,...]=())->OnboardingEvidenceBundle:
    return OnboardingEvidenceBundle(stable_id('i16-evidence',{'manifest':manifest.manifest_hash,'tests':test_summary}),'1.0.0',manifest.manifest_hash,tuple(x.report_hash for x in parity),tuple(x.report_hash for x in migrations),invariance.report_hash,canonical_sha256(test_summary),limitations,'UCE-I17')
