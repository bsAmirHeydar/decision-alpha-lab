from __future__ import annotations

from .canonical import content_hash, stable_id
from .models import DslPartitionManifest, TreatmentDslPackage


def deterministic_partition(package: TreatmentDslPackage, partition_count: int) -> DslPartitionManifest:
    if partition_count < 1:
        raise ValueError("partition_count must be positive")
    assignments = tuple(sorted(
        (program.program_id, int(content_hash(program.program_id)[:16], 16) % partition_count)
        for program in package.programs
    ))
    payload = {
        "package_id": package.package_id,
        "package_hash": package.package_hash,
        "partition_count": partition_count,
        "assignments": [{"program_id": key, "partition": value} for key, value in assignments],
    }
    manifest_id = stable_id("dslpartition", payload)
    return DslPartitionManifest(manifest_id, package.package_id, package.package_hash, partition_count, assignments, content_hash(payload))
