import json
from jsonschema import Draft202012Validator
from strategy_factory_contracts_v3 import canonical_sha256
from .helpers import ROOT,CONTEXT,REGISTRY,FIXTURE,load,records

INSTANCE_SCHEMA={
 'feature_catalog.v1.json':'rthp_ai_feature_catalog.schema.json',
 'view_catalog.v1.json':'rthp_ai_view_catalog.schema.json',
 'cluster_rules.v1.json':'rthp_ai_cluster_rules.schema.json',
 'task_references.v1.json':'rthp_ai_task_references.schema.json',
 'label_bindings.v1.json':'rthp_ai_label_bindings.schema.json',
 'data_binding.smoke.v1.json':'rthp_ai_data_binding.schema.json',
 'data_binding.real.template.v1.json':'rthp_ai_data_binding.schema.json',
 'train_activation.v1.json':'rthp_ai_train_activation.schema.json',
 'context_package_manifest.v1.json':'rthp_ai_context_package_manifest.schema.json',
 'research_objectives.v1.json':'rthp_ai_research_objectives.schema.json',
 'discovery_space.v1.json':'rthp_ai_discovery_space.schema.json',
 'known_time_and_leakage.v1.json':'rthp_ai_known_time.schema.json',
 'dataset_join_contract.v1.json':'rthp_ai_dataset_join.schema.json',
}

def test_all_rthp_ai_schemas_are_valid():
 for path in sorted(REGISTRY.glob('rthp_ai_*.schema.json')): Draft202012Validator.check_schema(json.loads(path.read_text()))

def test_all_contract_instances_validate():
 for instance,schema in INSTANCE_SCHEMA.items():
  Draft202012Validator(json.loads((REGISTRY/schema).read_text())).validate(load(instance))
 source_schema=json.loads((REGISTRY/'rthp_ai_source_record.schema.json').read_text()); v=Draft202012Validator(source_schema)
 for row in records(): v.validate(row)

def test_registration_validates_and_all_paths_exist():
 registration=json.loads((REGISTRY/'rthp_ai_input_registration.json').read_text()); schema=json.loads((REGISTRY/'rthp_ai_input_registration.schema.json').read_text()); Draft202012Validator(schema).validate(registration)
 for key in ('source_schema','feature_catalog','view_catalog','cluster_rules','task_references','label_bindings','research_objectives','discovery_space','train_activation'):
  assert (ROOT/registration[key]).is_file()

def test_catalog_digests_recompute_exactly():
 for name,field in [('feature_catalog.v1.json','catalog_digest'),('view_catalog.v1.json','catalog_digest'),('cluster_rules.v1.json','catalog_digest'),('task_references.v1.json','registry_digest'),('label_bindings.v1.json','binding_digest'),('data_binding.smoke.v1.json','binding_digest'),('data_binding.real.template.v1.json','binding_digest'),('train_activation.v1.json','activation_digest')]:
  d=load(name); got=d.pop(field); assert got==canonical_sha256(d)

def test_every_task_resolves_to_exact_label_and_view():
 tasks=load('task_references.v1.json')['tasks']; labels={x['label_contract_id'] for x in load('label_bindings.v1.json')['labels']}; views={x['view_id'] for x in load('view_catalog.v1.json')['views']}
 assert len(tasks)==30 and len({x['task_id'] for x in tasks})==30
 for t in tasks:
  assert t['label_contract_id'] in labels
  assert set(t['allowed_view_ids'])<=views

def test_labels_are_post_cut_only_and_never_features():
 labels=load('label_bindings.v1.json'); features={x['feature_id'] for x in load('feature_catalog.v1.json')['descriptors']}
 assert labels['causal_policy']['post_cut_prices']=='label_only'
 assert all(not x['feature_eligible'] and x['segregated_from_selection'] for x in labels['labels'])
 assert not any(label['label_contract_id'] in features for label in labels['labels'])

def test_real_binding_is_fail_closed_and_smoke_cannot_claim_alpha():
 real=load('data_binding.real.template.v1.json'); smoke=load('data_binding.smoke.v1.json')
 assert real['binding_status']=='EXTERNAL_ARTIFACT_REQUIRED' and real['fail_closed_reason']=='RTHP_REAL_DATA_BINDING_REQUIRED'
 assert all(x['artifact_uri']=='UNRESOLVED' and x['content_hash']=='UNRESOLVED' for x in real['sources'])
 assert smoke['binding_status']=='RESOLVED_SMOKE_ONLY' and smoke['alpha_claim_allowed'] is False

def test_discovery_contract_preserves_context_and_excludes_treatment():
 d=load('discovery_space.v1.json')
 assert 'cycle_definition' in d['versioned_mutable_dimensions']
 assert 'canonical v1 history is immutable' in d['immutable_core']
 assert {'entry_model','stop_loss','target','position_size','capital_allocation'}<=set(d['context_discovery_forbidden_dimensions'])
