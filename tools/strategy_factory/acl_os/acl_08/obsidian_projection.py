from __future__ import annotations


def front(title: str, report_id: str, tags: str) -> str:
    return (
        "---\n"
        f"title: {title}\n"
        "status: generated-reference\n"
        f"report_id: {report_id}\n"
        f"tags: [{tags}]\n"
        "---\n"
    )


def summary_md(run: dict, batch: dict, executive: dict) -> str:
    counts = "\n".join(
        f"- **{key}**: {value}" for key, value in sorted(batch["decision_counts"].items())
    )
    return (
        front("ACL-08 Reporting Summary", run["report_id"], "acl-os, acl-08, generated")
        + "# ACL-08 Reporting Summary\n\n"
        + "> [!warning] Claim ceiling\n"
        + f"> `{run['claim_ceiling']}`. This report grants no alpha, promotion, execution or capital authority.\n\n"
        + "## Answer first\n\n"
        + executive["answer_first"]
        + "\n\n## Identity\n\n"
        + f"- Report: `{run['report_id']}`\n"
        + f"- Validation: `{run['validation_id']}`\n"
        + f"- Run: `{run['run_id']}`\n"
        + f"- Batch: `{run['batch_id']}`\n\n"
        + "## Decision distribution\n\n"
        + counts
        + "\n\n## Navigation\n\n"
        + "- [[EXECUTIVE_SUMMARY]]\n"
        + "- [[CANDIDATE_REPORT_INDEX]]\n"
        + "- [[EXPERIENCE_LEDGER]]\n"
        + "- [[LIMITATIONS_AND_UNKNOWN]]\n"
    )


def executive_md(executive: dict) -> str:
    findings = "\n".join(f"- {item}" for item in executive["key_findings"])
    return (
        front("ACL-08 Executive Summary", executive["report_id"], "acl-os, acl-08, executive")
        + "# Executive Summary\n\n"
        + executive["answer_first"]
        + "\n\n## Findings\n\n"
        + findings
        + "\n"
    )


def index_md(reports: list[dict]) -> str:
    report_id = reports[0]["report_id"] if reports else "UNKNOWN"
    lines = [
        front("ACL-08 Candidate Report Index", report_id, "acl-os, acl-08, candidates"),
        "# Candidate Report Index",
        "",
    ]
    for report in reports:
        lines.append(
            f"- [[candidates/{report['setup_id']}|{report['setup_id']}]] — "
            f"`{report['decision_status']}` — {report['origin']} / {report['lane']}"
        )
    return "\n".join(lines) + "\n"


def candidate_md(report: dict) -> str:
    lines = [
        front(
            f"Candidate {report['setup_id']}",
            report["report_id"],
            "acl-os, acl-08, candidate",
        ),
        f"# {report['setup_id']}",
        "",
        f"- Decision: `{report['decision_status']}`",
        f"- Origin: `{report['origin']}`",
        f"- Lane: `{report['lane']}`",
        f"- Promotion allowed: `{str(report['promotion_allowed']).lower()}`",
        "",
        "## Reason codes",
        "",
    ]
    lines.extend(f"- `{code}`" for code in report["reason_codes"])
    lines.extend(["", "## Gate vector", "", "| Gate | Status |", "|---|---|"])
    lines.extend(f"| {gate['gate_id']} | {gate['status']} |" for gate in report["gates"])
    return "\n".join(lines) + "\n"


def experience_md(bundle: dict, records: list[dict]) -> str:
    lines = [
        front("ACL-08 Experience Ledger", bundle["report_id"], "acl-os, acl-08, experience"),
        "# Experience Ledger",
        "",
        "> [!note] Boundary",
        "> These records are not yet research memory. ACL-09 must ingest and govern them.",
        "",
        "## Class counts",
        "",
    ]
    lines.extend(f"- **{key}**: {value}" for key, value in sorted(bundle["experience_counts"].items()))
    lines.extend(["", "## Records", ""])
    lines.extend(
        f"- `{record['experience_id']}` — {record['setup_id']} — `{record['experience_class']}`"
        for record in records
    )
    return "\n".join(lines) + "\n"


def limitations_md(batch: dict) -> str:
    limitations = "\n".join(f"- {item}" for item in batch["limitations"])
    required = "\n".join(f"- `{item}`" for item in batch["required_next_evidence"])
    return (
        front("ACL-08 Limitations and Unknowns", batch["report_id"], "acl-os, acl-08, limitations")
        + "# Limitations and Unknowns\n\n"
        + limitations
        + "\n\n## Required next evidence categories\n\n"
        + required
        + "\n"
    )
