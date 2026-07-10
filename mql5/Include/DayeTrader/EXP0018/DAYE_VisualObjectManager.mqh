#ifndef __EXP0018_DAYE_VISUAL_OBJECT_MANAGER_MQH__
#define __EXP0018_DAYE_VISUAL_OBJECT_MANAGER_MQH__

#include <DayeTrader/EXP0018/DAYE_VisualIdentity.mqh>

long DAYE_VisualArgb(const color base_color,const int alpha)
{
   int bounded=alpha;
   if(bounded<0) bounded=0;
   if(bounded>255) bounded=255;
   return (long)ColorToARGB(base_color,(uchar)bounded);
}

bool DAYE_VisualSetCommon(const long chart_id,const string name,const bool back,
                          const bool selectable,const bool hidden,const string tooltip)
{
   bool ok=true;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_BACK,back)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_SELECTABLE,selectable)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_SELECTED,false)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_HIDDEN,hidden)&&ok;
   ok=ObjectSetString(chart_id,name,OBJPROP_TOOLTIP,tooltip)&&ok;
   return ok;
}

bool DAYE_VisualUpsertRectangle(const long chart_id,const string name,
                                const datetime t1,const datetime t2,
                                const double high_price,const double low_price,
                                const color base_color,const int fill_alpha,
                                const ENUM_LINE_STYLE style,const int width,
                                const bool fill,const DAYE_VisualConfig &config,
                                const string tooltip,bool &created)
{
   created=false;
   if(t1<=0 || t2<=t1 || high_price<=0.0 || low_price<=0.0 || high_price<low_price) return false;
   if(ObjectFind(chart_id,name)<0)
   {
      ResetLastError();
      if(!ObjectCreate(chart_id,name,OBJ_RECTANGLE,0,t1,high_price,t2,low_price)) return false;
      created=true;
   }
   bool ok=true;
   ok=ObjectMove(chart_id,name,0,t1,high_price)&&ok;
   ok=ObjectMove(chart_id,name,1,t2,low_price)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_COLOR,fill?DAYE_VisualArgb(base_color,fill_alpha):(long)base_color)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_STYLE,style)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_WIDTH,width)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_FILL,fill)&&ok;
   ok=DAYE_VisualSetCommon(chart_id,name,config.draw_boxes_in_background,config.objects_selectable,config.objects_hidden,tooltip)&&ok;
   return ok;
}

bool DAYE_VisualUpsertVLine(const long chart_id,const string name,const datetime time_value,
                            const color line_color,const ENUM_LINE_STYLE style,const int width,
                            const DAYE_VisualConfig &config,const string tooltip,bool &created)
{
   created=false;
   if(time_value<=0) return false;
   if(ObjectFind(chart_id,name)<0)
   {
      ResetLastError();
      if(!ObjectCreate(chart_id,name,OBJ_VLINE,0,time_value,0.0)) return false;
      created=true;
   }
   bool ok=true;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_TIME,0,time_value)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_COLOR,line_color)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_STYLE,style)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_WIDTH,width)&&ok;
   ok=DAYE_VisualSetCommon(chart_id,name,true,config.objects_selectable,config.objects_hidden,tooltip)&&ok;
   return ok;
}

bool DAYE_VisualUpsertHorizontalSegment(const long chart_id,const string name,
                                        const datetime t1,const datetime t2,const double price,
                                        const color line_color,const ENUM_LINE_STYLE style,const int width,
                                        const DAYE_VisualConfig &config,const string tooltip,bool &created)
{
   created=false;
   if(t1<=0 || t2<=t1 || price<=0.0) return false;
   if(ObjectFind(chart_id,name)<0)
   {
      ResetLastError();
      if(!ObjectCreate(chart_id,name,OBJ_TREND,0,t1,price,t2,price)) return false;
      created=true;
   }
   bool ok=true;
   ok=ObjectMove(chart_id,name,0,t1,price)&&ok;
   ok=ObjectMove(chart_id,name,1,t2,price)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_COLOR,line_color)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_STYLE,style)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_WIDTH,width)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_RAY_LEFT,false)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_RAY_RIGHT,false)&&ok;
   ok=DAYE_VisualSetCommon(chart_id,name,false,config.objects_selectable,config.objects_hidden,tooltip)&&ok;
   return ok;
}

bool DAYE_VisualUpsertText(const long chart_id,const string name,const datetime time_value,
                           const double price,const string text,const color text_color,
                           const int font_size,const DAYE_VisualConfig &config,
                           const string tooltip,bool &created)
{
   created=false;
   if(time_value<=0 || price<=0.0 || text=="") return false;
   if(ObjectFind(chart_id,name)<0)
   {
      ResetLastError();
      if(!ObjectCreate(chart_id,name,OBJ_TEXT,0,time_value,price)) return false;
      created=true;
   }
   bool ok=true;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_TIME,0,time_value)&&ok;
   ok=ObjectSetDouble(chart_id,name,OBJPROP_PRICE,0,price)&&ok;
   ok=ObjectSetString(chart_id,name,OBJPROP_TEXT,text)&&ok;
   ok=ObjectSetString(chart_id,name,OBJPROP_FONT,config.label_font)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_FONTSIZE,font_size)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_COLOR,text_color)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_ANCHOR,ANCHOR_CENTER)&&ok;
   ok=DAYE_VisualSetCommon(chart_id,name,false,config.objects_selectable,config.objects_hidden,tooltip)&&ok;
   return ok;
}

bool DAYE_VisualUpsertLegend(const long chart_id,const string name,const string text,
                             const DAYE_VisualConfig &config,bool &created)
{
   created=false;
   if(ObjectFind(chart_id,name)<0)
   {
      ResetLastError();
      if(!ObjectCreate(chart_id,name,OBJ_LABEL,0,0,0)) return false;
      created=true;
   }
   bool ok=true;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_CORNER,CORNER_LEFT_UPPER)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_XDISTANCE,12)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_YDISTANCE,18)&&ok;
   ok=ObjectSetString(chart_id,name,OBJPROP_TEXT,text)&&ok;
   ok=ObjectSetString(chart_id,name,OBJPROP_FONT,config.label_font)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_FONTSIZE,config.minor_label_font_size)&&ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_COLOR,config.label_color)&&ok;
   ok=DAYE_VisualSetCommon(chart_id,name,false,false,config.objects_hidden,"EXP0018 P10 visual legend")&&ok;
   return ok;
}

int DAYE_DeleteOwnedVisualObjectsFromChart(const long chart_id)
{
   int deleted=0;
   for(int i=ObjectsTotal(chart_id,-1,-1)-1;i>=0;i--)
   {
      string name=ObjectName(chart_id,i,-1,-1);
      if(DAYE_IsOwnedVisualObject(name) && ObjectDelete(chart_id,name)) deleted++;
   }
   if(deleted>0) ChartRedraw(chart_id);
   return deleted;
}

int DAYE_DeleteOwnedVisualObjectsFromAllCharts(void)
{
   int deleted=0;
   long chart=ChartFirst();
   while(chart>=0)
   {
      deleted+=DAYE_DeleteOwnedVisualObjectsFromChart(chart);
      chart=ChartNext(chart);
   }
   return deleted;
}

#endif
