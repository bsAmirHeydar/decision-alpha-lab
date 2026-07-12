from dataclasses import asdict
import platform,sys
from hashlib import sha256
from .canonical import canonical_sha256,stable_id
from .contracts import *
class ArtifactPackager:
 @staticmethod
 def environment_hash():return canonical_sha256({'python':sys.version.split()[0],'impl':platform.python_implementation(),'platform':platform.platform()})
 @staticmethod
 def package(d,c,t,s,o,b,m,serialized,cal,threshold,metrics,code_hash='unknown',limitations=()):
  transport_hash=sha256(serialized.encode()).hexdigest();calh=cal.state_hash if cal else canonical_sha256({'kind':'none'});th=canonical_sha256(asdict(threshold)) if threshold else canonical_sha256({'threshold':None})
  aid=stable_id('uce_model',{'d':d.descriptor_hash,'c':c.config_hash,'t':t.contract_hash,'data':s.dataset_manifest_hash,'state':m.state_hash,'transport':transport_hash,'cal':calh,'th':th})
  manifest=ModelArtifactManifest(aid,'3.0.0',d.descriptor_hash,c.config_hash,t.contract_hash,s.dataset_manifest_hash,o.protocol_hash,b.budget_hash,s.feature_order,t.output_names,m.state_hash,calh,th,ArtifactPackager.environment_hash(),code_hash,dict(metrics),tuple(limitations),d.export_formats,ArtifactRiskLevel.LOW if d.determinism is DeterminismLevel.BIT_EXACT else ArtifactRiskLevel.MODERATE)
  card=ModelCard(aid,f'{d.family} model',f'{d.key} fitted for {t.key}',(f'Governed research for {t.task_kind.value}',),('Ungoverned live trading','Changed feature order'),f'{s.dataset_id}: {s.row_count} rows',f'{t.primary_metric}: {dict(metrics)}',tuple(limitations),('UCE-I05 side-aware costs inherited through dataset lineage',),'Market representativeness, not human fairness',( 'Exact features','Exact transforms','Promotion approval'),('Schema drift','Economic drift','Serialization failure'),('Regime shift','Tail uncertainty'),canonical_sha256(asdict(manifest)))
  return manifest,card
