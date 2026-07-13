#ifndef __FP_NDS_F2_CANONICAL_POINT2_SETUP_ADAPTER_MQH__
#define __FP_NDS_F2_CANONICAL_POINT2_SETUP_ADAPTER_MQH__
#property strict

#include "FP_NDSF2WaistTradeTypes.mqh"

// ============================================================================
// NDS F2 Canonical Point-2 Setup Adapter
// ----------------------------------------------------------------------------
// This module does not detect, rebuild, reinterpret, or mutate F1/F2/F3.
// Phoenix remains the sole authority for:
//   F2 flag body       = Origin -> Leg1 -> Waist -> Leg2
//   F2 post-flag phase = internal count / Waist-break branch
//   F2 confirmation   = favorable re-break of the original F2 flag end
//
// The adapter owns only the execution projection requested for this setup:
//   projected Point 1 = the already-existing F2 flag Waist
//   executable Point 2 = the first strict price passage beyond that Waist
//   entry order = a pending limit staged beyond the Waist before Point 2 forms
//   fixed RR reference = the original F2 flag end / Leg2
//
// A fill is therefore an anticipatory capture of the canonical Waist-break
// branch. It is not evidence that the whole F2 has confirmed. Confirmation
// remains owned by the existing Phoenix lifecycle after post-flag counting and
// the later return through the F2 flag end.
// ============================================================================

bool FP_NDSF2CanonicalBodyCanProjectPoint2(const FP_FlagEvent &f2,
                                           const FP_NDSF2WaistTradeConfig &cfg)
{
   if(f2.level != FP_LEVEL_F2) return false;
   if(f2.direction != FP_DIR_BULLISH && f2.direction != FP_DIR_BEARISH) return false;
   if(!f2.f2_parent_ready || !f2.f2_origin_found || !f2.f2_body_complete) return false;
   if(cfg.require_f2_size_gate && !f2.f2_size_gate_passed) return false;

   if(FP_NDSF2ExitModeUsesEntryTimeframeF3(cfg.exit_mode) &&
      cfg.require_canonical_f3_spawn_for_local_exit &&
      !f2.f2_size_gate_passed)
      return false;

   if(f2.status == FP_STATUS_INVALIDATED ||
      f2.f2_lifecycle_status == FP_F2_LC_INVALIDATED)
      return false;

   // Once Phoenix confirms F2, the market has already returned through the
   // original flag end. That is the fixed economic target, so a new Point-2
   // limit would be retrospective and is forbidden.
   if(f2.status == FP_STATUS_CONFIRMED ||
      f2.f2_lifecycle_status == FP_F2_LC_CONFIRMED ||
      f2.has_confirm || f2.f2_can_spawn_f3)
      return false;

   if(!f2.has_origin || !f2.has_leg1 || !f2.has_waist || !f2.has_leg2)
      return false;
   if(f2.origin.price <= 0.0 || f2.waist.price <= 0.0 || f2.leg2.price <= 0.0)
      return false;
   if(f2.pos_origin < 0 || f2.pos_leg1 < 0 || f2.pos_waist < 0 || f2.pos_leg2 < 0)
      return false;
   if(!(f2.pos_origin < f2.pos_leg1 &&
        f2.pos_leg1 < f2.pos_waist &&
        f2.pos_waist < f2.pos_leg2))
      return false;

   // The adapter accepts both body-only and post-flag states. Existing Phoenix
   // owns the internal 1/2 pack; the pending order must exist before the strict
   // Waist passage that creates the desired Waist-break Point 2.
   if(f2.status != FP_STATUS_LIVE_BODY &&
      f2.status != FP_STATUS_QUALIFIED &&
      f2.status != FP_STATUS_POST_FLAG)
      return false;

   return true;
}

// Entry must sit beyond the same epsilon used by Phoenix structural-break
// rules. A one-tick order is not enough when boundary epsilon is wider than one
// tick. The extra tick guarantees strict passage after price normalization.
double FP_NDSF2CanonicalPoint2OffsetPrice(const string symbol,
                                           const double requested_ticks,
                                           const double epsilon_points)
{
   double tick = FP_NDSHookTradeTickSize(symbol);
   if(tick <= 0.0) return 0.0;
   double user_offset = MathMax(1.0, requested_ticks) * tick;
   double canonical_offset = MathMax(0.0, FP_EpsilonPrice(epsilon_points)) + tick;
   return MathMax(user_offset, canonical_offset);
}

bool FP_NDSF2SameCanonicalBodyIdentity(const FP_FlagEvent &f2,
                                       const string body_id,
                                       const int direction,
                                       const int scale_L,
                                       const int sequence_id,
                                       const int parent_sequence_id,
                                       const int parent_event_id,
                                       const int origin_node_id,
                                       const datetime origin_time,
                                       const int waist_node_id,
                                       const datetime waist_time,
                                       const int leg2_node_id,
                                       const datetime leg2_time)
{
   if(f2.level != FP_LEVEL_F2) return false;
   if(f2.direction != direction || f2.scale_L != scale_L) return false;
   if(f2.sequence_id != sequence_id ||
      f2.parent_sequence_id != parent_sequence_id)
      return false;

   // parent_event_id is retained in the attempt record for audit/dynamic-exit
   // lineage, but event-array ordinals may be rebuilt. Stable body/node identity
   // is the pending-order ownership authority.
   if(parent_event_id < -1) return false;

   if(body_id != "" && f2.body_id != "" && f2.body_id != body_id) return false;
   if(!f2.has_origin || !f2.has_waist || !f2.has_leg2) return false;

   if(f2.origin.id != origin_node_id || f2.origin.time_anchor != origin_time) return false;
   if(f2.waist.id != waist_node_id || f2.waist.time_anchor != waist_time) return false;
   if(f2.leg2.id != leg2_node_id || f2.leg2.time_anchor != leg2_time) return false;
   return true;
}

#endif // __FP_NDS_F2_CANONICAL_POINT2_SETUP_ADAPTER_MQH__
