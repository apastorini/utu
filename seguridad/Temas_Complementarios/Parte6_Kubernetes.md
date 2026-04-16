# CURSO COMPLETO DE CIBERSEGURIDAD - PARTE 7

## MÓDULO 11: KUBERNETES SECURITY

### 11.1 Arquitectura de Kubernetes

```
┌────────────────────────────────────────────────────────────┐
│              KUBERNETES CLUSTER                            │
└────────────────────────────────────────────────────────────┘

CONTROL PLANE
┌─────────────────────────────────────────────────────────┐
│  • API Server (puerto 6443)                             │
│  • etcd (almacén de configuración)                      │
│  • Scheduler                                            │
│  • Controller Manager                                   │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ Comunicación segura (TLS)
                 │
        ┌────────┴────────┐
        │                 │
   ┌────▼────┐       ┌────▼────┐
   │ Node 1  │       │ Node 2  │
   │         │       │         │
   │ ┌─────┐ │       │ ┌─────┐ │
   │ │ Pod │ │       │ │ Pod │ │
   │ └─────┘ │       │ └─────┘ │
   └─────────┘       └─────────┘
```

### 11.2 RBAC (Role-Based Access Control)

```yaml
# Role: Define permisos en un namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: produccion
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]

---
# RoleBinding: Asigna Role a usuario
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: produccion
subjects:
- kind: User
  name: juan
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### 11.3 Network Policies

```yaml
# Denegar todo el tráfico por defecto
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: produccion
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
# Permitir solo tráfico específico
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

### 11.4 Pod Security Standards

```yaml
# Pod con configuración segura
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  
  containers:
  - name: app
    image: myapp:1.0
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    resources:
      limits:
        memory: "128Mi"
        cpu: "500m"
      requests:
        memory: "64Mi"
        cpu: "250m"
```

### 11.5 Secrets Management

```bash
# Crear secret
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=secreto123

# Usar secret en Pod
apiVersion: v1
kind: Pod
metadata:
  name: app-with-secrets
spec:
  containers:
  - name: app
    image: myapp:1.0
    env:
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: password
```

### 11.6 Laboratorio: Cluster Seguro

```bash
# 1. Instalar Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# 2. Iniciar cluster
minikube start

# 3. Habilitar RBAC
kubectl create namespace secure-app

# 4. Crear ServiceAccount
kubectl create serviceaccount app-sa -n secure-app

# 5. Aplicar Network Policy
kubectl apply -f network-policy.yaml

# 6. Escanear vulnerabilidades
trivy k8s --report summary cluster
```

