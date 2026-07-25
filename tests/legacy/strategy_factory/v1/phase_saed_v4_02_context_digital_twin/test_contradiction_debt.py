import pytest
from saed_v4_context_twin.models import Contradiction,EvidenceDebtItem
from saed_v4_context_twin.enums import ContradictionSeverity,DebtSeverity
from saed_v4_context_twin.contradictions import ContradictionRegistry
from saed_v4_context_twin.evidence_debt import EvidenceDebtLedger
H='a'*64

def test_contradiction_open_resolve():
 r=ContradictionRegistry();x=Contradiction('t','k',H,'b'*64,ContradictionSeverity.CRITICAL,'2026-01-01T00:00:00Z','d');r.open(x);assert r.blocking('t');r.resolve(x.contradiction_id,'c'*64);assert not r.active('t')
def test_debt_open_resolve():
 l=EvidenceDebtLedger();x=EvidenceDebtItem('t','k','d',DebtSeverity.BLOCKING,'s','2026-01-01T00:00:00Z');l.open(x);assert l.blocking('t');l.resolve(x.debt_id,'c'*64);assert not l.active('t')
