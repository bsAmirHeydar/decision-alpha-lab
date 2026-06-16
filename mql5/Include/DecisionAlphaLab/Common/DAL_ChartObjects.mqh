#ifndef __DAL_CHART_OBJECTS_MQH__
#define __DAL_CHART_OBJECTS_MQH__

#include <DecisionAlphaLab/Common/DAL_Common.mqh>

void DAL_DeleteByPrefix(const string prefix)
{
   for(int i = ObjectsTotal(0, -1, -1) - 1; i >= 0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

void DAL_DrawTextLabel(
   const string name,
   const datetime t,
   const double price,
   const string text,
   const color c,
   const int font_size = 8
)
{
   ObjectCreate(0, name, OBJ_TEXT, 0, t, price);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
}

void DAL_DrawTrend(
   const string name,
   const datetime t1,
   const double p1,
   const datetime t2,
   const double p2,
   const color c,
   const int width = 1,
   const ENUM_LINE_STYLE style = STYLE_SOLID
)
{
   ObjectCreate(0, name, OBJ_TREND, 0, t1, p1, t2, p2);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, false);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
}

void DAL_DrawHLine(
   const string name,
   const double price,
   const color c,
   const ENUM_LINE_STYLE style = STYLE_DOT
)
{
   ObjectCreate(0, name, OBJ_HLINE, 0, 0, price);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
}

void DAL_DrawVLine(
   const string name,
   const datetime t,
   const color c,
   const ENUM_LINE_STYLE style = STYLE_DOT
)
{
   ObjectCreate(0, name, OBJ_VLINE, 0, t, 0);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
}

void DAL_DrawRectangle(
   const string name,
   const datetime t1,
   const double upper,
   const datetime t2,
   const double lower,
   const color c,
   const bool back = true,
   const bool fill = false
)
{
   ObjectCreate(0, name, OBJ_RECTANGLE, 0, t1, upper, t2, lower);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_BACK, back);
   ObjectSetInteger(0, name, OBJPROP_FILL, fill);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
}

#endif
