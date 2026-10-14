# ProductionOps Incident Report: Application Health Failure

## 1. Incident Overview

- **Project:** ProductionOps — End-to-End DevOps Platform
- **Service:** Day 5 Flask application
- **Container:** `productionops-day5-app`
- **Application endpoint:** `http://127.0.0.1:5001/health`
- **Monitoring:** Prometheus, Blackbox Exporter and Grafana
- **Incident type:** Application availability failure
- **Severity:** Simulated incident for troubleshooting practice
- **Environment:** Local Xubuntu DevOps VM

## 2. Incident Summary

A controlled application outage was introduced by stopping the
`productionops-day5-app` Docker container.

The application health endpoint became unreachable. Prometheus and
Blackbox Exporter detected the failure, and the Grafana dashboard
showed the availability transition from UP to DOWN.

The application was subsequently restarted. Its health endpoint
recovered, Prometheus reported a successful probe, and Grafana
showed the transition from DOWN back to UP.

## 3. Initial Healthy State

Before the incident, the following checks were successful.

### Application health check

Command:

```bash
curl -sS http://127.0.0.1:5001/health
```

Response:

```json
{
  "environment": "production",
  "status": "healthy",
  "version": "1.0.0"
}
```

### Docker container health

Command:

```bash
docker inspect --format='{{.Name}}: {{.State.Health.Status}}' \
  productionops-day5-app
```

Observed result:

```text
/productionops-day5-app: healthy
```

### Prometheus availability metric

PromQL query:

```promql
probe_success{job="productionops-health"}
```

Initial value:

```text
1
```

Interpretation: the application health endpoint was reachable.

## 4. Incident Symptoms

After the container was stopped, the following symptoms were observed:

- The health endpoint failed to accept connections on port 5001.
- The Docker container state changed to `exited`.
- Prometheus reported `probe_success = 0`.
- Grafana displayed the application availability as DOWN.
- The HTTP status code panel showed `0` during the failed probe.
- The response-time graph showed changes during the incident and recovery.

## 5. Investigation and Troubleshooting

### Step 1: Check the application endpoint

```bash
curl --max-time 3 -sS http://127.0.0.1:5001/health
```

Observed result: connection failure while the application container
was stopped.

### Step 2: Inspect the Docker container state

```bash
docker inspect --format='{{.State.Status}}' \
  productionops-day5-app
```

Observed result:

```text
exited
```

### Step 3: Check application availability in Prometheus

```promql
probe_success{job="productionops-health"}
```

Observed value during the incident:

```text
0
```

Interpretation: Blackbox Exporter could not successfully reach the
configured application health endpoint.

### Step 4: Review Grafana dashboard

The ProductionOps dashboard was opened at:

```text
http://127.0.0.1:3000
```

The dashboard was reviewed using a Last 15 minutes time range.

The following panels were checked:

- **Application Availability:** showed DOWN during the incident and
  UP after recovery.
- **HTTP Status Code:** showed `0` during the failed probe and `200`
  after the endpoint recovered.
- **HTTP Response Time:** showed changes across the outage and recovery.

The availability graph confirmed the DOWN-to-UP transition.

## 6. Root Cause

The container had been intentionally stopped to simulate an application
availability incident.

This was a controlled exercise, not an unplanned production outage.

## 7. Resolution and Recovery

The application container was restarted.

Command:

```bash
docker start productionops-day5-app
```

The application health endpoint was checked again:

```bash
curl -sS http://127.0.0.1:5001/health
```

The application returned a healthy response with version `1.0.0`.

The container health was verified, and Prometheus returned:

```text
probe_success = 1
```

Grafana confirmed that application availability returned to UP.
The HTTP status code returned to `200`.

## 8. Monitoring and Detection

The monitoring stack consists of:

- **Prometheus:** collects and stores monitoring metrics.
- **Blackbox Exporter:** probes the application HTTP health endpoint.
- **Grafana:** visualizes application availability, HTTP response time,
  and HTTP status code.

The configured health probe targets:

```text
http://host.docker.internal:5001/health
```

The Prometheus scrape interval is 15 seconds.

The monitoring dashboard makes it possible to correlate application
availability with the observed HTTP response and status metrics.

## 9. Preventive and Follow-up Actions

Recommended production improvements:

1. Configure Prometheus alert rules for sustained application failures.
2. Configure Alertmanager if notification delivery is required.
3. Review container restart policies and application health checks.
4. Collect application logs during incidents.
5. Document recovery procedures and verify them through controlled tests.
6. Avoid relying on a dashboard alone for incident notification.

Alert rules and Alertmanager notifications are follow-up improvements;
this exercise verified monitoring and visualization, not notification
delivery.

## 10. Lessons Learned

- An unavailable endpoint can be detected using an HTTP probe.
- Docker container state helps narrow down the cause of a failure.
- Prometheus `probe_success = 0` indicates a failed probe.
- A successful probe returns `probe_success = 1`.
- Grafana historical graphs help visualize the incident and recovery.
- Verifying recovery is as important as detecting the original failure.

## 11. Final Outcome

**Incident simulation:** Successful

**Detection:** Verified through Prometheus and Blackbox Exporter

**Investigation:** Container state and endpoint failure confirmed

**Recovery:** Application restarted successfully

**Grafana verification:** DOWN → UP confirmed

**Alert notifications:** Not configured or tested in this exercise
