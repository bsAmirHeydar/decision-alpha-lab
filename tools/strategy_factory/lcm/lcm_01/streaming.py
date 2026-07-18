from __future__ import annotations

import csv
import heapq
import json
from collections import Counter
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Any

from .canonical import canonical_json_bytes
from .io import _csv_value

EDGE_FIELDS = [
    "source_path",
    "edge_type",
    "raw_target",
    "line_number",
    "resolution_status",
    "resolved_path",
    "resolution_candidates",
    "resolution_candidate_count",
    "semantic_reachability_claimed",
]


def write_inventory_pair(
    csv_path: Path,
    jsonl_path: Path,
    rows: Iterable[Mapping[str, Any]],
) -> dict:
    """Write CSV and JSONL inventory projections in one bounded-memory pass."""

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    iterator = iter(rows)
    try:
        first = dict(next(iterator))
    except StopIteration:
        raise ValueError("artifact inventory cannot be empty")

    fieldnames = list(first.keys())
    language_counts: Counter[str] = Counter()
    family_counts: Counter[str] = Counter()
    semantic_role_counts: Counter[str] = Counter()
    path_count = 0
    unique_paths: set[str] = set()

    with csv_path.open("w", encoding="utf-8", newline="") as csv_handle, jsonl_path.open(
        "w", encoding="utf-8", newline="\n"
    ) as jsonl_handle:
        writer = csv.DictWriter(
            csv_handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in _prepend(first, iterator):
            record = dict(row)
            writer.writerow({key: _csv_value(record.get(key, "")) for key in fieldnames})
            jsonl_handle.write(canonical_json_bytes(record).decode("utf-8") + "\n")
            path_count += 1
            unique_paths.add(record["path"])
            language_counts[record["language"]] += 1
            family_counts[record["family_candidate"]] += 1
            semantic_role_counts[record["semantic_role_candidate"]] += 1

    return {
        "fieldnames": fieldnames,
        "record_count": path_count,
        "unique_path_count": len(unique_paths),
        "language_counts": dict(sorted(language_counts.items())),
        "family_counts": dict(sorted(family_counts.items())),
        "semantic_role_counts": dict(sorted(semantic_role_counts.items())),
    }


def write_dependency_merge(
    all_path: Path,
    unresolved_path: Path,
    edge_groups: Iterable[list[dict]],
) -> dict:
    """Merge already-sorted scanner outputs without materializing a fifth list."""

    all_path.parent.mkdir(parents=True, exist_ok=True)
    unresolved_path.parent.mkdir(parents=True, exist_ok=True)
    key = lambda row: (
        row["source_path"],
        int(row["line_number"]),
        row["edge_type"],
        row["raw_target"],
    )
    groups = [iter(group) for group in edge_groups]
    merged = heapq.merge(*groups, key=key)
    edge_counts: Counter[str] = Counter()
    resolution_counts: Counter[str] = Counter()
    total = 0
    unresolved_total = 0
    unresolved_statuses = {"UNRESOLVED", "AMBIGUOUS_INTERNAL", "PATH_ESCAPE"}

    with all_path.open("w", encoding="utf-8", newline="") as all_handle, unresolved_path.open(
        "w", encoding="utf-8", newline=""
    ) as unresolved_handle:
        all_writer = csv.DictWriter(
            all_handle,
            fieldnames=EDGE_FIELDS,
            extrasaction="ignore",
            lineterminator="\n",
        )
        unresolved_writer = csv.DictWriter(
            unresolved_handle,
            fieldnames=EDGE_FIELDS,
            extrasaction="ignore",
            lineterminator="\n",
        )
        all_writer.writeheader()
        unresolved_writer.writeheader()
        for row in merged:
            encoded = {field: _csv_value(row.get(field, "")) for field in EDGE_FIELDS}
            all_writer.writerow(encoded)
            total += 1
            edge_counts[row["edge_type"]] += 1
            resolution_counts[row["resolution_status"]] += 1
            if row["resolution_status"] in unresolved_statuses:
                unresolved_writer.writerow(encoded)
                unresolved_total += 1

    return {
        "edge_count": total,
        "unresolved_edge_count": unresolved_total,
        "edge_counts": dict(sorted(edge_counts.items())),
        "resolution_counts": dict(sorted(resolution_counts.items())),
    }


def _prepend(first: Mapping[str, Any], rest: Iterator[Mapping[str, Any]]):
    yield first
    yield from rest


def _csv_rows(path: Path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle)


def write_dependency_merge_from_csv(
    all_path: Path,
    unresolved_path: Path,
    source_paths: list[Path],
) -> dict:
    """Merge deterministic edge CSVs with bounded memory."""

    all_path.parent.mkdir(parents=True, exist_ok=True)
    unresolved_path.parent.mkdir(parents=True, exist_ok=True)

    def key(row: dict):
        return (
            row["source_path"],
            int(row["line_number"] or 0),
            row["edge_type"],
            row["raw_target"],
        )

    iterators = [_csv_rows(path) for path in source_paths]
    merged = heapq.merge(*iterators, key=key)
    edge_counts: Counter[str] = Counter()
    resolution_counts: Counter[str] = Counter()
    total = 0
    unresolved_total = 0
    unresolved_statuses = {"UNRESOLVED", "AMBIGUOUS_INTERNAL", "PATH_ESCAPE"}

    with all_path.open("w", encoding="utf-8", newline="") as all_handle, unresolved_path.open(
        "w", encoding="utf-8", newline=""
    ) as unresolved_handle:
        all_writer = csv.DictWriter(all_handle, fieldnames=EDGE_FIELDS, lineterminator="\n")
        unresolved_writer = csv.DictWriter(
            unresolved_handle, fieldnames=EDGE_FIELDS, lineterminator="\n"
        )
        all_writer.writeheader()
        unresolved_writer.writeheader()
        for row in merged:
            all_writer.writerow({field: row.get(field, "") for field in EDGE_FIELDS})
            total += 1
            edge_counts[row["edge_type"]] += 1
            resolution_counts[row["resolution_status"]] += 1
            if row["resolution_status"] in unresolved_statuses:
                unresolved_writer.writerow(
                    {field: row.get(field, "") for field in EDGE_FIELDS}
                )
                unresolved_total += 1

    return {
        "edge_count": total,
        "unresolved_edge_count": unresolved_total,
        "edge_counts": dict(sorted(edge_counts.items())),
        "resolution_counts": dict(sorted(resolution_counts.items())),
    }


def write_capability_merge(output_path: Path, source_paths: list[Path]) -> dict:
    fields = [
        "path",
        "language",
        "capability_kind",
        "matched_token",
        "line_number",
        "line_digest",
        "risk_indicator_only",
        "live_authority_inferred",
    ]

    def key(row: dict):
        return (
            row["path"],
            int(row["line_number"] or 0),
            row["capability_kind"],
            row["matched_token"],
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    iterators = [_csv_rows(path) for path in source_paths]
    merged = heapq.merge(*iterators, key=key)
    counts: Counter[str] = Counter()
    order_paths: set[str] = set()
    network_paths: set[str] = set()
    total = 0
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in merged:
            writer.writerow({field: row.get(field, "") for field in fields})
            total += 1
            kind = row["capability_kind"]
            counts[kind] += 1
            if kind == "ORDER_API":
                order_paths.add(row["path"])
            if kind == "NETWORK_API":
                network_paths.add(row["path"])
    return {
        "finding_count": total,
        "capability_counts": dict(sorted(counts.items())),
        "order_api_path_count": len(order_paths),
        "network_api_path_count": len(network_paths),
    }


def write_entry_point_merge(output_path: Path, source_paths: list[Path]) -> dict:
    fields = ["path", "entry_point_type", "evidence", "authority_inferred"]

    def key(row: dict):
        return (row["path"], row["entry_point_type"], row["evidence"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = heapq.merge(*[_csv_rows(path) for path in source_paths], key=key)
    total = 0
    last_key = None
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            current = key(row)
            if current == last_key:
                continue
            last_key = current
            writer.writerow({field: row.get(field, "") for field in fields})
            total += 1
    return {"entry_point_count": total}


def write_truncation_merge(output_path: Path, source_paths: list[Path]) -> dict:
    fields = ["path", "observed_edge_count", "retained_edge_count", "reason"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    for path in source_paths:
        rows.extend(_csv_rows(path))
    rows.sort(key=lambda row: (row["path"], row["reason"]))
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})
    return {"truncation_file_count": len(rows)}
