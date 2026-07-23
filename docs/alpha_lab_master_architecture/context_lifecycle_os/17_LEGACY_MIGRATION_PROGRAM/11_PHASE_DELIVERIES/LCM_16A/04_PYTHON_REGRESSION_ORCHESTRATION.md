# Python regression orchestration

A governed suite matrix replaces a single broad `pytest` invocation. Some historical suites require their own working directory or Python package roots; treating collection failure from the wrong working directory as a product failure would be incorrect.

The matrix covers the LCM stable chain, all ACL-OS suites, Strategy Factory core phases, UCEE and SAED high-risk phases, RTHP, Faerie Protocol I15 and NDS Hook 86.4. Git LFS materialization is a named prerequisite for LCM-12A.
