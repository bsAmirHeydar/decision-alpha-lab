from __future__ import annotations
from dataclasses import dataclass
from .manifest import RunManifest
from .generation import RuntimeGeneration
from .enums import GenerationState
@dataclass(frozen=True,slots=True)
class CompilationEvidence:
    plugin_descriptor_hash:str; plugin_requirements_hash:str; descriptor_valid:bool=True; requirements_ready:bool=True
class GenerationCompiler:
    def compile(self,manifest:RunManifest,evidence:CompilationEvidence,previous_generation_uid:str='')->RuntimeGeneration:
        m=manifest.materialized()
        if not evidence.descriptor_valid or not evidence.requirements_ready: raise ValueError('plugin not ready')
        g=RuntimeGeneration(generation_id=m.requested_generation_id,state=GenerationState.DRAFT,run_manifest_id=m.manifest_id,run_manifest_hash=m.manifest_hash,plugin_descriptor_hash=evidence.plugin_descriptor_hash,plugin_requirements_hash=evidence.plugin_requirements_hash,plugin_configuration_hash=m.plugin_configuration_hash,market_configuration_hash=m.market_configuration_hash,sink_configuration_hash=m.sink_config.config_hash,previous_generation_uid=previous_generation_uid,compiled_at_utc_msc=m.created_at_utc_msc).materialized()
        return g.transition(GenerationState.COMPILED,m.created_at_utc_msc).transition(GenerationState.VALIDATED,m.created_at_utc_msc).transition(GenerationState.WARMED,m.created_at_utc_msc)
