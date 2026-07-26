# Protected Reference Lifecycle Rules

## Definitions

`reference side` means one side of one previous cycle reference:

```text
group + trading day + reference cycle + HIGH/LOW
```

High and low retire independently. A high-side retirement does not retire the low side of the same cycle.

## Allowed repeated divergence

Repeated divergence is allowed when:

```text
same reference side
same protected symbol
protected symbol has not hunted that side
hunter symbol keeps being the hunter side
```

This preserves the user's rule: if the protected symbol is still protected in a later stage, the same reference can still form divergence again.

## Retirement event

The reference side retires when the protected symbol hunts its own corresponding reference high/low.

For SELL/high side:

```text
protected_symbol.current_high >= protected_symbol.reference_high
```

For BUY/low side:

```text
protected_symbol.current_low <= protected_symbol.reference_low
```

## Role switch suppression

If a prior protected symbol later appears as the hunter while the former hunter appears clean, the reference side is considered compromised and is suppressed. This prevents role-flip reuse after the clean side has effectively been breached.

## Day reset

Lifecycle records reset at the new 18:00 New York trading day by default.
