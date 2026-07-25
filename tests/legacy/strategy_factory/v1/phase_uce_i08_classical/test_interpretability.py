import pytest
from strategy_factory_classical_v3 import *
def test_final_test_selection_blocked():
 q=ExplanationRequest('q','m','d','f','final_test',ExplanationScope.FINAL_TEST_AUDIT_ONLY,(ImportanceKind.PERMUTATION,),True,7)
 with pytest.raises(ExplanationLeakageError):InterpretabilityEngine.validate_request(q)
def test_final_test_audit_allowed():InterpretabilityEngine.validate_request(ExplanationRequest('q','m','d','f','final_test',ExplanationScope.FINAL_TEST_AUDIT_ONLY,(ImportanceKind.PERMUTATION,),False,7))
def test_coefficient_stability():
 r1=FeatureImportanceRecord('x',0,ImportanceKind.COEFFICIENT,1,0,1,'f1','oof','m',1);r2=FeatureImportanceRecord('x',0,ImportanceKind.COEFFICIENT,.5,0,1,'f2','oof','m2',1);a=ExplanationArtifact('a','q','alg','d','f1','oof',True,(r1,),{}, {},(), 'h');b=ExplanationArtifact('b','q','alg','d','f2','oof',True,(r2,),{}, {},(), 'h2');assert InterpretabilityEngine.coefficient_stability((a,b))['x']['sign_consistency']==1
