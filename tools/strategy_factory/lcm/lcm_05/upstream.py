from .io import read_json,read_jsonl
from .canonical import digest_object,sha256_bytes
from .errors import IntegrityError
def latest_characterization(repo):
    roots=sorted((repo/'registry/legacy_context_migration/characterizations').glob('CHARACTERIZATION_*'))
    if not roots:raise IntegrityError("LCM-04 package not found")
    return roots[-1]
def verify_manifest(root,manifest):
    for rec in manifest.get('artifacts',[]):
        p=root/rec['path']
        if not p.is_file():raise IntegrityError(f"missing upstream artifact: {rec['path']}")
        if sha256_bytes(p.read_bytes())!=rec['sha256']:raise IntegrityError(f"upstream hash mismatch: {rec['path']}")
    return True
def load(repo):
    char=latest_characterization(repo);marker=read_json(char/'characterization_marker.json');handoff=read_json(char/'handoff/lcm04_to_lcm05_handoff.json');manifest=read_json(char/'output_manifest.json');receipt=read_json(char/'characterization_receipt.json');verify_manifest(char,manifest)
    if digest_object(handoff,'handoff_digest')!=handoff['handoff_digest']:raise IntegrityError('LCM04 handoff digest invalid')
    if receipt['handoff_digest']!=handoff['handoff_digest']:raise IntegrityError('LCM04 receipt binding invalid')
    ident_root=repo/'registry/legacy_context_migration/identities'/handoff['identity_run_id'];class_root=repo/'registry/legacy_context_migration/classifications'/read_json(ident_root/'input/lcm02_binding.json')['classification_id'];survey_id=read_json(class_root/'reports/classification_summary.json')['survey_id'];survey_root=repo/'registry/legacy_context_migration/surveys'/survey_id
    return {"characterization_root":char,"marker":marker,"handoff":handoff,"manifest":manifest,"receipt":receipt,"identity_root":ident_root,"classification_root":class_root,"survey_root":survey_root,"identities":read_jsonl(ident_root/'identities/canonical_identity_candidates.jsonl'),"ambiguities":read_jsonl(ident_root/'unresolved/identity_ambiguity_queue.jsonl'),"classifications":read_jsonl(class_root/'artifacts/artifact_classification_records.jsonl')}
