#ifndef __LCM11B_CHART_OBJECT_VISUALIZER_MQH__
#define __LCM11B_CHART_OBJECT_VISUALIZER_MQH__
#include "LCM11BVisualEvent.mqh"
#include "LCM11BStyle.mqh"
#include "LCM11BObjectRegistry.mqh"
class CLCM11BChartObjectVisualizer
  {
private:
   string m_owner,m_subsystem,m_instance;
public:
   void Configure(const string owner,const string subsystem,const string instance_id){m_owner=owner;m_subsystem=subsystem;m_instance=instance_id;}
   string Name(const LCM11BVisualEvent &event,const string role,const string visual_token)const{return LCM11BObjectId(m_owner,m_subsystem,m_instance,event.chart_id,event.symbol,event.timeframe,event.event_id,role,visual_token);}
   bool EnsureTrend(const LCM11BVisualEvent &event,const string visual_token,const LCM11BStyle &style)
     {
      string name=Name(event,"OBJ_TREND",visual_token);
      if(ObjectFind(event.chart_id,name)<0 && !ObjectCreate(event.chart_id,name,OBJ_TREND,0,event.time1,event.price1,event.time2,event.price2))return false;
      ObjectMove(event.chart_id,name,0,event.time1,event.price1);ObjectMove(event.chart_id,name,1,event.time2,event.price2);
      ObjectSetInteger(event.chart_id,name,OBJPROP_COLOR,style.line_color);ObjectSetInteger(event.chart_id,name,OBJPROP_WIDTH,style.width);ObjectSetInteger(event.chart_id,name,OBJPROP_STYLE,style.line_style);ObjectSetInteger(event.chart_id,name,OBJPROP_SELECTABLE,style.selectable);ObjectSetInteger(event.chart_id,name,OBJPROP_HIDDEN,style.hidden);return true;
     }
   bool EnsureVLine(const LCM11BVisualEvent &event,const string visual_token,const LCM11BStyle &style)
     {
      string name=Name(event,"OBJ_VLINE",visual_token);
      if(ObjectFind(event.chart_id,name)<0 && !ObjectCreate(event.chart_id,name,OBJ_VLINE,0,event.time1,0.0))return false;
      ObjectMove(event.chart_id,name,0,event.time1,0.0);ObjectSetInteger(event.chart_id,name,OBJPROP_COLOR,style.line_color);ObjectSetInteger(event.chart_id,name,OBJPROP_HIDDEN,style.hidden);return true;
     }
   bool EnsureText(const LCM11BVisualEvent &event,const string visual_token,const LCM11BStyle &style)
     {
      string name=Name(event,"OBJ_TEXT",visual_token);
      if(ObjectFind(event.chart_id,name)<0 && !ObjectCreate(event.chart_id,name,OBJ_TEXT,0,event.time1,event.price1))return false;
      ObjectMove(event.chart_id,name,0,event.time1,event.price1);ObjectSetString(event.chart_id,name,OBJPROP_TEXT,event.label);ObjectSetInteger(event.chart_id,name,OBJPROP_COLOR,style.line_color);ObjectSetInteger(event.chart_id,name,OBJPROP_FONTSIZE,style.font_size);ObjectSetInteger(event.chart_id,name,OBJPROP_HIDDEN,style.hidden);return true;
     }
   int Cleanup(const long chart_id)const{return LCM11BDeleteOwned(chart_id,LCM11BCleanupPrefix(m_owner,m_subsystem,m_instance,chart_id));}
  };
#endif
