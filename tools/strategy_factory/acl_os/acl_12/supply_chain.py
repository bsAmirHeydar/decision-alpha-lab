from __future__ import annotations
import sys
from importlib import metadata
from pathlib import Path
from .canonical import with_digest,digest_file
def _version(name:str)->str:
    try: return metadata.version(name)
    except metadata.PackageNotFoundError: return 'NOT_INSTALLED'
def build_reference_sbom(acl11_root:Path)->dict:
    components=[{'component_id':'python-runtime','name':'Python','version':f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}','component_type':'RUNTIME','source':'LOCAL_ENVIRONMENT_DECLARATION'}, {'component_id':'jsonschema','name':'jsonschema','version':_version('jsonschema'),'component_type':'PYTHON_DEPENDENCY','source':'INSTALLED_DISTRIBUTION'}, {'component_id':'pytest','name':'pytest','version':_version('pytest'),'component_type':'TEST_DEPENDENCY','source':'INSTALLED_DISTRIBUTION'}]
    manifest=acl11_root/'output_manifest.json'
    components.append({'component_id':'acl11-runtime-custody-package','name':'ACL-11 Runtime Custody Package','version':'1.0.0','component_type':'UPSTREAM_ARTIFACT_SET','source_digest':digest_file(manifest)})
    return with_digest({'schema_version':'1.0.0','sbom_id':'ACL12_REFERENCE_SBOM_V1','format':'ALPHA_LAB_REFERENCE_SBOM','component_count':len(components),'components':components,'production_completeness_claimed':False},'sbom_digest')
def build_dependency_recall_graph(sbom:dict,binding:dict)->dict:
    nodes=[{'node_id':c['component_id'],'artifact_digest':c.get('source_digest'),'component_type':c['component_type']} for c in sbom['components']]
    nodes.append({'node_id':'acl12-security-hardening','artifact_digest':binding['binding_digest'],'component_type':'SECURITY_CONTROL_PLANE'})
    edges=[{'from':'acl11-runtime-custody-package','to':'acl12-security-hardening','relation':'CONSUMED_BY'},{'from':'python-runtime','to':'acl12-security-hardening','relation':'EXECUTES'},{'from':'jsonschema','to':'acl12-security-hardening','relation':'VALIDATES_CONTRACTS'}]
    return with_digest({'schema_version':'1.0.0','graph_id':'ACL12_DEPENDENCY_RECALL_GRAPH_V1','nodes':nodes,'edges':edges,'recall_supported':True,'external_registry_lookup_performed':False},'graph_digest')
