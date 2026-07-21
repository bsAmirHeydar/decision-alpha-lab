#ifndef __LCM11B_STYLE_MQH__
#define __LCM11B_STYLE_MQH__
struct LCM11BStyle
  {
   color line_color;
   int width;
   ENUM_LINE_STYLE line_style;
   int font_size;
   bool selectable;
   bool hidden;
  };
void LCM11BDefaultStyle(LCM11BStyle &style)
  {
   style.line_color=clrDodgerBlue;style.width=1;style.line_style=STYLE_SOLID;
   style.font_size=9;style.selectable=false;style.hidden=true;
  }
#endif
