#ifndef SAED_V4_28_TYPES_MQH
#define SAED_V4_28_TYPES_MQH
struct SAEDV428Evidence { string hypothesis_id; string family_id; int sequence; double anytime_p; double e_value; datetime known_at; datetime decision_time; };
struct SAEDV428Decision { string hypothesis_id; string family_id; int local_index; double alpha; bool rejected; double wealth_before; double wealth_after; };
#endif
