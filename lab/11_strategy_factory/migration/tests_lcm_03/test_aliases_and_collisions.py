import pytest
from tools.strategy_factory.lcm.lcm_03.io import read_json,read_jsonl
from tools.strategy_factory.lcm.lcm_03.locators import Resolver
from tools.strategy_factory.lcm.lcm_03.errors import CollisionError,UnknownVersionError

def _resolver(root):
    loc=list(read_jsonl(root/'locators/artifact_locator_records.jsonl'));idx=read_json(root/'aliases/alias_resolution_index.json')['index'];cols=read_json(root/'collisions/alias_collision_report.json')['collisions'];keys={'|'.join([x['alias_type'],x['alias_scope'],x['normalized_alias_value']]) for x in cols};return Resolver(loc,idx,keys),loc,cols

def test_legacy_path_coverage(identity_root):
    aliases=list(read_jsonl(identity_root/'aliases/legacy_alias_records.jsonl'));summary=read_json(identity_root/'reports/identity_summary.json');assert sum(x['alias_type']=='LEGACY_PATH' for x in aliases)==summary['active_candidate_count']
def test_collision_records_blocked(identity_root):
    aliases=list(read_jsonl(identity_root/'aliases/legacy_alias_records.jsonl'));assert all(x['alias_status']=='AMBIGUOUS_BLOCKED' for x in aliases if x['resolution_status']=='AMBIGUOUS_BLOCKED')
def test_collision_resolver_rejects(identity_root):
    r,_,cols=_resolver(identity_root)
    if cols:
        c=cols[0]
        with pytest.raises(CollisionError): r.resolve_alias(c['alias_type'],c['alias_scope'],c['normalized_alias_value'])
def test_unknown_version_fails(identity_root):
    r,loc,_=_resolver(identity_root)
    with pytest.raises(UnknownVersionError): r.resolve_identity(loc[0]['identity_id'],'2.0.0')
def test_valid_identity_resolves(identity_root):
    r,loc,_=_resolver(identity_root);assert r.resolve_identity(loc[0]['identity_id'])['logical_uri'].startswith('alpha://')
def test_index_excludes_blocked(identity_root):
    idx=read_json(identity_root/'aliases/alias_resolution_index.json')['index'];cols=read_json(identity_root/'collisions/alias_collision_report.json')['collisions'];assert all('|'.join([c['alias_type'],c['alias_scope'],c['normalized_alias_value']]) not in idx for c in cols)
