#ifndef __FP_LICENSE_CRYPTO_MQH__
#define __FP_LICENSE_CRYPTO_MQH__
#property strict

#include "FP_LicenseTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Offline License Hash / Signature Helpers
// ----------------------------------------------------------------------------
// This is not public-key cryptography. It is a hardened offline signature gate
// for EX5 distribution: product/account/server/expiry/password/gates must all
// agree with the compiled secret. Offline client-side licensing is never
// mathematically unbreakable, but this makes casual copying and sharing hard.
// ============================================================================

uint FP_LicRotL32(const uint x, const int r)
{
   return (uint)((x << r) | (x >> (32 - r)));
}

uint FP_LicMix32(uint x)
{
   x ^= (x >> 16);
   x *= (uint)0x7feb352d;
   x ^= (x >> 15);
   x *= (uint)0x846ca68b;
   x ^= (x >> 16);
   return x;
}

uint FP_LicHash32(const string s, const uint seed=2166136261)
{
   uint h = seed;
   int n = StringLen(s);
   for(int i=0; i<n; i++)
   {
      uint c = (uint)StringGetCharacter(s, i);
      h ^= c;
      h *= (uint)16777619;
      h = FP_LicRotL32(h, 5) ^ (h >> 7);
   }
   return FP_LicMix32(h ^ (uint)n);
}

string FP_LicHexNibble(const int v)
{
   if(v < 10) return IntegerToString(v);
   if(v == 10) return "A";
   if(v == 11) return "B";
   if(v == 12) return "C";
   if(v == 13) return "D";
   if(v == 14) return "E";
   return "F";
}

string FP_LicHex8(uint x)
{
   string out = "";
   for(int shift=28; shift>=0; shift-=4)
   {
      int v = (int)((x >> shift) & 0x0F);
      out += FP_LicHexNibble(v);
   }
   return out;
}

string FP_LicUpperTrim(string s)
{
   StringTrimLeft(s);
   StringTrimRight(s);
   StringToUpper(s);
   return s;
}

string FP_LicReverse(const string s)
{
   string out = "";
   for(int i=StringLen(s)-1; i>=0; i--)
      out += StringSubstr(s, i, 1);
   return out;
}

string FP_LicSecretA()
{
   // Split constants to avoid one obvious literal secret in the compiled binary.
   uint a = FP_LicMix32((uint)0x51D4A11A ^ FP_LicHash32("phoenix", (uint)0xA341316C));
   uint b = FP_LicMix32((uint)0xC8013EA4 ^ FP_LicHash32("flag-count", (uint)0x8013EA4D));
   uint c = FP_LicMix32((uint)0xAD90777D ^ FP_LicHash32("dal", (uint)0x9E3779B9));
   return FP_LicHex8(a) + ":" + FP_LicHex8(b) + ":" + FP_LicHex8(c);
}

string FP_LicSecretB()
{
   uint a = FP_LicMix32((uint)0xB7E15162 ^ FP_LicHash32("nd-hook", (uint)0xC2B2AE35));
   uint b = FP_LicMix32((uint)0x8AED2A6B ^ FP_LicHash32("f1-f2-f3", (uint)0x27D4EB2F));
   uint c = FP_LicMix32((uint)0x165667B1 ^ FP_LicHash32("offline", (uint)0x85EBCA6B));
   return FP_LicHex8(a) + ":" + FP_LicHex8(b) + ":" + FP_LicHex8(c);
}

void FP_LicSignatures(const string canonical_payload,
                      const string passphrase,
                      string &sig_a,
                      string &sig_b)
{
   string p = canonical_payload + "|" + passphrase;
   uint a = FP_LicHash32(FP_LicSecretA() + "|" + p, (uint)0x811C9DC5);
   uint b = FP_LicHash32(FP_LicSecretB() + "|" + FP_LicReverse(p), (uint)0x9E3779B9);
   a = FP_LicMix32(a ^ FP_LicRotL32(b, 13));
   b = FP_LicMix32(b ^ FP_LicRotL32(a, 7));
   sig_a = FP_LicHex8(a);
   sig_b = FP_LicHex8(b);
}

long FP_LicGateValue(const string canonical_payload,
                     const string passphrase,
                     const int gate_index)
{
   string sig_a, sig_b;
   FP_LicSignatures(canonical_payload, passphrase, sig_a, sig_b);
   string material = canonical_payload + "|" + passphrase + "|" + sig_a + "|" + sig_b + "|G" + IntegerToString(gate_index);
   uint seed = (uint)0xA5A5A5A5;
   seed += (uint)(gate_index * 977);
   uint h = FP_LicHash32(FP_LicSecretB() + "|" + material, seed);
   long v = 100000 + (long)(h % 900000);
   return v;
}

string FP_LicServerHash(const string server)
{
   string s = FP_LicUpperTrim(server);
   return FP_LicHex8(FP_LicHash32(s, (uint)0xC3D2E1F0));
}

#endif // __FP_LICENSE_CRYPTO_MQH__
