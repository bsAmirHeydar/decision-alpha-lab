#ifndef ALPHALAB_ACL05_ENVIRONMENT_LOCK_MQH
#define ALPHALAB_ACL05_ENVIRONMENT_LOCK_MQH
struct ACL05EnvironmentLock { string environment_id; string environment_digest; bool network_allowed; bool secrets_allowed; bool order_submission_allowed; bool capital_activation_allowed; };
bool ACL05EnvironmentValid(const ACL05EnvironmentLock &x){ return StringLen(x.environment_id)>0 && StringLen(x.environment_digest)==71 && !x.network_allowed && !x.secrets_allowed && !x.order_submission_allowed && !x.capital_activation_allowed; }
#endif
