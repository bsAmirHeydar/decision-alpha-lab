#ifndef __SF01_HASH_MQH__
#define __SF01_HASH_MQH__

ulong SF01_Fnv1a64Utf16LE(const string value)
{
   ulong result = (((ulong)0xCBF29CE4) << 32) | (ulong)0x84222325;
   const ulong prime = (((ulong)0x00000100) << 32) | (ulong)0x000001B3;
   const int count = StringLen(value);
   for(int i = 0; i < count; i++)
   {
      const uint code = (uint)StringGetCharacter(value, i);
      const uint low_byte = code & 255;
      const uint high_byte = (code >> 8) & 255;
      result ^= (ulong)low_byte;
      result *= prime;
      result ^= (ulong)high_byte;
      result *= prime;
   }
   return result;
}

string SF01_UlongToHex16(ulong value)
{
   const string digits = "0123456789abcdef";
   string out = "";
   for(int i = 15; i >= 0; i--)
   {
      const int shift = i * 4;
      const int nibble = (int)((value >> shift) & (ulong)15);
      out += StringSubstr(digits, nibble, 1);
   }
   return out;
}

string SF01_StableId(const string prefix, const string canonical_payload)
{
   return prefix + "_" + SF01_UlongToHex16(SF01_Fnv1a64Utf16LE(canonical_payload));
}

#endif
