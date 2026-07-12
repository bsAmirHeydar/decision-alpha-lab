#ifndef __UCEI03_PARAMETER_PACKET_MQH__
#define __UCEI03_PARAMETER_PACKET_MQH__
#include "UCEI03_Contracts.mqh"
void UCEI03_ClearPacket(UCEI03_ParameterPacket &p){p.schema_definition_id="";ArrayResize(p.values,0);p.packet_id="";p.evidence_hash="";}
bool UCEI03_SetParameter(UCEI03_ParameterPacket &p,const string name,const string value,string &error){if(!UCE03_IsSafeIdentifier(name)){error="unsafe parameter name";return false;}for(int i=0;i<ArraySize(p.values);i++)if(p.values[i].name==name){p.values[i].value=value;error="";return true;}int n=ArraySize(p.values);ArrayResize(p.values,n+1);p.values[n].name=name;p.values[n].value=value;error="";return true;}
bool UCEI03_GetParameter(const UCEI03_ParameterPacket &p,const string name,string &value){for(int i=0;i<ArraySize(p.values);i++)if(p.values[i].name==name){value=p.values[i].value;return true;}return false;}
double UCEI03_GetDouble(const UCEI03_ParameterPacket &p,const string name,const double fallback){string v;if(!UCEI03_GetParameter(p,name,v))return fallback;return StringToDouble(v);}
long UCEI03_GetLong(const UCEI03_ParameterPacket &p,const string name,const long fallback){string v;if(!UCEI03_GetParameter(p,name,v))return fallback;return (long)StringToInteger(v);}
string UCEI03_PacketMaterial(const UCEI03_ParameterPacket &p){string material=p.schema_definition_id;for(int i=0;i<ArraySize(p.values);i++)material+="|"+p.values[i].name+"="+p.values[i].value;return material;}
void UCEI03_SealPacket(UCEI03_ParameterPacket &p){string material=UCEI03_PacketMaterial(p);p.packet_id="ucepp_"+UCE03_Fnv1a64HexUtf8(material);p.evidence_hash="fnv1a64:"+UCE03_Fnv1a64HexUtf8(material);}
bool UCEI03_BindDefaults(const UCEI03_AtomDescriptor &d,UCEI03_ParameterPacket &p,string &error){UCEI03_ClearPacket(p);p.schema_definition_id=d.definition_id+".params";for(int i=0;i<ArraySize(d.parameters);i++)if(!UCEI03_SetParameter(p,d.parameters[i].name,d.parameters[i].default_value,error))return false;UCEI03_SealPacket(p);error="";return true;}

bool UCEI03_ValidateParameterValue(const UCEI03_ParameterSpec &spec,const string value,string &error){
   if(spec.type==UCEI03_PARAM_DECIMAL||spec.type==UCEI03_PARAM_INTEGER){
      double x=StringToDouble(value);
      if(spec.minimum_value!=""&&x<StringToDouble(spec.minimum_value)){error="parameter below minimum: "+spec.name;return false;}
      if(spec.maximum_value!=""&&x>StringToDouble(spec.maximum_value)){error="parameter above maximum: "+spec.name;return false;}
      if(spec.type==UCEI03_PARAM_INTEGER&&MathAbs(x-MathRound(x))>1e-9){error="integer parameter required: "+spec.name;return false;}
   }
   if(spec.type==UCEI03_PARAM_BOOLEAN&&value!="true"&&value!="false"){error="boolean parameter required: "+spec.name;return false;}
   if(spec.type==UCEI03_PARAM_ENUM&&spec.allowed_values_csv!=""){
      string values[];StringSplit(spec.allowed_values_csv,',',values);bool found=false;for(int i=0;i<ArraySize(values);i++)if(values[i]==value){found=true;break;}
      if(!found){error="enum parameter not allowed: "+spec.name;return false;}
   }
   error="";return true;
}
bool UCEI03_ValidatePacketAgainstDescriptor(const UCEI03_AtomDescriptor &d,const UCEI03_ParameterPacket &p,string &error){
   for(int i=0;i<ArraySize(d.parameters);i++){string v;if(!UCEI03_GetParameter(p,d.parameters[i].name,v)){error="missing parameter: "+d.parameters[i].name;return false;}if(!UCEI03_ValidateParameterValue(d.parameters[i],v,error))return false;}
   for(int i=0;i<ArraySize(p.values);i++){bool known=false;for(int j=0;j<ArraySize(d.parameters);j++)if(p.values[i].name==d.parameters[j].name){known=true;break;}if(!known){error="unknown parameter: "+p.values[i].name;return false;}}
   error="";return true;
}
void UCEI03_SealInvocation(UCEI03_Invocation &i){
   string material=i.descriptor_definition_id+"|"+i.exact_key+"|"+i.context_occurrence_id+"|"+i.feature_frame_hash+"|"+UCEI03_SideName(i.side)+"|"+IntegerToString(i.decision_time_ms)+"|"+i.parameters.packet_id+"|"+i.provenance_json;
   i.invocation_id="ucei_"+UCE03_Fnv1a64HexUtf8(material);i.evidence_hash="fnv1a64:"+UCE03_Fnv1a64HexUtf8(material);
}

#endif
