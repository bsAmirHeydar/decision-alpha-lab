from .verify import verify_package
from .schema_validation import validate as validate_schemas
from .static_validation import validate as validate_static
from .delivery_validation import validate as validate_delivery

def run(repo_root, framework_root):
    checks = {
        "package": verify_package(framework_root),
        "schemas": validate_schemas(repo_root),
        "static": validate_static(repo_root),
        "delivery": validate_delivery(repo_root),
    }
    return {"passed": all(x.get("passed") for x in checks.values()), "checks": checks}
