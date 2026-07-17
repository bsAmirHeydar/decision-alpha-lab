from __future__ import annotations
from dataclasses import dataclass,field
from datetime import datetime,timezone
from typing import Any
from .canonical import digest_object
from .questionnaire import QuestionCatalog
from .errors import IntakeError

@dataclass
class InterviewSession:
    context_id:str; session_id:str; answers:dict[str,Any]=field(default_factory=dict); status:str="OPEN"; revision:int=0
    def answer(self,catalog:QuestionCatalog,question_id:str,value:Any)->None:
        if self.status!="OPEN": raise IntakeError("session is not open")
        q=catalog.get(question_id); self._validate(q.answer_type,value); self.answers[question_id]=value; self.revision+=1
    def _validate(self,kind:str,value:Any)->None:
        if kind=="text" and (not isinstance(value,str) or not value.strip()): raise IntakeError("non-empty text required")
        if kind=="boolean" and not isinstance(value,bool): raise IntakeError("boolean required")
        if kind=="list" and (not isinstance(value,list) or not value): raise IntakeError("non-empty list required")
        if kind=="integer" and (not isinstance(value,int) or isinstance(value,bool)): raise IntakeError("integer required")
        if kind=="mapping" and not isinstance(value,dict): raise IntakeError("mapping required")
    def unanswered_required(self,catalog:QuestionCatalog)->list[str]:
        return [q.question_id for q in catalog.applicable(self.answers) if q.required and q.question_id not in self.answers]
    def close(self,catalog:QuestionCatalog)->None:
        missing=self.unanswered_required(catalog)
        if missing: raise IntakeError(f"required questions unanswered: {missing}")
        self.status="CLOSED"; self.revision+=1
    def to_dict(self)->dict[str,Any]:
        obj={"context_id":self.context_id,"session_id":self.session_id,"answers":self.answers,"status":self.status,"revision":self.revision}
        return {**obj,"digest":digest_object(obj)}
