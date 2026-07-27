import json
from pathlib import Path
from strategy_factory_onboarding_v3.contracts import FeatureSpec,ViewSpec,CapabilityDeclaration,ContextSpecification
from strategy_factory_onboarding_v3.enums import ContextKind,MigrationWave,CapabilityDecision,InvarianceStatus
from strategy_factory_onboarding_v3.generator import ContextGenerator
from strategy_factory_onboarding_v3.invariance import snapshot,compare
from strategy_factory_onboarding_v3.tournament_template import default_template,compile_template
from strategy_factory_rthp_context_v1.preflight import run_preflight
from .helpers import ROOT,CONTEXT,FIXTURE,load

def spec_from_json():
 d=load('uce_i16_context_spec.v1.json'); caps=tuple(CapabilityDeclaration(x['capability_id'],CapabilityDecision(x['decision']),x['reason'],x['scope']) for x in d['capabilities'])
 return ContextSpecification(d['context_id'],d['version'],d['display_name'],ContextKind(d['kind']),MigrationWave(d['wave']),d['doctrine_hash'],tuple(d['source_hashes']),tuple(FeatureSpec(x['feature_id'],x['dtype'],x['known_time_rule'],x['required'],x['default'],x['description']) for x in d['features']),tuple(ViewSpec(x['view_id'],tuple(x['feature_ids']),tuple(x['shape']),x['causal'],x['optional']) for x in d['views']),tuple(d['lifecycle_states']),tuple(d['cluster_rule_ids']),tuple(d['task_ids']),d['manual_policy_id'],caps,tuple(d['legacy_source_paths']),tuple(d['exception_ids']))

def test_smoke_preflight_passes_with_zero_conformance_findings():
 r=run_preflight(FIXTURE)
 assert r['status']=='PASS' and r['accepted_record_count']==6
 assert r['context_package_conformance']['passed'] and r['context_package_conformance']['findings']==[]
 assert r['compiled_view_count']==30 and r['cluster_assignment_count']==24

def test_real_preflight_blocks_only_on_external_binding():
 r=run_preflight(FIXTURE,real_data_binding=CONTEXT/'data_binding.real.template.v1.json',require_real_data=True)
 assert r['status']=='BLOCKED'
 assert 'real_data_binding_required' in r['real_data_binding_blockers']
 assert r['context_package_conformance']['passed']

def test_uce_i16_spec_and_generator_are_deterministic(tmp_path):
 spec=spec_from_json(); stored=load('uce_i16_context_spec.v1.json')
 assert spec.spec_hash==stored['spec_hash'] and len(spec.task_ids)==30
 core=snapshot(ROOT); a=ContextGenerator().build(spec,core); b=ContextGenerator().build(spec,core)
 assert a[0].manifest_hash==b[0].manifest_hash and a[1]==b[1] and a[2].compiled_hash==b[2].compiled_hash
 assert len(a[1])==15

def test_tournament_is_full_and_final_test_sealed():
 spec=spec_from_json(); t=default_template(spec); c=compile_template(t)
 assert c.final_test_sealed and c.fixture_not_alpha_proof and len(c.stage_ids)>=8
 assert c.compiled_hash==load('uce_i16_compiled_tournament.v1.json')['compiled_hash']

def test_current_engine_snapshot_matches_committed_baseline():
 baseline=json.loads((CONTEXT/'generated/engine_core_baseline_snapshot.json').read_text())
 current=snapshot(ROOT)
 assert current.snapshot_hash==baseline['snapshot_hash']
 report=compare(current,current,tuple(baseline['allowed_plugin_paths']))
 assert report.status is InvarianceStatus.PASS and not report.changed_core_paths
