# ADR 0201 — Thin Host, Not Monolith

The Strategy Host is a composition root and lifecycle forwarder. Strategy semantics, candidate policies, statistics, risk and execution stay outside the Host. This is accepted to prevent one central EA from becoming the new duplication point.