def within_retention(event_time,now,history_days): return event_time>=now-history_days*86_400_000
def retain_snapshot(snapshot,now,history_days):
 from dataclasses import replace
 w=tuple(x for x in snapshot.windows if within_retention(x.end,now,history_days));r=tuple(x for x in snapshot.references if within_retention(x.end,now,history_days));h=tuple(x for x in snapshot.hunts if within_retention(x.time,now,history_days));s=tuple(x for x in snapshot.signals if within_retention(max(x.confirmation_time,x.first_hunt_time),now,history_days));ww=tuple(x for x in snapshot.ww_contexts if within_retention(x.end,now,history_days));return replace(snapshot,windows=w,references=r,hunts=h,signals=s,ww_contexts=ww)
