from __future__ import annotations
from dataclasses import replace
from .canonical import canonical_sha256
from .contracts import *
from .enums import EvidenceStatus, ReleaseStage

H = "a" * 64
H2 = "b" * 64
H3 = "c" * 64
NOW = 2_000_000


def environment() -> EnvironmentFingerprint:
    return EnvironmentFingerprint("env-golden", "Windows", "11", "5000", "5000", "Demo-Server", "demo", "UTC", H, H2, NOW)


def policy() -> QualificationPolicy:
    return QualificationPolicy(
        "qualification-policy-v1", "1.0.0",
        ("host", "diagnostic"), 0,
        ("feature-vector", "decision", "risk"),
        1440, 10000, 64.0, 250.0,
        ("terminal_disconnect", "process_restart", "stale_quote", "corrupt_checkpoint", "duplicate_event", "broker_reject"),
        120.0, 1.0,
        ("artifact_integrity", "secret_scan", "least_privilege", "backup_restore", "retention"),
        20, 1000, 20, 1000, 5, 100, 10, 250, 20, 500,
        0.05, 0.25, 0.5, 1.0, True,
    )


def compile_evidence(passed: bool = True) -> CompileEvidence:
    targets = tuple(CompileTargetResult(name, H, "5000", 0 if passed else 1, 0 if passed else 1, 0, H2, H3, NOW) for name in ("host", "diagnostic"))
    return CompileEvidence("compile-golden", "1.0.0", environment().fingerprint_hash, targets, ("host", "diagnostic"), 0, NOW)


def differential_report(passed: bool = True, source: str = "python", target: str = "mql5") -> DifferentialReport:
    cases = tuple(DifferentialCase(case_id, H, H if passed else H2, 0.0 if passed else 1.0, 0.0 if passed else 1.0, 1e-12, 1e-12, 100, 0 if passed else 1) for case_id in policy().required_differential_cases)
    return DifferentialReport(f"diff-{source}-{target}", "1.0.0", source, target, NOW - 1000, cases)


def soak_report(passed: bool = True) -> SoakReport:
    return SoakReport("soak-golden", "1.0.0", environment().fingerprint_hash, 1500, 12000, 500, 0 if passed else 1, 0, 0, 0, 0, 20.0, 100.0, 10, 0, 1_500 * 60_000)


def chaos_report(passed: bool = True) -> ChaosReport:
    scenarios = tuple(ChaosScenarioResult(s, NOW, True, True, passed, False, 0, 10.0, H) for s in policy().required_chaos_scenarios)
    return ChaosReport("chaos-golden", "1.0.0", environment().fingerprint_hash, scenarios, policy().required_chaos_scenarios)


def recovery_report(passed: bool = True) -> RecoveryReport:
    return RecoveryReport("recovery-golden", "1.0.0", environment().fingerprint_hash, H, H2, H2 if passed else H3, 3, 100, 0, 0, 0, 30.0, 0.0, True, True)


def security_report(passed: bool = True) -> SecurityReport:
    controls = tuple(SecurityControlResult(control, EvidenceStatus.PASS if passed else EvidenceStatus.FAIL, H, "fixture") for control in policy().required_security_controls)
    return SecurityReport("security-golden", "1.0.0", controls, policy().required_security_controls, 0 if passed else 1, 0, 0, True, True)


def stage_evidence(stage: ReleaseStage, passed: bool = True) -> ProspectiveStageEvidence:
    settings = {
        ReleaseStage.PAPER: (20, 1000, 0.0, 1.0, ""),
        ReleaseStage.SHADOW: (20, 1000, 0.0, 1.0, ""),
        ReleaseStage.MICRO_LIVE: (5, 100, 0.1, 0.25, "approval-1"),
        ReleaseStage.LIMITED_LIVE: (10, 250, 0.4, 0.5, "approval-2"),
        ReleaseStage.PRODUCTION: (20, 500, 0.8, 1.0, "approval-3"),
    }
    sessions, events, realized, allowed, approval = settings[stage]
    return ProspectiveStageEvidence(f"{stage.value}-golden", "1.0.0", stage, environment().fingerprint_hash, 0, NOW, sessions, events, 50, 0, 0, 0, 0 if passed else 1, realized, allowed, approval)


def rollback_report(passed: bool = True) -> RollbackDrillReport:
    return RollbackDrillReport("rollback-golden", "1.0.0", H, H2, 0, 30_000, 60.0, passed, passed, passed, H3)
