#ifndef __SF13_DATASET_ASSEMBLER_MQH__
#define __SF13_DATASET_ASSEMBLER_MQH__
#include "SF13_PredictionRecord.mqh"
class CSF13DatasetAssembler
{
private: SF13_DatasetRow m_rows[];int m_maximum_rows;
public:
   CSF13DatasetAssembler(void){m_maximum_rows=100000;ArrayResize(m_rows,0);}
   void SetMaximumRows(const int value){m_maximum_rows=MathMax(1,value);}
   int Count(void)const{return ArraySize(m_rows);}
   bool Add(const SF13_DatasetRow &row,string &error)
   {
      if(!SF13_ValidateDatasetRow(row,error))return false;if(ArraySize(m_rows)>=m_maximum_rows){error="dataset row bound exceeded";return false;}
      for(int i=0;i<ArraySize(m_rows);i++){if(m_rows[i].row_id==row.row_id){error="duplicate dataset row";return false;}if(m_rows[i].fold_id==row.fold_id&&m_rows[i].cluster_id==row.cluster_id&&m_rows[i].role!=row.role){error="cluster crosses fold role";return false;}}
      int n=ArraySize(m_rows);ArrayResize(m_rows,n+1);m_rows[n]=row;error="";return true;
   }
   bool Get(const int index,SF13_DatasetRow &row)const{if(index<0||index>=ArraySize(m_rows))return false;row=m_rows[index];return true;}
   bool BuildManifest(const string dataset_id,const string dataset_version,const string strategy_id,const string source_run_id,const string source_manifest_hash,const string source_artifact_hash,const string validation_plan_hash,const string feature_schema_hash,const string label_contract_hash,const long created_at_utc_msc,const string code_revision,SF13_DatasetManifest &manifest,string &error)const
   {
      manifest.dataset_id=dataset_id;manifest.dataset_version=dataset_version;manifest.strategy_id=strategy_id;manifest.source_run_id=source_run_id;manifest.source_manifest_hash=source_manifest_hash;manifest.source_artifact_hash=source_artifact_hash;manifest.validation_plan_hash=validation_plan_hash;manifest.feature_schema_hash=feature_schema_hash;manifest.label_contract_hash=label_contract_hash;manifest.row_count=ArraySize(m_rows);manifest.train_count=0;manifest.validation_count=0;manifest.test_count=0;manifest.excluded_count=0;string rowset="";
      for(int i=0;i<ArraySize(m_rows);i++){if(m_rows[i].role==SF13_ROLE_TRAIN)manifest.train_count++;else if(m_rows[i].role==SF13_ROLE_VALIDATION)manifest.validation_count++;else if(m_rows[i].role==SF13_ROLE_TEST)manifest.test_count++;else manifest.excluded_count++;rowset+=m_rows[i].row_hash+"|";}
      manifest.rowset_hash=SF01_StableId("rowset",rowset);manifest.created_at_utc_msc=created_at_utc_msc;manifest.code_revision=code_revision;manifest.dataset_hash=SF13_DeriveDatasetHash(manifest);return SF13_ValidateDatasetManifest(manifest,error);
   }
};
#endif
