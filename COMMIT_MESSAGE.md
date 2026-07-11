fix(alpha-lab): recover SF06 compatibility and unify CI preflight

Replace the remaining Phase 06 LongToString calls with the repository-approved IntegerToString serialization pattern, scope the Phase 06 no-authority test to Phase 06-owned modules, and make GitHub Actions and local pre-push verification use the same transparent engineering-policy runner with a readable failure summary.
