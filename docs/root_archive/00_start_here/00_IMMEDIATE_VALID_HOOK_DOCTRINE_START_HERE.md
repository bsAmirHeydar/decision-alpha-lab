# Immediate Valid Hook Doctrine Patch

Start here after expanding the patch.

This patch tightens valid Hook visibility to the exact doctrine:

1. **Immediate Hook After Opposing F3** — a completed/locked F3 validates only the immediate next Hook on the same structural scale, and only if that Hook is opposite to the F3 direction.
2. **Hook After Hook** — Hook-2 is valid only when its origin node is exactly the terminal/resolve node of Hook-1.

Hook-1 is displayed only as the required companion parent of a valid Hook-after-Hook child.
