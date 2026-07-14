from fp_i12_operator import *
def test_initial_alerts(snapshot):
 c=derive_alert_candidates(snapshot,None);types={x.alert_type for x in c};assert AlertType.DATA_READY in types and AlertType.SIGNAL_CONFIRMED in types and AlertType.QUOTA_WINNER in types
def test_no_repeat(snapshot):assert derive_alert_candidates(snapshot,snapshot)==()
def test_health_block(snapshot):
 s=OperatorSnapshot('S2',140,'R2',OperatorHealth.BLOCKED,'BLOCKED','NONE','',43,8,snapshot.items,'UNSET','');assert any(x.alert_type is AlertType.HEALTH_BLOCKED for x in derive_alert_candidates(s,snapshot))
