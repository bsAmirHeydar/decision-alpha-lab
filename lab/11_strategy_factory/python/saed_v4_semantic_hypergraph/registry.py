from __future__ import annotations

from .authority import validate_authority
from .errors import RegistryError
from .models import GraphBuildPolicy, RelationDefinition, SemanticRegistry


PROHIBITED_SELECTOR_TOKENS = (
    "future",
    "target",
    "label",
    "outcome",
    "realized_pnl",
    "forward_return",
)


def validate_registry(registry: SemanticRegistry) -> None:
    validate_authority(registry.authority)
    if not registry.registry_name or not registry.exact_version:
        raise RegistryError("registry name and exact version are required")
    node_kinds = [item.kind for item in registry.node_types]
    relation_kinds = [item.kind for item in registry.relations]
    if len(node_kinds) != len(set(node_kinds)):
        raise RegistryError("duplicate node kind definition")
    if len(relation_kinds) != len(set(relation_kinds)):
        raise RegistryError("duplicate relation definition")
    for definition in registry.relations:
        _validate_relation(definition)
    seen_rules: set[str] = set()
    for rule in registry.rules:
        if rule.rule_name in seen_rules:
            raise RegistryError(f"duplicate semantic rule: {rule.rule_name}")
        seen_rules.add(rule.rule_name)
        if rule.relation_kind not in relation_kinds:
            raise RegistryError(f"rule {rule.rule_name} references unknown relation kind")
        if rule.minimum_members < 2:
            raise RegistryError(f"rule {rule.rule_name} minimum_members must be at least two")
        if not rule.selectors:
            raise RegistryError(f"rule {rule.rule_name} requires selectors")
        selector_keys = [selector.key for selector in rule.selectors]
        if len(selector_keys) != len(set(selector_keys)):
            raise RegistryError(f"rule {rule.rule_name} contains duplicate selectors")
        for selector in rule.selectors:
            lowered = selector.key.lower()
            if any(token in lowered for token in PROHIBITED_SELECTOR_TOKENS):
                raise RegistryError(f"rule {rule.rule_name} uses prohibited selector token")


def _validate_relation(definition: RelationDefinition) -> None:
    if definition.minimum_arity < 2:
        raise RegistryError(f"relation {definition.kind.value} minimum arity must be at least two")
    if definition.maximum_arity < definition.minimum_arity:
        raise RegistryError(f"relation {definition.kind.value} maximum arity is invalid")
    if not definition.allowed_node_kinds:
        raise RegistryError(f"relation {definition.kind.value} requires allowed node kinds")


def validate_policy(policy: GraphBuildPolicy) -> None:
    if not policy.policy_name or not policy.exact_version:
        raise RegistryError("policy name and exact version are required")
    if not 0.0 <= policy.minimum_feature_quality <= 1.0:
        raise RegistryError("minimum_feature_quality must be in [0,1]")
    if policy.maximum_nodes < 1 or policy.maximum_edges < 1:
        raise RegistryError("graph budgets must be positive")
    if policy.maximum_edge_arity < 2:
        raise RegistryError("maximum_edge_arity must be at least two")
    if policy.deterministic_partition_count < 1:
        raise RegistryError("deterministic_partition_count must be positive")
    lowered = [token.strip().lower() for token in policy.prohibited_feature_tokens]
    if any(not token for token in lowered):
        raise RegistryError("prohibited feature tokens cannot be empty")
