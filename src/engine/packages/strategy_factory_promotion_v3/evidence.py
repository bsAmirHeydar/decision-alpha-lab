"""Evidence-bundle assembly and detached HMAC verification boundary."""
from __future__ import annotations
import hashlib,hmac
from dataclasses import replace
from typing import Mapping
from .canonical import canonical_json, canonical_sha256, stable_id
from .contracts import EvidenceBundle
from .errors import PromotionError

def build_bundle(*, candidate_key:str, universe_hash:str, policy_hash:str, artifact_hashes:Mapping[str,str], generated_known_time_ms:int, signer_key_id:str, version:str="1.0.0")->EvidenceBundle:
    payload={"candidate_key":candidate_key,"universe_hash":universe_hash,"policy_hash":policy_hash,"artifacts":dict(sorted(artifact_hashes.items())),"known_time":generated_known_time_ms,"signer":signer_key_id,"version":version}
    return EvidenceBundle(bundle_id=stable_id("evidence",payload),bundle_version=version,candidate_key=candidate_key,universe_hash=universe_hash,policy_hash=policy_hash,artifact_hashes=dict(sorted(artifact_hashes.items())),generated_known_time_ms=generated_known_time_ms,signer_key_id=signer_key_id)

def sign_bundle(bundle:EvidenceBundle, secret:bytes)->EvidenceBundle:
    if not secret: raise PromotionError("empty_signing_key","signing key cannot be empty")
    signature=hmac.new(secret,canonical_json(bundle.unsigned_payload).encode("utf-8"),hashlib.sha256).hexdigest(); return replace(bundle,signature=signature)

def verify_bundle(bundle:EvidenceBundle, secret:bytes)->bool:
    if not bundle.signature:return False
    expected=hmac.new(secret,canonical_json(bundle.unsigned_payload).encode("utf-8"),hashlib.sha256).hexdigest(); return hmac.compare_digest(bundle.signature,expected)

def artifact_integrity(bundle:EvidenceBundle, actual_hashes:Mapping[str,str])->Mapping[str,object]:
    expected=dict(bundle.artifact_hashes); missing=sorted(set(expected)-set(actual_hashes)); extra=sorted(set(actual_hashes)-set(expected)); mismatched=sorted(k for k in set(expected)&set(actual_hashes) if expected[k]!=actual_hashes[k]); payload={"passed":not missing and not extra and not mismatched,"missing":missing,"extra":extra,"mismatched":mismatched}
    return {**payload,"evidence_hash":canonical_sha256(payload)}
