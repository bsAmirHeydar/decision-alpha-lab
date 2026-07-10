#ifndef __EXP0018_DAYE_VISUAL_IDENTITY_MQH__
#define __EXP0018_DAYE_VISUAL_IDENTITY_MQH__

#include <DayeTrader/EXP0018/DAYE_VisualTypes.mqh>

uint DAYE_VisualHash32(const string value)
{
   uint hash=2166136261;
   for(int i=0;i<StringLen(value);i++)
   {
      hash^=(uint)StringGetCharacter(value,i);
      hash*=16777619;
   }
   return hash;
}

string DAYE_VisualHashText(const string value)
{
   return StringFormat("%08X",DAYE_VisualHash32(value));
}

string DAYE_VisualObjectName(const string kind,const string logical_id)
{
   return DAYE_VISUAL_OBJECT_PREFIX+kind+"_"+DAYE_VisualHashText(logical_id);
}

bool DAYE_IsOwnedVisualObject(const string name)
{
   return StringFind(name,DAYE_VISUAL_OBJECT_PREFIX)==0;
}

string DAYE_VisualLogicalId(const string kind,const string source_id,const long chart_id,const string suffix="")
{
   return "EXP0018|P10|"+kind+"|"+source_id+"|CHART|"+IntegerToString(chart_id)+"|"+suffix;
}

string DAYE_ParentSessionCode(const string subcycle_code)
{
   if(StringLen(subcycle_code)<1) return "";
   string first=StringSubstr(subcycle_code,0,1);
   StringToUpper(first);
   return first;
}

string DAYE_QuarterNumberFromCode(const string code)
{
   if(code=="A") return "Q1";
   if(code=="L") return "Q2";
   if(code=="N") return "Q3";
   if(code=="P") return "Q4";
   if(StringLen(code)>=2) return "Q"+StringSubstr(code,1,1);
   return "";
}

string DAYE_PhaseLabel(const string code)
{
   string q=DAYE_QuarterNumberFromCode(code);
   if(q=="") return code;
   if(code=="p4") return q+" "+code+" 30m";
   return q+" "+code;
}

color DAYE_SessionVisualColor(const string code,const DAYE_VisualConfig &config)
{
   if(code=="A") return config.session_a_color;
   if(code=="L") return config.session_l_color;
   if(code=="N") return config.session_n_color;
   if(code=="P") return config.session_p_color;
   return config.subcycle_color;
}

bool DAYE_VisualPeriodCompletenessAllowed(const DAYE_SymbolPeriodSnapshot &snapshot,const DAYE_VisualConfig &config)
{
   if(snapshot.completeness==DAYE_PERIOD_COMPLETENESS_COMPLETE) return config.render_complete_periods;
   if(snapshot.completeness==DAYE_PERIOD_COMPLETENESS_OPEN) return config.render_open_periods;
   if(snapshot.completeness==DAYE_PERIOD_COMPLETENESS_PARTIAL) return config.render_partial_periods;
   return false;
}

#endif
