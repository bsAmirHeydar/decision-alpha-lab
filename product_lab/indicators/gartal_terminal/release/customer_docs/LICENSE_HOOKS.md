# License Hooks — Stage 10

Stage 10 includes a lightweight license gate, not the final cryptographic licensing system.

## Current states

| Mode | Meaning |
|---|---|
| `0 OFF` | No license check. Useful for internal development. |
| `1 OPTIONAL` | Missing key is accepted as demo/audit build. |
| `2 REQUIRED` | Missing or short key blocks initialization. |

## Current validation

The current validator only checks that a required key exists and is at least 8 characters long. This is intentional: it creates the integration point without pretending to provide real anti-piracy security.

## Final licensing stage

A production license system should add:

- machine fingerprint
- account/broker binding where legally acceptable
- expiry date
- offline signed license file
- revocation list strategy
- customer name audit
- product/version entitlement
- graceful renewal messaging
