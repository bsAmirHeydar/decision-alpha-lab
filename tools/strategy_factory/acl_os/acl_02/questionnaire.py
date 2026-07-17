from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .policies import load_policy

@dataclass(frozen=True,slots=True)
class Question:
    question_id:str; section:str; prompt:str; answer_type:str; required:bool; weight:float; target_path:str; help_text:str; conditions:dict[str,Any]
    @classmethod
    def from_dict(cls,o:dict[str,Any])->"Question":
        return cls(o["question_id"],o["section"],o["prompt"],o["answer_type"],bool(o["required"]),float(o["weight"]),o["target_path"],o["help_text"],dict(o.get("conditions",{})))

class QuestionCatalog:
    def __init__(self): self._questions=tuple(Question.from_dict(x) for x in load_policy("question_catalog")["questions"])
    def all(self): return self._questions
    def applicable(self,answers:dict[str,Any]):
        out=[]
        for q in self._questions:
            ok=True
            for key,expected in q.conditions.items():
                if answers.get(key)!=expected: ok=False; break
            if ok: out.append(q)
        return tuple(out)
    def get(self,qid:str)->Question:
        for q in self._questions:
            if q.question_id==qid:return q
        raise KeyError(qid)
