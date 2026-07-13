from __future__ import annotations
from .canonical import canonical_sha256,stable_id
from .contracts import ConfirmationProjection,HostBar
from .errors import FPI07Error
from fp_i06_relations.enums import CandidateState

def project_candidate(candidate,bars,config):
    if candidate.state is not CandidateState.RAW_ACTIVE: raise FPI07Error("FP_CRC_CANDIDATE_NOT_ACTIVE","only active candidate can be projected")
    eligible=tuple(sorted((b for b in bars if b.canonical_symbol==config.host_symbol and b.timeframe is config.host_timeframe and b.close_utc_ms>candidate.first_hunt_minute_utc_ms),key=lambda b:(b.close_utc_ms,b.open_utc_ms,b.host_bar_id)))
    if not eligible: raise FPI07Error("FP_CRC_TARGET_BAR_UNAVAILABLE","no eligible host bar supplied")
    target=eligible[0]
    material={"candidate":candidate.semantic_hash,"host":config.host_symbol,"tf":config.host_timeframe,"bar":target.host_bar_id,"open":target.open_utc_ms,"close":target.close_utc_ms,"deadline":candidate.check_end_utc_ms,"config":config.config_hash}
    return ConfirmationProjection(stable_id("FPPROJ",material,32),candidate.candidate_id,candidate.side_plan_id,config.host_symbol,config.host_timeframe,candidate.first_hunt_minute_utc_ms,candidate.check_end_utc_ms,target.host_bar_id,target.open_utc_ms,target.close_utc_ms,candidate.semantic_hash,config.config_hash,canonical_sha256(material))

def first_eligible_bar(candidate,bars,config): return project_candidate(candidate,bars,config).target_host_bar_id
