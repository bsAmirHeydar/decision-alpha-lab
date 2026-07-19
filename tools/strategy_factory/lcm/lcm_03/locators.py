from __future__ import annotations
from .canonical import digest_object
from .errors import ResolutionError,UnknownVersionError,CollisionError

def build_locators(identities: list[dict]):
    rows=[]
    nouns={'CONTEXT':'contexts','SETUP':'setups','TREATMENT':'treatments','VISUALIZER':'visualizers','ENGINE':'engines','ADAPTER':'adapters','SUPPORT_ARTIFACT':'support'}
    for x in identities:
        logical=f"alpha://{nouns[x['identity_kind']]}/{x['identity_id']}@1"
        row={'identity_id':x['identity_id'],'identity_kind':x['identity_kind'],'semantic_version':'1.0.0','compatibility_range':'>=1.0.0,<2.0.0','logical_uri':logical,'current_artifact_path':x['source_artifact_path'],'current_artifact_sha256':x['source_artifact_sha256'],'materialized_canonical_path':None,'locator_status':'CURRENT_ARTIFACT_BOUND','canonical_path_materialized':False,'authority_class':'REFERENCE_ONLY','runtime_authority':False,'live_order_authority':False,'capital_authority':False,'locator_digest':None}
        row['locator_digest']=digest_object(row,'locator_digest'); rows.append(row)
    return rows

class Resolver:
    def __init__(self, locators: list[dict], alias_index: dict, collision_keys: set[str]|None=None):
        self.locators={x['identity_id']:x for x in locators}; self.alias_index=dict(alias_index); self.collision_keys=collision_keys or set()
    def resolve_identity(self, identity_id: str, version: str='1.0.0'):
        if identity_id not in self.locators: raise ResolutionError('unknown identity')
        if version.split('.')[0] != '1': raise UnknownVersionError('unknown major version')
        return self.locators[identity_id]
    def resolve_alias(self, alias_type: str, scope: str, normalized_value: str):
        key='|'.join([alias_type,scope,normalized_value])
        if key in self.collision_keys: raise CollisionError('alias collision blocks resolution')
        identity=self.alias_index.get(key)
        if not identity: raise ResolutionError('unknown alias')
        return self.resolve_identity(identity)
