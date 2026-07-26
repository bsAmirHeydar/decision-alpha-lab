# GitHub Actions pip-cache post-job fix

## Incident

The Engineering Policy preflight completed successfully, but the job was marked failed during the post-job cleanup of `actions/setup-python@v5`.

The workflow enabled `cache: pip` while the job did not install any Python dependencies. As a result, no pip cache directory was created, and the setup-python post action failed while attempting to save a non-existent cache path.

## Correction

The Engineering Policy workflow no longer enables pip caching. The job only provisions Python 3.11 and executes the repository preflight.

This is the correct configuration because the workflow runs repository-owned scripts that use the standard library and does not run `pip install`.

## Scope

This change does not alter:

- repository policy checks;
- Obsidian validation;
- MQL5 compatibility validation;
- repository layout validation;
- any MQL5 or Python runtime code.

It only removes an unnecessary CI cache feature that caused the post-job failure.
