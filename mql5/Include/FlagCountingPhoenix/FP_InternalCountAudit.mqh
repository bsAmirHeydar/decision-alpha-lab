#ifndef __FP_INTERNAL_COUNT_AUDIT_MQH__
#define __FP_INTERNAL_COUNT_AUDIT_MQH__
#property strict

#include "FP_InternalCountRules.mqh"

// ============================================================================
// Phoenix Level 06 - Internal Count Audit
// ----------------------------------------------------------------------------
// Structured reporting for post-flag internal count.  This is intentionally
// independent from main-chart rendering.
// ============================================================================

struct FP_InternalCountBuildReport
{
   int scale_L;
   int node_count;
   int bodies_seen;
   int f1_bodies;
   int f2_bodies;
   int f3_bodies;
   int packs_attempted;
   int packs_emitted;
   int count0;
   int count1;
   int count2;
   int count3;
   int count4;
   int valid12;
   int confirm_ready;
   int confirmed_breaks;
   int invalidations;
   int f1_middle_rejected;
   int missing_middle_rejected;
   int non_deeper_rejected;
   int pre_internal_extensions_seen;
   int pre_internal_extensions_absorbed;
   int max_extension_count;
   int max_count_seen;
   int f3_body_completed_without_pack;
};

void FP_ResetInternalCountBuildReport(FP_InternalCountBuildReport &r)
{
   r.scale_L = 0;
   r.node_count = 0;
   r.bodies_seen = 0;
   r.f1_bodies = 0;
   r.f2_bodies = 0;
   r.f3_bodies = 0;
   r.packs_attempted = 0;
   r.packs_emitted = 0;
   r.count0 = 0;
   r.count1 = 0;
   r.count2 = 0;
   r.count3 = 0;
   r.count4 = 0;
   r.valid12 = 0;
   r.confirm_ready = 0;
   r.confirmed_breaks = 0;
   r.invalidations = 0;
   r.f1_middle_rejected = 0;
   r.missing_middle_rejected = 0;
   r.non_deeper_rejected = 0;
   r.pre_internal_extensions_seen = 0;
   r.pre_internal_extensions_absorbed = 0;
   r.max_extension_count = 0;
   r.max_count_seen = 0;
   r.f3_body_completed_without_pack = 0;
}

void FP_SeedInternalCountBuildReport(FP_InternalCountBuildReport &r, const int scale_L, const int node_count)
{
   r.scale_L = scale_L;
   r.node_count = node_count;
}

void FP_CountInternalPackInReport(const FP_InternalPack &p, FP_InternalCountBuildReport &r)
{
   r.packs_emitted++;
   r.max_count_seen = MathMax(r.max_count_seen, p.count);
   if(p.count <= 0) r.count0++;
   else if(p.count == 1) r.count1++;
   else if(p.count == 2) r.count2++;
   else if(p.count == 3) r.count3++;
   else r.count4++;
   if(p.valid12 || p.has_valid12) r.valid12++;
   if((p.valid12 || p.has_valid12) && p.confirm_pos >= 0) r.confirm_ready++;
   if(p.confirm_pos >= 0) r.confirmed_breaks++;
   if(p.invalid_pos >= 0) r.invalidations++;
   if(p.has_pre_internal_leg2_extension) r.pre_internal_extensions_seen++;
}

void FP_PrintInternalCountBuildReport(const string tag, const FP_InternalCountBuildReport &r)
{
   Print(tag,
         " scale_L=", r.scale_L,
         " nodes=", r.node_count,
         " bodies=", r.bodies_seen,
         " f1_bodies=", r.f1_bodies,
         " f2_bodies=", r.f2_bodies,
         " f3_bodies=", r.f3_bodies,
         " attempts=", r.packs_attempted,
         " packs=", r.packs_emitted,
         " count0=", r.count0,
         " count1=", r.count1,
         " count2=", r.count2,
         " count3=", r.count3,
         " count4=", r.count4,
         " valid12=", r.valid12,
         " confirm_ready=", r.confirm_ready,
         " confirms=", r.confirmed_breaks,
         " invalidations=", r.invalidations,
         " pre_ext_seen=", r.pre_internal_extensions_seen,
         " pre_ext_absorbed=", r.pre_internal_extensions_absorbed,
         " f1_mid_rejected=", r.f1_middle_rejected,
         " missing_mid_rejected=", r.missing_middle_rejected,
         " non_deeper_rejected=", r.non_deeper_rejected,
         " max_ext=", r.max_extension_count,
         " max_count=", r.max_count_seen,
         " f3_body_only=", r.f3_body_completed_without_pack);
}

string FP_InternalNodeShort(const FP_Node &n)
{
   if(n.id < 0) return "none";
   return FP_NodeKindName(n.kind) + "#" + IntegerToString(n.id) +
          "@" + IntegerToString(n.index_anchor) +
          ":" + DoubleToString(n.price, _Digits);
}

void FP_PrintInternalPackSample(const string tag, const FP_FlagEvent &e)
{
   FP_InternalPack p = e.internal_pack;
   Print(tag,
         " event=", e.event_id,
         " seq=", e.sequence_id,
         " level=", FP_LevelName(e.level),
         " dir=", FP_DirectionName(e.direction),
         " L=", e.scale_L,
         " status=", FP_StatusName(e.status),
         " body_id=", e.body_id,
         " internal_pack_id=", p.internal_pack_id,
         " branch=", p.branch_id_text,
         " count=", p.count,
         " valid12=", FP_BoolName(p.valid12 || p.has_valid12),
         " first12=", p.first_valid12_pos,
         " confirm_pos=", p.confirm_pos,
         " invalid_pos=", p.invalid_pos,
         " scan=", p.scan_start_pos, "-", p.scan_end_pos,
         " n1=", FP_InternalNodeShort(p.n1),
         " n2=", FP_InternalNodeShort(p.n2),
         " n3=", FP_InternalNodeShort(p.n3),
         " n4=", FP_InternalNodeShort(p.n4),
         " mid12=", FP_InternalNodeShort(p.mid12),
         " mid_breaks_leg2=", FP_BoolName(p.middle_opposite_breaks_leg2),
         " pre_ext=", FP_InternalNodeShort(p.pre_internal_leg2_extension_node),
         " reason=", p.reason);
}

void FP_PrintInternalPackSamples(const string tag,
                                 const FP_FlagEvent &events[],
                                 const int event_count,
                                 const int limit)
{
   int printed = 0;
   int max_print = (limit <= 0 ? 6 : limit);
   for(int i=0; i<event_count && printed<max_print; i++)
   {
      if(events[i].internal_pack.internal_pack_id == "" && events[i].internal_pack.count <= 0) continue;
      FP_PrintInternalPackSample(tag, events[i]);
      printed++;
   }
}

#endif // __FP_INTERNAL_COUNT_AUDIT_MQH__
