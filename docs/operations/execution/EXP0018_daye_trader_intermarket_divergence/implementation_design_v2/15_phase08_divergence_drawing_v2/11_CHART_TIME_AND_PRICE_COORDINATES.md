# Chart Time and Price Coordinates

Upstream identities use UTC. MT5 chart objects require broker-time coordinates. P08 resolves the broker offset through the P01 time adapter and converts both anchors before object creation.

Both prices come from the Hunter symbol. Cross-symbol price scales are never mixed. A geometry is invalid when times are nonchronological, prices are nonpositive, or the source extreme is absent.
