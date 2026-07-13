#ifndef __EXP0019_FP_I03_ENUMS_MQH__
#define __EXP0019_FP_I03_ENUMS_MQH__

enum FP_I03_DstRegime
  {
   FP_I03_DST_STANDARD=0,
   FP_I03_DST_DAYLIGHT=1
  };

enum FP_I03_LocalTimeStatus
  {
   FP_I03_LOCAL_UNIQUE=0,
   FP_I03_LOCAL_AMBIGUOUS=1,
   FP_I03_LOCAL_NONEXISTENT=2
  };

enum FP_I03_LocalResolutionPolicy
  {
   FP_I03_LOCAL_REJECT=0,
   FP_I03_LOCAL_EARLIEST=1,
   FP_I03_LOCAL_LATEST=2
  };

enum FP_I03_CalendarSegment
  {
   FP_I03_SEGMENT_A=0,
   FP_I03_SEGMENT_L=1,
   FP_I03_SEGMENT_N=2,
   FP_I03_SEGMENT_DAILY_GAP=3,
   FP_I03_SEGMENT_WEEKEND_CLOSED=4
  };

enum FP_I03_WeekState
  {
   FP_I03_WEEK_ACTIVE=0,
   FP_I03_WEEK_CLOSED_AFTER_FRIDAY=1,
   FP_I03_WEEK_CLOSED_BEFORE_SUNDAY_OPEN=2
  };

enum FP_I03_CalendarHealth
  {
   FP_I03_HEALTH_READY=0,
   FP_I03_HEALTH_DEGRADED=1,
   FP_I03_HEALTH_BLOCKED=2
  };

string FP_I03_SegmentToString(const FP_I03_CalendarSegment value)
  {
   switch(value)
     {
      case FP_I03_SEGMENT_A:return "A";
      case FP_I03_SEGMENT_L:return "L";
      case FP_I03_SEGMENT_N:return "N";
      case FP_I03_SEGMENT_DAILY_GAP:return "DAILY_GAP";
      case FP_I03_SEGMENT_WEEKEND_CLOSED:return "WEEKEND_CLOSED";
     }
   return "UNKNOWN";
  }

#endif
