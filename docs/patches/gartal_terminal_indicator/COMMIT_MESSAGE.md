feat(product-lab): add gartal terminal news indicator architecture

- add gartal terminal as a commercial MT5 news indicator product under product_lab
- add complete product specification for a Forex Factory style economic calendar terminal
- add luxury dashboard, filter panel, chart timeline, vertical event line, and alert engine design documents
- add data-source architecture for Forex Factory direct adapter, future API bridge, and local cache fallback
- add broker GMT auto/manual offset model and UTC-to-broker normalization doctrine
- add configurable currency, impact, speech, holiday, tentative, breaking, and date-range filter model
- add multi-stage alert design for 60m/30m/15m/5m/1m/pre-release/release/actual update workflows
- add validation plan for news days, high-impact events, broker GMT, WebRequest failures, cache fallback, and UI stress cases
- add MQL5 scaffold split into config, source client, parser, dashboard, timeline, and alert modules
- add Obsidian start page, product brief, UI board, algorithm map, release backlog, and canvas overview
- add release packaging helper script and Product Lab registry entry

This establishes gartal terminal as a sellable macro-news terminal product, separating the data adapter, parser, renderer, chart objects, and alert state so the source can evolve without rewriting the full indicator.
