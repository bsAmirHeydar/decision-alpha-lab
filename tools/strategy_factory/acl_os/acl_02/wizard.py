from __future__ import annotations
from pathlib import Path
from typing import Any
from dataclasses import asdict
from .interview import InterviewSession
from .questionnaire import QuestionCatalog
from .io import dump_json

class IntakeWizard:
    def __init__(self,context_id:str,session_id:str): self.catalog=QuestionCatalog();self.session=InterviewSession(context_id,session_id)
    def next_questions(self,limit:int=10):
        return [asdict(q) for q in self.catalog.applicable(self.session.answers) if q.question_id not in self.session.answers][:limit]
    def answer(self,question_id:str,value:Any):self.session.answer(self.catalog,question_id,value)
    def save(self,path:Path):dump_json(path,self.session.to_dict())
