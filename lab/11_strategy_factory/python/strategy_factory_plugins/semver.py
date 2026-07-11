import re
_PATTERN=re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
def validate_semver(value:str)->str:
    if not _PATTERN.fullmatch(value): raise ValueError(f"invalid semantic version: {value!r}")
    return value
