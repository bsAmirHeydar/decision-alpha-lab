from .contracts import *
from .canonical import sha256
def build_acceptance(risk_cap_pass,sell_spread_pass,quota_pass,lifecycle_pass,restart_pass,metaeditor=AcceptanceStatus.PENDING,local_runtime=AcceptanceStatus.PENDING):
    source=AcceptanceStatus.PASS if all((risk_cap_pass,sell_spread_pass,quota_pass,lifecycle_pass,restart_pass)) else AcceptanceStatus.FAIL
    payload={"source":source,"risk":risk_cap_pass,"sell":sell_spread_pass,"quota":quota_pass,"lifecycle":lifecycle_pass,"restart":restart_pass,"metaeditor":metaeditor,"runtime":local_runtime}
    return PaperAcceptance("FP-I15",source,AcceptanceStatus.PASS if risk_cap_pass else AcceptanceStatus.FAIL,AcceptanceStatus.PASS if sell_spread_pass else AcceptanceStatus.FAIL,AcceptanceStatus.PASS if quota_pass else AcceptanceStatus.FAIL,AcceptanceStatus.PASS if lifecycle_pass else AcceptanceStatus.FAIL,AcceptanceStatus.PASS if restart_pass else AcceptanceStatus.FAIL,metaeditor,local_runtime,source==AcceptanceStatus.PASS,False,sha256(payload))
