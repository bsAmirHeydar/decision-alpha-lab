from __future__ import annotations
from collections import defaultdict,deque
from .models import OntologyTerm,OntologyRelation
from .enums import RelationKind
from .errors import OntologyError

class OntologyGraph:
    def __init__(self,terms=(),relations=()):
        self.terms={x.term_id:x for x in terms};self.relations=[]
        for r in relations:self.add_relation(r)
    def add_term(self,term:OntologyTerm):
        old=self.terms.get(term.term_id)
        if old and old.term_hash!=term.term_hash:raise OntologyError('term rebind')
        self.terms[term.term_id]=term
    def add_relation(self,r:OntologyRelation):
        if r.source_term_id not in self.terms or r.target_term_id not in self.terms:raise OntologyError('unknown term')
        if r.source_term_id==r.target_term_id and r.relation_kind in {RelationKind.IS_A,RelationKind.PART_OF,RelationKind.PRECEDES}:raise OntologyError('self cycle')
        if any(x.relation_id==r.relation_id for x in self.relations):return
        self.relations.append(r)
        if r.relation_kind in {RelationKind.IS_A,RelationKind.PART_OF,RelationKind.PRECEDES,RelationKind.REQUIRES} and self._has_cycle(r.relation_kind):
            self.relations.pop();raise OntologyError('ontology cycle')
    def _has_cycle(self,kind):
        g=defaultdict(list)
        for r in self.relations:
            if r.relation_kind==kind:g[r.source_term_id].append(r.target_term_id)
        visiting=set();done=set()
        def dfs(n):
            if n in visiting:return True
            if n in done:return False
            visiting.add(n)
            for m in g[n]:
                if dfs(m):return True
            visiting.remove(n);done.add(n);return False
        return any(dfs(n) for n in self.terms)
    def ancestors(self,term_id:str,kind:RelationKind=RelationKind.IS_A)->tuple[str,...]:
        rev=defaultdict(list)
        for r in self.relations:
            if r.relation_kind==kind:rev[r.source_term_id].append(r.target_term_id)
        out=set();q=deque([term_id])
        while q:
            n=q.popleft()
            for m in rev[n]:
                if m not in out:out.add(m);q.append(m)
        return tuple(sorted(out))
