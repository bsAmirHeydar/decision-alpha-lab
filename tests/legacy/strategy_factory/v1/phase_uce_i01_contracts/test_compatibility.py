from strategy_factory_contracts_v3.capability import CapabilityDescriptor,ResourceBudget
from strategy_factory_contracts_v3.compatibility import CompatibilityEngine,CompatibilityRequest
from strategy_factory_contracts_v3.enums import CompatibilityStatus,MigrationMode,RepresentationKind,RuntimeMode,SupportLevel,TaskType
from strategy_factory_contracts_v3.migration import MigrationEdge,MigrationRegistry
from strategy_factory_contracts_v3.schema import SchemaDescriptor,SchemaId,SchemaRegistry,SemanticVersion

def setup_engine():
    old=SchemaDescriptor(SchemaId("alpha_lab.ucee","features",SemanticVersion(3,0,0)),"owner",("x",))
    new=SchemaDescriptor(SchemaId("alpha_lab.ucee","features",SemanticVersion(3,1,0)),"owner",("x","y"))
    out=SchemaDescriptor(SchemaId("alpha_lab.ucee","prediction",SemanticVersion(3,0,0)),"owner",("score",))
    schemas=SchemaRegistry((old,new,out))
    edge=MigrationEdge("features_300_to_310",old.schema_id,new.schema_id,old.semantic_hash,new.semantic_hash,MigrationMode.LOSSLESS,lambda row:{**row,"y":0})
    migrations=MigrationRegistry(schemas,(edge,))
    cap=CapabilityDescriptor("trainer.logistic","1.0.0",SupportLevel.RESEARCH,("hook",),(RepresentationKind.TABULAR,),(TaskType.BINARY_CLASSIFICATION,),("entry_matrix",),(RuntimeMode.RESEARCH,), ("onnx",),(new.schema_id.exact_key,),(out.schema_id.exact_key,),True,True,False,True,ResourceBudget(128,1,100000,1024,5000))
    return CompatibilityEngine(schemas,migrations),cap,old,new,out

def request(old,out,**changes):
    values=dict(consumer_component_id="trainer.logistic",context_kind="hook",representation_kind=RepresentationKind.TABULAR,task_type=TaskType.BINARY_CLASSIFICATION,treatment_family="entry_matrix",runtime_mode=RuntimeMode.RESEARCH,export_target="onnx",input_schema=old.schema_id,required_output_schema=out.schema_id,feature_count=64,latency_budget_us=1000,minimum_support_level=SupportLevel.RESEARCH)
    values.update(changes);return CompatibilityRequest(**values)

def test_compatible_after_explicit_migration():
    engine,cap,old,_,out=setup_engine();decision=engine.evaluate(cap,request(old,out))
    assert decision.status==CompatibilityStatus.COMPATIBLE_AFTER_MIGRATION
    assert decision.migration_path==("features_300_to_310",)

def test_budget_and_runtime_fail_closed_with_reasons():
    engine,cap,old,_,out=setup_engine();decision=engine.evaluate(cap,request(old,out,feature_count=1000,runtime_mode=RuntimeMode.LIVE))
    assert decision.status==CompatibilityStatus.INCOMPATIBLE
    assert "feature_budget_exceeded" in decision.reason_codes
    assert "runtime_mode_unsupported" in decision.reason_codes

def test_support_level_is_non_compensatory():
    engine,cap,old,_,out=setup_engine()
    decision=engine.evaluate(cap,request(old,out,minimum_support_level=SupportLevel.PRODUCTION))
    assert decision.status==CompatibilityStatus.INCOMPATIBLE
    assert "support_level_insufficient" in decision.reason_codes
