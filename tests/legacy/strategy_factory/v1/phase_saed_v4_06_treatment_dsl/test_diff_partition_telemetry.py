from .helpers import build
from saed_v4_treatment_dsl.catalog import institutional_registry
from saed_v4_treatment_dsl.diff import semantic_diff
from saed_v4_treatment_dsl.partition import deterministic_partition
from saed_v4_treatment_dsl.telemetry import build_telemetry
def test_identical_diff():assert semantic_diff(build(),build()).classification.value=='identical'
def test_partition_is_total_and_stable():
 p=build();a=deterministic_partition(p,8);b=deterministic_partition(p,8);assert a==b;assert len(a.assignments)==len(p.programs);assert all(0<=x[1]<8 for x in a.assignments)
def test_telemetry_counts():
 t=build_telemetry(build(),institutional_registry());assert t.program_count==3;assert t.bound_descriptor_count==1;assert t.skip_present and t.abstain_present;assert t.authority_violation_count==0
