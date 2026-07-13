#ifndef __FP_I05_WINDOW_STORE_MQH__
#define __FP_I05_WINDOW_STORE_MQH__
#include "FP_I05_Contracts.mqh"
class FP_I05_WindowStore {
 private: FP_I05_PairWindowAggregate m_windows[]; FP_I05_ReferenceLevel m_refs[];
 public:
  void Clear(){ ArrayResize(m_windows,0); ArrayResize(m_refs,0); }
  int WindowCount() const { return ArraySize(m_windows); }
  int ReferenceCount() const { return ArraySize(m_refs); }
  bool AddWindow(const FP_I05_PairWindowAggregate &value){ if(!value.Valid()) return false; int n=ArraySize(m_windows); ArrayResize(m_windows,n+1); m_windows[n]=value; return true; }
  bool AddReference(const FP_I05_ReferenceLevel &value){ if(!value.Valid()) return false; int n=ArraySize(m_refs); ArrayResize(m_refs,n+1); m_refs[n]=value; return true; }
  bool FindWindow(const string trading_date,const FP_I05_WINDOW_KIND kind,FP_I05_PairWindowAggregate &out) const { for(int i=0;i<ArraySize(m_windows);i++) if(m_windows[i].descriptor.trading_date==trading_date && m_windows[i].descriptor.kind==kind){ out=m_windows[i]; return true; } return false; }
};
#endif
