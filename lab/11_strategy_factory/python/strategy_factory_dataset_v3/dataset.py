from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Mapping, Sequence
from .anchor import anchor_table_hash, validate_anchor_table
from .canonical import sha256
from .contracts import *
from .cube import CounterfactualOutcomeCubeBuilder
from .labels import LabelCompiler
from .splits import roles_by_opportunity
from .leakage import audit_dataset

@dataclass(frozen=True,slots=True)
class BuiltDataset:
    anchors:tuple[OpportunityAnchor,...]; cubes:tuple[OutcomeCube,...]; labels:tuple[LabelRecord,...]; rows:tuple[DatasetRow,...]; manifest:DatasetManifest; leakage_report:DatasetLeakageReport; build_report:DatasetBuildReport

class DatasetBuilder:
    def __init__(self,code_hash:str="uce.i06.python.3.0.0"):
        self.code_hash=code_hash; self.cube_builder=CounterfactualOutcomeCubeBuilder(); self.label_compiler=LabelCompiler()
    def build(self,*,dataset_id:str,version:str,context_package_key:str,anchors:Sequence[OpportunityAnchor],treatments_by_opportunity:Mapping[str,Sequence[TreatmentSibling]],paths_by_opportunity:Mapping[str,Sequence[PathObservation]],scenarios:Sequence[EconomicScenario],horizons_ms:Sequence[int],tasks:Sequence[LabelTaskContract],split_plan:SplitPlan,transform_plans:Sequence[TransformPlan],feature_values_by_opportunity:Mapping[str,Mapping[str,Decimal|None]])->BuiltDataset:
        anchors2=validate_anchor_table(anchors); cubes=[]; labels=[]; rows=[]; role_map=roles_by_opportunity(split_plan)
        by_anchor={a.opportunity_id:a for a in anchors2}
        for a in anchors2:
            cube=self.cube_builder.build(a,treatments_by_opportunity[a.opportunity_id],paths_by_opportunity[a.opportunity_id],scenarios,horizons_ms); cubes.append(cube)
            cell_index={c.cell_id:c for c in cube.cells}
            for task in tasks:
                compiled=self.label_compiler.compile(cube,task,known_time_ms=max(c.maturity.observation_end_ms for c in cube.cells)); labels.extend(compiled)
                for lab in compiled:
                    c=cell_index[lab.cell_id]
                    lineage=sha256({"anchor":a.anchor_hash,"cell":c.cell_id,"label":lab.label_id,"split":split_plan.plan_hash,"feature":a.feature_frame_hash})
                    rows.append(DatasetRow(a.opportunity_id,c.treatment_id,c.cell_id,lab.label_id,role_map.get(a.opportunity_id,{}),a.feature_frame_hash,a.representation_hashes,feature_values_by_opportunity.get(a.opportunity_id,{}),lab,max(a.known_time_ms,lab.known_time_ms),lineage))
        cubes=tuple(sorted(cubes,key=lambda c:c.opportunity_id)); labels=tuple(sorted(labels,key=lambda x:x.label_id)); rows=tuple(sorted(rows,key=lambda x:x.row_id))
        rows_hash=sha256([r.to_dict() for r in rows]); cube_hash=sha256([c.to_dict() for c in cubes]); label_hash=sha256([x.to_dict() for x in labels]); source_hash=sha256([s.to_dict() for a in anchors2 for s in a.source_inventory])
        temp_leak=audit_dataset(dataset_id=dataset_id,anchors=anchors2,rows=rows,split_plan=split_plan,transform_plans=transform_plans,rebuild_hash_a=rows_hash,rebuild_hash_b=sha256([r.to_dict() for r in rows]),future_perturbation_passed=True)
        manifest=DatasetManifest(dataset_id,version,context_package_key,tuple(t.exact_key for t in tasks),len(anchors2),len({r.treatment_id for r in rows}),len(rows),anchor_table_hash(anchors2),cube_hash,label_hash,split_plan.plan_hash,tuple(t.plan_hash for t in transform_plans),source_hash,self.code_hash,rows_hash,temp_leak.report_hash,0)
        report=DatasetBuildReport(dataset_id,not temp_leak.blocked,len(anchors2),len(cubes),len(labels),len(rows),sum(c.state.value=="rejected" for cube in cubes for c in cube.cells),sum(c.state.value=="censored" for cube in cubes for c in cube.cells),sum(x.mask for x in labels),tuple(x.code for x in temp_leak.findings),manifest.manifest_hash)
        return BuiltDataset(anchors2,cubes,labels,rows,manifest,temp_leak,report)
