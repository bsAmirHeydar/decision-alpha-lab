# MetaTrader Compile Checklist

Use this checklist after applying any MQL5 release.

---

## Before compile

- Close MetaEditor before applying the release.
- Apply ZIP or PATCH, not both.
- Run the release installer if one exists.
- Reopen MetaEditor.

---

## Compile order

Compile shared include changes through the Experts that use them.

Suggested order:

1. M0001 / node and event Experts,
2. M0004 / regime memory Experts,
3. M0005 / directional memory Experts,
4. Debug validators,
5. Execution EAs.

---

## Error handling

If compile fails, capture the full MetaEditor error list. Do not summarize from memory.

A useful error report contains:

- file path,
- line number,
- column number,
- exact error text,
- whether the file is repo-level or terminal include-level.

---

## Frequent failure modes

### Include mismatch

The repo include changed, but MetaEditor is reading an older terminal-level include.

Fix: run the installer or manually copy the include tree.

### Enum mismatch

An enum name was assumed from memory and does not exist in the current project.

Fix: inspect the actual enum definition and patch the exact symbol.

### Function signature mismatch

A collector or report function changed parameters.

Fix: patch both declaration and every call site.

### Debug-only logic not promoted

A validator contains the correct logic, but the main Expert still uses old logic.

Fix: promote the contract into the main Expert and shared include.
