from .contracts import OutputBufferFrame
from .constants import BUFFER_NAMES,OUTPUT_VERSION
from .canonical import canonical_sha256,stable_id

def project_buffers(*,health,lifecycle,data_readiness,active_ww_direction,confirmed_signal_count,allowed_signal_count,suppressed_by_ww_count,suppressed_by_quota_count,quota_winner_signal_id,ledger_event_count,source_revision_sequence,generated_utc_ms,enabled=True):
    values=(
        float(int(health)),float(int(lifecycle)),float(int(data_readiness)),float(int(active_ww_direction)),
        float(confirmed_signal_count),float(allowed_signal_count),float(suppressed_by_ww_count),float(suppressed_by_quota_count),
        1.0 if quota_winner_signal_id else 0.0,float(ledger_event_count),float(source_revision_sequence),float(generated_utc_ms//60000),
    )
    payload={'names':BUFFER_NAMES,'values':values,'available':bool(enabled),'generated_utc_ms':generated_utc_ms,'output_version':OUTPUT_VERSION}
    return OutputBufferFrame(stable_id('FPBUF',payload),values,bool(enabled),generated_utc_ms,OUTPUT_VERSION,canonical_sha256(payload))

def buffer_mapping(): return tuple(enumerate(BUFFER_NAMES))
