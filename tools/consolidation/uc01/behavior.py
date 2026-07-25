"""Build behavior-characterization and critical-logic evidence maps."""
from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from .classification import critical_domains, owner_domain


def build_critical_logic_inventory(
    artifact_rows: Iterable[dict],
    python_symbols: Iterable[dict],
    mql5_symbols: Iterable[dict],
    tests: Iterable[dict],
) -> tuple[list[dict], dict]:
    artifacts = {row["path"]: row for row in artifact_rows}
    symbols_by_path: dict[str, list[dict]] = defaultdict(list)
    for row in [*python_symbols, *mql5_symbols]:
        symbols_by_path[row["path"]].append(row)
    test_rows = list(tests)
    tests_by_domain: dict[str, list[dict]] = defaultdict(list)
    for test in test_rows:
        domains = test.get("critical_domains") or critical_domains(test.get("path", ""), test.get("qualified_name", ""))
        for domain in domains:
            tests_by_domain[domain].append(test)

    rows: list[dict] = []
    domain_counts: Counter[str] = Counter()
    evidence_counts: Counter[str] = Counter()
    for path, artifact in sorted(artifacts.items()):
        if artifact.get("criticality") not in {"critical", "high"}:
            continue
        if artifact.get("category") not in {"source_code", "schema", "policy", "registry_state"}:
            continue
        symbols = symbols_by_path.get(path, [])
        domains = sorted(set(artifact.get("critical_domains") or critical_domains(path, " ".join(str(x.get("qualified_name") or x.get("name") or "") for x in symbols))))
        if not domains:
            continue
        for domain in domains:
            domain_counts[domain] += 1
        symbol_fingerprints = sorted(str(x.get("surface_sha256") or "") for x in symbols if x.get("surface_sha256"))
        surface_digest = hashlib.sha256("\n".join(symbol_fingerprints).encode("utf-8")).hexdigest() if symbol_fingerprints else artifact["sha256"]
        related_tests = []
        stem = Path(path).stem.lower()
        for test in test_rows:
            test_path = test.get("path", "").lower()
            qn = test.get("qualified_name", "").lower()
            if stem and (stem in test_path or stem in qn):
                related_tests.append(test)
        if not related_tests:
            for domain in domains:
                related_tests.extend(tests_by_domain.get(domain, [])[:5])
        unique_tests = []
        seen = set()
        for test in related_tests:
            key = (test.get("path"), test.get("qualified_name"))
            if key not in seen:
                seen.add(key)
                unique_tests.append({"path": key[0], "qualified_name": key[1]})
            if len(unique_tests) >= 10:
                break
        evidence_type = "EXECUTABLE_TEST_AND_STATIC_SURFACE" if unique_tests else "STATIC_SURFACE_ONLY"
        evidence_counts[evidence_type] += 1
        rows.append({
            "path": path,
            "artifact_sha256": artifact["sha256"],
            "owner_domain": owner_domain(path),
            "critical_domains": domains,
            "surface_fingerprint_sha256": surface_digest,
            "symbol_count": len(symbols),
            "characterization_evidence": evidence_type,
            "related_tests": unique_tests,
            "retirement_allowed": False,
        })

    domain_summary = {}
    for domain in sorted(domain_counts):
        domain_tests = tests_by_domain.get(domain, [])
        domain_summary[domain] = {
            "critical_artifact_count": domain_counts[domain],
            "test_symbol_count": len(domain_tests),
            "executable_evidence_present": bool(domain_tests),
        }
    manifest = {
        "critical_artifact_count": len(rows),
        "test_symbol_count": len(test_rows),
        "evidence_type_counts": dict(sorted(evidence_counts.items())),
        "domain_coverage": domain_summary,
        "all_critical_artifacts_have_surface_fingerprint": all(bool(row["surface_fingerprint_sha256"]) for row in rows),
        "all_critical_domains_have_executable_evidence": all(item["executable_evidence_present"] for item in domain_summary.values()) if domain_summary else False,
        "claim_ceiling": "Preservation evidence only; no semantic equivalence, cutover, or deletion authority is granted.",
    }
    return rows, manifest
