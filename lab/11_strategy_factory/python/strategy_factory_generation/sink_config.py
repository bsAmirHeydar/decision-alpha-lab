from __future__ import annotations
from dataclasses import dataclass
from .enums import SinkMode, FileScope
from strategy_factory_contracts.hashing import stable_id
@dataclass(frozen=True,slots=True)
class ResultSinkConfig:
    sink_id:str='sf05.jsonl'; sink_version:str='1.0.0'; mode:SinkMode=SinkMode.JSONL; file_scope:FileScope=FileScope.TERMINAL_LOCAL; root_path:str='StrategyFactory'; append_only:bool=True; fail_closed_on_write_error:bool=True; mirror_to_print:bool=False; include_payload_hash:bool=True; flush_every_records:int=32; flush_every_milliseconds:int=1000; max_record_bytes:int=1048576; schema:str='alpha_lab.strategy_factory/result_sink_config@1.0.0'
    def __post_init__(self):
        if self.schema!='alpha_lab.strategy_factory/result_sink_config@1.0.0': raise ValueError('unsupported sink schema')
        if not self.append_only: raise ValueError('append_only required')
        if '..' in self.root_path or not self.root_path: raise ValueError('invalid root_path')
        if not 1<=self.flush_every_records<=100000: raise ValueError('flush_every_records')
        if not 10<=self.flush_every_milliseconds<=3600000: raise ValueError('flush interval')
        if not 256<=self.max_record_bytes<=16777216: raise ValueError('max_record_bytes')
    @property
    def canonical(self)->str: return '|'.join(map(str,[self.schema,self.sink_id,self.sink_version,int(self.mode),int(self.file_scope),self.root_path,str(self.append_only).lower(),str(self.fail_closed_on_write_error).lower(),str(self.mirror_to_print).lower(),str(self.include_payload_hash).lower(),self.flush_every_records,self.flush_every_milliseconds,self.max_record_bytes]))
    @property
    def config_hash(self)->str: return stable_id('snk',self.canonical)
