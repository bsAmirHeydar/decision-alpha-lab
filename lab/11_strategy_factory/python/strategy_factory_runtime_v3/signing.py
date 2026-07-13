from __future__ import annotations
import hashlib,hmac
from dataclasses import replace
from .canonical import canonical_bytes
from .contracts import RuntimeBundleManifest
from .errors import BundleValidationError

def sign_manifest(manifest:RuntimeBundleManifest,secret:bytes)->RuntimeBundleManifest:
    if not secret:raise BundleValidationError('empty_signing_secret','signing secret cannot be empty')
    sig=hmac.new(secret,canonical_bytes(manifest.unsigned_payload),hashlib.sha256).hexdigest()
    return replace(manifest,signature=sig)
def verify_manifest(manifest:RuntimeBundleManifest,secret:bytes)->bool:
    expected=hmac.new(secret,canonical_bytes(manifest.unsigned_payload),hashlib.sha256).hexdigest()
    return bool(manifest.signature) and hmac.compare_digest(expected,manifest.signature)
def require_valid_signature(manifest:RuntimeBundleManifest,secret:bytes)->None:
    if not verify_manifest(manifest,secret):raise BundleValidationError('signature_failure','runtime bundle signature invalid')
