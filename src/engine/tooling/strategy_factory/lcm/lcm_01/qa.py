from __future__ import annotations
import compileall, json, tempfile, shutil
from pathlib import Path
from .delivery_validation import validate_delivery
from .service import RunConfig, run_survey
from .static_validation import validate_registries
from .verify import verify_survey_package

def run_qa(repo_root: Path, survey_root: Path) -> dict:
    compile_ok=compileall.compile_dir(str(repo_root/'src/engine/tooling/strategy_factory/lcm/lcm_01'),quiet=1,force=True)
    static=validate_registries(repo_root); delivery=validate_delivery(repo_root); package=verify_survey_package(survey_root)
    # Determinism is checked by running into a fresh temporary destination and comparing the summary digest.
    tmp=Path(tempfile.mkdtemp(prefix='lcm01-repeat-'))
    try:
        repeat=tmp/'survey'; run_survey(RunConfig(repo_root=repo_root,destination=repeat))
        a=json.loads((survey_root/'reports/survey_summary.json').read_text(encoding='utf-8'))
        b=json.loads((repeat/'reports/survey_summary.json').read_text(encoding='utf-8'))
        deterministic=a['summary_digest']==b['summary_digest'] and a['survey_id']==b['survey_id']
    finally: shutil.rmtree(tmp,ignore_errors=True)
    return {'passed':bool(compile_ok and static['passed'] and delivery['passed'] and deterministic),'compileall_passed':compile_ok,'static_validation':static,'delivery_validation':delivery,'survey_package':package,'repeat_run_deterministic':deterministic}
