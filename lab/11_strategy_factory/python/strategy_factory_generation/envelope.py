from __future__ import annotations
from dataclasses import dataclass,replace
from strategy_factory_contracts.hashing import stable_id
from .enums import RecordType
@dataclass(frozen=True,slots=True)
class ResultEnvelope:
    sequence:int;record_type:RecordType;run_id:str;generation_uid:str;aggregate_id:str;producer_id:str;producer_version:str;occurred_at_utc_msc:int;known_at_utc_msc:int;payload_schema:str;payload_hash:str;payload:dict;schema:str='alpha_lab.strategy_factory/result_envelope@1.0.0';record_id:str=''
    def __post_init__(self):
        if self.sequence<=0:raise ValueError('sequence')
        if self.known_at_utc_msc<self.occurred_at_utc_msc:raise ValueError('causality')
        if self.record_id and self.record_id!=self.derived_id:raise ValueError('record id mismatch')
    @property
    def canonical(self):return '|'.join(map(str,[self.schema,self.sequence,int(self.record_type),self.run_id,self.generation_uid,self.aggregate_id,self.producer_id,self.producer_version,self.occurred_at_utc_msc,self.known_at_utc_msc,self.payload_schema,self.payload_hash]))
    @property
    def derived_id(self):return stable_id('rec',self.canonical)
    def materialized(self):return self if self.record_id else replace(self,record_id=self.derived_id)
class EnvelopeFactory:
    def __init__(self,run_id:str,generation_uid:str):self.run_id=run_id;self.generation_uid=generation_uid;self.sequence=0
    def create(self,record_type:RecordType,aggregate_id:str,producer_id:str,producer_version:str,occurred_at:int,known_at:int,payload_schema:str,payload:dict):
        import json
        self.sequence+=1;raw=json.dumps(payload,sort_keys=True,separators=(',',':'));return ResultEnvelope(self.sequence,record_type,self.run_id,self.generation_uid,aggregate_id,producer_id,producer_version,occurred_at,known_at,payload_schema,stable_id('pay',raw),payload).materialized()
