# Treatment Selection and Action Masks

Treatment selection chooses among entry, stop, target, trailing, management, and capital combinations compiled by UCE-I04. The learner does not create a new treatment. It can select only an exact-version treatment key present in both the frozen treatment registry and the opportunity-specific action mask.

The mask is known-time evidence. It blocks economically invalid, broker-incompatible, structurally impossible, unavailable, unsupported, or operator-prohibited actions. The mask identity is part of every prediction identity.

The default decision sequence is: validate mask lineage, remove blocked actions, apply support audit, predict utility and uncertainty for remaining actions, apply conservative penalty, compare to baseline/manual action, then choose action, baseline, or abstain. A model score cannot override an incompatible stop distance, unsupported volume, stale quote, or missing economic scenario.
