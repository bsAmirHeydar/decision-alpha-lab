#ifndef ALPHA_LAB_UC04W1_REFERENCE_DATETIME_FORMAT_MQH
#define ALPHA_LAB_UC04W1_REFERENCE_DATETIME_FORMAT_MQH

// UC04-W1A reference-only implementation.
// This file is intentionally located under mql5/Tests and has no production
// materialization or consumer-cutover authority.
string AL_UC04W1_ReferenceFormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}

#endif
