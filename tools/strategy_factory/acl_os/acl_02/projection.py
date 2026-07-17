from __future__ import annotations
from pathlib import Path

def render_readiness(report: dict) -> str:
    lines = [
        "---",
        f"title: {report['context_id']} Context Intake Readiness",
        f"status: {report['decision'].lower()}",
        "tags: [acl-os, acl-02, generated, context-readiness]",
        "---",
        "",
        f"# {report['context_id']} — Context Intake Readiness",
        "",
        "> [!warning] Generated projection",
        "> This note is generated from the machine-readable readiness report. Do not edit it by hand.",
        "",
        "## Decision",
        "",
        f"- Decision: `{report['decision']}`",
        f"- Highest state: `{report['highest_state']}`",
        f"- Completeness: `{report['completeness_score']:.2%}`",
        f"- Blocking findings: `{report['blocking_count']}`",
        f"- Warnings: `{report['warning_count']}`",
        f"- Claim ceiling: `{report['claim_ceiling']}`",
        "",
        "## Blocking findings",
        "",
    ]
    if not report["blocking_findings"]:
        lines.append("- None.")
    for finding in report["blocking_findings"]:
        lines.append(
            f"- `{finding['code']}` — `{finding['path']}` — {finding['message']}  \n"
            f"  Remediation: {finding['remediation']}"
        )
    lines += ["", "## Warnings", ""]
    if not report["warning_findings"]:
        lines.append("- None.")
    for finding in report["warning_findings"]:
        lines.append(f"- `{finding['code']}` — `{finding['path']}` — {finding['message']}")
    lines += ["", "## Stage gates", ""]
    for name, stage in report["stages"].items():
        lines.append(f"- `{name}`: **{'READY' if stage.get('ready') else 'BLOCKED'}**")
    lines += [
        "",
        "## Related",
        "",
        "- [[ACL_02_CONTEXT_STANDARD_AND_INTAKE]]",
        "- [[CONTEXT_PACKAGE_STANDARD]]",
        "- [[CONTEXT_READINESS_REPORT]]",
        "",
    ]
    return "\n".join(lines)

def write_projection(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_readiness(report), encoding="utf-8")
