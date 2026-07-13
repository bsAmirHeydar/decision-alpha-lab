#ifndef __UCEI09_REGISTRY_MQH__
#define __UCEI09_REGISTRY_MQH__
#include "UCEI09_Catalog.mqh"
class CUCEI09Registry{private:UCEI09_AlgorithmDescriptor m_items[];bool m_frozen;public:CUCEI09Registry(){m_frozen=false;}bool BuildDefault(){if(m_frozen)return false;ArrayResize(m_items,CUCEI09Catalog::Count());for(int i=0;i<ArraySize(m_items);i++)if(!CUCEI09Catalog::Get(i,m_items[i]))return false;return true;}void Freeze(){m_frozen=true;}bool Frozen()const{return m_frozen;}int Count()const{return ArraySize(m_items);}bool ResolveExact(const string key,UCEI09_AlgorithmDescriptor &out)const{for(int i=0;i<ArraySize(m_items);i++)if(m_items[i].Key()==key){out=m_items[i];return true;}return false;}};
#endif
