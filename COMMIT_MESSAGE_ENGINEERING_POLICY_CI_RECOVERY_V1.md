fix(ci): restore canonical engineering preflight

- bind the Obsidian policy stage to the LCM-15B canonical vault
- require canonical policy entry points instead of generated redirects
- upgrade checkout and setup-python to Node 24 action majors
- add focused regression coverage for runner, policy and workflow wiring
- document root cause, invariants, verification, rollback and residual risk

Verification:
- 3 focused tests passed
- canonical vault: 253 notes, 247 IDs, 0 errors, 0 warnings
- repository preflight: all four stages passed
- selected clean base-plus-patch archive: focused tests and vault validation passed
