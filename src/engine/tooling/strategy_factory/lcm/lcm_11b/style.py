from __future__ import annotations
from .canonical import stable_id
from .models import StyleProfile

def style_for(obj):
    ot=obj["object_type"]
    defaults={"color":"CALLER_OR_THEME_BOUND","width":"CALLER_OR_DEFAULT_BOUND","line_style":"CALLER_OR_DEFAULT_BOUND","font":"CALLER_OR_DEFAULT_BOUND","z_order":"INSTANCE_SCOPED","selectable":False,"hidden":True}
    if obj["surface_kind"]=="INDICATOR_BUFFER":defaults.update({"plot_index":"CONTRACT_BOUND","empty_value":"PLATFORM_BOUND"})
    if obj["surface_kind"]=="REPORT_PROJECTION":defaults={"format":"DETERMINISTIC_SERIALIZATION","ordering":"CANONICAL_KEY_ORDER","encoding":"UTF_8"}
    return StyleProfile(stable_id("VISSTYLE",obj["visual_object_id"],ot),obj["visual_object_id"],ot,("object_type","anchors","label_meaning","source_event_type","lifecycle_action"),defaults,False)
