#ifndef __SF02_RUNTIME_CONFIG_MQH__
#define __SF02_RUNTIME_CONFIG_MQH__

#include "SF02_RuntimeEnums.mqh"
#include "../Contracts/SF01_StringCodec.mqh"

struct SF02_RuntimeConfig
{
   string strategy_id;
   string strategy_version;
   string run_id;
   long generation_id;
   ENUM_SF02_RUN_MODE run_mode;
   bool strict_fail_closed;
   bool enable_audit_bus;
   int timer_period_ms;
   int max_events_per_cycle;
   int audit_bus_capacity;
   ENUM_SF02_BUS_OVERFLOW_POLICY audit_overflow_policy;
};

SF02_RuntimeConfig SF02_DefaultRuntimeConfig()
{
   SF02_RuntimeConfig value;
   value.strategy_id = "unbound_strategy";
   value.strategy_version = "0.0.0";
   value.run_id = "run_unbound";
   value.generation_id = 1;
   value.run_mode = SF02_MODE_ANATOMY_AUDIT;
   value.strict_fail_closed = true;
   value.enable_audit_bus = true;
   value.timer_period_ms = 250;
   value.max_events_per_cycle = 32;
   value.audit_bus_capacity = 512;
   value.audit_overflow_policy = SF02_BUS_REJECT_NEW;
   return value;
}

bool SF02_ValidateRuntimeConfig(const SF02_RuntimeConfig &value, string &error)
{
   if(!SF01_IsSafeIdentifier(value.strategy_id)) { error = "invalid strategy_id"; return false; }
   if(!SF01_IsSafeIdentifier(value.strategy_version)) { error = "invalid strategy_version"; return false; }
   if(!SF01_IsSafeIdentifier(value.run_id)) { error = "invalid run_id"; return false; }
   if(value.generation_id <= 0) { error = "generation_id must be positive"; return false; }
   if(value.timer_period_ms < 10 || value.timer_period_ms > 60000)
   { error = "timer_period_ms out of range"; return false; }
   if(value.max_events_per_cycle <= 0 || value.max_events_per_cycle > 10000)
   { error = "max_events_per_cycle out of range"; return false; }
   if(value.audit_bus_capacity < 8 || value.audit_bus_capacity > 1000000)
   { error = "audit_bus_capacity out of range"; return false; }
   error = "";
   return true;
}

#endif
