# Time Coordinate Conversion

P03 windows are identified in UTC and New York time. MT5 chart objects require broker chart time. P09 converts start and end UTC through the P01 broker-offset adapter.

Manual fixed broker offset remains replay-canonical. Current-live auto offset is explicitly not assumed to reconstruct historical broker DST behavior.
