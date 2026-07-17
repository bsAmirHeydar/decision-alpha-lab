#ifndef FP_SAEDV430SECURITY_MQH
#define FP_SAEDV430SECURITY_MQH
struct FP_SAEDV430SecurityReview { int network_events; int install_events; int adaptation_events; int raw_transfers; int hidden_label_exports; bool default_deny_verified; bool passed; };
bool FP_SAEDV430SecurityPassed(const FP_SAEDV430SecurityReview &value) { return(value.network_events==0 && value.install_events==0 && value.adaptation_events==0 && value.raw_transfers==0 && value.hidden_label_exports==0 && value.default_deny_verified && value.passed); }
#endif
