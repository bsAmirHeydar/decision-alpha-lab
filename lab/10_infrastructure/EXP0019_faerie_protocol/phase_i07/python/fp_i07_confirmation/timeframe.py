from .enums import HostTimeframe
from .errors import FPI07Error
_SECONDS={
HostTimeframe.M1:60,HostTimeframe.M2:120,HostTimeframe.M3:180,HostTimeframe.M4:240,HostTimeframe.M5:300,HostTimeframe.M6:360,
HostTimeframe.M10:600,HostTimeframe.M12:720,HostTimeframe.M15:900,HostTimeframe.M20:1200,HostTimeframe.M30:1800,
HostTimeframe.H1:3600,HostTimeframe.H2:7200,HostTimeframe.H3:10800,HostTimeframe.H4:14400,HostTimeframe.H6:21600,HostTimeframe.H8:28800,HostTimeframe.H12:43200,HostTimeframe.D1:86400}
def timeframe_seconds(tf):
    try:return _SECONDS[HostTimeframe(tf)]
    except Exception as exc:raise FPI07Error("FP_CRC_TIMEFRAME_UNSUPPORTED","unsupported host timeframe",{"timeframe":str(tf)}) from exc
def resolve_timeframe(value):
    if value in (None,"","PERIOD_CURRENT"): raise FPI07Error("FP_CRC_TIMEFRAME_NOT_RESOLVED","PERIOD_CURRENT must be resolved at initialization")
    tf=HostTimeframe(value); return tf,timeframe_seconds(tf)
