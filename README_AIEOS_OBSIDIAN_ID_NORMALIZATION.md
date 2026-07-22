# AI Algorithm Engineering OS — Obsidian Identity Normalization

This patch adds a transactional migration tool and a canonical, versioned note-identity map for `docs/ai_algorithm_engineering_os`.

## Safety properties

- Existing note IDs are preserved only when they match the canonical map.
- Missing IDs are inserted as the first frontmatter key.
- Frontmatter keys, note bodies, paths, filenames, and wikilinks are otherwise byte-preserved.
- The canonical map covers the exact 246 normative notes in the 253-note vault; exempt README/operational files remain untouched.
- Unknown paths, missing canonical paths, malformed frontmatter, duplicate IDs, ID mismatches, or map-digest drift fail closed before any write.
- Apply mode requires an external backup ZIP.
- Writes are atomic and automatically rolled back if any file write fails.
- A second planning pass must produce zero changes.
- The complete engineering policy must pass after migration.

The production migration uses the verified canonical map rather than inferring identities from the current working tree. This preserves both historical `AIEOS-*` and later `AIEOS2-*` identity namespaces exactly.
