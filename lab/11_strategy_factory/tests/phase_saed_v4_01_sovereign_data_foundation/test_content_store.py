import pytest
from saed_v4_data_foundation.content_store import ContentAddressedStore
from saed_v4_data_foundation.canonical import sha256_bytes

def test_put_get(tmp_path):
 s=ContentAddressedStore(tmp_path); h=s.put_bytes(b'abc'); assert h==sha256_bytes(b'abc'); assert s.get_bytes(h)==b'abc'
def test_idempotent_put(tmp_path):
 s=ContentAddressedStore(tmp_path); assert s.put_text('x')==s.put_text('x')
def test_has_verify(tmp_path):
 s=ContentAddressedStore(tmp_path); h=s.put_text('x'); assert s.has(h) and s.verify(h)
def test_missing(tmp_path):
 with pytest.raises(FileNotFoundError): ContentAddressedStore(tmp_path).get_bytes('0'*64)
def test_detect_corruption(tmp_path):
 s=ContentAddressedStore(tmp_path); h=s.put_text('x'); s._path(h).write_text('bad'); assert not s.verify(h)
