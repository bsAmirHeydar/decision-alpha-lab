from __future__ import annotations
from datetime import datetime
from pathlib import Path
import json
from .dependency import DependencyEdge
from .lineage import LineageEdge
from .migrations import MigrationPlan
from .registry import RepositoryRegistry
from .types import ArtifactDescriptor


def load_registry(path:Path,policies)->RepositoryRegistry:
    obj=json.loads(path.read_text(encoding="utf-8")); reg=RepositoryRegistry(policies)
    reg.revision=int(obj.get("revision",0)); reg.owners=dict(obj.get("owners",{})); reg.schemas=dict(obj.get("schemas",{})); reg.plugins=dict(obj.get("plugins",{}))
    reg.artifacts={k:ArtifactDescriptor.from_dict(v) for k,v in obj.get("artifacts",{}).items()}; reg.aliases=dict(obj.get("aliases",{}))
    reg.dependencies=[DependencyEdge(**x) for x in obj.get("dependencies",[])]
    reg.lineage=[LineageEdge(x["edge_id"],x["source_artifact_id"],x["target_artifact_id"],x["edge_type"],x.get("transformation_id"),datetime.fromisoformat(x["recorded_at"].replace("Z","+00:00")),dict(x.get("metadata",{}))) for x in obj.get("lineage",[])]
    reg.migrations=[MigrationPlan(**x) for x in obj.get("migrations",[])]
    return reg


def save_registry(path:Path,registry:RepositoryRegistry):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(registry.snapshot(),indent=2,sort_keys=True)+"\n",encoding="utf-8")
