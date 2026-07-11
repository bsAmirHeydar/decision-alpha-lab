# Performance

The pilot runs on timer, not tick fast path. Complexity is dominated by legacy group/reference scans. Dedup and mapping are bounded. Profiling must track pulse latency by enabled group count, history depth, candidate count, and terminal synchronization state.
