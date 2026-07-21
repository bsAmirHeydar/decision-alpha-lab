#ifndef __LCM10B_TYPES_MQH__
#define __LCM10B_TYPES_MQH__
enum ENUM_LCM10B_SIDE { LCM10B_SIDE_UNKNOWN=0, LCM10B_SIDE_BUY=1, LCM10B_SIDE_SELL=-1 };
enum ENUM_LCM10B_ENTRY_KIND { LCM10B_ENTRY_UNSPECIFIED=0, LCM10B_ENTRY_MARKET=1, LCM10B_ENTRY_LIMIT=2, LCM10B_ENTRY_STOP=3, LCM10B_ENTRY_STOP_LIMIT=4 };
enum ENUM_LCM10B_RESULT { LCM10B_RESULT_BLOCKED=0, LCM10B_RESULT_DRY_REFERENCE=1 };
struct LCM10BExecutionIntent { string intent_id; string treatment_package_id; string symbol; ENUM_LCM10B_SIDE side; ENUM_LCM10B_ENTRY_KIND entry_kind; double entry_price; double stop_price; double volume_value; datetime decision_time; datetime availability_time; bool submission_requested; };
#endif
