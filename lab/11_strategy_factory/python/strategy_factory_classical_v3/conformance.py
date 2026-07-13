from strategy_factory_trainers_v3.golden import build_case
from strategy_factory_trainers_v3.enums import TaskKind
from strategy_factory_trainers_v3.canonical import canonical_sha256
from .catalog import CATALOG
from .dependency import DependencyProbe
from .registry import ClassicalAlgorithmRegistry
from .benchmark import BenchmarkRunner,ClassicalGateEvaluator
from .contracts import BenchmarkCase,DependencyRequirement
from .enums import *
def run_conformance():
 probe=DependencyProbe();snap=ClassicalAlgorithmRegistry(probe).freeze().snapshot();s,rows,p=build_case(TaskKind.BINARY_CLASSIFICATION);case=BenchmarkCase('golden_binary','synthetic_reference',s.dataset_id,s.dataset_manifest_hash,p.task.key,'',p.trainer.config_hash,p.trainer.seed,AlgorithmFamily.BASELINE);report=BenchmarkRunner(probe).report('uce_i08_conformance',((case,p,s,rows),),('prevalence','manual_threshold','logistic_regression','decision_tree_classifier'));gate=ClassicalGateEvaluator.evaluate('synthetic_reference',report);missing=DependencyProbe(disabled=('definitely_missing_module',)).probe_one(DependencyRequirement('definitely_missing_module','definitely-missing','>=1',DependencyMode.OPTIONAL));out={'release':'UCE-I08','catalog_count':len(CATALOG),'available_count':sum(1 for x in snap.availability if x.available),'families':sorted({x.family.value for x in CATALOG}),'benchmark_observation_count':len(report.observations),'benchmark_ready':report.classical_comparison_ready,'gate_state':gate.state.value,'optional_missing_clean':missing.state is AvailabilityState.DISABLED,'all_probability_disclosed':report.all_probability_disclosed,'deterministic':all(x.deterministic_rerun for x in report.observations if x.status is BenchmarkStatus.SUCCEEDED),'failed_algorithms':[x.algorithm_key for x in report.observations if x.status is BenchmarkStatus.FAILED]};out['evidence_hash']=canonical_sha256(out);out['passed']=out['catalog_count']>=35 and out['benchmark_ready'] and out['gate_state']=='pass' and out['optional_missing_clean'] and out['all_probability_disclosed'] and not out['failed_algorithms'];return out
