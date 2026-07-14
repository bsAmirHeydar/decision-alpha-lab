#ifndef __FP_I11_OBJECT_MANAGER_MQH__
#define __FP_I11_OBJECT_MANAGER_MQH__
#include "FP_I11_ObjectIdentity.mqh"
class FP_I11_ObjectManager {
private:
 long m_chart_id; string m_namespace; string m_names[],m_hashes[],m_semantic_hashes[]; bool m_immutable[]; long m_seen_generation[]; long m_generation; int m_max_objects; SFP_I11_ProjectionStats m_stats;
 int Find(const string name){for(int i=0;i<ArraySize(m_names);i++)if(m_names[i]==name)return i;return -1;}
 bool EnsureObject(const SFP_I11_ObjectSpec &s){
  ENUM_OBJECT type=OBJ_TEXT;
  if(s.kind==FP_I11_SESSION_BOX||s.kind==FP_I11_WEEK_BOX||s.kind==FP_I11_WW_CONTEXT)type=OBJ_RECTANGLE;
  else if(s.kind==FP_I11_REFERENCE_LINE||s.kind==FP_I11_CANDIDATE_SIGNAL||s.kind==FP_I11_CONFIRMED_SIGNAL)type=OBJ_TREND;
  else if(s.kind==FP_I11_HEALTH_BADGE)type=OBJ_LABEL;
  else if(s.kind==FP_I11_HUNT_MARKER||s.kind==FP_I11_INVALIDATION_MARKER)type=OBJ_ARROW;
  if(ObjectFind(m_chart_id,s.object_id)<0){
   bool ok=false;
   if(type==OBJ_LABEL)ok=ObjectCreate(m_chart_id,s.object_id,type,0,0,0);
   else if(type==OBJ_TEXT||type==OBJ_ARROW)ok=ObjectCreate(m_chart_id,s.object_id,type,0,s.time1,s.price1);
   else ok=ObjectCreate(m_chart_id,s.object_id,type,0,s.time1,s.price1,s.time2,s.price2);
   if(!ok)return false;
  }
  if(type==OBJ_RECTANGLE||type==OBJ_TREND){ObjectMove(m_chart_id,s.object_id,0,s.time1,s.price1);ObjectMove(m_chart_id,s.object_id,1,s.time2,s.price2);}
  else if(type==OBJ_TEXT||type==OBJ_ARROW){ObjectMove(m_chart_id,s.object_id,0,s.time1,s.price1);}
  if(type==OBJ_LABEL){ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_CORNER,s.corner);ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_XDISTANCE,s.x);ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_YDISTANCE,s.y);}
  ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_COLOR,s.style.stroke);ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_WIDTH,s.style.width);ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_STYLE,s.style.line_style);ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_BACK,s.layer<=20);ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_ZORDER,s.style.z_order);ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_SELECTABLE,false);ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_HIDDEN,true);
  if(type==OBJ_RECTANGLE){ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_FILL,true);ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_COLOR,s.style.fill);}
  if(type==OBJ_TEXT||type==OBJ_LABEL){ObjectSetString(m_chart_id,s.object_id,OBJPROP_TEXT,s.text);ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_FONTSIZE,s.style.font_size);}
  if(type==OBJ_ARROW){ObjectSetInteger(m_chart_id,s.object_id,OBJPROP_ARROWCODE,159);}
  ObjectSetString(m_chart_id,s.object_id,OBJPROP_TOOLTIP,s.tooltip);return true;
 }
public:
 FP_I11_ObjectManager(){m_chart_id=0;m_namespace="";m_generation=0;m_max_objects=2500;ResetStats();}
 void ResetStats(){m_stats.frame_sequence=m_generation;m_stats.created=0;m_stats.updated=0;m_stats.deleted=0;m_stats.unchanged=0;m_stats.retained_immutable=0;m_stats.total_objects=ArraySize(m_names);m_stats.degraded=false;m_stats.reason_code="FP_VIS_READY";}
 bool Initialize(long chart_id,string object_namespace,int max_objects){m_chart_id=chart_id;m_namespace=object_namespace;m_max_objects=max_objects;return StringFind(m_namespace,"FP19::")==0;}
 void BeginFrame(){m_generation++;ResetStats();m_stats.frame_sequence=m_generation;}
 bool Upsert(SFP_I11_ObjectSpec &s){
  if(ArraySize(m_names)>=m_max_objects && Find(s.object_id)<0){m_stats.degraded=true;m_stats.reason_code="FP_VIS_OBJECT_BUDGET_DEGRADED";return false;}
  int idx=Find(s.object_id);string ph=FP_I11_ProjectionHash(s);s.projection_hash=ph;
  if(idx>=0 && m_hashes[idx]==ph){m_seen_generation[idx]=m_generation;m_stats.unchanged++;return true;}
  if(idx>=0 && m_immutable[idx] && m_semantic_hashes[idx]!=s.semantic_hash){m_seen_generation[idx]=m_generation;m_stats.retained_immutable++;m_stats.degraded=true;m_stats.reason_code="FP_VIS_IMMUTABLE_OBJECT_CHANGED";return false;}
  if(!EnsureObject(s)){m_stats.degraded=true;m_stats.reason_code="FP_VIS_OBJECT_CREATE_FAILED";return false;}
  if(idx<0){idx=ArraySize(m_names);ArrayResize(m_names,idx+1);ArrayResize(m_hashes,idx+1);ArrayResize(m_semantic_hashes,idx+1);ArrayResize(m_immutable,idx+1);ArrayResize(m_seen_generation,idx+1);m_names[idx]=s.object_id;m_stats.created++;}else m_stats.updated++;
  m_hashes[idx]=ph;m_semantic_hashes[idx]=s.semantic_hash;m_immutable[idx]=s.immutable;m_seen_generation[idx]=m_generation;return true;
 }
 void EndFrame(){
  for(int i=ArraySize(m_names)-1;i>=0;i--){if(m_seen_generation[i]==m_generation)continue;if(m_immutable[i]){m_stats.retained_immutable++;continue;}ObjectDelete(m_chart_id,m_names[i]);for(int j=i;j<ArraySize(m_names)-1;j++){m_names[j]=m_names[j+1];m_hashes[j]=m_hashes[j+1];m_semantic_hashes[j]=m_semantic_hashes[j+1];m_immutable[j]=m_immutable[j+1];m_seen_generation[j]=m_seen_generation[j+1];}int n=ArraySize(m_names)-1;ArrayResize(m_names,n);ArrayResize(m_hashes,n);ArrayResize(m_semantic_hashes,n);ArrayResize(m_immutable,n);ArrayResize(m_seen_generation,n);m_stats.deleted++;}
  m_stats.total_objects=ArraySize(m_names);ChartRedraw(m_chart_id);
 }
 void CleanupOwnNamespace(bool include_immutable=false){for(int i=ArraySize(m_names)-1;i>=0;i--){if(include_immutable||!m_immutable[i])ObjectDelete(m_chart_id,m_names[i]);}if(include_immutable){ArrayResize(m_names,0);ArrayResize(m_hashes,0);ArrayResize(m_semantic_hashes,0);ArrayResize(m_immutable,0);ArrayResize(m_seen_generation,0);}ChartRedraw(m_chart_id);}
 SFP_I11_ProjectionStats Stats()const{return m_stats;} int Count()const{return ArraySize(m_names);}
};
#endif
