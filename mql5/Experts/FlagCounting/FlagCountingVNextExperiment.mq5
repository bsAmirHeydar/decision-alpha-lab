#property strict
#property version   "2.00"
#property description "Fractal multi-scale multi-sequence flag-counting vNext visual experiment."

#include "../../Include/FlagCountingVNext/FCN_Detector.mqh"
#include "../../Include/FlagCountingVNext/FCN_Renderer.mqh"

input int  InpBarsToScan = 5000;
input bool InpRedrawOnNewBarOnly = true;

input bool InpUseMultiScale = true;
input int  InpSwingL1 = 2;
input int  InpSwingL2 = 3;
input int  InpSwingL3 = 5;
input int  InpSwingL4 = 8;
input int  InpSwingL5 = 13;
input int  InpSwingL6 = 21;

input bool InpScanF1 = true;
input bool InpScanF2 = true;
input bool InpScanF3 = true;
input bool InpScanND = true;
input int  InpMaxNDPerScale = 80;
input bool InpRequireParentConfirmedForNextF = true;
input bool InpRequireF2AtLeastParentSize = true;
input double InpF2MinParentSizeRatio = 1.0;

input int  InpMaxEvents = 1200;
input int  InpMaxRootSequencesPerScale = 0;
input bool InpVerboseAuditLogs = false;

input string InpObjectPrefix = "DAL_FCN_";
input bool InpCleanObjectsOnInit = true;
input bool InpCleanObjectsOnDeinit = true;
input int  InpMaxEventsToDraw = 350;
input bool InpDrawF1 = true;
input bool InpDrawF2 = true;
input bool InpDrawF3 = true;
input bool InpDrawND = true;
input bool InpDrawBullish = true;
input bool InpDrawBearish = true;
input bool InpDrawOnlyConfirmed = false;
input bool InpShowLevelLabels = true;
input bool InpShowInternal12Labels = true;
input int  InpBaseLevelFontSize = 7;
input int  InpBaseInternalFontSize = 7;
input bool InpUseSequenceColorShades = true;
input int  InpFixedLineWidth = 1;

input color InpBullishLiveColor = clrDeepSkyBlue;
input color InpBullishConfirmedColor = clrLime;
input color InpBearishLiveColor = clrOrange;
input color InpBearishConfirmedColor = clrTomato;
input color InpBullishF3TerminalColor = clrAqua;
input color InpBearishF3TerminalColor = clrMagenta;
input color InpNDColor = clrSilver;

static datetime g_last_bar_time = 0;

bool FCN_ShouldRedraw()
{
   datetime t = iTime(_Symbol, _Period, 0);
   if(!InpRedrawOnNewBarOnly) return true;
   if(t != g_last_bar_time)
   {
      g_last_bar_time = t;
      return true;
   }
   return false;
}

void FCN_RunExperiment()
{
   MqlRates rates[];
   ArraySetAsSeries(rates, false);
   int copied = CopyRates(_Symbol, _Period, 0, InpBarsToScan, rates);
   if(copied <= 100)
   {
      Print("FCN_SUMMARY symbol=", _Symbol, " tf=", EnumToString(_Period), " copied=", copied, " status=not_enough_bars");
      return;
   }
   ArraySetAsSeries(rates, false);

   int scales[];
   int scale_count = FCN_BuildScaleList(InpUseMultiScale,
                                        InpSwingL1,
                                        InpSwingL2,
                                        InpSwingL3,
                                        InpSwingL4,
                                        InpSwingL5,
                                        InpSwingL6,
                                        scales);
   if(scale_count <= 0)
   {
      Print("FCN_SUMMARY status=no_scales");
      return;
   }

   FCN_Config cfg;
   cfg.scan_f1 = InpScanF1;
   cfg.scan_f2 = InpScanF2;
   cfg.scan_f3 = InpScanF3;
   cfg.require_parent_confirmed = InpRequireParentConfirmedForNextF;
   cfg.require_f2_parent_size = InpRequireF2AtLeastParentSize;
   cfg.f2_min_parent_size_ratio = InpF2MinParentSizeRatio;
   cfg.scan_nd = InpScanND;
   cfg.max_nd_per_scale = InpMaxNDPerScale;
   cfg.max_events = InpMaxEvents;
   cfg.max_roots_per_scale = InpMaxRootSequencesPerScale;
   cfg.verbose_logs = InpVerboseAuditLogs;

   FCN_Event events[];
   int detected = FCN_DetectFractalFlagCounting(rates, copied, scales, scale_count, cfg, events);
   int drawn = FCN_DrawEvents(events,
                              InpMaxEventsToDraw,
                              InpObjectPrefix,
                              InpDrawF1,
                              InpDrawF2,
                              InpDrawF3,
                              InpDrawND,
                              InpDrawBullish,
                              InpDrawBearish,
                              InpDrawOnlyConfirmed,
                              InpShowLevelLabels,
                              InpShowInternal12Labels,
                              InpBaseLevelFontSize,
                              InpBaseInternalFontSize,
                              InpBullishLiveColor,
                              InpBullishConfirmedColor,
                              InpBearishLiveColor,
                              InpBearishConfirmedColor,
                              InpBullishF3TerminalColor,
                              InpBearishF3TerminalColor,
                              InpNDColor,
                              InpUseSequenceColorShades,
                              InpFixedLineWidth);

   Print("FCN_SUMMARY symbol=", _Symbol,
         " tf=", EnumToString(_Period),
         " bars=", copied,
         " scales=", scale_count,
         " events=", detected,
         " drawn=", drawn,
         " drawOnlyConfirmed=", (InpDrawOnlyConfirmed ? "true" : "false"));
}

int OnInit()
{
   if(InpCleanObjectsOnInit)
      FCN_DeleteObjectsByPrefix(InpObjectPrefix);
   g_last_bar_time = 0;
   FCN_RunExperiment();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   if(InpCleanObjectsOnDeinit)
      FCN_DeleteObjectsByPrefix(InpObjectPrefix);
}

void OnTick()
{
   if(FCN_ShouldRedraw())
      FCN_RunExperiment();
}
