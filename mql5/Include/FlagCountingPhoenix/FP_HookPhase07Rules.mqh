#ifndef __FP_HOOK_PHASE07_RULES_MQH__
#define __FP_HOOK_PHASE07_RULES_MQH__
#property strict

#include "FP_HookPhase07Types.mqh"

bool FP_HookP07ShouldRun(const FP_HookPhase07Config &cfg)
{
   if(!cfg.enabled)
      return false;
   return true;
}

void FP_HookP07ApplyDisplayFamily(const FP_HookPhase07Config &cfg,
                                  FP_HookPhase01Config &p01,
                                  FP_HookPhase02Config &p02,
                                  FP_HookPhase03Config &p03,
                                  FP_HookPhase04Config &p04,
                                  FP_HookPhase05Config &p05,
                                  FP_HookPhase06Config &p06)
{
   p01.display_family = cfg.display_family;
   p02.display_family = cfg.display_family;
   p03.display_family = cfg.display_family;
   p04.display_family = cfg.display_family;
   p05.display_family = cfg.display_family;
   p06.display_family = cfg.display_family;
}

void FP_HookP07ForceEnablePhases(const FP_HookPhase07Config &cfg,
                                 FP_HookPhase01Config &p01,
                                 FP_HookPhase02Config &p02,
                                 FP_HookPhase03Config &p03,
                                 FP_HookPhase04Config &p04,
                                 FP_HookPhase05Config &p05,
                                 FP_HookPhase06Config &p06)
{
   if(!cfg.force_enable_required_phases)
      return;
   if(cfg.respect_individual_phase_enabled)
      return;

   p01.enabled = true;
   p02.enabled = true;
   p03.enabled = true;
   p04.enabled = true;
   p05.enabled = true;
   p06.enabled = true;
}

void FP_HookP07DisableAllDrawing(FP_HookPhase01Config &p01,
                                 FP_HookPhase02Config &p02,
                                 FP_HookPhase03Config &p03,
                                 FP_HookPhase04Config &p04,
                                 FP_HookPhase05Config &p05,
                                 FP_HookPhase06Config &p06)
{
   p01.draw_nodes = false;
   p01.draw_labels = false;

   p02.draw_sequences = false;
   p02.draw_origin = false;
   p02.draw_x_nodes = false;
   p02.draw_x_lines = false;
   p02.draw_death_boundary = false;
   p02.draw_cycle_arc = false;
   p02.draw_sequence_count_label = false;
   p02.draw_labels = false;

   p03.draw_y_extremes = false;
   p03.draw_y_lines = false;
   p03.draw_x_reference = false;
   p03.draw_labels = false;

   p04.draw_nd = false;
   p04.draw_death = false;
   p04.draw_x_closure = false;
   p04.draw_thresholds = false;
   p04.draw_labels = false;

   p05.draw_type_label = false;
   p05.draw_type_anchor = false;
   p05.draw_type_comparison_lines = false;
   p05.draw_labels = false;

   p06.draw_quality_label = false;
   p06.draw_xy_anchor = false;
   p06.draw_projection_lines = false;
   p06.draw_labels = false;
}

void FP_HookP07ApplyGlobalLabels(const FP_HookPhase07Config &cfg,
                                 FP_HookPhase01Config &p01,
                                 FP_HookPhase02Config &p02,
                                 FP_HookPhase03Config &p03,
                                 FP_HookPhase04Config &p04,
                                 FP_HookPhase05Config &p05,
                                 FP_HookPhase06Config &p06)
{
   if(!cfg.show_labels)
   {
      p01.draw_labels = false;
      p02.draw_labels = false;
      p03.draw_labels = false;
      p04.draw_labels = false;
      p05.draw_labels = false;
      p06.draw_labels = false;
      p06.draw_quality_label = false;
      p05.draw_type_label = false;
   }
}

void FP_HookP07ApplyDrawBudgets(const FP_HookPhase07Config &cfg,
                                FP_HookPhase01Config &p01,
                                FP_HookPhase02Config &p02,
                                FP_HookPhase03Config &p03,
                                FP_HookPhase04Config &p04,
                                FP_HookPhase05Config &p05,
                                FP_HookPhase06Config &p06)
{
   if(cfg.view_profile == FP_HOOK_P07_VIEW_SEQUENCE_CYCLE_DEBUG)
   {
      p01.max_nodes_to_draw = 0;
      p02.max_sequences_to_draw = 1;
      p03.max_sequences_to_draw = 0;
      p04.max_sequences_to_draw = 0;
      p05.max_sequences_to_draw = 0;
      p06.max_sequences_to_draw = 0;
      return;
   }

   if(cfg.max_nodes_to_draw > 0)
      p01.max_nodes_to_draw = cfg.max_nodes_to_draw;

   if(cfg.max_sequences_to_draw > 0)
   {
      p02.max_sequences_to_draw = cfg.max_sequences_to_draw;
      p03.max_sequences_to_draw = cfg.max_sequences_to_draw;
      p04.max_sequences_to_draw = cfg.max_sequences_to_draw;
      p05.max_sequences_to_draw = cfg.max_sequences_to_draw;
      p06.max_sequences_to_draw = cfg.max_sequences_to_draw;
   }
}

void FP_HookP07ApplyGlobalAuditFlags(const FP_HookPhase07Config &cfg,
                                     FP_HookPhase01Config &p01,
                                     FP_HookPhase02Config &p02,
                                     FP_HookPhase03Config &p03,
                                     FP_HookPhase04Config &p04,
                                     FP_HookPhase05Config &p05,
                                     FP_HookPhase06Config &p06)
{
   if(cfg.global_export_csv)
   {
      p01.export_csv = true;
      p02.export_csv = true;
      p03.export_csv = true;
      p04.export_csv = true;
      p05.export_csv = true;
      p06.export_csv = true;
   }

   if(cfg.global_print_summary)
   {
      p01.print_summary = true;
      p02.print_summary = true;
      p03.print_summary = true;
      p04.print_summary = true;
      p05.print_summary = true;
      p06.print_summary = true;
   }

   if(cfg.global_print_samples)
   {
      p01.print_samples = true;
      p02.print_samples = true;
      p03.print_samples = true;
      p04.print_samples = true;
      p05.print_samples = true;
      p06.print_samples = true;
   }
}

void FP_HookP07ApplyProfileDrawing(const FP_HookPhase07Config &cfg,
                                   FP_HookPhase01Config &p01,
                                   FP_HookPhase02Config &p02,
                                   FP_HookPhase03Config &p03,
                                   FP_HookPhase04Config &p04,
                                   FP_HookPhase05Config &p05,
                                   FP_HookPhase06Config &p06)
{
   if(cfg.view_profile == FP_HOOK_P07_VIEW_KEEP_INPUTS)
      return;

   FP_HookP07DisableAllDrawing(p01, p02, p03, p04, p05, p06);

   if(cfg.view_profile == FP_HOOK_P07_VIEW_RAW_NODES)
   {
      p01.draw_nodes = true;
      p01.draw_labels = cfg.show_labels;
      return;
   }

   if(cfg.view_profile == FP_HOOK_P07_VIEW_SEQUENCE_XY)
   {
      p02.draw_sequences = true;
      p02.draw_origin = true;
      p02.draw_x_nodes = true;
      p02.draw_x_lines = true;
      p02.draw_death_boundary = true;
      p02.draw_labels = cfg.show_labels;

      p03.draw_y_extremes = true;
      p03.draw_y_lines = true;
      p03.draw_x_reference = true;
      p03.draw_labels = cfg.show_labels;
      return;
   }

   if(cfg.view_profile == FP_HOOK_P07_VIEW_LIFECYCLE)
   {
      p02.draw_origin = true;
      p02.draw_death_boundary = true;
      p02.draw_labels = false;

      p03.draw_y_extremes = true;
      p03.draw_y_lines = true;
      p03.draw_labels = false;

      p04.draw_nd = true;
      p04.draw_death = true;
      p04.draw_x_closure = true;
      p04.draw_thresholds = true;
      p04.draw_labels = cfg.show_labels;
      return;
   }

   if(cfg.view_profile == FP_HOOK_P07_VIEW_TYPE_QUALITY)
   {
      p05.draw_type_label = cfg.show_labels;
      p05.draw_type_anchor = true;
      p05.draw_type_comparison_lines = true;
      p05.draw_labels = cfg.show_labels;

      p06.draw_quality_label = cfg.show_labels;
      p06.draw_xy_anchor = true;
      p06.draw_projection_lines = true;
      p06.draw_labels = false;
      return;
   }

   if(cfg.view_profile == FP_HOOK_P07_VIEW_QUALITY_FOCUS)
   {
      p06.draw_quality_label = cfg.show_labels;
      p06.draw_xy_anchor = true;
      p06.draw_projection_lines = true;
      p06.draw_labels = false;
      return;
   }

   if(cfg.view_profile == FP_HOOK_P07_VIEW_SEQUENCE_CYCLE_DEBUG)
   {
      // Hard inspector lens: Phase 01 is allowed to build node inputs, but it
      // does not draw. Phase 02 is the only visible layer. Later Hook phases are
      // disabled so stale P03/P04/P05/P06 text cannot be redrawn during sequence
      // inspection even if their individual inputs are still true in MT5.
      p01.draw_nodes = false;
      p01.draw_labels = false;

      p02.enabled = true;
      p02.draw_sequences = true;
      p02.draw_origin = true;
      p02.draw_x_nodes = true;
      p02.draw_x_lines = true;
      p02.draw_death_boundary = false;
      p02.draw_cycle_arc = true;
      p02.draw_sequence_count_label = true;
      p02.draw_labels = false;

      p03.enabled = false;
      p03.draw_y_extremes = false;
      p03.draw_y_lines = false;
      p03.draw_x_reference = false;
      p03.draw_labels = false;

      p04.enabled = false;
      p04.draw_nd = false;
      p04.draw_death = false;
      p04.draw_x_closure = false;
      p04.draw_thresholds = false;
      p04.draw_labels = false;

      p05.enabled = false;
      p05.draw_type_label = false;
      p05.draw_type_anchor = false;
      p05.draw_type_comparison_lines = false;
      p05.draw_labels = false;

      p06.enabled = false;
      p06.draw_quality_label = false;
      p06.draw_xy_anchor = false;
      p06.draw_projection_lines = false;
      p06.draw_labels = false;
      return;
   }

   if(cfg.view_profile == FP_HOOK_P07_VIEW_OFFICIAL_SCHEMATIC)
   {
      p02.draw_sequences = true;
      p02.draw_origin = true;
      p02.draw_x_nodes = true;
      p02.draw_x_lines = true;
      p02.draw_death_boundary = false;
      p02.draw_labels = false;

      p03.draw_y_extremes = true;
      p03.draw_y_lines = true;
      p03.draw_x_reference = false;
      p03.draw_labels = false;

      p04.draw_nd = true;
      p04.draw_death = true;
      p04.draw_x_closure = true;
      p04.draw_thresholds = false;
      p04.draw_labels = false;

      p05.draw_type_label = true;
      p05.draw_type_anchor = true;
      p05.draw_type_comparison_lines = false;
      p05.draw_labels = false;

      p06.draw_quality_label = true;
      p06.draw_xy_anchor = true;
      p06.draw_projection_lines = false;
      p06.draw_labels = false;
      return;
   }

   if(cfg.view_profile == FP_HOOK_P07_VIEW_FULL_DEBUG)
   {
      p01.draw_nodes = true;
      p01.draw_labels = cfg.show_labels;

      p02.draw_sequences = true;
      p02.draw_origin = true;
      p02.draw_x_nodes = true;
      p02.draw_x_lines = true;
      p02.draw_death_boundary = true;
      p02.draw_labels = cfg.show_labels;

      p03.draw_y_extremes = true;
      p03.draw_y_lines = true;
      p03.draw_x_reference = true;
      p03.draw_labels = cfg.show_labels;

      p04.draw_nd = true;
      p04.draw_death = true;
      p04.draw_x_closure = true;
      p04.draw_thresholds = true;
      p04.draw_labels = cfg.show_labels;

      p05.draw_type_label = cfg.show_labels;
      p05.draw_type_anchor = true;
      p05.draw_type_comparison_lines = true;
      p05.draw_labels = cfg.show_labels;

      p06.draw_quality_label = cfg.show_labels;
      p06.draw_xy_anchor = true;
      p06.draw_projection_lines = true;
      p06.draw_labels = cfg.show_labels;
      return;
   }

   if(cfg.view_profile == FP_HOOK_P07_VIEW_AUDIT_EXPORT_ONLY)
   {
      p01.export_csv = true;
      p02.export_csv = true;
      p03.export_csv = true;
      p04.export_csv = true;
      p05.export_csv = true;
      p06.export_csv = true;
      p01.print_summary = cfg.global_print_summary;
      p02.print_summary = cfg.global_print_summary;
      p03.print_summary = cfg.global_print_summary;
      p04.print_summary = cfg.global_print_summary;
      p05.print_summary = cfg.global_print_summary;
      p06.print_summary = cfg.global_print_summary;
      return;
   }
}

bool FP_HookP07Phase01DrawEnabled(const FP_HookPhase01Config &p01)
{
   return (p01.draw_nodes || p01.draw_labels);
}

bool FP_HookP07Phase02DrawEnabled(const FP_HookPhase02Config &p02)
{
   return (p02.draw_sequences || p02.draw_origin || p02.draw_x_nodes ||
           p02.draw_x_lines || p02.draw_death_boundary || p02.draw_labels);
}

bool FP_HookP07Phase03DrawEnabled(const FP_HookPhase03Config &p03)
{
   return (p03.draw_y_extremes || p03.draw_y_lines ||
           p03.draw_x_reference || p03.draw_labels);
}

bool FP_HookP07Phase04DrawEnabled(const FP_HookPhase04Config &p04)
{
   return (p04.draw_nd || p04.draw_death || p04.draw_x_closure ||
           p04.draw_thresholds || p04.draw_labels);
}

bool FP_HookP07Phase05DrawEnabled(const FP_HookPhase05Config &p05)
{
   return (p05.draw_type_label || p05.draw_type_anchor ||
           p05.draw_type_comparison_lines || p05.draw_labels);
}

bool FP_HookP07Phase06DrawEnabled(const FP_HookPhase06Config &p06)
{
   return (p06.draw_quality_label || p06.draw_xy_anchor ||
           p06.draw_projection_lines || p06.draw_labels);
}

void FP_HookP07FillReportFromConfigs(const FP_HookPhase07Config &cfg,
                                     const FP_HookPhase01Config &p01,
                                     const FP_HookPhase02Config &p02,
                                     const FP_HookPhase03Config &p03,
                                     const FP_HookPhase04Config &p04,
                                     const FP_HookPhase05Config &p05,
                                     const FP_HookPhase06Config &p06,
                                     FP_HookPhase07Report &r)
{
   r.display_family = cfg.display_family;
   r.view_profile = cfg.view_profile;

   r.p01_enabled = p01.enabled;
   r.p02_enabled = p02.enabled;
   r.p03_enabled = p03.enabled;
   r.p04_enabled = p04.enabled;
   r.p05_enabled = p05.enabled;
   r.p06_enabled = p06.enabled;

   r.p01_draw = FP_HookP07Phase01DrawEnabled(p01);
   r.p02_draw = FP_HookP07Phase02DrawEnabled(p02);
   r.p03_draw = FP_HookP07Phase03DrawEnabled(p03);
   r.p04_draw = FP_HookP07Phase04DrawEnabled(p04);
   r.p05_draw = FP_HookP07Phase05DrawEnabled(p05);
   r.p06_draw = FP_HookP07Phase06DrawEnabled(p06);

   r.p01_export = p01.export_csv;
   r.p02_export = p02.export_csv;
   r.p03_export = p03.export_csv;
   r.p04_export = p04.export_csv;
   r.p05_export = p05.export_csv;
   r.p06_export = p06.export_csv;

   r.max_nodes_to_draw = p01.max_nodes_to_draw;
   r.max_sequences_to_draw = p06.max_sequences_to_draw;
}

void FP_PrintHookPhase07Report(const string tag, const FP_HookPhase07Report &r)
{
   Print(tag,
         " status=", r.status,
         " reason=", r.reason,
         " attempted=", FP_HookP07BoolName(r.attempted),
         " ok=", FP_HookP07BoolName(r.ok),
         " display_family=", FP_HookP01DisplayFamilyName(r.display_family),
         " profile=", FP_HookP07ViewProfileName(r.view_profile),
         " p01_draw=", FP_HookP07BoolName(r.p01_draw),
         " p02_draw=", FP_HookP07BoolName(r.p02_draw),
         " p03_draw=", FP_HookP07BoolName(r.p03_draw),
         " p04_draw=", FP_HookP07BoolName(r.p04_draw),
         " p05_draw=", FP_HookP07BoolName(r.p05_draw),
         " p06_draw=", FP_HookP07BoolName(r.p06_draw),
         " p01_export=", FP_HookP07BoolName(r.p01_export),
         " p02_export=", FP_HookP07BoolName(r.p02_export),
         " p03_export=", FP_HookP07BoolName(r.p03_export),
         " p04_export=", FP_HookP07BoolName(r.p04_export),
         " p05_export=", FP_HookP07BoolName(r.p05_export),
         " p06_export=", FP_HookP07BoolName(r.p06_export),
         " deleted=", r.objects_deleted,
         " files=", r.files_written,
         " file_errors=", r.file_errors);
}

#endif // __FP_HOOK_PHASE07_RULES_MQH__
