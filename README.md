# ProductionOps — End-to-End DevOps Platform

A production-style DevOps portfolio project demonstrating the application
delivery lifecycle, from containerization and CI/CD to Kubernetes deployment,
cloud infrastructure automation, monitoring, and incident response.

The project is organized into seven days of practical implementation.
Each day adds a different capability to the same ProductionOps workflow.

## Project Goals

- Package and run a Python Flask application using Docker.
- Automate testing and security/quality checks in a Jenkins pipeline.
- Deploy an application to Kubernetes using Helm and Ingress.
- Provision AWS infrastructure using Terraform and manage an EC2 instance
  through AWS Systems Manager (SSM).
- Automate operational tasks with Ansible and Bash.
- Monitor application availability using Prometheus, Blackbox Exporter,
  and Grafana.
- Simulate an application outage, investigate it, restore service,
  and document the incident.

## Architecture

```text
                   Developer / GitHub
                           |
                           v
                    Jenkins CI/CD
                           |
                +----------+----------+
                |                     |
                v                     v
             Pytest             SonarQube
                                      |
                                      v
                               Trivy Image Scan
                                      |
                                      v
                              Docker Application
                                      |
                     +----------------+----------------+
                     |                                 |
                     v                                 v
              Kubernetes + Helm                  AWS + Terraform
               Ingress / Service               EC2 + SSM + NGINX

  Application Health Endpoint
             |
             v
      Blackbox Exporter
             |
             v
         Prometheus
             |
             v
           Grafana
             |
             v
    Availability / HTTP Status /
       Response-Time Dashboard

  Operations:
  Ansible + Bash Health Check + Incident Report
```

The diagram represents the project's implemented workflow and components.
The Kubernetes and AWS deployments are separate deployment exercises;
they are not presented as one continuously connected production system.

## Technology Stack

| Area | Technologies |
|---|---|
| Application | Python, Flask, Gunicorn |
| Version control | Git, GitHub |
| Containers | Docker, Docker Compose |
| CI/CD | Jenkins, GitHub |
| Testing | Pytest |
| Code quality | SonarQube |
| Image security | Trivy |
| Orchestration | Kubernetes, kind |
| Deployment packaging | Helm |
| Traffic routing | Kubernetes Ingress |
| Cloud | AWS EC2, Systems Manager (SSM) |
| Infrastructure as Code | Terraform |
| Configuration automation | Ansible |
| Scripting | Bash |
| Monitoring | Prometheus |
| HTTP probing | Blackbox Exporter |
| Dashboards | Grafana |
| Operating environment | Linux, Xubuntu |

## Project Journey

### Day 1 — Application and Docker

Implemented the Flask application and prepared it for container execution.

Key work:
- Created the Flask application and health endpoint.
- Added application dependencies and test dependencies.
- Created a Dockerfile to package the application.
- Configured Gunicorn to serve the application.
- Added a container health check.
- Added automated application tests.

Health endpoint:

```text
GET /health
```

Example response:

```json
{
  "environment": "production",
  "status": "healthy",
  "version": "1.0.0"
}
```

### Day 2 — CI/CD, Code Quality and Security

Created a Jenkins pipeline to automate important application checks.

Key work:
- Checked out source code from GitHub.
- Installed project and test dependencies.
- Executed automated tests with Pytest.
- Integrated SonarQube code analysis.
- Added a Trivy container-image vulnerability scan.
- Used Jenkins credentials for repository access.

The Trivy scan is configured to examine HIGH and CRITICAL vulnerabilities.
A scan finding can fail the pipeline, helping prevent vulnerable images
from passing the configured security gate.

Note: a configured scan or quality-analysis stage does not itself mean
that every vulnerability has been fixed or every quality gate has passed.

### Day 3 — Kubernetes, Helm and Ingress

Prepared Kubernetes deployment resources for the application.

Key work:
- Defined a Kubernetes namespace.
- Created application Deployment and Service manifests.
- Organized deployment configuration in a Helm chart.
- Added Ingress configuration for application routing.
- Used a local kind Kubernetes cluster for deployment practice.

This day demonstrates declarative deployment configuration and the use
of Kubernetes resources to run and expose an application.

### Day 4 — AWS and Terraform

Practiced cloud infrastructure provisioning and remote instance management.

Key work:
- Used Terraform to define AWS infrastructure.
- Configured AWS CLI authentication with an IAM user.
- Worked in the AWS Mumbai region (`ap-south-1`).
- Provisioned an EC2 instance.
- Verified AWS Systems Manager connectivity.
- Used SSM to install and start NGINX.
- Accessed the deployed NGINX website through the instance's public IP.
- Destroyed the AWS resources after verification to avoid ongoing costs.

**Current status:** The AWS deployment exercise was completed, but its
cloud resources have been destroyed. Reapply the Terraform configuration
only when you intentionally want to provision the infrastructure again.

Terraform state and local configuration files must remain out of GitHub.
Never commit AWS access keys, credentials, private keys, or sensitive
Terraform variables.

### Day 5 — Ansible and Bash Automation

Added repeatable operational checks and application verification.

Key work:
- Configured Ansible and its inventory.
- Created a system-information playbook.
- Created a preflight-check playbook.
- Created an application deployment playbook.
- Created an application verification playbook.
- Added a Bash health-check script.

The application was verified through its health endpoint and Docker
container health status.

### Day 6 — Prometheus and Grafana Monitoring

Built a lightweight monitoring stack using Docker Compose.

Components:
- **Prometheus:** scrapes and stores monitoring metrics.
- **Blackbox Exporter:** checks the application's HTTP health endpoint.
- **Grafana:** displays availability, response time, and HTTP status.

The monitoring target is:

```text
http://host.docker.internal:5001/health
```

The Prometheus scrape interval is 15 seconds. Prometheus data retention
is configured for three days to limit local disk usage.

Grafana dashboard panels:

1. **Application Availability**
   - Metric: `probe_success{job="productionops-health"}`
   - `1` means the HTTP probe succeeded.
   - `0` means the HTTP probe failed.

2. **HTTP Response Time**
   - Metric: `probe_duration_seconds{job="productionops-health"}`
   - Shows the duration of the HTTP probe.

3. **HTTP Status Code**
   - Metric: `probe_http_status_code{job="productionops-health"}`
   - A successful application response returns HTTP `200`.
   - A failed probe may show `0` because no successful HTTP response
     was received.

The Grafana dashboard and Prometheus configuration are provisioned
from files in the repository.

Local service URLs:

| Service | URL |
|---|---|
| Grafana | http://127.0.0.1:3000 |
| Prometheus | http://127.0.0.1:9090 |

Grafana login uses the locally configured admin credentials.
The password is supplied through `day-06/.env`, which must not be committed.

### Day 7 — Incident Response and Recovery

Performed a controlled application outage to practice troubleshooting.

Incident scenario:
1. Recorded the application's initial healthy state.
2. Stopped the `productionops-day5-app` container.
3. Confirmed that the health endpoint became unreachable.
4. Confirmed the Docker container entered the `exited` state.
5. Queried Prometheus and observed `probe_success = 0`.
6. Reviewed Grafana's historical dashboard.
7. Observed application availability transition from DOWN to UP.
8. Observed the HTTP status transition from `0` to `200`.
9. Restarted the application container and verified recovery.

Incident report:

```text
day-07/incident-reports/application-health-incident.md
```

This was a controlled practice incident, not an unplanned production outage.

Prometheus probing and Grafana dashboard verification were completed.
Prometheus alert rules and Alertmanager notifications are potential
future improvements and were not verified as part of this exercise.

## Repository Structure

```text
ProductionOps-DevOps-Platform/
├── day-01/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-test.txt
│   └── test_app.py
├── day-02/
│   ├── Jenkinsfile
│   └── sonar-project-properties
├── day-03/
│   ├── helm/
│   │   └── productionops-app/
│   ├── ingress/
│   └── kubernetes/
├── day-04/
│   └── terraform/
│       ├── main.tf
│       ├── provider.tf
│       └── variables.tf
├── day-05/
│   ├── ansible/
│   │   ├── ansible.cfg
│   │   ├── inventory/
│   │   └── playbooks/
│   └── scripts/
│       └── health-check.sh
├── day-06/
│   ├── blackbox/
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── provisioning/
│   ├── prometheus/
│   └── compose.yaml
├── day-07/
│   └── incident-reports/
└── README.md
```

Local secrets, virtual environments, cache directories, and Terraform state
files are intentionally excluded from the repository.

## Prerequisites

Install or configure the tools required for the specific task you want to run:

- Git
- Docker Engine and Docker Compose
- Python and pip
- Jenkins, Java, and SonarQube for CI/CD exercises
- Trivy for image scanning
- Kubernetes and kind
- Helm
- AWS CLI and suitable IAM permissions for the cloud exercise
- Terraform
- Ansible
- Prometheus and Grafana are started through the Day 6 Compose configuration

You do not need to run every component simultaneously. On a machine with
limited RAM, start only the services required for the current exercise.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/devopsbyammar/Productionops-DevOps-Platform.git
cd Productionops-DevOps-Platform
```

### Run the Flask application locally

```bash
cd day-01

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Use the application's configured address and port to test the health
endpoint. For the containerized application, the health endpoint is
`/health`.

Run the automated tests:

```bash
pip install -r requirements-test.txt
pytest -v test_app.py
```

### Build and run the Docker image

From the repository root:

```bash
docker build -t production-app:1.0.0 ./day-01

docker run -d \
  --name productionops-local-app \
  -p 5000:5000 \
  production-app:1.0.0
```

Verify the application:

```bash
curl -sS http://127.0.0.1:5000/health
```

Clean up this example container when finished:

```bash
docker rm -f productionops-local-app
```

If the chosen port or container name is already in use, inspect existing
containers before starting another instance.

### Start the Day 6 monitoring stack

First ensure the Day 5 application is running on host port 5001.
Create `day-06/.env` with a strong, private Grafana admin password.
Do not put the password in Git or share it publicly.

Start monitoring from the repository root:

```bash
cd day-06
docker compose config -q
docker compose up -d
docker compose ps
```

Open Grafana at `http://127.0.0.1:3000` and sign in using the configured
admin credentials. Prometheus is available at `http://127.0.0.1:9090`.

To stop the monitoring stack when finished:

```bash
docker compose down
```

This command stops and removes the Compose containers and network but
retains named data volumes. Do not use `-v` unless you intend to remove
the monitoring data as well.

## Useful Verification Commands

Check container state:

```bash
docker ps
docker ps -a
```

Inspect application logs:

```bash
docker logs productionops-day5-app
```

Check the health endpoint:

```bash
curl -sS http://127.0.0.1:5001/health
```

Query application availability in Prometheus:

```promql
probe_success{job="productionops-health"}
```

Review Git changes before committing:

```bash
git status --short
git diff --check
```

## Security and Cost Management

- Never commit `.env` files or passwords.
- Never commit AWS credentials, SSH private keys, or access tokens.
- Do not commit Terraform state files or local Terraform working directories.
- Review `.gitignore` before staging project changes.
- Keep `day-04/terraform/main.tf.backup` out of commits unless there is
  a deliberate reason to version it.
- Check AWS resources and billing after cloud exercises.
- Destroy cloud resources when they are no longer needed.
- Bind local monitoring interfaces to `127.0.0.1` unless remote access
  is deliberately configured and secured.

## Future Improvements

Possible next steps beyond the seven-day implementation:

- Add Prometheus alert rules and configure Alertmanager notifications.
- Add application-specific metrics and infrastructure exporters.
- Add automated deployment and rollback strategies.
- Add Kubernetes resource monitoring and alerting.
- Improve vulnerability remediation and CI/CD security gates.
- Capture sanitized screenshots of pipeline results, dashboards,
  deployments, and incident recovery.

These are improvement ideas, not claims that the features are already
implemented.

## Project Outcome

ProductionOps brings together practical experience with application
containerization, CI/CD, code-quality and image-security checks,
Kubernetes deployment, infrastructure automation, cloud operations,
monitoring, and incident troubleshooting.

The project is designed as a hands-on portfolio demonstrating how these
DevOps practices fit into an application delivery and operations workflow.

## Author

**Muhammad Ammar**

Junior DevOps Engineer | Linux | Docker | Kubernetes | CI/CD

- GitHub: https://github.com/devopsbyammar
- Project Repository: https://github.com/devopsbyammar/Productionops-DevOps-Platform

---
