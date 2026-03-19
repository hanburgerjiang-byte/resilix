# k8s-health-service

Production-grade FastAPI service for Kubernetes health monitoring, dependency checks, resilience guidance, and Prometheus metrics.

## Features

- `/healthz` for liveness and resource snapshot
- `/readyz` for readiness based on downstream dependency checks
- `/startupz` for startup probe support
- `/metrics` for Prometheus scraping
- `/metrics-summary` for quick bottleneck-oriented JSON output
- `/resilience` for platform hardening recommendations
- non-root container with stricter security defaults
- Kubernetes manifests with Deployment, Service, PDB, HPA, NetworkPolicy, and ServiceMonitor

## Dependency checks

Set optional env vars to check downstream services.

- `HTTP_CHECKS` format: `name=https://url,name2=https://url2`
- `TCP_CHECKS` format: `postgres=postgres.default.svc.cluster.local:5432,redis=redis.default.svc.cluster.local:6379`
- `CHECK_TIMEOUT_SECONDS` default: `2.0`

Example:

```bash
export HTTP_CHECKS="api=https://example.com/healthz"
export TCP_CHECKS="postgres=postgres.default.svc.cluster.local:5432"
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

## Deploy raw manifests

Update the image reference in `k8s.yaml`, then deploy:

```bash
kubectl apply -f k8s.yaml
```

## Deploy with Helm

```bash
helm upgrade --install k8s-health-service ./helm/k8s-health-service -n observability --create-namespace
```

## Recommended platform additions

For full production visibility, pair this with:

- Prometheus Operator or kube-prometheus-stack
- Grafana dashboards
- Alertmanager rules for latency, error rate, restart spikes, CPU throttling, memory pressure, and failed dependency checks
- kube-state-metrics and node-exporter
- ingress/TLS if you want external access

## Suggested alerts

- readiness failures > 0 for 5m
- p95 latency above threshold for 10m
- error rate above threshold for 5m
- restart count increase
- CPU throttling sustained
- memory usage above 85% of limit
- dependency status metric equals 0
