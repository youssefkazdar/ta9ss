# ta9ss - Weather API (DevOps Project)

## Description
A REST API built with FastAPI that provides mock weather data, featuring structured logging, Prometheus metrics, and a full CI/CD pipeline.

## Features
- **Backend:** FastAPI
- **Container:** Docker
- **Orchestration:** Kubernetes (Minikube)
- **CI/CD:** GitHub Actions
- **Observability:** Prometheus Metrics (/metrics) and JSON Logging
- **Security:** SAST (Bandit) and DAST (OWASP ZAP)

## How to Run Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run app: `python main.py`
3. Access API: `http://localhost:8000/weather/tunis`

## Docker Usage
`docker pull youssefkazdar/ta9ss:latest`
`docker run -p 8000:8000 youssefkazdar/ta9ss:latest`

## Kubernetes Deployment
`kubectl apply -f k8s/deployment.yaml`