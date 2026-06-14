# Applications

This folder contains user-facing applications that sit on top of the Python research lab.

```text
apps/api   FastAPI bridge from lab outputs to typed UI contracts
apps/web   React visual research terminal
```

The apps must remain separate from the research engine.

```text
lab/ owns research truth
apps/api normalizes research truth
apps/web visualizes research truth
```
