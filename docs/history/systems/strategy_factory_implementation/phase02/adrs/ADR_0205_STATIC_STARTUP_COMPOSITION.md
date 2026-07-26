# ADR 0205 — Static Startup Composition

No dynamic code discovery or runtime JSON parsing is allowed in the decision fast path. Plugins and configuration are validated and bound during initialization. A later compiler may generate immutable runtime generations.