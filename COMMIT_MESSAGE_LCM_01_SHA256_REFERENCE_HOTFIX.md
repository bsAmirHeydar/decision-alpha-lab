fix(lcm): accept qualified SHA-256 baseline references

- accept both bare and sha256:-qualified baseline digests
- preserve strict 64-hex validation and fail-closed semantics
- add regression coverage for real LCM-00 manifest representation
- retain binary raw-byte and text EOL canonical verification boundaries
