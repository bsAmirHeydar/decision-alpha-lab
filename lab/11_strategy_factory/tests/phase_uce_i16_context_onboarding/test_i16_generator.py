from pathlib import Path
import pytest
from strategy_factory_onboarding_v3.golden import golden_spec
from strategy_factory_onboarding_v3.generator import ContextGenerator
from strategy_factory_onboarding_v3.invariance import snapshot
from strategy_factory_onboarding_v3.registry import ContextRegistry
from strategy_factory_onboarding_v3.contracts import ContextSpecification,CapabilityDeclaration
from strategy_factory_onboarding_v3.enums import CapabilityDecision
from strategy_factory_onboarding_v3.errors import OnboardingError

@pytest.fixture
def built():
 spec=golden_spec();return spec,ContextGenerator().build(spec,snapshot(Path('.')))

def test_generator_produces_fifteen_files(built):assert len(built[1][1])==15
def test_generator_paths_are_context_local(built):assert all('/fixture_onboarded_context/' in p for p in built[1][1])
def test_generator_manifest_matches_files(built):
 _,(m,f,_)=built;assert {a.path for a in m.artifacts}==set(f)
def test_generator_contents_repeat(built):
 spec,(m,f,c)=built;m2,f2,c2=ContextGenerator().build(spec,snapshot(Path('.')));assert f==f2 and m.manifest_hash==m2.manifest_hash and c.compiled_hash==c2.compiled_hash
def test_materialize_roundtrip(tmp_path,built):
 spec,(m,f,_)=built;m2=ContextGenerator().materialize(spec,snapshot(Path('.')),tmp_path);assert m.manifest_hash==m2.manifest_hash;assert all((tmp_path/p).read_bytes()==b for p,b in f.items())
def test_registry_idempotent(built):
 _,(m,_,_)=built;r=ContextRegistry();a=r.register(m);b=r.register(m);assert a==b
def test_registry_rejects_same_id_different_manifest(built):
 spec,(m,_,_)=built;r=ContextRegistry();r.register(m)
 spec2=ContextSpecification(spec.context_id,'1.0.1',spec.display_name,spec.kind,spec.wave,spec.doctrine_hash,spec.source_hashes,spec.features,spec.views,spec.lifecycle_states,spec.cluster_rule_ids,spec.task_ids,spec.manual_policy_id,spec.capabilities)
 m2,_,_=ContextGenerator().build(spec2,snapshot(Path('.')))
 with pytest.raises(OnboardingError):r.register(m2)
@pytest.mark.parametrize('capability',['order_send','broker_write','network_fetch','future_data'])
def test_generator_rejects_forbidden_authority(capability):
 s=golden_spec();caps=tuple(x for x in s.capabilities if x.capability_id!=capability)+(CapabilityDeclaration(capability,CapabilityDecision.ALLOW,'bad'),)
 bad=ContextSpecification(s.context_id,s.version,s.display_name,s.kind,s.wave,s.doctrine_hash,s.source_hashes,s.features,s.views,s.lifecycle_states,s.cluster_rule_ids,s.task_ids,s.manual_policy_id,caps)
 with pytest.raises(OnboardingError):ContextGenerator().build(bad,snapshot(Path('.')))
@pytest.mark.parametrize('required',['shared_treatment','shared_economics','shared_validation','shared_runtime','known_time','deterministic_replay'])
def test_generator_rejects_missing_required_shared_path(required):
 s=golden_spec();caps=tuple(x for x in s.capabilities if x.capability_id!=required)
 bad=ContextSpecification(s.context_id,s.version,s.display_name,s.kind,s.wave,s.doctrine_hash,s.source_hashes,s.features,s.views,s.lifecycle_states,s.cluster_rule_ids,s.task_ids,s.manual_policy_id,caps)
 with pytest.raises(OnboardingError):ContextGenerator().build(bad,snapshot(Path('.')))
