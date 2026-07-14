#ifndef ALPHA_LAB_SAED_V4_EVENT_CONTRACTS
#define ALPHA_LAB_SAED_V4_EVENT_CONTRACTS
struct SAED_EventEnvelope{string stream_id;long source_sequence;datetime event_time;datetime known_time;string event_kind;string subject_id;string payload_hash;string source_hash;};
struct SAED_EventWatermark{string stream_id;datetime maximum_event_time;datetime watermark_time;long accepted_events;long late_events;};
#endif
