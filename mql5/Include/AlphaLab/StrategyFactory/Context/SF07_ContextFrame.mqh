#ifndef __SF07_CONTEXT_FRAME_MQH__
#define __SF07_CONTEXT_FRAME_MQH__

#include "SF07_FeatureVector.mqh"

struct SF07_ContextFrame
{
   string schema;
   string frame_id;
   string event_id;
   string snapshot_id;
   string graph_hash;
   string vector_schema_hash;
   string vector_id;
   long state_generation;
   int feature_count;
   SF01_MarketTimestamp snapshot_time;
   string source_hash;
};

string SF07_ContextFrameCanonical(const SF07_ContextFrame &frame)
{
   return frame.schema + "|" + frame.event_id + "|" + frame.snapshot_id + "|" +
          frame.graph_hash + "|" + frame.vector_schema_hash + "|" + frame.vector_id + "|" +
          IntegerToString(frame.state_generation) + "|" + IntegerToString(frame.feature_count) + "|" +
          IntegerToString(frame.snapshot_time.utc_epoch_milliseconds) + "|" + frame.source_hash;
}

string SF07_DeriveContextFrameId(const SF07_ContextFrame &frame)
{
   return SF01_StableId("ctx", SF07_ContextFrameCanonical(frame));
}

bool SF07_ValidateContextFrame(const SF07_ContextFrame &frame, string &error)
{
   if(frame.schema != "alpha_lab.strategy_factory/context_frame@1.0.0")
   { error = "unsupported context frame schema"; return false; }
   if(!SF01_IsSafeIdentifier(frame.event_id, 128) || !SF01_IsSafeIdentifier(frame.snapshot_id, 128) ||
      !SF01_IsSafeIdentifier(frame.graph_hash, 128) || !SF01_IsSafeIdentifier(frame.vector_schema_hash, 128) ||
      !SF01_IsSafeIdentifier(frame.vector_id, 128) || !SF01_IsSafeIdentifier(frame.source_hash, 128))
   { error = "invalid context frame identity"; return false; }
   if(frame.state_generation < 0 || frame.feature_count < 0)
   { error = "invalid context frame counters"; return false; }
   if(!SF01_ValidateTimestamp(frame.snapshot_time, error)) return false;
   const string expected = SF07_DeriveContextFrameId(frame);
   if(frame.frame_id != "" && frame.frame_id != expected)
   { error = "context frame id mismatch"; return false; }
   error = "";
   return true;
}

#endif
