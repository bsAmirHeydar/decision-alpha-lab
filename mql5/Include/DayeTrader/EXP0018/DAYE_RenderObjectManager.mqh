#ifndef __EXP0018_DAYE_RENDER_OBJECT_MANAGER_MQH__
#define __EXP0018_DAYE_RENDER_OBJECT_MANAGER_MQH__

#include <DayeTrader/EXP0018/DAYE_RenderChartResolver.mqh>

bool DAYE_SetTrendLineProperties(const long chart_id,const string name,
                                 const DAYE_ReferenceUseRecord &use,
                                 const DAYE_RenderGeometry &geometry,
                                 const DAYE_RenderConfig &config)
{
   bool ok=true;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_TIME,0,geometry.reference_time_broker) && ok;
   ok=ObjectSetDouble(chart_id,name,OBJPROP_PRICE,0,geometry.reference_price) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_TIME,1,geometry.confirmation_time_broker) && ok;
   ok=ObjectSetDouble(chart_id,name,OBJPROP_PRICE,1,geometry.confirmation_price) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_COLOR,config.line_color) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_STYLE,config.line_style) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_WIDTH,config.line_width) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_RAY_LEFT,config.line_ray_left) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_RAY_RIGHT,config.line_ray_right) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_BACK,config.line_back) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_SELECTABLE,config.line_selectable) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_SELECTED,false) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_HIDDEN,config.line_hidden) && ok;
   string description=(use.is_major && config.show_major_labels)?use.chart_label:"";
   ok=ObjectSetString(chart_id,name,OBJPROP_TEXT,description) && ok;
   ok=ObjectSetString(chart_id,name,OBJPROP_TOOLTIP,
                      "EXP0018 P08 | "+use.source_alias+" | "+DAYE_HuntSideToString(use.side)+" | "+use.use_id) && ok;
   return ok;
}

bool DAYE_CreateOrUpdateMidpointText(const long chart_id,const string name,
                                     const DAYE_ReferenceUseRecord &use,
                                     const DAYE_RenderGeometry &geometry,
                                     const DAYE_RenderConfig &config)
{
   if(!config.use_midpoint_text_object || !config.show_major_labels || !use.is_major || use.chart_label=="")
   {
      if(ObjectFind(chart_id,name)>=0) ObjectDelete(chart_id,name);
      return true;
   }
   double point=SymbolInfoDouble(use.hunter_broker_symbol,SYMBOL_POINT);
   double price=geometry.label_price;
   if(point>0.0 && config.label_vertical_offset_points!=0.0)
   {
      if(use.side==DAYE_HUNT_SIDE_HIGH) price+=config.label_vertical_offset_points*point;
      else price-=config.label_vertical_offset_points*point;
   }
   if(ObjectFind(chart_id,name)<0)
   {
      ResetLastError();
      if(!ObjectCreate(chart_id,name,OBJ_TEXT,0,geometry.label_time_broker,price)) return false;
   }
   bool ok=true;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_TIME,0,geometry.label_time_broker) && ok;
   ok=ObjectSetDouble(chart_id,name,OBJPROP_PRICE,0,price) && ok;
   ok=ObjectSetString(chart_id,name,OBJPROP_TEXT,use.chart_label) && ok;
   ok=ObjectSetString(chart_id,name,OBJPROP_FONT,config.label_font) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_FONTSIZE,config.label_font_size) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_COLOR,config.label_color) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_ANCHOR,ANCHOR_CENTER) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_BACK,config.line_back) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_SELECTABLE,config.line_selectable) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_SELECTED,false) && ok;
   ok=ObjectSetInteger(chart_id,name,OBJPROP_HIDDEN,config.line_hidden) && ok;
   ok=ObjectSetString(chart_id,name,OBJPROP_TOOLTIP,"EXP0018 P08 major relationship label | "+use.use_id) && ok;
   return ok;
}

bool DAYE_LineGeometryMatches(const long chart_id,const string name,const DAYE_RenderGeometry &geometry)
{
   if(ObjectFind(chart_id,name)<0) return false;
   datetime t1=(datetime)ObjectGetInteger(chart_id,name,OBJPROP_TIME,0);
   datetime t2=(datetime)ObjectGetInteger(chart_id,name,OBJPROP_TIME,1);
   double p1=ObjectGetDouble(chart_id,name,OBJPROP_PRICE,0);
   double p2=ObjectGetDouble(chart_id,name,OBJPROP_PRICE,1);
   double tolerance=MathMax(MathAbs(geometry.reference_price),MathAbs(geometry.confirmation_price))*1.0e-10;
   if(tolerance<=0.0) tolerance=1.0e-10;
   return t1==geometry.reference_time_broker && t2==geometry.confirmation_time_broker &&
          MathAbs(p1-geometry.reference_price)<=tolerance && MathAbs(p2-geometry.confirmation_price)<=tolerance;
}

DAYE_RenderProjectionStatus DAYE_ProjectAcceptedUseToChart(const DAYE_ReferenceUseRecord &use,
                                                            const long chart_id,
                                                            const DAYE_RenderGeometry &geometry,
                                                            const DAYE_RenderConfig &config,
                                                            const bool previously_recorded_as_drawn,
                                                            string &reason_code,
                                                            bool &manual_delete_repaired)
{
   reason_code="";
   manual_delete_repaired=false;
   string line_name=DAYE_BuildRenderLineName(use.use_id);
   string text_name=DAYE_BuildRenderTextName(use.use_id);
   bool existed=(ObjectFind(chart_id,line_name)>=0);

   if(!existed)
   {
      if(previously_recorded_as_drawn && !config.recreate_manually_deleted_owned_objects)
      {
         reason_code="owned_object_missing_and_recreation_disabled";
         return DAYE_RENDER_STATUS_OBJECT_UPDATE_FAILED;
      }
      ResetLastError();
      if(!ObjectCreate(chart_id,line_name,OBJ_TREND,0,
                       geometry.reference_time_broker,geometry.reference_price,
                       geometry.confirmation_time_broker,geometry.confirmation_price))
      {
         reason_code="trend_line_create_failed_error_"+IntegerToString(GetLastError());
         return DAYE_RENDER_STATUS_OBJECT_CREATE_FAILED;
      }
      manual_delete_repaired=previously_recorded_as_drawn && config.recreate_manually_deleted_owned_objects;
      if(!DAYE_SetTrendLineProperties(chart_id,line_name,use,geometry,config) ||
         !DAYE_CreateOrUpdateMidpointText(chart_id,text_name,use,geometry,config))
      {
         reason_code="new_object_property_assignment_failed";
         return DAYE_RENDER_STATUS_OBJECT_UPDATE_FAILED;
      }
      ChartRedraw(chart_id);
      reason_code=manual_delete_repaired?"owned_object_recreated_after_manual_delete":"immutable_accepted_use_line_created";
      return DAYE_RENDER_STATUS_CREATED;
   }

   if(!config.verify_existing_owned_objects)
   {
      reason_code="existing_owned_object_preserved_without_verification";
      return DAYE_RENDER_STATUS_VERIFIED;
   }

   bool geometry_matches=DAYE_LineGeometryMatches(chart_id,line_name,geometry);
   if(geometry_matches)
   {
      if(!DAYE_SetTrendLineProperties(chart_id,line_name,use,geometry,config) ||
         !DAYE_CreateOrUpdateMidpointText(chart_id,text_name,use,geometry,config))
      {
         reason_code="existing_object_style_verification_failed";
         return DAYE_RENDER_STATUS_OBJECT_UPDATE_FAILED;
      }
      reason_code="existing_owned_line_geometry_verified";
      return DAYE_RENDER_STATUS_VERIFIED;
   }

   if(!config.repair_existing_owned_objects)
   {
      reason_code="existing_owned_line_geometry_mismatch_repair_disabled";
      return DAYE_RENDER_STATUS_OBJECT_UPDATE_FAILED;
   }
   if(!DAYE_SetTrendLineProperties(chart_id,line_name,use,geometry,config) ||
      !DAYE_CreateOrUpdateMidpointText(chart_id,text_name,use,geometry,config))
   {
      reason_code="owned_line_repair_failed";
      return DAYE_RENDER_STATUS_OBJECT_UPDATE_FAILED;
   }
   ChartRedraw(chart_id);
   reason_code="owned_line_geometry_repaired_from_immutable_source";
   return DAYE_RENDER_STATUS_REPAIRED;
}

int DAYE_DeleteOwnedObjectsFromChart(const long chart_id)
{
   int deleted=0;
   int total=ObjectsTotal(chart_id,-1,-1);
   for(int i=total-1;i>=0;i--)
   {
      string name=ObjectName(chart_id,i,-1,-1);
      if(DAYE_IsOwnedRenderObjectName(name) && ObjectDelete(chart_id,name)) deleted++;
   }
   if(deleted>0) ChartRedraw(chart_id);
   return deleted;
}

int DAYE_DeleteOwnedObjectsFromAllCharts(void)
{
   int deleted=0;
   long chart=ChartFirst();
   while(chart>=0)
   {
      deleted+=DAYE_DeleteOwnedObjectsFromChart(chart);
      chart=ChartNext(chart);
   }
   return deleted;
}

#endif
