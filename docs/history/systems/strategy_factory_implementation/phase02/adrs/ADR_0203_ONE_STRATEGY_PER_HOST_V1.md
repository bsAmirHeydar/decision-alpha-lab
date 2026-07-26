# ADR 0203 — One Strategy per Host in V1

Although the platform will support portfolio mode, V1 closes one strategy at a time. This reduces cross-strategy state, correlation and failure complexity. Multi-strategy hosting is deferred until two independent pilots reuse the same core.