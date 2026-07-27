//+------------------------------------------------------------------+
//| Alpha Lab UC04-W1A deterministic datetime format native self-test|
//| Reference-only: no trading, order, capital or consumer authority  |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "UC04-W1A native byte-exact characterization for the deterministic datetime formatter candidate."

#include "..\..\Include\AlphaLab\UC04W1\AL_UC04W1_ReferenceDateTimeFormat.mqh"

#define UC04W1_RUNTIME_OUTPUT "UC04W1_DeterministicDateTimeFormatSelfTest.csv"

string UC04W1_LegacyFormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}

bool UC04W1_WriteRow(const int handle,
                     const string fixture_id,
                     const datetime value,
                     const string expected,
                     const string legacy_output,
                     const string reference_output,
                     const bool passed)
{
   if(handle == INVALID_HANDLE)
      return false;
   FileWrite(handle,
             fixture_id,
             IntegerToString((long)value),
             expected,
             legacy_output,
             reference_output,
             (passed ? "PASS" : "FAIL"));
   return true;
}

int OnInit()
{
   datetime values[] =
   {
      D'1970.01.01 00:00:00',
      D'1970.01.01 00:00:01',
      D'1970.01.01 00:00:59',
      D'1970.01.01 00:01:00',
      D'1970.01.01 23:59:59',
      D'1970.01.02 00:00:00',
      D'1999.12.31 23:59:59',
      D'2000.02.29 12:34:56',
      D'2009.02.13 23:31:30',
      D'2024.02.29 00:00:00',
      D'2026.07.27 12:34:56',
      D'2038.01.19 03:14:07',
      D'2099.12.31 23:59:59'
   };
   string expected[] =
   {
      "1970.01.01 00:00:00",
      "1970.01.01 00:00:01",
      "1970.01.01 00:00:59",
      "1970.01.01 00:01:00",
      "1970.01.01 23:59:59",
      "1970.01.02 00:00:00",
      "1999.12.31 23:59:59",
      "2000.02.29 12:34:56",
      "2009.02.13 23:31:30",
      "2024.02.29 00:00:00",
      "2026.07.27 12:34:56",
      "2038.01.19 03:14:07",
      "2099.12.31 23:59:59"
   };

   if(ArraySize(values) != ArraySize(expected))
      return INIT_FAILED;

   int handle = FileOpen(UC04W1_RUNTIME_OUTPUT,
                         FILE_COMMON | FILE_WRITE | FILE_CSV | FILE_ANSI,
                         ',');
   if(handle == INVALID_HANDLE)
   {
      Print("UC04-W1A SELFTEST FAIL: runtime receipt could not be opened. error=", GetLastError());
      return INIT_FAILED;
   }
   FileWrite(handle,
             "fixture_id",
             "unix_seconds",
             "expected",
             "legacy_output",
             "reference_output",
             "status");

   bool all_passed = true;
   for(int i = 0; i < ArraySize(values); i++)
   {
      string legacy_output = UC04W1_LegacyFormatDateTime(values[i]);
      string reference_output = AL_UC04W1_ReferenceFormatDateTime(values[i]);
      bool passed = (legacy_output == expected[i] &&
                     reference_output == expected[i] &&
                     legacy_output == reference_output &&
                     StringLen(reference_output) == 19);
      string fixture_id = "UC04W1_DT_" + StringFormat("%03d", i + 1);
      if(!UC04W1_WriteRow(handle,
                          fixture_id,
                          values[i],
                          expected[i],
                          legacy_output,
                          reference_output,
                          passed))
      {
         all_passed = false;
      }
      if(!passed)
      {
         all_passed = false;
         Print("UC04-W1A SELFTEST mismatch fixture=", fixture_id,
               " expected=", expected[i],
               " legacy=", legacy_output,
               " reference=", reference_output);
      }
   }

   FileWrite(handle,
             "SUMMARY",
             IntegerToString(ArraySize(values)),
             "BYTE_EXACT_ASCII",
             "LEGACY_REFERENCE",
             "TEST_ONLY_REFERENCE_ENGINE",
             (all_passed ? "PASS" : "FAIL"));
   FileFlush(handle);
   FileClose(handle);

   if(!all_passed)
   {
      Print("UC04-W1A SELFTEST FAIL");
      return INIT_FAILED;
   }

   Print("UC04-W1A SELFTEST PASS vectors=", ArraySize(values));
   return INIT_SUCCEEDED;
}

void OnTick()
{
}
