#ifndef ALPHALAB_UCEI16_MIGRATION_MQH
#define ALPHALAB_UCEI16_MIGRATION_MQH
#include "UCEI16_Types.mqh"
struct UCEI16_MigrationUnit { string unit_id; string context_id; UCEI16_MigrationWave wave; bool parity_passed; bool core_invariant; };
bool UCEI16_CanMigrate(const UCEI16_MigrationUnit &u){ return StringLen(u.unit_id)>0 && StringLen(u.context_id)>0 && u.parity_passed && u.core_invariant; }
#endif
