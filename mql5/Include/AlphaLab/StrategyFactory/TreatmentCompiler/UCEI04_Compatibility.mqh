#ifndef __UCEI04_COMPATIBILITY_MQH__
#define __UCEI04_COMPATIBILITY_MQH__
#include "UCEI04_Contracts.mqh"
class CUCEI04Compatibility{
private:
 void Add(UCEI04_RuleFinding &out[],const string id,const bool passed,const bool fatal,const string code,const string message,const string evidence="{}"){int n=ArraySize(out);ArrayResize(out,n+1);out[n].rule_definition_id=id;out[n].passed=passed;out[n].fatal=fatal;out[n].code=code;out[n].message=message;out[n].evidence_json=evidence;}
public:
 bool Evaluate(const UCEI04_TreatmentDraft &d,const UCEI03_BuildContext &c,CUCEI03Catalog &catalog,UCEI04_RuleFinding &out[],string &error){ArrayResize(out,0);int counts[6]={0,0,0,0,0,0};for(int i=0;i<ArraySize(d.selections);i++){int k=(int)d.selections[i].role;if(k>=0&&k<6)counts[k]++;string id,ver;if(!SplitExactKey(d.selections[i].exact_key,id,ver)){error="invalid exact key";return false;}UCEI03_AtomDescriptor desc;if(!Resolve(catalog,d.selections[i].role,id,ver,desc)){error="exact atom version missing: "+d.selections[i].exact_key;return false;}bool side_ok=((desc.compatibility.side_mask&(d.side==UCEI03_LONG?1:2))!=0);Add(out,desc.definition_id,side_ok,true,side_ok?"side_compatible":"unsupported_side","side compatibility");bool mode_ok=((desc.compatibility.runtime_mode_mask&(1<<c.runtime_mode))!=0);Add(out,desc.definition_id,mode_ok,true,mode_ok?"mode_compatible":"unsupported_mode","runtime compatibility");if(!UCEI03_ValidatePacketAgainstDescriptor(desc,d.selections[i].parameters,error))return false;}
 for(int k=0;k<6;k++){bool ok=(k==(int)UCEI03_MANAGEMENT)?counts[k]<=8:counts[k]==1;Add(out,"ucerule_cardinality_"+IntegerToString((long)k),ok,true,ok?"cardinality_ok":"invalid_cardinality","canonical role cardinality");}
 for(int i=0;i<ArraySize(out);i++)if(!out[i].passed&&out[i].fatal){error=out[i].code;return false;}error="";return true;}
 bool SplitExactKey(const string key,string &id,string &version){int p=StringFind(key,"@",0);if(p<=0)return false;id=StringSubstr(key,0,p);version=StringSubstr(key,p+1);return id!=""&&version!="";}
 bool Resolve(CUCEI03Catalog &c,const ENUM_UCEI03_ATOM_KIND kind,const string id,const string version,UCEI03_AtomDescriptor &d){if(kind==UCEI03_ENTRY)return c.entry.Resolve(id,version,d);if(kind==UCEI03_STOP)return c.stop.Resolve(id,version,d);if(kind==UCEI03_TARGET)return c.target.Resolve(id,version,d);if(kind==UCEI03_TRAILING)return c.trailing.Resolve(id,version,d);if(kind==UCEI03_MANAGEMENT)return c.management.Resolve(id,version,d);if(kind==UCEI03_SIZING)return c.sizing.Resolve(id,version,d);return false;}
};
#endif
