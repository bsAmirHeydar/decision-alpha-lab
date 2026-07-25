import pytest
from strategy_factory_onboarding_v3.contracts import *
from strategy_factory_onboarding_v3.capabilities import default_capabilities
from strategy_factory_onboarding_v3.canonical import canonical_sha256
from strategy_factory_onboarding_v3.enums import *
from strategy_factory_onboarding_v3.errors import OnboardingError
from strategy_factory_onboarding_v3.golden import golden_spec

@pytest.mark.parametrize('dtype',['float','int','bool','string','category'])
def test_feature_dtypes(dtype):assert FeatureSpec('f_'+dtype,dtype,'known_at_close').dtype==dtype
@pytest.mark.parametrize('dtype',['double','object','array',''])
def test_feature_rejects_unknown_dtype(dtype):
 with pytest.raises(OnboardingError):FeatureSpec('f','%s'%dtype,'known')
@pytest.mark.parametrize('shape',[(1,),(4,),(2,3),(1,2,3)])
def test_view_shapes(shape):assert ViewSpec('view',('f',),shape).shape==shape
@pytest.mark.parametrize('shape',[(),(0,),(-1,2)])
def test_view_rejects_bad_shape(shape):
 with pytest.raises(OnboardingError):ViewSpec('view',('f',),shape)
def test_context_rejects_unknown_view_feature():
 s=golden_spec()
 with pytest.raises(OnboardingError):ContextSpecification(s.context_id,s.version,s.display_name,s.kind,s.wave,s.doctrine_hash,s.source_hashes,s.features,(ViewSpec('x',('missing',),(1,)),),s.lifecycle_states,s.cluster_rule_ids,s.task_ids,s.manual_policy_id,s.capabilities)
def test_legacy_adapter_requires_all_shared_paths():
 with pytest.raises(OnboardingError):LegacyAdapterSpec('a','1.0.0','c',('a.py',),(canonical_sha256('x'),),AdapterMode.DIFFERENTIAL,True,False,True,True,True)
def test_tournament_fixture_cannot_claim_alpha():
 spec=golden_spec();t=TournamentTemplateSpec('t','1.0.0',spec.spec_hash,'a','b','c','d','e','f','g','h',1)
 with pytest.raises(OnboardingError):CompiledTournamentTemplate('c','1.0.0',t.template_hash,('x',),{'x':canonical_sha256('x')},True,False)
def test_false_invariance_pass_rejected():
 h=canonical_sha256('x')
 with pytest.raises(OnboardingError):EngineInvarianceReport('r','1.0.0',h,h,InvarianceStatus.PASS,('core.py',),())
def test_adr_gate_requires_evidence():
 h=canonical_sha256('x')
 with pytest.raises(OnboardingError):EngineInvarianceReport('r','1.0.0',h,h,InvarianceStatus.ADR_REQUIRED,('core.py',),())
def test_migration_plan_requires_same_wave():
 h=canonical_sha256('x');u=MigrationUnit('u','c',MigrationWave.A,h,h,'f',h,MigrationStatus.PLANNED)
 with pytest.raises(OnboardingError):MigrationWavePlan('p','1.0.0',MigrationWave.B,(u,),None,h)
