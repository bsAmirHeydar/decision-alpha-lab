---
title: "LCM-02 Ownership Boundary"
status: reference-restricted
---
# Ownership Boundary

Each artifact is bound to semantic-owner, code-owner and documentation-owner roles. Security-sensitive artifacts are additionally bound to `SECURITY_REVIEWER`. These are role bindings only. With no approved human assignees in the source evidence, ownership remains `ROLE_BOUND_HUMAN_ASSIGNEE_PENDING`.

Commit authorship, directory names and generated metadata are not accepted as ownership evidence. Missing human approval blocks move, delete, semantic refactor, merge, cutover and runtime authority.
