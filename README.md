
# workerid-frontend Helm Chart

## Description
This Helm chart deploys the "workerid-frontend" application,includes configurations for CPU horizontal pod autoscaling.

## Chart Details
- **Chart Name:** workerid-frontend
- **Chart Version:** 1.0.1
- **API Version:** v2

## Maintainers
- Hazhir (hdakei@gmail.com)

## Prerequisites
- Kubernetes 1.19+
- Helm 3.0+

## Installing the Chart
To install the chart with the release name `workerid`:

```bash
helm install workerid path/to/your/chart/workerid-frontend
```

## Uninstalling the Chart
To uninstall/delete the `workerid` deployment:

```bash
helm delete workerid
```

## Configuration
The following table lists the configurable parameters of the workerid-frontend chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `2` |
| `service.type` | Kubernetes Service type | `"ClusterIP"` |
| `service.port` | Service HTTP port | `80` |

## Templates Included 3 files as following:
- `deployment.yaml`: Defines the deployment configuration for the application.
- `hpa.yaml`: Configures horizontal pod autoscaling based on CPU utilization.
- `service.yaml`: Defines the service that exposes the application.
