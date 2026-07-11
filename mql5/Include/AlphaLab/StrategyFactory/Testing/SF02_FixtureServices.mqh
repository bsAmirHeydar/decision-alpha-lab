#ifndef __SF02_FIXTURE_SERVICES_MQH__
#define __SF02_FIXTURE_SERVICES_MQH__

#include "../Ports/SF02_AllPorts.mqh"
#include "../Contracts/SF01_ContractRegistry.mqh"
#include "../Contracts/SF01_FeatureValue.mqh"

class CSF02FixtureClock : public ISF02ClockPort
{
private:
   long m_now;
public:
   CSF02FixtureClock(void) { m_now = 1783771260000; }
   void SetNow(const long value) { m_now = value; }
   virtual string ServiceId(void) const { return "sf02.fixture_clock"; }
   virtual ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_CLOCK; }
   virtual bool Initialize(const SF02_RuntimeConfig &config, string &error) { error = ""; return true; }
   virtual bool Start(string &error) { error = ""; return true; }
   virtual void Stop(void) {}
   virtual void Shutdown(void) {}
   virtual SF02_ServiceHealth Health(const long now_utc_msc) const
   { SF02_ServiceHealth h; h.service_id=ServiceId(); h.service_kind=ServiceKind(); h.status=SF02_HEALTH_HEALTHY; h.detail="fixture"; h.observed_at_utc_msc=now_utc_msc; return h; }
   virtual long UtcNowMilliseconds(void) const { return m_now; }
   virtual ulong MonotonicMicroseconds(void) const { return 1000; }
   virtual SF01_MarketTimestamp Now(const string source_clock_id = "fixture") const
   { return SF01_MakeUtcMilliseconds(m_now, "UTC", 0, source_clock_id, SF01_TIME_MILLISECONDS); }
};

class CSF02FixtureAnatomyProvider : public ISF02AnatomyProvider
{
private:
   bool m_ready;
   bool m_emitted;
   SF01_AnatomyEvent m_event;
public:
   CSF02FixtureAnatomyProvider(void) { m_ready=false; m_emitted=false; }
   virtual string ServiceId(void) const { return "sf02.fixture_anatomy"; }
   virtual ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_ANATOMY; }
   virtual bool Initialize(const SF02_RuntimeConfig &config, string &error)
   {
      m_event.schema = SF01_AnatomyEventSchema();
      m_event.strategy_id = config.strategy_id;
      m_event.strategy_version = config.strategy_version;
      m_event.producer_id = ServiceId();
      m_event.producer_version = "1.0.0";
      m_event.symbol = "NQ";
      m_event.reference_symbol = "ES";
      m_event.direction = SF01_DIRECTION_LONG;
      m_event.event_time = SF01_MakeUtcMilliseconds(1783771200000, "UTC", 0, "fixture", SF01_TIME_MILLISECONDS);
      m_event.known_time = SF01_MakeUtcMilliseconds(1783771260000, "UTC", 0, "fixture", SF01_TIME_MILLISECONDS);
      m_event.confirmation_time = m_event.known_time;
      m_event.reference_price = 22500.25;
      m_event.invalidation_price = 22480.00;
      m_event.timeframe_seconds = 60;
      m_event.session_id = "new_york_am";
      m_event.parent_event_id = "none";
      m_event.market_event_cluster_id = "cluster_20260711_001";
      m_event.source_hash = "sha256_fixture_event";
      m_event.anatomy_state = "confirmed";
      m_event.event_id = SF01_DeriveAnatomyEventId(m_event);
      m_ready=true; m_emitted=false; error=""; return true;
   }
   virtual bool Start(string &error) { error=""; return m_ready; }
   virtual void Stop(void) {}
   virtual void Shutdown(void) { m_ready=false; }
   virtual SF02_ServiceHealth Health(const long now_utc_msc) const
   { SF02_ServiceHealth h; h.service_id=ServiceId(); h.service_kind=ServiceKind(); h.status=m_ready?SF02_HEALTH_HEALTHY:SF02_HEALTH_UNHEALTHY; h.detail="fixture"; h.observed_at_utc_msc=now_utc_msc; return h; }
   virtual void ProcessTick(const MqlTick &tick) { if(m_ready) m_emitted=true; }
   virtual void ProcessTimer(const long now_utc_msc) {}
   virtual bool PopEvent(SF01_AnatomyEvent &event)
   { if(!m_emitted) return false; event=m_event; m_emitted=false; return true; }
   virtual int PendingEventCount(void) const { return m_emitted ? 1 : 0; }
};

class CSF02FixtureFeatureProvider : public ISF02FeatureProvider
{
public:
   virtual string ServiceId(void) const { return "sf02.fixture_features"; }
   virtual ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_FEATURES; }
   virtual bool Initialize(const SF02_RuntimeConfig &config, string &error) { error=""; return true; }
   virtual bool Start(string &error) { error=""; return true; }
   virtual void Stop(void) {}
   virtual void Shutdown(void) {}
   virtual SF02_ServiceHealth Health(const long now_utc_msc) const
   { SF02_ServiceHealth h; h.service_id=ServiceId(); h.service_kind=ServiceKind(); h.status=SF02_HEALTH_HEALTHY; h.detail="fixture"; h.observed_at_utc_msc=now_utc_msc; return h; }
   virtual bool BuildSnapshot(const SF01_AnatomyEvent &event,
                              const long state_generation,
                              CSF01FeatureSnapshot &snapshot,
                              string &error)
   {
      snapshot.schema = SF01_FeatureSnapshotSchema();
      snapshot.event_id = event.event_id;
      snapshot.strategy_id = event.strategy_id;
      snapshot.snapshot_time = event.confirmation_time;
      snapshot.producer_id = ServiceId();
      snapshot.producer_version = "1.0.0";
      snapshot.source_hash = "sha256_fixture_snapshot";
      snapshot.state_generation = state_generation;
      SF01_FeatureValue feature = SF01_MakeDoubleFeature("fixture_strength", "1.0.0", 0.75,
                                                         event.known_time, event.event_id,
                                                         "sha256_fixture_feature");
      if(!snapshot.Add(feature, error)) return false;
      snapshot.snapshot_id = snapshot.DeriveId();
      return snapshot.Validate(error);
   }
};

class CSF02FixtureSink : public ISF02ResultSink
{
private:
   long m_events;
   long m_snapshots;
public:
   CSF02FixtureSink(void) { m_events=0; m_snapshots=0; }
   virtual string ServiceId(void) const { return "sf02.fixture_sink"; }
   virtual ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_RESULT_SINK; }
   virtual bool Initialize(const SF02_RuntimeConfig &config, string &error) { m_events=0; m_snapshots=0; error=""; return true; }
   virtual bool Start(string &error) { error=""; return true; }
   virtual void Stop(void) {}
   virtual void Shutdown(void) {}
   virtual SF02_ServiceHealth Health(const long now_utc_msc) const
   { SF02_ServiceHealth h; h.service_id=ServiceId(); h.service_kind=ServiceKind(); h.status=SF02_HEALTH_HEALTHY; h.detail="fixture"; h.observed_at_utc_msc=now_utc_msc; return h; }
   virtual bool WriteEvent(const SF01_AnatomyEvent &event, string &error) { m_events++; error=""; return true; }
   virtual bool WriteSnapshot(const CSF01FeatureSnapshot &snapshot, string &error) { m_snapshots++; error=""; return true; }
   virtual bool Flush(string &error) { error=""; return true; }
   long Events(void) const { return m_events; }
   long Snapshots(void) const { return m_snapshots; }
};

#endif
