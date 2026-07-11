#ifndef __SF15_FEATURE_ORDER_MQH__
#define __SF15_FEATURE_ORDER_MQH__
struct SF15_FeatureBinding { string feature_id; string feature_version; int ordinal; string value_type; bool required; };
class CSF15FeatureOrder
  {
private:
   string m_feature_schema_hash,m_order_hash; SF15_FeatureBinding m_items[];
public:
   bool Configure(const string schema_hash,const string order_hash,const SF15_FeatureBinding &items[],string &error)
     {
      if(schema_hash=="" || order_hash=="" || ArraySize(items)<1){error="empty feature-order contract";return false;}
      ArrayResize(m_items,ArraySize(items));
      for(int i=0;i<ArraySize(items);i++)
        {
         if(items[i].feature_id=="" || items[i].feature_version=="" || items[i].ordinal!=i || items[i].value_type!="float32") {error="feature-order mismatch at ordinal "+IntegerToString(i);return false;}
         m_items[i]=items[i];
        }
      m_feature_schema_hash=schema_hash;m_order_hash=order_hash;error="";return true;
     }
   int Width()const{return ArraySize(m_items);} string FeatureSchemaHash()const{return m_feature_schema_hash;} string OrderHash()const{return m_order_hash;}
   bool Matches(const string schema_hash,const string order_hash,const int width)const{return schema_hash==m_feature_schema_hash && order_hash==m_order_hash && width==ArraySize(m_items);}
  };
#endif
