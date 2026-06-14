from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.routers.lab import router as lab_router
from apps.api.routers.visualizations import router as visualization_router
from apps.api.routers.data import router as data_router

app = FastAPI(
    title="Decision Alpha Lab API",
    version="0.3.0",
    description="Research registry, document reader, run explorer, and visualization contract API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lab_router)
app.include_router(visualization_router)
app.include_router(data_router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "decision-alpha-lab"}
