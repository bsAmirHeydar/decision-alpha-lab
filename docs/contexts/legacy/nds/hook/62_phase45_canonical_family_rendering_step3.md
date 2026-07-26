# 62 — Phase 45: Canonical Family Rendering Step 3

## 1. Purpose

Phase 45 implements the visual vocabulary for the canonical valid Hook doctrine.

The system already has three separable layers:

```text
Hook sequence construction
→ Hook validity determination
→ Canonical visible-set filtering
```

This phase adds the next layer:

```text
Canonical visible set
→ Family rendering and family labels
```

The purpose is to make valid Hooks readable without altering how they are counted or validated.

## 2. Family classes

Production-visible Hooks belong to the following display classes.

### 2.1 F3H — Hook After Opposing F3

A Hook receives the `F3H` display class when it is selected by the canonical Hook-after-opposing-F3 rule.

Meaning:

```text
An opposing F3 has produced a terminal context, and the Hook forms from that terminal side.
```

Label prefix:

```text
F3H
```

### 2.2 HH — Hook After Hook

A Hook receives the `HH` display class when it is Hook-2 in a same-genus Hook-after-Hook chain.

Meaning:

```text
Hook-1 closed its cycle/sequence.
Hook-2 starts from Hook-1 structural terminal node.
Hook-2 is the valid Hook.
```

Label prefix:

```text
HH
```

### 2.3 PARENT — Parent Companion Hook

A Hook receives the `PARENT` display class only when it is Hook-1 required to read a valid Hook-after-Hook pair.

Meaning:

```text
The parent Hook is visible because the child Hook depends on it.
It is not promoted into an independently valid Hook.
```

Label prefix:

```text
PARENT
```

### 2.4 F3H+HH — Dual-family Hook

A Hook can theoretically qualify by both valid families.

Meaning:

```text
The same Hook is both a post-F3 Hook and a Hook-after-Hook child.
```

Label prefix:

```text
F3H+HH
```

## 3. Color doctrine

The renderer applies family-level colors in valid-only mode.

| Class | Meaning | Visual role |
|---|---|---|
| `F3H` | post-F3 valid Hook | distinct post-F3 color |
| `HH` | Hook-after-Hook valid child | distinct chain color |
| `F3H+HH` | dual-family valid Hook | priority/highlight color |
| `PARENT` | visible companion only | neutral companion color |

The exact color constants are implementation details. The doctrine is that the family must be visually separable.

## 4. Label doctrine

If valid-only mode is active, sequence labels must carry the family tag:

```text
F3H H123B1:1
HH H130B1:2
PARENT H129B1:1
```

The tag appears before the existing Hook/branch/node label.

## 5. What this phase does not change

This phase does not change:

- Hook sequence construction
- origin selection
- terminal selection
- F3 matching
- Hook-after-Hook matching
- lifecycle invalidation
- Zone creation
- execution
- risk
- broker behavior

## 6. Implementation contract

The renderer must answer three questions for every selected sequence:

```text
1. Is this sequence itself valid by F3H?
2. Is this sequence itself valid by HH?
3. Is this sequence visible only because it is the parent companion of HH?
```

Then it must derive:

```text
family_tag
family_color
```

The arc, node markers, labels, and sequence lines must use the same family rendering decision.

## 7. Debug expectations

In valid-only mode:

- no unqualified Hook labels should appear
- no unqualified Hook arcs should appear
- parent companion labels must say `PARENT`
- Hook-after-Hook child labels must say `HH`
- post-F3 Hook labels must say `F3H`
- dual-family Hook labels may say `F3H+HH`

