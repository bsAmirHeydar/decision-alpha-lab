#ifndef __UCEI10_CATALOG_MQH__
#define __UCEI10_CATALOG_MQH__

#include "UCEI10_AlgorithmDescriptor.mqh"

class CUCEI10Catalog
  {
public:
   static int Count()
     {
      return 17;
     }

   static int NativeCount()
     {
      return 10;
     }

   static bool Get(const int index,UCEI10_AlgorithmDescriptor &out)
     {
      string ids[]=
        {
         "causal_temporal_conv_ridge",
         "compact_gru_adapter",
         "small_transformer_adapter",
         "deterministic_chart_raster_conv",
         "compact_image_cnn_adapter",
         "deterministic_graph_message_passing",
         "graph_neural_network_adapter",
         "deterministic_regime_kmeans",
         "cusum_change_point",
         "distance_novelty",
         "gaussian_hmm_adapter",
         "autoencoder_novelty_adapter",
         "late_weighted_fusion",
         "stacked_linear_fusion",
         "gated_cross_attention_adapter",
         "linear_teacher_student_distillation",
         "symmetric_int8_quantization"
        };
      int families[]={0,0,0,1,1,2,2,3,3,3,3,3,4,4,4,5,5};
      string formulations[]=
        {
         "causal_fixed_tcn_plus_ridge",
         "masked_compact_gru",
         "causal_small_transformer",
         "deterministic_raster_fixed_conv_plus_ridge",
         "small_causal_chart_cnn",
         "fixed_message_passing_plus_ridge",
         "graph_neural_network",
         "deterministic_kmeans",
         "two_sided_cusum",
         "standardized_distance",
         "gaussian_hmm",
         "compact_autoencoder",
         "validation_weighted_late_fusion",
         "oof_only_stacking",
         "gated_cross_attention",
         "teacher_student_linear_distillation",
         "symmetric_int8"
        };
      string views[]=
        {
         "sequence","sequence","sequence,event_set","image","image",
         "graph","graph","tabular,multi_view","sequence,tabular",
         "tabular,multi_view","sequence,tabular","tabular,sequence,image",
         "multi_view","multi_view","multi_view","tabular,multi_view",
         "sequence,image,graph,multi_view"
        };
      string tasks[]=
        {
         "binary_classification,regression,multi_task",
         "binary_classification,regression,multi_task",
         "binary_classification,regression,ranking,multi_task",
         "binary_classification,regression",
         "binary_classification,regression",
         "binary_classification,regression",
         "binary_classification,regression,ranking",
         "regime_gating,novelty",
         "novelty,regime_gating",
         "novelty,regime_gating",
         "regime_gating",
         "novelty",
         "binary_classification,regression,ranking",
         "binary_classification,regression",
         "binary_classification,regression,multi_task",
         "regression,binary_classification",
         "runtime_compression"
        };
      bool native_flags[]={true,false,false,true,false,true,false,true,true,true,false,false,true,true,false,true,true};
      if(index<0 || index>=ArraySize(ids))
         return false;

      out.algorithm_id=ids[index];
      out.algorithm_version="1.0.0";
      out.family=(UCEI10_DEEP_FAMILY)families[index];
      out.formulation=formulations[index];
      out.native_algorithm=native_flags[index];
      out.determinism=out.native_algorithm ? "bit_exact" : "numeric_tolerance";
      out.dependency_profile=out.native_algorithm ? "" : ((index==6) ? "ucee-graph" : "ucee-deep");
      out.view_kinds=views[index];
      out.tasks=tasks[index];
      out.export_paths=out.native_algorithm ? "native_json,distilled_mql5" : "onnx";
      out.limitations="research_only; admission, ablation, export, and qualification gates required";
      return out.Valid();
     }
  };

#endif
