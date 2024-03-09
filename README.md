# Automated BigQuery Transformations with dbt, Airflow, Kubernetes, and GitHub Actions

This repository showcases a complete workflow for automating BigQuery transformations using dbt (data build tool), Apache Airflow for workflow orchestration, Kubernetes for container orchestration, and GitHub Actions for CI/CD. It demonstrates how to set up a robust data engineering environment, automating the deployment and execution of dbt models on BigQuery through a Kubernetes cluster managed by Apache Airflow.


![Project_architecture.png](Assets%2FProject_architecture.png)


## Table of Contents

- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [Assets](#assets)
- [Acknowledgments](#acknowledgments)

## Repository Structure

The repository is organized into several key directories and files:
![Project_directories.png](Assets%2FProject_directories.png)

## Getting Started

### Prerequisites

- A Kubernetes cluster (enable kubernetes in Docker Desktop)
- kubectl installed and configured -> https://kubernetes.io/docs/tasks/tools/
- Helm for managing Kubernetes applications -> https://helm.sh/docs/intro/install/
- Docker Desktop installed (for building and pushing the Docker image)
- A Google Cloud Platform account with BigQuery set up -> https://console.cloud.google.com/

### Setup Instructions

1. **Build and Push Docker Image:** Use the provided `Dockerfile` to build the Docker image containing dbt, and push it to a container registry like Docker Hub manually but you have available Github Action to do that for you.

   ```bash
   docker build --no-cache -t dbt-bigquery-image:latest .
   docker tag dbt-bigquery-image jrvm/dbt_bigquery:dbt-image
   docker push jrvm/dbt_bigquery:dbt-image
2. **Deploy Apache Airflow on Kubernetes:** You can use Helm or custom YAML files to deploy Apache Airflow on your Kubernetes cluster.

 ```bash
helm repo add apache-airflow https://airflow.apache.org
helm install airflow apache-airflow/airflow
```

3. **Configure GitHub Actions:** Set up GitHub Actions workflow (ci-cd.yml) for CI/CD to automatically build and push the Docker image upon changes to the dbt project.

4. **Deploy dbt and Run Transformations:** Use the Airflow DAG (dbt_bq_final.py) to run dbt commands (dbt run, dbt test, dbt seed) against your BigQuery dataset.

### Usage
- **Apache Airflow Web UI:** Access the Airflow web UI to manage, schedule, and monitor the dbt transformation workflows.
- **Kubernetes Dashboard:** Optionally, use the Kubernetes Dashboard to monitor the Kubernetes cluster.
- **GitHub Actions:** Monitor the CI/CD pipeline runs within your GitHub repository's Actions tab.

### Contributing
Contributions to enhance the functionality, improve documentation, or fix issues are welcome. Please open an issue or submit a pull request.
Or support my contributions with buying me a coffe: https://www.buymeacoffee.com/rafael.vera

### Assets
in this folder you can find useful docs like used and helpfull commands, image, and simple slides presentation with light comments

### Acknowledgments
I'd like to express my sincere gratitude to all contributors and mentors who have supported this project. A special shoutout to my teacher Yusuf Ganiyu for his guidance and to my family for their patience and support.
