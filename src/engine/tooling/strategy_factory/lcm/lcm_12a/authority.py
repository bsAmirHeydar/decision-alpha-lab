from __future__ import annotations
import re
from pathlib import Path

CANONICAL_PREFIXES = (
    "docs/architecture/master/",
    "docs/architecture/",
    "docs/doctrine/",
    "docs/specifications/",
)
GENERATED_HINTS = ("/fixtures/", "/generated/", "/projections/", "/projection/", "/source_cards/", "/atomic_concepts/", "/reports/generated/", "/reference_report/")
ARCHIVE_HINTS = ("/archive/", "/archived/", "/attic/", "/backup/", "/backups/")
SUPPORTING_NAME_PREFIXES = ("README_", "INSTALL_", "ROLLBACK_", "COMMIT_MESSAGE_", "LCM_", "ACL_OS_", "SAED_", "NDS_")

def owner_for(row):
    path = row["path"]
    text = row["text"]
    match = re.search(r"(?im)^\s*(?:owner|maintainer|author)\s*:\s*[\"']?([^\n\"']+)", text[:5000])
    if match:
        return match.group(1).strip(), "DECLARED"
    if path.startswith("docs/architecture/master/"):
        return "ALPHA_LAB_ARCHITECTURE_OWNER", "PATH_POLICY"
    if path.startswith("docs/"):
        return "ALPHA_LAB_DOCUMENTATION_OWNER", "PATH_POLICY"
    if path.startswith("registry/"):
        return "REGISTRY_PRODUCER_BOUND_OWNER", "PATH_POLICY"
    if path.startswith("lab/"):
        return "ALPHA_LAB_TEST_EVIDENCE_OWNER", "PATH_POLICY"
    if path.startswith("mql5/"):
        return "ALPHA_LAB_MQL5_DOMAIN_OWNER", "PATH_POLICY"
    name = Path(path).name
    if name in {"README.md", "AGENTS.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md"}:
        return "REPOSITORY_GOVERNANCE_OWNER", "ROOT_POLICY"
    if name.startswith(SUPPORTING_NAME_PREFIXES):
        return "RELEASE_EVIDENCE_OWNER", "ROOT_POLICY"
    return "UNASSIGNED_OWNER", "UNKNOWN"

def provisional_authority(row):
    path = row["path"]; low = "/" + path.lower(); name = Path(path).name
    if any(hint in low for hint in ARCHIVE_HINTS):
        return "ARCHIVE_ONLY", "ARCHIVE_PATH_POLICY"
    if any(hint in low for hint in GENERATED_HINTS):
        return "GENERATED_PROJECTION", "GENERATED_PATH_POLICY"
    if path.startswith(CANONICAL_PREFIXES):
        if "projection" in name.lower() or "generated" in row["declared_status"].lower():
            return "GENERATED_PROJECTION", "EXPLICIT_PROJECTION_POLICY"
        return "CANONICAL", "ARCHITECTURE_PATH_POLICY"
    if name in {"README.md", "AGENTS.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md"}:
        return "CANONICAL", "ROOT_GOVERNANCE_POLICY"
    if name.startswith(SUPPORTING_NAME_PREFIXES) or "audit_report" in name.lower() or "release" in low:
        return "SUPPORTING_EVIDENCE", "RELEASE_EVIDENCE_POLICY"
    if "deprecated" in low or "superseded" in low or re.search(r"(?:^|[_-])old(?:[_-]|$)", name.lower()):
        return "SUPERSEDED", "SUPERSEDED_PATH_POLICY"
    if path.startswith("registry/"):
        return "SUPPORTING_EVIDENCE", "REGISTRY_DOCUMENT_POLICY"
    if path.startswith("lab/"):
        return "SUPPORTING_EVIDENCE", "TEST_EVIDENCE_POLICY"
    if path.startswith("mql5/"):
        return "SUPPORTING_EVIDENCE", "SOURCE_ADJACENT_DOCUMENT_POLICY"
    return "UNKNOWN", "NO_DETERMINISTIC_AUTHORITY_RULE"

def classify(rows, exact_membership):
    output = []
    for row in rows:
        authority, rationale = provisional_authority(row)
        duplicate = exact_membership.get(row["document_id"])
        if duplicate and duplicate["canonical_document_id"] != row["document_id"]:
            authority = "DUPLICATE"; rationale = "BYTE_IDENTICAL_NON_CANONICAL_REPRESENTATIVE"
        owner, owner_source = owner_for(row)
        output.append({
            "document_id": row["document_id"], "path": row["path"], "title": row["title"],
            "authority_class": authority, "authority_rationale": rationale,
            "owner": owner, "owner_source": owner_source,
            "declared_version": row["declared_version"], "declared_status": row["declared_status"],
            "active": row["active"], "byte_digest": row["byte_digest"], "normalized_digest": row["normalized_digest"],
            "validation_status": "PASS" if authority != "UNKNOWN" else "UNKNOWN",
        })
    return output
