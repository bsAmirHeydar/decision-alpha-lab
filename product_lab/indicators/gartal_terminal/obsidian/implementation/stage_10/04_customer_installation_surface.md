# Customer Installation Surface

The customer should never read engineering docs to install the product.

Customer docs live in:

```text
release/customer_docs/
```

## Included docs

- English installation guide
- Persian installation guide
- beta QA checklist
- release manifest template
- license hook explanation

## Customer mental model

The user installs two moving parts:

1. Downloader EA fetches Forex Factory/Fair Economy calendar.
2. Indicator reads local bridge file and renders the terminal.

This is a deliberate workaround because MT5 custom indicators cannot reliably use WebRequest.
