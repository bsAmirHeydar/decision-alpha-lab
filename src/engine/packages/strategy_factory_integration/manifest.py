from __future__ import annotations
from .enums import IntegrationMode
from .hashing import canonical_hash
from .models import AdapterConfig, IntegrationManifest, MigrationWave

def build_manifest(config:AdapterConfig,run_id:str,generation_id:str,legacy_source_hash:str,created_at_utc_ms:int)->IntegrationManifest:
    provisional=IntegrationManifest("pending",run_id,generation_id,"exp0017_cycle_group_divergence","sf20.exp0017.temporal_intermarket_divergence","1.0.0",config.config_hash,legacy_source_hash,20,config.mode,False,created_at_utc_ms,("context","candidate","outcome","inference","decision","paper_shadow","monitoring"),(("anatomy_event","1.0.0"),("context_frame","1.0.0"),("trade_candidate","1.0.0"),("outcome_record","1.0.0"),("inference_result","1.0.0"),("execution_intent","1.0.0")))
    object.__setattr__(provisional,"manifest_id",canonical_hash(provisional,"sf20manifest"))
    return provisional

def default_migration_waves()->tuple[MigrationWave,...]:
    return (
      MigrationWave("sf20-wave-01",1,"EXP0017 Temporal Intermarket Divergence",("mql5/Include/IntermarketDivergenceExecution/CG","mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Divergence_Anatomy.mq5"),"sf20.exp0017.temporal_intermarket_divergence","legacy golden ledger available","differential parity and shadow stability","PILOT"),
      MigrationWave("sf20-wave-02",2,"NDS Hook F Rally Zone",("mql5/Include/DecisionAlphaLab/NDS",),"sf20.nds.hook_f_rally_zone","EXP0017 pilot stable","canonical event parity","PLANNED"),
      MigrationWave("sf20-wave-03",3,"Daye Cycle Groups",("mql5/Include/DecisionAlphaLab/Daye",),"sf20.daye.cycle_groups","NDS adapter stable","cycle replay parity","PLANNED"),
      MigrationWave("sf20-wave-04",4,"Structural Nodes",("mql5/Include/DecisionAlphaLab/Nodes",),"sf20.structural.nodes","source inventory frozen","node reveal-time parity","PLANNED"),
      MigrationWave("sf20-wave-05",5,"ICT Deterministic",("mql5/Include/DecisionAlphaLab/ICT",),"sf20.ict.deterministic","hard-rule inventory approved","event ledger parity","PLANNED"),
      MigrationWave("sf20-wave-06",6,"Astro and Auxiliary Features",("mql5/Include/Astro",),"sf20.astro.feature_pack","feature-only authority declared","feature parity","PLANNED"),
      MigrationWave("sf20-wave-07",7,"Manual Setup Adapters",("docs/manual_setups",),"sf20.manual.setup_adapter","manual schema approved","replayable annotation lineage","PLANNED"),
    )
