# Engineering Policy GitHub Actions cache fix

Removes the unnecessary pip cache from `actions/setup-python@v5` so a successful repository preflight is not converted into a failed job during post-job cleanup.
