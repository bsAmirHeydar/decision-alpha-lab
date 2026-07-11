from __future__ import annotations
from dataclasses import dataclass,asdict
from strategy_factory_contracts.hashing import stable_id
from .sink_config import ResultSinkConfig
@dataclass(frozen=True,slots=True)
class PluginSelection:
    plugin_id:str; exact_version:str; required_capabilities:int=0; expected_descriptor_hash:str=''
@dataclass(frozen=True,slots=True)
class RunManifest:
    run_id:str; strategy_id:str; strategy_version:str; run_mode:int; requested_generation_id:int; plugin_selection:PluginSelection; plugin_configuration_hash:str; market_configuration_hash:str; sink_config:ResultSinkConfig; git_commit:str; build_id:str; environment_id:str; terminal_instance_id:str; strict_fail_closed:bool; created_at_utc_msc:int; schema:str='alpha_lab.strategy_factory/run_manifest@1.0.0'; manifest_id:str=''
    def __post_init__(self):
        if self.requested_generation_id<=0: raise ValueError('generation id')
        if self.schema!='alpha_lab.strategy_factory/run_manifest@1.0.0': raise ValueError('schema')
        if self.manifest_id and self.manifest_id!=self.derived_id: raise ValueError('manifest_id mismatch')
    @property
    def canonical(self)->str:
        p=self.plugin_selection
        return '|'.join(map(str,[self.schema,self.run_id,self.strategy_id,self.strategy_version,self.run_mode,self.requested_generation_id,p.plugin_id,p.exact_version,p.required_capabilities,p.expected_descriptor_hash,self.plugin_configuration_hash,self.market_configuration_hash,self.sink_config.config_hash,self.git_commit,self.build_id,self.environment_id,self.terminal_instance_id,str(self.strict_fail_closed).lower(),self.created_at_utc_msc]))
    @property
    def derived_id(self)->str:return stable_id('man',self.canonical)
    @property
    def manifest_hash(self)->str:return stable_id('mnh',self.canonical)
    def materialized(self)->'RunManifest':
        return self if self.manifest_id else RunManifest(**{**asdict(self),'plugin_selection':self.plugin_selection,'sink_config':self.sink_config,'manifest_id':self.derived_id})
