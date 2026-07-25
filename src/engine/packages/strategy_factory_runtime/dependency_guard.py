from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json, re

_INCLUDE = re.compile(r'#include\s+[<"]([^>"]+)[>"]')

@dataclass(frozen=True, slots=True)
class Violation:
    file: str
    include: str
    reason: str


def load_rules(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def scan_mql5_boundaries(repo_root: Path, rules_path: Path) -> list[Violation]:
    rules = load_rules(rules_path)
    base = repo_root / rules["mql5_root"]
    violations: list[Violation] = []
    forbidden_tokens = tuple(rules["global_forbidden_tokens"])
    for file in sorted(base.rglob("*.mqh")):
        text = file.read_text(encoding="utf-8", errors="ignore")
        rel = file.relative_to(repo_root).as_posix()
        for token in forbidden_tokens:
            if token in text:
                violations.append(Violation(rel, token, "forbidden live authority token"))
        layer = next((x for x in rules["layers"] if f"/{x['name']}/" in f"/{rel}/"), None)
        if not layer:
            continue
        allowed = set(layer["may_include_layers"])
        for inc in _INCLUDE.findall(text):
            target_layer = next((x["name"] for x in rules["layers"] if f"/{x['name']}/" in f"/{inc}/"), None)
            if target_layer and target_layer not in allowed and target_layer != layer["name"]:
                violations.append(Violation(rel, inc, f"{layer['name']} may not include {target_layer}"))
    return violations
