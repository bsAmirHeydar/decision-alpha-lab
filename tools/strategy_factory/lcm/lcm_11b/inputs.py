from __future__ import annotations
from pathlib import Path
from .io import load_json
class LCM11AInputs:
    def __init__(self,root:Path):self.root=root
    def load(self):
        inv=load_json(self.root/"visual_object_inventory.json")
        ns=load_json(self.root/"visual_namespace_registry.json")
        bindings=load_json(self.root/"bindings/visual_source_event_binding_registry.json")
        anchors={load_json(p)["visual_object_id"]:load_json(p) for p in (self.root/"visual_anchor_contracts").glob("*.json")}
        lifecycles={load_json(p)["visual_object_id"]:load_json(p) for p in (self.root/"visual_lifecycle_contracts").glob("*.json")}
        blockers={p.stem:load_json(p) for p in (self.root/"blockers").glob("*.json")}
        return {"inventory":inv,"namespace_registry":ns,"binding_registry":bindings,"anchors":anchors,"lifecycles":lifecycles,"blockers":blockers}
