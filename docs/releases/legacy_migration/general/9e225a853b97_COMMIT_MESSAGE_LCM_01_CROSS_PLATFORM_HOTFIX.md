fix(lcm): make LCM-01 installation integrity cross-platform

- preserve raw SHA-256 as the primary integrity authority
- accept CRLF working-tree materialization only when LF canonicalization matches the frozen digest
- deny binary canonicalization and semantic text changes
- add Windows checkout, mutation, binary, and path-escape regression coverage
- document the correction without modifying the frozen survey package
