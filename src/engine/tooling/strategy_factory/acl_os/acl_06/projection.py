from pathlib import Path

def write_docs(root: Path, run: dict, dag: dict, bundle: dict, results: dict, accounting: dict) -> None:
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    summary = f"""# ACL-06 Research Run Summary

- Run ID: `{run['run_id']}`
- Batch ID: `{run['batch_id']}`
- State: `{run['state']}`
- Claim ceiling: `{run['claim_ceiling']}`
- DAG tasks: `{dag['task_count']}`
- Candidate results: `{results['candidate_count']}`
- Research lane: `{results['research_candidate_count']}`
- Diagnostic lane: `{results['diagnostic_candidate_count']}`
- CPU seconds charged: `{accounting['cpu_seconds_charged']}`

This output is descriptive research evidence only. It is not a validation pass, an alpha claim, an execution authorization or a capital decision.
"""
    (docs / "ACL06_RESEARCH_RUN_SUMMARY.md").write_text(summary, encoding="utf-8", newline="\n")
    lines = [
        "# ACL-06 DAG Index",
        "",
        f"Plan: `{dag['plan_id']}`",
        "",
        "| Task | Type | Lane | Segment | Dependencies |",
        "|---|---|---|---|---|",
    ]
    for task in dag["tasks"]:
        lines.append(
            f"| `{task['task_id']}` | {task['task_type']} | {task['lane']} | "
            f"{task.get('segment') or '-'} | {len(task['dependencies'])} |"
        )
    (docs / "RESEARCH_DAG_INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
