from strategy_factory_deep_views_v3.gates import evaluate_deep_admission
from strategy_factory_deep_views_v3.qualification import qualify_deep_model
from strategy_factory_deep_views_v3.golden import qualification_evidence
from strategy_factory_deep_views_v3.contracts import ExportAssessment
from strategy_factory_deep_views_v3.enums import AdmissionDecision,QualificationDecision,ExportPath
from strategy_factory_deep_views_v3.canonical import canonical_sha256
def test_admission_rejects_missing_classical_and_causal_gates():
    e=evaluate_deep_admission('d','m',10,2,1,False,False,False,False,0,'','');assert e.decision is AdmissionDecision.REJECT;assert 'classical_gate_failed' in e.blockers
def test_qualification_requires_export_uplift_and_three_seeds():
    admission=evaluate_deep_admission('d','m',1000,100,4,True,True,True,True,.6,'a','b');seeds,ablations,_=qualification_evidence();bad=ExportAssessment(ExportPath.NONE,False,1.,99.,'','','x')
    q=qualify_deep_model('a@1','m',admission,seeds[:2],ablations,bad,.7);assert q.decision is QualificationDecision.REJECTED;assert 'fewer_than_three_seed_runs' in q.blockers;assert 'export_path_unavailable' in q.blockers
