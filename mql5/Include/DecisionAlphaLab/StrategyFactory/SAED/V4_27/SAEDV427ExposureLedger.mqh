#ifndef SAED_V4_27_EXPOSURE_LEDGER_MQH
#define SAED_V4_27_EXPOSURE_LEDGER_MQH
bool SAEDV427ExposureAllowed(const int role){ return !SAEDV427IsProtectedRole(role); }
#endif
