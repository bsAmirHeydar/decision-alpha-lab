# Control-plane snapshot

The frozen snapshot covers root phase manifests, QA reports, file indexes, hash ledgers, release controls, program governance documents, migration handoffs, output manifests and rollback manifests. Paths are canonical POSIX repository-relative identifiers.

Symlinks, duplicate paths, path traversal and hash drift are rejected. The snapshot is not a full 52-thousand-file repository backup; it is the exact migration governance and recovery control plane.
