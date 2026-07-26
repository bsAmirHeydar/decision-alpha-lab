---
id: UCPS-04D7EA4D8A16
title: "Consumer Cutover Packet Template"
type: template
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Consumer Cutover Packet Template

```yaml
cutover_id: <CUTOVER-ID>
consumer_id: <stable consumer identity>
consumer_type: <python|mql5|ci|terminal|external|documentation>
old_interface: <reference>
new_interface: <reference>
baseline_evidence: []
rewrite_commit: <commit>
compatibility_shim: <none or ID>
telemetry_window: <definition>
parity_result: <PASS|FAILED|BLOCKED>
rollback: <command or record>
owner_attestation: <reference>
final_status: <canonical|quarantined>
```
