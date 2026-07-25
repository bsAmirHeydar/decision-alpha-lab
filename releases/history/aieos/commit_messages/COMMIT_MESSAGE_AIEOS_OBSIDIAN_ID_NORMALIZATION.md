fix(obsidian): normalize AI engineering OS note identities

- add deterministic IDs only to normative notes missing an ID
- preserve existing frontmatter, note bodies, paths, and wikilinks
- add transactional migration, rollback evidence, and idempotency tests
- restore full engineering-policy compliance without changing RTHP or engine code
