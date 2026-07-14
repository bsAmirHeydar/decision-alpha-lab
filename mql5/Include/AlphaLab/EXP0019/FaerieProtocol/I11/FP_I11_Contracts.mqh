#ifndef __FP_I11_CONTRACTS_MQH__
#define __FP_I11_CONTRACTS_MQH__
#include "FP_I11_Enums.mqh"
struct SFP_I11_Config {
 string instance_id,object_namespace; ENUM_FP_I11_VISUAL_MODE mode; int history_days,max_objects,lane_count;
 bool show_sessions,show_references,show_hunts,show_candidates,show_confirmed,show_ww,show_suppressed,show_health;
};
struct SFP_I11_Style { color stroke,fill; int width,line_style,opacity,font_size,z_order; string style_id; };
struct SFP_I11_ObjectSpec {
 string object_id,semantic_id,text,tooltip,semantic_hash,projection_hash,reason_code;
 ENUM_FP_I11_OBJECT_KIND kind; ENUM_FP_I11_VISUAL_STATE state; int layer;
 datetime time1,time2; double price1,price2; int corner,x,y; bool immutable;
 SFP_I11_Style style;
};
struct SFP_I11_WindowFact { string window_id,kind,state,semantic_hash; datetime start_time,end_time; double high_price,low_price; };
struct SFP_I11_ReferenceFact { string reference_id,symbol,side,state,semantic_hash; datetime start_time,end_time; double price; };
struct SFP_I11_HuntFact { string hunt_id,symbol,side,role,semantic_hash; datetime hunt_time; double price; };
struct SFP_I11_SignalFact { string signal_id,relation,direction,hunter_symbol,protected_symbol,state,semantic_hash,reason_code; ENUM_FP_I11_SIGNAL_DISPOSITION disposition; datetime first_hunt_time,confirmation_time; double hunter_price,protected_price; };
struct SFP_I11_WWFact { string context_id,direction,state,hunter_symbol,protected_symbol,semantic_hash; datetime start_time,end_time; };
struct SFP_I11_ProjectionStats { long frame_sequence; int created,updated,deleted,unchanged,retained_immutable,total_objects; bool degraded; string reason_code; };
#endif
