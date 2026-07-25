from __future__ import annotations
import json,re
from pathlib import Path
from .canonical import digest_file
from .identity import build_artifact_id
from .policies import PolicyBundle
from .registry import RepositoryRegistry
from .types import ArtifactDescriptor,ArtifactIdentity,ArtifactMutability
from .io import save_registry
from ..common import REPO_ROOT


def _name(stem:str)->str:
    out=stem.replace('.schema','-schema').replace('_','-').lower()
    out=re.sub(r'[^a-z0-9_-]+','-',out).strip('-_')
    return out


def build(repo_root:Path=REPO_ROOT)->RepositoryRegistry:
    policies=PolicyBundle.load(repo_root/'registry/acl_os/acl_01/policies/v1')
    reg=RepositoryRegistry(policies)
    owner_id='OWNER_ACL_OS_CORE'
    reg.owners[owner_id]={"tenant_id":"system","display_name":"ACL-OS Core Maintainers","roles":["SCHEMA_STEWARD","POLICY_STEWARD","TECHNICAL_OWNER","PLUGIN_OWNER","SECURITY_OWNER"],"status":"ACTIVE","review_routes":["acl-os-core","security"]}
    for path in sorted((repo_root/'registry/acl_os/acl_01/schemas/v1').glob('*.schema.json')):
        obj=json.loads(path.read_text(encoding='utf-8')); sid=obj['$id']; rel=path.relative_to(repo_root).as_posix(); digest=digest_file(path)
        reg.schemas[sid]={"tenant_id":"system","version":"1.0.0","path":rel,"digest":digest,"status":"ACTIVE"}
        name=_name(path.stem); aid=build_artifact_id('system','acl-os','schema',name,'1.0.0')
        reg.artifacts[aid]=ArtifactDescriptor(ArtifactIdentity(aid,'system','acl-os','schema',name,'1.0.0',digest),'registry',rel,'contracts',owner_id,sid,'INTERNAL',ArtifactMutability.AUTHORED,metadata={"schema_semver":"1.0.0","visibility":"PUBLIC","interfaces":{"schema.read":"1.0.0"}})
    reg.revision=len(reg.artifacts)+len(reg.schemas)+1
    return reg


def main(argv=None)->int:
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,default=REPO_ROOT/'registry/acl_os/acl_01/reference/bootstrap_registry.json'); p.add_argument('--repo-root',type=Path,default=REPO_ROOT); args=p.parse_args(argv)
    reg=build(args.repo_root); save_registry(args.output,reg); print(json.dumps({"passed":True,"output":str(args.output),"artifacts":len(reg.artifacts),"schemas":len(reg.schemas),"registry_digest":reg.digest,"live_order_submission_allowed":False,"capital_activation_allowed":False},indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
