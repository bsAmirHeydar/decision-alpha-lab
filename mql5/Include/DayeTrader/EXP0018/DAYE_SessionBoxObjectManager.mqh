#ifndef __EXP0018_DAYE_SESSION_BOX_OBJECT_MANAGER_MQH__
#define __EXP0018_DAYE_SESSION_BOX_OBJECT_MANAGER_MQH__

#include <DayeTrader/EXP0018/DAYE_SessionBoxChartResolver.mqh>

long DAYE_SessionBoxArgb(const color base_color,const int alpha)
{
   int bounded=alpha;
   if(bounded<0) bounded=0;
   if(bounded>255) bounded=255;
   return (long)ColorToARGB(base_color,(uchar)bounded);
}

bool DAYE_SessionBoxGeometryMatches(const long chart_id,const string object_name,
                                    const DAYE_SessionBoxGeometry &geometry)
{
   if(ObjectFind(chart_id,object_name)<0) return false;
   if((ENUM_OBJECT)ObjectGetInteger(chart_id,object_name,OBJPROP_TYPE)!=OBJ_RECTANGLE) return false;
   datetime t1=(datetime)ObjectGetInteger(chart_id,object_name,OBJPROP_TIME,0);
   datetime t2=(datetime)ObjectGetInteger(chart_id,object_name,OBJPROP_TIME,1);
   double p1=ObjectGetDouble(chart_id,object_name,OBJPROP_PRICE,0);
   double p2=ObjectGetDouble(chart_id,object_name,OBJPROP_PRICE,1);
   double tolerance=MathMax(MathAbs(geometry.high_price),MathAbs(geometry.low_price))*1.0e-10;
   if(tolerance<=0.0) tolerance=1.0e-10;
   return t1==geometry.start_time_broker && t2==geometry.end_time_broker &&
          MathAbs(p1-geometry.high_price)<=tolerance && MathAbs(p2-geometry.low_price)<=tolerance;
}

bool DAYE_SetSessionBoxProperties(const long chart_id,const string object_name,
                                  const DAYE_SymbolPeriodSnapshot &snapshot,
                                  const DAYE_SessionBoxGeometry &geometry,
                                  const DAYE_SessionBoxConfig &config)
{
   bool ok=true;
   ok=ObjectMove(chart_id,object_name,0,geometry.start_time_broker,geometry.high_price) && ok;
   ok=ObjectMove(chart_id,object_name,1,geometry.end_time_broker,geometry.low_price) && ok;
   ok=ObjectSetInteger(chart_id,object_name,OBJPROP_COLOR,DAYE_SessionBoxArgb(DAYE_SessionColor(snapshot.period_code,config),config.fill_alpha)) && ok;
   ok=ObjectSetInteger(chart_id,object_name,OBJPROP_STYLE,config.border_style) && ok;
   ok=ObjectSetInteger(chart_id,object_name,OBJPROP_WIDTH,config.border_width) && ok;
   ok=ObjectSetInteger(chart_id,object_name,OBJPROP_FILL,true) && ok;
   ok=ObjectSetInteger(chart_id,object_name,OBJPROP_BACK,config.draw_in_background) && ok;
   ok=ObjectSetInteger(chart_id,object_name,OBJPROP_SELECTABLE,config.selectable) && ok;
   ok=ObjectSetInteger(chart_id,object_name,OBJPROP_SELECTED,false) && ok;
   ok=ObjectSetInteger(chart_id,object_name,OBJPROP_HIDDEN,config.hidden) && ok;
   ok=ObjectSetString(chart_id,object_name,OBJPROP_TOOLTIP,
      "EXP0018 P09 Session "+snapshot.period_code+" | "+snapshot.canonical_symbol+" | "+
      snapshot.trading_day_key+" | "+DAYE_PeriodCompletenessToString(snapshot.completeness)) && ok;
   return ok;
}

DAYE_SessionBoxProjectionStatus DAYE_ProjectSessionBoxToChart(const DAYE_SymbolPeriodSnapshot &snapshot,
                                                               const long chart_id,
                                                               const DAYE_SessionBoxGeometry &geometry,
                                                               const DAYE_SessionBoxConfig &config,
                                                               string &reason_code,
                                                               bool &manual_delete_repaired)
{
   reason_code="";
   manual_delete_repaired=false;
   string object_name=DAYE_BuildSessionBoxObjectName(snapshot.snapshot_id);
   bool existed=(ObjectFind(chart_id,object_name)>=0);
   if(!existed)
   {
      ResetLastError();
      if(!ObjectCreate(chart_id,object_name,OBJ_RECTANGLE,0,
                       geometry.start_time_broker,geometry.high_price,
                       geometry.end_time_broker,geometry.low_price))
      {
         reason_code="rectangle_create_failed_error_"+IntegerToString(GetLastError());
         return DAYE_SESSION_BOX_STATUS_OBJECT_CREATE_FAILED;
      }
      if(!DAYE_SetSessionBoxProperties(chart_id,object_name,snapshot,geometry,config))
      {
         reason_code="new_rectangle_property_assignment_failed";
         return DAYE_SESSION_BOX_STATUS_OBJECT_UPDATE_FAILED;
      }
      manual_delete_repaired=config.recreate_manually_deleted_owned_objects;
      ChartRedraw(chart_id);
      reason_code=manual_delete_repaired?"owned_session_box_recreated":"session_box_created";
      return DAYE_SESSION_BOX_STATUS_CREATED;
   }

   bool matches=DAYE_SessionBoxGeometryMatches(chart_id,object_name,geometry);
   if(snapshot.completeness==DAYE_PERIOD_COMPLETENESS_OPEN)
   {
      if(!DAYE_SetSessionBoxProperties(chart_id,object_name,snapshot,geometry,config))
      {
         reason_code="open_session_box_update_failed";
         return DAYE_SESSION_BOX_STATUS_OBJECT_UPDATE_FAILED;
      }
      ChartRedraw(chart_id);
      reason_code=matches?"open_session_box_reaffirmed":"open_session_range_updated";
      return DAYE_SESSION_BOX_STATUS_UPDATED_OPEN;
   }

   if(!config.verify_existing_owned_objects)
   {
      reason_code="closed_session_box_preserved_without_verification";
      return DAYE_SESSION_BOX_STATUS_VERIFIED_CLOSED;
   }
   if(matches)
   {
      if(!DAYE_SetSessionBoxProperties(chart_id,object_name,snapshot,geometry,config))
      {
         reason_code="closed_session_box_style_verification_failed";
         return DAYE_SESSION_BOX_STATUS_OBJECT_UPDATE_FAILED;
      }
      reason_code="closed_session_box_geometry_verified";
      return DAYE_SESSION_BOX_STATUS_VERIFIED_CLOSED;
   }
   if(!config.repair_existing_owned_objects)
   {
      reason_code="closed_session_box_geometry_mismatch_repair_disabled";
      return DAYE_SESSION_BOX_STATUS_OBJECT_UPDATE_FAILED;
   }
   if(!DAYE_SetSessionBoxProperties(chart_id,object_name,snapshot,geometry,config))
   {
      reason_code="closed_session_box_repair_failed";
      return DAYE_SESSION_BOX_STATUS_OBJECT_UPDATE_FAILED;
   }
   ChartRedraw(chart_id);
   reason_code="closed_session_box_repaired_from_p03_source";
   return DAYE_SESSION_BOX_STATUS_REPAIRED;
}

bool DAYE_StringArrayContains(const string &items[],const string value)
{
   for(int i=0;i<ArraySize(items);i++) if(items[i]==value) return true;
   return false;
}

int DAYE_DeleteOrphanedSessionBoxes(const long chart_id,const string &expected_names[])
{
   int deleted=0;
   for(int i=ObjectsTotal(chart_id,-1,-1)-1;i>=0;i--)
   {
      string name=ObjectName(chart_id,i,-1,-1);
      if(DAYE_IsOwnedSessionBoxObjectName(name) && !DAYE_StringArrayContains(expected_names,name))
      {
         if(ObjectDelete(chart_id,name)) deleted++;
      }
   }
   if(deleted>0) ChartRedraw(chart_id);
   return deleted;
}

int DAYE_DeleteOwnedSessionBoxesFromChart(const long chart_id)
{
   string none[];
   ArrayResize(none,0);
   return DAYE_DeleteOrphanedSessionBoxes(chart_id,none);
}

int DAYE_DeleteOwnedSessionBoxesFromAllCharts(void)
{
   int deleted=0;
   long chart=ChartFirst();
   while(chart>=0)
   {
      deleted+=DAYE_DeleteOwnedSessionBoxesFromChart(chart);
      chart=ChartNext(chart);
   }
   return deleted;
}

#endif
