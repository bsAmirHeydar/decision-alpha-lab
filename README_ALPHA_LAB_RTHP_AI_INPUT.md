# Alpha Lab RTHP AI-Engine Input Binding

## Release purpose

This patch supplies every RTHP-specific input required by the existing Strategy Factory / SAED / UCEE engine while preserving the central engine and the approved canonical RTHP Context unchanged.

It does not redesign the engine. It implements the engine's existing `ContextPackage` contract, generates the standard UCE-I16 scaffold, registers RTHP-specific schemas and catalogs, declares known-time-safe features and views, binds dependence clusters, declares research tasks and post-cut labels, and provides deterministic smoke and real-data preflight evidence.

## Frozen semantic dependency

- Canonical Context ID: `CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1`
- Canonical Context version: `1.0.2`
- Required lifecycle state: `CONTEXT_COMPILED`
- AI package: `rthp.cross_symbol_cycle_divergence@1.0.0`

The patch contains no files under the canonical semantic Context root. This preserves the ACL-03 approved source digest and deterministic recompilation.

## Engine contract implemented

The additive plugin implements the existing `strategy_factory_contexts_v3.ContextPackage` interface:

- package manifest;
- 31 feature descriptors;
- 5 representation views;
- 4 dependence-cluster rules;
- 30 research task references;
- canonical source-record validation;
- deterministic `ContextObservation` mapping;
- deterministic `FeatureFrame` materialization.

## Research surface

The task and label contracts support:

- reference exhaustion and survival;
- Hunter and Protected polarity-signed forward returns;
- polarity-aligned direction;
- MFE and MAE;
- family-relative strength;
- reference-age effectiveness;
- sequential versus non-sequential comparison;
- versioned cycle and confirmation discovery.

All future outcomes are label-only and are excluded from Context features.

## Engine invariance

Protected shared namespaces include the Context SDK, dataset builder, trainers, onboarding, experiments, contracts, economics, promotion, policy, runtime, ACL tools, and ACL registries. The committed extended snapshot covers 1,398 protected files. The expected and observed result is:

```text
changed_core_paths = []
central_engine_modified = false
canonical_context_modified = false
status = PASS
```

## Readiness state

### Ready

- Context package registration
- canonical source schema
- observation mapping
- feature materialization
- view compilation
- cluster assignment
- task and label binding contracts
- UCE-I16 generated scaffold
- smoke preflight
- shared-engine regression compatibility
- ACL-05 handoff contract

### Intentionally blocked

Real training remains blocked by `RTHP_REAL_DATA_BINDING_REQUIRED` until immutable external source artifacts are supplied for:

1. canonical RTHP occurrences;
2. reference-state history;
3. cycle instances;
4. role-local post-cut price paths for labels only.

No real-data URI, hash, provider, entitlement, symbol pair, date range, or rollover policy is fabricated by this patch.

## Non-authorities

This patch creates no entry, stop, target, position-size, order, broker-write, capital, promotion, or production authority. It does not unseal final tests and does not bypass ACL-05/ACL-07 governance.

## Main paths

```text
lab/11_strategy_factory/python/strategy_factory_rthp_context_v1/
lab/11_strategy_factory/generated_contexts/rthp_cross_symbol_cycle_divergence/
registry/strategy_factory/contexts/rthp/v1/
lab/11_strategy_factory/tests/rthp_ai_input/
docs/alpha_lab_master_architecture/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_03/RTHP/
```

See the generated acceptance, train-readiness, Context-immutability, and Engine-invariance reports under:

```text
lab/11_strategy_factory/generated_contexts/rthp_cross_symbol_cycle_divergence/ai_input/generated/
```
