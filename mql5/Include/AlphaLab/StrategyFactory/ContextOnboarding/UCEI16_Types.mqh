#ifndef ALPHALAB_UCEI16_TYPES_MQH
#define ALPHALAB_UCEI16_TYPES_MQH
enum UCEI16_MigrationWave { UCEI16_WAVE_A=0, UCEI16_WAVE_B=1, UCEI16_WAVE_C=2 };
enum UCEI16_ParityStatus { UCEI16_PARITY_PASS=0, UCEI16_PARITY_FAIL=1, UCEI16_PARITY_INSUFFICIENT=2 };
enum UCEI16_InvarianceStatus { UCEI16_INVARIANCE_PASS=0, UCEI16_INVARIANCE_FAIL=1, UCEI16_ADR_REQUIRED=2 };
struct UCEI16_FeatureSpec { string feature_id; string dtype; string known_time_rule; bool required; };
struct UCEI16_ContextSpec { string context_id; string version; UCEI16_MigrationWave wave; string doctrine_hash; string manual_policy_id; };
#endif
