#ifndef __FP_I11_RESPONSIVE_LAYOUT_MQH__
#define __FP_I11_RESPONSIVE_LAYOUT_MQH__
class FP_I11_ResponsiveLayout {
public:
 static double PricePerPixel(const long chart_id){double hi=ChartGetDouble(chart_id,CHART_PRICE_MAX,0),lo=ChartGetDouble(chart_id,CHART_PRICE_MIN,0);long h=ChartGetInteger(chart_id,CHART_HEIGHT_IN_PIXELS,0);if(h<=0||hi<=lo)return 0.0;return (hi-lo)/(double)h;}
 static double LaneStep(const long chart_id,const string symbol){double tick=SymbolInfoDouble(symbol,SYMBOL_TRADE_TICK_SIZE);if(tick<=0)tick=SymbolInfoDouble(symbol,SYMBOL_POINT);double raw=MathMax(tick,PricePerPixel(chart_id)*12.0);return MathCeil(raw/tick)*tick;}
 static double LanePrice(const long chart_id,const string symbol,const double base,const int slot,const bool above){double step=LaneStep(chart_id,symbol);return above?base+step*slot:base-step*slot;}
 static int StableLane(const string semantic_id,const int lane_count){if(lane_count<=1)return 0;uint h=0;for(int i=0;i<StringLen(semantic_id);i++)h=h*33+(uint)StringGetCharacter(semantic_id,i);return (int)(h%(uint)lane_count);}
};
#endif
