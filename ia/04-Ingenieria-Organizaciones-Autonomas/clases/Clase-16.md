# Clase 16: Auto-scaling de Agentes

## Duración
4 horas (240 minutos)

## Objetivos de Aprendizaje
- Comprender las estrategias de auto-scaling para agentes basados en carga de trabajo real
- Implementar Horizontal Pod Autoscaler (HPA) con métricas de CPU, memoria y personalizadas
- Configurar KEDA (Kubernetes Event-Driven Autoscaling) para scaling basado en eventos
- Implementar queue-based scaling con RabbitMQ y Kafka
- Diseñar estrategias de scaling predictivo usando machine learning
- Integrar Prometheus como fuente de métricas para decisiones de scaling

## Contenidos Detallados

### 16.1 Fundamentos de Auto-scaling para Agentes (60 minutos)

El auto-scaling de agentes es crítico en organizaciones autónomas donde la carga de trabajo varía dinámicamente. A diferencia de aplicaciones web tradicionales, los agentes pueden experimentar picos de demanda impredecibles debido a eventos externos, decisiones de otros agentes, o cambios en el entorno.

#### 16.1.1 Arquitectura de Auto-scaling

```mermaid
graph TB
    subgraph "Metrics Sources"
        CPU["CPU/Memory Metrics<br/>(Metrics Server)"]
        PROM["Custom Metrics<br/>(Prometheus)"]
        KAFKA["Queue Depth<br/>(Kafka/RabbitMQ)"]
        CUST["Custom Events<br/>(HTTP, gRPC)"]
        SCHED["Scheduled<br/>(Cron)"]
        PRED["Predictive<br/>(ML Model)"]
    end
    
    subgraph "Scaling Controllers"
        HPA["Horizontal Pod<br/>Autoscaler"]
        KEDA["KEDA Scaler<br/>(Event-Driven)"]
        VPA["Vertical Pod<br/>Autoscaler"]
        CA["Cluster<br/>Autoscaler"]
    end
    
    subgraph "Scaling Decisions"
        SD["Scale Decision Engine"]
    end
    
    subgraph "Actions"
        SCALE_UP["Scale Up<br/>+ pods"]
        SCALE_DOWN["Scale Down<br/>- pods"]
        VERTICAL["Adjust Resources<br/>CPU/Memory"]
        NODES["Add/Remove<br/>Nodes"]
    end
    
    CPU --> HPA
    PROM --> HPA
    KAFKA --> KEDA
    CUST --> KEDA
    SCHED --> KEDA
    PRED --> HPA
    PRED --> KEDA
    
    HPA --> SD
    KEDA --> SD
    VPA --> SD
    CA --> SD
    
    SD --> SCALE_UP
    SD --> SCALE_DOWN
    SD --> VERTICAL
    SD --> NODES
    
    style HPA fill:#2196f3
    style KEDA fill:#4caf50
    style VPA fill:#ff9800
    style CA fill:#9c27b0
    style SCALE_UP fill:#e8f5e9
    style SCALE_DOWN fill:#ffebee
```

#### 16.1.2 Métricas Clave para Scaling de Agentes

```mermaid
graph LR
    subgraph "Resource Metrics"
        CPU["CPU Utilization<br/>Target: 70%"]
        MEM["Memory Usage<br/>Target: 80%"]
    end
    
    subgraph "Business Metrics"
        DPS["Decisions/sec<br/>Per Pod"]
        QD["Queue Depth<br/>Total"]
        LAT["Latency P95<br/>< 500ms"]
        ERR["Error Rate<br/>< 1%"]
    end
    
    subgraph "Event-Driven Metrics"
        MSG["Messages in Queue<br/>(Kafka/RabbitMQ)"]
        EVT["Event Stream Rate<br/>Events/sec"]
        BATCH["Batch Size<br/>Pending Jobs"]
    end
    
    subgraph "Predictive Metrics"
        HIST["Historical Patterns<br/>Time Series"]
        TREND["Trend Analysis<br/>ML Forecast"]
        SEASON["Seasonal Patterns<br/>Day/Week/Month"]
    end
    
    CPU -->|"HPA Resource"| SCALE
    MEM -->|"HPA Resource"| SCALE
    DPS -->|"HPA Custom"| SCALE
    QD -->|"HPA Custom"| SCALE
    LAT -->|"Alert"| SCALE
    MSG -->|"KEDA"| SCALE
    EVT -->|"KEDA"| SCALE
    HIST -->|"ML Model"| SCALE
    TREND -->|"ML Model"| SCALE
    
    SCALE["Scale Decision"]
    
    style SCALE fill:#e91e63
```

**Tipos de Escalado:**

| Tipo | Mecanismo | Latencia | Ideal para |
|------|-----------|----------|------------|
| **Reactive** | HPA (CPU/Memoria) | 1-5 min | Cargas predecibles |
| **Custom Metrics** | HPA + Prometheus | 1-3 min | Métricas de negocio |
| **Event-Driven** | KEDA | 10-30s | Colas de mensajes |
| **Predictive** | ML + Pre-scaling | 0s (pre-escalado) | Patrones conocidos |
| **Scheduled** | Cron + KEDA | Exacto | Horarios fijos |

### 16.2 HPA Avanzado con Prometheus (75 minutos)

#### 16.2.1 Configuración de Prometheus Adapter

```bash
# 1. Instalar Prometheus Stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

cat <<EOF > prometheus-values.yaml
prometheus:
  prometheusSpec:
    scrapeInterval: 15s
    evaluationInterval: 15s
    ruleSelectorNilUsesHelmValues: false
    serviceMonitorSelectorNilUsesHelmValues: false
  
  additionalScrapeConfigs:
    - job_name: 'agent-metrics'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        regex: agent-worker
        action: keep
      - source_labels: [__address__]
        regex: (.+):(\d+)
        action: replace
        target_label: __address__
        replacement: \1:8000
      metrics_path: /metrics

grafana:
  adminPassword: admin
  defaultDashboardsTimezone: America/Mexico_City
EOF

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  -f prometheus-values.yaml

# 2. Instalar Prometheus Adapter para custom metrics
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

cat <<EOF > adapter-values.yaml
prometheus:
  url: http://prometheus-kube-prometheus-prometheus.monitoring:9090
  port: 9090

rules:
  default: false
  custom:
  - seriesQuery: 'agent_decisions_total'
    resources:
      overrides:
        namespace:
          resource: "namespace"
        pod:
          resource: "pod"
    name:
      matches: 'agent_decisions_total'
      as: 'agent_decisions_per_second'
    metricsQuery: |
      sum(rate(agent_decisions_total[1m])) by (<<.GroupBy>>)
  - seriesQuery: 'agent_request_queue_depth'
    resources:
      overrides:
        namespace:
          resource: "namespace"
        pod:
          resource: "pod"
    name:
      matches: 'agent_request_queue_depth'
      as: 'agent_queue_depth'
    metricsQuery: |
      avg(agent_request_queue_depth) by (<<.GroupBy>>)
  - seriesQuery: 'agent_active_connections'
    resources:
      overrides:
        namespace:
          resource: "namespace"
        pod:
          resource: "pod"
    name:
      matches: 'agent_active_connections'
      as: 'agent_active_connections'
    metricsQuery: |
      sum(agent_active_connections) by (<<.GroupBy>>)
EOF

helm install prometheus-adapter prometheus-community/prometheus-adapter \
  --namespace monitoring \
  -f adapter-values.yaml

# 3. Verificar que el adapter expone las métricas
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1 | jq .

# Probar métricas específicas
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1/namespaces/agents/pods/*/agent_queue_depth | jq .
```

#### 16.2.2 HPA Multi-Métrica para Agentes

```yaml
# 16-scaling/agent-hpa-advanced.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: agent-hpa-advanced
  namespace: agents
  annotations:
    description: "HPA avanzado para agentes con múltiples métricas"
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-worker
  minReplicas: 3
  maxReplicas: 30
  metrics:
  # 1. Resource: CPU (escalado base)
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  
  # 2. Resource: Memoria (escalado base)
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  
  # 3. Custom: Decisiones por segundo (métrica de negocio)
  - type: Pods
    pods:
      metric:
        name: agent_decisions_per_second
      target:
        type: AverageValue
        averageValue: "50"
  
  # 4. Custom: Profundidad de cola de requests
  - type: Pods
    pods:
      metric:
        name: agent_queue_depth
      target:
        type: AverageValue
        averageValue: "100"
  
  # 5. Custom: Conexiones activas
  - type: Pods
    pods:
      metric:
        name: agent_active_connections
      target:
        type: AverageValue
        averageValue: "25"
  
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

#### 16.2.3 Generación de Métricas desde el Agente

```python
# src/metrics/advanced_metrics.py
"""
Sistema de métricas avanzadas para auto-scaling de agentes.
Expone métricas en formato Prometheus para consumo por HPA/KEDA.
"""
import os
import time
import asyncio
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from prometheus_client import (
    Counter, Histogram, Gauge, Summary,
    start_http_server, generate_latest, REGISTRY
)
from fastapi import FastAPI, Response
from contextlib import asynccontextmanager

# ─── Métricas de Negocio ─────────────────────────────────────────────

# Decisiones del agente
decisions_total = Counter(
    'agent_decisions_total',
    'Total number of decisions made',
    ['agent_id', 'decision_type', 'status']
)

decisions_per_second = Counter(
    'agent_decisions_per_second',
    'Rate of decisions per second',
    ['agent_id']
)

# Latencia de decisiones
decision_duration = Histogram(
    'agent_decision_duration_seconds',
    'Decision processing duration',
    ['agent_id', 'decision_type'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0)
)

# Cola de requests
request_queue_depth = Gauge(
    'agent_request_queue_depth',
    'Current request queue depth per agent',
    ['agent_id']
)

request_queue_latency = Gauge(
    'agent_request_queue_latency_seconds',
    'Current queue wait time',
    ['agent_id']
)

# Conexiones activas
active_connections = Gauge(
    'agent_active_connections',
    'Current active connections',
    ['agent_id']
)

# LLM Usage
llm_calls_total = Counter(
    'agent_llm_calls_total',
    'Total LLM API calls',
    ['agent_id', 'model', 'provider']
)

llm_tokens_consumed = Counter(
    'agent_llm_tokens_total',
    'Total tokens consumed',
    ['agent_id', 'direction']  # input / output
)

llm_latency = Histogram(
    'agent_llm_latency_seconds',
    'LLM API call latency',
    ['agent_id', 'model'],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0)
)

# Memoria del agente
memory_usage = Gauge(
    'agent_memory_usage_bytes',
    'Memory usage per component',
    ['agent_id', 'component']  # state, cache, working, llm_context
)

# Performance de peers
peer_communication_latency = Summary(
    'agent_peer_comm_latency_seconds',
    'Latency in peer-to-peer communication',
    ['agent_id', 'peer_id']
)

# Cache hit ratio
cache_hits_total = Counter(
    'agent_cache_hits_total',
    'Total cache operations',
    ['agent_id', 'cache_type', 'result']  # hit / miss
)


@dataclass
class AgentMetricsCollector:
    """Recolector de métricas para auto-scaling"""
    
    agent_id: str
    metrics_port: int = 8001
    
    def __post_init__(self):
        self._setup_metrics()
    
    def _setup_metrics(self):
        """Inicializa métricas con labels del agente"""
        self.agent_labels = {'agent_id': self.agent_id}
    
    def record_decision(self, decision_type: str, duration: float, status: str = "success"):
        """Registra una decisión del agente"""
        decisions_total.labels(
            agent_id=self.agent_id,
            decision_type=decision_type,
            status=status
        ).inc()
        
        decisions_per_second.labels(
            agent_id=self.agent_id
        ).inc()
        
        decision_duration.labels(
            agent_id=self.agent_id,
            decision_type=decision_type
        ).observe(duration)
    
    def update_queue_depth(self, depth: int):
        """Actualiza profundidad de cola (métrica crítica para HPA)"""
        request_queue_depth.labels(
            agent_id=self.agent_id
        ).set(depth)
    
    def update_connections(self, count: int):
        """Actualiza número de conexiones activas"""
        active_connections.labels(
            agent_id=self.agent_id
        ).set(count)
    
    def record_llm_call(self, model: str, provider: str, duration: float, tokens_in: int, tokens_out: int):
        """Registra llamada a LLM"""
        llm_calls_total.labels(
            agent_id=self.agent_id,
            model=model,
            provider=provider
        ).inc()
        
        llm_tokens_consumed.labels(
            agent_id=self.agent_id,
            direction="input"
        ).inc(tokens_in)
        
        llm_tokens_consumed.labels(
            agent_id=self.agent_id,
            direction="output"
        ).inc(tokens_out)
        
        llm_latency.labels(
            agent_id=self.agent_id,
            model=model
        ).observe(duration)
    
    def record_cache_operation(self, cache_type: str, hit: bool):
        """Registra operación de caché"""
        cache_hits_total.labels(
            agent_id=self.agent_id,
            cache_type=cache_type,
            result="hit" if hit else "miss"
        ).inc()
    
    def update_memory_usage(self, component: str, bytes_used: int):
        """Actualiza uso de memoria por componente"""
        memory_usage.labels(
            agent_id=self.agent_id,
            component=component
        ).set(bytes_used)


# ─── Aplicación FastAPI con métricas ─────────────────────────────────

metrics_collector = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa el recolector de métricas al inicio"""
    global metrics_collector
    agent_id = os.getenv('AGENT_ID', 'unknown')
    metrics_collector = AgentMetricsCollector(agent_id=agent_id)
    
    # Iniciar servidor de métricas en puerto separado
    start_http_server(metrics_collector.metrics_port)
    
    # Iniciar tarea de actualización periódica de gauges
    asyncio.create_task(_periodic_gauges_update())
    
    yield
    
    # Cleanup al apagar
    REGISTRY.unregister(decisions_total)


app = FastAPI(lifespan=lifespan)


async def _periodic_gauges_update():
    """Actualiza métricas de gauge periódicamente (simulación)"""
    while True:
        if metrics_collector:
            # Simular cambios en la carga
            metrics_collector.update_queue_depth(random.randint(0, 500))
            metrics_collector.update_connections(random.randint(5, 100))
            metrics_collector.update_memory_usage("state", random.randint(50, 200) * 1024 * 1024)
            metrics_collector.update_memory_usage("cache", random.randint(20, 100) * 1024 * 1024)
            metrics_collector.update_memory_usage("working", random.randint(100, 500) * 1024 * 1024)
        await asyncio.sleep(15)


@app.get("/metrics")
async def metrics_endpoint():
    """Endpoint de métricas Prometheus para scraping"""
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_id": os.getenv('AGENT_ID'),
        "metrics_port": metrics_collector.metrics_port if metrics_collector else 8001
    }


@app.post("/api/decide")
async def make_decision(decision_type: str = "default", duration: float = None):
    """Endpoint de ejemplo que registra métricas de decisión"""
    import time
    start = time.time()
    
    # Simular procesamiento
    actual_duration = duration or random.uniform(0.01, 2.0)
    await asyncio.sleep(actual_duration)
    
    if metrics_collector:
        metrics_collector.record_decision(
            decision_type=decision_type,
            duration=time.time() - start
        )
    
    return {
        "decision_id": f"dec_{int(time.time())}",
        "duration": time.time() - start
    }
```

### 16.3 KEDA: Event-Driven Autoscaling (60 minutos)

KEDA (Kubernetes Event-Driven Autoscaling) es un controlador de escalado que extiende HPA para manejar fuentes de eventos externas, permitiendo escalar agentes basados en la demanda real de procesamiento.

#### 16.3.1 Arquitectura de KEDA

```mermaid
graph TB
    subgraph "KEDA Architecture"
        OP["KEDA Operator"]
        MET["Metrics Server<br/>(gRPC)"]
        SVC["ScaledObject CRD"]
    end
    
    subgraph "Event Sources (Scalers)"
        RABBIT["RabbitMQ"]
        KAFKA["Kafka"]
        PROM["Prometheus"]
        HTTP["HTTP Requests"]
        CRON["Cron Schedule"]
        AWS["AWS SQS/SNS"]
        AZURE["Azure Queue"]
    end
    
    subgraph "Kubernetes"
        HPA["Horizontal Pod<br/>Autoscaler"]
        DEPLOY["Deployment"]
        PODS["Pods (Agentes)"]
    end
    
    RABBIT -->|"queue depth"| MET
    KAFKA -->|"lag"| MET
    PROM -->|"custom metric"| MET
    HTTP -->|"request rate"| MET
    CRON -->|"schedule"| MET
    AWS -->|"message count"| MET
    AZURE -->|"message count"| MET
    
    MET -->|"expose metric"| HPA
    OP -->|"watch"| SVC
    SVC -->|"configure"| OP
    OP -->|"create/update"| HPA
    HPA -->|"scale"| DEPLOY
    DEPLOY -->|"manage"| PODS
    
    style OP fill:#4caf50
    style MET fill:#4caf50
    style SVC fill:#4caf50
    style HPA fill:#2196f3
```

```bash
# Instalación de KEDA
helm repo add kedacore https://kedacore.github.io/charts
helm repo update

helm install keda kedacore/keda \
  --namespace keda \
  --create-namespace \
  --set podIdentity.provider=none \
  --set serviceAccount.create=true

# Verificar instalación
kubectl get pods -n keda
kubectl get crd | grep keda

# Debería mostrar:
# scaledobjects.keda.sh
# triggerauthentications.keda.sh
# clustertriggerauthentications.keda.sh
```

#### 16.3.2 ScaledObject para Agentes

```yaml
# 16-scaling/keda-rabbitmq.yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: agent-rabbitmq-scaler
  namespace: agents
  labels:
    app: agent-worker
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-worker
  minReplicaCount: 1
  maxReplicaCount: 20
  pollingInterval: 10
  cooldownPeriod: 120
  idReplicaCount: 0  # Permitir 0 réplicas si no hay mensajes
  triggers:
  - type: rabbitmq
    metadata:
      protocol: amqp
      queueName: agent.decisions
      mode: QueueLength
      value: "5"  # Escalar si cola > 5 mensajes
      activationValue: "1"  # Activar desde 0 si hay al menos 1 mensaje
    authenticationRef:
      name: keda-rabbitmq-auth
---
apiVersion: keda.sh/v1alpha1
kind: TriggerAuthentication
metadata:
  name: keda-rabbitmq-auth
  namespace: agents
spec:
  secretTargetRef:
  - parameter: host
    name: rabbitmq-secrets
    key: connection-string
```

```yaml
# 16-scaling/keda-kafka.yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: agent-kafka-scaler
  namespace: agents
  labels:
    app: agent-worker
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-worker
  minReplicaCount: 2
  maxReplicaCount: 30
  pollingInterval: 10
  cooldownPeriod: 60
  advanced:
    restoreNormalized: false
    horizontalPodAutoscalerConfig:
      behavior:
        scaleUp:
          stabilizationWindowSeconds: 0
          policies:
          - type: Percent
            value: 200
            periodSeconds: 15
          selectPolicy: Max
        scaleDown:
          stabilizationWindowSeconds: 300
          policies:
          - type: Percent
            value: 20
            periodSeconds: 60
  triggers:
  - type: kafka
    metadata:
      bootstrapServers: kafka-cluster.kafka.svc.cluster.local:9092
      topic: agent-events
      consumerGroup: agent-workers
      lagThreshold: "50"  # Escalar si lag > 50 mensajes
      offsetResetPolicy: latest
    authenticationRef:
      name: keda-kafka-auth
---
apiVersion: v1
kind: Secret
metadata:
  name: kafka-secrets
  namespace: agents
stringData:
  sasl: "scram-sha-512"
  username: "agent-consumer"
  password: "secure-password-123"
---
apiVersion: keda.sh/v1alpha1
kind: TriggerAuthentication
metadata:
  name: keda-kafka-auth
  namespace: agents
spec:
  secretTargetRef:
  - parameter: sasl
    name: kafka-secrets
    key: sasl
  - parameter: username
    name: kafka-secrets
    key: username
  - parameter: password
    name: kafka-secrets
    key: password
```

#### 16.3.3 ScaledObject con Prometheus y Múltiples Triggers

```yaml
# 16-scaling/keda-multi-trigger.yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: agent-multi-trigger
  namespace: agents
  labels:
    app: agent-worker
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-worker
  minReplicaCount: 2
  maxReplicaCount: 50
  pollingInterval: 15
  cooldownPeriod: 60
  triggers:
  # Trigger 1: Prometheus - métricas personalizadas
  - type: prometheus
    metadata:
      serverAddress: http://prometheus-kube-prometheus-prometheus.monitoring:9090
      metricName: agent_decisions_per_second
      query: |
        sum(rate(agent_decisions_total[2m])) by (pod)
      threshold: "50"
      activationThreshold: "10"
  
  # Trigger 2: CPU Utilization (via Prometheus)
  - type: prometheus
    metadata:
      serverAddress: http://prometheus-kube-prometheus-prometheus.monitoring:9090
      metricName: agent_cpu_utilization
      query: |
        avg(rate(container_cpu_usage_seconds_total{namespace="agents",container="agent"}[1m])) by (pod) 
        / ignoring(pod) 
        avg(kube_pod_container_resource_limits{namespace="agents", resource="cpu"}) by (pod)
        * 100
      threshold: "70"
  
  # Trigger 3: Memory Usage (via Prometheus)
  - type: prometheus
    metadata:
      serverAddress: http://prometheus-kube-prometheus-prometheus.monitoring:9090
      metricName: agent_memory_usage_percent
      query: |
        avg(container_memory_working_set_bytes{namespace="agents",container="agent"}) by (pod)
        / ignoring(pod)
        avg(kube_pod_container_resource_limits{namespace="agents", resource="memory"}) by (pod)
        * 100
      threshold: "80"
  
  # Trigger 4: Queue Depth (via RabbitMQ)
  - type: rabbitmq
    metadata:
      protocol: amqp
      queueName: agent.decisions
      mode: QueueLength
      value: "10"
    authenticationRef:
      name: keda-rabbitmq-auth
  
  # Trigger 5: Scheduled scaling (horario laboral)
  - type: cron
    metadata:
      timezone: America/Mexico_City
      start: "0 8 * * 1-5"    # Lunes a Viernes 8:00 AM
      end: "0 20 * * 1-5"     # Lunes a Viernes 8:00 PM
      desiredReplicas: "10"
  
  # Trigger 6: HTTP request rate
  - type: http
    metadata:
      host: agent-worker.agents.svc.cluster.local
      path: /api/decide
      port: "8000"
      targetPendingRequests: "100"
```

### 16.4 Queue-Based Scaling: RabbitMQ y Kafka (45 minutos)

#### 16.4.1 Agente Worker con RabbitMQ

```python
# src/queue/rabbitmq_worker.py
"""
Agente worker que procesa mensajes de RabbitMQ.
El número de workers es controlado por KEDA según la profundidad de la cola.
"""
import os
import json
import asyncio
import signal
from typing import Callable, Dict, Any, Optional

import aio_pika
from aio_pika import Message, DeliveryMode, ExchangeType, Queue
from aio_pika.abc import AbstractIncomingMessage

from src.metrics.advanced_metrics import metrics_collector


class RabbitMQWorkerAgent:
    """
    Agente worker que consume mensajes de RabbitMQ.
    Se escala automáticamente con KEDA según la profundidad de cola.
    """
    
    def __init__(
        self,
        agent_id: str,
        amqp_url: str = None,
        queue_name: str = "agent.decisions",
        prefetch_count: int = 10,
        process_fn: Optional[Callable] = None
    ):
        self.agent_id = agent_id or os.getenv('AGENT_ID', 'unknown')
        self.amqp_url = amqp_url or os.getenv(
            'RABBITMQ_URL',
            'amqp://guest:guest@rabbitmq.agents.svc.cluster.local:5672/'
        )
        self.queue_name = queue_name
        self.prefetch_count = prefetch_count
        self.process_fn = process_fn or self.default_process
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.queue: Optional[Queue] = None
        self.consumer_tag: Optional[str] = None
        self._running = False
    
    async def start(self):
        """Inicia el worker y comienza a consumir mensajes"""
        self._running = True
        
        # Conectar a RabbitMQ
        self.connection = await aio_pika.connect_robust(
            self.amqp_url,
            heartbeat=60,
            timeout=30
        )
        
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=self.prefetch_count)
        
        # Declarar cola (debe ser durable para que sobreviva a reinicios)
        self.queue = await self.channel.declare_queue(
            self.queue_name,
            durable=True,
            arguments={
                "x-queue-type": "quorum",  # Alta disponibilidad
                "x-max-length": 100000,
                "x-message-ttl": 86400000  # 24 horas
            }
        )
        
        # Iniciar consumo
        self.consumer_tag = await self.queue.consume(
            self._process_message,
            no_ack=False  # Requiere confirmación manual
        )
        
        print(f"[{self.agent_id}] Worker iniciado - Cola: {self.queue_name}")
        
        # Mantener vivo
        try:
            await asyncio.Future()  # Ejecuta hasta que se cancele
        except asyncio.CancelledError:
            await self.stop()
    
    async def _process_message(self, message: AbstractIncomingMessage):
        """Procesa un mensaje de la cola"""
        async with message.process(ignore_processed=True):
            try:
                # Decodificar mensaje
                body = json.loads(message.body.decode())
                
                # Registrar métrica de queue depth decreciente
                if metrics_collector:
                    remaining = await self.queue.declare(passive=True)
                    metrics_collector.update_queue_depth(
                        remaining.message_count
                    )
                
                # Procesar el mensaje
                result = await self.process_fn(body)
                
                # Confirmar procesamiento exitoso
                await message.ack()
                
                # Registrar métrica
                if metrics_collector:
                    metrics_collector.record_decision(
                        decision_type=body.get('type', 'unknown'),
                        duration=result.get('duration', 0),
                        status="success"
                    )
                
            except Exception as e:
                print(f"[{self.agent_id}] Error procesando mensaje: {e}")
                
                # Rechazar mensaje (puede ir a DLQ)
                await message.reject(requeue=False)
                
                if metrics_collector:
                    metrics_collector.record_decision(
                        decision_type="error",
                        duration=0,
                        status="error"
                    )
    
    async def default_process(self, message: Dict) -> Dict[str, Any]:
        """Procesador por defecto (sobrescribir en producción)"""
        import time
        start = time.time()
        
        # Simular procesamiento
        processing_time = min(message.get('priority', 1) * 0.5, 10.0)
        await asyncio.sleep(processing_time)
        
        return {
            "status": "processed",
            "duration": time.time() - start,
            "message_id": message.get('id', 'unknown')
        }
    
    async def stop(self):
        """Detiene el worker gracefulmente"""
        self._running = False
        
        if self.consumer_tag and self.channel:
            await self.queue.cancel(self.consumer_tag)
        
        if self.connection:
            await self.connection.close()
        
        print(f"[{self.agent_id}] Worker detenido")


# ─── Uso del worker ──────────────────────────────────────────────────

async def main():
    """Punto de entrada del worker"""
    agent_id = os.getenv('AGENT_ID', f'worker-{os.getpid()}')
    
    worker = RabbitMQWorkerAgent(
        agent_id=agent_id,
        amqp_url=os.getenv('RABBITMQ_URL'),
        queue_name=os.getenv('QUEUE_NAME', 'agent.decisions'),
        prefetch_count=int(os.getenv('PREFETCH_COUNT', '10'))
    )
    
    # Manejar señal de terminación
    stop_event = asyncio.Event()
    
    def _signal_handler():
        stop_event.set()
    
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _signal_handler)
    
    # Iniciar worker
    worker_task = asyncio.create_task(worker.start())
    
    # Esperar señal de stop
    await stop_event.wait()
    worker_task.cancel()
    
    try:
        await worker_task
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    asyncio.run(main())
```

#### 16.4.2 Agente Consumer de Kafka

```python
# src/queue/kafka_consumer.py
"""
Agente consumer de Kafka.
KEDA escala el número de consumers según el lag de Kafka.
"""
import os
import json
import asyncio
import signal
from typing import Dict, Any, Optional, Callable

from aiokafka import AIOKafkaConsumer, ConsumerRecord
from aiokafka.errors import CommitFailedError

from src.metrics.advanced_metrics import metrics_collector


class KafkaConsumerAgent:
    """
    Agente que consume eventos de Kafka.
    KEDA monitorea el consumer lag y escala los pods según sea necesario.
    """
    
    def __init__(
        self,
        agent_id: str,
        bootstrap_servers: str = None,
        topic: str = "agent-events",
        group_id: str = "agent-workers",
        process_fn: Optional[Callable] = None
    ):
        self.agent_id = agent_id or os.getenv('AGENT_ID', 'unknown')
        self.bootstrap_servers = bootstrap_servers or os.getenv(
            'KAFKA_BOOTSTRAP_SERVERS',
            'kafka-cluster.kafka.svc.cluster.local:9092'
        )
        self.topic = topic
        self.group_id = group_id
        self.process_fn = process_fn or self.default_process
        self.consumer: Optional[AIOKafkaConsumer] = None
        self._running = False
    
    async def start(self):
        """Inicia el consumer de Kafka"""
        self._running = True
        
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset='latest',
            enable_auto_commit=False,
            max_poll_records=100,
            max_poll_interval_ms=300000,
            session_timeout_ms=60000,
            heartbeat_interval_ms=20000,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None
        )
        
        await self.consumer.start()
        
        print(f"[{self.agent_id}] Consumer Kafka iniciado - "
              f"Topic: {self.topic}, Group: {self.group_id}")
        
        try:
            async for message in self.consumer:
                await self._process_message(message)
        except asyncio.CancelledError:
            pass
        finally:
            await self.stop()
    
    async def _process_message(self, message: ConsumerRecord):
        """Procesa un mensaje de Kafka"""
        try:
            result = await self.process_fn(message.value)
            
            # Commit manual después de procesar
            await self.consumer.commit()
            
            # Métricas
            if metrics_collector:
                metrics_collector.record_decision(
                    decision_type=message.value.get('type', 'kafka-event'),
                    duration=result.get('duration', 0),
                    status="success"
                )
            
        except Exception as e:
            print(f"[{self.agent_id}] Error: {e}")
            
            if metrics_collector:
                metrics_collector.record_decision(
                    decision_type="kafka-error",
                    duration=0,
                    status="error"
                )
    
    async def default_process(self, message: Dict) -> Dict[str, Any]:
        """Procesador por defecto"""
        import time
        start = time.time()
        
        await asyncio.sleep(0.5)  # Simular procesamiento
        
        return {
            "status": "processed",
            "duration": time.time() - start,
            "partition": message.get('partition', 'unknown')
        }
    
    async def stop(self):
        """Detiene el consumer gracefulmente"""
        self._running = False
        
        if self.consumer:
            await self.consumer.stop()
        
        print(f"[{self.agent_id}] Consumer detenido")
```

### 16.5 Scaling Predictivo de Agentes (40 minutos)

#### 16.5.1 Modelo Predictivo con Prometheus y ML

```python
# src/scaling/predictive_scaler.py
"""
Sistema de scaling predictivo para agentes.
Utiliza datos históricos de Prometheus para predecir la demanda futura.
"""
import os
import time
import json
import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import deque

import httpx
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

logger = logging.getLogger(__name__)


class PredictiveScaler:
    """
    Scaler predictivo que anticipa la demanda de agentes.
    Usa regresión polinomial sobre datos históricos de Prometheus.
    """
    
    def __init__(
        self,
        prometheus_url: str = None,
        prediction_window: int = 300,  # 5 minutos adelante
        history_window: int = 3600,    # 1 hora de historia
        min_replicas: int = 2,
        max_replicas: int = 30
    ):
        self.prometheus_url = prometheus_url or os.getenv(
            'PROMETHEUS_URL',
            'http://prometheus-kube-prometheus-prometheus.monitoring:9090'
        )
        self.prediction_window = prediction_window
        self.history_window = history_window
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        
        self.history: Dict[str, deque] = {}
        self.client = httpx.AsyncClient(timeout=30.0)
        self.model_cache = {}
    
    async def query_prometheus(self, query: str) -> List[Dict]:
        """Ejecuta query contra Prometheus API"""
        response = await self.client.get(
            f"{self.prometheus_url}/api/v1/query",
            params={"query": query}
        )
        response.raise_for_status()
        return response.json()['data']['result']
    
    async def query_range_prometheus(
        self, query: str, start: datetime, end: datetime, step: int = 15
    ) -> List[Dict]:
        """Ejecuta query de rango contra Prometheus"""
        response = await self.client.get(
            f"{self.prometheus_url}/api/v1/query_range",
            params={
                "query": query,
                "start": start.timestamp(),
                "end": end.timestamp(),
                "step": str(step)
            }
        )
        response.raise_for_status()
        return response.json()['data']['result']
    
    async def get_historical_metrics(
        self, metric_name: str, namespace: str = "agents"
    ) -> np.ndarray:
        """Obtiene datos históricos de una métrica"""
        query = f'sum({metric_name}{{namespace="{namespace}"}})'
        
        end = datetime.now()
        start = end - timedelta(seconds=self.history_window)
        
        results = await self.query_range_prometheus(query, start, end)
        
        if not results:
            return np.array([])
        
        # Extraer valores [timestamp, value]
        values = np.array(results[0]['values'], dtype=float)
        return values[:, 1]  # Solo valores
    
    def predict_demand(self, history: np.ndarray, steps_ahead: int = 20) -> np.ndarray:
        """
        Predice la demanda futura usando regresión polinomial.
        
        Args:
            history: Array de valores históricos
            steps_ahead: Número de pasos a predecir (cada paso = 15s)
        
        Returns:
            Array de valores predichos
        """
        if len(history) < 50:
            return np.array([])
        
        # Preparar datos
        X = np.arange(len(history)).reshape(-1, 1)
        y = history
        
        # Regresión polinomial (grado 2 para capturar tendencias suaves)
        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_poly = poly.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_poly, y)
        
        # Predecir siguientes pasos
        future_X = np.arange(len(history), len(history) + steps_ahead).reshape(-1, 1)
        future_X_poly = poly.transform(future_X)
        predictions = model.predict(future_X_poly)
        
        # Suavizar predicciones (moving average)
        window = 3
        predictions = np.convolve(predictions, np.ones(window)/window, mode='same')
        
        return predictions
    
    async def calculate_required_replicas(
        self, deployment_name: str, namespace: str
    ) -> Tuple[int, float]:
        """
        Calcula el número de réplicas necesarias basado en predicciones.
        
        Returns:
            Tuple (replicas_recomendadas, confianza)
        """
        # Obtener métricas históricas
        decisions_history = await self.get_historical_metrics(
            'agent_decisions_total', namespace
        )
        
        if len(decisions_history) == 0:
            return self.min_replicas, 0.0
        
        # Predecir demanda futura
        predictions = self.predict_demand(decisions_history)
        
        if len(predictions) == 0:
            return self.min_replicas, 0.0
        
        # Calcular demanda pico predicha
        peak_predicted = np.max(predictions)
        current = np.mean(decisions_history[-5:]) if len(decisions_history) >= 5 else 0
        
        # Calcular réplicas necesarias
        # Asumiendo que cada pod maneja 50 decisiones/segundo
        decisions_per_pod = 50.0
        required = max(
            self.min_replicas,
            min(
                self.max_replicas,
                int(np.ceil(peak_predicted / decisions_per_pod))
            )
        )
        
        # Calcular confianza basada en varianza de la predicción
        variance = np.var(decisions_history[-100:]) if len(decisions_history) >= 100 else 1.0
        confidence = max(0.0, min(1.0, 1.0 / (1.0 + variance / 100.0)))
        
        return required, confidence
    
    async def predictive_scale_loop(self, namespace: str = "agents"):
        """Loop principal de scaling predictivo"""
        while True:
            try:
                required, confidence = await self.calculate_required_replicas(
                    "agent-worker", namespace
                )
                
                if confidence > 0.7 and required > 0:
                    logger.info(
                        f"Predicción: {required} réplicas "
                        f"(confianza: {confidence:.2f})"
                    )
                    
                    # Escalar deployment
                    # Nota: En producción, usar API de Kubernetes
                    await self._scale_deployment("agent-worker", namespace, required)
                
            except Exception as e:
                logger.error(f"Error en scaling predictivo: {e}")
            
            # Ejecutar cada 2 minutos
            await asyncio.sleep(120)
    
    async def _scale_deployment(self, name: str, namespace: str, replicas: int):
        """Escala un deployment al número especificado de réplicas"""
        # Implementar usando kubernetes_asyncio client
        pass
```

#### 16.5.2 Integración con Kubernetes

```yaml
# 16-scaling/predictive-autoscaler.yaml
# Deployment del scaler predictivo como un servicio separado
apiVersion: apps/v1
kind: Deployment
metadata:
  name: predictive-scaler
  namespace: agents
  labels:
    app: predictive-scaler
spec:
  replicas: 1
  selector:
    matchLabels:
      app: predictive-scaler
  template:
    metadata:
      labels:
        app: predictive-scaler
    spec:
      serviceAccountName: scaler-service-account
      containers:
      - name: scaler
        image: predictive-scaler:latest
        env:
        - name: PROMETHEUS_URL
          value: "http://prometheus-kube-prometheus-prometheus.monitoring:9090"
        - name: PREDICTION_WINDOW
          value: "300"
        - name: MIN_REPLICAS
          value: "2"
        - name: MAX_REPLICAS
          value: "30"
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: scaler-service-account
  namespace: agents
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: scaler-role
rules:
- apiGroups: ["apps"]
  resources: ["deployments/scale"]
  verbs: ["get", "update", "patch"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: scaler-role-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: scaler-role
subjects:
- kind: ServiceAccount
  name: scaler-service-account
  namespace: agents
```

### 16.6 VPA (Vertical Pod Autoscaler) para Agentes (20 minutos)

```bash
# Instalar VPA
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh

# Verificar instalación
kubectl get pods -n kube-system | grep vpa
```

```yaml
# 16-scaling/agent-vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: agent-vpa
  namespace: agents
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-worker
  updatePolicy:
    updateMode: "Auto"  # Auto | Initial | Off
  resourcePolicy:
    containerPolicies:
    - containerName: "agent"
      minAllowed:
        cpu: "100m"
        memory: "256Mi"
      maxAllowed:
        cpu: "4000m"
        memory: "8Gi"
      controlledResources: ["cpu", "memory"]
      controlledValues: RequestsAndLimits
```

### 16.7 Cluster Autoscaler (20 minutos)

```yaml
# 16-scaling/cluster-autoscaler.yaml
# Ejemplo para AWS EKS
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
    spec:
      serviceAccountName: cluster-autoscaler
      containers:
      - image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.28.1
        name: cluster-autoscaler
        command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled
```

### 16.8 Estrategias y Mejores Prácticas

```mermaid
graph TB
    subgraph "Scaling Strategy Matrix"
        subgraph "Low Load"
            L1["HPA+CPU<br/>2-5 replicas"]
            L2["KEDA+Queue<br/>1-3 replicas"]
        end
        
        subgraph "Medium Load"
            M1["HPA+CPU+Custom<br/>5-15 replicas"]
            M2["KEDA+Prometheus<br/>3-10 replicas"]
        end
        
        subgraph "High Load"
            H1["Multi-metric HPA<br/>15-30 replicas"]
            H2["KEDA+Multi-trigger<br/>10-30 replicas"]
            H3["Predictive+Reactive<br/>Pre-scale + react"]
        end
        
        subgraph "Extreme Load"
            E1["All scalers combined<br/>30-100 replicas"]
            E2["Cluster Autoscaler<br/>+ nodes"]
        end
    end
    
    L1 --> M1
    L2 --> M2
    M1 --> H1
    M2 --> H2
    H1 --> H3
    H2 --> H3
    H3 --> E1
    E1 --> E2
    
    style H3 fill:#e91e63
    style E1 fill:#9c27b0
    style E2 fill:#9c27b0
```

**Mejores Prácticas:**

1. **Stabilization Windows**: Usar ventanas de estabilización para evitar thrashing (escalado/oscilación). Para scale-up: 0s (reaccionar rápido a picos). Para scale-down: 300s+ (evitar reducir muy rápido)

2. **Cooldown Periods**: En KEDA, el `cooldownPeriod` determina cuánto tiempo esperar después del último evento antes de escalar down. Ajustar según la naturaleza de la carga: 60-300s

3. **Múltiples Métricas**: Combinar métricas de resource (CPU/memoria) con métricas de negocio (decisiones/s, cola). El HPA usa el valor más alto

4. **Predictivo + Reactivo**: Combinar escalado predictivo (preparar recursos antes del pico) con reactivo (responder a cambios inesperados)

5. **0 Replicas**: Usar `idReplicaCount: 0` en KEDA para escalar a 0 cuando no hay trabajo. Ahorra recursos significativamente

6. **Canary Scaling**: Escalar gradualmente. No escalar de 2 a 30 pods en un solo paso. Usar políticas de `scaleUp` conservadoras

7. **Monitoreo Constante**: Las métricas de decisión de scaling deben monitorearse para ajustar thresholds continuamente

## Ejercicios Prácticos

### Ejercicio 1: Implementar HPA Multi-Métrica (45 minutos)

**Objetivo:** Configurar HPA con métricas de CPU y personalizadas.

**Solución:**

```bash
# 1. Desplegar agente con métricas
kubectl apply -f k8s/agent-deployment.yaml
kubectl apply -f k8s/agent-service.yaml

# 2. Verificar que las métricas están expuestas
kubectl port-forward -n agents deploy/agent-worker 8000:8000 &
curl http://localhost:8000/metrics | head -20

# 3. Configurar Prometheus Adapter
helm upgrade --install prometheus-adapter prometheus-community/prometheus-adapter \
  --namespace monitoring \
  -f adapter-values.yaml

# 4. Aplicar HPA
kubectl apply -f 16-scaling/agent-hpa-advanced.yaml

# 5. Verificar HPA
kubectl get hpa agent-hpa-advanced -n agents -o wide

# 6. Generar carga para probar escalado
kubectl run -it --rm load-generator --image=busybox --restart=Never -- /bin/sh -c '
  while true; do
    wget -qO- http://agent-worker.agents.svc.cluster.local/api/decide
    sleep 0.1
  done
' &

# 7. Ver escalado en acción
watch -n 5 'kubectl get hpa agent-hpa-advanced -n agents && echo "---" && kubectl get pods -n agents -l app=agent-worker'
```

**Explicación:**
1. El agente expone métricas en `/metrics` en formato Prometheus
2. Prometheus recopila las métricas cada 15s
3. Prometheus Adapter las expone a la API de Kubernetes como custom metrics
4. HPA consulta las métricas cada 15s y calcula el número deseado de réplicas
5. La política de scale-up es agresiva (duplicar pods en 15s), scale-down es conservadora

### Ejercicio 2: Configurar KEDA con RabbitMQ (45 minutos)

**Objetivo:** Implementar scaling event-driven con KEDA y RabbitMQ.

**Solución:**

```bash
# 1. Instalar KEDA
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda --namespace keda --create-namespace

# 2. Desplegar RabbitMQ
kubectl create namespace rabbitmq
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install rabbitmq bitnami/rabbitmq \
  --namespace rabbitmq \
  --set auth.username=agent \
  --set auth.password=agent-pass \
  --set auth.erlangCookie=secret-cookie

# 3. Obtener conexión
RABBITMQ_URL="amqp://agent:agent-pass@rabbitmq.rabbitmq.svc.cluster.local:5672/"

# 4. Crear cola
kubectl run -it --rm rabbitmqadmin --image=perfiz/rabbitmqadmin -- \
  --host=rabbitmq.rabbitmq.svc.cluster.local \
  --username=agent --password=agent-pass \
  declare queue name=agent.decisions durable=true

# 5. Aplicar ScaledObject
kubectl create secret generic rabbitmq-secrets -n agents \
  --from-literal=connection-string="$RABBITMQ_URL"

kubectl apply -f 16-scaling/keda-rabbitmq.yaml

# 6. Verificar ScaledObject
kubectl get scaledobject -n agents
kubectl describe scaledobject agent-rabbitmq-scaler -n agents

# 7. Probar: publicar mensajes para escalar
kubectl run -it --rm publisher --image=perfiz/rabbitmqadmin -- \
  --host=rabbitmq.rabbitmq.svc.cluster.local \
  --username=agent --password=agent-pass \
  publish exchange=amq.default routing_key=agent.decisions \
  payload="{\"id\":\"1\",\"type\":\"decision\",\"priority\":5}"

# 8. Publicar en lote para forzar escalado
for i in $(seq 1 100); do
  kubectl run -it --rm publisher-$i --image=perfiz/rabbitmqadmin --restart=Never \
    --host=rabbitmq.rabbitmq.svc.cluster.local \
    --username=agent --password=agent-pass \
    publish exchange=amq.default routing_key=agent.decisions \
    payload="{\"id\":\"$i\",\"type\":\"batch\",\"priority\":1}" 2>/dev/null &
done

# 9. Ver escalado en acción
watch -n 5 'echo "=== ScaledObject ===" && kubectl get scaledobject -n agents && echo "=== Pods ===" && kubectl get pods -n agents -l app=agent-worker'
```

**Explicación del ScaledObject:**
```yaml
# Análisis de configuración:
# - pollingInterval: 10s (KEDA consulta RabbitMQ cada 10s)
# - cooldownPeriod: 120s (espera 2 min antes de escalar down)
# - minReplicaCount: 1 (mínimo 1 pod siempre)
# - maxReplicaCount: 20 (máximo 20 pods)
# - idReplicaCount: 0 (puede escalar a 0 si no hay mensajes)
#
# Trigger rabbitmq:
# - mode: QueueLength (escala basado en longitud de cola)
# - value: "5" (escala UP si cola > 5 mensajes)
# - activationValue: "1" (escala desde 0 si hay al menos 1 mensaje)
```

### Ejercicio 3: Combinar Múltiples Estrategias de Scaling (60 minutos)

**Objetivo:** Implementar una estrategia híbrida que combine HPA, KEDA y scaling predictivo.

**Solución:**

```bash
# 1. Configurar Prometheus como fuente central de métricas
echo "Prometheus ya configurado en el ejercicio 1"

# 2. Aplicar ScaledObject multi-trigger
kubectl apply -f 16-scaling/keda-multi-trigger.yaml

# 3. Ver los triggers activos
kubectl describe scaledobject agent-multi-trigger -n agents

# 4. Ver que KEDA creó un HPA automáticamente
kubectl get hpa -n agents -l 'app.kubernetes.io/instance=agent-multi-trigger'

# 5. Configurar cron para escalado en horas pico
cat <<EOF | kubectl apply -f -
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: agent-cron-scaler
  namespace: agents
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-worker
  minReplicaCount: 2
  maxReplicaCount: 20
  triggers:
  - type: cron
    metadata:
      timezone: America/Mexico_City
      start: "0 9 * * 1-5"
      end: "0 18 * * 1-5"
      desiredReplicas: "15"
  - type: cron
    metadata:
      timezone: America/Mexico_City
      start: "0 18 * * 1-5"
      end: "0 22 * * 1-5"
      desiredReplicas: "8"
EOF

# 6. Desplegar scaler predictivo
kubectl apply -f 16-scaling/predictive-autoscaler.yaml

# 7. Ver el estado completo de auto-scaling
echo "=== HPA ==="
kubectl get hpa -n agents

echo "=== ScaledObjects ==="
kubectl get scaledobject -n agents

echo "=== VPA ==="
kubectl get vpa -n agents

echo "=== Current Pods ==="
kubectl get pods -n agents -l app=agent-worker

echo "=== Resource Usage ==="
kubectl top pods -n agents -l app=agent-worker
```

**Estrategia Híbrida Explicada:**

```
┌──────────────────────────────────────────────────────────────────┐
│                   ESTRATEGIA DE SCALING HÍBRIDA                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Mañana (9:00 - 18:00): Hora pico laboral                           │
│  ├── Predictivo: Pre-escala a 15 pods a las 8:30                   │
│  ├── KEDA Prometheus: Escala según decisiones/segundo               │
│  └── HPA CPU/Memoria: Backstop para recursos físicos               │
│                                                                      │
│  Tarde (18:00 - 22:00): Media carga                                 │
│  ├── Cron: Mantiene 8 pods base                                     │
│  └── KEDA RabbitMQ: Escala según cola de mensajes                   │
│                                                                      │
│  Noche (22:00 - 9:00): Carga baja                                   │
│  └── KEDA con idReplicaCount=0: Escala a 0 si no hay trabajo       │
│                                                                      │
└──────────────────────────────────────────────────────────────────┘
```

## Tecnologías Específicas

- **KEDA**: v2.14+ (event-driven autoscaling)
- **Kubernetes HPA**: Autoscaling/v2
- **Prometheus**: v2.50+ (métricas)
- **Prometheus Adapter**: v0.12+ (custom metrics API)
- **Metrics Server**: v0.7+ (resource metrics)
- **RabbitMQ**: v3.13+ (message queuing)
- **Apache Kafka**: v3.6+ (event streaming)
- **VPA**: v1.0+ (vertical pod autoscaling)
- **Cluster Autoscaler**: v1.28+ (node scaling)
- **scikit-learn**: v1.4+ (predictive models)

## Actividades de Laboratorio

### Laboratorio 1: Configuración Completa de Auto-scaling (90 minutos)

**Objetivo:** Implementar un sistema completo de auto-scaling multi-estrategia.

1. **Preparación del cluster:**
   - Minikube con 8GB RAM, 4 CPUs
   - Instalar Prometheus Stack, KEDA, Metrics Server
   - Desplegar RabbitMQ y agente de ejemplo

2. **Configurar HPA multi-métrica:**
   - CPU target: 70%
   - Custom metric: decisions_per_second target: 50
   - Políticas de scale-up agresivas, scale-down conservadoras

3. **Configurar KEDA con múltiples triggers:**
   - RabbitMQ queue depth trigger
   - Prometheus custom metric trigger
   - Cron trigger para horas laborales

4. **Desplegar scaler predictivo:**
   - Basado en datos históricos de Prometheus
   - Regresión polinomial para predicción
   - Pre-escalado 5 minutos antes del pico

5. **Prueba de estrés:**
   - Generar carga creciente (100 → 1000 decisiones/minuto)
   - Observar la respuesta de escalado en tiempo real
   - Verificar que el sistema no thrash (oscile)

### Laboratorio 2: Optimización de Costos con Scaling a Cero (90 minutos)

**Objetivo:** Implementar escalado a 0 réplicas para ahorrar recursos en horas de baja demanda.

1. **Configurar KEDA con `idReplicaCount: 0`:**
   ```yaml
   spec:
     minReplicaCount: 0
     maxReplicaCount: 20
     idReplicaCount: 0
   ```

2. **Configurar warm-up:** Los pods deben iniciar rápido (< 30s) para que el escalado desde 0 sea efectivo:
   - Usar imágenes pequeñas (Python slim)
   - Pre-cargar modelos en shared volume
   - Health checks optimizados

3. **Verificar ahorro de recursos:**
   ```bash
   # Medir antes del scaling a 0
   kubectl top pods -n agents
   
   # Esperar a que escale a 0
   kubectl get pods -n agents -l app=agent-worker -w
   
   # Medir después
   kubectl top pods -n agents  # No debe mostrar pods
   ```

4. **Probar cold start:**
   ```bash
   # Publicar mensaje en cola vacía
   kubectl run publisher --image=perfiz/rabbitmqadmin --rm -it -- \
     --host=rabbitmq.rabbitmq.svc.cluster.local \
     --username=agent --password=agent-pass \
     publish exchange=amq.default routing_key=agent.decisions \
     payload="{\"id\":\"cold-start-test\"}"
   
   # Medir tiempo hasta que el pod esté listo
   time kubectl get pods -n agents -l app=agent-worker -w | head -5
   ```

## Resumen de Puntos Clave

1. **Auto-scaling multi-estrategia**: Combinar HPA (métricas de resource y personalizadas) con KEDA (event-driven) y escalado predictivo para cubrir todos los escenarios de carga.

2. **KEDA extiende HPA**: KEDA no reemplaza a HPA, lo extiende. Crea ScaledObjects que generan HPA automáticos. Los triggers pueden ser de RabbitMQ, Kafka, Prometheus, HTTP, cron y más.

3. **Métricas de negocio**: Las métricas más relevantes para escalar agentes son las de negocio: decisiones/segundo, profundidad de cola, latency P95. Las métricas de resource (CPU/memoria) son secundarias.

4. **Scaling predictivo**: Usar modelos de ML sobre datos históricos de Prometheus para anticipar picos de demanda. La regresión polinomial simple puede predecir tendencias a corto plazo efectivamente.

5. **Políticas de escalado**: Configurar stabilizationWindows y policies para evitar thrashing. Scale-up rápido, scale-down lento. Usar selectPolicy (Max para up, Min para down).

6. **Escalado a 0**: KEDA permite escalar a 0 réplicas cuando no hay trabajo. Ideal para entornos de desarrollo y horas de baja demanda. Requiere startups rápidos (cold start < 30s).

7. **Vertical Pod Autoscaler**: VPA ajusta los recursos (CPU/memoria) de los pods existentes. Complementa a HPA que ajusta el número de pods. Usar VPA en modo "Initial" para recomendar recursos.

8. **Cluster Autoscaler**: Cuando HPA no puede escalar más porque no hay recursos en el cluster, Cluster Autoscaler añade nuevos nodos. Es el último nivel de escalado.

## Referencias Externas

1. **KEDA Documentation** - Kubernetes Event-Driven Autoscaling
   https://keda.sh/docs/

2. **KEDA Scalers** - Lista completa de triggers soportados
   https://keda.sh/docs/2.14/scalers/

3. **Kubernetes HPA** - Horizontal Pod Autoscaler
   https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/

4. **Kubernetes VPA** - Vertical Pod Autoscaler
   https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler

5. **Cluster Autoscaler** - Auto-scaling de nodos
   https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler

6. **Prometheus Adapter** - Custom Metrics API
   https://github.com/kubernetes-sigs/prometheus-adapter

7. **RabbitMQ Documentation** - Message queuing
   https://www.rabbitmq.com/documentation.html

8. **Kafka Documentation** - Event streaming
   https://kafka.apache.org/documentation/

9. **Prometheus Documentation** - Monitoring system
   https://prometheus.io/docs/

10. **KEDA: Scaling to Zero** - Guía de escalado a 0
    https://keda.sh/blog/how-to-scale-to-zero-with-keda/

11. **Predictive Autoscaling** - Patrones de escalado predictivo
    https://kubernetes.io/blog/2023/05/01/predictive-autoscaling/

12. **Auto-scaling Patterns** - Patrones de escalado en Kubernetes
    https://www.cncf.io/blog/2023/06/15/kubernetes-autoscaling-patterns/
