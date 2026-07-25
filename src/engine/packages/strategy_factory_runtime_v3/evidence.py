from __future__ import annotations
from dataclasses import asdict
from .canonical import canonical_sha256

def build_evidence_bundle(manifest,certificate,failure_report,activation_receipt=None,limitations=()):
    payload={'manifest_hash':manifest.bundle_hash,'parity_certificate_hash':certificate.certificate_hash,'failure_report_hash':failure_report.report_hash,'activation_receipt_hash':activation_receipt.receipt_hash if activation_receipt else None,'limitations':list(limitations)}
    return {**payload,'evidence_hash':canonical_sha256(payload)}
def verify_evidence_bundle(bundle):
    payload={k:v for k,v in bundle.items() if k!='evidence_hash'}
    return bundle.get('evidence_hash')==canonical_sha256(payload)
