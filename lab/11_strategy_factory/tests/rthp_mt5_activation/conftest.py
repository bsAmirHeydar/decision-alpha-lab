from __future__ import annotations
import json,math
from datetime import datetime,timedelta,timezone
from pathlib import Path
import pytest

class Row(dict):
    pass
class FakeProvider:
    package_version='5.0.fake'
    def __init__(self,start:datetime,minutes:int=2200):
        self.start=start; self.minutes=minutes; self.selected=set(); self._err=(1,'Success')
        self.data={s:self._rows(s,phase) for s,phase in [('FAKE_A',0.0),('FAKE_B',0.8)]}
    def _rows(self,symbol,phase):
        rows=[]
        for i in range(self.minutes):
            t=int((self.start+timedelta(minutes=i)).timestamp()); base=100+0.01*i+math.sin(i/11+phase)*0.7
            # Introduce symbol-local excursions that create M15 divergences.
            pulse=(1.2 if symbol=='FAKE_A' and i%90 in range(45,50) else 0.0) + (-1.0 if symbol=='FAKE_B' and i%120 in range(75,80) else 0.0)
            o=base; c=base+math.sin(i/5+phase)*0.05; h=max(o,c)+0.12+max(pulse,0.0); l=min(o,c)-0.12+min(pulse,0.0)
            rows.append(Row(time=t,open=o,high=h,low=l,close=c,tick_volume=10+i%7,spread=2,real_volume=0))
        return rows
    def initialize(self,path,timeout_ms,portable): return True
    def shutdown(self): pass
    def last_error(self): return self._err
    def terminal_info(self): return {'connected':True,'path':'C:/Fake/terminal64.exe','data_path':'C:/Fake/Data','build':5000}
    def account_info(self): return {'login':123,'server':'FAKE-SERVER'}
    def version(self): return (5000,5000,'2026-01-01')
    def symbols_get(self): return [{'name':'FAKE_A'},{'name':'FAKE_B'}]
    def symbol_select(self,symbol,enable): self.selected.add(symbol); return True
    def symbol_info(self,symbol): return {'name':symbol,'description':symbol,'path':'Fake','digits':2,'point':0.01,'trade_tick_size':0.01,'trade_contract_size':1.0,'trade_calc_mode':0,'trade_mode':4,'currency_base':'USD','currency_profit':'USD','currency_margin':'USD','start_time':0,'expiration_time':0,'spread':2,'spread_float':False,'visible':True,'select':True}
    def copy_rates_range(self,symbol,date_from,date_to):
        a=int(date_from.timestamp()); b=int(date_to.timestamp()); return [r for r in self.data[symbol] if a<=r['time']<=b]
    def copy_rates_from_pos(self,symbol,start_pos,count): return self.data[symbol][-count:]

@pytest.fixture
def repo_root(): return Path(__file__).resolve().parents[4]
@pytest.fixture
def fake_provider(): return FakeProvider(datetime(2026,1,5,0,0,tzinfo=timezone.utc))
@pytest.fixture
def config_path(tmp_path):
    raw={'schema_version':'1.0.0','run_id':'FAKE_RUN','output_root':(tmp_path/'output').as_posix(),
         'symbols':{'primary':'FAKE_A','secondary':'FAKE_B','canonical_primary_id':'FAKE_A','canonical_secondary_id':'FAKE_B'},
         'terminal':{'path':None,'timeout_ms':1000,'portable':False,'require_connected':True},
         'history':{'mode':'EXPLICIT_UTC_RANGE','start_utc':'2026-01-05T00:00:00Z','end_utc':'2026-01-06T12:00:00Z','max_lookback_days':10,'minimum_common_days':1,'chunk_days':1,'overlap_minutes':2,'retry_count':1,'retry_delay_seconds':0.0},
         'quality':{'minimum_common_bars':1000,'max_symbol_specific_gap_ratio':0.02,'max_joint_gap_minutes':240,'max_unexplained_gap_minutes':15,'require_exact_m15_coverage':True,'reject_sub_m1':True,'drop_incomplete_current_bar':True},
         'train':{'enabled':False,'selected_task_ids':[],'family_filter':['M15_CYCLE_GROUP'],'minimum_mature_rows':8,'max_rows':100000,'max_memory_mb':1024,'max_wall_seconds':120,'seed':1701},
         'source_revision':'TEST_R1','contract_roll_policy':'NO_IMPLICIT_STITCHING_V1','entitlement_id':'TEST'}
    p=tmp_path/'config.json'; p.write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8'); return p
