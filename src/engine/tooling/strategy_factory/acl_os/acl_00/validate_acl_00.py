from __future__ import annotations
import argparse
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from ..common import REPO_ROOT, load_json, result
from .catalogs import PolicyBundle

PHASE_ROOT = REPO_ROOT / "registry" / "acl_os" / "acl_00"
SCHEMA_ROOT = PHASE_ROOT / "schemas" / "v1"
DOC_ROOT = (
    REPO_ROOT
    / "docs"
    / "alpha_lab_master_architecture"
    / "context_lifecycle_os"
    / "12_PHASE_DELIVERIES"
    / "ACL_00"
)
MQL5_ROOT = (
    REPO_ROOT
    / "lab"
    / "11_strategy_factory"
    / "mql5"
    / "Include"
    / "AlphaLab"
    / "ACL_OS"
    / "ACL00"
)
FORBIDDEN_MQL5 = ("OrderSend(", "CTrade", "trade.Buy", "trade.Sell", "PositionOpen")


def validate(repo: Path = REPO_ROOT) -> dict:
    checks = []
    schema_errors = []
    schemas = list(SCHEMA_ROOT.glob("*.schema.json"))
    for path in schemas:
        try:
            Draft202012Validator.check_schema(load_json(path))
        except Exception as exc:
            schema_errors.append(f"{path.name}: {exc}")
    checks.append(
        result(
            len(schemas) >= 10 and not schema_errors,
            "ACL00_SCHEMA_CLOSURE",
            "ACL-00 closed schemas",
            count=len(schemas),
            errors=schema_errors,
        )
    )

    try:
        bundle = PolicyBundle.load(PHASE_ROOT / "policies" / "v1")
        policy_error = None
    except Exception as exc:
        bundle = None
        policy_error = str(exc)
    checks.append(
        result(
            bundle is not None,
            "ACL00_POLICY_BUNDLE",
            "policy bundle loads",
            error=policy_error,
            digest=bundle.digest if bundle else None,
        )
    )

    transition_errors = []
    if bundle:
        transitions = bundle.documents["lifecycle_transitions"].get("transitions", {})
        state_catalog = yaml.safe_load(
            (repo / "registry" / "acl_os" / "catalogs" / "lifecycle_states.yaml").read_text(
                encoding="utf-8"
            )
        )
        states = set(state_catalog["states"])
        for key, spec in transitions.items():
            try:
                source, target = key.split("->")
            except ValueError:
                transition_errors.append(f"bad key {key}")
                continue
            if source not in states or target not in states:
                transition_errors.append(f"unknown state in {key}")
            references = (
                ("evidence_policy", "evidence_requirements"),
                ("approval_policy", "approval_policy"),
                ("security_policy", "security_hook_policy"),
            )
            for field, document in references:
                value = spec.get(field)
                if value not in bundle.documents[document]["policies"]:
                    transition_errors.append(f"{key} unknown {field}={value}")
    checks.append(
        result(
            not transition_errors,
            "ACL00_TRANSITION_REFERENCES",
            "transition references resolve",
            errors=transition_errors,
        )
    )

    docs = list(DOC_ROOT.glob("*.md"))
    bad_front = [
        str(path.relative_to(repo))
        for path in docs
        if not path.read_text(encoding="utf-8").startswith("---\n")
    ]
    checks.append(
        result(
            len(docs) >= 24 and not bad_front,
            "ACL00_OBSIDIAN_DELIVERY",
            "phase delivery documentation",
            count=len(docs),
            bad_frontmatter=bad_front,
        )
    )

    mql5 = list(MQL5_ROOT.glob("*.mqh"))
    mql5_errors = []
    for path in mql5:
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in FORBIDDEN_MQL5:
            if token in text:
                mql5_errors.append(f"{path.name}: forbidden {token}")
    checks.append(
        result(
            len(mql5) >= 5 and not mql5_errors,
            "ACL00_MQL5_STATIC",
            "MQL5 non-trading mirror",
            count=len(mql5),
            errors=mql5_errors,
        )
    )

    required = [
        "releases/history/acl_os/manifests/ACL_OS_00_PATCH_MANIFEST.json",
        "releases/history/acl_os/indexes/ACL_OS_00_FILE_INDEX.txt",
        "releases/history/acl_os/hashes/ACL_OS_00_FILE_HASHES.sha256",
        "releases/history/acl_os/readmes/README_ALPHA_LAB_ACL_OS_00.md",
        "releases/history/acl_os/installers/INSTALL_ALPHA_LAB_ACL_OS_00.md",
    ]
    missing = [item for item in required if not (repo / item).is_file()]
    checks.append(
        result(
            not missing,
            "ACL00_REQUIRED_ARTIFACTS",
            "delivery artifacts present",
            missing=missing,
        )
    )
    passed = all(item["passed"] for item in checks)
    return {
        "passed": passed,
        "checks": checks,
        "counts": {"schemas": len(schemas), "docs": len(docs), "mql5": len(mql5)},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    args = parser.parse_args()
    output = validate(args.repo)
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
