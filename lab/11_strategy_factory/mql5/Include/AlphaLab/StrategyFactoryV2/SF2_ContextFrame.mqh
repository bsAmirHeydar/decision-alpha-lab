#ifndef __ALPHA_LAB_SF2_CONTEXT_FRAME_MQH__
#define __ALPHA_LAB_SF2_CONTEXT_FRAME_MQH__

#include "SF2_Contracts.mqh"

class SF2_ContextFrame
  {
private:
   SF2_FeatureValue m_values[];
   int              m_count;
   datetime         m_snapshot_time_utc;
   string           m_schema_version;

public:
                     SF2_ContextFrame(void)
     {
      m_count=0;
      m_snapshot_time_utc=0;
      m_schema_version="2.0.0";
      ArrayResize(m_values,0);
     }

   void              Reset(const datetime snapshot_time_utc)
     {
      m_count=0;
      m_snapshot_time_utc=snapshot_time_utc;
      ArrayResize(m_values,0);
     }

   bool              Put(const string name,
                         const double value,
                         const datetime known_time_utc,
                         const string source_id,
                         const string version)
     {
      if(name=="" || known_time_utc>m_snapshot_time_utc)
         return(false);
      for(int i=0;i<m_count;i++)
        {
         if(m_values[i].name==name)
           {
            m_values[i].numeric_value=value;
            m_values[i].known_time_utc=known_time_utc;
            m_values[i].source_id=source_id;
            m_values[i].version=version;
            m_values[i].available=true;
            return(true);
           }
        }
      ArrayResize(m_values,m_count+1);
      m_values[m_count].name=name;
      m_values[m_count].numeric_value=value;
      m_values[m_count].known_time_utc=known_time_utc;
      m_values[m_count].source_id=source_id;
      m_values[m_count].version=version;
      m_values[m_count].available=true;
      m_count++;
      return(true);
     }

   bool              TryGet(const string name,double &value) const
     {
      for(int i=0;i<m_count;i++)
        {
         if(m_values[i].name==name && m_values[i].available)
           {
            value=m_values[i].numeric_value;
            return(true);
           }
        }
      return(false);
     }

   bool              HasAll(const string &required_names[],string &missing_name) const
     {
      double unused=0.0;
      for(int i=0;i<ArraySize(required_names);i++)
        {
         if(!TryGet(required_names[i],unused))
           {
            missing_name=required_names[i];
            return(false);
           }
        }
      missing_name="";
      return(true);
     }

   int               Count(void) const { return(m_count); }
   datetime          SnapshotTime(void) const { return(m_snapshot_time_utc); }
   string            SchemaVersion(void) const { return(m_schema_version); }
  };

#endif
