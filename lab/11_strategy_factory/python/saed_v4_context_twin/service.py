from __future__ import annotations
from .compiler import compile_twin
from .registry import TwinRegistry
from .observations import ObservationLedger
from .hypotheses import HypothesisLedger
from .contradictions import ContradictionRegistry
from .evidence_debt import EvidenceDebtLedger
from .lifecycle import LifecycleMachine
from .transition import TransitionLedger
from .support import evaluate_support
from .state import build_snapshot

class ContextTwinService:
    def __init__(self):self.registry=TwinRegistry();self.cells={}
    def initialize(self,context_spec,seed,exact_version='1.0.0'):
        m=compile_twin(context_spec,seed,exact_version);self.registry.register(m)
        cell={'manifest':m,'observations':ObservationLedger(m.observables),'hypotheses':HypothesisLedger(m.hypotheses),'contradictions':ContradictionRegistry(),'debt':EvidenceDebtLedger(),'transitions':TransitionLedger(LifecycleMachine(m.lifecycle_states,m.transition_rules,m.initial_lifecycle_state)),'lifecycle_state':m.initial_lifecycle_state,'snapshots':[]}
        self.cells[(m.twin_id,m.exact_version)]=cell;return m
    def cell(self,twin_id,version):return self.cells[(twin_id,version)]
    def evaluate_support(self,twin_id,version,known_as_of):
        c=self.cell(twin_id,version);return evaluate_support(twin_id,c['manifest'].support_geometry,c['observations'].latest_by_observable(twin_id,known_as_of),known_as_of)
    def snapshot(self,twin_id,version,known_as_of):
        c=self.cell(twin_id,version);obs=c['observations'].visible(twin_id,known_as_of);sup=self.evaluate_support(twin_id,version,known_as_of)
        s=build_snapshot(c['manifest'],known_as_of,c['lifecycle_state'],obs,c['hypotheses'].states(),sup,c['contradictions'].all(twin_id),c['debt'].active(twin_id),tuple(c['transitions'].events),len(c['snapshots'])+1);c['snapshots'].append(s);return s
