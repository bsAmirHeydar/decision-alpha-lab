#ifndef ALPHALAB_UCEI07_TRAINER_REGISTRY_MQH
#define ALPHALAB_UCEI07_TRAINER_REGISTRY_MQH
#include "UCEI07_Contracts.mqh"
#include "UCEI07_Identity.mqh"
class CUCEI07TrainerRegistry{
private:
 UCEI07_TrainerCapability m_items[];bool m_frozen;
public:
 CUCEI07TrainerRegistry(){m_frozen=false;ArrayResize(m_items,0);}
 bool Register(const UCEI07_TrainerCapability &item,string &reason){reason="";if(m_frozen){reason="registry_frozen";return false;}string key=UCEI07_TrainerKey(item.trainer_id,item.trainer_version);for(int i=0;i<ArraySize(m_items);i++)if(UCEI07_TrainerKey(m_items[i].trainer_id,m_items[i].trainer_version)==key){reason="duplicate_exact_version";return false;}int n=ArraySize(m_items);ArrayResize(m_items,n+1);m_items[n]=item;return true;}
 void Freeze(){m_frozen=true;}
 bool ResolveExact(const string trainer_id,const string trainer_version,UCEI07_TrainerCapability &out,string &reason)const{reason="";string key=UCEI07_TrainerKey(trainer_id,trainer_version);for(int i=0;i<ArraySize(m_items);i++)if(UCEI07_TrainerKey(m_items[i].trainer_id,m_items[i].trainer_version)==key){out=m_items[i];return true;}reason="trainer_exact_version_not_found";return false;}
 int Size()const{return ArraySize(m_items);} bool Frozen()const{return m_frozen;}
 string SnapshotHash()const{string material="";for(int i=0;i<ArraySize(m_items);i++)material+=UCEI07_TrainerKey(m_items[i].trainer_id,m_items[i].trainer_version)+"|"+m_items[i].descriptor_hash+";";return UCEI07_StableId("ucereg",material);}
};
#endif
