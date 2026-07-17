from __future__ import annotations
from copy import deepcopy
from .contracts import exact
from .errors import StateError
from .canonical import seal,hash_chain

def initial_state(v:dict)->dict:
 exact(v,["state_version","last_known_time","sequence","last_decision","cooldown_bars","drawdown_state","research_only"])
 if v["sequence"]!=0 or v["research_only"] is not True:raise StateError("initial state invalid")
 return seal(deepcopy(v),"v438_state","state_id","state_hash")
def transition(state:dict,decision:dict,known_time:str)->dict:
 if known_time<=state["last_known_time"] and state["last_known_time"]:raise StateError("state time must advance")
 x={"state_version":state["state_version"],"last_known_time":known_time,"sequence":state["sequence"]+1,"last_decision":decision["decision"],"cooldown_bars":max(0,int(state["cooldown_bars"])-1),"drawdown_state":state["drawdown_state"],"research_only":True}
 return seal(x,"v438_state","state_id","state_hash")
def state_ledger(states:list[dict])->dict:return seal({"phase":"SAED_V4_38","events":hash_chain(states,"v438_state_event"),"research_only":True},"v438_state_ledger","ledger_id","ledger_hash")
