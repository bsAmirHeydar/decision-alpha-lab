# Confirmed-use admission

A source result is eligible only when it is final, confirmed, immutable, identity-complete, side-valid, role-valid, and price-valid. Nonconfirmed P06 results do not activate references.

Admission order:

1. mark result ID processed;
2. validate immutable confirmation;
3. resolve reference ID;
4. inspect terminal retirement state;
5. inspect protected-role continuity;
6. inspect exact-opportunity duplicate key;
7. accept or reject;
8. persist use evidence;
9. update lifecycle counters and events.
