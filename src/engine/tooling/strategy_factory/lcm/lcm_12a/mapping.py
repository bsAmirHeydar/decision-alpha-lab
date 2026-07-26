from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from .canonical import digest_object, stable_id, slug

def proposed_target(row,authority):
    path=row["path"]
    if path.startswith("docs/architecture/master/"):
        return path,"NO_MOVE_CANONICAL_TOPOLOGY"
    name=Path(path).name
    identity_token=row["document_id"].split("_",1)[-1][:12].lower()
    phase="GENERAL"
    for token in name.replace("-","_").split("_"):
        if token.startswith("LCM") and any(c.isdigit() for c in token):phase=token;break
    if name.startswith(("README_","INSTALL_","ROLLBACK_","COMMIT_MESSAGE_")) or name.endswith("_ARTIFACT_INVENTORY.csv"):
        return f"docs/history/delivery/releases/legacy_migration/{phase.lower()}/{identity_token}_{name}","PROPOSED_RELEASE_EVIDENCE_RELOCATION"
    if authority=="GENERATED_PROJECTION":
        return f"docs/history/generated/{slug(row['topic_key']).lower()}/{identity_token}_{name}","PROPOSED_GENERATED_BOUNDARY"
    if authority=="SUPPORTING_EVIDENCE":
        return f"docs/operations/evidence/{slug(row['topic_key']).lower()}/{identity_token}_{name}","PROPOSED_SUPPORTING_EVIDENCE_BOUNDARY"
    return path,"NO_APPROVED_TARGET"

def build_map(rows,authority_rows,exact_membership,normalized_membership,entity_refs,inbound_counts,contradictions):
    auth={x["document_id"]:x for x in authority_rows};conflicted=set()
    for c in contradictions:conflicted.update((c["left_document_id"],c["right_document_id"]))
    mappings=[];targets=defaultdict(list)
    for row in rows:
        exact=exact_membership.get(row["document_id"]);norm=normalized_membership.get(row["document_id"])
        group=exact or norm
        canonical_id=group["canonical_document_id"] if group else row["document_id"]
        canonical_path=group["canonical_path"] if group else row["path"]
        authority=auth[row["document_id"]]["authority_class"]
        target,reason=proposed_target(row,authority)
        refs=entity_refs[row["document_id"]]
        issues=[]
        if authority=="UNKNOWN":issues.append("AUTHORITY_UNKNOWN")
        if auth[row["document_id"]]["owner"]=="UNASSIGNED_OWNER":issues.append("OWNER_UNKNOWN")
        if row["document_id"] in conflicted:issues.append("CONTRADICTION_OWNER_DECISION_REQUIRED")
        if refs["unknown"]:issues.append("UNVALIDATED_ENTITY_REFERENCE")
        relocation=(not issues and authority in {"CANONICAL","SUPPORTING_EVIDENCE","GENERATED_PROJECTION","DUPLICATE","SUPERSEDED"})
        redirect_required=bool(inbound_counts.get(row["path"],0)) and target!=row["path"]
        rec={"mapping_id":stable_id("DOCMAPREC",row["document_id"],canonical_id,target),"document_id":row["document_id"],"source_path":row["path"],"source_digest":row["byte_digest"],"authority_class":authority,"canonical_document_id":canonical_id,"canonical_path":canonical_path,"contract_version":row["declared_version"],"associated_entity_ids":refs["valid"],"unvalidated_entity_references":refs["unknown"],"proposed_target_path":target,"target_rationale":reason,"inbound_reference_count":inbound_counts.get(row["path"],0),"redirect_required":redirect_required,"relocation_approved":relocation,"relocation_blockers":issues,"move_performed":False,"delete_performed":False,"validation_status":"PASS" if relocation or issues else "UNKNOWN"}
        rec["mapping_digest"]=digest_object(rec,"mapping_digest");mappings.append(rec);targets[target].append(rec)
    collisions=[]
    for target,members in targets.items():
        canonical={m["canonical_document_id"] for m in members if m["relocation_approved"]}
        if len(canonical)>1:
            collisions.append({"collision_id":stable_id("DOCTARGETCOLLISION",target),"target_path":target,"mapping_ids":[m["mapping_id"] for m in members],"canonical_document_ids":sorted(canonical),"validation_status":"FAILED"})
            for m in members:
                m["relocation_approved"]=False;m["relocation_blockers"].append("PROPOSED_TARGET_COLLISION");m["validation_status"]="FAILED";m["mapping_digest"]=digest_object(m,"mapping_digest")
    return mappings,collisions
