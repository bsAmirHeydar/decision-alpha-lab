# Symbol-Local Price Scale

SPX and NDX ranges are never merged. The SPX box uses SPX session High/Low and is drawn only on SPX broker-symbol charts. NDX follows the same rule. Cross-symbol comparison is unnecessary and prohibited at the renderer boundary.

A valid paired P03 period can therefore produce two independent boxes with identical time boundaries but different price coordinates.
