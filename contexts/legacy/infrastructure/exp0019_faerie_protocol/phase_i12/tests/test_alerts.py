from fp_i12_operator import *
def candidate(t=100,h=False):return AlertCandidate('SIG-A',AlertType.SIGNAL_CONFIRMED,t,AlertSeverity.INFO,'t','m',h,sha256('x'))
def test_deliver_once(config):
 r=AlertRouter(config.instance_id,config.alerts);a=r.route(candidate(),101);b=r.route(candidate(),102);assert a.disposition is AlertDisposition.DELIVERED and b.disposition is AlertDisposition.SUPPRESSED_DUPLICATE
def test_historical_suppression(config):
 r=AlertRouter(config.instance_id,config.alerts);assert r.route(candidate(40),100).disposition is AlertDisposition.SUPPRESSED_HISTORICAL
def test_rate_limit(config):
 c=AlertConfig(channels=(AlertChannel.LOG,),startup_watermark=0,max_per_minute=1);r=AlertRouter('I',c);r.route(candidate(100),100);x=AlertCandidate('SIG-B',AlertType.SIGNAL_CONFIRMED,101,AlertSeverity.INFO,'t','m',False,sha256('y'));assert r.route(x,101).disposition is AlertDisposition.SUPPRESSED_RATE_LIMIT
def test_ack(config):
 r=AlertRouter(config.instance_id,config.alerts);e=r.route(candidate(),101);assert r.acknowledge(e.alert_id) and e.alert_id in r.snapshot().acknowledged_ids
def test_state_restart(config):
 r=AlertRouter(config.instance_id,config.alerts);r.route(candidate(),101);r2=AlertRouter(config.instance_id,config.alerts,r.snapshot());assert r2.route(candidate(),102).disposition is AlertDisposition.SUPPRESSED_DUPLICATE
