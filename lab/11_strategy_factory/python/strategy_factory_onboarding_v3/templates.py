from __future__ import annotations
from dataclasses import asdict
from .canonical import canonical_json
from .contracts import ContextSpecification,TournamentTemplateSpec

def render_files(spec:ContextSpecification,tournament:TournamentTemplateSpec)->dict[str,bytes]:
    slug=spec.context_id.replace('.','_').replace('-','_').lower()
    base=f'lab/11_strategy_factory/generated_contexts/{slug}'
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':f'urn:alpha-lab:context:{spec.context_id}:{spec.version}','type':'object','additionalProperties':False,'required':['context_id','version','known_time_ms','features'],'properties':{'context_id':{'const':spec.context_id},'version':{'const':spec.version},'known_time_ms':{'type':'integer'},'features':{'type':'object','additionalProperties':False,'required':[f.feature_id for f in spec.features if f.required],'properties':{f.feature_id:{'type':{'float':'number','int':'integer','bool':'boolean','string':'string','category':'string'}[f.dtype]} for f in spec.features}}}}
    feature_rows='\n'.join(f"- `{f.feature_id}` — {f.dtype}; known-time: `{f.known_time_rule}`; required: `{str(f.required).lower()}`" for f in spec.features)
    view_rows='\n'.join(f"- `{v.view_id}` — features: {', '.join(v.feature_ids)}; shape: {list(v.shape)}" for v in spec.views)
    files={
      f'{base}/context_spec.json':canonical_json(asdict(spec)).encode(),
      f'{base}/schemas/context_occurrence.schema.json':canonical_json(schema).encode(),
      f'{base}/feature_descriptor.json':canonical_json([asdict(x) for x in spec.features]).encode(),
      f'{base}/view_descriptor.json':canonical_json([asdict(x) for x in spec.views]).encode(),
      f'{base}/lifecycle.json':canonical_json({'states':spec.lifecycle_states,'known_time_required':True}).encode(),
      f'{base}/cluster_rules.json':canonical_json({'cluster_rule_ids':spec.cluster_rule_ids}).encode(),
      f'{base}/tasks.json':canonical_json({'task_ids':spec.task_ids}).encode(),
      f'{base}/manual_policy.json':canonical_json({'manual_policy_id':spec.manual_policy_id,'version':spec.version}).encode(),
      f'{base}/capabilities.json':canonical_json([asdict(x) for x in spec.capabilities]).encode(),
      f'{base}/tournament_template.json':canonical_json(asdict(tournament)).encode(),
      f'{base}/fixtures/golden.json':canonical_json({'context_id':spec.context_id,'known_time_ms':1000,'features':{f.feature_id:(0 if f.dtype in {'float','int'} else False if f.dtype=='bool' else 'fixture') for f in spec.features}}).encode(),
      f'{base}/fixtures/negative_future.json':canonical_json({'context_id':spec.context_id,'event_time_ms':2000,'known_time_ms':1000,'expected_error':'future_known_time'}).encode(),
      f'{base}/tests/test_contract.py':("def test_generated_contract_marker():\n    assert True\n").encode(),
      f'{base}/README.md':f"# {spec.display_name}\n\nGenerated context package for `{spec.context_id}` version `{spec.version}`.\n\n## Features\n{feature_rows}\n\n## Views\n{view_rows}\n\n## Authority\nThis package cannot send orders, bypass shared economics, or read future data.\n".encode(),
      f'{base}/PHASE_STATUS.json':canonical_json({'context_id':spec.context_id,'status':'scaffolded','wave':spec.wave.value,'core_edit_required':False}).encode(),
    }
    return dict(sorted(files.items()))
