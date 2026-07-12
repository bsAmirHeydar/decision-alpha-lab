#ifndef ALPHALAB_UCEI06_TELEMETRY_MQH
#define ALPHALAB_UCEI06_TELEMETRY_MQH
struct UCEI06_Telemetry{long anchor_count;long cube_count;long cell_count;long label_count;long censored_count;long masked_count;long rejected_count;long leakage_finding_count;long build_duration_us;void Reset(){anchor_count=0;cube_count=0;cell_count=0;label_count=0;censored_count=0;masked_count=0;rejected_count=0;leakage_finding_count=0;build_duration_us=0;}};
#endif
