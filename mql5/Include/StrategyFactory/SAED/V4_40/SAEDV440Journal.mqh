#ifndef __SAEDV440JOURNAL_MQH__
#define __SAEDV440JOURNAL_MQH__
// SAEDV440 static mirror. Reference control-plane contract only.
struct SAEDV440JournalEvent { string event_id; string previous_hash; string cell_id; string action; bool accepted; };
#endif
