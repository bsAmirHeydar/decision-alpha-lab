#!/usr/bin/env python3
"""Generate and archive offline runtime codes for FlagCounting Phoenix.

Keep this file private; do not ship it to license recipients.

The recipient only receives the neutral MT5 input values:
  - InpPhaseModelProfile
  - InpRenderMemo
  - InpNodeModelSeed
  - InpBoundaryModelSeed
  - InpValidationModelSeed
  - InpReleaseModelSeed

By default this issuer tool also archives every issued license under:
  licenses/user0001-First-Middle-Last/

Committed repository policy:
  - Keep licenses/README_LICENSE_ISSUER.md in git as the guide.
  - Do not commit generated user folders.
"""
from __future__ import annotations

import argparse
import json
import re
import secrets
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

MASK = 0xFFFFFFFF
TOKEN_PREFIX = "FCPHX1"
PRODUCT_ID = "FCPHX"
DEFAULT_OUT_ROOT = "licenses"


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
    payload: str
    sig_a: str
    sig_b: str


@dataclass
class IssuerRecord:
    user_code: str
    first_name: str
    middle_name: str
    last_name: str
    display_name: str
    account: int
    server: str
    server_any: bool
    server_hash: str
    expires: int
    feature: str
    nonce: str
    issued_at_utc: str
    output_folder: str
    recipient_inputs_file: str
    issuer_audit_file: str
    full_record_file: str
    token_prefix: str
    product_id: str
    signature_a: str
    signature_b: str


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
        payload=payload,
        sig_a=sig_a,
        sig_b=sig_b,
    )


def slug_part(value: str) -> str:
    value = value.strip()
    if not value:
        return "NA"
    # Keep readable Latin names. Replace whitespace/unsafe chars with hyphens.
    value = re.sub(r"[^A-Za-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "NA"


def next_user_code(out_root: Path) -> str:
    out_root.mkdir(parents=True, exist_ok=True)
    max_n = 0
    pat = re.compile(r"^user(\d{4})(?:-|$)", re.IGNORECASE)
    for child in out_root.iterdir():
        if not child.is_dir():
            continue
        m = pat.match(child.name)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return f"user{max_n + 1:04d}"


def normalize_user_code(user_code: str, out_root: Path) -> str:
    user_code = user_code.strip()
    if not user_code:
        return next_user_code(out_root)
    if user_code.isdigit():
        return f"user{int(user_code):04d}"
    m = re.fullmatch(r"user(\d{1,4})", user_code, re.IGNORECASE)
    if m:
        return f"user{int(m.group(1)):04d}"
    raise SystemExit("--user-code must be empty, a number like 1, or user0001")


def user_folder_name(user_code: str, first_name: str, middle_name: str, last_name: str) -> str:
    parts = [user_code, slug_part(first_name)]
    if middle_name.strip():
        parts.append(slug_part(middle_name))
    parts.append(slug_part(last_name))
    return "-".join(parts)


def recipient_input_text(bundle: LicenseBundle) -> str:
    return "\n".join([
        "# Give only this section to the recipient.",
        "# The input names are intentionally neutral inside MT5.",
        f"InpPhaseModelProfile={bundle.token}",
        f"InpRenderMemo={bundle.passphrase}",
        f"InpNodeModelSeed={bundle.gate_a}",
        f"InpBoundaryModelSeed={bundle.gate_b}",
        f"InpValidationModelSeed={bundle.gate_c}",
        f"InpReleaseModelSeed={bundle.gate_d}",
        "",
    ])


def full_record_text(record: IssuerRecord, bundle: LicenseBundle) -> str:
    return "\n".join([
        "# FlagCounting Phoenix offline license full issuer record",
        "# Keep this file private. Do not send this full record to the recipient.",
        "",
        "[recipient_inputs]",
        recipient_input_text(bundle).strip(),
        "",
        "[issuer_audit]",
        f"user_code={record.user_code}",
        f"first_name={record.first_name}",
        f"middle_name={record.middle_name}",
        f"last_name={record.last_name}",
        f"display_name={record.display_name}",
        f"account={record.account}",
        f"server={record.server}",
        f"server_any={str(record.server_any).lower()}",
        f"server_hash={record.server_hash}",
        f"expires={record.expires}",
        f"feature={record.feature}",
        f"nonce={record.nonce}",
        f"issued_at_utc={record.issued_at_utc}",
        f"token_prefix={record.token_prefix}",
        f"product_id={record.product_id}",
        f"signature_a={record.signature_a}",
        f"signature_b={record.signature_b}",
        f"output_folder={record.output_folder}",
        "",
    ])


def write_license_files(out_root: Path, record: IssuerRecord, bundle: LicenseBundle, overwrite: bool) -> None:
    folder = Path(record.output_folder)
    if folder.exists() and not overwrite:
        raise SystemExit(f"Output folder already exists: {folder}. Use --overwrite to replace files.")
    folder.mkdir(parents=True, exist_ok=True)

    recipient_path = Path(record.recipient_inputs_file)
    audit_path = Path(record.issuer_audit_file)
    full_path = Path(record.full_record_file)

    recipient_path.write_text(recipient_input_text(bundle), encoding="utf-8")
    audit_path.write_text(json.dumps(asdict(record), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    full_path.write_text(full_record_text(record, bundle), encoding="utf-8")

    index_path = out_root / "issued_licenses_index.csv"
    index_exists = index_path.exists()
    with index_path.open("a", encoding="utf-8", newline="") as f:
        if not index_exists:
            f.write("user_code,display_name,account,server,server_hash,expires,feature,issued_at_utc,folder\n")
        safe_display = record.display_name.replace('"', '""')
        safe_server = record.server.replace('"', '""')
        f.write(
            f'{record.user_code},"{safe_display}",{record.account},"{safe_server}",{record.server_hash},'
            f'{record.expires},{record.feature},{record.issued_at_utc},"{folder.as_posix()}"\n'
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
    ap.add_argument("--first-name", required=True, help="Recipient first name, e.g. Amir")
    ap.add_argument("--middle-name", default="", help="Optional middle name, e.g. Hosein")
    ap.add_argument("--last-name", required=True, help="Recipient last name, e.g. Heydar")
    ap.add_argument("--user-code", default="", help="Optional user number/code: 1, 0001, or user0001. Default auto-increments.")
    ap.add_argument("--out-root", default=DEFAULT_OUT_ROOT, help="Issuer archive folder. Default: licenses")
    ap.add_argument("--no-save", action="store_true", help="Print only; do not archive files")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing user folder files")
    args = ap.parse_args()

    if not args.server_any and not args.server.strip():
        raise SystemExit("--server is required unless --server-any is used")

    out_root = Path(args.out_root)
    user_code = normalize_user_code(args.user_code, out_root)
    folder_name = user_folder_name(user_code, args.first_name, args.middle_name, args.last_name)
    output_folder = out_root / folder_name
    file_base = folder_name

    passphrase = args.passphrase or secrets.token_urlsafe(18)
    nonce = args.nonce or secrets.token_hex(5).upper()
    bundle = build_license(args.account, args.server, args.expires, passphrase, args.feature, nonce, args.server_any)

    display_parts = [args.first_name.strip()]
    if args.middle_name.strip():
        display_parts.append(args.middle_name.strip())
    display_parts.append(args.last_name.strip())
    display_name = " ".join(display_parts)
    issued_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    record = IssuerRecord(
        user_code=user_code,
        first_name=args.first_name.strip(),
        middle_name=args.middle_name.strip(),
        last_name=args.last_name.strip(),
        display_name=display_name,
        account=args.account,
        server="ANY" if args.server_any else args.server.strip(),
        server_any=bool(args.server_any),
        server_hash=bundle.server_hash,
        expires=args.expires,
        feature=args.feature.upper(),
        nonce=nonce.upper(),
        issued_at_utc=issued_at,
        output_folder=output_folder.as_posix(),
        recipient_inputs_file=(output_folder / f"{file_base}_recipient_inputs.txt").as_posix(),
        issuer_audit_file=(output_folder / f"{file_base}_issuer_audit.json").as_posix(),
        full_record_file=(output_folder / f"{file_base}_full_record.txt").as_posix(),
        token_prefix=TOKEN_PREFIX,
        product_id=PRODUCT_ID,
        signature_a=bundle.sig_a,
        signature_b=bundle.sig_b,
    )

    print("Give these values to the recipient:")
    print(f"InpPhaseModelProfile={bundle.token}")
    print(f"InpRenderMemo={bundle.passphrase}")
    print(f"InpNodeModelSeed={bundle.gate_a}")
    print(f"InpBoundaryModelSeed={bundle.gate_b}")
    print(f"InpValidationModelSeed={bundle.gate_c}")
    print(f"InpReleaseModelSeed={bundle.gate_d}")
    print("")
    print("Issuer audit:")
    print(f"user_code={record.user_code}")
    print(f"display_name={record.display_name}")
    print(f"account={args.account}")
    print(f"server_hash={bundle.server_hash}")
    print(f"expires={args.expires}")
    print(f"feature={args.feature.upper()}")

    if args.no_save:
        print("")
        print("Archive: disabled by --no-save")
    else:
        write_license_files(out_root, record, bundle, args.overwrite)
        print("")
        print("Archive written:")
        print(f"folder={record.output_folder}")
        print(f"recipient_inputs={record.recipient_inputs_file}")
        print(f"issuer_audit={record.issuer_audit_file}")
        print(f"full_record={record.full_record_file}")
        print(f"index={(out_root / 'issued_licenses_index.csv').as_posix()}")


if __name__ == "__main__":
    main()
