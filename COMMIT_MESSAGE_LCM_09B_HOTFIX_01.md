Fix LCM-09B Windows reproducibility verification

- normalize textual source bindings to LF for cross-platform SHA-256 checks
- preserve byte-exact hashing for binary artifacts
- verify repeated clean builds at the same deterministic target
- compare committed and rebuilt publication wrappers by stable semantics
- add Windows reproducibility documentation and regression coverage
