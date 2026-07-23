# Program closure decision

All gates are mandatory and non-compensatory. A deterministic failure yields `FAILED`; any UNKNOWN, BLOCKED or PARTIAL mandatory gate yields `BLOCKED`; only all-PASS evidence plus approvals yields `ACCEPTED`.

The current decision is `BLOCKED`. This state is valid and expected until the Windows/terminal and external-consumer evidence bundle is attached.
