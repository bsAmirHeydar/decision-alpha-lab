from __future__ import annotations
from .contracts import PromotionAdmission,ContextOccurrence,ModelOutput
from .enums import CalibrationState,FallbackReason
from .errors import PolicyError

def validate_model_output(admission:PromotionAdmission,occurrence:ContextOccurrence,output:ModelOutput,*,max_uncertainty:float=.35,max_novelty:float=.35,allow_degraded_calibration:bool=False)->tuple[bool,FallbackReason|None,tuple[str,...]]:
    try: admission.assert_ai_usable(occurrence.known_time_ms)
    except PolicyError as e:
        reason=FallbackReason.SIGNATURE_FAILURE if e.code=='signature_failure' else FallbackReason.INVALID_MODEL
        return False,reason,(e.code,)
    if output.model_id!=admission.model_id or output.model_version!=admission.model_version:return False,FallbackReason.INVALID_MODEL,('model_identity_mismatch',)
    if output.occurrence_id!=occurrence.occurrence_id:return False,FallbackReason.INVALID_MODEL,('occurrence_identity_mismatch',)
    if output.as_of_ms>occurrence.known_time_ms:return False,FallbackReason.STALE_FEATURES,('future_model_as_of',)
    if occurrence.known_time_ms>output.valid_until_ms:return False,FallbackReason.STALE_MODEL,('model_output_expired',)
    if occurrence.context_type not in admission.context_types:return False,FallbackReason.OUT_OF_DISTRIBUTION,('unsupported_context_type',)
    missing=sorted(set(output.required_views)-set(occurrence.views_present))
    if missing:return False,FallbackReason.MISSING_VIEW,tuple(f'missing_view:{v}' for v in missing)
    if output.novelty>max_novelty:return False,FallbackReason.OUT_OF_DISTRIBUTION,('novelty_threshold_exceeded',)
    if output.uncertainty>max_uncertainty:return False,FallbackReason.LOW_CONFIDENCE,('uncertainty_threshold_exceeded',)
    if output.calibration_state is CalibrationState.INVALID or output.calibration_state is CalibrationState.UNKNOWN:return False,FallbackReason.INVALID_MODEL,('calibration_invalid',)
    if output.calibration_state is CalibrationState.DEGRADED and not allow_degraded_calibration:return False,FallbackReason.LOW_CONFIDENCE,('calibration_degraded',)
    if set(output.action_probabilities)-set(admission.actions):return False,FallbackReason.UNSUPPORTED_ACTION,('action_support_violation',)
    if set(output.treatment_distribution)-set(admission.treatments):return False,FallbackReason.UNSUPPORTED_TREATMENT,('treatment_support_violation',)
    if set(output.risk_distribution)-set(admission.risk_tiers):return False,FallbackReason.UNSUPPORTED_RISK,('risk_support_violation',)
    return True,None,('model_output_valid',)

def argmax_stable(distribution): return sorted(distribution.items(),key=lambda kv:(-kv[1],kv[0]))[0][0]
