from .conftest import j
def test_upstream_digest_is_exact():assert j("handoff/lcm10b_to_lcm10c_handoff.json")["upstream_handoff_digest"]=="sha256:6f513e66cc269c963e7380429b82ea78e0fba7812a3ec50fde1070e3c9c5c14b"
