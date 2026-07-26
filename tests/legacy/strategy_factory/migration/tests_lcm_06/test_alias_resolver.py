import json
from src.engine.tooling.strategy_factory.lcm.lcm_06.alias_resolver import AliasResolver
def resolver(repo_root): return AliasResolver(json.loads((repo_root/"tests/legacy/strategy_factory/migration/fixtures/lcm_06/aliases/reference_alias_records.json").read_text())["records"])
def test_alias_resolved(repo_root): assert resolver(repo_root).resolve("legacy/simple_context")["resolution_status"]=="RESOLVED"
def test_alias_casefold(repo_root): assert resolver(repo_root).resolve("LEGACY/SIMPLE_CONTEXT")["resolution_status"]=="RESOLVED"
def test_alias_ambiguous(repo_root): assert resolver(repo_root).resolve("legacy/ambiguous")["resolution_status"]=="AMBIGUOUS"
def test_alias_missing(repo_root): assert resolver(repo_root).resolve("legacy/missing")["resolution_status"]=="NOT_FOUND"
