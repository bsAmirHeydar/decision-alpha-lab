# MQL5 Module Architecture

- `DAYE_RenderTypes`: schemas and statuses
- `DAYE_RenderIdentity`: deterministic IDs, ownership, UTC→broker conversion
- `DAYE_RenderProjection`: period lookup and geometry
- `DAYE_RenderChartResolver`: Hunter-chart selection
- `DAYE_RenderObjectManager`: create, verify, repair, delete-owned-only
- `DAYE_RenderStore`: bounded projection evidence
- `DAYE_RenderEvents`: operational transitions
- `DAYE_RenderDiagnostics`: runtime formatting
- `DAYE_RenderAudit`: optional CSV
- `DAYE_RenderSelfTest`: embedded pure tests
- `DAYE_RenderEngine`: orchestration and sole render-state owner
- Expert: inputs, timer, lifecycle only
