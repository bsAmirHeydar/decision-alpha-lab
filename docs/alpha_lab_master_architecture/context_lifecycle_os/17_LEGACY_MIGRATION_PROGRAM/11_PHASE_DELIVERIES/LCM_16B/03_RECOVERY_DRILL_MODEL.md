# Recovery drill model

The drill has four distinct dimensions. First, the current migration control plane is frozen by repository-relative path, size and SHA-256. Second, a deterministic subset is removed only inside an external temporary workspace and restored byte-for-byte. Third, the complete LCM-16A audit package is rehydrated from its output manifest after simulated artifact loss. Fourth, the closure policy is replayed once with UNKNOWN evidence and once with a synthetic all-PASS evidence set.

Remote Git credentials, network fetch/push, terminal installation and full machine disaster recovery remain external operational evidence. A local copy drill cannot be mislabeled as remote disaster recovery.
