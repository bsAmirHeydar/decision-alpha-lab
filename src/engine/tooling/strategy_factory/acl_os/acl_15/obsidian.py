from __future__ import annotations
from pathlib import Path
from .canonical import digest_file,with_digest
from .io import dump_json

def project(root:Path,run:dict,decision:dict,contracts:dict,ops:dict,handoff:dict)->dict:
    docs={
      'ACL15_EXECUTIVE_BRIEF.md': f"# ACL-15 Executive Brief\n\nState: `{decision['state']}`\n\nThe reference lifecycle is closed without pilot execution, runtime, orders or capital.\n",
      'ACL15_FLEET_REGISTRATION.md': f"# ACL-15 Fleet Registration\n\nFleet: `{contracts['fleet']['fleet_id']}`\n\nPackage status: `{contracts['fleet']['fleet_status']}`\n",
      'ACL15_RETENTION_AND_SURVEILLANCE.md': f"# ACL-15 Retention and Surveillance\n\nRetention: `{ops['retention_status']['status']}`\n\nSurveillance: `{ops['surveillance_status']['status']}`\n",
      'ACL15_CLOSURE_DECISION.md': f"# ACL-15 Closure Decision\n\nDecision: `{decision['decision']}`\n\nNo prospective outcome or capital authority is created.\n",
      'ACL15_REOPEN_AND_MIGRATION.md': '# ACL-15 Reopen and Migration\n\nReopening requires new authority, a new immutable package and new real evidence. Closed history cannot be mutated.\n',
      'ACL15_PROGRAM_CLOSURE.md': f"# ACL-15 Program Closure\n\nHandoff: `{handoff['handoff_type']}`\n\nThe reference program is closed; production readiness is not claimed.\n",
    }
    out=root/'docs'; out.mkdir(parents=True,exist_ok=True)
    for name,text in docs.items():
        (out/name).write_text(text,encoding='utf-8',newline='\n')
    rows=[{'path':'docs/'+name,'digest':digest_file(out/name)} for name in sorted(docs)]
    manifest=with_digest({'schema_version':'1.0.0','fleet_closure_run_id':run['fleet_closure_run_id'],'document_count':len(rows),'documents':rows},'projection_manifest_digest')
    dump_json(out/'obsidian_projection_manifest.json',manifest)
    return manifest
