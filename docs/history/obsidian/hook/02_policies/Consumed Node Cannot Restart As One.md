# Consumed Node Cannot Restart As One

A node that has already participated in an accepted Hook sequence cannot become node 1 of a later overlapping Hook sequence.

This is a seed restriction, not a full exclusion rule. The same node may still become node 2, 3, or 4 later if the strict forward scan naturally includes it.
