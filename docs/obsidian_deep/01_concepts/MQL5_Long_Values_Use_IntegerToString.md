# MQL5 Long Values Use IntegerToString

In the EXP0017 MQL5 bridge contracts, integer serialization should use `IntegerToString`, including values stored as `long` such as file byte size.

`LongToString` is not portable to the target MetaEditor compiler and causes parser cascades when used inside a long string-concatenation expression.

## Rule

```mql5
string serialized = IntegerToString(long_value);
```

This is a serialization concern only and does not change the underlying numeric type.
