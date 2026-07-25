from .canonical import content_hash, stable_id

def boundary():
    payload={"phase":"SAED_V4_27","research_only":True,"ucee_authority_preserved":True,"safe_action":"skip","authority":{"decision":False,"promotion":False,"runtime":False,"risk_allocation":False,"execution":False,"production":False,"online_learning":False}}
    payload["boundary_id"]=stable_id("search_exposure_authority",payload); payload["boundary_hash"]=content_hash(payload)
    return payload
