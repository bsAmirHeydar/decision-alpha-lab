#ifndef __SF15_PREPROCESSING_MQH__
#define __SF15_PREPROCESSING_MQH__
#include "SF15_Hashing.mqh"
class CSF15Preprocessor
  {
private:
   string m_feature_schema_hash,m_transform_hash,m_manifest_hash; double m_impute[],m_mean[],m_scale[]; bool m_ready;
public:
   CSF15Preprocessor(){m_ready=false;}
   bool Configure(const string feature_schema_hash,const string transform_hash,const string manifest_hash,const double &impute[],const double &means[],const double &scales[],string &error)
     {
      int n=ArraySize(impute); if(feature_schema_hash==""||transform_hash==""||manifest_hash==""||n<1||ArraySize(means)!=n||ArraySize(scales)!=n){error="preprocessing contract mismatch";m_ready=false;return false;}
      ArrayResize(m_impute,n);ArrayResize(m_mean,n);ArrayResize(m_scale,n);
      for(int i=0;i<n;i++){if(!SF15_IsFinite(impute[i])||!SF15_IsFinite(means[i])||!SF15_IsFinite(scales[i])||scales[i]<=0.0){error="invalid preprocessing value";m_ready=false;return false;}m_impute[i]=impute[i];m_mean[i]=means[i];m_scale[i]=scales[i];}
      m_feature_schema_hash=feature_schema_hash;m_transform_hash=transform_hash;m_manifest_hash=manifest_hash;m_ready=true;error="";return true;
     }
   bool Transform(const double &values[],const bool &missing[],double &output[],string &error)const
     {
      int n=ArraySize(m_impute);if(!m_ready||ArraySize(values)!=n||ArraySize(missing)!=n){error="preprocessing input width mismatch";return false;}ArrayResize(output,n);
      for(int i=0;i<n;i++){double source=missing[i]?m_impute[i]:values[i];if(!missing[i]&&!SF15_IsFinite(source)){error="non-finite observed feature";return false;}output[i]=(source-m_mean[i])/m_scale[i];if(!SF15_IsFinite(output[i])){error="non-finite transformed feature";return false;}}
      error="";return true;
     }
   bool Ready()const{return m_ready;}int Width()const{return ArraySize(m_impute);}string TransformHash()const{return m_transform_hash;}string ManifestHash()const{return m_manifest_hash;}
  };
#endif
