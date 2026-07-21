# EXP0013 Astro Raw Axes Oscillator

This guide adds a compact, separate-window oscillator view for the **Level 1 raw astro axes**.
It is designed to reduce chart clutter while making the candle-by-candle sky-state easier to read.

---

## File

```text
mql5/Indicators/Research/EXP0013_AstroRawAxesOscillator.mq5
```

---

## Goal

Instead of reading the full text panel every time, this indicator plots the raw astro axes on a **0..100 oscillator scale**:

- Flow
- Impulse
- Friction
- Pressure
- Transition
- MoonTempo
- SaturnDrag

The default compact layout keeps only the four most important axes visible:

- Flow
- Impulse
- Friction
- Pressure

The other three are available through inputs and are hidden by default to keep the subwindow clean.

---

## Time contract

Use the same CSV time contract already established for EXP0013:

- the CSV already contains `broker_time`
- chart candle open time is matched directly against `broker_time`
- there must be **no second GMT shift** inside the oscillator logic

If the CSV was built with broker GMT+3 already baked into `broker_time`, then the current runtime convention is:

```text
InpBrokerGmtOffsetHours = 0
```

That input is only passed through to the store loader for consistency. The lookup itself is broker-time aligned.

---

## Default reading model

### 1) Breakout / impulse reading

A cleaner impulse-style move usually looks like this:

```text
Impulse high
Friction low
Pressure low to mid
Transition low
```

Interpretation:

- the environment has movement force
- drag is low
- hard-pressure noise is controlled
- regime is not in a transition state

### 2) Smooth continuation reading

A smoother continuation usually looks like this:

```text
Flow high
Friction low
Pressure low
Transition low
```

Interpretation:

- geometry is softer
- continuation is less interrupted
- lower chance of deep adverse pullback

### 3) Dirty / noisy movement risk

A dirtier path usually looks like this:

```text
Friction high
Pressure high
Transition high
```

Interpretation:

- more drag
- more hard-pressure noise
- higher regime-change risk
- higher chance of chop, pullback, or fake move

---

## Quick reading cheat sheet

```text
Impulse rising   = movement force increasing
Flow rising      = smoother geometry increasing
Friction rising  = drag / dirty path risk increasing
Pressure rising  = hard-pressure / volatility tension increasing
Transition rising= regime-change risk increasing
MoonTempo rising = short-term speed increasing
SaturnDrag rising= structural resistance / delay increasing
```

---

## Suggested compact setup

For the cleanest first read:

```text
InpShowFlow       = true
InpShowImpulse    = true
InpShowFriction   = true
InpShowPressure   = true
InpShowTransition = false
InpShowMoonTempo  = false
InpShowSaturnDrag = false
```

This gives a compact four-line oscillator.

If later you need more nuance, enable:

```text
InpShowTransition = true
InpShowMoonTempo  = true
InpShowSaturnDrag = true
```

---

## Compile and attach

Compile:

```text
mql5/Indicators/Research/EXP0013_AstroRawAxesOscillator.mq5
```

Then attach it to a chart or use it in Visual Tester.

Recommended input values:

```text
InpAstroCsvFile         = astro_GMT3_M1_2026_to_now_mql.csv
InpBrokerGmtOffsetHours = 0
InpRequireExactBarTime  = true
InpMaxBarsToProcess     = 5000
```

If your CSV is placed in `MQL5\Files\astro\`, you can instead use:

```text
InpAstroCsvFile = astro\astro_GMT3_M1_2026_to_now_mql.csv
```

---

## How to use together with the text panel

Use the oscillator for **fast structural reading**.
Use the existing text-panel expert when you want the detailed diagnostic breakdown.

Practical workflow:

1. Scan the oscillator first.
2. Mark zones where:
   - Impulse is high
   - Friction is low
   - Pressure is low/mid
3. Open the detailed panel only on the interesting bars.
4. Later compare those bars with market path metrics such as:
   - MAE_R
   - pullback_depth_R
   - path_efficiency
   - bars_to_target

---

## Research meaning

This oscillator does **not** predict direction by itself.
It only gives a compact visual representation of the **raw Level 1 astro axes**.

The intended role is:

```text
Market provides direction.
Astro raw axes provide path-quality context.
```

So the correct question is not:

```text
Will this go up or down?
```

The correct question is:

```text
If the market gives a direction here, does the astro state look more like
clean impulse, smooth continuation, or dirty chop risk?
```
