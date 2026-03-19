# k8s-health-service

A small Python/FastAPI service you can deploy to Kubernetes to expose:

- `/healthz` — liveness-style health status
- `/readyz` — readiness-style dependency status
- `/metrics-summary` — bottleneck hints and recommended signals
- `/resilience` — operational hardening recommendations

## Run locally

```bash
cd k8s-health-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080
```

## Build container

```bash
docker build -t your-registry/k8s-health-service:latest .
```

## Deploy to Kubernetes

```bash
kubectl apply -f k8s.yaml
```

## Notes

This is a starter service. For real bottleneck detection, plug in:

- Prometheus + Grafana
- kube-state-metrics
- node-exporter
- application request/error/latency metrics
- dependency checks for DB, cache, queue, and external APIs
