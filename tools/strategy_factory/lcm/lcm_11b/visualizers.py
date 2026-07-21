from __future__ import annotations
from .canonical import stable_id
from .models import VisualizerContract,ProjectionRecord

def kind_for(surface_kind):
    return {"CHART_OBJECT":"MQL5_CANONICAL_CHART_OBJECT_VISUALIZER","INDICATOR_BUFFER":"MQL5_CANONICAL_BUFFER_PROJECTION","REPORT_PROJECTION":"PYTHON_CANONICAL_REPORT_PROJECTION"}.get(surface_kind,"BLOCKED_UNKNOWN_VISUALIZER")
def build_contract(obj,binding,namespace,anchor,lifecycle,style,eligibility):
    return VisualizerContract(stable_id("VISUALIZER",obj["visual_object_id"],kind_for(obj["surface_kind"])),obj["visual_object_id"],kind_for(obj["surface_kind"]),binding.get("source_event_type"),namespace["canonical_object_id_template"],namespace["canonical_cleanup_prefix_template"],anchor["anchor_contract_id"],lifecycle["lifecycle_contract_id"],style.style_profile_id,"EVENT_TO_PROJECTION_PURE_FUNCTION",False,False,False,False,eligibility["status"],tuple(eligibility["blocking_reasons"]))
def render(contract,event,obj,style):
    name=contract.namespace_template
    for key,val in {"{INSTANCE_ID}":event.instance_id,"{CHART_ID}":event.chart_id,"{SYMBOL}":event.symbol,"{TIMEFRAME}":event.timeframe,"{EVENT_ID}":event.event_id}.items():name=name.replace(key,str(val))
    return ProjectionRecord(stable_id("VISPROJ",contract.visualizer_id,event.event_id),contract.visualizer_id,event.event_id,name,obj["surface_kind"],obj["object_type"],event.chart_id,event.symbol,event.timeframe,event.anchors,event.payload,style.style_profile_id,event.lifecycle_action)
