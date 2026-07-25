from __future__ import annotations
import json
from pathlib import Path
from .models import ContextSnapshot,PriceObservation,OutcomePolicy
from .costs import CostRegistry
from .cube import build_cube

def load_json(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def build_from_files(lattice_path,handoff_path,context_path,path_path,policy_path,cost_registry_path,cost_model_id,cost_model_version):
    lattice=load_json(lattice_path);handoff=load_json(handoff_path);context=ContextSnapshot.from_mapping(load_json(context_path));observations=[PriceObservation.from_mapping(x) for x in load_json(path_path)['observations']];policy=OutcomePolicy.from_mapping(load_json(policy_path));registry=CostRegistry.from_mapping(load_json(cost_registry_path));return build_cube(lattice,handoff,context,observations,policy,registry,cost_model_id,cost_model_version)
