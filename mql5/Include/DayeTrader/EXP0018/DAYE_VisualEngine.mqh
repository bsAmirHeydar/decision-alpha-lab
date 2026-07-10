#ifndef __EXP0018_DAYE_VISUAL_ENGINE_MQH__
#define __EXP0018_DAYE_VISUAL_ENGINE_MQH__

#include <DayeTrader/EXP0018/DAYE_VisualSelfTest.mqh>
#include <DayeTrader/EXP0018/DAYE_SymbolResolver.mqh>

class CDayeVisualEngine
{
private:
   DAYE_VisualConfig m_config;
   DAYE_TimeConfig m_time_config;
   CDayeRenderEngine m_render_engine;
   DAYE_RenderConfig m_render_config;
   DAYE_VisualSummary m_summary;
   bool m_initialized;
   bool m_render_pipeline_initialized;
   string m_render_pipeline_reason;
   string m_last_local_fallback_reason;
   datetime m_last_visual_refresh_utc;

   bool ValidateConfig(string &reason)
   {
      reason="";
      if(m_config.schema_version!=DAYE_VISUAL_SCHEMA_VERSION) { reason="schema_version_invalid"; return false; }
      if(m_config.lookback_weeks<1 || m_config.lookback_weeks>104) { reason="lookback_weeks_out_of_range"; return false; }
      if(m_config.maximum_target_charts_per_symbol<1 || m_config.maximum_target_charts_per_symbol>64) { reason="target_chart_limit_invalid"; return false; }
      if(m_config.major_label_font_size<6 || m_config.minor_label_font_size<6) { reason="font_size_invalid"; return false; }
      if(m_config.anchor_width<1 || m_config.anchor_width>5) { reason="anchor_width_invalid"; return false; }
      if(m_config.local_visual_minimum_bars<2) { reason="local_visual_minimum_bars_too_small"; return false; }
      return true;
   }

   int ResolveTargetCharts(const string symbol_a,const string symbol_b,long &chart_ids[])
   {
      ArrayResize(chart_ids,0);
      long current=ChartID();
      if(m_config.target_policy==DAYE_VISUAL_TARGET_CURRENT_CHART_IF_SYMBOL)
      {
         string current_symbol=ChartSymbol(current);
         if(current_symbol==symbol_a || current_symbol==symbol_b)
         {
            ArrayResize(chart_ids,1); chart_ids[0]=current;
         }
         return ArraySize(chart_ids);
      }
      long chart=ChartFirst();
      while(chart>=0 && ArraySize(chart_ids)<m_config.maximum_target_charts_per_symbol*2)
      {
         string chart_symbol=ChartSymbol(chart);
         if(chart_symbol==symbol_a || chart_symbol==symbol_b)
         {
            int n=ArraySize(chart_ids); ArrayResize(chart_ids,n+1); chart_ids[n]=chart;
            if(m_config.target_policy==DAYE_VISUAL_TARGET_FIRST_OPEN_SYMBOL_CHART && n>=1) break;
         }
         chart=ChartNext(chart);
      }
      if(ArraySize(chart_ids)==0 && m_config.open_missing_symbol_chart)
      {
         ENUM_TIMEFRAMES tf=m_config.opened_chart_timeframe;
         if(tf==PERIOD_CURRENT) tf=PERIOD_M15;
         long first=ChartOpen(symbol_a,tf);
         long second=ChartOpen(symbol_b,tf);
         if(first>0) { ArrayResize(chart_ids,1); chart_ids[0]=first; }
         if(second>0) { int n=ArraySize(chart_ids); ArrayResize(chart_ids,n+1); chart_ids[n]=second; }
      }
      return ArraySize(chart_ids);
   }

   bool SnapshotForChart(const DAYE_PairedPeriodSnapshot &period,const string chart_symbol,
                         DAYE_SymbolPeriodSnapshot &snapshot)
   {
      if(period.symbol_a.broker_symbol==chart_symbol) { snapshot=period.symbol_a; return true; }
      if(period.symbol_b.broker_symbol==chart_symbol) { snapshot=period.symbol_b; return true; }
      ZeroMemory(snapshot); return false;
   }

   bool ToBroker(const datetime utc_time,datetime &broker_time)
   {
      bool replay_safe=true; string reason="";
      return DAYE_UtcToBrokerRenderTime(utc_time,m_time_config,broker_time,replay_safe,reason);
   }

   bool LocalToBroker(const datetime local_ny,const DAYE_LocalResolutionPolicy policy,datetime &broker_time)
   {
      datetime utc_time=0; string reason="";
      DAYE_StatusCode status=DAYE_ResolveNewYorkLocalToUtc(local_ny,m_time_config,policy,utc_time,reason);
      if(status!=DAYE_STATUS_OK) return false;
      return ToBroker(utc_time,broker_time);
   }

   double LabelPrice(const DAYE_SymbolPeriodSnapshot &snapshot,const bool above=true)
   {
      double point=SymbolInfoDouble(snapshot.broker_symbol,SYMBOL_POINT);
      if(point<=0.0) point=MathMax(MathAbs(snapshot.high),1.0)*1.0e-6;
      if(above) return snapshot.high+m_config.label_vertical_offset_points*point;
      return snapshot.low-m_config.label_vertical_offset_points*point;
   }

   void CountResult(const bool ok,const bool created)
   {
      if(ok)
      {
         if(created) m_summary.created_count++;
         else m_summary.updated_count++;
      }
      else m_summary.failed_count++;
   }

   bool DrawBoundary(const long chart_id,const string logical_id,const datetime broker_time,
                     const color line_color,const ENUM_LINE_STYLE style,const int width,
                     const string tooltip,const string kind)
   {
      bool created=false;
      string name=DAYE_VisualObjectName(kind,logical_id);
      ResetLastError();
      bool ok=DAYE_VisualUpsertVLine(chart_id,name,broker_time,line_color,style,width,m_config,tooltip,created);
      if(!ok && m_config.print_detailed_source_diagnostics)
         Print("EXP0018 P10 object failure kind=",kind," name=",name," chart=",chart_id," error=",GetLastError());
      CountResult(ok,created);
      if(ok) m_summary.boundary_count++;
      return ok;
   }

   bool DrawText(const long chart_id,const string logical_id,const datetime broker_time,
                 const double price,const string text,const int font_size,const string kind)
   {
      bool created=false;
      string name=DAYE_VisualObjectName(kind,logical_id);
      ResetLastError();
      bool ok=DAYE_VisualUpsertText(chart_id,name,broker_time,price,text,m_config.label_color,font_size,m_config,
                                   "EXP0018 P10 "+text,created);
      if(!ok && m_config.print_detailed_source_diagnostics)
         Print("EXP0018 P10 object failure kind=",kind," name=",name," chart=",chart_id," price=",DoubleToString(price,8)," error=",GetLastError());
      CountResult(ok,created);
      if(ok) m_summary.label_count++;
      return ok;
   }

   bool DrawRangeBox(const long chart_id,const string logical_id,const datetime start_broker,
                     const datetime end_broker,const double high_price,const double low_price,
                     const color box_color,const int alpha,const string kind,const string tooltip)
   {
      bool created=false;
      string name=DAYE_VisualObjectName(kind,logical_id);
      ResetLastError();
      bool ok=DAYE_VisualUpsertRectangle(chart_id,name,start_broker,end_broker,high_price,low_price,
                                         box_color,alpha,STYLE_SOLID,1,true,m_config,tooltip,created);
      if(!ok && m_config.print_detailed_source_diagnostics)
         Print("EXP0018 P10 object failure kind=",kind," name=",name," chart=",chart_id,
               " t1=",TimeToString(start_broker,TIME_DATE|TIME_SECONDS),
               " t2=",TimeToString(end_broker,TIME_DATE|TIME_SECONDS),
               " high=",DoubleToString(high_price,8)," low=",DoubleToString(low_price,8),
               " error=",GetLastError());
      CountResult(ok,created);
      return ok;
   }

   void DrawDaily(const long chart_id,const DAYE_SymbolPeriodSnapshot &snapshot)
   {
      datetime start_broker=0,end_broker=0;
      if(!ToBroker(snapshot.window.start_utc,start_broker) || !ToBroker(snapshot.window.end_utc,end_broker))
      { m_summary.failed_count++; return; }
      string logical=DAYE_VisualLogicalId("DAY",snapshot.snapshot_id,chart_id);
      if(m_config.render_daily_frame)
      {
         if(DrawRangeBox(chart_id,logical,start_broker,end_broker,snapshot.high,snapshot.low,
                         m_config.daily_color,m_config.daily_fill_alpha,"DAY_BOX",
                         "EXP0018 P10 Daily frame | "+snapshot.trading_day_key)) m_summary.daily_frame_count++;
      }
      if(m_config.render_daily_boundaries)
      {
         DrawBoundary(chart_id,logical+"|START",start_broker,m_config.daily_color,m_config.major_boundary_style,
                      m_config.major_boundary_width,"Daye day start 18:00 NY","DAY_START");
         DrawBoundary(chart_id,logical+"|END",end_broker,m_config.daily_color,m_config.major_boundary_style,
                      m_config.major_boundary_width,"Daye day end 17:00 NY","DAY_END");
      }
      if(m_config.render_daily_label)
      {
         datetime mid=start_broker+(datetime)(((long)end_broker-(long)start_broker)/2);
         DrawText(chart_id,logical+"|LABEL",mid,LabelPrice(snapshot,true),"D "+snapshot.trading_day_key,
                  m_config.major_label_font_size,"DAY_LABEL");
      }
      if(m_config.render_gap_band || m_config.render_gap_boundaries) DrawGap(chart_id,snapshot);
      if(m_config.render_two) DrawTwo(chart_id,snapshot);
      if(m_config.render_provisional_week_boundaries) DrawProvisionalWeek(chart_id,snapshot);
   }

   void DrawGap(const long chart_id,const DAYE_SymbolPeriodSnapshot &daily)
   {
      datetime gap_start_ny=daily.window.end_ny;
      datetime gap_end_ny=0;
      if(!DAYE_BuildCivilDateTime(gap_start_ny,0,18*3600,gap_end_ny)) return;
      datetime gap_start_broker=0,gap_end_broker=0;
      if(!LocalToBroker(gap_start_ny,m_time_config.ambiguous_start_policy,gap_start_broker) ||
         !LocalToBroker(gap_end_ny,m_time_config.ambiguous_end_policy,gap_end_broker)) return;
      string logical=DAYE_VisualLogicalId("GAP",daily.snapshot_id,chart_id);
      if(m_config.render_gap_boundaries)
      {
         DrawBoundary(chart_id,logical+"|START",gap_start_broker,m_config.gap_color,STYLE_DOT,1,"Gap start 17:00 NY","GAP_START");
         DrawBoundary(chart_id,logical+"|END",gap_end_broker,m_config.gap_color,STYLE_DOT,1,"Gap end 18:00 NY","GAP_END");
      }
      if(m_config.render_gap_band)
      {
         double chart_max=0.0,chart_min=0.0;
         if(ChartGetDouble(chart_id,CHART_PRICE_MAX,0,chart_max) && ChartGetDouble(chart_id,CHART_PRICE_MIN,0,chart_min) && chart_max>chart_min)
         {
            if(DrawRangeBox(chart_id,logical,gap_start_broker,gap_end_broker,chart_max,chart_min,
                            m_config.gap_color,m_config.gap_fill_alpha,"GAP_BOX","Declared Daye gap 17:00-18:00 NY")) m_summary.gap_count++;
         }
      }
   }

   void DrawSession(const long chart_id,const DAYE_SymbolPeriodSnapshot &snapshot)
   {
      datetime start_broker=0,end_broker=0;
      if(!ToBroker(snapshot.window.start_utc,start_broker) || !ToBroker(snapshot.window.end_utc,end_broker))
      { m_summary.failed_count++; return; }
      string logical=DAYE_VisualLogicalId("SESSION",snapshot.snapshot_id,chart_id);
      color session_color=DAYE_SessionVisualColor(snapshot.period_code,m_config);
      if(m_config.render_session_boxes)
      {
         if(DrawRangeBox(chart_id,logical,start_broker,end_broker,snapshot.high,snapshot.low,session_color,
                         m_config.session_fill_alpha,"SESSION_BOX","Daye Session "+snapshot.period_code)) m_summary.session_box_count++;
      }
      if(m_config.render_session_boundaries)
      {
         DrawBoundary(chart_id,logical+"|START",start_broker,session_color,m_config.major_boundary_style,
                      m_config.major_boundary_width,"Session "+snapshot.period_code+" start","SESSION_START");
      }
      if(m_config.render_session_labels)
      {
         datetime mid=start_broker+(datetime)(((long)end_broker-(long)start_broker)/2);
         DrawText(chart_id,logical+"|LABEL",mid,LabelPrice(snapshot,true),
                  DAYE_QuarterNumberFromCode(snapshot.period_code)+" "+snapshot.period_code,
                  m_config.major_label_font_size,"SESSION_LABEL");
      }
      if(m_config.render_tdo && snapshot.period_code=="L") DrawTdo(chart_id,snapshot,start_broker);
   }

   void DrawSubcycle(const long chart_id,const DAYE_SymbolPeriodSnapshot &snapshot)
   {
      datetime start_broker=0,end_broker=0;
      if(!ToBroker(snapshot.window.start_utc,start_broker) || !ToBroker(snapshot.window.end_utc,end_broker))
      { m_summary.failed_count++; return; }
      string logical=DAYE_VisualLogicalId("SUBCYCLE",snapshot.snapshot_id,chart_id);
      color subcycle_color=DAYE_SessionVisualColor(DAYE_ParentSessionCode(snapshot.period_code),m_config);
      if(m_config.render_subcycle_boxes)
      {
         if(DrawRangeBox(chart_id,logical,start_broker,end_broker,snapshot.high,snapshot.low,subcycle_color,
                         m_config.subcycle_fill_alpha,"SUB_BOX","Daye Subcycle "+snapshot.period_code)) m_summary.subcycle_box_count++;
      }
      if(m_config.render_subcycle_boundaries)
      {
         DrawBoundary(chart_id,logical+"|START",start_broker,subcycle_color,m_config.subcycle_boundary_style,
                      m_config.subcycle_boundary_width,"Subcycle "+snapshot.period_code+" start","SUB_START");
      }
      if(m_config.render_subcycle_labels)
      {
         datetime mid=start_broker+(datetime)(((long)end_broker-(long)start_broker)/2);
         DrawText(chart_id,logical+"|LABEL",mid,LabelPrice(snapshot,true),DAYE_PhaseLabel(snapshot.period_code),
                  m_config.minor_label_font_size,"SUB_LABEL");
      }
      if(snapshot.period_family==DAYE_FAMILY_SUBCYCLE_90M && m_config.render_micro_22_5_boundaries)
         DrawMicroQuarters(chart_id,snapshot);
      if(m_config.render_extended_session_true_opens) DrawExtendedTrueOpen(chart_id,snapshot,start_broker);
   }

   void DrawMicroQuarters(const long chart_id,const DAYE_SymbolPeriodSnapshot &snapshot)
   {
      // A full 90-minute subcycle is exactly four local-time quarters of 1,350 seconds.
      // Every local boundary is converted separately so DST gaps/folds remain explicit.
      string logical=DAYE_VisualLogicalId("MICRO",snapshot.snapshot_id,chart_id);
      for(int q=1;q<=3;q++)
      {
         datetime local_boundary=snapshot.window.start_ny+(datetime)(q*1350);
         datetime broker_boundary=0;
         if(!LocalToBroker(local_boundary,m_time_config.ambiguous_start_policy,broker_boundary))
         { m_summary.skipped_count++; continue; }
         bool ok=DrawBoundary(chart_id,logical+"|B|"+IntegerToString(q),broker_boundary,m_config.micro_color,
                              m_config.micro_boundary_style,m_config.micro_boundary_width,
                              "22.5-minute micro-quarter boundary","MICRO_BOUNDARY");
         if(ok) m_summary.micro_boundary_count++;
      }
      if(m_config.render_micro_22_5_labels)
      {
         for(int q=1;q<=4;q++)
         {
            datetime local_mid=snapshot.window.start_ny+(datetime)((q-1)*1350+675);
            datetime broker_mid=0;
            if(!LocalToBroker(local_mid,m_time_config.ambiguous_start_policy,broker_mid)) continue;
            DrawText(chart_id,logical+"|L|"+IntegerToString(q),broker_mid,LabelPrice(snapshot,false),
                     "q"+IntegerToString(q),m_config.minor_label_font_size,"MICRO_LABEL");
         }
      }
   }

   void DrawTdo(const long chart_id,const DAYE_SymbolPeriodSnapshot &session_l,const datetime start_broker)
   {
      datetime end_ny=0;
      if(!DAYE_BuildCivilDateTime(session_l.window.start_ny,0,17*3600,end_ny)) return;
      datetime end_broker=0;
      if(!LocalToBroker(end_ny,m_time_config.ambiguous_end_policy,end_broker)) return;
      string logical=DAYE_VisualLogicalId("TDO",session_l.snapshot_id,chart_id);
      bool created=false;
      bool ok=DAYE_VisualUpsertHorizontalSegment(chart_id,DAYE_VisualObjectName("TDO",logical),start_broker,end_broker,
                                                 session_l.open,m_config.tdo_color,STYLE_SOLID,m_config.anchor_width,m_config,
                                                 "TDO 00:00 NY to 17:00 NY",created);
      CountResult(ok,created); if(ok)
      {
         m_summary.tdo_count++;
         datetime mid=start_broker+(datetime)(((long)end_broker-(long)start_broker)/2);
         DrawText(chart_id,logical+"|LABEL",mid,session_l.open,"TDO",m_config.major_label_font_size,"TDO_LABEL");
      }
   }

   void DrawTwo(const long chart_id,const DAYE_SymbolPeriodSnapshot &daily)
   {
      MqlDateTime parts; if(!TimeToStruct(daily.window.start_ny,parts)) return;
      int required_day=(m_config.two_anchor_policy==DAYE_TWO_TUESDAY_1800_LITERAL)?2:1;
      if(parts.day_of_week!=required_day) return;
      int day_offset=(required_day==2)?3:4;
      datetime end_ny=0;
      if(!DAYE_BuildCivilDateTime(daily.window.start_ny,day_offset,17*3600,end_ny)) return;
      datetime start_broker=0,end_broker=0;
      if(!ToBroker(daily.window.start_utc,start_broker) || !LocalToBroker(end_ny,m_time_config.ambiguous_end_policy,end_broker)) return;
      string logical=DAYE_VisualLogicalId("TWO",daily.snapshot_id,chart_id,IntegerToString((int)m_config.two_anchor_policy));
      bool created=false;
      bool ok=DAYE_VisualUpsertHorizontalSegment(chart_id,DAYE_VisualObjectName("TWO",logical),start_broker,end_broker,
                                                 daily.open,m_config.two_color,STYLE_SOLID,m_config.anchor_width,m_config,
                                                 "TWO policy="+IntegerToString((int)m_config.two_anchor_policy),created);
      CountResult(ok,created); if(ok)
      {
         m_summary.two_count++;
         datetime mid=start_broker+(datetime)(((long)end_broker-(long)start_broker)/2);
         DrawText(chart_id,logical+"|LABEL",mid,daily.open,"TWO",m_config.major_label_font_size,"TWO_LABEL");
      }
   }

   void DrawExtendedTrueOpen(const long chart_id,const DAYE_SymbolPeriodSnapshot &subcycle,const datetime start_broker)
   {
      string code=subcycle.period_code;
      if(code!="a2" && code!="l2" && code!="n2" && code!="p2") return;
      string parent=DAYE_ParentSessionCode(code);
      int end_second=17*3600; int day_offset=0;
      if(parent=="A") { end_second=0; day_offset=1; }
      else if(parent=="L") end_second=6*3600;
      else if(parent=="N") end_second=12*3600;
      datetime end_ny=0;
      if(!DAYE_BuildCivilDateTime(subcycle.window.start_ny,day_offset,end_second,end_ny)) return;
      datetime end_broker=0;
      if(!LocalToBroker(end_ny,m_time_config.ambiguous_end_policy,end_broker)) return;
      string logical=DAYE_VisualLogicalId("TSO",subcycle.snapshot_id,chart_id);
      bool created=false;
      bool ok=DAYE_VisualUpsertHorizontalSegment(chart_id,DAYE_VisualObjectName("TSO",logical),start_broker,end_broker,
                                                 subcycle.open,m_config.true_open_color,STYLE_DASH,1,m_config,
                                                 "Optional session True Open from Q2 subcycle "+code,created);
      CountResult(ok,created); if(ok) m_summary.true_open_count++;
   }

   void DrawProvisionalWeek(const long chart_id,const DAYE_SymbolPeriodSnapshot &daily)
   {
      MqlDateTime parts; if(!TimeToStruct(daily.window.start_ny,parts)) return;
      int required_day=(m_config.provisional_week_policy==DAYE_WEEK_SUNDAY_1800_TO_FRIDAY_1700)?0:1;
      if(parts.day_of_week!=required_day) return;
      int day_offset=(required_day==0)?5:4;
      datetime start_broker=0,end_ny=0,end_broker=0;
      if(!ToBroker(daily.window.start_utc,start_broker)) return;
      if(!DAYE_BuildCivilDateTime(daily.window.start_ny,day_offset,17*3600,end_ny)) return;
      if(!LocalToBroker(end_ny,m_time_config.ambiguous_end_policy,end_broker)) return;
      string logical=DAYE_VisualLogicalId("WEEK",daily.snapshot_id,chart_id,IntegerToString((int)m_config.provisional_week_policy));
      DrawBoundary(chart_id,logical+"|START",start_broker,m_config.week_color,STYLE_DASHDOT,2,
                   "PROVISIONAL weekly boundary; WW remains doctrine-blocked","WEEK_START");
      DrawBoundary(chart_id,logical+"|END",end_broker,m_config.week_color,STYLE_DASHDOT,2,
                   "PROVISIONAL weekly end; WW remains doctrine-blocked","WEEK_END");
      m_summary.week_boundary_count+=2;
   }

   void DrawLegend(const long chart_id)
   {
      if(!m_config.render_legend) return;
      string text="EXP0018 DAYE VISUAL ANATOMY\nD 18:00-17:00 | A/L/N/P | a1-p4\n22.5m micro quarters | GAP 17:00-18:00\nTDO | TWO | P08 divergence lines";
      bool created=false;
      string logical=DAYE_VisualLogicalId("LEGEND","CORE",chart_id);
      bool ok=DAYE_VisualUpsertLegend(chart_id,DAYE_VisualObjectName("LEGEND",logical),text,m_config,created);
      CountResult(ok,created);
   }

   void ProcessSymbolPeriodsChart(const long chart_id,const DAYE_SymbolPeriodSnapshot &periods[],const datetime lookback_start_utc)
   {
      DrawLegend(chart_id);
      for(int i=0;i<ArraySize(periods);i++)
      {
         DAYE_SymbolPeriodSnapshot snapshot=periods[i];
         if(snapshot.window.end_utc<lookback_start_utc) { m_summary.skipped_count++; continue; }
         if(!DAYE_VisualPeriodCompletenessAllowed(snapshot,m_config)) { m_summary.skipped_count++; continue; }
         if(snapshot.high<=0.0 || snapshot.low<=0.0 || snapshot.high<snapshot.low) { m_summary.failed_count++; continue; }
         if(snapshot.period_family==DAYE_FAMILY_DAILY) DrawDaily(chart_id,snapshot);
         else if(snapshot.period_family==DAYE_FAMILY_SESSION) DrawSession(chart_id,snapshot);
         else if(snapshot.period_family==DAYE_FAMILY_SUBCYCLE_90M || snapshot.period_family==DAYE_FAMILY_SUBCYCLE_TAIL)
            DrawSubcycle(chart_id,snapshot);
      }
      ChartRedraw(chart_id);
   }

   void ProcessChart(const long chart_id,const DAYE_PairedPeriodSnapshot &periods[],const datetime lookback_start_utc)
   {
      string chart_symbol=ChartSymbol(chart_id);
      DAYE_SymbolPeriodSnapshot local_periods[];
      ArrayResize(local_periods,0);
      for(int i=0;i<ArraySize(periods);i++)
      {
         DAYE_SymbolPeriodSnapshot snapshot;
         if(!SnapshotForChart(periods[i],chart_symbol,snapshot)) continue;
         int n=ArraySize(local_periods);
         ArrayResize(local_periods,n+1);
         local_periods[n]=snapshot;
      }
      ProcessSymbolPeriodsChart(chart_id,local_periods,lookback_start_utc);
   }

   bool BuildLocalPeriodsForChart(const long chart_id,const datetime current_broker_time,
                                  DAYE_SymbolPeriodSnapshot &periods[],string &reason)
   {
      ArrayResize(periods,0);
      reason="";
      string chart_symbol=ChartSymbol(chart_id);
      if(chart_symbol=="") { reason="current_chart_symbol_empty"; return false; }

      DAYE_SymbolDescriptor descriptor;
      if(!DAYE_LoadSymbolDescriptor(chart_symbol,chart_symbol,descriptor))
      {
         reason="local_symbol_descriptor_failed:"+descriptor.reason_code;
         return false;
      }

      DAYE_PeriodAggregationConfig period_config=m_render_config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config;
      DAYE_DataSyncConfig data_config=period_config.data_config;
      data_config.broker_symbol_a=chart_symbol;
      data_config.broker_symbol_b=chart_symbol+"__LOCAL_VISUAL_UNUSED";
      data_config.canonical_symbol_a=chart_symbol;
      data_config.canonical_symbol_b="LOCAL_VISUAL_UNUSED";
      int minimum_bars=m_config.local_visual_minimum_bars;
      if(minimum_bars>data_config.requested_bars_per_symbol) minimum_bars=data_config.requested_bars_per_symbol;
      if(minimum_bars<2) minimum_bars=2;
      data_config.minimum_common_bars=minimum_bars;
      data_config.require_series_synchronized=false;
      data_config.fail_on_any_invalid_bar=false;
      data_config.require_complete_alignment=false;
      data_config.enforce_freshness=false;
      period_config.data_config=data_config;
      period_config.require_both_symbols_complete=false;
      period_config.minimum_complete_paired_periods=0;

      DAYE_SymbolBar bars[];
      DAYE_SymbolDataHealth health;
      if(!DAYE_LoadClosedBars(descriptor,data_config,m_time_config,current_broker_time,bars,health))
      {
         reason="local_bar_load_failed:"+health.reason_code+
                " available="+IntegerToString(health.bars_available)+
                " copied="+IntegerToString(health.copied_bars)+
                " accepted="+IntegerToString(health.accepted_bars);
         return false;
      }

      datetime now_utc=0;
      int broker_offset=0;
      bool replay_safe=true;
      string time_reason="";
      if(!DAYE_BrokerToUtc(current_broker_time,m_time_config,now_utc,broker_offset,replay_safe,time_reason))
      {
         reason="local_time_conversion_failed:"+time_reason;
         return false;
      }

      DAYE_PeriodDefinition registry[];
      DAYE_BuildCanonicalPeriodRegistry(registry);
      string aggregate_reason="";
      if(!DAYE_AggregateSymbolBars(bars,period_config,m_time_config,registry,now_utc,now_utc,periods,aggregate_reason))
      {
         reason="local_period_aggregation_failed:"+aggregate_reason;
         return false;
      }
      if(ArraySize(periods)<=0)
      {
         reason="local_period_aggregation_returned_zero_periods";
         return false;
      }
      reason="local_single_symbol_periods_ready";
      return true;
   }

   bool ProcessLocalCurrentChart(const datetime current_broker_time,const datetime lookback_start_utc)
   {
      if(!m_config.allow_single_symbol_time_fallback) return false;
      long chart_id=ChartID();
      DAYE_SymbolPeriodSnapshot periods[];
      string reason="";
      if(!BuildLocalPeriodsForChart(chart_id,current_broker_time,periods,reason))
      {
         m_summary.local_fallback_reason=reason;
         if(m_config.print_detailed_source_diagnostics && reason!=m_last_local_fallback_reason)
            Print("EXP0018 P10 local visual fallback waiting: ",reason," chart=",ChartSymbol(chart_id));
         m_last_local_fallback_reason=reason;
         return false;
      }
      m_last_local_fallback_reason="";
      m_summary.local_fallback_used=true;
      m_summary.local_period_count=ArraySize(periods);
      m_summary.local_fallback_reason=reason;
      m_summary.target_chart_count=1;
      ProcessSymbolPeriodsChart(chart_id,periods,lookback_start_utc);
      return true;
   }

public:
   CDayeVisualEngine(void)
   {
      ZeroMemory(m_summary);
      ZeroMemory(m_render_config);
      m_initialized=false;
      m_render_pipeline_initialized=false;
      m_render_pipeline_reason="not_initialized";
      m_last_local_fallback_reason="";
      m_last_visual_refresh_utc=0;
   }

   bool Initialize(const DAYE_RenderConfig &render_config,const DAYE_VisualConfig &visual_config,
                   const DAYE_TimeConfig &time_config,const bool run_self_tests,
                   const bool write_p08_audit,const string p08_audit_filename)
   {
      m_config=visual_config; m_time_config=time_config; m_render_config=render_config;
      string reason="";
      if(!ValidateConfig(reason)) { Print("EXP0018 P10 invalid visual config reason=",reason); return false; }
      if(run_self_tests && !DAYE_RunEmbeddedVisualSelfTests())
      {
         Print("EXP0018 P10 visual self-test stage failed.");
         return false;
      }

      m_render_pipeline_initialized=m_render_engine.Initialize(render_config,time_config,run_self_tests,write_p08_audit,p08_audit_filename);
      if(m_render_pipeline_initialized)
         m_render_pipeline_reason="paired_divergence_pipeline_initialized";
      else
      {
         m_render_pipeline_reason="paired_divergence_pipeline_unavailable";
         Print("EXP0018 P10 WARNING: paired divergence source did not initialize. Temporal anatomy fallback remains available on the attached chart.");
         if(m_config.fail_init_when_pair_pipeline_unavailable || !m_config.allow_single_symbol_time_fallback)
            return false;
      }
      m_initialized=true;
      Print("EXP0018 P10 Unified Visual Anatomy initialized. pair_pipeline=",
            (m_render_pipeline_initialized?"READY":"DEGRADED_LOCAL_FALLBACK"),
            " chart=",ChartSymbol(ChartID())," no trading authority.");
      if(m_config.render_provisional_week_boundaries)
         Print("EXP0018 P10 WARNING: provisional weekly boundaries enabled while WW doctrine remains blocked.");
      if(m_config.render_extended_session_true_opens)
         Print("EXP0018 P10 NOTICE: extended session True Opens are optional context, not Core signal filters.");
      return true;
   }

   bool Process(const datetime current_broker_time,const bool print_p08_summary,const bool print_visual_summary,
                const bool show_chart_comment)
   {
      if(!m_initialized) return false;
      DAYE_RenderStoreSummary render_summary;
      ZeroMemory(render_summary);
      bool has_render_summary=false;
      DAYE_PairedPeriodSnapshot periods[];
      ArrayResize(periods,0);
      int period_count=0;
      if(m_render_pipeline_initialized)
      {
         m_render_engine.Process(current_broker_time,print_p08_summary,false,false,false,false,0);
         has_render_summary=m_render_engine.GetCurrentSummary(render_summary);
         period_count=m_render_engine.ExportSourcePeriods(periods);
      }

      datetime processing_time_utc=TimeGMT(); if(processing_time_utc<=0) processing_time_utc=current_broker_time;
      ZeroMemory(m_summary); m_summary.schema_version=DAYE_VISUAL_SCHEMA_VERSION;
      m_summary.processing_time_utc=processing_time_utc; m_summary.source_period_count=period_count;
      m_summary.is_replay_safe=has_render_summary?render_summary.is_replay_safe:true;
      m_summary.pair_pipeline_initialized=m_render_pipeline_initialized;
      m_summary.pair_pipeline_reason=m_render_pipeline_reason;
      datetime lookback_start_utc=processing_time_utc-(datetime)(m_config.lookback_weeks*7*86400);

      bool projected_from_pair=false;
      if(period_count>0)
      {
         string symbol_a=periods[0].symbol_a.broker_symbol;
         string symbol_b=periods[0].symbol_b.broker_symbol;
         long charts[];
         m_summary.target_chart_count=ResolveTargetCharts(symbol_a,symbol_b,charts);
         for(int i=0;i<ArraySize(charts);i++)
         {
            ProcessChart(charts[i],periods,lookback_start_utc);
            projected_from_pair=true;
         }
      }

      bool current_chart_covered=false;
      if(projected_from_pair && period_count>0)
      {
         string current_symbol=ChartSymbol(ChartID());
         current_chart_covered=(current_symbol==periods[0].symbol_a.broker_symbol || current_symbol==periods[0].symbol_b.broker_symbol);
      }
      bool projected_from_local=false;
      if(!projected_from_pair || !current_chart_covered)
         projected_from_local=ProcessLocalCurrentChart(current_broker_time,lookback_start_utc);

      if(!projected_from_pair && !projected_from_local)
      {
         m_summary.status=DAYE_VISUAL_STATUS_SOURCE_NOT_READY;
         m_summary.reason_code=(period_count<=0?"paired_source_not_ready_and_local_fallback_waiting":"no_matching_pair_chart_and_local_fallback_waiting");
         if(print_visual_summary) Print(FormatSummary());
         return true;
      }
      m_summary.is_ready=true;
      if(m_summary.failed_count>0) { m_summary.status=DAYE_VISUAL_STATUS_DEGRADED; m_summary.reason_code="one_or_more_visual_objects_failed"; }
      else if(m_summary.local_fallback_used && !m_summary.pair_pipeline_initialized)
      { m_summary.status=DAYE_VISUAL_STATUS_DEGRADED; m_summary.reason_code="time_anatomy_ready_pair_divergence_source_unavailable"; }
      else { m_summary.status=DAYE_VISUAL_STATUS_READY; m_summary.reason_code="all_enabled_visual_layers_projected"; }
      m_last_visual_refresh_utc=processing_time_utc;
      if(print_visual_summary) Print(FormatSummary());
      if(show_chart_comment) Comment(FormatSummary()+"\nNo order, risk, or execution authority.");
      else Comment("");
      return true;
   }

   string FormatSummary(void)
   {
      return "EXP0018 P10 status="+DAYE_VisualStatusToString(m_summary.status)+
             " periods="+IntegerToString(m_summary.source_period_count)+
             " charts="+IntegerToString(m_summary.target_chart_count)+
             " daily="+IntegerToString(m_summary.daily_frame_count)+
             " sessions="+IntegerToString(m_summary.session_box_count)+
             " subcycles="+IntegerToString(m_summary.subcycle_box_count)+
             " micro="+IntegerToString(m_summary.micro_boundary_count)+
             " TDO="+IntegerToString(m_summary.tdo_count)+
             " TWO="+IntegerToString(m_summary.two_count)+
             " pair="+(m_summary.pair_pipeline_initialized?"READY":"OFF")+
             " local="+(m_summary.local_fallback_used?"YES":"NO")+
             " local_periods="+IntegerToString(m_summary.local_period_count)+
             " failed="+IntegerToString(m_summary.failed_count)+
             " reason="+m_summary.reason_code+
             (m_summary.local_fallback_reason!=""?" local_reason="+m_summary.local_fallback_reason:"");
   }

   bool GetCurrentSummary(DAYE_VisualSummary &summary)
   { summary=m_summary; return m_initialized; }

   void Shutdown(void)
   {
      if(m_config.delete_owned_objects_on_deinit) DAYE_DeleteOwnedVisualObjectsFromAllCharts();
      Comment("");
      if(m_render_pipeline_initialized) m_render_engine.Shutdown();
      ZeroMemory(m_summary);
      m_initialized=false;
      m_render_pipeline_initialized=false;
      m_render_pipeline_reason="shutdown";
      m_last_local_fallback_reason="";
      m_last_visual_refresh_utc=0;
   }
};

#endif
