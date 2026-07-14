#ifndef ALPHA_LAB_SAED_V4_VIEW_COMPATIBILITY_MQH
#define ALPHA_LAB_SAED_V4_VIEW_COMPATIBILITY_MQH
bool SAEDViewsCompatible(const string left_twin,const string right_twin,const datetime left_known,const datetime right_known,const datetime left_event,const datetime right_event){ return left_twin==right_twin && left_known==right_known && left_event==right_event; }
#endif
