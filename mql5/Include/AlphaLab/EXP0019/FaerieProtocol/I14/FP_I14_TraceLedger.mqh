#ifndef __FP_I14_TRACE_LEDGER_MQH__
#define __FP_I14_TRACE_LEDGER_MQH__
#include "FP_I14_Contracts.mqh"
#include "FP_I14_Hash.mqh"
class CFP_I14_TraceLedger {
 private: FP_I14_TraceEvent m_events[]; string m_hashes[]; string m_chain; long m_duplicates;
 public:
  CFP_I14_TraceLedger(){ m_chain="00000000";m_duplicates=0; }
  bool Append(const FP_I14_TraceEvent &e,string &reason){
   string fp=FP_I14_EventFingerprint(e);
   for(int i=0;i<ArraySize(m_events);i++) if(m_events[i].semantic_id==e.semantic_id && m_events[i].sequence==e.sequence){ if(m_hashes[i]==fp){m_duplicates++;reason="FP_DIAG_DUPLICATE_IGNORED";return true;} reason="FP_DIAG_DUPLICATE_COLLISION";return false; }
   int n=ArraySize(m_events); if(n>0 && e.sequence<=m_events[n-1].sequence){reason="FP_DIAG_SEQUENCE_REGRESSION";return false;}
   ArrayResize(m_events,n+1);ArrayResize(m_hashes,n+1);m_events[n]=e;m_hashes[n]=fp;m_chain=FP_I14_HashText(m_chain+"|"+fp);reason="FP_DIAG_EVENT_APPLIED";return true;
  }
  int Count()const{return ArraySize(m_events);} long Duplicates()const{return m_duplicates;} string ChainHash()const{return m_chain;} bool Get(const int index,FP_I14_TraceEvent &out)const{if(index<0||index>=ArraySize(m_events))return false;out=m_events[index];return true;}
};
#endif
