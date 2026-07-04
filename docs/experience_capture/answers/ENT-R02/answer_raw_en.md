# ENT-R02 — Raw Answer

## Topic

Limit entry, stop behind node, trainable stop buffer, spread adjustment, and max-lot splitting.

## Original Experience, translated to English

The stop location is obvious: behind the node.

However, in some cases giving it a few points of room makes it better. This should be trained and tested.

Entry is limit.

For a buy limit, the entry should come higher by the amount of spread.

For a sell limit, both stop loss and take profit should come higher by the amount of spread.

Naturally, if max lot is reached, split it into several trades.

Some things are already clear.
