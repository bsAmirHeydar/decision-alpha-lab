from src.engine.tooling.strategy_factory.acl_os.acl_15.schema_validation import validate_schema_file
def test_all_schemas(root):
 for p in (root/'registry/history/acl/acl_15/schemas/v1').glob('*.json'): assert validate_schema_file(p)==[]
