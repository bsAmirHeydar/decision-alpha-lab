# ADR I09-002 — Offline Policy Learning Cannot Create Actions

## Decision

The bounded policy learner operates over a frozen finite treatment set and rejects unseen actions.

## Consequence

The engine avoids unsupported extrapolation and keeps all executable behavior inside reviewed treatment atoms and compiled policies.
