from collections import Counter
from .io import read_json,read_jsonl
from .canonical import digest_object,sha256_bytes
from .path_policy import validate,casefold_key
from .authority import verify_permit
from .errors import IntegrityError
def verify_package(root):
    marker=read_json(root/'topology_marker.json');handoff=read_json(root/'handoff/lcm05_to_lcm06_handoff.json');receipt=read_json(root/'topology_receipt.json');manifest=read_json(root/'output_manifest.json')
    for rec in manifest['artifacts']:
        p=root/rec['path']
        if not p.is_file() or p.stat().st_size!=rec['size_bytes'] or sha256_bytes(p.read_bytes())!=rec['sha256']:raise IntegrityError(f"manifest mismatch: {rec['path']}")
    if digest_object(manifest,'output_manifest_digest')!=manifest['output_manifest_digest']:raise IntegrityError('manifest digest')
    if digest_object(marker,'marker_digest')!=marker['marker_digest']:raise IntegrityError('marker digest')
    if digest_object(handoff,'handoff_digest')!=handoff['handoff_digest']:raise IntegrityError('handoff digest')
    verify_permit(read_json(root/'authority/authority_permit.json'),marker['source_handoff_digest'])
    maps=read_jsonl(root/'mappings/artifact_target_map.jsonl');identities=read_jsonl(root/'mappings/identity_target_map.jsonl');roots=read_jsonl(root/'root_relocation/root_relocation_plan.jsonl');ambiguities=read_jsonl(root/'mappings/identity_ambiguity_target_queue.jsonl')
    if len(maps)!=marker['artifact_mapping_count']:raise IntegrityError('artifact map count')
    file_entries=[];package_entries=[]
    for m in maps:
        validate(m['target_path']);file_entries.append((m['artifact_path'],m['target_path']))
        if any(m[k] for k in ['source_move_authorized','source_delete_authorized','semantic_refactor_authorized','cutover_authorized','runtime_authorized','live_order_authorized','capital_authorized']):raise IntegrityError('authority escalation')
    for m in roots:validate(m['target_path']);file_entries.append((m['source_path'],m['target_path']))
    for m in ambiguities:validate(m['target_path']);file_entries.append((m['source_artifact_path'],m['target_path']))
    for m in identities:validate(m['target_package_root']);package_entries.append((m['identity_id'],m['target_package_root']))
    by={}
    for source,target in file_entries:by.setdefault(casefold_key(target),set()).add(source.casefold())
    pby={}
    for source,target in package_entries:pby.setdefault(casefold_key(target),set()).add(source)
    collisions=[k for k,v in by.items() if len(v)>1]+[k for k,v in pby.items() if len(v)>1]
    collision_report=read_json(root/'collisions/target_path_collision_report.json')
    if collision_report['casefold_collision_count']!=len(collisions):raise IntegrityError('collision report mismatch')
    if receipt['handoff_digest']!=handoff['handoff_digest']:raise IntegrityError('receipt binding')
    return {"passed":True,"topology_run_id":marker['topology_run_id'],"artifact_mapping_count":len(maps),"identity_mapping_count":len(identities),"manifest_artifact_count":manifest['artifact_count'],"casefold_collision_count":len(collisions)}
