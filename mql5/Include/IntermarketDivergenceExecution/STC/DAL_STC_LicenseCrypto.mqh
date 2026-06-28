#ifndef __DAL_STC_LICENSE_CRYPTO_MQH__
#define __DAL_STC_LICENSE_CRYPTO_MQH__
#property strict

#include "DAL_STC_LicenseTypes.mqh"

// ============================================================================
// Decision Alpha Lab - STC/SMT Cycles Offline License Hash / Signature Helpers
// ----------------------------------------------------------------------------
// This is not public-key cryptography. It is a hardened offline signature gate
// for EX5 distribution: product/account/server/expiry/password/gates must all
// agree with the compiled secret. Offline client-side licensing is never
// mathematically unbreakable, but this makes casual copying and sharing hard.
// ============================================================================

uint STC_LicRotL32(const uint x, const int r)
{
   return (uint)((x << r) | (x >> (32 - r)));
}

uint STC_LicMix32(uint x)
{
   x ^= (x >> 16);
   x *= (uint)0x7feb352d;
   x ^= (x >> 15);
   x *= (uint)0x846ca68b;
   x ^= (x >> 16);
   return x;
}

uint STC_LicHash32(const string s, const uint seed=2166136261)
{
   uint h = seed;
   int n = StringLen(s);
   for(int i=0; i<n; i++)
   {
      uint c = (uint)StringGetCharacter(s, i);
      h ^= c;
      h *= (uint)16777619;
      h = STC_LicRotL32(h, 5) ^ (h >> 7);
   }
   return STC_LicMix32(h ^ (uint)n);
}

string STC_LicHexNibble(const int v)
{
   if(v < 10) return IntegerToString(v);
   if(v == 10) return "A";
   if(v == 11) return "B";
   if(v == 12) return "C";
   if(v == 13) return "D";
   if(v == 14) return "E";
   return "F";
}

string STC_LicHex8(uint x)
{
   string out = "";
   for(int shift=28; shift>=0; shift-=4)
   {
      int v = (int)((x >> shift) & 0x0F);
      out += STC_LicHexNibble(v);
   }
   return out;
}

string STC_LicUpperTrim(string s)
{
   StringTrimLeft(s);
   StringTrimRight(s);
   StringToUpper(s);
   return s;
}

string STC_LicReverse(const string s)
{
   string out = "";
   for(int i=StringLen(s)-1; i>=0; i--)
      out += StringSubstr(s, i, 1);
   return out;
}

string STC_LicSecretA()
{
   // Split constants to avoid one obvious literal secret in the compiled binary.
   uint a = STC_LicMix32((uint)0x6C79636C ^ STC_LicHash32("stc-smt", (uint)0xA341316C));
   uint b = STC_LicMix32((uint)0xD1A7E617 ^ STC_LicHash32("time-divergence", (uint)0x8013EA4D));
   uint c = STC_LicMix32((uint)0xC5C1E501 ^ STC_LicHash32("dal-cycles", (uint)0x9E3779B9));
   return STC_LicHex8(a) + ":" + STC_LicHex8(b) + ":" + STC_LicHex8(c);
}

string STC_LicSecretB()
{
   uint a = STC_LicMix32((uint)0xB7E15162 ^ STC_LicHash32("w-levels", (uint)0xC2B2AE35));
   uint b = STC_LicMix32((uint)0x8AED2A6B ^ STC_LicHash32("smt-hunts", (uint)0x27D4EB2F));
   uint c = STC_LicMix32((uint)0x165667B1 ^ STC_LicHash32("offline-exec", (uint)0x85EBCA6B));
   return STC_LicHex8(a) + ":" + STC_LicHex8(b) + ":" + STC_LicHex8(c);
}

void STC_LicSignatures(const string canonical_payload,
                       const string passphrase,
                       string &sig_a,
                       string &sig_b)
{
   string p = canonical_payload + "|" + passphrase;
   uint a = STC_LicHash32(STC_LicSecretA() + "|" + p, (uint)0x811C9DC5);
   uint b = STC_LicHash32(STC_LicSecretB() + "|" + STC_LicReverse(p), (uint)0x9E3779B9);
   a = STC_LicMix32(a ^ STC_LicRotL32(b, 13));
   b = STC_LicMix32(b ^ STC_LicRotL32(a, 7));
   sig_a = STC_LicHex8(a);
   sig_b = STC_LicHex8(b);
}

long STC_LicGateValue(const string canonical_payload,
                      const string passphrase,
                      const int gate_index)
{
   string sig_a, sig_b;
   STC_LicSignatures(canonical_payload, passphrase, sig_a, sig_b);
   string material = canonical_payload + "|" + passphrase + "|" + sig_a + "|" + sig_b + "|G" + IntegerToString(gate_index);
   uint seed = (uint)0xA5A5A5A5;
   seed += (uint)(gate_index * 977);
   uint h = STC_LicHash32(STC_LicSecretB() + "|" + material, seed);
   long v = 100000 + (long)(h % 900000);
   return v;
}

string STC_LicServerHash(const string server)
{
   string s = STC_LicUpperTrim(server);
   return STC_LicHex8(STC_LicHash32(s, (uint)0xC3D2E1F0));
}

#endif // __DAL_STC_LICENSE_CRYPTO_MQH__
