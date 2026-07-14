"""Detached integrity signatures.

HMAC is provided as a deterministic test/reference adapter. Production deployments
must replace it with an approved key-management and asymmetric-signature service.
"""
from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass


@dataclass(frozen=True)
class SignatureEnvelope:
    algorithm: str
    key_id: str
    payload_hash: str
    signature: str


class HMACSHA256Signer:
    algorithm = "HMAC-SHA256-REFERENCE-ONLY"

    def __init__(self, key_id: str, secret: bytes) -> None:
        if not secret:
            raise ValueError("secret must not be empty")
        self.key_id = key_id
        self.secret = secret

    def sign_hash(self, payload_hash: str) -> SignatureEnvelope:
        sig = hmac.new(self.secret, payload_hash.encode("ascii"), hashlib.sha256).hexdigest()
        return SignatureEnvelope(self.algorithm, self.key_id, payload_hash, sig)

    def verify(self, envelope: SignatureEnvelope) -> bool:
        if envelope.algorithm != self.algorithm or envelope.key_id != self.key_id:
            return False
        expected = hmac.new(self.secret, envelope.payload_hash.encode("ascii"), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, envelope.signature)
