from __future__ import annotations
from dataclasses import dataclass,replace
from strategy_factory_contracts.hashing import stable_id
from .enums import GenerationState
_ALLOWED={(GenerationState.DRAFT,GenerationState.COMPILED),(GenerationState.COMPILED,GenerationState.VALIDATED),(GenerationState.VALIDATED,GenerationState.WARMED),(GenerationState.WARMED,GenerationState.ACTIVE),(GenerationState.ACTIVE,GenerationState.RETIRED)}
@dataclass(frozen=True,slots=True)
class RuntimeGeneration:
    generation_id:int; state:GenerationState; run_manifest_id:str; run_manifest_hash:str; plugin_descriptor_hash:str; plugin_requirements_hash:str; plugin_configuration_hash:str; market_configuration_hash:str; sink_configuration_hash:str; compiler_id:str='sf05.generation_compiler'; compiler_version:str='1.0.0'; previous_generation_uid:str=''; compiled_at_utc_msc:int=0; activated_at_utc_msc:int=0; retired_at_utc_msc:int=0; failure_reason:str=''; schema:str='alpha_lab.strategy_factory/runtime_generation@1.0.0'; generation_uid:str=''
    def __post_init__(self):
        if self.generation_id<=0: raise ValueError('generation id')
        if self.generation_uid and self.generation_uid!=self.derived_uid: raise ValueError('generation uid mismatch')
    @property
    def canonical(self)->str:return '|'.join(map(str,[self.schema,self.generation_id,self.run_manifest_id,self.run_manifest_hash,self.plugin_descriptor_hash,self.plugin_requirements_hash,self.plugin_configuration_hash,self.market_configuration_hash,self.sink_configuration_hash,self.compiler_id,self.compiler_version,self.previous_generation_uid,self.compiled_at_utc_msc]))
    @property
    def derived_uid(self)->str:return stable_id('gen',self.canonical)
    def materialized(self)->'RuntimeGeneration':return self if self.generation_uid else replace(self,generation_uid=self.derived_uid)
    def transition(self,to:GenerationState,now_utc_msc:int,reason:str='')->'RuntimeGeneration':
        if to is GenerationState.FAILED and self.state is not GenerationState.RETIRED:return replace(self,state=to,failure_reason=reason)
        if (self.state,to) not in _ALLOWED: raise ValueError(f'illegal generation transition {self.state.name}->{to.name}')
        kw={'state':to}
        if to is GenerationState.ACTIVE:kw['activated_at_utc_msc']=now_utc_msc
        if to is GenerationState.RETIRED:kw['retired_at_utc_msc']=now_utc_msc
        return replace(self,**kw)
