//+------------------------------------------------------------------+
//| Alpha Lab UC04-W1B deterministic datetime native runner          |
//| Test-only script: no trading, order or capital authority          |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property script_show_inputs
#property description "UC04-W1B native byte-exact qualification runner for the test-only datetime formatter reference."

#include "..\..\Include\AlphaLab\UC04W1\AL_UC04W1_ReferenceDateTimeFormat.mqh"

#define UC04W1B_RUNTIME_OUTPUT "AlphaLab\\UC04W1B\\UC04W1B_DeterministicDateTimeFormatNativeRunner.csv"

string UC04W1B_LegacyFormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}

void OnStart()
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

   int handle = FileOpen(UC04W1B_RUNTIME_OUTPUT,
                         FILE_COMMON | FILE_WRITE | FILE_CSV | FILE_ANSI,
                         ',');
   if(handle == INVALID_HANDLE)
   {
      Print("UC04-W1B SELFTEST FAIL: FileOpen error=", GetLastError());
      return;
   }

   FileWrite(handle,
             "fixture_id",
             "unix_seconds",
             "expected",
             "legacy_output",
             "reference_output",
             "status");

   bool all_passed = (ArraySize(values) == ArraySize(expected));
   for(int i = 0; i < ArraySize(values); i++)
   {
      string legacy_output = UC04W1B_LegacyFormatDateTime(values[i]);
      string reference_output = AL_UC04W1_ReferenceFormatDateTime(values[i]);
      bool passed = (legacy_output == expected[i] &&
                     reference_output == expected[i] &&
                     legacy_output == reference_output &&
                     StringLen(reference_output) == 19);
      if(!passed)
         all_passed = false;
      FileWrite(handle,
                "UC04W1_DT_" + StringFormat("%03d", i + 1),
                IntegerToString((long)values[i]),
                expected[i],
                legacy_output,
                reference_output,
                (passed ? "PASS" : "FAIL"));
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

   Print("UC04-W1B SELFTEST ", (all_passed ? "PASS" : "FAIL"),
         " vectors=", ArraySize(values));
}
