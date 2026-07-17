from __future__ import annotations
import json, shutil, tempfile
from pathlib import Path
from typing import Any
from .artifact_manifest import build_output_manifest
from .authority import validate_authority
from .candidate_freeze import freeze_candidates, freeze_search_space
from .canonical import canonical_bytes, digest_object, stable_id, with_digest
from .contracts import compile_dataset_snapshot, validate_batch_request, validate_compute_budget, validate_environment_lock, validate_label_contract, validate_split_contract
from .errors import IntegrityError, PublicationError
from .event_ledger import EventLedger, verify_event_ledger
from .handoff import build_acl06_handoff
from .handoff_input import load_acl04_bundle
from .io import atomic_publish, dump_json, require_clean_output
from .lineage import build_provenance
from .object_store import ContentAddressedStore
from .policies import CLAIM_CEILING, FACTORY_VERSION
from .projection import write_summary
from .schema_validation import validate_instance
from .security import evaluate_security

class ACL05ImmutableBatchService:
    """Build one deterministic, immutable ACL-05 research batch from exact ACL-04 artifacts."""
    def build(self,*,acl04_root: Path,output_root: Path,fixture_root: Path,authority_permit: dict[str,Any],batch_request: dict[str,Any],dataset_documents: list[dict[str,Any]],label_documents: list[dict[str,Any]],split_contract: dict[str,Any],environment_lock: dict[str,Any],compute_budget: dict[str,Any]) -> dict[str,Any]:
        output_root=output_root.resolve()
        if output_root.exists() and any(output_root.iterdir()): raise PublicationError("output root must be empty")
        bundle=load_acl04_bundle(acl04_root); handoff=bundle["handoff"]
        authority_report=validate_authority(authority_permit,handoff)
        request=validate_batch_request(batch_request,handoff)
        budget=validate_compute_budget(compute_budget)
        environment=validate_environment_lock(environment_lock)
        candidate_freeze=freeze_candidates(bundle["candidates"],request)
        search_freeze=freeze_search_space(bundle["exposure"],bundle["dedup"],candidate_freeze)
        compiled_snapshots=[]; dataset_payloads={}
        for doc in dataset_documents:
            snapshot,payload=compile_dataset_snapshot(doc,fixture_root)
            compiled_snapshots.append(snapshot); dataset_payloads[snapshot["snapshot_id"]]=payload
        if not compiled_snapshots: raise IntegrityError("at least one dataset snapshot required")
        snapshots_by_id={s["snapshot_id"]:s for s in compiled_snapshots}
        if len(snapshots_by_id)!=len(compiled_snapshots): raise IntegrityError("duplicate dataset snapshot id")
        dataset_set_body={"schema_version":"1.0.0","snapshots":sorted(compiled_snapshots,key=lambda x:x["snapshot_id"]),"snapshot_count":len(compiled_snapshots),"known_time_verified":True}
        dataset_set=with_digest(dataset_set_body,"dataset_snapshot_set_digest")
        labels=[]
        for doc in label_documents:
            sid=doc["dataset_snapshot_id"]
            if sid not in snapshots_by_id: raise IntegrityError("label references unknown dataset")
            labels.append(validate_label_contract(doc,snapshots_by_id[sid]))
        if not any(x["role"]=="PRIMARY" for x in labels): raise IntegrityError("primary label contract required")
        label_set_body={"schema_version":"1.0.0","labels":sorted(labels,key=lambda x:x["label_id"]),"label_count":len(labels),"diagnostic_labels_segregated":all(x["role"]!="DIAGNOSTIC" or x["segregated_from_selection"] for x in labels)}
        label_set=with_digest(label_set_body,"label_contract_set_digest")
        split=validate_split_contract(split_contract,compiled_snapshots[0])
        binding_body={"schema_version":"1.0.0","context_id":handoff["context_id"],"context_version":handoff["context_version"],"acl04_handoff_digest":handoff["handoff_digest"],"acl04_factory_receipt_digest":bundle["receipt"]["receipt_digest"],"acl04_output_manifest_digest":bundle["manifest"]["manifest_digest"],"acl04_candidate_set_digest":bundle["candidate_set_digest"],"acl04_deduplication_report_digest":bundle["dedup"]["report_digest"],"acl04_search_exposure_ledger_digest":bundle["exposure"]["ledger_digest"],"acl04_provenance_graph_digest":bundle["provenance"]["graph_digest"],"acl03_handoff_digest":handoff["upstream_acl03_handoff_digest"],"candidate_behavior_mutable":False,"upstream_semantics_mutable":False}
        binding=with_digest(binding_body,"binding_digest")
        security=evaluate_security(Path(__file__).parent)
        if not security["passed"]: raise IntegrityError("ACL05 security isolation failed")
        staging=Path(tempfile.mkdtemp(prefix=".acl05-staging-",dir=str(output_root.parent)))
        try:
            (staging/".acl05_generated_root").write_text("ACL-05 GENERATED ROOT — DO NOT HAND EDIT\n",encoding="utf-8",newline="\n")
            store=ContentAddressedStore(staging/"store",budget["max_store_objects"],budget["max_store_bytes"])
            for c in sorted(bundle["candidates"],key=lambda x:x["setup_id"]):
                store.put(logical_id=c["setup_id"],artifact_class="ACL04_CANONICAL_CANDIDATE",media_type="application/json",payload=canonical_bytes(c)+b"\n",semantic_digest=c["candidate_digest"],source_path=f"ACL04:candidates/canonical/{c['setup_id']}.json")
            for snapshot in compiled_snapshots:
                store.put(logical_id=snapshot["snapshot_id"],artifact_class="DATASET_SNAPSHOT_BYTES",media_type=snapshot["media_type"],payload=dataset_payloads[snapshot["snapshot_id"]],semantic_digest=snapshot["snapshot_digest"],source_path=snapshot["source_path"])
            material_docs=[("ACL04_BINDING","ACL04_BINDING",binding,"binding_digest"),("BATCH_REQUEST","BATCH_REQUEST",request,"request_digest"),("CANDIDATE_FREEZE","CANDIDATE_FREEZE_SET",candidate_freeze,"candidate_freeze_digest"),("SEARCH_SPACE_FREEZE","SEARCH_SPACE_FREEZE",search_freeze,"search_space_freeze_digest"),("DATASET_SNAPSHOT_SET","DATASET_SNAPSHOT_SET",dataset_set,"dataset_snapshot_set_digest"),("LABEL_CONTRACT_SET","LABEL_CONTRACT_SET",label_set,"label_contract_set_digest"),(split["split_id"],"SPLIT_CONTRACT",split,"split_digest"),(environment["environment_id"],"ENVIRONMENT_LOCK",environment,"environment_digest"),(budget["budget_id"],"COMPUTE_BUDGET",budget,"budget_digest")]
            for logical,klass,doc,field in material_docs:
                store.put(logical_id=logical,artifact_class=klass,media_type="application/json",payload=canonical_bytes(doc)+b"\n",semantic_digest=doc[field],source_path="ACL05:material-contract")
            object_index=store.index(); validate_instance("object_index",object_index)
            identity_material={"schema_version":"1.0.0","batch_key":request["batch_key"],"context_id":handoff["context_id"],"context_version":handoff["context_version"],"acl04_binding_digest":binding["binding_digest"],"candidate_freeze_digest":candidate_freeze["candidate_freeze_digest"],"search_space_freeze_digest":search_freeze["search_space_freeze_digest"],"dataset_snapshot_set_digest":dataset_set["dataset_snapshot_set_digest"],"label_contract_set_digest":label_set["label_contract_set_digest"],"split_digest":split["split_digest"],"environment_digest":environment["environment_digest"],"budget_digest":budget["budget_digest"],"object_index_digest":object_index["object_index_digest"],"frozen_at":request["frozen_at"]}
            batch_id=stable_id("BATCH",digest_object(identity_material),length=32)
            batch_body={**identity_material,"batch_id":batch_id,"owner":request["owner"],"purpose":request["purpose"],"state":"FROZEN","claim_ceiling":CLAIM_CEILING,"material_mutation_allowed":False,"candidate_regeneration_allowed":False,"alpha_claim_allowed":False,"live_order_submission_allowed":False,"capital_activation_allowed":False}
            batch=with_digest(batch_body,"batch_definition_digest"); validate_instance("batch_definition",batch)
            ledger=EventLedger(batch_id)
            for event_type,payload in [
              ("ACL04_HANDOFF_ACCEPTED",{"handoff_digest":handoff["handoff_digest"]}),
              ("CANDIDATE_UNIVERSE_FROZEN",{"candidate_freeze_digest":candidate_freeze["candidate_freeze_digest"]}),
              ("SEARCH_SPACE_FROZEN",{"search_space_freeze_digest":search_freeze["search_space_freeze_digest"]}),
              ("DATA_AND_LABEL_CONTRACTS_BOUND",{"dataset_snapshot_set_digest":dataset_set["dataset_snapshot_set_digest"],"label_contract_set_digest":label_set["label_contract_set_digest"]}),
              ("ENVIRONMENT_AND_BUDGET_BOUND",{"environment_digest":environment["environment_digest"],"budget_digest":budget["budget_digest"]}),
              ("CONTENT_ADDRESSED_OBJECTS_WRITTEN",{"object_index_digest":object_index["object_index_digest"]}),
              ("RESEARCH_BATCH_FROZEN",{"batch_id":batch_id,"batch_definition_digest":batch["batch_definition_digest"]}),
            ]: ledger.append(event_type,payload,request["frozen_at"])
            event_ledger=ledger.document()
            if not verify_event_ledger(event_ledger): raise IntegrityError("event ledger hash chain invalid")
            provenance=build_provenance(batch_id=batch_id,handoff=handoff,binding=binding,candidate_freeze=candidate_freeze,search_freeze=search_freeze,datasets=dataset_set,labels=label_set,split=split,environment=environment,budget=budget,object_index=object_index)
            batch_manifest_body={"schema_version":"1.0.0","batch_id":batch_id,"state":"FROZEN","material_digests":sorted([binding["binding_digest"],request["request_digest"],candidate_freeze["candidate_freeze_digest"],search_freeze["search_space_freeze_digest"],dataset_set["dataset_snapshot_set_digest"],label_set["label_contract_set_digest"],split["split_digest"],environment["environment_digest"],budget["budget_digest"],object_index["object_index_digest"],event_ledger["ledger_digest"],provenance["graph_digest"]]),"research_candidate_count":candidate_freeze["research_count"],"diagnostic_candidate_count":candidate_freeze["diagnostic_count"],"immutable":True}
            batch_manifest=with_digest(batch_manifest_body,"batch_manifest_digest")
            freeze_receipt_body={"schema_version":"1.0.0","factory_version":FACTORY_VERSION,"batch_id":batch_id,"batch_definition_digest":batch["batch_definition_digest"],"batch_manifest_digest":batch_manifest["batch_manifest_digest"],"authority_report_digest":authority_report["report_digest"],"event_ledger_digest":event_ledger["ledger_digest"],"claim_ceiling":CLAIM_CEILING,"frozen":True,"live_order_submission_allowed":False,"capital_activation_allowed":False}
            freeze_receipt=with_digest(freeze_receipt_body,"freeze_receipt_digest")
            acl06=build_acl06_handoff(batch=batch,manifest=batch_manifest,receipt_digest=freeze_receipt["freeze_receipt_digest"],candidate_freeze=candidate_freeze,search_freeze=search_freeze,datasets=dataset_set,labels=label_set,split=split,environment=environment,budget=budget,object_index=object_index,event_ledger=event_ledger,provenance=provenance)
            integrity_body={"schema_version":"1.0.0","batch_id":batch_id,"acl04_bundle_verified":True,"candidate_payloads_unchanged":True,"known_time_verified":True,"manifest_closed":True,"event_chain_verified":True,"cas_byte_addressing_verified":True,"all_material_digests_bound":True,"passed":True}
            integrity=with_digest(integrity_body,"report_digest")
            paths={
              "binding/acl04_binding.json":binding,"authority/authority_report.json":authority_report,"batch/batch_request.json":request,"batch/candidate_freeze_set.json":candidate_freeze,"batch/search_space_freeze.json":search_freeze,"batch/dataset_snapshot_set.json":dataset_set,"batch/label_contract_set.json":label_set,"batch/split_contract.json":split,"batch/environment_lock.json":environment,"batch/compute_budget.json":budget,"batch/batch_definition.json":batch,"batch/batch_manifest.json":batch_manifest,"batch/freeze_receipt.json":freeze_receipt,"store/object_index.json":object_index,"events/batch_event_ledger.json":event_ledger,"lineage/batch_provenance_graph.json":provenance,"reports/integrity_report.json":integrity,"reports/security_isolation_report.json":security,"handoff/acl06_handoff.json":acl06}
            for rel,doc in paths.items(): dump_json(staging/rel,doc)
            write_summary(staging,batch,candidate_freeze,dataset_set,label_set,split,environment,budget,object_index)
            output_manifest=build_output_manifest(staging,batch_id); dump_json(staging/"output_manifest.json",output_manifest)
            receipt_body={"schema_version":"1.0.0","factory_version":FACTORY_VERSION,"batch_id":batch_id,"batch_definition_digest":batch["batch_definition_digest"],"batch_manifest_digest":batch_manifest["batch_manifest_digest"],"freeze_receipt_digest":freeze_receipt["freeze_receipt_digest"],"acl06_handoff_digest":acl06["handoff_digest"],"output_manifest_digest":output_manifest["manifest_digest"],"claim_ceiling":CLAIM_CEILING,"live_order_submission_allowed":False,"capital_activation_allowed":False}
            receipt=with_digest(receipt_body,"receipt_digest"); dump_json(staging/"batch_receipt.json",receipt)
            atomic_publish(staging,output_root)
        except Exception:
            shutil.rmtree(staging,ignore_errors=True); raise
        return {"passed":True,"batch_id":batch_id,"research_candidate_count":candidate_freeze["research_count"],"diagnostic_candidate_count":candidate_freeze["diagnostic_count"],"object_count":object_index["object_count"],"object_bytes":object_index["total_bytes"],"batch":batch,"candidate_freeze":candidate_freeze,"search_freeze":search_freeze,"dataset_set":dataset_set,"label_set":label_set,"split":split,"environment":environment,"budget":budget,"object_index":object_index,"event_ledger":event_ledger,"provenance":provenance,"batch_manifest":batch_manifest,"freeze_receipt":freeze_receipt,"handoff":acl06,"output_manifest":output_manifest,"receipt":receipt,"output_root":str(output_root)}
