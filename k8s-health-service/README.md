# k8s-health-service

Production-grade FastAPI service for Kubernetes health monitoring, dependency checks, resilience guidance, Prometheus metrics, alert rules, and Grafana dashboards.

## Features

- `/healthz` for liveness and resource snapshot
- `/readyz` for readiness based on downstream dependency checks
- `/startupz` for startup probe support
- `/metrics` for Prometheus scraping
- `/metrics-summary` for quick bottleneck-oriented JSON output
- `/resilience` for platform hardening recommendations
- first-class Postgres and Redis checks
- non-root container with stricter security defaults
- Kubernetes manifests with Deployment, Service, PDB, HPA, NetworkPolicy, and ServiceMonitor
- Helm templates for PrometheusRule alerts
- Grafana dashboard JSON included

## Dependency checks

Set optional env vars to check downstream services.

- `HTTP_CHECKS` format: `name=https://url,name2=https://url2`
- `TCP_CHECKS` format: `service=host:port,service2=host:port`
- `POSTGRES_DSN` format: `postgresql://user:password@host:5432/dbname`
- `REDIS_URL` format: `redis://:password@host:6379/0`
- `CHECK_TIMEOUT_SECONDS` default: `2.0`

Example:

```bash
export HTTP_CHECKS="api=https://example.com/healthz"
export TCP_CHECKS="broker=rabbitmq.default.svc.cluster.local:5672"
export POSTGRES_DSN="postgresql://app:secret@postgres.default.svc.cluster.local:5432/app"
export REDIS_URL="redis://:secret@redis.default.svc.cluster.local:6379/0"
```

## Run locally

```bash
cd k8s-health-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080
curl http://127.0.0.1:8080/healthz
curl http://127.0.0.1:8080/metrics
```

## Build and push image

```bash
docker build -t your-registry/k8s-health-service:latest .
docker push your-registry/k8s-health-service:latest
```

## Deploy with Helm

```bash
helm upgrade --install k8s-health-service ./helm/k8s-health-service -n observability --create-namespace
```

Then set your real image and env values, for example with `--set` or a custom values file.

## Included observability assets

- Grafana dashboard: `grafana/k8s-health-service-dashboard.json`
- Alert rules: `helm/k8s-health-service/templates/prometheusrule.yaml`

## Suggested next integrations

- kube-prometheus-stack
- Alertmanager notification routes
- ingress/TLS if you want external access
- OpenTelemetry tracing if you want cross-service latency breakdowns
