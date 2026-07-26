# Immutability and terminal states

Terminal reference states are immutable. Accepted use records are also immutable. Corrections require a versioned migration or replay rebuild, not in-place mutation.

Forbidden transitions:

- retired reference to surviving;
- accepted use to rejected;
- historical confirmation endpoint rewrite;
- protected role rewrite after activation.
