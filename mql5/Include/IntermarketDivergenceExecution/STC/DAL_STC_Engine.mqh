#ifndef __DAL_STC_ENGINE_MQH__
#define __DAL_STC_ENGINE_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Journal.mqh>

class CSTC_Engine
{
private:
   STC_Config       m_cfg;
   STC_RuntimeState m_state;
   STC_BuildSanity  m_sanity;

public:
   CSTC_Engine()
   {
      STC_ResetConfig(m_cfg);
      STC_ResetRuntimeState(m_state);
      STC_ResetBuildSanity(m_sanity);
   }

   void Configure(STC_Config &cfg)
   {
      m_cfg = cfg;
      m_state.configured = true;
   }

   STC_RuntimeState State()
   {
      return m_state;
   }

   bool Init()
   {
      if(!m_state.configured)
      {
         m_state.init_status = STC_INIT_CONFIG_ERROR;
         m_state.init_error = "engine was not configured";
         Print("STC LEVEL01 init failed: ", m_state.init_error);
         return false;
      }

      string validation_error = "";
      string validation_warning = "";
      if(!STC_ValidateConfig(m_cfg, validation_error, validation_warning))
      {
         m_state.init_status = STC_INIT_CONFIG_ERROR;
         m_state.init_error = validation_error;
         m_state.init_warning = validation_warning;
         Print("STC LEVEL01 config validation failed: ", validation_error, " warning=", validation_warning);
         return false;
      }
      m_state.init_warning = validation_warning;
      m_state.output_root_common = m_cfg.output_root_common;
      m_state.sanity_file_common = STC_JoinPath(m_state.output_root_common, "stc_level01_build_sanity.csv");
      m_state.runtime_events_file_common = STC_JoinPath(m_state.output_root_common, "stc_level01_runtime_events.csv");

      if(!STC_EnsureCommonFolderTree(m_state.output_root_common))
      {
         m_state.init_status = STC_INIT_FOLDER_ERROR;
         m_state.init_error = "failed to create common output folder: " + m_state.output_root_common;
         Print("STC LEVEL01 folder setup failed: ", m_state.init_error);
         return false;
      }

      if(!STC_AcquireInstanceLock(m_cfg, m_state))
      {
         Print("STC LEVEL01 instance lock failed: ", m_state.init_error);
         return false;
      }

      m_state.started_server_time = TimeCurrent();
      m_state.last_pulse_server_time = 0;
      m_state.last_heartbeat_server_time = 0;
      m_state.pulse_count = 0;
      m_state.initialized = true;
      m_state.init_status = STC_INIT_OK;

      STC_PrintConfig(m_cfg);
      STC_WriteBuildSanityCsv(m_cfg, m_state, m_sanity);
      STC_AppendRuntimeEventCsv(m_cfg, m_state, "INIT", "level01 skeleton initialized; no signal detection and no order execution are enabled");

      if(m_state.init_warning != "")
         Print("STC LEVEL01 validation warning: ", m_state.init_warning);

      Print("STC LEVEL01 initialized. sanity_file=", m_state.sanity_file_common,
            " events_file=", m_state.runtime_events_file_common);
      return true;
   }

   void Pulse(const datetime server_time)
   {
      if(!m_state.initialized) return;
      m_state.pulse_count++;
      m_state.last_pulse_server_time = server_time;
      STC_RefreshInstanceLock(m_cfg, m_state);

      if(m_cfg.write_heartbeat)
      {
         if(m_state.last_heartbeat_server_time <= 0 || server_time - m_state.last_heartbeat_server_time >= m_cfg.heartbeat_seconds)
         {
            m_state.last_heartbeat_server_time = server_time;
            string details = "heartbeat; level01 no-op engine; no W levels, no SMT candidates, no entries, no orders";
            STC_AppendRuntimeEventCsv(m_cfg, m_state, "HEARTBEAT", details);
            Print("STC LEVEL01 heartbeat pulse=", m_state.pulse_count,
                  " mode=", STC_RuntimeModeText(m_cfg.runtime_mode),
                  " symbols=", m_cfg.symbol1, "/", m_cfg.symbol2,
                  " output=", m_state.output_root_common);
         }
      }
   }

   void Deinit(const int reason)
   {
      if(m_state.initialized)
      {
         STC_AppendRuntimeEventCsv(m_cfg, m_state, "DEINIT", "reason=" + IntegerToString(reason));
         Print("STC LEVEL01 deinit reason=", reason, " pulses=", m_state.pulse_count);
      }
      STC_ReleaseInstanceLock(m_cfg, m_state);
      m_state.initialized = false;
   }
};

#endif
