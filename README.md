# Resilix

Resilix is a Kubernetes-native health, bottleneck detection, and resilience monitoring service with Prometheus metrics, dependency checks, alerting, and production-ready deployment support.

## What it does

Resilix helps you monitor service health and operational resilience across Kubernetes environments by exposing:

- health and readiness endpoints
- startup probe support
- Prometheus metrics
- dependency checks for HTTP, TCP, Postgres, and Redis
- Grafana dashboard assets
- Prometheus alert rules
- Helm-based deployment

## Project layout

- `k8s-health-service/` — application source, container files, manifests, Helm chart, alerts, dashboards
- `k8s-health-service/app.py` — FastAPI service
- `k8s-health-service/helm/k8s-health-service/` — Helm chart
- `k8s-health-service/grafana/` — Grafana dashboard JSON
- `k8s-health-service/alerts/` — example Prometheus alert rules

## Features

- `/healthz` for liveness checks
- `/readyz` for readiness checks
- `/startupz` for startup probe support
- `/metrics` for Prometheus scraping
- request count and latency instrumentation
- resource usage snapshots
- dependency latency and status metrics
- HPA, PDB, NetworkPolicy, and ServiceMonitor support

## Supported dependency checks

Configure downstream checks with environment variables:

- `HTTP_CHECKS`
- `TCP_CHECKS`
- `POSTGRES_DSN`
- `REDIS_URL`
- `CHECK_TIMEOUT_SECONDS`

Example:

```bash
export HTTP_CHECKS="api=https://example.com/healthz"
export TCP_CHECKS="broker=rabbitmq.default.svc.cluster.local:5672"
export POSTGRES_DSN="postgresql://app:secret@postgres.default.svc.cluster.local:5432/app"
export REDIS_URL="redis://:secret@redis.default.svc.cluster.local:6379/0"
```

## Quick start

### Run locally

```bash
cd k8s-health-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080
```

### Deploy with Helm

```bash
cd k8s-health-service
./deploy.sh dev
# or
./deploy.sh prod
```

## Included production assets

- Helm chart
- raw Kubernetes manifests
- PrometheusRule template
- Grafana dashboard JSON
- example alert rules
- dev and prod values files

## Roadmap ideas

- OpenTelemetry tracing
- deeper bottleneck diagnostics
- service-specific probes beyond Postgres and Redis
- prebuilt dashboards and alert packs for common workloads

## License

Apache-2.0

## Maintainer

- Author: Han
- Organization: Resilix
