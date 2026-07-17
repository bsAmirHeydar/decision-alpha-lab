#ifndef FP_SAEDV430ENVIRONMENT_MQH
#define FP_SAEDV430ENVIRONMENT_MQH
struct FP_SAEDV430Environment { string environment_id; string dependency_lock_hash; string image_hash; bool network_access; bool package_installation; bool interactive_shell; bool mutable_clock; bool shared_mutable_state; };
bool FP_SAEDV430EnvironmentDefaultDeny(const FP_SAEDV430Environment &value) { return(!value.network_access && !value.package_installation && !value.interactive_shell && !value.mutable_clock && !value.shared_mutable_state); }
#endif
