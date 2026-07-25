from __future__ import annotations
from .ontology import validate_fact
from .canonical import content_hash
from .errors import FactError,ContradictionError

class FactStore:
    def __init__(self,ontology,decision_time,max_facts=1000):
        self.ontology=ontology;self.decision_time=decision_time;self.max_facts=max_facts;self._facts=[];self._keys={}
    def add(self,fact,derived_by=None,depth=0):
        if len(self._facts)>=self.max_facts:raise FactError('fact budget exhausted')
        validate_fact(self.ontology,fact,self.decision_time)
        k=(fact['subject_id'],fact['concept_id'],jsonable(fact['value']))
        prior=self._keys.get(k)
        if prior and prior['polarity']!=fact['polarity']:raise ContradictionError(f'contradiction at {k}')
        if prior:return False
        row=dict(fact);row['derived_by']=derived_by;row['depth']=int(depth);row['fact_hash']=content_hash(fact)
        self._facts.append(row);self._keys[k]=row;return True
    def facts(self):return [dict(x) for x in self._facts]
    def query(self,subject_id=None,concept_id=None):
        return [x for x in self._facts if (subject_id is None or x['subject_id']==subject_id) and (concept_id is None or x['concept_id']==concept_id)]
    def has(self,subject_id,concept_id,value=None,polarity=1):
        for x in self.query(subject_id,concept_id):
            if x['polarity']==polarity and (value is None or x['value']==value):return True
        return False

def jsonable(v):
    import json
    return json.dumps(v,sort_keys=True,separators=(',',':'))
