#ifndef __UCEI10_VIEW_CONTRACTS_MQH__
#define __UCEI10_VIEW_CONTRACTS_MQH__

struct UCEI10_ViewTensorSpec
  {
   string view_id;
   string view_version;
   string view_kind;
   int    shape[];
   string layout;
   string feature_order;
   string context_observation_id;
   long   known_time_ms;
   string descriptor_hash;
   string payload_hash;
   bool   mask_required;
   bool   runtime_exportable;

   int Width() const
     {
      if(ArraySize(shape)<1)
         return 0;
      int width=1;
      for(int index=0; index<ArraySize(shape); index++)
        {
         if(shape[index]<1)
            return 0;
         width*=shape[index];
        }
      return width;
     }

   bool Valid() const
     {
      return view_id!="" && view_version!="" && view_kind!="" &&
             layout!="" && context_observation_id!="" &&
             known_time_ms>=0 && Width()>0;
     }
  };

struct UCEI10_SequenceWindowSpec
  {
   string sequence_id;
   string version;
   int    steps;
   int    channels;
   string layout;
   double pad_value;
   bool   require_strict_time;

   bool Valid() const
     {
      return sequence_id!="" && version!="" && steps>0 && channels>0 &&
             (layout=="time_major" || layout=="feature_major") &&
             MathIsValidNumber(pad_value);
     }
  };

struct UCEI10_SequenceArtifact
  {
   string artifact_id;
   string spec_hash;
   string context_observation_id;
   long   known_time_ms;
   int    step_count;
   int    channel_count;
   int    value_count;
   int    mask_count;
   string source_hash;
   string evidence_hash;

   bool Valid() const
     {
      return artifact_id!="" && spec_hash!="" && context_observation_id!="" &&
             known_time_ms>=0 && step_count>0 && channel_count>0 &&
             value_count==step_count*channel_count &&
             mask_count==value_count && source_hash!="" && evidence_hash!="";
     }
  };

struct UCEI10_RasterArtifact
  {
   string artifact_id;
   string spec_hash;
   string context_observation_id;
   long   known_time_ms;
   int    channels;
   int    height;
   int    width;
   int    value_count;
   string source_hash;
   string evidence_hash;

   bool Valid() const
     {
      return artifact_id!="" && spec_hash!="" && context_observation_id!="" &&
             channels>0 && height>0 && width>0 && known_time_ms>=0 &&
             value_count==channels*height*width &&
             source_hash!="" && evidence_hash!="";
     }
  };

struct UCEI10_PixelAuditReport
  {
   string report_id;
   string artifact_a_hash;
   string artifact_b_hash;
   double max_abs_difference;
   int    changed_pixel_count;
   bool   prefix_invariant;
   string evidence_hash;

   bool Valid() const
     {
      return report_id!="" && artifact_a_hash!="" && artifact_b_hash!="" &&
             MathIsValidNumber(max_abs_difference) && max_abs_difference>=0.0 &&
             changed_pixel_count>=0 && evidence_hash!="";
     }
  };

struct UCEI10_GraphArtifact
  {
   string artifact_id;
   string spec_hash;
   string context_observation_id;
   long   known_time_ms;
   string topology_hash;
   string evidence_hash;
   int    node_count;
   int    edge_count;
   int    node_feature_count;

   bool Valid() const
     {
      return artifact_id!="" && spec_hash!="" && context_observation_id!="" &&
             node_count>0 && edge_count>=0 && node_feature_count>0 &&
             known_time_ms>=0 && topology_hash!="" && evidence_hash!="";
     }
  };

#endif
