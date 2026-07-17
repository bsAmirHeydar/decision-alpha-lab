#ifndef SAED_V4_39_PAPER_LEDGER_MQH
#define SAED_V4_39_PAPER_LEDGER_MQH
struct SAEDV439PaperEvent { string observation_id; string status; double fill_price; double net_pnl_bps; bool order_submitted; };
#endif
