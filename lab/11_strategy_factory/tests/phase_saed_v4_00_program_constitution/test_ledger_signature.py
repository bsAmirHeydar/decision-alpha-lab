import pytest
from saed_v4_constitution.ledger import HashChainLedger,LedgerEntry
from saed_v4_constitution.signatures import HMACSHA256Signer,SignatureEnvelope
from saed_v4_constitution.errors import IntegrityViolation

def test_hash_chain_roundtrip():
 l=HashChainLedger(); l.append('2026-07-13T00:00:00Z','decision',{'x':1}); l.append('2026-07-13T00:01:00Z','review',{'x':2}); assert l.verify()

def test_hash_chain_detects_tamper():
 l=HashChainLedger(); a=l.append('2026-07-13T00:00:00Z','decision',{'x':1})
 bad=LedgerEntry(a.sequence,a.known_time,a.event_type,'f'*64,a.previous_hash,a.entry_hash)
 with pytest.raises(IntegrityViolation): HashChainLedger([bad])

def test_hmac_reference_signer():
 s=HMACSHA256Signer('k',b'secret'); e=s.sign_hash('a'*64); assert s.verify(e)

def test_hmac_wrong_signature_rejected():
 s=HMACSHA256Signer('k',b'secret'); e=SignatureEnvelope(s.algorithm,'k','a'*64,'0'*64); assert not s.verify(e)

def test_hmac_wrong_key_id_rejected():
 s=HMACSHA256Signer('k',b'secret'); e=s.sign_hash('a'*64); other=HMACSHA256Signer('other',b'secret'); assert not other.verify(e)
