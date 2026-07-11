from __future__ import annotations
import json,os
from pathlib import Path
from dataclasses import dataclass
from .envelope import ResultEnvelope
@dataclass(slots=True)
class SinkTelemetry:
    records_written:int=0;flush_count:int=0;write_errors:int=0;duplicate_rejections:int=0;bytes_written:int=0;last_sequence:int=0;sealed:bool=False
class AppendOnlyMemorySink:
    def __init__(self):self.records=[];self.ids=set();self.telemetry=SinkTelemetry()
    def write(self,e:ResultEnvelope):
        if self.telemetry.sealed:raise RuntimeError('sink sealed')
        if e.sequence!=self.telemetry.last_sequence+1:raise ValueError('non-monotonic sequence')
        if e.record_id in self.ids:self.telemetry.duplicate_rejections+=1;raise ValueError('duplicate')
        self.records.append(e);self.ids.add(e.record_id);self.telemetry.records_written+=1;self.telemetry.last_sequence=e.sequence
    def flush(self):self.telemetry.flush_count+=1
    def seal(self):self.flush();self.telemetry.sealed=True
class JsonlResultSink:
    def __init__(self,path:Path):self.path=Path(path);self.telemetry=SinkTelemetry();self.ids=set();self._fh=None
    def open(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        if self.path.exists() and self.path.stat().st_size>0:raise FileExistsError('ledger already exists; use a new run or generation')
        self._fh=self.path.open('a+',encoding='utf-8')
    def write(self,e:ResultEnvelope):
        if self.telemetry.sealed:raise RuntimeError('sink sealed')
        if self._fh is None:raise RuntimeError('sink not open')
        if e.sequence!=self.telemetry.last_sequence+1:raise ValueError('non-monotonic sequence')
        if e.record_id in self.ids:self.telemetry.duplicate_rejections+=1;raise ValueError('duplicate')
        line=json.dumps({'schema':e.schema,'sequence':e.sequence,'record_type':e.record_type.name,'record_id':e.record_id,'run_id':e.run_id,'generation_uid':e.generation_uid,'aggregate_id':e.aggregate_id,'producer_id':e.producer_id,'producer_version':e.producer_version,'occurred_at_utc_msc':e.occurred_at_utc_msc,'known_at_utc_msc':e.known_at_utc_msc,'payload_schema':e.payload_schema,'payload_hash':e.payload_hash,'payload':e.payload},sort_keys=True,separators=(',',':'))+'\n'
        self._fh.write(line);self.ids.add(e.record_id);self.telemetry.records_written+=1;self.telemetry.last_sequence=e.sequence;self.telemetry.bytes_written+=len(line.encode())
    def flush(self):self._fh.flush();os.fsync(self._fh.fileno());self.telemetry.flush_count+=1
    def seal(self):self.flush();self._fh.close();self._fh=None;self.telemetry.sealed=True
