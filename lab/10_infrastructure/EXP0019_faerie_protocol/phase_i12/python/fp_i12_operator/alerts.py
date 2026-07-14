from __future__ import annotations
from .contracts import *
from .canonical import sha256,stable_id
class AlertRouter:
 def __init__(self,instance_id,config,state=None):
  self.instance_id=instance_id;self.config=config;self.delivered=set();self.acknowledged=set();self.minute_buckets={}
  if state:
   self.delivered.update(state.delivered_ids);self.acknowledged.update(state.acknowledged_ids);self.minute_buckets=dict(state.minute_buckets)
 def _suppress(self,c):
  if not self.config.enabled or c.alert_type not in self.config.alert_types:return AlertDisposition.FAILED,'FP_ALERT_DISABLED'
  if c.alert_id in self.delivered:return AlertDisposition.SUPPRESSED_DUPLICATE,'FP_ALERT_DUPLICATE'
  if self.config.suppress_historical and (c.is_historical or c.event_time<self.config.startup_watermark):return AlertDisposition.SUPPRESSED_HISTORICAL,'FP_ALERT_HISTORICAL_SUPPRESSED'
  minute=c.event_time//60;count=self.minute_buckets.get(minute,0)
  if count>=self.config.max_per_minute:return AlertDisposition.SUPPRESSED_RATE_LIMIT,'FP_ALERT_RATE_LIMIT'
  return AlertDisposition.READY,'FP_ALERT_READY'
 def route(self,candidate,now):
  status,reason=self._suppress(candidate);deliveries=[]
  if status is AlertDisposition.READY:
   minute=candidate.event_time//60;self.minute_buckets[minute]=self.minute_buckets.get(minute,0)+1
   for ch in self.config.channels: deliveries.append(AlertDelivery(candidate.alert_id,ch,AlertDisposition.DELIVERED,now,'FP_ALERT_CHANNEL_DELIVERED'))
   self.delivered.add(candidate.alert_id);status=AlertDisposition.DELIVERED;reason='FP_ALERT_DELIVERED'
  event_hash=sha256({'candidate':candidate,'deliveries':deliveries,'status':status.value,'reason':reason})
  return AlertEvent(candidate.alert_id,candidate,tuple(deliveries),status,candidate.alert_id in self.acknowledged,event_hash)
 def acknowledge(self,alert_id):
  if alert_id in self.delivered:self.acknowledged.add(alert_id);return True
  return False
 def acknowledge_all(self): self.acknowledged.update(self.delivered)
 def snapshot(self):
  payload={'instance_id':self.instance_id,'delivered':sorted(self.delivered),'acknowledged':sorted(self.acknowledged),'minute_buckets':sorted(self.minute_buckets.items())}
  return AlertStateSnapshot(self.instance_id,tuple(payload['delivered']),tuple(payload['acknowledged']),tuple(payload['minute_buckets']),sha256(payload))

def derive_alert_candidates(snapshot,previous=None):
 candidates=[];prev_health=previous.health if previous else None
 if snapshot.health is OperatorHealth.BLOCKED and prev_health is not OperatorHealth.BLOCKED:
  candidates.append(AlertCandidate(snapshot.snapshot_id,AlertType.HEALTH_BLOCKED,snapshot.generated_at,AlertSeverity.CRITICAL,'Faerie Protocol blocked','Indicator health is BLOCKED',False,sha256(snapshot.snapshot_id)))
 elif snapshot.health is OperatorHealth.DEGRADED and prev_health is OperatorHealth.READY:
  candidates.append(AlertCandidate(snapshot.snapshot_id,AlertType.HEALTH_DEGRADED,snapshot.generated_at,AlertSeverity.WARNING,'Faerie Protocol degraded','Indicator health is DEGRADED',False,sha256(snapshot.snapshot_id)))
 if snapshot.data_readiness=='READY' and (previous is None or previous.data_readiness!='READY'):
  candidates.append(AlertCandidate(snapshot.snapshot_id,AlertType.DATA_READY,snapshot.generated_at,AlertSeverity.INFO,'Faerie Protocol ready','Data is ready',False,sha256(snapshot.snapshot_id)))
 prev_ids=set(x.semantic_id for x in previous.items) if previous else set()
 for item in snapshot.items:
  if item.semantic_id in prev_ids:continue
  hist=item.is_historical
  if item.kind=='CONFIRMED_SIGNAL': candidates.append(AlertCandidate(item.semantic_id,AlertType.SIGNAL_CONFIRMED,item.event_time,AlertSeverity.INFO,'Confirmed signal',f'{item.relation} {item.direction} {item.symbol}',hist,item.semantic_hash or sha256(item)))
  if item.kind=='WW_CONTEXT' and item.state=='CONFIRMED': candidates.append(AlertCandidate(item.semantic_id,AlertType.WW_CONTEXT_ACTIVE,item.event_time,AlertSeverity.INFO,'WW context active',item.direction,hist,item.semantic_hash or sha256(item)))
  if item.kind=='WW_CONTEXT' and item.state=='NEUTRALIZED': candidates.append(AlertCandidate(item.semantic_id,AlertType.WW_NEUTRALIZED,item.event_time,AlertSeverity.INFO,'WW context neutralized',item.direction,hist,item.semantic_hash or sha256(item)))
  if item.disposition=='QUOTA_WINNER': candidates.append(AlertCandidate(item.semantic_id,AlertType.QUOTA_WINNER,item.event_time,AlertSeverity.INFO,'Pair-session winner',item.semantic_id,hist,item.semantic_hash or sha256(item)))
 return tuple(sorted(candidates,key=lambda x:(x.event_time,x.alert_id)))
