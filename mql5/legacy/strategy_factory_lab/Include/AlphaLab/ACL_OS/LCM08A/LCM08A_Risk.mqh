#ifndef ALPHALAB_ACL_OS_LCM08A_RISK_MQH
#define ALPHALAB_ACL_OS_LCM08A_RISK_MQH
bool LCM08A_IsCriticalDimension(const string dimension){return dimension=="EXECUTION_COUPLING"||dimension=="BROKER_OR_NETWORK_COUPLING"||dimension=="CURRENT_BAR_OR_FUTURE_AWARENESS"||dimension=="NONDETERMINISM"||dimension=="SECURITY_SENSITIVITY"||dimension=="IDENTITY_AMBIGUITY";}
#endif
