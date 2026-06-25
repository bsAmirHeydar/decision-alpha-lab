#ifndef __DAL_ASTRO_EXECUTION_STATE_MACHINE_MQH__
#define __DAL_ASTRO_EXECUTION_STATE_MACHINE_MQH__

#include <Research/DAL_AstroPureAstrologySignals.mqh>

struct DAL_AstroExecState
{
   bool     initialized;
   string   family_name;
   string   phase;
   string   position_direction;
   string   action;
   int      hold_bars;
   datetime last_bar_time;
   double   last_entry_score;
   double   last_exit_score;
   string   last_reason;
};

void DAL_AstroExecState_Reset(DAL_AstroExecState &s, const string family_name)
{
   s.initialized = true;
   s.family_name = family_name;
   s.phase = "wait";
   s.position_direction = "flat";
   s.action = "wait";
   s.hold_bars = 0;
   s.last_bar_time = 0;
   s.last_entry_score = 0.0;
   s.last_exit_score = 0.0;
   s.last_reason = "";
}

void DAL_AstroExecState_Step(
   DAL_AstroExecState &state,
   const DAL_AstroMapRow &row,
   const DAL_AstroPureSignal &signal,
   const double arm_threshold,
   const double enter_threshold,
   const double reduce_threshold,
   const double exit_threshold
)
{
   if(!state.initialized)
      DAL_AstroExecState_Reset(state, "astro_family");

   state.last_bar_time = row.broker_time;
   state.last_entry_score = signal.entry_score;
   state.last_exit_score = signal.exit_score;
   state.action = "wait";
   state.last_reason = signal.astro_language;

   bool has_long = (signal.entry_signal == "enter_long");
   bool has_short = (signal.entry_signal == "enter_short");
   bool wants_exit = (signal.exit_signal == "exit_or_reduce");
   bool opposite_long = (state.position_direction == "short" && has_long);
   bool opposite_short = (state.position_direction == "long" && has_short);

   if(state.phase == "wait")
   {
      if(signal.entry_score >= enter_threshold && (has_long || has_short))
      {
         state.phase = "enter";
         state.position_direction = has_long ? "long" : "short";
         state.action = state.phase;
         state.hold_bars = 0;
         return;
      }
      if(signal.entry_score >= arm_threshold && signal.direction_name != "flat")
      {
         state.phase = "armed";
         state.position_direction = signal.direction_name;
         state.action = "armed";
         return;
      }
      return;
   }

   if(state.phase == "armed")
   {
      if(signal.entry_score >= enter_threshold && (has_long || has_short))
      {
         state.phase = "enter";
         state.position_direction = has_long ? "long" : "short";
         state.action = "enter";
         state.hold_bars = 0;
         return;
      }
      if(signal.entry_score < arm_threshold || signal.direction_name == "flat")
      {
         state.phase = "wait";
         state.position_direction = "flat";
         state.action = "wait";
      }
      return;
   }

   if(state.phase == "enter")
   {
      state.phase = "hold";
      state.action = "hold";
      state.hold_bars = 1;
      return;
   }

   if(state.phase == "hold")
   {
      state.hold_bars++;
      if(wants_exit && signal.exit_score >= exit_threshold)
      {
         state.phase = "exit";
         state.action = "exit";
         return;
      }
      if((opposite_long || opposite_short) && signal.entry_score >= enter_threshold)
      {
         state.phase = "exit";
         state.action = "exit";
         state.last_reason = signal.astro_language + "|collision=opposite_entry";
         return;
      }
      if(wants_exit && signal.exit_score >= reduce_threshold)
      {
         state.phase = "reduce";
         state.action = "reduce";
         return;
      }
      state.action = "hold";
      return;
   }

   if(state.phase == "reduce")
   {
      state.hold_bars++;
      if(wants_exit && signal.exit_score >= exit_threshold)
      {
         state.phase = "exit";
         state.action = "exit";
         return;
      }
      if(signal.entry_score >= enter_threshold && signal.direction_name == state.position_direction)
      {
         state.phase = "hold";
         state.action = "hold";
         return;
      }
      state.action = "reduce";
      return;
   }

   if(state.phase == "exit")
   {
      state.phase = "wait";
      state.position_direction = "flat";
      state.action = "wait";
      state.hold_bars = 0;
      return;
   }
}

string DAL_AstroExecState_ToText(const DAL_AstroExecState &state)
{
   string txt = "family=" + state.family_name;
   txt += "|phase=" + state.phase;
   txt += "|position=" + state.position_direction;
   txt += "|action=" + state.action;
   txt += "|hold_bars=" + IntegerToString(state.hold_bars);
   txt += "|entry_score=" + DoubleToString(state.last_entry_score, 1);
   txt += "|exit_score=" + DoubleToString(state.last_exit_score, 1);
   return txt;
}

#endif
