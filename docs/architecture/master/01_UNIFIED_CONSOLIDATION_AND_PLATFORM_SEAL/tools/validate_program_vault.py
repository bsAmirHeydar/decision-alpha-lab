#!/usr/bin/env python3
"""Validate the Unified Consolidation and Platform Seal Obsidian program."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

REQUIRED_FRONTMATTER = {
    "id", "title", "type", "status", "domain", "version", "created", "updated", "tags"
}
WIKI_RE = re.compile(r"\[\[([^\]]+)\]\]")
ID_RE = re.compile(r"^id:\s*([^\s]+)\s*$", re.MULTILINE)
FORBIDDEN_TEXT = ("src/alpha_lab/",)
STAGE_RE = re.compile(r"^\d{2}_UC(\d{2})_.*\.md$")


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing_frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated_frontmatter")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter_not_mapping")
    return data, text[end + 5 :]


def normalize_wikilink(raw: str) -> str:
    return raw.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/").removesuffix(".md")


def hash_variants(path: Path) -> set[str]:
    raw = path.read_bytes()
    variants = {hashlib.sha256(raw).hexdigest()}
    if b"\x00" in raw[:4096]:
        return variants
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    body = raw[3:] if had_bom else raw
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        return variants
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    for newline in ("\n", "\r\n"):
        payload = normalized.replace("\n", newline).encode("utf-8")
        variants.add(hashlib.sha256(payload).hexdigest())
        variants.add(hashlib.sha256(b"\xef\xbb\xbf" + payload).hexdigest())
    return variants


def hash_matches(path: Path, expected: str) -> bool:
    return expected.lower() in hash_variants(path)


def main() -> int:
    program = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]).resolve()
    vault = program.parent.resolve()

    def looks_like_repository(candidate: Path) -> bool:
        return (
            (candidate / "README.md").is_file()
            and (candidate / "src/engine").is_dir()
            and (candidate / "registry/consolidation/uc03/part3/uc04_handoff.json").is_file()
        )

    repo = next(
        (
            candidate
            for candidate in (vault, *vault.parents)
            if ((candidate / ".git").exists() and (candidate / "src/engine").is_dir())
            or looks_like_repository(candidate)
        ),
        None,
    )
    if repo is None:
        print(f"ERROR: repository root not found from {program}")
        return 2
    errors: list[str] = []
    warnings: list[str] = []

    release_integrity_policy_path = repo / "registry/consolidation/release_integrity/policy_v1.json"
    immutable_prefixes: tuple[str, ...] = ()
    immutable_exact_paths: set[str] = set()
    if release_integrity_policy_path.is_file():
        try:
            release_policy = json.loads(release_integrity_policy_path.read_text(encoding="utf-8-sig"))
            immutable_prefixes = tuple(str(item) for item in release_policy.get("immutable_prefixes", []))
            immutable_exact_paths = {str(item) for item in release_policy.get("immutable_exact_paths", [])}
        except Exception as exc:
            errors.append(f"invalid release integrity policy: {exc}")

    def is_release_immutable(relative: str) -> bool:
        normalized = relative.replace("\\", "/")
        return normalized in immutable_exact_paths or any(normalized.startswith(prefix) for prefix in immutable_prefixes)

    if not program.is_dir():
        print(f"ERROR: program root not found: {program}")
        return 2

    md_files = sorted(program.rglob("*.md"))
    if len(md_files) < 80:
        errors.append(f"program note count unexpectedly low: {len(md_files)}")

    # Build vault-wide indexes to catch collisions and resolve full-path links.
    vault_md = sorted(vault.rglob("*.md"))
    path_index = {p.relative_to(vault).with_suffix("").as_posix().lower(): p for p in vault_md}
    canvas_index = {p.relative_to(vault).as_posix().lower(): p for p in vault.rglob("*.canvas")}
    all_ids: dict[str, Path] = {}
    program_ids: dict[str, Path] = {}

    for p in vault_md:
        text = p.read_text(encoding="utf-8")
        match = ID_RE.search(text)
        if match:
            note_id = match.group(1)
            prior = all_ids.get(note_id)
            if prior and (p.is_relative_to(program) or prior.is_relative_to(program)):
                errors.append(
                    f"duplicate note id {note_id}: {prior.relative_to(vault)} / {p.relative_to(vault)}"
                )
            all_ids[note_id] = p

    for p in md_files:
        rel = p.relative_to(program).as_posix()
        text = p.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"empty note: {rel}")
            continue
        try:
            fm, body = split_frontmatter(text)
        except Exception as exc:
            errors.append(f"invalid frontmatter {rel}: {exc}")
            continue
        missing = sorted(REQUIRED_FRONTMATTER - set(fm))
        if missing:
            errors.append(f"missing frontmatter keys {rel}: {missing}")
        if fm.get("domain") != "unified-consolidation-platform-seal":
            errors.append(f"wrong domain {rel}: {fm.get('domain')}")
        note_id = str(fm.get("id", ""))
        if not note_id.startswith("UCPS-"):
            errors.append(f"invalid program note id {rel}: {note_id}")
        prior = program_ids.get(note_id)
        if prior:
            errors.append(f"duplicate program note id {note_id}: {prior} / {rel}")
        program_ids[note_id] = p
        if not re.search(r"^#\s+\S", body, re.MULTILINE):
            errors.append(f"missing H1: {rel}")
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in text:
                errors.append(f"forbidden program expansion or nested product path in {rel}: {forbidden}")
        for raw in WIKI_RE.findall(text):
            target = normalize_wikilink(raw)
            if not target:
                continue
            key = target.lower()
            if key not in path_index and key not in canvas_index and (key + ".canvas") not in canvas_index:
                errors.append(f"broken or non-full-path wikilink in {rel}: [[{raw}]]")

    # MOC completeness: each section MOC must reference every sibling markdown note.
    for section in sorted(p for p in program.iterdir() if p.is_dir() and re.match(r"^\d{2}_", p.name) and p.name != "00_START_HERE"):
        moc = section / "00_MOC.md"
        if not moc.exists():
            errors.append(f"missing MOC: {section.name}")
            continue
        moc_text = moc.read_text(encoding="utf-8")
        targets = {normalize_wikilink(x).lower() for x in WIKI_RE.findall(moc_text)}
        for note in sorted(section.glob("*.md")):
            if note == moc:
                continue
            target = note.relative_to(vault).with_suffix("").as_posix().lower()
            if target not in targets:
                errors.append(f"MOC missing note {section.name}: {note.name}")

    # Exactly seven stage notes and stage metadata/order.
    stage_dir = program / "03_EXECUTION_STAGES"
    stage_notes = []
    for p in sorted(stage_dir.glob("*.md")):
        match = STAGE_RE.match(p.name)
        if match and 1 <= int(match.group(1)) <= 7:
            stage_notes.append(p)
    if len(stage_notes) != 7:
        errors.append(f"expected exactly seven stage notes, found {len(stage_notes)}")
    for expected, p in enumerate(stage_notes, 1):
        fm, _ = split_frontmatter(p.read_text(encoding="utf-8"))
        if fm.get("stage_id") != f"UC-{expected:02d}":
            errors.append(f"stage id mismatch {p.name}: {fm.get('stage_id')}")
        if fm.get("execution_order") != expected:
            errors.append(f"stage order mismatch {p.name}: {fm.get('execution_order')}")

    # Machine-readable data.
    data_dir = program / "_data"
    required_data = {
        "program_manifest.yaml", "canonical_topology.yaml", "stage_gate_matrix.yaml",
        "artifact_disposition_vocabulary.yaml", "quality_bar.yaml", "context_lifecycle.yaml",
        "document_authority.yaml",
    }
    present = {p.name for p in data_dir.glob("*.yaml")}
    if present != required_data:
        errors.append(f"data file set mismatch; missing={sorted(required_data-present)} extra={sorted(present-required_data)}")
    loaded: dict[str, dict] = {}
    for name in sorted(required_data & present):
        try:
            obj = yaml.safe_load((data_dir / name).read_text(encoding="utf-8"))
            if not isinstance(obj, dict):
                raise ValueError("root_not_mapping")
            loaded[name] = obj
        except Exception as exc:
            errors.append(f"invalid YAML {name}: {exc}")
    manifest = loaded.get("program_manifest.yaml", {})
    if manifest.get("stage_count") != 7 or len(manifest.get("stages", [])) != 7:
        errors.append("program manifest does not declare exactly seven stages")
    if manifest.get("phase_expansion_allowed") is not False:
        errors.append("program manifest must disable phase expansion")
    topology_text = (data_dir / "canonical_topology.yaml").read_text(encoding="utf-8") if (data_dir / "canonical_topology.yaml").exists() else ""
    if "src/engine" not in topology_text or "src/alpha_lab" in topology_text:
        errors.append("canonical topology must use src/engine and must not create src/alpha_lab")

    # Canvas references.
    canvas_path = program / "Unified_Consolidation_Program.canvas"
    try:
        canvas = json.loads(canvas_path.read_text(encoding="utf-8"))
        if len(canvas.get("nodes", [])) < 10 or len(canvas.get("edges", [])) < 8:
            errors.append("canvas is incomplete")
        for node in canvas.get("nodes", []):
            file_ref = node.get("file")
            if file_ref and not (vault / file_ref).exists():
                errors.append(f"canvas references missing file: {file_ref}")
    except Exception as exc:
        errors.append(f"invalid canvas: {exc}")

    # UC-03 physical relocation map. Historical foundation indexes keep their
    # original paths; this map resolves them to the accepted physical targets.
    relocation_map: dict[str, str] = {}
    for receipt_path in (
        repo / "registry/consolidation/uc03/part1/root_relocation_receipt.json",
        repo / "registry/consolidation/uc03/part2/code_relocation_receipt.json",
        repo / "registry/consolidation/uc03/part3/documentation_relocation_receipt.json",
        repo / "registry/consolidation/uc03/part3/registry_relocation_receipt.json",
    ):
        if not receipt_path.is_file():
            continue
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
            if receipt.get("status") != "PASS":
                errors.append(f"relocation receipt is not PASS: {receipt_path.relative_to(repo)}")
                continue
            for row in receipt.get("relocations", []):
                source = str(row.get("source", "")).replace("\\", "/")
                destination = str(row.get("destination", "")).replace("\\", "/")
                if source and destination:
                    relocation_map[source] = destination
        except Exception as exc:
            errors.append(f"invalid relocation receipt {receipt_path.relative_to(repo)}: {exc}")

    def resolve_delivery_path(relative: str) -> Path:
        return repo / relocation_map.get(relative.replace("\\", "/"), relative.replace("\\", "/"))

    # Delivery controls and hash ledger.
    # Later accepted consolidation patches may amend a bounded subset of the
    # foundation files. The original ledger remains authoritative for every
    # non-amended path; the amendment file supplies the exact replacement hash.
    amendment_hashes: dict[str, list[str]] = {}

    def add_amendment(relative: str, digest: str) -> None:
        if relative and digest:
            amendment_hashes.setdefault(relative, []).append(digest.lower())

    amendment_path = repo / "releases/unified_consolidation/uc03/part1/OBSIDIAN_AMENDMENT.json"
    if amendment_path.is_file():
        try:
            amendment = json.loads(amendment_path.read_text(encoding="utf-8"))
            if amendment.get("program_id") != "UCPS" or amendment.get("part_id") != "UC03-P1":
                errors.append("invalid UC-03 Part 1 Obsidian amendment identity")
            for row in amendment.get("amended_paths", []):
                add_amendment(str(row.get("path", "")), str(row.get("sha256", "")))
        except Exception as exc:
            errors.append(f"invalid UC-03 Part 1 Obsidian amendment: {exc}")

    for receipt_path in (
        repo / "registry/consolidation/uc03/part1/reference_rewrite_receipt.json",
        repo / "registry/consolidation/uc03/part2/compatibility_rewrite_receipt.json",
        repo / "registry/consolidation/uc03/part3/reference_rewrite_receipt.json",
    ):
        if not receipt_path.is_file():
            continue
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
            if receipt.get("status") != "PASS":
                errors.append(f"rewrite receipt is not PASS: {receipt_path.relative_to(repo)}")
                continue
            for row in receipt.get("files", []):
                add_amendment(str(row.get("path", "")), str(row.get("after_sha256", "")))
        except Exception as exc:
            errors.append(f"invalid rewrite receipt {receipt_path.relative_to(repo)}: {exc}")

    recovery_amendment = repo / "releases/unified_consolidation/ci_recovery_02/OBSIDIAN_FOUNDATION_AMENDMENT.json"
    if recovery_amendment.is_file():
        try:
            payload = json.loads(recovery_amendment.read_text(encoding="utf-8"))
            for row in payload.get("amended_paths", []):
                add_amendment(str(row.get("path", "")), str(row.get("sha256", "")))
        except Exception as exc:
            errors.append(f"invalid CI recovery Obsidian amendment: {exc}")

    part3_amendment = repo / "releases/unified_consolidation/uc03/part3/OBSIDIAN_FOUNDATION_AMENDMENT.json"
    if part3_amendment.is_file():
        try:
            payload = json.loads(part3_amendment.read_text(encoding="utf-8-sig"))
            if payload.get("program_id") != "UCPS" or payload.get("part_id") != "UC03-P3":
                errors.append("invalid UC-03 Part 3 Obsidian amendment identity")
            for row in payload.get("amended_paths", []):
                digest = str(row.get("sha256", ""))
                add_amendment(str(row.get("historical_path", "")), digest)
                add_amendment(str(row.get("path", "")), digest)
        except Exception as exc:
            errors.append(f"invalid UC-03 Part 3 Obsidian amendment: {exc}")

    uc04_w0_amendment = repo / "registry/consolidation/uc04/w0/uc03_post_closure_amendment.json"
    if uc04_w0_amendment.is_file():
        try:
            payload = json.loads(uc04_w0_amendment.read_text(encoding="utf-8-sig"))
            if payload.get("program_id") != "UCPS" or payload.get("stage_id") != "UC04-W0" or payload.get("status") != "PASS":
                errors.append("invalid UC04-W0 post-closure amendment identity")
            for row in payload.get("records", []):
                if row.get("semantic_change") is not False:
                    errors.append(f"UC04-W0 semantic change is forbidden: {row.get('path')}")
                digest = str(row.get("current_sha256", "")).removeprefix("sha256:")
                add_amendment(str(row.get("path", "")), digest)
        except Exception as exc:
            errors.append(f"invalid UC04-W0 post-closure amendment: {exc}")

    uc04_obsidian_amendment = repo / "registry/consolidation/uc04/w0/obsidian_foundation_amendment.json"
    if uc04_obsidian_amendment.is_file():
        try:
            payload = json.loads(uc04_obsidian_amendment.read_text(encoding="utf-8-sig"))
            if payload.get("program_id") != "UCPS" or payload.get("stage_id") != "UC04-W0" or payload.get("status") != "PASS":
                errors.append("invalid UC04-W0 Obsidian foundation amendment identity")
            for row in payload.get("records", []):
                if row.get("semantic_change") is not False:
                    errors.append(f"UC04-W0 Obsidian semantic change is forbidden: {row.get('current_path')}")
                digest = str(row.get("current_sha256", "")).removeprefix("sha256:")
                add_amendment(str(row.get("historical_path", "")), digest)
                add_amendment(str(row.get("current_path", "")), digest)
        except Exception as exc:
            errors.append(f"invalid UC04-W0 Obsidian foundation amendment: {exc}")

    release = program / "_release"
    required_release = {
        "COMMIT_MESSAGE.txt",
        "UCPS_OBSIDIAN_FOUNDATION_FILE_INDEX.txt",
        "UCPS_OBSIDIAN_FOUNDATION_FILE_HASHES.sha256",
        "UCPS_OBSIDIAN_FOUNDATION_PATCH_MANIFEST.json",
        "UCPS_OBSIDIAN_FOUNDATION_QA_REPORT.json",
        "UCPS_OBSIDIAN_FOUNDATION_ARTIFACT_INVENTORY.csv",
    }
    release_present = {p.name for p in release.iterdir() if p.is_file()} if release.is_dir() else set()
    if release_present != required_release:
        errors.append(f"release control set mismatch; missing={sorted(required_release-release_present)} extra={sorted(release_present-required_release)}")
    index_path = release / "UCPS_OBSIDIAN_FOUNDATION_FILE_INDEX.txt"
    ledger_path = release / "UCPS_OBSIDIAN_FOUNDATION_FILE_HASHES.sha256"
    if index_path.exists():
        indexed = [line.strip().replace("\\", "/") for line in index_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(indexed) != 103 or len(set(indexed)) != 103:
            errors.append(f"file index must contain 103 unique paths, found {len(indexed)} / {len(set(indexed))}")
        for rel in indexed:
            if not resolve_delivery_path(rel).is_file():
                errors.append(f"indexed delivery path missing after relocation: {rel}")
    else:
        indexed = []
    if ledger_path.exists():
        ledger_lines = [line for line in ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(ledger_lines) != 102:
            errors.append(f"hash ledger must contain 102 entries, found {len(ledger_lines)}")
        for line in ledger_lines:
            try:
                expected, rel = line.split("  ", 1)
                target = resolve_delivery_path(rel)
                if not target.is_file():
                    errors.append(f"hash-ledger target missing after relocation: {rel}")
                    continue
                if not hash_matches(target, expected):
                    resolved_rel = relocation_map.get(rel.replace("\\", "/"), rel.replace("\\", "/"))
                    amended = [*amendment_hashes.get(rel, []), *amendment_hashes.get(resolved_rel, [])]
                    if not any(hash_matches(target, candidate) for candidate in amended):
                        resolved_rel = relocation_map.get(rel.replace("\\", "/"), rel.replace("\\", "/"))
                        if is_release_immutable(resolved_rel):
                            errors.append(f"hash mismatch: {rel}")
            except Exception as exc:
                errors.append(f"invalid hash ledger line: {line}: {exc}")
    manifest_path = release / "UCPS_OBSIDIAN_FOUNDATION_PATCH_MANIFEST.json"
    if manifest_path.exists():
        try:
            delivery_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if delivery_manifest.get("total_path_count") != 103 or delivery_manifest.get("deleted_file_count") != 0:
                errors.append("delivery manifest counts or deletion claim are invalid")
        except Exception as exc:
            errors.append(f"invalid delivery manifest: {exc}")
    inventory_path = release / "UCPS_OBSIDIAN_FOUNDATION_ARTIFACT_INVENTORY.csv"
    if inventory_path.exists():
        with inventory_path.open(encoding="utf-8", newline="") as handle:
            inventory_rows = list(csv.DictReader(handle))
        if len(inventory_rows) != 103:
            errors.append(f"artifact inventory must contain 103 rows, found {len(inventory_rows)}")

    # Required master-vault integrations.
    required_links = {
        vault / "00_START_HERE/00_Home.md": "17_Unified_Consolidation_And_Platform_Seal",
        vault / "00_START_HERE/01_Quick_Start.md": "17_Unified_Consolidation_And_Platform_Seal",
        vault / "00_MASTER_ARCHITECTURE/13_Implementation_Program.md": "01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL",
        vault / "context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/00_START_HERE/00_LCM_HOME.md": "01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL",
    }
    for path, token in required_links.items():
        if token not in path.read_text(encoding="utf-8"):
            errors.append(f"missing master-vault integration: {path.relative_to(vault)}")

    print(f"Program root: {program}")
    print(f"Markdown notes: {len(md_files)}")
    print(f"Program note IDs: {len(program_ids)}")
    print(f"Machine data files: {len(present)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    for item in errors[:100]:
        print("ERROR:", item)
    for item in warnings[:30]:
        print("WARN :", item)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
