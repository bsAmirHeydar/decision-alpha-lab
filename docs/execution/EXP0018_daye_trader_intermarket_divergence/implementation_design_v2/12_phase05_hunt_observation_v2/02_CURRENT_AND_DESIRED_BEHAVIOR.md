---
id: EXP0018-P05-BEHAVIOR
title: "P05 Current and Desired Behavior"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Current and Desired Behavior

Before P05, P04 resolves which current period belongs with which reference period but deliberately does not inspect price extremes. Desired behavior is a pure touch classifier that can be replayed and independently tested.

The patch also fixes the P04 refresh fingerprint to include source availability time. Without that change, an open current period could change high/low while P04 incorrectly considered its source unchanged.
