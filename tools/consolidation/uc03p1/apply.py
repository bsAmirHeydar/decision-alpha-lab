from __future__ import annotations

import argparse
import codecs
import hashlib
import json
import os
import shutil
import subprocess
from collections import deque
from pathlib import Path

KEEP_ROOT = {
    '.editorconfig', '.gitattributes', '.gitignore', 'AGENTS.md',
    'CODE_OF_CONDUCT.md', 'COMMIT_MESSAGE.md', 'COMMIT_MESSAGE.txt',
    'CONTRIBUTING.md', 'FILE_INDEX.txt', 'LICENSE', 'PATCH_MANIFEST.json',
    'QA_REPORT.json', 'README.md', 'requirements.txt',
}
TEXT_EXTENSIONS = {
    '.py', '.md', '.txt', '.json', '.jsonl', '.yaml', '.yml', '.toml',
    '.ini', '.cfg', '.csv', '.sha256', '.ps1', '.bat', '.mq5', '.mqh',
    '.xml', '.html', '.js', '.ts', '.tsx', '.jsx', '.sql', '.rst',
    '.properties', '.env', '.lock', '.canvas',
}
EXCLUDED_PARTS = {
    '.git', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    '.venv', 'venv', 'node_modules',
}
EXCLUDED_PREFIXES = (
    'releases/history/',
    'releases/unified_consolidation/uc03/part1/',
    'tools/consolidation/uc03p1/',
    'tests/consolidation/uc03p1/',
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read_rows(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding='utf-8').splitlines()
        if line.strip()
    ]


def atomic_write(path: Path, data: bytes) -> None:
    tmp = path.with_name(path.name + '.uc03tmp')
    tmp.write_bytes(data)
    os.replace(tmp, path)


def clean_generated_caches(repo: Path) -> None:
    roots = (
        repo / 'tools/consolidation/uc03p1',
        repo / 'tests/consolidation/uc03p1',
    )
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root, topdown=False):
            current = Path(dirpath)
            for filename in filenames:
                if filename.endswith('.pyc'):
                    (current / filename).unlink(missing_ok=True)
            for dirname in dirnames:
                if dirname in EXCLUDED_PARTS:
                    shutil.rmtree(current / dirname, ignore_errors=True)


def artifact_type_for(name: str) -> str:
    upper = name.upper()
    suffix = Path(name).suffix.lower()
    if upper.startswith('README'):
        return 'readmes'
    if upper.startswith('INSTALL'):
        return 'installers'
    if upper.startswith('ROLLBACK'):
        return 'rollbacks'
    if upper.startswith('COMMIT_MESSAGE'):
        return 'commit_messages'
    if 'ARTIFACT_INVENTORY' in upper or upper.endswith('_INVENTORY.CSV'):
        return 'inventories'
    if 'FILE_HASHES' in upper or suffix == '.sha256':
        return 'hashes'
    if 'FILE_INDEX' in upper or 'CONTENTS_TREE' in upper:
        return 'indexes'
    if 'MANIFEST' in upper:
        return 'manifests'
    if 'QA_REPORT' in upper or 'AUDIT_REPORT' in upper or upper.endswith('_REPORT.JSON'):
        return 'reports'
    if suffix in {'.ps1', '.bat', '.cmd'} or upper.startswith(('APPLY_', 'EXPAND_', 'RUN_')):
        return 'scripts'
    if suffix in {'.zip', '.7z', '.tar', '.gz'}:
        return 'bundles'
    if suffix in {'.json', '.jsonl', '.yaml', '.yml', '.toml', '.ini', '.cfg'}:
        return 'metadata'
    return 'documents'


def program_for(name: str) -> str:
    upper = name.upper()
    rules = (
        ('ACL_OS', 'acl_os'),
        ('AIEOS', 'aieos'),
        ('ENGINEERING_POLICY', 'engineering_policy'),
        ('ENGINEERING_OS', 'engineering_os'),
        ('LCM', 'lcm'),
        ('RTHP', 'rthp'),
        ('NDS', 'nds'),
        ('SAED', 'saed'),
        ('UCEE', 'ucee'),
        ('STRATEGY_FACTORY', 'strategy_factory'),
        ('EXP0017', 'exp0017'),
        ('EXP0018', 'exp0018'),
        ('EXP0019', 'exp0019'),
        ('SETUP_AI', 'setup_ai'),
        ('MASTER_ARCHITECTURE', 'master_architecture'),
    )
    for token, program in rules:
        if token in upper:
            return program
    return 'misc'


def dynamic_destination(name: str) -> str:
    return (
        Path('releases/history')
        / program_for(name)
        / artifact_type_for(name)
        / name
    ).as_posix()


def unique_conflict_path(repo: Path, destination: Path, digest: str) -> Path:
    conflict_root = repo / 'releases/history/conflicts'
    candidate = conflict_root / destination.parent.name / (
        f'{destination.stem}__{digest[:12]}{destination.suffix}'
    )
    index = 1
    while candidate.exists():
        candidate = conflict_root / destination.parent.name / (
            f'{destination.stem}__{digest[:12]}_{index}{destination.suffix}'
        )
        index += 1
    candidate.parent.mkdir(parents=True, exist_ok=True)
    return candidate


class AhoRewriter:
    def __init__(self, mapping: dict[str, str]) -> None:
        self.patterns = list(mapping)
        self.replacements = [mapping[p] for p in self.patterns]
        self.next: list[dict[str, int]] = [{}]
        self.fail: list[int] = [0]
        self.out: list[list[int]] = [[]]
        for idx, pattern in enumerate(self.patterns):
            state = 0
            for char in pattern:
                if char not in self.next[state]:
                    self.next[state][char] = len(self.next)
                    self.next.append({})
                    self.fail.append(0)
                    self.out.append([])
                state = self.next[state][char]
            self.out[state].append(idx)
        queue = deque(self.next[0].values())
        while queue:
            parent = queue.popleft()
            for char, child in self.next[parent].items():
                queue.append(child)
                fallback = self.fail[parent]
                while fallback and char not in self.next[fallback]:
                    fallback = self.fail[fallback]
                self.fail[child] = self.next[fallback].get(char, 0)
                self.out[child].extend(self.out[self.fail[child]])

    def rewrite(self, text: str) -> tuple[str, int]:
        if not self.patterns:
            return text, 0
        matches: list[tuple[int, int, int]] = []
        state = 0
        for end, char in enumerate(text):
            while state and char not in self.next[state]:
                state = self.fail[state]
            state = self.next[state].get(char, 0)
            for idx in self.out[state]:
                start = end - len(self.patterns[idx]) + 1
                replacement = self.replacements[idx]
                prefix = replacement[:-len(self.patterns[idx])]
                if prefix and start >= len(prefix) and text[start-len(prefix):start] == prefix:
                    continue
                matches.append((start, end + 1, idx))
        if not matches:
            return text, 0
        matches.sort(key=lambda item: (item[0], -(item[1] - item[0]), item[2]))
        selected: list[tuple[int, int, int]] = []
        cursor = -1
        for item in matches:
            if item[0] < cursor:
                continue
            selected.append(item)
            cursor = item[1]
        parts: list[str] = []
        cursor = 0
        for start, end, idx in selected:
            parts.append(text[cursor:start])
            parts.append(self.replacements[idx])
            cursor = end
        parts.append(text[cursor:])
        return ''.join(parts), len(selected)


def iter_text_files(repo: Path):
    active_roots = (
        '.github', 'tools', 'tests', 'lab', 'src', 'contexts', 'adapters',
        'configs', 'ops', 'policies', 'contracts', 'schemas',
        'docs/alpha_lab_master_architecture/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL',
        'docs/alpha_lab_master_architecture/00_START_HERE',
    )
    for relative_root in active_roots:
        root = repo / relative_root
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            rel_dir = Path(dirpath).relative_to(repo).as_posix()
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_PARTS]
            if any(rel_dir == p.rstrip('/') or rel_dir.startswith(p) for p in EXCLUDED_PREFIXES):
                dirnames[:] = []
                continue
            for filename in filenames:
                path = Path(dirpath) / filename
                rel = path.relative_to(repo).as_posix()
                if any(rel.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
                    continue
                if path.suffix.lower() not in TEXT_EXTENSIONS and filename not in {'.gitignore', '.gitattributes'}:
                    continue
                yield path, rel


def decode_text(raw: bytes) -> tuple[str, str, bool] | None:
    if b'\x00' in raw[:4096]:
        return None
    bom = raw.startswith(codecs.BOM_UTF8)
    try:
        return raw.decode('utf-8-sig' if bom else 'utf-8'), 'utf-8', bom
    except UnicodeDecodeError:
        return None


def git_changed_paths(repo: Path) -> set[str] | None:
    if not (repo / '.git').exists():
        return None

    def run(*args: str) -> list[str]:
        result = subprocess.run(
            ['git', '-c', 'core.quotepath=false', *args],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode('utf-8', errors='replace').strip())
        return [
            item.decode('utf-8', errors='surrogateescape').replace('\\', '/')
            for item in result.stdout.split(b'\0')
            if item
        ]

    paths = set(run('diff', '--name-only', '-z'))
    paths.update(run('diff', '--cached', '--name-only', '-z'))
    paths.update(run('ls-files', '--others', '--exclude-standard', '-z'))
    return paths


def apply(repo: Path) -> dict:
    repo = repo.resolve()
    release = repo / 'releases/unified_consolidation/uc03/part1'
    release.mkdir(parents=True, exist_ok=True)
    rows = read_rows(release / 'ROOT_RELOCATION_MAP.jsonl')

    row_by_source: dict[str, dict] = {str(row['source']): dict(row) for row in rows}
    for path in sorted(repo.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file() or path.name in KEEP_ROOT:
            continue
        if path.name not in row_by_source:
            row_by_source[path.name] = {
                'source': path.name,
                'destination': dynamic_destination(path.name),
                'program': program_for(path.name),
                'artifact_type': artifact_type_for(path.name),
                'sha256': sha256(path),
                'map_origin': 'RUNTIME_HEAD',
            }

    moved: list[dict] = []
    active_mapping: dict[str, str] = {}
    conflict_paths: list[str] = []

    for source_name in sorted(row_by_source):
        row = row_by_source[source_name]
        source = repo / source_name
        destination = repo / str(row['destination'])
        destination.parent.mkdir(parents=True, exist_ok=True)

        status = 'ABSENT_IN_CHECKOUT'
        runtime_hash = None
        if source.is_file():
            runtime_hash = sha256(source)
            if destination.is_file():
                destination_hash = sha256(destination)
                if destination_hash == runtime_hash:
                    source.unlink()
                    status = 'DUPLICATE_SOURCE_REMOVED'
                else:
                    conflict = unique_conflict_path(repo, destination, destination_hash)
                    shutil.move(str(destination), str(conflict))
                    conflict_paths.append(conflict.relative_to(repo).as_posix())
                    shutil.move(str(source), str(destination))
                    status = 'MOVED_DESTINATION_CONFLICT_PRESERVED'
            else:
                shutil.move(str(source), str(destination))
                status = 'MOVED'
        elif destination.is_file():
            runtime_hash = sha256(destination)
            status = 'ALREADY_MOVED'

        if destination.is_file():
            destination_hash = sha256(destination)
            if runtime_hash is not None and destination_hash != runtime_hash:
                raise RuntimeError(f'byte preservation failed: {source_name}')
            active_mapping[source_name] = destination.relative_to(repo).as_posix()
            moved_row = dict(row)
            moved_row.update({
                'status': status,
                'runtime_sha256': destination_hash,
                'frozen_sha256_advisory_only': row.get('sha256'),
            })
            moved.append(moved_row)

    # Catch any root file introduced after the map was frozen.
    for path in sorted(repo.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file() or path.name in KEEP_ROOT:
            continue
        destination = repo / dynamic_destination(path.name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        before = sha256(path)
        if destination.exists() and sha256(destination) != before:
            conflict = unique_conflict_path(repo, destination, sha256(destination))
            shutil.move(str(destination), str(conflict))
            conflict_paths.append(conflict.relative_to(repo).as_posix())
        if path.exists():
            shutil.move(str(path), str(destination))
        if sha256(destination) != before:
            raise RuntimeError(f'byte preservation failed: {path.name}')
        active_mapping[path.name] = destination.relative_to(repo).as_posix()
        moved.append({
            'source': path.name,
            'destination': destination.relative_to(repo).as_posix(),
            'program': program_for(path.name),
            'artifact_type': artifact_type_for(path.name),
            'status': 'MOVED_RUNTIME_DISCOVERY',
            'runtime_sha256': before,
            'map_origin': 'RUNTIME_HEAD',
        })

    receipt_root = repo / 'registry/consolidation/uc03/part1'
    receipt_root.mkdir(parents=True, exist_ok=True)
    relocation_receipt = receipt_root / 'root_relocation_receipt.json'
    rewrite_receipt = receipt_root / 'reference_rewrite_receipt.json'
    stage_receipt = receipt_root / 'part1_exit_decision.json'

    previous_rewrites: dict[str, dict] = {}
    if rewrite_receipt.is_file():
        try:
            prior = json.loads(rewrite_receipt.read_text(encoding='utf-8'))
            previous_rewrites = {str(item['path']): item for item in prior.get('files', [])}
        except Exception:
            previous_rewrites = {}

    rewriter = AhoRewriter(active_mapping)
    new_rewrites: list[dict] = []
    for path, rel in iter_text_files(repo):
        raw = path.read_bytes()
        decoded = decode_text(raw)
        if decoded is None:
            continue
        text, encoding, bom = decoded
        updated, count = rewriter.rewrite(text)
        if not count or updated == text:
            continue
        before = hashlib.sha256(raw).hexdigest()
        payload = updated.encode(encoding)
        if bom:
            payload = codecs.BOM_UTF8 + payload
        atomic_write(path, payload)
        new_rewrites.append({
            'path': rel,
            'replacement_count': count,
            'before_sha256': before,
            'after_sha256': hashlib.sha256(payload).hexdigest(),
        })

    root_files = sorted(path.name for path in repo.iterdir() if path.is_file())
    unexpected = sorted(set(root_files) - KEEP_ROOT)
    if unexpected:
        raise RuntimeError(f'root cleanup incomplete: {unexpected}')

    combined_rewrites = dict(previous_rewrites)
    combined_rewrites.update({item['path']: item for item in new_rewrites})
    rewrites = [combined_rewrites[path] for path in sorted(combined_rewrites)]

    relocation_receipt.write_text(json.dumps({
        'schema_version': '1.1.0',
        'program_id': 'UCPS',
        'stage_id': 'UC-03',
        'part_id': 'UC03-P1',
        'status': 'PASS',
        'relocation_count': len(moved),
        'moved_count': len(moved),
        'retained_root_count': len(root_files),
        'retained_root_files': root_files,
        'conflict_preservation_paths': sorted(conflict_paths),
        'relocations': moved,
        'hash_policy': 'RUNTIME_SOURCE_TO_DESTINATION_BYTE_EQUALITY',
        'frozen_map_hashes': 'ADVISORY_ONLY',
        'semantic_change_authority': False,
        'deletion_authority': False,
    }, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    rewrite_receipt.write_text(json.dumps({
        'schema_version': '1.1.0',
        'status': 'PASS',
        'modified_file_count': len(rewrites),
        'replacement_count': sum(item['replacement_count'] for item in rewrites),
        'files': rewrites,
    }, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    stage_receipt.write_text(json.dumps({
        'schema_version': '1.1.0',
        'program_id': 'UCPS',
        'stage_id': 'UC-03',
        'part_id': 'UC03-P1',
        'status': 'ACCEPTED',
        'uc03_part2_authorized': True,
        'uc04_authorized': False,
        'semantic_merge_authority': False,
        'deletion_authority': False,
    }, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    clean_generated_caches(repo)

    index_path = release / 'PATCH_FILE_INDEX.txt'
    changed = git_changed_paths(repo)
    if changed is None:
        static_index = release / 'STATIC_PATCH_FILE_INDEX.txt'
        commit_paths = {
            line.strip().replace('\\', '/')
            for line in static_index.read_text(encoding='utf-8').splitlines()
            if line.strip() and '__pycache__' not in line and '.pytest_cache' not in line and not line.endswith('.pyc')
        }
        for item in moved:
            commit_paths.add(str(item['source']))
            commit_paths.add(str(item['destination']))
        commit_paths.update(item['path'] for item in rewrites)
        commit_paths.update(conflict_paths)
        commit_paths.update({
            relocation_receipt.relative_to(repo).as_posix(),
            rewrite_receipt.relative_to(repo).as_posix(),
            stage_receipt.relative_to(repo).as_posix(),
            index_path.relative_to(repo).as_posix(),
        })
    else:
        commit_paths = set(changed)
        commit_paths.add(index_path.relative_to(repo).as_posix())

    index_path.write_text('\n'.join(sorted(commit_paths)) + '\n', encoding='utf-8')

    # Include the newly written index itself and refresh against real Git state.
    refreshed = git_changed_paths(repo)
    if refreshed is not None:
        refreshed.add(index_path.relative_to(repo).as_posix())
        index_path.write_text('\n'.join(sorted(refreshed)) + '\n', encoding='utf-8')
        commit_paths = refreshed

    return {
        'status': 'PASS',
        'relocation_count': len(moved),
        'moved_count': len(moved),
        'rewrite_file_count': len(rewrites),
        'replacement_count': sum(item['replacement_count'] for item in rewrites),
        'root_file_count': len(root_files),
        'commit_path_count': len(commit_paths),
        'conflict_count': len(conflict_paths),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo-root', default='.')
    args = parser.parse_args()
    result = apply(Path(args.repo_root))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
