# Multi-Task Shared Representation

Related targets can share context signal: trade probability, net utility, maximum adverse excursion, time to target, stop-first probability, and preferred treatment. UCE-I09 provides a deterministic shared-feature, multiple-head baseline and contracts for later neural shared representations.

Each head has its own task key, loss, weight, prediction lineage, and metric. The aggregate objective is never the only report. Gradient or loss imbalance is monitored so a high-scale regression target cannot dominate a rare-event head.

Missing labels require explicit masks. A row cannot be interpreted as a zero target merely because one head is unavailable. Multi-task output is promoted only when each critical head meets its own non-compensatory gate.
