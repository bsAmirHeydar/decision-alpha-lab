import pytest
from saed_v4_neurosymbolic_setup_reasoning.synthesis import bounded_program_synthesis
from saed_v4_neurosymbolic_setup_reasoning.counterexamples import search,mutate_rows
from saed_v4_neurosymbolic_setup_reasoning.symbolic_regression import fit_reference
from saed_v4_neurosymbolic_setup_reasoning.disagreement import compare
from saed_v4_neurosymbolic_setup_reasoning.mdl import score

def rows():
 out=[]
 for i in range(60):
  p={'a':i%2==0,'b':i%3!=0,'c':i%5!=0};t='treatment_alpha' if p['a'] and p['b'] else 'skip';out.append({'row_id':str(i),'predicate_values':p,'target_treatment':t,'features':{'x':i/60,'z':(i%7)/7},'y':i/60+0.1*(i%7)})
 return out
def test_synthesis():
 s=bounded_program_synthesis(rows(),['a','b','c'],'treatment_alpha',2,20);assert s['champion']['conditions']==['a','b'] and s['champion']['fidelity']==1.0
def test_counterexamples():
 s=bounded_program_synthesis(rows(),['a','b','c'],'treatment_alpha',1,20);assert search(s['champion'],rows(),64)['count']>0
def test_mutations():assert len(mutate_rows(rows(),['a','b']))==40
def test_symreg():
 r=fit_reference(rows(),['x','z'],'y',2);assert r['model_count']==3 and r['champion']
def test_disagreement_abstain():assert compare({'a':1.0},{'a':0.0},0.2)['directive']=='abstain'
def test_disagreement_continue():assert compare({'a':0.6},{'a':0.5},0.2)['directive']=='continue_reference'
def test_mdl():assert score(1,2,0,0,1.0)['total_mdl_cost']==2.0
