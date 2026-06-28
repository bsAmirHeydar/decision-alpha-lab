#!/usr/bin/env python3
"""Generate offline runtime codes for FlagCounting Phoenix.

This mirrors FP_LicenseCrypto.mqh. Keep this file private; do not ship it to
license recipients. The recipient only receives:
  - InpPhaseModelProfile
  - InpRenderMemo
  - InpNodeModelSeed
  - InpBoundaryModelSeed
  - InpValidationModelSeed
  - InpReleaseModelSeed
"""
from __future__ import annotations

import argparse
import secrets
from dataclasses import dataclass

MASK = 0xFFFFFFFF
TOKEN_PREFIX = "FCPHX1"
PRODUCT_ID = "FCPHX"


def u32(x: int) -> int:
    return x & MASK


def rotl32(x: int, r: int) -> int:
    x = u32(x)
    return u32((x << r) | (x >> (32 - r)))


def mix32(x: int) -> int:
    x = u32(x)
    x ^= x >> 16
    x = u32(x * 0x7FEB352D)
    x ^= x >> 15
    x = u32(x * 0x846CA68B)
    x ^= x >> 16
    return u32(x)


def h32(s: str, seed: int = 2166136261) -> int:
    h = u32(seed)
    for ch in s:
        h ^= ord(ch)
        h = u32(h * 16777619)
        h = u32(rotl32(h, 5) ^ (h >> 7))
    return mix32(h ^ len(s))


def hx(x: int) -> str:
    return f"{u32(x):08X}"


def secret_a() -> str:
    a = mix32(0x51D4A11A ^ h32("phoenix", 0xA341316C))
    b = mix32(0xC8013EA4 ^ h32("flag-count", 0x8013EA4D))
    c = mix32(0xAD90777D ^ h32("dal", 0x9E3779B9))
    return f"{hx(a)}:{hx(b)}:{hx(c)}"


def secret_b() -> str:
    a = mix32(0xB7E15162 ^ h32("nd-hook", 0xC2B2AE35))
    b = mix32(0x8AED2A6B ^ h32("f1-f2-f3", 0x27D4EB2F))
    c = mix32(0x165667B1 ^ h32("offline", 0x85EBCA6B))
    return f"{hx(a)}:{hx(b)}:{hx(c)}"


def signatures(payload: str, passphrase: str) -> tuple[str, str]:
    p = payload + "|" + passphrase
    a = h32(secret_a() + "|" + p, 0x811C9DC5)
    b = h32(secret_b() + "|" + p[::-1], 0x9E3779B9)
    a = mix32(a ^ rotl32(b, 13))
    b = mix32(b ^ rotl32(a, 7))
    return hx(a), hx(b)


def gate_value(payload: str, passphrase: str, gate_index: int) -> int:
    sig_a, sig_b = signatures(payload, passphrase)
    material = f"{payload}|{passphrase}|{sig_a}|{sig_b}|G{gate_index}"
    h = h32(secret_b() + "|" + material, 0xA5A5A5A5 + gate_index * 977)
    return 100000 + (h % 900000)


def server_hash(server: str) -> str:
    return hx(h32(server.strip().upper(), 0xC3D2E1F0))


@dataclass
class LicenseBundle:
    token: str
    passphrase: str
    gate_a: int
    gate_b: int
    gate_c: int
    gate_d: int
    server_hash: str


def build_license(account: int, server: str, expires: int, passphrase: str,
                  feature: str, nonce: str, server_any: bool) -> LicenseBundle:
    srv_hash = "ANY" if server_any else server_hash(server)
    payload = f"{TOKEN_PREFIX}|{PRODUCT_ID}|{account}|{srv_hash}|{expires}|{feature.upper()}|{nonce.upper()}"
    sig_a, sig_b = signatures(payload, passphrase)
    token = f"{payload}|{sig_a}|{sig_b}"
    return LicenseBundle(
        token=token,
        passphrase=passphrase,
        gate_a=gate_value(payload, passphrase, 1),
        gate_b=gate_value(payload, passphrase, 2),
        gate_c=gate_value(payload, passphrase, 3),
        gate_d=gate_value(payload, passphrase, 4),
        server_hash=srv_hash,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--account", type=int, required=True, help="MT5 account login")
    ap.add_argument("--server", default="", help="Exact MT5 AccountInfoString(ACCOUNT_SERVER)")
    ap.add_argument("--server-any", action="store_true", help="Do not bind to server hash")
    ap.add_argument("--expires", type=int, required=True, help="YYYYMMDD expiry date")
    ap.add_argument("--feature", default="FULL")
    ap.add_argument("--passphrase", default="", help="Human password. Omit for generated password")
    ap.add_argument("--nonce", default="", help="Optional public nonce")
    args = ap.parse_args()

    if not args.server_any and not args.server.strip():
        raise SystemExit("--server is required unless --server-any is used")

    passphrase = args.passphrase or secrets.token_urlsafe(18)
    nonce = args.nonce or secrets.token_hex(5).upper()
    b = build_license(args.account, args.server, args.expires, passphrase, args.feature, nonce, args.server_any)

    print("Give these values to the recipient:")
    print(f"InpPhaseModelProfile={b.token}")
    print(f"InpRenderMemo={b.passphrase}")
    print(f"InpNodeModelSeed={b.gate_a}")
    print(f"InpBoundaryModelSeed={b.gate_b}")
    print(f"InpValidationModelSeed={b.gate_c}")
    print(f"InpReleaseModelSeed={b.gate_d}")
    print("")
    print("Issuer audit:")
    print(f"account={args.account}")
    print(f"server_hash={b.server_hash}")
    print(f"expires={args.expires}")
    print(f"feature={args.feature.upper()}")


if __name__ == "__main__":
    main()
