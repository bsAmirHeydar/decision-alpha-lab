from __future__ import annotations
from datetime import datetime,time,timedelta
from zoneinfo import ZoneInfo
NY=ZoneInfo("America/New_York")
CYCLES={"L":(time(7),time(9,30)),"N":(time(9,30),time(16)),"A":(time(16),time(20)),"FCR_1":(time(9,30),time(10)),"FCR_2":(time(10),time(16)),"PP_1":(time(9),time(9,30)),"PP_2":(time(9,30),time(16))}
def in_half_open(local_dt:datetime,cycle_id:str)->bool:
 d=local_dt.astimezone(NY);start,end=CYCLES[cycle_id];t=d.timetz().replace(tzinfo=None);return start<=t<end
