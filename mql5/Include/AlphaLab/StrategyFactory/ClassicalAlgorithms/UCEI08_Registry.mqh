#ifndef UCEI08_REGISTRY_MQH
#define UCEI08_REGISTRY_MQH
#include "UCEI08_AlgorithmDescriptor.mqh"
class CUCEI08_Registry{
 private:UCEI08_AlgorithmDescriptor m_items[];bool m_frozen;
 public:
 CUCEI08_Registry():m_frozen(false){}
 bool Register(const UCEI08_AlgorithmDescriptor &d){if(m_frozen || !d.IsValid())return false;for(int i=0;i<ArraySize(m_items);i++)if(m_items[i].Key()==d.Key())return false;int n=ArraySize(m_items);ArrayResize(m_items,n+1);m_items[n]=d;return true;}
 void Freeze(){m_frozen=true;}
 bool Frozen()const{return m_frozen;}
 int Size()const{return ArraySize(m_items);}
 bool ResolveExact(const string key,UCEI08_AlgorithmDescriptor &out)const{for(int i=0;i<ArraySize(m_items);i++)if(m_items[i].Key()==key){out=m_items[i];return true;}return false;}
};
#endif
