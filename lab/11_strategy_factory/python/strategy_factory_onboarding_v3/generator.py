from __future__ import annotations
from pathlib import Path
from .contracts import *
from .canonical import bytes_sha256,stable_id
from .templates import render_files
from .tournament_template import default_template,compile_template
from .capabilities import validate_capabilities
class ContextGenerator:
    VERSION='1.0.0'
    def build(self,spec:ContextSpecification,core_snapshot:CoreSnapshot)->tuple[ScaffoldManifest,dict[str,bytes],CompiledTournamentTemplate]:
        validate_capabilities(spec)
        template=default_template(spec);compiled=compile_template(template);files=render_files(spec,template)
        artifacts=tuple(GeneratedArtifact(p,bytes_sha256(b),self._kind(p),True) for p,b in files.items())
        manifest=ScaffoldManifest(stable_id('scaffold',{'spec':spec.spec_hash,'files':[(a.path,a.content_hash) for a in artifacts]}),'1.0.0',spec.context_id,spec.spec_hash,self.VERSION,artifacts,compiled.compiled_hash,core_snapshot.snapshot_hash)
        return manifest,files,compiled
    def materialize(self,spec:ContextSpecification,core_snapshot:CoreSnapshot,destination:Path)->ScaffoldManifest:
        manifest,files,_=self.build(spec,core_snapshot)
        for rel,data in files.items():
            target=destination/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        return manifest
    @staticmethod
    def _kind(path:str)->str:
        if '/schemas/' in path:return 'schema'
        if '/fixtures/' in path:return 'fixture'
        if '/tests/' in path:return 'test'
        if path.endswith('.md'):return 'documentation'
        return 'contract'
