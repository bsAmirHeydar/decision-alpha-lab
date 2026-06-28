#ifndef __DAL_STC_ENGINE_MQH__
#define __DAL_STC_ENGINE_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_WLevels.mqh>

class CSTC_Engine
{
private:
   STC_Config       m_cfg;
   STC_RuntimeState m_state;
   STC_BuildSanity  m_sanity;
   STC_TimeSnapshot m_time;

public:
   CSTC_Engine()
   {
      STC_ResetConfig(m_cfg);
      STC_ResetRuntimeState(m_state);
      STC_ResetBuildSanity(m_sanity);
      STC_ResetTimeSnapshot(m_time);
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

   STC_TimeSnapshot CurrentTimeSnapshot()
   {
      return m_time;
   }

   bool Init()
   {
      if(!m_state.configured)
      {
         m_state.init_status = STC_INIT_CONFIG_ERROR;
         m_state.init_error = "engine was not configured";
         Print("STC LEVEL04 init failed: ", m_state.init_error);
         return false;
      }

      string validation_error = "";
      string validation_warning = "";
      if(!STC_ValidateConfig(m_cfg, validation_error, validation_warning))
      {
         m_state.init_status = STC_INIT_CONFIG_ERROR;
         m_state.init_error = validation_error;
         m_state.init_warning = validation_warning;
         Print("STC LEVEL04 config validation failed: ", validation_error, " warning=", validation_warning);
         return false;
      }
      m_state.init_warning = validation_warning;
      m_state.output_root_common = m_cfg.output_root_common;
      m_state.sanity_file_common = STC_JoinPath(m_state.output_root_common, "stc_level04_build_sanity.csv");
      m_state.runtime_events_file_common = STC_JoinPath(m_state.output_root_common, "stc_level04_runtime_events.csv");
      m_state.time_audit_file_common = STC_JoinPath(m_state.output_root_common, "stc_level04_time_audit.csv");
      m_state.check_candle_audit_file_common = STC_JoinPath(m_state.output_root_common, "stc_level04_check_candles.csv");
      m_state.w_level_audit_file_common = STC_JoinPath(m_state.output_root_common, "stc_level04_w_levels.csv");

      if(!STC_EnsureCommonFolderTree(m_state.output_root_common))
      {
         m_state.init_status = STC_INIT_FOLDER_ERROR;
         m_state.init_error = "failed to create common output folder: " + m_state.output_root_common;
         Print("STC LEVEL04 folder setup failed: ", m_state.init_error);
         return false;
      }

      if(!STC_AcquireInstanceLock(m_cfg, m_state))
      {
         Print("STC LEVEL04 instance lock failed: ", m_state.init_error);
         return false;
      }

      m_state.started_server_time = TimeCurrent();
      m_state.last_pulse_server_time = 0;
      m_state.last_heartbeat_server_time = 0;
      m_state.last_time_audit_server_time = 0;
      m_state.pulse_count = 0;
      m_state.initialized = true;
      m_state.init_status = STC_INIT_OK;
      STC_BuildTimeSnapshot(m_cfg, TimeCurrent(), m_time);

      STC_PrintConfig(m_cfg);
      STC_WriteBuildSanityCsv(m_cfg, m_state, m_sanity);
      STC_AppendRuntimeEventCsv(m_cfg, m_state, "INIT", "level04 check candle aggregator initialized; W levels audited; no SMT, no signals, no orders");
      if(m_cfg.write_time_audit)
      {
         m_state.last_time_audit_server_time = TimeCurrent();
         STC_AppendTimeAuditCsv(m_cfg, m_state, m_time);
      }
      STC_ProcessClosedCheckCandles(m_cfg, m_state, m_time);
      STC_ProcessClosedWLevels(m_cfg, m_state, m_time);

      if(m_state.init_warning != "")
         Print("STC LEVEL04 validation warning: ", m_state.init_warning);

      Print("STC LEVEL04 initialized. sanity_file=", m_state.sanity_file_common,
            " events_file=", m_state.runtime_events_file_common,
            " time_audit_file=", m_state.time_audit_file_common,
            " check_candles_file=", m_state.check_candle_audit_file_common,
            " w_levels_file=", m_state.w_level_audit_file_common);
      Print("STC LEVEL04 initial time *** ", STC_TimeSnapshotOneLine(m_time));
      return true;
   }

   void Pulse(const datetime server_time)
   {
      if(!m_state.initialized) return;
      m_state.pulse_count++;
      m_state.last_pulse_server_time = server_time;
      STC_RefreshInstanceLock(m_cfg, m_state);
      STC_BuildTimeSnapshot(m_cfg, server_time, m_time);

      if(m_cfg.write_time_audit)
      {
         if(m_state.last_time_audit_server_time <= 0 || server_time - m_state.last_time_audit_server_time >= m_cfg.time_audit_seconds)
         {
            m_state.last_time_audit_server_time = server_time;
            STC_AppendTimeAuditCsv(m_cfg, m_state, m_time);
         }
      }

      STC_ProcessClosedCheckCandles(m_cfg, m_state, m_time);
      STC_ProcessClosedWLevels(m_cfg, m_state, m_time);

      if(m_cfg.write_heartbeat)
      {
         if(m_state.last_heartbeat_server_time <= 0 || server_time - m_state.last_heartbeat_server_time >= m_cfg.heartbeat_seconds)
         {
            m_state.last_heartbeat_server_time = server_time;
            string details = "heartbeat; level04 W level builder; " + STC_TimeSnapshotOneLine(m_time) + "; auditedCheckCandles=" + IntegerToString((int)m_state.check_candles_audited) + "; auditedWLevels=" + IntegerToString((int)m_state.w_levels_audited) + "; no SMT candidates, no entries, no orders";
            STC_AppendRuntimeEventCsv(m_cfg, m_state, "HEARTBEAT", details);
            Print("STC LEVEL04 heartbeat pulse=", m_state.pulse_count,
                  " mode=", STC_RuntimeModeText(m_cfg.runtime_mode),
                  " symbols=", m_cfg.symbol1, "/", m_cfg.symbol2,
                  " ", STC_TimeSnapshotOneLine(m_time));
         }
      }
   }

   void Deinit(const int reason)
   {
      if(m_state.initialized)
      {
         STC_AppendRuntimeEventCsv(m_cfg, m_state, "DEINIT", "reason=" + IntegerToString(reason) + "; last_time=" + STC_TimeSnapshotOneLine(m_time));
         Print("STC LEVEL04 deinit reason=", reason, " pulses=", m_state.pulse_count);
      }
      STC_ReleaseInstanceLock(m_cfg, m_state);
      m_state.initialized = false;
   }
};

#endif
