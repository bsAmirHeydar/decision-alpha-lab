---
title: Install — Alpha Lab Context Lifecycle OS Architecture
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# Install — Alpha Lab Context Lifecycle OS Architecture

Install from the repository root. The patch is additive and repository-relative.

## Preconditions

- Review or clean the working tree.
- Use Python 3.11 or newer.
- Ensure `pytest`, `PyYAML` and `jsonschema` are installed.
- Preserve existing SAED, UCEE and Strategy Factory files.

## Validation

Run `python -m tools.strategy_factory.acl_os.run_acl_os_architecture_qa` and `python -m tools.strategy_factory.acl_os.validate_acl_os_architecture_delivery` before staging.

## Rollback

Before commit, remove only paths in `ACL_OS_ARCHITECTURE_FILE_INDEX.txt`. After commit, use a normal Git revert. The patch does not activate a terminal, route or live account.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
