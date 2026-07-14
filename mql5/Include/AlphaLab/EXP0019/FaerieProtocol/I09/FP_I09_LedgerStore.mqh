#ifndef __FP_I09_LEDGER_STORE_MQH__
#define __FP_I09_LEDGER_STORE_MQH__
#include "FP_I09_EventChain.mqh"
class CFP_I09_LedgerStore { private: FP_I09_LedgerEvent m_events[]; public: int Size(){return ArraySize(m_events);} bool Append(const FP_I09_LedgerEvent &e){ int n=ArraySize(m_events); if(e.sequence!=n) return false; if(n>0 && e.prior_event_hash!=m_events[n-1].event_hash) return false; ArrayResize(m_events,n+1); m_events[n]=e; return true; } };
#endif
