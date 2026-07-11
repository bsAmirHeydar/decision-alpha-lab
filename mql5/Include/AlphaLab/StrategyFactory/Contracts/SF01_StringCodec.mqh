#ifndef __SF01_STRING_CODEC_MQH__
#define __SF01_STRING_CODEC_MQH__

bool SF01_IsAscii(const string value)
{
   const int count = StringLen(value);
   for(int i = 0; i < count; i++)
   {
      const int code = StringGetCharacter(value, i);
      if(code < 0 || code > 127) return false;
   }
   return true;
}

string SF01_Trim(const string value)
{
   string out = value;
   StringTrimLeft(out);
   StringTrimRight(out);
   return out;
}

string SF01_JsonEscape(const string value)
{
   string out = value;
   StringReplace(out, "\\", "\\\\");
   StringReplace(out, "\"", "\\\"");
   StringReplace(out, "\r", "\\r");
   StringReplace(out, "\n", "\\n");
   StringReplace(out, "\t", "\\t");
   return out;
}

string SF01_CsvEscape(const string value)
{
   string out = value;
   StringReplace(out, "\"", "\"\"");
   return "\"" + out + "\"";
}

string SF01_CanonicalDouble(const double value, const int digits = 10)
{
   return DoubleToString(value, digits);
}

string SF01_CanonicalBool(const bool value)
{
   return value ? "true" : "false";
}

bool SF01_IsSafeIdentifier(const string value, const int max_length = 128)
{
   const int count = StringLen(value);
   if(count <= 0 || count > max_length) return false;
   if(!SF01_IsAscii(value)) return false;
   for(int i = 0; i < count; i++)
   {
      const int c = StringGetCharacter(value, i);
      const bool ok = (c >= 'a' && c <= 'z') ||
                      (c >= 'A' && c <= 'Z') ||
                      (c >= '0' && c <= '9') ||
                      c == '_' || c == '-' || c == '.' || c == ':' || c == '/';
      if(!ok) return false;
   }
   return true;
}

// Terminal symbols are broker transport identifiers, not schema identifiers.
// Common MT5 symbols include #US30, NQ.cash, ES-m, GOLD@, and similar forms.
bool SF01_IsSafeTerminalSymbol(const string value, const int max_length = 64)
{
   const int count = StringLen(value);
   if(count <= 0 || count > max_length) return false;
   if(!SF01_IsAscii(value)) return false;
   for(int i = 0; i < count; i++)
   {
      const int c = StringGetCharacter(value, i);
      if(c <= 32 || c == '|' || c == ',' || c == ';' || c == '"' || c == '\\')
         return false;
   }
   return true;
}

// Compatibility alias retained because Strategy Factory phases 08-17 use the concise name.
// The implementation delegates to the canonical transport-symbol validator above.
bool SF01_IsTerminalSymbol(const string value, const int max_length = 64)
{
   return SF01_IsSafeTerminalSymbol(value, max_length);
}

#endif
