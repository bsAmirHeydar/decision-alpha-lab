from __future__ import annotations
from .enums import RetcodeClass

SUCCESS={0,10008,10009,10010}
TRANSIENT={10004,10012,10020,10021,10024}
POLICY={10017,10026,10027,10032,10033,10034,10040,10041,10042,10043,10044,10045,10046}
MARKET={10018}
ACCOUNT={10019}
REQUEST={10006,10007,10011,10013,10014,10015,10016,10030,10035,10036,10038,10039}
CONNECTION={10031}

def classify_retcode(retcode: int) -> RetcodeClass:
    if retcode in SUCCESS: return RetcodeClass.SUCCESS
    if retcode in TRANSIENT: return RetcodeClass.TRANSIENT
    if retcode in POLICY: return RetcodeClass.POLICY_REJECT
    if retcode in MARKET: return RetcodeClass.MARKET_STATE
    if retcode in ACCOUNT: return RetcodeClass.ACCOUNT_STATE
    if retcode in REQUEST: return RetcodeClass.REQUEST_INVALID
    if retcode in CONNECTION: return RetcodeClass.CONNECTION
    return RetcodeClass.UNKNOWN

def retcode_is_success(retcode: int) -> bool:
    return classify_retcode(retcode)==RetcodeClass.SUCCESS
