#ifndef ALPHALAB_UCEI14_JOURNAL
#define ALPHALAB_UCEI14_JOURNAL
#include "UCEI14_Canonical.mqh"
class CUCEI14DecisionJournal{private:string m_keys[];public:bool Contains(const string key){for(int i=0;i<ArraySize(m_keys);i++)if(m_keys[i]==key)return(true);return(false);}bool Append(const string key){if(Contains(key))return(false);int n=ArraySize(m_keys);ArrayResize(m_keys,n+1);m_keys[n]=key;return(true);}int Size(){return(ArraySize(m_keys));}};
#endif
