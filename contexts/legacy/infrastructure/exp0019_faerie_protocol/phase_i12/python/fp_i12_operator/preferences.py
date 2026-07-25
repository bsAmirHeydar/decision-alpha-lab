from dataclasses import replace
from .contracts import *
from .canonical import sha256

def default_preferences(config):
 p=OperatorPreferences(config.panel,config.filters,(),0,'');return replace(p,preferences_hash=p.computed_hash)
def normalize_preferences(p):
 page=max(0,p.page);acks=tuple(sorted(set(p.acknowledged_alert_ids)));n=replace(p,page=page,acknowledged_alert_ids=acks,preferences_hash='');return replace(n,preferences_hash=n.computed_hash)
def set_panel(p,panel):return normalize_preferences(replace(p,panel=panel))
def set_filters(p,filters):return normalize_preferences(replace(p,filters=filters,page=0))
