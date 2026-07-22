# Install — RTHP Real Train Activation v1

## Preconditions

- The English canonical RTHP Context package is installed.
- RTHP ACL-03 compilation/onboarding is installed at Context version 1.0.2.
- The RTHP AI-engine input binding is installed.
- Python and project test dependencies are available.
- The Git working tree and staging area are clean.

## Installation

Expand the release ZIP from the repository root, remove the ZIP, verify the patch hash ledger, compile the new package, run the direct activation tests and all existing RTHP/ACL/UCEE regression tests, stage exactly the paths in the release file index, commit, and push.

## Real training

After installation, copy the real configuration template to a run-specific path, provide two local causally ordered tick JSONL artifacts and all required source metadata, validate the configuration, run activation, and verify the immutable run directory.
