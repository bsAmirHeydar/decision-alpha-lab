#ifndef __UCEI03_REGISTRY_MQH__
#define __UCEI03_REGISTRY_MQH__
#include "UCEI03_PriceMath.mqh"
class CUCEI03ExactRegistry{
private:ENUM_UCEI03_ATOM_KIND m_kind;UCEI03_AtomDescriptor m_items[];bool m_frozen;
public:CUCEI03ExactRegistry(const ENUM_UCEI03_ATOM_KIND kind){m_kind=kind;m_frozen=false;ArrayResize(m_items,0);}bool Register(UCEI03_AtomDescriptor &d,string &error){if(m_frozen){error="registry frozen";return false;}if(d.kind!=m_kind){error="registry kind mismatch";return false;}if(!UCEI03_ValidateDescriptor(d,error))return false;for(int i=0;i<ArraySize(m_items);i++)if(m_items[i].atom_id==d.atom_id&&m_items[i].version==d.version){error="duplicate exact atom version";return false;}UCEI03_SealDescriptor(d);int n=ArraySize(m_items);ArrayResize(m_items,n+1);m_items[n]=d;error="";return true;}void Freeze(){m_frozen=true;}int Count()const{return ArraySize(m_items);}bool Resolve(const string id,const string version,UCEI03_AtomDescriptor &out)const{for(int i=0;i<ArraySize(m_items);i++)if(m_items[i].atom_id==id&&m_items[i].version==version){out=m_items[i];return true;}return false;}bool Get(const int index,UCEI03_AtomDescriptor &out)const{if(index<0||index>=ArraySize(m_items))return false;out=m_items[index];return true;}string SnapshotId()const{string m=UCEI03_KindName(m_kind);for(int i=0;i<ArraySize(m_items);i++)m+="|"+m_items[i].definition_id;return "ucers_"+UCE03_Fnv1a64HexUtf8(m);}
};
#endif
