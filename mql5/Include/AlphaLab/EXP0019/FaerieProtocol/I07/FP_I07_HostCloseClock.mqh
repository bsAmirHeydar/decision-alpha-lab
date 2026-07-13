#ifndef FP_I07_HOST_CLOSE_CLOCK_MQH
#define FP_I07_HOST_CLOSE_CLOCK_MQH
bool FP_I07_IsClosedBar(const SFP_I07_HostBar &bar, const datetime now_utc) { return bar.is_closed && now_utc>=bar.close_time; }
bool FP_I07_CloseInsideDeadline(const SFP_I07_HostBar &bar, const SFP_I07_Projection &projection) { return bar.close_time<projection.deadline; }
#endif
