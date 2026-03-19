from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import os
import time
import socket

app = FastAPI(title="k8s-health-service", version="0.1.0")
START_TIME = time.time()
HOSTNAME = socket.gethostname()


class HealthResponse(BaseModel):
    status: str
    uptime_seconds: float
    hostname: str
    checks: Dict[str, Any]


def get_basic_checks() -> Dict[str, Any]:
    return {
        "process": "ok",
        "memory_pressure": "unknown",
        "cpu_pressure": "unknown",
        "dependency_checks": {
            "database": os.getenv("DATABASE_HEALTH", "not_configured"),
            "cache": os.getenv("CACHE_HEALTH", "not_configured"),
        },
    }


@app.get("/")
def root():
    return {
        "service": "k8s-health-service",
        "version": "0.1.0",
        "endpoints": ["/healthz", "/readyz", "/metrics-summary", "/resilience"],
    }


@app.get("/healthz", response_model=HealthResponse)
def healthz():
    return HealthResponse(
        status="ok",
        uptime_seconds=round(time.time() - START_TIME, 2),
        hostname=HOSTNAME,
        checks=get_basic_checks(),
    )


@app.get("/readyz")
def readyz():
    db = os.getenv("DATABASE_HEALTH", "ok")
    cache = os.getenv("CACHE_HEALTH", "ok")
    ready = db == "ok" and cache == "ok"
    return {
        "status": "ready" if ready else "not_ready",
        "dependencies": {
            "database": db,
            "cache": cache,
        },
    }


@app.get("/metrics-summary")
def metrics_summary():
    return {
        "status": "ok",
        "signals": {
            "uptime_seconds": round(time.time() - START_TIME, 2),
            "hostname": HOSTNAME,
            "recommended_to_add": [
                "Prometheus node/container metrics",
                "request latency histogram",
                "error rate",
                "restart count",
                "CPU throttling",
                "OOM kills",
                "disk pressure",
            ],
        },
        "possible_bottlenecks": [
            "CPU saturation",
            "memory pressure",
            "database connection pool exhaustion",
            "I/O wait",
            "network latency",
        ],
    }


@app.get("/resilience")
def resilience():
    return {
        "recommendations": [
            "Use liveness and readiness probes",
            "Run at least 2 replicas",
            "Set CPU/memory requests and limits",
            "Configure PodDisruptionBudget",
            "Use rolling updates with maxUnavailable=0 for critical services",
            "Add HorizontalPodAutoscaler",
            "Send logs/metrics to centralized monitoring",
        ]
    }
