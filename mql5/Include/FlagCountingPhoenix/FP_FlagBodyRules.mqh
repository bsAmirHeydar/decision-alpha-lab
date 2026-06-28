#ifndef __FP_FLAG_BODY_RULES_MQH__
#define __FP_FLAG_BODY_RULES_MQH__
#property strict

#include "FP_HookEngine.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 05 / Flag Body Rules
// ----------------------------------------------------------------------------
// Pure body-construction predicates.  This file owns no sequence lifecycle and
// does not draw anything.  It only answers whether a node can play O/A/W/B.
// ============================================================================

bool FP_NodeIsOriginKind(const FP_Node &n, const int direction)
{
   return (n.kind == FP_OriginKindForDirection(direction));
}

bool FP_NodeIsLegKind(const FP_Node &n, const int direction)
{
   return (n.kind == FP_OppositeKind(FP_OriginKindForDirection(direction)));
}

bool FP_WaistStaysInsideOrigin(const FP_Node &waist, const FP_Node &origin, const int direction, const double eps)
{
   if(direction == FP_DIR_BULLISH) return !FP_BreaksBelow(waist.price, origin.price, eps);
   if(direction == FP_DIR_BEARISH) return !FP_BreaksAbove(waist.price, origin.price, eps);
   return false;
}

bool FP_WaistEqualsOrigin(const FP_Node &waist, const FP_Node &origin, const double eps)
{
   return FP_AlmostEqual(waist.price, origin.price, eps);
}

bool FP_BodyOriginInvalidatedByNode(const FP_Node &n, const FP_Node &origin, const int direction, const double eps)
{
   if(direction == FP_DIR_BULLISH) return (n.kind == FP_NODE_LOW && FP_BreaksBelow(n.price, origin.price, eps));
   if(direction == FP_DIR_BEARISH) return (n.kind == FP_NODE_HIGH && FP_BreaksAbove(n.price, origin.price, eps));
   return false;
}

bool FP_LegBreaksLeg1(const FP_Node &n, const FP_Node &leg1, const int direction, const double eps)
{
   if(direction == FP_DIR_BULLISH) return (n.kind == FP_NODE_HIGH && FP_BreaksAbove(n.price, leg1.price, eps));
   if(direction == FP_DIR_BEARISH) return (n.kind == FP_NODE_LOW && FP_BreaksBelow(n.price, leg1.price, eps));
   return false;
}

bool FP_LegEqualsLeg1(const FP_Node &n, const FP_Node &leg1, const double eps)
{
   return FP_AlmostEqual(n.price, leg1.price, eps);
}

bool FP_LegExtendsLeg1(const FP_Node &n, const FP_Node &leg1, const int direction, const double eps)
{
   return FP_LegBreaksLeg1(n, leg1, direction, eps);
}

double FP_FlagSize(const FP_Node &origin, const FP_Node &leg2)
{
   return MathAbs(leg2.price - origin.price);
}

string FP_BodyNodeKey(const FP_Node &n)
{
   if(n.id < 0) return "none";
   return FP_NodeKindName(n.kind) + "#" + IntegerToString(n.id) +
          "@" + IntegerToString(n.index_anchor) +
          ":" + DoubleToString(n.price, _Digits) +
          ":L" + IntegerToString(n.L);
}

string FP_BodyId(const FP_FlagEvent &e)
{
   return "BD:lv=" + FP_LevelName(e.level) +
          "|dir=" + FP_DirectionName(e.direction) +
          "|L=" + IntegerToString(e.scale_L) +
          "|O=" + FP_BodyNodeKey(e.origin) +
          "|A=" + FP_BodyNodeKey(e.leg1) +
          "|W=" + FP_BodyNodeKey(e.waist) +
          "|B=" + FP_BodyNodeKey(e.leg2);
}

void FP_FinalizeBodyIdentity(FP_FlagEvent &event, const int body_status, const string body_reason)
{
   event.body_status = body_status;
   event.body_reason = body_reason;
   event.body_id = FP_BodyId(event);
}

#endif // __FP_FLAG_BODY_RULES_MQH__
