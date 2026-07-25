from fp_i12_operator import *
def test_open_decision_degrades(snapshot,config):
 o=OperatorUXEngine(config).process(snapshot);assert o.diagnostic.health is OperatorHealth.DEGRADED and 'FP_UX_OPEN_DECISION_UNSET' in o.diagnostic.reason_codes
def test_resolved_decision_ready(snapshot):
 c=OperatorConfig('I','FP19::I::',open_decision_state='RESOLVED');s=OperatorSnapshot(snapshot.snapshot_id,snapshot.generated_at,snapshot.revision_id,snapshot.health,snapshot.data_readiness,snapshot.active_ww_direction,snapshot.quota_winner_signal_id,snapshot.ledger_event_count,snapshot.source_revision_sequence,snapshot.items,'RESOLVED','');assert OperatorUXEngine(c).process(s).diagnostic.health is OperatorHealth.READY
