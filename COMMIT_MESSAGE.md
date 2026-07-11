fix(ci): remove invalid pip cache from engineering policy workflow

Remove setup-python pip caching from the Engineering Policy job because the workflow installs no dependencies and therefore creates no pip cache path. Preserve the exact repository preflight command while preventing setup-python post-job cache-save failures.
