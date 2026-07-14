#ifndef ALPHA_LAB_SAED_V4_VIEW_CONTRACTS_MQH
#define ALPHA_LAB_SAED_V4_VIEW_CONTRACTS_MQH
#include "ViewEnums.mqh"
struct SAEDViewFeatureValue { string feature_id; double numeric_value; string string_value; bool bool_value; bool missing; bool stale; int mask; double quality; string source_hash; };
struct SAEDViewHeader { string view_id; string specification_id; string twin_id; ENUM_SAED_VIEW_KIND kind; ENUM_SAED_VIEW_STATUS status; datetime known_as_of; datetime event_as_of; string view_hash; string lineage_root; };
struct SAEDViewPackageHeader { string package_id; string twin_id; datetime known_as_of; datetime event_as_of; int view_count; string package_hash; string lineage_root; };
#endif
