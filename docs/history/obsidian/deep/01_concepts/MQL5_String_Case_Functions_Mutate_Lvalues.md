---
type: concept
project: EXP0017
phase: 10
---

# MQL5 String Case Functions Mutate Lvalues

In MQL5, `StringToLower()` and `StringToUpper()` mutate a string passed by reference and return a boolean success flag.

Correct:

```mql5
string x = source;
StringToUpper(x);
```

Incorrect:

```mql5
string x = StringToUpper(source);
```

A temporary expression such as `CGM_Clean(source)` cannot be passed where a writable `string&` is required.
