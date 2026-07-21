from __future__ import annotations
from pathlib import Path
from typing import Any
from .canonical import digest_object
from .errors import AuthorityError,ContractError
from .io import load_json
class SetupFactoryReferencePort:
    """Read-only ACL-04 extension port for LCM reference registrations."""
    def __init__(self,registration_path:Path):
        doc=load_json(registration_path);self._doc=doc;self._by_id={x["setup_id"]:x for x in doc["registrations"]};self._validate()
    def _validate(self):
        if self._doc.get("factory_port")!="ACL04_LEGACY_REFERENCE_PORT_V1":raise ContractError("LCM09B_FACTORY_PORT_INVALID")
        if len(self._by_id)!=len(self._doc["registrations"]):raise ContractError("LCM09B_FACTORY_DUPLICATE_SETUP")
        for x in self._doc["registrations"]:
            for key in ("promotion_authority","runtime_authority","live_order_authority","capital_authority"):
                if x.get(key) is not False:raise AuthorityError(f"LCM09B_FACTORY_AUTHORITY:{key}")
            if x["registration_status"] not in {"REFERENCE_READY","REFERENCE_BLOCKED"}:raise ContractError("LCM09B_FACTORY_STATUS_INVALID")
        if digest_object(self._doc,"registration_digest")!=self._doc["registration_digest"]:raise ContractError("LCM09B_FACTORY_DIGEST_MISMATCH")
    def list_reference_candidates(self)->list[dict[str,Any]]:return [dict(x) for x in sorted(self._doc["registrations"],key=lambda v:v["setup_id"])]
    def get(self,setup_id:str)->dict[str,Any]:
        if setup_id not in self._by_id:raise KeyError(setup_id)
        return dict(self._by_id[setup_id])
