# Deploy

## Quick start

From the `k8s-health-service` directory:

### Dev

```bash
./deploy.sh dev
```

### Prod

```bash
./deploy.sh prod
```

## Before deploying

Update these values in the appropriate file:

- `helm/k8s-health-service/values-dev.yaml`
- `helm/k8s-health-service/values-prod.yaml`

Set at minimum:

- `image.repository`
- `image.tag`
- `env.HTTP_CHECKS`
- `env.TCP_CHECKS`
- `env.POSTGRES_DSN`
- `env.REDIS_URL`

## Example prod command with overrides

```bash
helm upgrade --install k8s-health-service ./helm/k8s-health-service \
  -n observability \
  --create-namespace \
  -f ./helm/k8s-health-service/values-prod.yaml \
  --set image.repository=ghcr.io/your-org/k8s-health-service \
  --set image.tag=1.0.0
```
