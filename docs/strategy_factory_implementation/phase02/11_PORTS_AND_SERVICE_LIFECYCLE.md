# Ports and Service Lifecycle

## Ports Introduced

- Clock
- Market data
- Symbol specification
- Anatomy provider
- Feature provider
- Result sink
- Execution boundary

Every service follows:

```text
Initialize
→ Start
→ Health
→ Stop
→ Shutdown
```

The runtime binds interfaces directly. A registry exists for startup sequencing, duplicate detection, health inspection and reverse-order shutdown. It is not a global service locator for arbitrary runtime calls.
