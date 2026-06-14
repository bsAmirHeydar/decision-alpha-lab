# Quant Lab Web Terminal

## Purpose

The web app is the visual research terminal for Decision Alpha Lab.
It provides a professional replay environment where candles, structural nodes, metric events, hypotheses, experiments, validations, and execution evidence can be inspected together.

---

## Current Implementation

The first implemented screen is the **M0001 Visual Replay Terminal**.

It includes:

```text
Top lab header and run controls
Left research lineage tree
Center candlestick replay chart
Right object inspector and layer controls
Bottom dynamic data tables
```

The frontend does not calculate research truth. It renders the `ReplayPayload` returned by the API.

---

## Stack

```text
React
TypeScript
Vite
TanStack Query
TradingView Lightweight Charts
Lucide icons
```

---

## Run

Start the API first from the repository root:

```powershell
py -m uvicorn apps.api.main:app --reload --host 127.0.0.1 --port 8000
```

Then start the web terminal:

```powershell
cd apps/web
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

The Vite dev server proxies `/api/*` requests to `http://127.0.0.1:8000`.

---

## Build Check

```powershell
cd apps/web
npm run build
```

---

## Frontend Rule

The frontend displays research truth.
It does not create research truth.

No React component may independently calculate:

```text
structural nodes
event validity
RTV values
validation status
signal approval
```

All of those must come from the API.
