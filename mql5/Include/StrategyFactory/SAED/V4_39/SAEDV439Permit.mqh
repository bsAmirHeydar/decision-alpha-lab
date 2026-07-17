#ifndef SAED_V4_39_PERMIT_MQH
#define SAED_V4_39_PERMIT_MQH
struct SAEDV439Permit { string permit_id; string runtime_hash; datetime valid_from; datetime valid_until; bool signed_by_risk; bool signed_by_operator; bool revoked; };
bool SAEDV439PermitValid(const SAEDV439Permit &p,const datetime now){return false;}
#endif
