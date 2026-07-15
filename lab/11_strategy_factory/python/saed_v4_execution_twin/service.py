from __future__ import annotations
from .models import ExecutionTwinProfile
from .serialization import load_json
from .twin import build_execution_twin


def build_from_files(cube_path, handoff_path, profile_path):
    cube = load_json(cube_path); handoff = load_json(handoff_path); profile = ExecutionTwinProfile.from_mapping(load_json(profile_path))
    return build_execution_twin(cube, handoff, profile)
