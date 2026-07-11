from __future__ import annotations
from .enums import IntegrationMode, LegacyDirection, LegacySide
from .models import AdapterConfig, LegacyDivergenceCandidate

def reference_config()->AdapterConfig:
    return AdapterConfig("SPXUSD","NDXUSD",group_minutes=(15,60),mode=IntegrationMode.AUDIT_ONLY)

def reference_candidates()->tuple[LegacyDivergenceCandidate,...]:
    common=dict(current_cycle_index=4,current_cycle_number=5,reference_cycle_index=3,reference_cycle_number=4,trading_day_start_ny_s=1783771200,trading_day_end_ny_s=1783857600,current_cycle_start_ny_s=1783792800,current_cycle_end_ny_s=1783793700,reference_cycle_start_ny_s=1783791900,reference_cycle_end_ny_s=1783792800,one_sided_hunt=True,data_ready=True)
    return (
      LegacyDivergenceCandidate("EXP0017|cg_15m|buy","cg_15m",15,direction=LegacyDirection.BUY,side=LegacySide.LOW,hunter_symbol="SPXUSD",clean_symbol="NDXUSD",hunter_reference_price=6240.0,clean_reference_price=22400.0,hunter_current_extreme=6238.0,clean_current_extreme=22402.0,clean_stop_reference_price=22400.0,note="one sided low hunt",**common),
      LegacyDivergenceCandidate("EXP0017|cg_60m|sell","cg_60m",60,direction=LegacyDirection.SELL,side=LegacySide.HIGH,hunter_symbol="NDXUSD",clean_symbol="SPXUSD",hunter_reference_price=22500.0,clean_reference_price=6260.0,hunter_current_extreme=22508.0,clean_current_extreme=6258.0,clean_stop_reference_price=6260.0,note="one sided high hunt",**{**common,"current_cycle_start_ny_s":1783794000,"current_cycle_end_ny_s":1783797600,"reference_cycle_start_ny_s":1783790400,"reference_cycle_end_ny_s":1783794000}),
    )
