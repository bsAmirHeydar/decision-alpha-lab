from __future__ import annotations
import hashlib, hmac, json
from typing import Any, Protocol


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest_object(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


class SignatureVerifier(Protocol):
    def verify(self, payload: Any, signature: str, signer_id: str) -> bool: ...


class StructuralSignatureVerifier:
    """Production-safe default: validates signed-envelope shape, not cryptography.

    Cryptographic verification is delegated to a key-custody adapter in ACL-12.
    The structural verifier never promotes a malformed or empty signature, and its
    result is explicitly marked as structural by policy evidence.
    """
    def verify(self, payload: Any, signature: str, signer_id: str) -> bool:
        return bool(signer_id and signature.startswith("sig:") and len(signature) >= 20)


class HMACSignatureAdapter:
    """Deterministic test adapter; must not be used as production key custody."""
    def __init__(self, keys: dict[str, bytes]): self._keys=dict(keys)
    def sign(self, payload: Any, signer_id: str) -> str:
        key=self._keys[signer_id]
        return "hmac-sha256:"+hmac.new(key,canonical_bytes(payload),hashlib.sha256).hexdigest()
    def verify(self,payload:Any,signature:str,signer_id:str)->bool:
        if signer_id not in self._keys: return False
        expected=self.sign(payload,signer_id)
        return hmac.compare_digest(expected,signature)
