
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
##
## Configuration
The following table lists the configurable parameters of the workerid-frontend chart.

**Deployment Manifest Structure**

* **apiVersion:**  Specifies the Kubernetes API version used for this resource; here, "apps/v1" is for the Deployments API group.
* **kind:**  Identifies the kind of resource; in this case, it's a "Deployment".
* **metadata:**
    * **name:**  Assigns the name "workerid-frontend" to the Deployment.

**Specification (spec)**

* **replicas:**  Sets the desired number of Pod replicas to 2, ensuring the application has two instances running.
* **selector:**
    * **matchLabels:**  Defines how the Deployment should find Pods to manage. Pods with the label "app: workerid-frontend" will be selected.
* **template:** This section provides a blueprint for the Pods to be created by the Deployment.
    * **metadata:**
        * **labels:** Assigns the label "app: workerid-frontend" to the Pods, ensuring consistency with the selector for management.
    * **spec:**
        * **containers:**
            * **name:**  Names the container within the Pod "workerid-frontend".
            * **image:** Specifies the Docker image "chinooth/workerid-frontend:latest" to be used for the container.
            * **livenessProbe:**
                 * **httpGet:** Defines a periodic HTTP GET request to the "/health" path on port 80 of the container. Kubernetes will restart the container if this fails.
                 * **initialDelaySeconds:** Delay of 120 seconds before the first probe.
                 * **periodSeconds:**  Probe frequency set to every 30 seconds.
            * **readinessProbe (httpGet):**
                * **httpGet:**  Defines a periodic HTTP GET request to the "/ready" path on port 80 of the container. Kubernetes won't direct traffic to the Pod until this probe succeeds.
                 * **initialDelaySeconds:** Delay of 30 seconds before the first probe.
                 * **periodSeconds:** Probe frequency set to every 10 seconds.
            * **readinessProbe (exec):**
                 * **exec:** Executes the command "sh -c 'python check_db_connection.py'" inside the container to check database connectivity.
                 * **initialDelaySeconds:** Delay of 30 seconds before the first probe.
                 * **periodSeconds:** Probe frequency set to every 10 seconds.
            * **resources:**
                * **limits:**
                    * **cpu:**  Sets a CPU limit of 1 millicore (0.001 core).
##


**HPA Manifest Structure**

* **apiVersion:** `autoscaling/v2` - This specifies the use of the more flexible HorizontalPodAutoscaler API, version 2. This version allows for scaling based on multiple metrics and custom metrics (in addition to CPU).
* **kind:** `HorizontalPodAutoscaler` - Defines that this Kubernetes resource is specifically a HorizontalPodAutoscaler.
* **metadata.name:** `workerid-frontend-hpa` - Unique identifier for this HPA configuration.
* **spec.scaleTargetRef:**
   * **apiVersion:** `apps/v1` - The targeted resource is in the 'apps' API group, version 1.
   * **kind:** `Deployment` - The HPA will manage the scaling of a Deployment.
   * **name:**  `workerid-frontend` - The HPA controls the 'workerid-frontend' Deployment.
* **spec.minReplicas:** `2` -  The Deployment will always have at least 2 Pods running.
* **spec.maxReplicas:** `5` - The Deployment will scale up to a maximum of 5 Pods.
* **spec.metrics:**
   * **type:** `Resource` - This is a built-in resource metric (specifically, CPU utilization).
   * **resource.name:** `cpu` -  Indicates that the metric being tracked is CPU.
   * **resource.target:**
      * **type:** `Utilization` -  Specifies that the metric is a percentage of CPU use.
      *  **averageUtilization:** `80` - The goal is to maintain an average CPU usage of 80% across Pods in the Deployment.
* **spec.behavior.scaleDownCooldownSeconds:** `3` - After scaling down, there will be a delay of 3 seconds before the HPA can trigger another scale-down event.

**How the HPA Works:**

1. The HPA continuously watches the 'workerid-frontend' Deployment.
2. It measures the average CPU utilization of the Deployment's Pods.
3. **Scaling up:** If the average CPU utilization goes above 80%, the HPA instructs the Deployment to add Pods (up to the `maxReplicas` limit).
4. **Scaling down:** If the average CPU utilization falls below 80%, the HPA instructs the Deployment to reduce the number of Pods (down to the `minReplicas` limit) after the cooldown period to avoid rapid back-and-forth scaling.

##

**service Manifest Structure**

* **apiVersion: v1**
  * Specifies the Kubernetes API version to use. In this case, the core version 1.
* **kind: Service** 
  * Declares that this is a Kubernetes Service object. 
* **metadata:**
  * **name: workerid-frontend-service**
    * Assigns a human-readable name to this service. 

* **spec:**
  * **selector:**
    * **app: workerid-frontend**
      * The service will direct traffic to Pods that have the label `app: workerid-frontend`.  This is how the service identifies the backend Pods to route traffic.
  * **ports:**
    * **protocol: TCP**
      * Specifies that the service and target Pods will use TCP (Transmission Control Protocol) for communication.
    * **port: 80**
      * This is the port the service itself will expose. Clients will access the service through this port.
    * **targetPort: 80**
      * The port on the targeted Pods where the traffic will be sent. In this configuration, incoming traffic on port 80 of the service will be forwarded to port 80 of the Pods.
  * **type: ClusterIP**
    * Defines the service type.  `ClusterIP` creates a service that is only reachable from within the Kubernetes cluster.

**How It Works**

1. **Deploy Pods:**  Pods with the label `app: workerid-frontend` are deployed into your Kubernetes cluster. These are likely the Pods running the frontend application.
2. **Service Creation:** It creates an internal "virtual IP" that allows pods within the cluster to reach the service.
3. **Accessing the Frontend:** 
     * Any Pod within the Kubernetes cluster can now reach the frontend application by using the following:
       *  `workerid-frontend-service:80` 
     * Kubernetes handles the routing and balancing of traffic across replicas of Pods.

##

**Important Considerations**

* **Health Checks:** You've commendably included both liveness and readiness probes. Note that you'd need a backend to serve responses at "/health" and "/ready" for the HTTP probes to function correctly in a real project scenario.
* **Database Check:** The 'exec' readiness probe is a good way to integrate database connectivity checks. Ensure the 'check_db_connection.py' script correctly verifies your database.

## Templates Included 3 files as following:
- `deployment.yaml`: Defines the deployment configuration for the application.
- `hpa.yaml`: Configures horizontal pod autoscaling based on CPU utilization.
- `service.yaml`: Defines the service that exposes the application.
