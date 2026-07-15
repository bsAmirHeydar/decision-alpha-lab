#ifndef __SAED_V4_EXECUTION_TWIN_HANDOFF_MQH__
#define __SAED_V4_EXECUTION_TWIN_HANDOFF_MQH__
bool SAEDV409HandoffAuthoritySafe(const bool send_order,const bool select_treatment,const bool replace_shadow){return !send_order && !select_treatment && !replace_shadow;}
#endif
