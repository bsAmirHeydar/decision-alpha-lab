"""Non-bypassable validation rules for FP-I00."""
from __future__ import annotations

from pathlib import Path
import csv
import json
import re

from .canonical import canonical_sha256, file_sha256
from .models import Severity, ValidationIssue, ValidationReport
from .scanner import load_json, scan_dependencies, scan_tests, scan_forbidden_authority


SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class GovernanceValidator:
    def __init__(self, repo: Path, policy: dict) -> None:
        self.repo = repo.resolve()
        self.policy = policy
        self.issues: list[ValidationIssue] = []
        self.checks_run = 0

    def _check(self, condition: bool, code: str, message: str, path: str = "", severity: Severity = Severity.ERROR, **details) -> None:
        self.checks_run += 1
        if not condition:
            self.issues.append(ValidationIssue(code, severity, message, path, details))

    def validate_required_files(self) -> None:
        for relative in self.policy["required_files"]:
            self._check((self.repo / relative).is_file(), "FP_I00_REQUIRED_FILE_MISSING", "required governance input is missing", relative)

    def validate_source_hash_contract(self) -> None:
        path = self.repo / self.policy["source_hash_contract"]
        if not path.is_file():
            return
        rows = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        self._check(len(rows) == self.policy["expected_source_count"], "FP_I00_SOURCE_COUNT_MISMATCH", "source hash contract count differs", self.policy["source_hash_contract"], actual=len(rows))
        names = set()
        for row in rows:
            parts = row.split(None, 1)
            self._check(len(parts) == 2, "FP_I00_SOURCE_HASH_ROW_INVALID", "source hash row is invalid", self.policy["source_hash_contract"], row=row)
            if len(parts) != 2:
                continue
            digest, name = parts
            self._check(bool(SHA256_PATTERN.fullmatch(digest)), "FP_I00_SOURCE_HASH_INVALID", "source SHA-256 is invalid", self.policy["source_hash_contract"], source=name)
            self._check(name not in names, "FP_I00_SOURCE_NAME_DUPLICATE", "source filename is duplicated", self.policy["source_hash_contract"], source=name)
            names.add(name)

    def validate_decisions(self) -> None:
        owner_path = self.repo / self.policy["owner_decisions_path"]
        open_path = self.repo / self.policy["open_decisions_path"]
        if not owner_path.is_file() or not open_path.is_file():
            return
        owner = load_json(owner_path)
        open_decisions = load_json(open_path)
        decisions = owner.get("decisions", [])
        ids = [item.get("decision_id") for item in decisions]
        self._check(len(decisions) == 15, "FP_I00_DECISION_COUNT_MISMATCH", "owner decision freeze must contain 15 decisions", self.policy["owner_decisions_path"], actual=len(decisions))
        self._check(len(ids) == len(set(ids)), "FP_I00_DECISION_ID_DUPLICATE", "owner decision IDs must be unique", self.policy["owner_decisions_path"])
        open_ids = tuple(owner.get("open_decision_ids", []))
        self._check(open_ids == ("FP-DEC-012",), "FP_I00_OPEN_DECISION_SET_INVALID", "only FP-DEC-012 may remain open", self.policy["owner_decisions_path"], actual=open_ids)
        open_rows = open_decisions.get("open_decisions", [])
        self._check(len(open_rows) == 1 and open_rows[0].get("decision_id") == "FP-DEC-012", "FP_I00_OPEN_DECISION_CONTRACT_INVALID", "open-decision contract must contain only FP-DEC-012", self.policy["open_decisions_path"])
        live_behavior = open_rows[0].get("canonical_live_behavior") if open_rows else None
        self._check(live_behavior == "DISABLED_UNTIL_FROZEN", "FP_I00_LIVE_GATE_NOT_CLOSED", "live execution must remain disabled while FP-DEC-012 is open", self.policy["open_decisions_path"], actual=live_behavior)
        for item in decisions:
            status = item.get("status")
            if item.get("decision_id") == "FP-DEC-012":
                self._check(status == "OPEN_DECISION", "FP_I00_DEC012_STATUS_INVALID", "FP-DEC-012 must remain open", self.policy["owner_decisions_path"])
            else:
                self._check(status == "OWNER_CONFIRMED", "FP_I00_OWNER_DECISION_NOT_CONFIRMED", "non-open owner decision is not confirmed", self.policy["owner_decisions_path"], decision_id=item.get("decision_id"))

    def validate_relation_registry(self) -> None:
        path = self.repo / self.policy["relation_registry_path"]
        if not path.is_file():
            return
        data = load_json(path)
        codes = [item.get("code") for item in data.get("relations", [])]
        self._check(codes == ["AL", "AN", "LN", "NA", "NL", "NN", "WW"], "FP_I00_RELATION_REGISTRY_INVALID", "relation registry order or membership differs", self.policy["relation_registry_path"], actual=codes)
        self._check(data.get("naming") == "REFERENCE_THEN_CHECK", "FP_I00_RELATION_NAMING_INVALID", "relation naming must remain REFERENCE_THEN_CHECK", self.policy["relation_registry_path"])

    def validate_program_registry(self) -> None:
        path = self.repo / self.policy["program_registry_path"]
        if not path.is_file():
            return
        data = load_json(path)
        phases = data.get("phases", [])
        ids = [item.get("phase_id") for item in phases]
        self._check(ids == [f"FP-I{index:02d}" for index in range(17)], "FP_I00_PROGRAM_PHASE_SEQUENCE_INVALID", "implementation program phase sequence differs", self.policy["program_registry_path"], actual=ids)
        self._check(data.get("live_blocker") == "FP-DEC-012", "FP_I00_PROGRAM_LIVE_BLOCKER_INVALID", "implementation program must preserve FP-DEC-012 live blocker", self.policy["program_registry_path"])

    def validate_dependencies(self) -> None:
        records = scan_dependencies(self.repo, self.policy)
        ids = [record.dependency_id for record in records]
        self._check(len(ids) == len(set(ids)), "FP_I00_DEPENDENCY_ID_DUPLICATE", "dependency IDs must be unique")
        for record in records:
            self._check(record.file_count > 0, "FP_I00_DEPENDENCY_MISSING", "shared-core dependency root is missing or empty", record.relative_root, dependency_id=record.dependency_id)
            self._check(bool(SHA256_PATTERN.fullmatch(record.aggregate_sha256)), "FP_I00_DEPENDENCY_HASH_INVALID", "dependency aggregate hash is invalid", record.relative_root, dependency_id=record.dependency_id)
            self._check(record.mutation_allowed is False, "FP_I00_SHARED_CORE_MUTATION_ALLOWED", "FP-I00 may not mutate shared cores", record.relative_root, dependency_id=record.dependency_id)

    def validate_previous_tests(self) -> None:
        records = scan_tests(self.repo, self.policy)
        contexts = {record.context_id for record in records if record.exists}
        for record in records:
            self._check(record.exists, "FP_I00_PREVIOUS_TEST_NOT_DISCOVERABLE", "previous-context test entry point is missing", record.relative_path, context_id=record.context_id, test_id=record.test_id)
        self._check("EXP0017" in contexts, "FP_I00_EXP0017_TEST_COVERAGE_MISSING", "EXP0017 compatibility tests are not discoverable")
        self._check("EXP0018" in contexts, "FP_I00_EXP0018_TEST_COVERAGE_MISSING", "EXP0018 compatibility tests are not discoverable")

    def validate_authority_boundary(self) -> None:
        hits = scan_forbidden_authority(self.repo, self.policy["phase_owned_code_roots"])
        for path, token in hits:
            self.issues.append(ValidationIssue("FP_I00_FORBIDDEN_RUNTIME_AUTHORITY", Severity.ERROR, "FP-I00 code imports or invokes forbidden runtime authority", path, {"token": token}))
        self.checks_run += max(1, len(hits))
        for forbidden in self.policy["forbidden_runtime_paths"]:
            self._check(not (self.repo / forbidden).exists(), "FP_I00_RUNTIME_FILE_CREATED", "FP-I00 must not create runtime Detector/Indicator/EA files", forbidden)

    def validate_phase_ownership(self) -> None:
        prefixes = [item["path_prefix"] for item in self.policy["phase_ownership"]]
        self._check(len(prefixes) == len(set(prefixes)), "FP_I00_OWNERSHIP_PREFIX_DUPLICATE", "phase ownership prefixes must be unique")
        for item in self.policy["phase_ownership"]:
            self._check(item["owner_phase"] == "FP-I00", "FP_I00_OWNERSHIP_PHASE_INVALID", "owned path has wrong phase owner", item["path_prefix"])
            self._check(item["rollback_policy"] == "REMOVE_ONLY_INDEXED_FILES", "FP_I00_ROLLBACK_POLICY_INVALID", "rollback must remove only indexed files", item["path_prefix"])

    def validate_manifest_if_present(self) -> None:
        path = self.repo / self.policy["baseline_manifest_path"]
        if not path.is_file():
            self.issues.append(ValidationIssue("FP_I00_BASELINE_MANIFEST_MISSING", Severity.ERROR, "baseline manifest has not been generated", self.policy["baseline_manifest_path"]))
            self.checks_run += 1
            return
        data = load_json(path)
        supplied = data.get("manifest_hash", "")
        material = dict(data)
        material.pop("manifest_hash", None)
        self._check(supplied == canonical_sha256(material), "FP_I00_BASELINE_MANIFEST_HASH_MISMATCH", "baseline manifest hash does not match content", self.policy["baseline_manifest_path"])
        self._check(data.get("authority", {}).get("execution_authority") is False, "FP_I00_EXECUTION_AUTHORITY_PRESENT", "baseline manifest must deny execution authority", self.policy["baseline_manifest_path"])
        self._check(data.get("open_decision_ids") == ["FP-DEC-012"], "FP_I00_MANIFEST_OPEN_DECISION_INVALID", "baseline manifest must carry FP-DEC-012", self.policy["baseline_manifest_path"])

    def run(self) -> ValidationReport:
        self.validate_required_files()
        self.validate_source_hash_contract()
        self.validate_decisions()
        self.validate_relation_registry()
        self.validate_program_registry()
        self.validate_dependencies()
        self.validate_previous_tests()
        self.validate_authority_boundary()
        self.validate_phase_ownership()
        self.validate_manifest_if_present()
        evidence = canonical_sha256({
            "phase_id": self.policy["phase_id"],
            "policy_version": self.policy["phase_version"],
            "checks_run": self.checks_run,
            "issues": [
                {"code": issue.code, "severity": issue.severity.value, "message": issue.message, "path": issue.path, "details": dict(issue.details)}
                for issue in self.issues
            ],
        })
        return ValidationReport(self.policy["phase_id"], self.policy["phase_version"], tuple(self.issues), self.checks_run, evidence)
