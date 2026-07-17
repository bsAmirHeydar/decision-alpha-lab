#ifndef SAED_V4_29_TRANSPORT_LEDGER_MQH
#define SAED_V4_29_TRANSPORT_LEDGER_MQH
bool SAEDV429TransportValid(const int one_way_flows,const int round_trips,const int raw_hidden_transfers){ return one_way_flows==3 && round_trips==0 && raw_hidden_transfers==0; }
#endif
