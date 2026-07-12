#ifndef UCEI05_RESERVATION_LEDGER_MQH
#define UCEI05_RESERVATION_LEDGER_MQH
#include "UCEI05_MaximumLossSolver.mqh"
class CUCEI05ReservationLedger {
private: UCEI05_ReservationRecord m_records[]; long m_sequence;
 int Find(const string id) const { for(int i=0;i<ArraySize(m_records);i++) if(m_records[i].reservation_id==id)return i; return -1; }
public:
 CUCEI05ReservationLedger(){m_sequence=0;}
 int Count() const{return ArraySize(m_records);} double TotalOpen() const{double x=0.0;for(int i=0;i<ArraySize(m_records);i++)x+=MathMax(0.0,m_records[i].reserved_cash-m_records[i].consumed_cash-m_records[i].released_cash);return x;}
 bool Reserve(const string id,const string account,const string treatment,const double cash){if(Find(id)>=0||cash<0.0)return false;int n=ArraySize(m_records);ArrayResize(m_records,n+1);m_records[n].reservation_id=id;m_records[n].account_id=account;m_records[n].treatment_id=treatment;m_records[n].reserved_cash=cash;m_records[n].consumed_cash=0.0;m_records[n].released_cash=0.0;m_records[n].state=UCEI05_RESERVED;m_records[n].last_sequence=++m_sequence;return true;}
 bool Consume(const string id,const double cash){int i=Find(id);if(i<0||cash<0.0||cash>m_records[i].reserved_cash-m_records[i].consumed_cash-m_records[i].released_cash+1e-8)return false;m_records[i].consumed_cash+=cash;m_records[i].state=(m_records[i].consumed_cash+m_records[i].released_cash>=m_records[i].reserved_cash?UCEI05_CONSUMED:UCEI05_PARTIALLY_CONSUMED);m_records[i].last_sequence=++m_sequence;return true;}
 bool Release(const string id,const double cash){int i=Find(id);if(i<0||cash<0.0||cash>m_records[i].reserved_cash-m_records[i].consumed_cash-m_records[i].released_cash+1e-8)return false;m_records[i].released_cash+=cash;m_records[i].state=(m_records[i].consumed_cash+m_records[i].released_cash>=m_records[i].reserved_cash?UCEI05_RELEASED:UCEI05_ADJUSTED);m_records[i].last_sequence=++m_sequence;return true;}
};
#endif
