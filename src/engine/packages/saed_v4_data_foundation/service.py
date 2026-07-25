from __future__ import annotations
from pathlib import Path
from .content_store import ContentAddressedStore
from .schema_registry import SchemaRegistry
from .revisions import RevisionStore
from .quarantine import QuarantineRegistry
from .lineage import LineageGraph
from .catalog import ArtifactCatalog
from .ingestion import IngestionEngine
class SovereignDataFoundation:
    def __init__(self,content_root:str|Path):
        self.content=ContentAddressedStore(content_root); self.schemas=SchemaRegistry(); self.revisions=RevisionStore(); self.quarantine=QuarantineRegistry(); self.lineage=LineageGraph(); self.catalog=ArtifactCatalog(); self.ingestion=IngestionEngine(self.schemas,self.revisions,self.quarantine)
