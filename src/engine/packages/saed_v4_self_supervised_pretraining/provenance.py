from __future__ import annotations
import platform,sys
from .canonical import content_hash, stable_id

def build_sbom(source_files:list[str])->dict:
    payload={"phase":"SAED_V4_11","format":"decision-alpha-lab-sbom-v1","runtime":{"python_implementation":platform.python_implementation(),"python_major_minor":f'{sys.version_info.major}.{sys.version_info.minor}'},"dependencies":[{"name":"python-standard-library","scope":"runtime","required":True},{"name":"pytest","scope":"qa","required":True},{"name":"jsonschema","scope":"qa","required":True}],"source_files":sorted(source_files),"external_network_required":False,"pickle_or_opaque_binary_checkpoint":False,"checkpoint_format":"canonical_json"}
    payload['sbom_id']=stable_id('v411sbom',payload);payload['sbom_hash']=content_hash(payload);return payload
