from __future__ import annotations

from .canonical import stable_id
from .enums import DiffClass
from .models import DslDiff, TreatmentDslPackage


def semantic_diff(left: TreatmentDslPackage, right: TreatmentDslPackage) -> DslDiff:
    left_programs = {item.program_id: item.program_hash for item in left.programs}
    right_programs = {item.program_id: item.program_hash for item in right.programs}
    left_bindings = {item.binding_id: item.binding_hash for item in left.bindings}
    right_bindings = {item.binding_id: item.binding_hash for item in right.bindings}
    added = tuple(sorted(set(right_programs) - set(left_programs)))
    removed = tuple(sorted(set(left_programs) - set(right_programs)))
    changed = tuple(sorted(key for key in set(left_programs) & set(right_programs) if left_programs[key] != right_programs[key]))
    changed_bindings = tuple(sorted(
        set(left_bindings) ^ set(right_bindings)
        | {key for key in set(left_bindings) & set(right_bindings) if left_bindings[key] != right_bindings[key]}
    ))
    if left.package_hash == right.package_hash:
        classification = DiffClass.IDENTICAL
    elif not (added or removed or changed or changed_bindings):
        classification = DiffClass.METADATA_ONLY
    else:
        classification = DiffClass.SEMANTIC
    payload = {
        "left_package_hash": left.package_hash,
        "right_package_hash": right.package_hash,
        "classification": classification.value,
        "added_program_ids": added,
        "removed_program_ids": removed,
        "changed_program_ids": changed,
        "changed_binding_ids": changed_bindings,
    }
    return DslDiff(stable_id("dsldiff", payload), left.package_hash, right.package_hash, classification, added, removed, changed, changed_bindings)
