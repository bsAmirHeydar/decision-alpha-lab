# LCM-01 Bidirectional EOL Integrity Hotfix

This corrective patch closes the remaining Windows/Linux verification asymmetry in LCM-01.

The frozen LCM-00 baseline contains both LF-authored and CRLF-authored text artifacts. A Windows or Git-normalized working tree can materialize either representation in the opposite line-ending form. The verifier now accepts a text artifact only when its frozen SHA-256 matches exactly one of three closed byte representations derived from the working-tree file:

1. raw bytes;
2. all-LF bytes;
3. all-CRLF bytes.

No whitespace trimming, encoding conversion, Unicode normalization, final-newline insertion/removal, semantic parsing, or binary normalization is allowed.

The apply script now checks every native process exit code and cannot commit or push after a failed verification or test command.
