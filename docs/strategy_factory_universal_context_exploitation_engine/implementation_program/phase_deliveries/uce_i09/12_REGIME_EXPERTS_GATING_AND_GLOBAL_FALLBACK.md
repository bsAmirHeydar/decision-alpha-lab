# Regime Experts, Gating, and Global Fallback

Regime-specific experts are useful only when regimes are known causally and have enough support. The gate takes a context row, estimates or resolves a regime, checks support, and selects either an exact expert or the global model.

The native centroid gate is an auditable baseline. Later mixture-of-experts gates may be added in UCE-I10. Every assignment records probability, support count, fallback usage, and reason. Sparse regimes cannot force a specialist.

Fallback policies are global model, nearest supported regime, or abstention. The policy is versioned. Regime definitions, gate model, expert versions, and fallback are all part of release identity.
