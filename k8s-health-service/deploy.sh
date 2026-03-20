#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${1:-dev}"
RELEASE="k8s-health-service"
NAMESPACE="observability"
CHART="./helm/k8s-health-service"

case "$ENVIRONMENT" in
  dev)
    VALUES_FILE="$CHART/values-dev.yaml"
    ;;
  prod)
    VALUES_FILE="$CHART/values-prod.yaml"
    ;;
  *)
    echo "Usage: $0 [dev|prod]" >&2
    exit 1
    ;;
esac

helm upgrade --install "$RELEASE" "$CHART" \
  -n "$NAMESPACE" \
  --create-namespace \
  -f "$VALUES_FILE"
