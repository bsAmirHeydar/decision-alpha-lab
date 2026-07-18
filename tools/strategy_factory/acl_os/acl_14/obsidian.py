from __future__ import annotations
from pathlib import Path
from .canonical import digest_file,with_digest
from .io import dump_json

def project(root:Path,run:dict,req:dict,contract:dict,readiness:dict,decision:dict,report:dict,handoff:dict)->None:
    docs=root/'docs'
    docs.mkdir(parents=True,exist_ok=True)
    content={
      'ACL14_EXECUTIVE_BRIEF.md': (
          f"# ACL-14 Executive Brief\n\n"
          f"Decision: `{decision['state']}`\n\n"
          f"Real Context evidence present: `{str(req['real_context_evidence_present']).lower()}`\n\n"
          f"Pilot ready: `{str(decision['pilot_ready_non_capital']).lower()}`\n\n"
          "Pilot execution allowed: `false`\n"
      ),
      'ACL14_FIRST_REAL_CONTEXT_PILOT_CONTRACT.md': (
          "# First Real Context Pilot Contract\n\n"
          f"Pilot Contract ID: `{contract['pilot_contract_id']}`\n\n"
          f"Context: `{req['context_id']}@{req['context_version']}`\n\n"
          f"Evidence classification: `{req['evidence_classification']}`\n\n"
          f"Period: `{req['pilot_period']['start_at']}` through `{req['pilot_period']['end_at']}`\n"
      ),
      'ACL14_READINESS_MATRIX.md': "# Pilot Readiness Matrix\n\n"+'\n'.join(f"- `{x['gate_id']}` — `{x['status']}`" for x in readiness['gates'])+'\n',
      'ACL14_LIMITATIONS_AND_NEXT_ACTIONS.md': (
          "# Limitations and Next Actions\n\n"
          "- Reference fixture is not real market evidence.\n"
          "- No prospective outcomes have been observed.\n"
          "- No validation, runtime, live-order or capital authority exists.\n"
          "- Supply approved real data, owner approvals and externally verified availability semantics before rebuilding.\n"
      ),
      'ACL14_ACL15_HANDOFF.md': (
          "# ACL-14 to ACL-15 Handoff\n\n"
          f"Handoff digest: `{handoff['handoff_digest']}`\n\n"
          "Pilot execution materialized: `false`\n"
      ),
    }
    entries=[]
    for name,text in content.items():
        p=docs/name
        p.write_text(text,encoding='utf-8',newline='\n')
        entries.append({'path':f'docs/{name}','digest':digest_file(p)})
    dump_json(docs/'obsidian_projection_manifest.json',with_digest({'schema_version':'1.0.0','pilot_run_id':run['pilot_run_id'],'file_count':len(entries),'files':entries,'generated_projection':True,'source_of_truth':False},'projection_manifest_digest'))
