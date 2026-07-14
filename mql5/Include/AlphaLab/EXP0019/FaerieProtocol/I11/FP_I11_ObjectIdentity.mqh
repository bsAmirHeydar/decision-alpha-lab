#ifndef __FP_I11_OBJECT_IDENTITY_MQH__
#define __FP_I11_OBJECT_IDENTITY_MQH__
#include <AlphaLab/EXP0019/FaerieProtocol/I10/FP_I10_Hash.mqh>
#include "FP_I11_Contracts.mqh"
string FP_I11_KindCode(ENUM_FP_I11_OBJECT_KIND k){string v[13]={"SESS","WEEK","REFL","REFX","HUNT","ROLE","CAND","CONF","INVAL","WW","SUP","WIN","HLTH"};return v[(int)k];}
string FP_I11_ObjectId(string ns,ENUM_FP_I11_OBJECT_KIND k,string semantic_id){string nh=FP_I10_StableId("N",ns),oh=FP_I10_StableId("O",semantic_id+"|"+FP_I11_KindCode(k));return "FP19::"+StringSubstr(nh,2,8)+"::"+FP_I11_KindCode(k)+"::"+StringSubstr(oh,2,16);}
string FP_I11_ProjectionHash(const SFP_I11_ObjectSpec &s){return FP_I10_StableId("P",s.object_id+"|"+s.semantic_hash+"|"+s.style.style_id+"|"+IntegerToString((long)s.time1)+"|"+IntegerToString((long)s.time2)+"|"+DoubleToString(s.price1,8)+"|"+DoubleToString(s.price2,8)+"|"+s.text+"|"+IntegerToString((int)s.state));}
#endif
