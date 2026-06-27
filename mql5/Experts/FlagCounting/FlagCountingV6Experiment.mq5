#property strict
#property version   "6.00"
#property description "FlagCounting V6: modular sequence-state implementation aligned with engineering contract V5."

#include "../../Include/FlagCountingV6/FC6_SequenceEngine.mqh"
#include "../../Include/FlagCountingV6/FC6_Renderer.mqh"
#include "../../Include/FlagCountingV6/FC6_Audit.mqh"

input int  InpBarsToScan = 5000;
input bool InpRedrawOnNewBarOnly = true;

input bool InpUseMultiScale = true;
input int  InpSwingL1 = 2;
input int  InpSwingL2 = 3;
input int  InpSwingL3 = 5;
input int  InpSwingL4 = 8;
input int  InpSwingL5 = 13;
input int  InpSwingL6 = 21;
input int  InpSwingL7 = 34;
input int  InpSwingL8 = 55;
input bool InpIncludePendingNodes = false;

input bool InpScanF1 = true;
input bool InpScanF2 = true;
input bool InpScanF3 = true;
input bool InpScanHooks = true;
input bool InpShowInvalidatedInAudit = false;
input bool InpKeepConfirmedF1F2AfterBoundaryHit = false;

input int    InpMaxEvents = 3000;
input int    InpMaxHooks = 3000;
input int    InpMaxRootsPerScaleDirection = 0;
input double InpBoundaryEpsilonPoints = 0.0;
input double InpF2MinParentSizeRatio = 1.0;
input double InpF3MinParentSizeRatio = 0.70;
input double InpF3Leg1LMinRatio = 0.80;
input double InpNDMinRetraceRatio = 0.50;
input bool   InpNDAllowBelowHalfCycle = false;
input bool   InpVerboseAuditLogs = false;

input string InpObjectPrefix = "DAL_FC6_";
input bool   InpCleanObjectsOnInit = true;
input bool   InpCleanObjectsOnDeinit = true;
input int    InpMaxEventsToDraw = 1200;
input int    InpMaxHooksToDraw = 1200;
input bool   InpDrawF1 = true;
input bool   InpDrawF2 = true;
input bool   InpDrawF3 = true;
input bool   InpDrawBullish = true;
input bool   InpDrawBearish = true;
input bool   InpDrawCandidates = true;
input bool   InpDrawConfirmed = true;
input bool   InpDrawLocked = true;
input bool   InpDrawInvalidated = false;
input bool   InpDrawHooks = true;
input bool   InpDetailedLabels = true;
input bool   InpShowOriginLabels = true;
input bool   InpShowInternalLabels = true;
input bool   InpUseSequenceColorShades = true;
input int    InpFixedLineWidth = 1;
input int    InpCurveSegments = 32;
input int    InpLabelFontSize = 7;

input color InpBullishCandidateColor = clrDeepSkyBlue;
input color InpBullishConfirmedColor = clrLime;
input color InpBearishCandidateColor = clrOrange;
input color InpBearishConfirmedColor = clrTomato;
input color InpF3LockedColor = clrMagenta;
input color InpHookColor = clrGray;

static datetime g_fc6_last_bar_time = 0;

bool FC6_ShouldRedraw()
{
   datetime t = iTime(_Symbol, _Period, 0);
   if(!InpRedrawOnNewBarOnly) return true;
   if(t != g_fc6_last_bar_time)
   {
      g_fc6_last_bar_time = t;
      return true;
   }
   return false;
}

void FC6_LoadConfig(FC6_Config &cfg)
{
   FC6_DefaultConfig(cfg);
   cfg.include_pending_nodes = InpIncludePendingNodes;
   cfg.scan_f1 = InpScanF1;
   cfg.scan_f2 = InpScanF2;
   cfg.scan_f3 = InpScanF3;
   cfg.scan_hooks = InpScanHooks;
   cfg.show_invalidated_in_audit = InpShowInvalidatedInAudit;
   cfg.keep_confirmed_f1_f2_after_boundary_hit = InpKeepConfirmedF1F2AfterBoundaryHit;
   cfg.max_events = InpMaxEvents;
   cfg.max_hooks = InpMaxHooks;
   cfg.max_roots_per_scale_direction = InpMaxRootsPerScaleDirection;
   cfg.boundary_epsilon_points = InpBoundaryEpsilonPoints;
   cfg.f2_min_parent_size_ratio = InpF2MinParentSizeRatio;
   cfg.f3_min_parent_size_ratio = InpF3MinParentSizeRatio;
   cfg.f3_leg1_L_min_ratio = InpF3Leg1LMinRatio;
   cfg.nd_min_retrace_ratio = InpNDMinRetraceRatio;
   cfg.nd_allow_below_half_cycle = InpNDAllowBelowHalfCycle;
   cfg.verbose_logs = InpVerboseAuditLogs;
}

void FC6_Run()
{
   MqlRates rates[];
   ArraySetAsSeries(rates, false);
   int copied = CopyRates(_Symbol, _Period, 0, InpBarsToScan, rates);
   if(copied <= 200)
   {
      Print("FC6_SUMMARY status=not_enough_bars copied=", copied);
      return;
   }
   ArraySetAsSeries(rates, false);

   int scales[];
   int scale_count = FC6_BuildScaleList(InpUseMultiScale,
                                        InpSwingL1,
                                        InpSwingL2,
                                        InpSwingL3,
                                        InpSwingL4,
                                        InpSwingL5,
                                        InpSwingL6,
                                        InpSwingL7,
                                        InpSwingL8,
                                        scales);
   if(scale_count <= 0)
   {
      Print("FC6_SUMMARY status=no_scales");
      return;
   }

   FC6_Config cfg;
   FC6_LoadConfig(cfg);

   FC6_FlagEvent events[];
   FC6_HookBranch hooks[];
   FC6_DetectResult result;
   FC6_DetectAllScales(rates, copied, scales, scale_count, cfg, events, hooks, result);

   int drawn = FC6_DrawAll(events,
                           hooks,
                           InpObjectPrefix,
                           InpMaxEventsToDraw,
                           InpMaxHooksToDraw,
                           InpDrawF1,
                           InpDrawF2,
                           InpDrawF3,
                           InpDrawBullish,
                           InpDrawBearish,
                           InpDrawCandidates,
                           InpDrawConfirmed,
                           InpDrawLocked,
                           InpDrawInvalidated,
                           InpDrawHooks,
                           InpDetailedLabels,
                           InpShowOriginLabels,
                           InpShowInternalLabels,
                           InpUseSequenceColorShades,
                           InpFixedLineWidth,
                           InpCurveSegments,
                           InpLabelFontSize,
                           InpBullishCandidateColor,
                           InpBullishConfirmedColor,
                           InpBearishCandidateColor,
                           InpBearishConfirmedColor,
                           InpF3LockedColor,
                           InpHookColor);

   FC6_PrintSummary(_Symbol, _Period, copied, scale_count, result, drawn);
   if(InpVerboseAuditLogs)
   {
      for(int i=0; i<ArraySize(events); i++) FC6_PrintEventAudit(events[i]);
      for(int h=0; h<ArraySize(hooks); h++) FC6_PrintHookAudit(hooks[h]);
   }
}

int OnInit()
{
   if(InpCleanObjectsOnInit)
      FC6_DeleteObjectsByPrefix(InpObjectPrefix);
   g_fc6_last_bar_time = 0;
   FC6_Run();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   if(InpCleanObjectsOnDeinit)
      FC6_DeleteObjectsByPrefix(InpObjectPrefix);
}

void OnTick()
{
   if(FC6_ShouldRedraw())
      FC6_Run();
}
