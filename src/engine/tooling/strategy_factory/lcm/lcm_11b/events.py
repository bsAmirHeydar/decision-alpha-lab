from __future__ import annotations
from .canonical import stable_id,digest_object
from .models import VisualEventRecord

def fixture_event(obj,binding,anchor):
    vid=obj["visual_object_id"];base=int(vid.split("_")[-1][:8],16)
    t1=1700000000+(base%500000);t2=t1+300
    anchors={"time_1":t1,"price_1":round(1.0+(base%10000)/10000,6),"time_2":t2,"price_2":round(1.0+((base//7)%10000)/10000,6),"anchor_kind":anchor.get("anchor_kind"),"availability_time":t2}
    payload={"label":"LCM11B_GOLDEN","value":base%1000,"source_path":obj.get("source_path"),"function_name":obj.get("function_name")}
    eid=stable_id("VISEVT",vid,binding.get("source_event_type"),t1,t2)
    provisional={"event_id":eid,"visual_object_id":vid,"event_type":binding.get("source_event_type"),"instance_id":"INSTANCE_A","chart_id":"CHART_1001","symbol":"EURUSD","timeframe":"M5","availability_time":t2,"lifecycle_action":"ENSURE","anchors":anchors,"payload":payload,"source_digest":obj.get("source_digest")}
    provisional["source_digest"]=digest_object(provisional)
    return VisualEventRecord(**provisional)
