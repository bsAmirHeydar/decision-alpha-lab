#ifndef __FP_FLAG_BODY_AUDIT_MQH__
#define __FP_FLAG_BODY_AUDIT_MQH__
#property strict

#include "FP_FlagBodyRules.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 05 / Flag Body Audit
// ----------------------------------------------------------------------------
// Structured evidence for Origin -> Leg1 -> Waist -> Leg2 construction.
// Renderer output is intentionally not involved.
// ============================================================================

struct FP_FlagBodyBuildReport
{
   int    scale_L;
   int    node_count;
   int    direction;
   int    level;

   int    body_attempts;
   int    origin_kind_mismatch;
   int    invalid_origin_pos;
   int    no_leg1;
   int    no_waist;
   int    no_leg2;
   int    probable_child_legs;

   int    leg1_candidates;
   int    leg1_extensions;
   int    waist_candidates;
   int    waist_deepenings;
   int    waist_equal_origin_touches;
   int    origin_break_invalidations;
   int    leg2_equal_touches;
   int    leg2_strict_breaks;

   int    body_complete;
   int    body_invalid;
   int    body_live_leg;
   int    body_live_correction;
   int    body_extended;
   int    pre_internal_extensions_absorbed;
   int    max_extension_count;

   int    first_origin_anchor;
   int    last_origin_anchor;
   int    last_scan_end_pos;
   string first_reason;
   string last_reason;
};

void FP_ResetFlagBodyBuildReport(FP_FlagBodyBuildReport &r)
{
   r.scale_L = 0;
   r.node_count = 0;
   r.direction = FP_DIR_NONE;
   r.level = FP_LEVEL_NONE;

   r.body_attempts = 0;
   r.origin_kind_mismatch = 0;
   r.invalid_origin_pos = 0;
   r.no_leg1 = 0;
   r.no_waist = 0;
   r.no_leg2 = 0;
   r.probable_child_legs = 0;

   r.leg1_candidates = 0;
   r.leg1_extensions = 0;
   r.waist_candidates = 0;
   r.waist_deepenings = 0;
   r.waist_equal_origin_touches = 0;
   r.origin_break_invalidations = 0;
   r.leg2_equal_touches = 0;
   r.leg2_strict_breaks = 0;

   r.body_complete = 0;
   r.body_invalid = 0;
   r.body_live_leg = 0;
   r.body_live_correction = 0;
   r.body_extended = 0;
   r.pre_internal_extensions_absorbed = 0;
   r.max_extension_count = 0;

   r.first_origin_anchor = -1;
   r.last_origin_anchor = -1;
   r.last_scan_end_pos = -1;
   r.first_reason = "";
   r.last_reason = "";
}

void FP_SeedFlagBodyBuildReport(FP_FlagBodyBuildReport &r, const int scale_L, const int node_count, const int direction, const int level)
{
   if(r.scale_L <= 0) r.scale_L = scale_L;
   r.node_count = node_count;
   if(r.direction == FP_DIR_NONE) r.direction = direction;
   if(r.level == FP_LEVEL_NONE) r.level = level;
}

void FP_FlagBodyReportReason(FP_FlagBodyBuildReport &r, const FP_Node &origin, const string reason, const int scan_end_pos)
{
   if(r.first_origin_anchor < 0 && origin.index_anchor >= 0) r.first_origin_anchor = origin.index_anchor;
   if(origin.index_anchor >= 0) r.last_origin_anchor = origin.index_anchor;
   r.last_scan_end_pos = scan_end_pos;
   if(r.first_reason == "") r.first_reason = reason;
   r.last_reason = reason;
}

void FP_MergeFlagBodyBuildReport(FP_FlagBodyBuildReport &dst, const FP_FlagBodyBuildReport &src)
{
   if(src.scale_L > 0) dst.scale_L = src.scale_L;
   if(src.node_count > 0) dst.node_count = src.node_count;
   if(dst.direction == FP_DIR_NONE) dst.direction = src.direction;
   if(dst.level == FP_LEVEL_NONE) dst.level = src.level;

   dst.body_attempts += src.body_attempts;
   dst.origin_kind_mismatch += src.origin_kind_mismatch;
   dst.invalid_origin_pos += src.invalid_origin_pos;
   dst.no_leg1 += src.no_leg1;
   dst.no_waist += src.no_waist;
   dst.no_leg2 += src.no_leg2;
   dst.probable_child_legs += src.probable_child_legs;

   dst.leg1_candidates += src.leg1_candidates;
   dst.leg1_extensions += src.leg1_extensions;
   dst.waist_candidates += src.waist_candidates;
   dst.waist_deepenings += src.waist_deepenings;
   dst.waist_equal_origin_touches += src.waist_equal_origin_touches;
   dst.origin_break_invalidations += src.origin_break_invalidations;
   dst.leg2_equal_touches += src.leg2_equal_touches;
   dst.leg2_strict_breaks += src.leg2_strict_breaks;

   dst.body_complete += src.body_complete;
   dst.body_invalid += src.body_invalid;
   dst.body_live_leg += src.body_live_leg;
   dst.body_live_correction += src.body_live_correction;
   dst.body_extended += src.body_extended;
   dst.pre_internal_extensions_absorbed += src.pre_internal_extensions_absorbed;
   dst.max_extension_count = MathMax(dst.max_extension_count, src.max_extension_count);

   if(dst.first_origin_anchor < 0) dst.first_origin_anchor = src.first_origin_anchor;
   if(src.last_origin_anchor >= 0) dst.last_origin_anchor = src.last_origin_anchor;
   if(src.last_scan_end_pos >= 0) dst.last_scan_end_pos = src.last_scan_end_pos;
   if(dst.first_reason == "") dst.first_reason = src.first_reason;
   if(src.last_reason != "") dst.last_reason = src.last_reason;
}

void FP_PrintFlagBodyBuildReport(const string tag, const FP_FlagBodyBuildReport &r)
{
   Print(tag,
         " scale_L=", r.scale_L,
         " nodes=", r.node_count,
         " dir=", FP_DirectionName(r.direction),
         " level=", FP_LevelName(r.level),
         " attempts=", r.body_attempts,
         " complete=", r.body_complete,
         " invalid=", r.body_invalid,
         " live_leg=", r.body_live_leg,
         " live_correction=", r.body_live_correction,
         " probable_child_legs=", r.probable_child_legs,
         " leg1_candidates=", r.leg1_candidates,
         " leg1_extensions=", r.leg1_extensions,
         " waist_candidates=", r.waist_candidates,
         " waist_deepenings=", r.waist_deepenings,
         " waist_equal_origin=", r.waist_equal_origin_touches,
         " origin_break_invalidations=", r.origin_break_invalidations,
         " leg2_equal_touches=", r.leg2_equal_touches,
         " leg2_strict_breaks=", r.leg2_strict_breaks,
         " pre_internal_extensions_absorbed=", r.pre_internal_extensions_absorbed,
         " body_extended=", r.body_extended,
         " max_extension_count=", r.max_extension_count,
         " no_leg1=", r.no_leg1,
         " no_waist=", r.no_waist,
         " no_leg2=", r.no_leg2,
         " first_origin=", r.first_origin_anchor,
         " last_origin=", r.last_origin_anchor,
         " last_scan_end=", r.last_scan_end_pos,
         " first_reason=", r.first_reason,
         " last_reason=", r.last_reason);
}

void FP_PrintBodyEventSamples(const string tag, const FP_FlagEvent &events[], const int count, const int max_samples)
{
   int n = MathMin(count, MathMax(0, max_samples));
   for(int i=0; i<n; i++)
   {
      FP_FlagEvent e = events[i];
      Print(tag,
            " sample=", i,
            " event=", e.event_id,
            " seq=", e.sequence_id,
            " level=", FP_LevelName(e.level),
            " dir=", FP_DirectionName(e.direction),
            " L=", e.scale_L,
            " body_status=", FP_BodyStatusName(e.body_status),
            " body_ext=", e.leg2_extension_count,
            " status=", FP_StatusName(e.status),
            " O=", FP_BodyNodeKey(e.origin),
            " A=", FP_BodyNodeKey(e.leg1),
            " W=", FP_BodyNodeKey(e.waist),
            " B=", FP_BodyNodeKey(e.leg2),
            " body_id=", e.body_id,
            " body_reason=", e.body_reason,
            " reason=", e.reason);
   }
}

#endif // __FP_FLAG_BODY_AUDIT_MQH__
