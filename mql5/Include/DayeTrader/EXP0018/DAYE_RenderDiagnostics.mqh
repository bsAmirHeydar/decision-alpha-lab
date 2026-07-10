#ifndef __EXP0018_DAYE_RENDER_DIAGNOSTICS_MQH__
#define __EXP0018_DAYE_RENDER_DIAGNOSTICS_MQH__

#include <DayeTrader/EXP0018/DAYE_RenderEvents.mqh>

string DAYE_FormatRenderProjection(const DAYE_RenderProjection &p)
{
   return StringFormat("P08 projection=%s use=%s rel=%s side=%s hunter=%s chart=%I64d tf=%s status=%s object=%s reason=%s",
                       p.projection_id,p.use_id,p.source_alias,DAYE_HuntSideToString(p.side),p.hunter_canonical_symbol,
                       p.target_chart_id,EnumToString(p.target_chart_timeframe),DAYE_RenderProjectionStatusToString(p.status),
                       p.line_object_name,p.reason_code);
}

string DAYE_FormatRenderSummary(const DAYE_RenderStoreSummary &s)
{
   return StringFormat("EXP0018 P08 status=%s ready=%s uses=%d accepted=%d periods=%d charts=%d projections=%d created=%d verified=%d repaired=%d waiting=%d missing_period=%d missing_extreme=%d failed=%d major_labels=%d minor_lines=%d reason=%s",
                       DAYE_RenderEngineStatusToString(s.status),s.is_ready?"true":"false",s.source_use_count,
                       s.accepted_source_use_count,s.source_period_count,s.open_hunter_chart_count,s.projection_count,
                       s.created_count,s.verified_count,s.repaired_count,s.waiting_chart_count,
                       s.source_period_missing_count,s.source_extreme_missing_count,s.failed_object_count,
                       s.major_label_count,s.minor_unlabeled_count,s.reason_code);
}

string DAYE_FormatRenderEvent(const DAYE_RenderEvent &e)
{
   return StringFormat("EXP0018 P08 event=%s projection=%s use=%s chart=%I64d object=%s from=%s to=%s reason=%s",
                       DAYE_RenderEventTypeToString(e.event_type),e.projection_id,e.use_id,e.target_chart_id,e.object_name,
                       DAYE_RenderProjectionStatusToString(e.from_status),DAYE_RenderProjectionStatusToString(e.to_status),e.reason_code);
}

#endif
