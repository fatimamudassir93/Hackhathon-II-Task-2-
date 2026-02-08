# Quickstart: Cloud-Native Todo Chatbot Deployment

**Feature**: 003-cloud-native-todo-deploy
**Date**: 2026-02-08

## Prerequisites

| Tool | Minimum Version | Verify Command |
|------|----------------|----------------|
| Docker Desktop | 4.x | `docker --version` |
| Minikube | 1.32+ | `minikube version` |
| kubectl | 1.28+ | `kubectl version --client` |
| Helm | 3.14+ | `helm version` |
| Docker AI (Gordon) | Latest | `docker ai --version` |
| kubectl-ai | Latest | `kubectl-ai --version` |
| Node.js | 20.x | `node --version` |
| Python | 3.11.x | `python --version` |

## Step 1: Start Minikube

```bash
minikube start --driver=docker --cpus=2 --memory=4096
```

Verify:

```bash
minikube status
kubectl cluster-info
```

## Step 2: Build Docker Images

### Frontend

```bash
docker build -t todo-frontend:1.0.0 frontend/
```

### Backend

```bash
docker build -t todo-backend:1.0.0 backend/
```

## Step 3: Load Images into Minikube

```bash
minikube image load todo-frontend:1.0.0
minikube image load todo-backend:1.0.0
```

Verify:

```bash
minikube image ls | grep todo-
```

## Step 4: Deploy with Helm

```bash
helm install todo-chatbot ./charts/todo-chatbot \
  --set backend.secrets.DATABASE_URL="<your-database-url>" \
  --set backend.secrets.BETTER_AUTH_SECRET="<your-auth-secret>" \
  --set backend.secrets.GROQ_API_KEY="<your-groq-key>" \
  --set frontend.secrets.BETTER_AUTH_SECRET="<your-auth-secret>" \
  --set frontend.secrets.DATABASE_URL="<your-database-url>"
```

Verify:

```bash
kubectl get pods
kubectl get services
helm status todo-chatbot
```

## Step 5: Access the Application

### Frontend (browser)

```bash
minikube service todo-frontend --url
```

Open the returned URL in your browser.

### Backend (API verification)

```bash
kubectl port-forward svc/todo-backend 8001:8001
curl http://localhost:8001/health
```

## Step 6: Verify Health

```bash
# All pods running
kubectl get pods

# Pod logs
kubectl logs -l app.kubernetes.io/name=frontend
kubectl logs -l app.kubernetes.io/name=backend

# Pod details
kubectl describe pods -l app.kubernetes.io/name=frontend
kubectl describe pods -l app.kubernetes.io/name=backend
```

## Step 7: Test Pod Recovery

```bash
# Delete a frontend pod
kubectl delete pod -l app.kubernetes.io/name=frontend --wait=false

# Watch it recover
kubectl get pods -w
```

## Teardown

```bash
# Remove all deployed resources
helm uninstall todo-chatbot

# Verify cleanup
kubectl get all

# Stop Minikube (optional)
minikube stop
```

## Troubleshooting

### Pods stuck in ImagePullBackOff

```bash
# Images not loaded into Minikube. Reload:
minikube image load todo-frontend:1.0.0
minikube image load todo-backend:1.0.0

# Verify imagePullPolicy is "Never" in values.yaml
```

### Pods in CrashLoopBackOff

```bash
# Check logs for startup errors
kubectl logs <pod-name>

# Check environment variables are set
kubectl describe pod <pod-name>
```

### Cannot access frontend via browser

```bash
# Use minikube service to get the URL
minikube service todo-frontend --url

# Or use minikube tunnel for LoadBalancer type
minikube tunnel
```

### Frontend cannot reach backend

```bash
# Verify backend service exists
kubectl get svc todo-backend

# Test DNS resolution from a pod
kubectl exec -it <frontend-pod> -- nslookup todo-backend

# Check backend logs for errors
kubectl logs -l app.kubernetes.io/name=backend
```
