#ifndef __CGX_EXECUTION_VISUALS_MQH__
#define __CGX_EXECUTION_VISUALS_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_Utilities.mqh>

#define CGX_EXECUTION_OBJECT_PREFIX "EXP0017_P14_"

class CCGX_ExecutionVisuals
{
private:
   SCGXExecutionConfig m_config;

   string Sanitize(const string raw)
   {
      string value=raw;
      StringReplace(value,":","_");
      StringReplace(value,".","_");
      StringReplace(value," ","_");
      StringReplace(value,"-","_");
      StringReplace(value,"|","_");
      StringReplace(value,"/","_");
      return value;
   }

   string Key(const string signal_id,const string symbol,const string suffix)
   {
      return CGX_EXECUTION_OBJECT_PREFIX+CGX_ShortSignalHash(signal_id)+"_"+Sanitize(symbol)+"_"+suffix;
   }

   long FindChartForSymbol(const string symbol)
   {
      long chart_id=ChartFirst();
      while(chart_id>=0)
      {
         if(ChartSymbol(chart_id)==symbol)
            return chart_id;
         chart_id=ChartNext(chart_id);
      }

      if(m_config.open_missing_visual_charts && symbol!="")
      {
         SymbolSelect(symbol,true);
         return ChartOpen(symbol,(ENUM_TIMEFRAMES)_Period);
      }
      return -1;
   }

   datetime NyToBroker(SCGCFinalSignal &signal,const datetime ny_time)
   {
      if(ny_time<=0 || signal.confirmation_time_broker<=0 || signal.confirmation_time_ny<=0)
         return signal.confirmation_time_broker;
      int offset=(int)(signal.confirmation_time_broker-signal.confirmation_time_ny);
      return (datetime)(ny_time+offset);
   }

   double SymbolReferencePrice(SCGCFinalSignal &signal,const string symbol)
   {
      if(symbol==m_config.symbol_a) return signal.symbol_a_reference_price;
      if(symbol==m_config.symbol_b) return signal.symbol_b_reference_price;
      if(symbol==signal.hunter_symbol) return signal.hunter_reference_price;
      if(symbol==signal.clean_symbol) return signal.clean_reference_price;
      return 0.0;
   }

   double SymbolCurrentExtreme(SCGCFinalSignal &signal,const string symbol)
   {
      if(symbol==m_config.symbol_a) return signal.symbol_a_current_extreme;
      if(symbol==m_config.symbol_b) return signal.symbol_b_current_extreme;
      if(symbol==signal.hunter_symbol) return signal.hunter_current_extreme;
      if(symbol==signal.clean_symbol) return signal.clean_current_extreme;
      return 0.0;
   }

   color SignalColor(const ECGCSignalDirection direction)
   {
      if(direction==CGC_DIRECTION_BUY) return clrLimeGreen;
      if(direction==CGC_DIRECTION_SELL) return clrTomato;
      return clrSilver;
   }

   void ApplyCommon(const long chart_id,const string name,const string tooltip)
   {
      ObjectSetInteger(chart_id,name,OBJPROP_SELECTABLE,true);
      ObjectSetInteger(chart_id,name,OBJPROP_SELECTED,false);
      ObjectSetInteger(chart_id,name,OBJPROP_BACK,false);
      ObjectSetInteger(chart_id,name,OBJPROP_HIDDEN,false);
      ObjectSetInteger(chart_id,name,OBJPROP_TIMEFRAMES,OBJ_ALL_PERIODS);
      ObjectSetString(chart_id,name,OBJPROP_TOOLTIP,tooltip);
   }

   bool DrawTrend(const long chart_id,
                  const string name,
                  datetime t1,
                  const double p1,
                  datetime t2,
                  const double p2,
                  const color line_color,
                  const int width,
                  const ENUM_LINE_STYLE style,
                  const string tooltip)
   {
      if(chart_id<0 || p1<=0.0 || p2<=0.0)
         return false;
      if(t1<=0) t1=TimeCurrent();
      if(t2<=t1)
      {
         int span=PeriodSeconds((ENUM_TIMEFRAMES)_Period);
         if(span<=0) span=60;
         t2=(datetime)(t1+span);
      }

      if(ObjectFind(chart_id,name)>=0)
         return true;
      if(!ObjectCreate(chart_id,name,OBJ_TREND,0,t1,p1,t2,p2))
         return false;
      ObjectSetInteger(chart_id,name,OBJPROP_RAY_RIGHT,false);
      ObjectSetInteger(chart_id,name,OBJPROP_COLOR,line_color);
      ObjectSetInteger(chart_id,name,OBJPROP_WIDTH,MathMax(1,width));
      ObjectSetInteger(chart_id,name,OBJPROP_STYLE,style);
      ApplyCommon(chart_id,name,tooltip);
      return true;
   }

   bool DrawDivergenceLeg(SCGCFinalSignal &signal,const string symbol)
   {
      long chart_id=FindChartForSymbol(symbol);
      if(chart_id<0)
         return false;

      double reference_price=SymbolReferencePrice(signal,symbol);
      double current_extreme=SymbolCurrentExtreme(signal,symbol);
      if(reference_price<=0.0 || current_extreme<=0.0)
         return false;

      datetime origin_time=NyToBroker(signal,signal.reference_cycle_end_ny);
      datetime destination_time=signal.confirmation_time_broker;
      color line_color=SignalColor(signal.direction);
      if(symbol==signal.clean_symbol)
         line_color=clrDeepSkyBlue;

      string tooltip=StringFormat("EXP0017 Phase14 executed signal | %s | %s | %s | hunter=%s | protected=%s",
                                  signal.group_name,
                                  CGX_DirectionText(signal.direction),
                                  symbol,
                                  signal.hunter_symbol,
                                  signal.clean_symbol);
      bool drawn=DrawTrend(chart_id,
                           Key(signal.signal_id,symbol,"divergence"),
                           origin_time,
                           reference_price,
                           destination_time,
                           current_extreme,
                           line_color,
                           3,
                           STYLE_SOLID,
                           tooltip);
      if(drawn)
         ChartRedraw(chart_id);
      return drawn;
   }

   void DrawTradeLevels(SCGXTradePlan &plan)
   {
      if(!m_config.draw_execution_levels)
         return;
      long chart_id=FindChartForSymbol(plan.trade_symbol);
      if(chart_id<0)
         return;

      int seconds=PeriodSeconds(plan.confirmation_timeframe);
      if(seconds<=0) seconds=60;
      datetime t1=plan.confirmation_time_broker;
      datetime t2=(datetime)(t1+seconds*6);
      string tooltip=StringFormat("EXP0017 Phase14 trade levels | %s | risk_budget=%.2f | planned_loss=%.2f | volume=%.4f",
                                  plan.group_name,
                                  plan.risk_budget_money,
                                  plan.planned_loss_at_stop,
                                  plan.volume);

      DrawTrend(chart_id,Key(plan.signal_id,plan.trade_symbol,"entry"),t1,plan.planned_entry_price,t2,plan.planned_entry_price,clrGold,2,STYLE_DOT,tooltip+" | ENTRY");
      DrawTrend(chart_id,Key(plan.signal_id,plan.trade_symbol,"stop"),t1,plan.stop_loss,t2,plan.stop_loss,clrRed,2,STYLE_DASH,tooltip+" | STOP");
      DrawTrend(chart_id,Key(plan.signal_id,plan.trade_symbol,"target"),t1,plan.take_profit,t2,plan.take_profit,clrLime,2,STYLE_DASH,tooltip+" | TARGET");
      ChartRedraw(chart_id);
   }

   int ClearOnChart(const long chart_id)
   {
      if(chart_id<0)
         return 0;
      int removed=0;
      for(int i=ObjectsTotal(chart_id,0,-1)-1;i>=0;i--)
      {
         string name=ObjectName(chart_id,i,0,-1);
         if(StringFind(name,CGX_EXECUTION_OBJECT_PREFIX)==0 && ObjectDelete(chart_id,name))
            removed++;
      }
      ChartRedraw(chart_id);
      return removed;
   }

public:
   void Configure(const SCGXExecutionConfig &config)
   {
      m_config=config;
      if(m_config.clear_execution_objects_on_init)
         ClearOwnedObjects();
   }

   int ClearOwnedObjects()
   {
      int removed=0;
      long chart_id=ChartFirst();
      while(chart_id>=0)
      {
         removed+=ClearOnChart(chart_id);
         chart_id=ChartNext(chart_id);
      }
      return removed;
   }

   void DrawAcceptedExecution(SCGCFinalSignal &signal,SCGXTradePlan &plan,SCGXExecutionResult &result)
   {
      if(!m_config.draw_executed_signals)
         return;
      if(!result.sent && !result.paper_only)
         return;

      if(m_config.draw_on_both_input_symbol_charts)
      {
         DrawDivergenceLeg(signal,m_config.symbol_a);
         if(m_config.symbol_b!=m_config.symbol_a)
            DrawDivergenceLeg(signal,m_config.symbol_b);
      }
      else
         DrawDivergenceLeg(signal,plan.trade_symbol);

      DrawTradeLevels(plan);
   }

   void Clear()
   {
      if(m_config.clear_execution_objects_on_deinit)
         ClearOwnedObjects();
   }
};

#endif
