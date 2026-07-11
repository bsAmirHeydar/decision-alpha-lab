from dataclasses import dataclass
from strategy_factory_contracts.hashing import stable_id
from strategy_factory_contracts.validation import validate_safe_identifier
from .enums import Capability,PluginKind,QueueOverflowPolicy,UpdateScope
from .semver import validate_semver
SCHEMA="alpha_lab.strategy_factory/plugin_descriptor@1.0.0"
@dataclass(frozen=True,slots=True)
class PluginDescriptor:
    plugin_id:str;display_name:str;version:str;kind:PluginKind;provider_id:str;provider_version:str;capability_mask:Capability;update_scope_mask:UpdateScope;event_queue_capacity:int;queue_overflow_policy:QueueOverflowPolicy;deterministic:bool;replay_safe:bool;fast_path_safe:bool;stateful:bool;description:str;configuration_schema_hash:str;descriptor_schema:str=SCHEMA
    def __post_init__(self):
        if self.descriptor_schema!=SCHEMA: raise ValueError("unsupported descriptor schema")
        validate_safe_identifier(self.plugin_id,"plugin_id");validate_safe_identifier(self.provider_id,"provider_id");validate_semver(self.version);validate_semver(self.provider_version)
        if not self.display_name or len(self.display_name)>128: raise ValueError("invalid display_name")
        if self.update_scope_mask==UpdateScope.NONE: raise ValueError("missing update scope")
        if not 1<=self.event_queue_capacity<=65536: raise ValueError("queue capacity out of range")
        if self.fast_path_safe and not self.deterministic: raise ValueError("fast path requires deterministic")
        if self.replay_safe and not self.deterministic: raise ValueError("replay requires deterministic")
        if not self.configuration_schema_hash: raise ValueError("configuration hash required")
    @property
    def canonical_payload(self):
        return "|".join([self.descriptor_schema,self.plugin_id,self.display_name,self.version,str(list(PluginKind).index(self.kind)+1),self.provider_id,self.provider_version,str(int(self.capability_mask)),str(int(self.update_scope_mask)),str(self.event_queue_capacity),self.queue_overflow_policy.value,str(self.deterministic).lower(),str(self.replay_safe).lower(),str(self.fast_path_safe).lower(),str(self.stateful).lower(),self.configuration_schema_hash])
    @property
    def descriptor_hash(self): return stable_id("plg",self.canonical_payload)
@dataclass(frozen=True,slots=True)
class PluginSelection:
    plugin_id:str;exact_version:str;required_capabilities:Capability=Capability.NONE;expected_descriptor_hash:str=""
    def __post_init__(self): validate_safe_identifier(self.plugin_id,"plugin_id");validate_semver(self.exact_version)
    def matches(self,d): return d.plugin_id==self.plugin_id and d.version==self.exact_version and d.capability_mask&self.required_capabilities==self.required_capabilities and (not self.expected_descriptor_hash or d.descriptor_hash==self.expected_descriptor_hash)
