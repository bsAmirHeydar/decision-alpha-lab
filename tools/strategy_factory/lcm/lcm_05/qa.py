from .verify import verify_package
from .schema_validation import validate as schemas
from .static_validation import validate as static
def run(repo_root,topology_root):
    checks={'package':verify_package(topology_root),'schemas':schemas(repo_root),'static':static(repo_root)};return {'passed':all(x.get('passed') for x in checks.values()),'checks':checks}
