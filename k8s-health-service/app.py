from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional
import os
import socket
import time

import httpx
import psutil
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from pydantic import BaseModel

APP_NAME = os.getenv("APP_NAME", "k8s-health-service")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
HOSTNAME = socket.gethostname()
START_TIME = time.time()
READY = False

REQUEST_COUNT = Counter(
    "app_http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "app_http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)
APP_INFO = Gauge("app_info", "Application build info", ["name", "version", "hostname"])
UP = Gauge("app_up", "Application up status")
READY_GAUGE = Gauge("app_ready", "Application readiness status")
DEPENDENCY_STATUS = Gauge("app_dependency_status", "Dependency health status", ["dependency", "type"])
PROCESS_RESIDENT_MEMORY_BYTES = Gauge("app_process_resident_memory_bytes", "Resident memory")
PROCESS_CPU_PERCENT = Gauge("app_process_cpu_percent", "CPU percent for process")


class DependencyResult(BaseModel):
    name: str
    type: str
    target: str
    status: str
    latency_ms: Optional[float] = None
    detail: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    uptime_seconds: float
    hostname: str
    version: str
    checks: Dict[str, Any]


class DependencyChecker:
    def __init__(self) -> None:
        self.timeout = float(os.getenv("CHECK_TIMEOUT_SECONDS", "2.0"))
        self.http_targets = self._parse_targets("HTTP_CHECKS")
        self.tcp_targets = self._parse_targets("TCP_CHECKS")

    @staticmethod
    def _parse_targets(env_name: str) -> List[Dict[str, str]]:
        raw = os.getenv(env_name, "").strip()
        if not raw:
            return []
        items: List[Dict[str, str]] = []
        for chunk in raw.split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            if "=" in chunk:
                name, target = chunk.split("=", 1)
            else:
                name, target = chunk, chunk
            items.append({"name": name.strip(), "target": target.strip()})
        return items

    async def run(self) -> List[DependencyResult]:
        results: List[DependencyResult] = []
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
            for item in self.http_targets:
                start = time.perf_counter()
                try:
                    resp = await client.get(item["target"])
                    latency_ms = round((time.perf_counter() - start) * 1000, 2)
                    status_name = "ok" if resp.status_code < 500 else "fail"
                    results.append(
                        DependencyResult(
                            name=item["name"],
                            type="http",
                            target=item["target"],
                            status=status_name,
                            latency_ms=latency_ms,
                            detail=f"status_code={resp.status_code}",
                        )
                    )
                except Exception as exc:
                    results.append(
                        DependencyResult(
                            name=item["name"],
                            type="http",
                            target=item["target"],
                            status="fail",
                            detail=str(exc),
                        )
                    )
        for item in self.tcp_targets:
            start = time.perf_counter()
            host, port = item["target"].rsplit(":", 1)
            try:
                with socket.create_connection((host, int(port)), timeout=self.timeout):
                    latency_ms = round((time.perf_counter() - start) * 1000, 2)
                    results.append(
                        DependencyResult(
                            name=item["name"],
                            type="tcp",
                            target=item["target"],
                            status="ok",
                            latency_ms=latency_ms,
                        )
                    )
            except Exception as exc:
                results.append(
                    DependencyResult(
                        name=item["name"],
                        type="tcp",
                        target=item["target"],
                        status="fail",
                        detail=str(exc),
                    )
                )
        return results


checker = DependencyChecker()
process = psutil.Process()
process.cpu_percent(interval=None)


@asynccontextmanager
async def lifespan(_: FastAPI):
    global READY
    APP_INFO.labels(name=APP_NAME, version=APP_VERSION, hostname=HOSTNAME).set(1)
    UP.set(1)
    READY = True
    READY_GAUGE.set(1)
    try:
        yield
    finally:
        READY = False
        READY_GAUGE.set(0)
        UP.set(0)


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    path = request.url.path
    method = request.method
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    REQUEST_COUNT.labels(method=method, path=path, status_code=str(response.status_code)).inc()
    REQUEST_LATENCY.labels(method=method, path=path).observe(duration)
    return response


def resource_snapshot() -> Dict[str, Any]:
    memory = process.memory_info().rss
    cpu_percent = process.cpu_percent(interval=None)
    PROCESS_RESIDENT_MEMORY_BYTES.set(memory)
    PROCESS_CPU_PERCENT.set(cpu_percent)
    return {
        "process": "ok",
        "memory": {"resident_bytes": memory},
        "cpu": {"percent": cpu_percent},
    }


async def dependency_snapshot() -> Dict[str, Any]:
    results = await checker.run()
    if not results:
        return {"configured": False, "items": []}
    for item in results:
        DEPENDENCY_STATUS.labels(dependency=item.name, type=item.type).set(1 if item.status == "ok" else 0)
    return {
        "configured": True,
        "items": [item.model_dump() for item in results],
    }


@app.get("/")
async def root():
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "endpoints": ["/healthz", "/readyz", "/metrics", "/metrics-summary", "/resilience"],
    }


@app.get("/healthz", response_model=HealthResponse)
async def healthz():
    checks = {
        "resources": resource_snapshot(),
        "dependencies": await dependency_snapshot(),
    }
    return HealthResponse(
        status="ok",
        uptime_seconds=round(time.time() - START_TIME, 2),
        hostname=HOSTNAME,
        version=APP_VERSION,
        checks=checks,
    )


@app.get("/readyz")
async def readyz():
    dependencies = await checker.run()
    failing = [item.model_dump() for item in dependencies if item.status != "ok"]
    ready = READY and not failing
    READY_GAUGE.set(1 if ready else 0)
    payload = {
        "status": "ready" if ready else "not_ready",
        "hostname": HOSTNAME,
        "dependencies_checked": len(dependencies),
        "failing_dependencies": failing,
    }
    if ready:
        return payload
    return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=payload)


@app.get("/metrics")
async def metrics():
    resource_snapshot()
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/metrics-summary")
async def metrics_summary():
    resources = resource_snapshot()
    dependencies = await dependency_snapshot()
    return {
        "status": "ok",
        "signals": {
            "uptime_seconds": round(time.time() - START_TIME, 2),
            "hostname": HOSTNAME,
            "process_memory_bytes": resources["memory"]["resident_bytes"],
            "process_cpu_percent": resources["cpu"]["percent"],
            "dependency_results": dependencies,
            "recommended_platform_metrics": [
                "container_cpu_usage_seconds_total",
                "container_memory_working_set_bytes",
                "container_cpu_cfs_throttled_seconds_total",
                "kube_pod_container_status_restarts_total",
                "kube_deployment_status_replicas_available",
                "node_load1",
                "node_filesystem_avail_bytes",
            ],
        },
        "possible_bottlenecks": [
            "CPU saturation and throttling",
            "memory pressure and OOM risk",
            "database or cache latency spikes",
            "network latency or packet loss",
            "thread or worker exhaustion",
            "slow downstream dependencies",
        ],
    }


@app.get("/resilience")
async def resilience():
    return {
        "recommendations": [
            "Use readiness, liveness, and startup probes",
            "Run at least 2 replicas across nodes",
            "Set CPU and memory requests/limits from load tests",
            "Enable HPA based on CPU and optionally custom latency metrics",
            "Use a PodDisruptionBudget for voluntary disruptions",
            "Use rolling updates with maxUnavailable=0 for critical services",
            "Use a NetworkPolicy to restrict ingress/egress",
            "Ship logs and metrics to centralized observability",
            "Define SLOs and alerts for latency, error rate, saturation, and restarts",
        ]
    }


@app.get("/startupz")
async def startupz():
    if READY:
        return PlainTextResponse("ok")
    return PlainTextResponse("starting", status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
