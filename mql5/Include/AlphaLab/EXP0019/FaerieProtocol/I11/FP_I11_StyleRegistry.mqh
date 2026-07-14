#ifndef __FP_I11_STYLE_REGISTRY_MQH__
#define __FP_I11_STYLE_REGISTRY_MQH__
#include "FP_I11_Contracts.mqh"
SFP_I11_Style FP_I11_MakeStyle(string id,color stroke,color fill,int width,int ls,int opacity,int font_size,int z){SFP_I11_Style s;s.style_id=id;s.stroke=stroke;s.fill=fill;s.width=width;s.line_style=ls;s.opacity=opacity;s.font_size=font_size;s.z_order=z;return s;}
class FP_I11_StyleRegistry {
public:
 static SFP_I11_Style Session(string kind){if(kind=="A")return FP_I11_MakeStyle("SESSION_A",C'138,92,246',C'138,92,246',1,STYLE_SOLID,28,8,20);if(kind=="L")return FP_I11_MakeStyle("SESSION_L",C'0,168,232',C'0,168,232',1,STYLE_SOLID,24,8,20);if(kind=="N")return FP_I11_MakeStyle("SESSION_N",C'245,158,11',C'245,158,11',1,STYLE_SOLID,22,8,20);return FP_I11_MakeStyle("WEEK",C'107,114,128',C'107,114,128',1,STYLE_DASH,12,8,10);}
 static SFP_I11_Style Reference(string side){return side=="HIGH"?FP_I11_MakeStyle("REF_HIGH",C'239,68,68',clrNONE,1,STYLE_DASH,220,8,30):FP_I11_MakeStyle("REF_LOW",C'34,197,94',clrNONE,1,STYLE_DASH,220,8,30);}
 static SFP_I11_Style Hunt(){return FP_I11_MakeStyle("HUNT",C'249,115,22',clrNONE,2,STYLE_SOLID,255,9,40);}
 static SFP_I11_Style Signal(string direction,string state,ENUM_FP_I11_SIGNAL_DISPOSITION d){if(d==FP_I11_QUOTA_WINNER)return FP_I11_MakeStyle("WINNER",C'250,204,21',clrNONE,3,STYLE_SOLID,255,11,70);if(d==FP_I11_SUPPRESSED_BY_WW)return FP_I11_MakeStyle("SUPPRESSED_WW",C'168,85,247',clrNONE,1,STYLE_DOT,180,9,60);if(d==FP_I11_SUPPRESSED_BY_QUOTA)return FP_I11_MakeStyle("SUPPRESSED_QUOTA",C'100,116,139',clrNONE,1,STYLE_DOT,160,9,60);if(state=="INVALIDATED")return FP_I11_MakeStyle("INVALID",C'156,163,175',clrNONE,1,STYLE_DOT,190,8,50);if(state=="CONFIRMED")return direction=="BULLISH"?FP_I11_MakeStyle("CONFIRMED_BULL",C'34,197,94',clrNONE,2,STYLE_SOLID,255,10,50):FP_I11_MakeStyle("CONFIRMED_BEAR",C'239,68,68',clrNONE,2,STYLE_SOLID,255,10,50);return FP_I11_MakeStyle("CANDIDATE",C'251,191,36',clrNONE,1,STYLE_DOT,210,9,50);}
 static SFP_I11_Style WW(string direction){return direction=="BULLISH"?FP_I11_MakeStyle("WW_BULL",C'22,163,74',C'22,163,74',2,STYLE_SOLID,25,10,15):FP_I11_MakeStyle("WW_BEAR",C'220,38,38',C'220,38,38',2,STYLE_SOLID,25,10,15);}
 static SFP_I11_Style Health(int state){if(state==0)return FP_I11_MakeStyle("HEALTH_READY",C'22,163,74',C'15,23,42',1,STYLE_SOLID,230,9,80);if(state==1)return FP_I11_MakeStyle("HEALTH_DEGRADED",C'245,158,11',C'15,23,42',1,STYLE_SOLID,230,9,80);return FP_I11_MakeStyle("HEALTH_BLOCKED",C'220,38,38',C'15,23,42',1,STYLE_SOLID,230,9,80);}
};
#endif
