fix(rthp-mt5): harden latest closed M1 discovery

- exclude the forming position-zero M1 bar
- retry while terminal history synchronizes
- record failed probe evidence
- add real-terminal regression coverage
- preserve Engine and Canonical Context boundaries
