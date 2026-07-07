# Hook Root Rebuild Patch

Start here after expanding the patch.

This patch rebuilds the Hook Phase 02 sequence-counting layer from the corrected Hook doctrine:

```text
first unused raw same-side node = node 1
scan forward to the end
strict adverse continuation = node 2/3/4/...
participated nodes cannot restart as node 1
participated nodes may still appear as continuation nodes
```

Main documentation:

```text
docs/nds_hook_architecture/47_phase34_seed_owned_hook_sequence_and_validity_filter.md
docs/obsidian_hook/00_mocs/HOOK_ROOT_REBUILD_MOC.md
```
