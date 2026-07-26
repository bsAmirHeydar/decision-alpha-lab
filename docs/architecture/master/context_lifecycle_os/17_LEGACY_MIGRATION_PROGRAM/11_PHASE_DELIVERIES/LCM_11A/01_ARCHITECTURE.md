# LCM-11A Architecture

The phase has four layers: source discovery, semantic classification, contract freeze and evidence publication. Source discovery parses MQL5 object creation and buffer binding calls plus bounded report-output APIs. Semantic classification determines owner, subsystem, source-event class, chart scope and active status without rewriting source behavior. Contract freeze creates one namespace, anchor and lifecycle contract per visual surface. Evidence publication seals registries, blockers, collision reports and handoff records with deterministic digests.

The visual layer is strictly downstream. It may consume canonical Context, Setup, Treatment, research-observation or report events, but it cannot mutate those records or become evidence authority.
