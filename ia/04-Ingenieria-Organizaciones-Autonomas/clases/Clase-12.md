# Clase 12: Monitoreo y Alerting para Agentes Industriales

## Duración
4 horas (240 minutos)

## Objetivos de Aprendizaje
- Implementar sistemas de monitoreo específicos para agentes industriales
- Configurar SLI/SLO/SLA apropiados para workloads agénticos
- Integrar herramientas de alerting (Grafana, PagerDuty, OpsGenie)
- Diseñar dashboards de observabilidad para arquitecturas agénticas
- Establecer procedimientos de respuesta a incidentes

## Contenidos Detallados

### 12.1 Fundamentos de Observabilidad en Sistemas Agénticos (60 minutos)

La observabilidad en sistemas agénticos industriales presenta desafíos únicos que requieren una aproximación diferente al monitoreo tradicional. A diferencia de las aplicaciones stateless, los agentes mantienen estado complejo, ejecutan flujos asíncronos de larga duración, y toman decisiones que requieren tracking específico.

#### 12.1.1 El Tridente de Observabilidad

El modelo de observabilidad para agentes industriales se construye sobre tres pilares fundamentales:

**Métricas (Metrics)**
Las métricas proporcionan información cuantitativa sobre el comportamiento del sistema. Para agentes industriales, las métricas críticas incluyen:

- Latencia de decisiones: Tiempo desde que el agente recibe una solicitud hasta que toma una acción
- Throughput de tokens: Velocidad de procesamiento de tokens por segundo
- Tasa de éxito de herramientas: Porcentaje de llamadas a herramientas externas que completan exitosamente
- Ciclos deReasoning: Número de iteraciones que el agente necesita para tomar una decisión

**Logs**
Los logs en sistemas agénticos deben capturar no solo eventos técnicos, sino también el razonamiento del agente. Esto requiere un formato estructurado que incluya:

- Trace ID único para cada interacción
- Estado del agente en el momento del log
- Herramientas ejecutadas con sus parámetros
- Resultados intermedios del reasoning
- Contexto de memoria utilizado

**Traces**
Los traces distribuitos son esenciales para entender el flujo de ejecución en sistemas agénticos. Cada trace debe representar una decisión del agente con:
- Parent span para llamadas a herramientas
- Span de reasoning con chain of thought
- Span de acceso a memoria
- Span de llamadas a sistemas externos

#### 12.1.2 SLI/SLA para Agentes Industriales

Los Service Level Indicators para agentes deben reflejar la naturaleza única de su operación:

```yaml
# Ejemplo de SLI para agente industrial
service_level_indicators:
  decision_latency:
    description: "Tiempo para tomar una decisión"
    sli: "percentile(99, decision_time_ms) < 5000"
    
  tool_execution_success:
    description: "Éxito en ejecución de herramientas"
    sli: "rate(tool_success_total / tool_calls_total) > 0.95"
    
  state_consistency:
    description: "Consistencia del estado del agente"
    sli: "rate(state_checks_passed / state_checks_total) > 0.999"
    
  reasoning_quality:
    description: "Calidad del razonamiento del agente"
    sli: "rate(acceptable_reasoning_total / reasoning_total) > 0.90"
    
  memory_latency:
    description: "Latencia de acceso a memoria"
    sli: "percentile(99, memory_access_ms) < 200"
```

Los Service Level Objectives traducen los SLI en metas operativas:

```yaml
service_level_objectives:
  availability:
    description: "Disponibilidad del servicio de agentes"
    slo: "99.9% (uptime_monthly)"
    error_budget: "43.8 minutos/mes"
    
  performance:
    description: "Rendimiento de decisiones"
    slo: "P99 < 5 segundos"
    error_budget: "3.6 horas/mes"
    
  quality:
    description: "Calidad de decisiones"
    slo: "95% de decisiones válidas"
    error_budget: "5% de decisiones pueden ser inválidas"
```

Los Service Level Agreements representan los compromisos contractuales:

```yaml
service_level_agreements:
  response_time:
   承诺: "Tiempo de respuesta inicial < 2 segundos"
    penalty: "10% de crédito por cada 5 segundos de delay"
    
  resolution_time:
   承诺: "Tiempo de resolución de incidentes críticos < 1 hora"
    penalty: "25% de crédito por cada hora adicional"
    
  accuracy:
   承诺: "Precisión de decisiones > 90%"
    penalty: "15% de crédito por cada punto porcentual bajo"
```

### 12.2 Arquitectura de Monitoreo para Agentes (75 minutos)

#### 12.2.1 Stack de Observabilidad

La arquitectura de monitoreo para agentes industriales se construye sobre un stack especializado:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA DE MONITOREO                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   AGENTES    │    │   AGENTES    │    │   AGENTES    │      │
│  │   (Inst. 1)  │    │   (Inst. 2)  │    │   (Inst. N)  │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │              │
│         └───────────────────┼───────────────────┘              │
│                             ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              AGENTE DE COLECCIÓN (Prometheus)           │   │
│  │  - scrapes métricas de cada instancia                    │   │
│  │  - Agrega métricas de aplicación                        │   │
│  │  - Expone endpoint /metrics                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                             │                                  │
│         ┌───────────────────┼───────────────────┐              │
│         ▼                   ▼                   ▼              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │   Grafana   │     │  Alertmanager│    │   Loki      │      │
│  │  (Dashboards)│     │  (Alertas)   │    │  (Logs)     │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                             │                                  │
│                             ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           PAGERDUTY / OPSGENIE                          │   │
│  │  - Escalamiento de incidentes                           │   │
│  │  - Notificaciones on-call                              │   │
│  │  - Integración con sistemas de ticketing               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 12.2.2 Implementación de Métricas con Prometheus

La instrumentación de agentes requiere métricas específicas que capturen el comportamiento único de cada componente:

```python
# metrics/agent_metrics.py
from prometheus_client import Counter, Histogram, Gauge, Info
import time

class AgentMetrics:
    """Métricas específicas para agentes industriales"""
    
    # Métricas de decisiones
    decisions_total = Counter(
        'agent_decisions_total',
        'Total de decisiones tomadas por el agente',
        ['agent_id', 'decision_type', 'outcome']
    )
    
    decision_latency = Histogram(
        'agent_decision_duration_seconds',
        'Tiempo de duración de decisiones',
        ['agent_id', 'decision_type'],
        buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0]
    )
    
    # Métricas de herramientas
    tool_calls_total = Counter(
        'agent_tool_calls_total',
        'Total de llamadas a herramientas',
        ['agent_id', 'tool_name', 'status']
    )
    
    tool_execution_time = Histogram(
        'agent_tool_execution_seconds',
        'Tiempo de ejecución de herramientas',
        ['agent_id', 'tool_name'],
        buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0]
    )
    
    # Métricas de memoria
    memory_operations = Counter(
        'agent_memory_operations_total',
        'Operaciones de memoria',
        ['agent_id', 'operation_type', 'status']
    )
    
    memory_access_time = Histogram(
        'agent_memory_access_seconds',
        'Tiempo de acceso a memoria',
        ['agent_id', 'memory_type'],
        buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
    )
    
    # Métricas de estado
    agent_state_size = Gauge(
        'agent_state_size_bytes',
        'Tamaño del estado del agente',
        ['agent_id', 'state_type']
    )
    
    active_agents = Gauge(
        'agent_active_instances',
        'Número de instancias activas de agentes',
        ['agent_type']
    )
    
    # Métricas de reasoning
    reasoning_cycles = Histogram(
        'agent_reasoning_cycles',
        'Ciclos de razonamiento por decisión',
        ['agent_id', 'decision_type'],
        buckets=[1, 2, 3, 5, 10, 20, 50]
    )
    
    reasoning_token_usage = Counter(
        'agent_reasoning_tokens_total',
        'Tokens utilizados en reasoning',
        ['agent_id', 'reasoning_type']
    )
    
    # Métricas de errores
    error_counts = Counter(
        'agent_errors_total',
        'Total de errores del agente',
        ['agent_id', 'error_type', 'severity']
    )


class MetricsMiddleware:
    """Middleware para capturar métricas automáticamente"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.metrics = AgentMetrics()
    
    def record_decision(self, decision_type: str, outcome: str, duration: float):
        self.metrics.decisions_total.labels(
            agent_id=self.agent_id,
            decision_type=decision_type,
            outcome=outcome
        ).inc()
        
        self.metrics.decision_latency.labels(
            agent_id=self.agent_id,
            decision_type=decision_type
        ).observe(duration)
    
    def record_tool_call(self, tool_name: str, status: str, duration: float):
        self.metrics.tool_calls_total.labels(
            agent_id=self.agent_id,
            tool_name=tool_name,
            status=status
        ).inc()
        
        if status == 'success':
            self.metrics.tool_execution_time.labels(
                agent_id=self.agent_id,
                tool_name=tool_name
            ).observe(duration)
    
    def record_memory_access(self, memory_type: str, operation: str, duration: float):
        self.metrics.memory_operations.labels(
            agent_id=self.agent_id,
            operation_type=operation,
            status='success'
        ).inc()
        
        self.metrics.memory_access_time.labels(
            agent_id=self.agent_id,
            memory_type=memory_type
        ).observe(duration)
```

#### 12.2.3 Configuración de Prometheus para Agentes

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

rule_files:
  - /etc/prometheus/rules/*.yml

scrape_configs:
  - job_name: 'agent-service'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: agent-service
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: pod
    metric_relabel_configs:
      - source_labels: [agent_id]
        regex: '(.*)'
        target_label: agent_id
        replacement: '${1}'

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:9121']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'llm-provider'
    static_configs:
      - targets: ['llm-provider:8000']
```

```yaml
# prometheus/rules/agent_rules.yml
groups:
  - name: agent_decision_rules
    interval: 30s
    rules:
      - alert: HighDecisionLatency
        expr: |
          histogram_quantile(0.99, 
            rate(agent_decision_duration_seconds_bucket[5m])
          ) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Alta latencia de decisiones"
          description: "P99 latencia de decisiones es {{ $value }}s"
          
      - alert: DecisionFailureRate
        expr: |
          rate(agent_decisions_total{outcome="failure"}[5m]) 
          / rate(agent_decisions_total[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Alta tasa de fallos en decisiones"
          description: "Tasa de fallos es {{ $value | humanizePercentage }}"

  - name: agent_tool_rules
    interval: 30s
    rules:
      - alert: ToolExecutionFailures
        expr: |
          rate(agent_tool_calls_total{status="failure"}[5m]) 
          / rate(agent_tool_calls_total[5m]) > 0.05
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "Fallos en ejecución de herramientas"
          description: "Tasa de fallos en {{ $labels.tool_name }} es {{ $value }}"
          
      - alert: ToolExecutionTimeout
        expr: |
          histogram_quantile(0.95, 
            rate(agent_tool_execution_seconds_bucket[5m])
          ) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Timeouts en herramientas"
          description: "P95 tiempo de ejecución de {{ $labels.tool_name }} es {{ $value }}s"

  - name: agent_memory_rules
    interval: 30s
    rules:
      - alert: HighMemoryLatency
        expr: |
          histogram_quantile(0.99, 
            rate(agent_memory_access_seconds_bucket[5m])
          ) > 0.2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Alta latencia de memoria"
          description: "P99 latencia de acceso a {{ $labels.memory_type }} es {{ $value }}s"
          
      - alert: AgentStateSizeHigh
        expr: agent_state_size_bytes > 1000000000
        for: 10m
        labels:
          severity: info
        annotations:
          summary: "Tamaño de estado elevado"
          description: "Estado del agente {{ $labels.agent_id }} es {{ $value | humanize }}"

  - name: agent_reasoning_rules
    interval: 30s
    rules:
      - alert: HighReasoningCycles
        expr: |
          histogram_quantile(0.95, 
            rate(agent_reasoning_cycles_bucket[5m])
          ) > 20
        for: 10m
        labels:
          severity: info
        annotations:
          summary: "Alto número de ciclos de razonamiento"
          description: "P95 ciclos de razonamiento es {{ $value }}"
```

### 12.3 Dashboards de Observabilidad (45 minutos)

#### 12.3.1 Dashboard Principal de Agentes

```yaml
# grafana/dashboards/agent-overview.json
{
  "dashboard": {
    "title": "Agent Industrial Overview",
    "tags": ["agents", "industrial"],
    "timezone": "browser",
    "refresh": "30s",
    "panels": [
      {
        "title": "Decisiones por Minuto",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "rate(agent_decisions_total[1m])",
            "legendFormat": "{{agent_id}} - {{decision_type}}"
          }
        ]
      },
      {
        "title": "Latencia de Decisiones (P99)",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(agent_decision_duration_seconds_bucket[5m]))",
            "legendFormat": "P99 {{agent_id}}"
          },
          {
            "expr": "histogram_quantile(0.95, rate(agent_decision_duration_seconds_bucket[5m]))",
            "legendFormat": "P95 {{agent_id}}"
          }
        ]
      },
      {
        "title": "Tasa de Éxito de Herramientas",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
        "targets": [
          {
            "expr": "sum by (tool_name) (rate(agent_tool_calls_total{status='success'}[5m])) / sum by (tool_name) (rate(agent_tool_calls_total[5m]))",
            "legendFormat": "{{tool_name}}"
          }
        ]
      },
      {
        "title": "Agentes Activos",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 12, "y": 8},
        "targets": [
          {
            "expr": "agent_active_instances",
            "legendFormat": "{{agent_type}}"
          }
        ]
      },
      {
        "title": "Estado de Memoria",
        "type": "table",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16},
        "targets": [
          {
            "expr": "agent_state_size_bytes by (agent_id, state_type)",
            "format": "table"
          }
        ]
      },
      {
        "title": "Errores Recientes",
        "type": "table",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16},
        "targets": [
          {
            "expr": "topk(20, agent_errors_total)",
            "format": "table"
          }
        ]
      }
    ]
  }
}
```

#### 12.3.2 Dashboard de Reasoning

```yaml
# grafana/dashboards/agent-reasoning.json
{
  "dashboard": {
    "title": "Agent Reasoning Analysis",
    "tags": ["agents", "reasoning"],
    "panels": [
      {
        "title": "Distribución de Ciclos de Reasoning",
        "type": "heatmap",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "rate(agent_reasoning_cycles_bucket[5m])",
            "legendFormat": "{{le}}"
          }
        ]
      },
      {
        "title": "Token Usage por Tipo",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "rate(agent_reasoning_tokens_total[5m])",
            "legendFormat": "{{reasoning_type}}"
          }
        ]
      },
      {
        "title": "Calidad de Decisiones",
        "type": "gauge",
        "gridPos": {"h": 6, "w": 8, "x": 0, "y": 8},
        "targets": [
          {
            "expr": "sum(rate(agent_decisions_total{outcome='success'}[5m])) / sum(rate(agent_decisions_total[5m])) * 100"
          }
        ]
      },
      {
        "title": "Decisiones por Tipo",
        "type": "piechart",
        "gridPos": {"h": 6, "w": 8, "x": 8, "y": 8},
        "targets": [
          {
            "expr": "sum by (decision_type) (rate(agent_decisions_total[5m]))"
          }
        ]
      },
      {
        "title": "Latencia de Acceso a Memoria",
        "type": "graph",
        "gridPos": {"h": 8, "w": 8, "x": 16, "y": 8},
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(agent_memory_access_seconds_bucket[5m]))",
            "legendFormat": "P99 {{memory_type}}"
          }
        ]
      }
    ]
  }
}
```

### 12.4 Integración con Sistemas de Alerting (35 minutos)

#### 12.4.1 Configuración de Alertmanager

```yaml
# alertmanager/config.yml
global:
  resolve_timeout: 5m
  smtp_smarthost: 'smtp.company.com:587'
  smtp_from: 'alertmanager@company.com'
  smtp_auth_username: 'alerts'
  smtp_auth_password: '${SMTP_PASSWORD}'

route:
  group_by: ['alertname', 'agent_id']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'critical-team'
      continue: true
    - match:
        severity: warning
      receiver: 'ops-team'
    - match:
        agent_type: 'reasoning-intensive'
      receiver: 'ai-team'

receivers:
  - name: 'default'
    email_configs:
      - to: 'agent-alerts@company.com'
        send_resolved: true
    webhook_configs:
      - url: 'http://webhook-service:5000/alerts'
        send_resolved: true

  - name: 'critical-team'
    pagerduty_configs:
      - service_key: '${PAGERDUTY_CRITICAL_KEY}'
        severity: critical
        details:
          agent_id: '{{ .GroupLabels.agent_id }}'
          alertname: '{{ .GroupLabels.alertname }}'
    slack_configs:
      - channel: '#agent-critical'
        title: '🚨 Alerta Crítica de Agente'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'ops-team'
    email_configs:
      - to: 'ops-team@company.com'
    slack_configs:
      - channel: '#agent-ops'
        title: '⚠️ Alerta de Agente'

  - name: 'ai-team'
    webhook_configs:
      - url: 'http://ai-team-service:8000/webhooks/alerts'
        send_resolved: true

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'agent_id']
```

#### 12.4.2 Integración con PagerDuty

```python
# integrations/pagerduty.py
from pypd import EventV2
import os

class PagerDutyAlerter:
    """Integración con PagerDuty para escalamiento de incidentes"""
    
    def __init__(self, integration_key: str):
        self.integration_key = integration_key
    
    def trigger_incident(
        self,
        alert_name: str,
        severity: str,
        agent_id: str,
        description: str,
        custom_details: dict
    ):
        """Genera un incidente en PagerDuty"""
        
        event = EventV2(
            routing_key=self.integration_key,
            event_action='trigger',
            dedup_key=f"{alert_name}-{agent_id}",
            payload={
                'summary': f"{alert_name}: {agent_id}",
                'severity': severity,
                'source': agent_id,
                'custom_details': {
                    'agent_id': agent_id,
                    'alert_name': alert_name,
                    **custom_details
                }
            }
        )
        event.send()
    
    def resolve_incident(self, alert_name: str, agent_id: str):
        """Resuelve un incidente en PagerDuty"""
        
        event = EventV2(
            routing_key=self.integration_key,
            event_action='resolve',
            dedup_key=f"{alert_name}-{agent_id}"
        )
        event.send()


class AgentAlertHandler:
    """Manejador de alertas específico para agentes"""
    
    def __init__(self, pagerduty: PagerDutyAlerter):
        self.pagerduty = pagerduty
    
    def handle_decision_failure(self, agent_id: str, failure_count: int):
        """Maneja fallos consecutivos en decisiones"""
        
        if failure_count >= 5:
            self.pagerduty.trigger_incident(
                alert_name='AgentDecisionFailure',
                severity='critical',
                agent_id=agent_id,
                description=f'Agente {agent_id} ha fallado {failure_count} decisiones consecutivamente',
                custom_details={
                    'failure_count': failure_count,
                    'action': 'Agente puesto en modo degradado'
                }
            )
    
    def handle_tool_failure(self, agent_id: str, tool_name: str, error: str):
        """Maneja fallos en herramientas"""
        
        self.pagerduty.trigger_incident(
            alert_name='AgentToolFailure',
            severity='warning',
            agent_id=agent_id,
            description=f'Herramienta {tool_name} falló en agente {agent_id}',
            custom_details={
                'tool_name': tool_name,
                'error': error
            }
        )
    
    def handle_high_latency(self, agent_id: str, latency_ms: float):
        """Maneja latencia elevada"""
        
        if latency_ms > 10000:
            self.pagerduty.trigger_incident(
                alert_name='AgentHighLatency',
                severity='warning',
                agent_id=agent_id,
                description=f'Agente {agent_id} tiene latencia de {latency_ms}ms',
                custom_details={
                    'latency_ms': latency_ms,
                    'threshold_ms': 10000
                }
            )
```

#### 12.4.3 Integración con OpsGenie

```python
# integrations/opsgenie.py
from opsgenie_sdk import (
    ApiClient,
    Configuration,
    CreateAlertRequest,
    AlertApi,
    CloseAlertRequest
)
from typing import Optional

class OpsGenieAlerter:
    """Integración con OpsGenie para gestión de alertas"""
    
    def __init__(self, api_key: str):
        config = Configuration()
        config.api_key['api_key'] = api_key
        self.api_client = ApiClient(configuration=config)
        self.alert_api = AlertApi(api_client=self.api_client)
    
    def create_alert(
        self,
        message: str,
        description: str,
        priority: str,
        tags: list,
        responders: Optional[list] = None
    ) -> str:
        """Crea una alerta en OpsGenie"""
        
        create_alert_request = CreateAlertRequest(
            message=message,
            description=description,
            priority=priority,
            tags=tags,
            responders=responders or []
        )
        
        response = self.alert_api.create_alert(create_alert_request)
        return response.id
    
    def close_alert(self, alert_id: str, note: str = "Resolved"):
        """Cierra una alerta en OpsGenie"""
        
        close_alert_request = CloseAlertRequest(note=note)
        self.alert_api.close_alert(alert_id, close_alert_request)


class AgentOpsGenieHandler:
    """Manejador de alertas para OpsGenie específico para agentes"""
    
    PRIORITY_MAP = {
        'critical': 'P1',
        'high': 'P2',
        'medium': 'P3',
        'low': 'P4'
    }
    
    def __init__(self, opsgenie: OpsGenieAlerter):
        self.opsgenie = opsgenie
    
    def handle_agent_down(self, agent_id: str, reason: str):
        """Alerta cuando un agente no está respondiendo"""
        
        alert_id = self.opsgenie.create_alert(
            message=f"Agent {agent_id} is down",
            description=f"Agent {agent_id} ha dejado de responder. Razón: {reason}",
            priority=self.PRIORITY_MAP['critical'],
            tags=['agent-down', agent_id],
            responders=[
                {'name': 'ai-oncall', 'type': 'team'}
            ]
        )
        return alert_id
    
    def handle_state_corruption(self, agent_id: str, state_type: str):
        """Alerta cuando se detecta corrupción de estado"""
        
        alert_id = self.opsgenie.create_alert(
            message=f"Agent state corruption detected in {agent_id}",
            description=f"Se detectó corrupción en el estado {state_type} del agente {agent_id}",
            priority=self.PRIORITY_MAP['critical'],
            tags=['state-corruption', agent_id, state_type],
            responders=[
                {'name': 'data-oncall', 'type': 'team'}
            ]
        )
        return alert_id
    
    def handle_security_violation(self, agent_id: str, violation_type: str):
        """Alerta cuando se detecta una violación de seguridad"""
        
        alert_id = self.opsgenie.create_alert(
            message=f"Security violation by agent {agent_id}",
            description=f"El agente {agent_id} realizó una acción no autorizada: {violation_type}",
            priority=self.PRIORITY_MAP['critical'],
            tags=['security', agent_id, violation_type],
            responders=[
                {'name': 'security-oncall', 'type': 'team'},
                {'name': 'ai-oncall', 'type': 'team'}
            ]
        )
        return alert_id
```

### 12.5 Prácticas de Respuesta a Incidentes (25 minutos)

#### 12.5.1 Runbook para Incidentes de Agentes

```markdown
# Runbook: Incidentes de Agentes Industriales

## Alerta: Agente No Responde

### Detección
- Alerta: `agent_not_responding`
- Métrica: `agent_active_instances` = 0 por más de 2 minutos

### Impacto
- Los procesos automatizados se detienen
- Solicitudes de usuarios quedan sin atender

### Pasos de Respuesta

1. **Verificar estado del pod**
   ```bash
   kubectl get pods -l app=agent-service
   kubectl describe pod <agent-pod>
   ```

2. **Revisar logs**
   ```bash
   kubectl logs <agent-pod> --previous
   ```

3. **Verificar memoria y CPU**
   ```bash
   kubectl top pod <agent-pod>
   ```

4. **Si hay OOMKilled:**
   - Aumentar límite de memoria
   - Revisar fugas de memoria en código
   
5. **Si hay CrashLoopBackOff:**
   - Revisar configuración
   - Verificar conectividad a Redis/PostgreSQL

6. **Si hay Deadlock:**
   - Revisar traces en Jaeger
   - Identificar bloqueos

7. **Recuperación:**
   - `kubectl rollout restart deployment/agent-service`

### Prevención
- Implementar liveness/readiness probes
- Configurar límites de recursos apropiados
- Monitorear uso de memoria

---

## Alerta: Alta Tasa de Fallos en Decisiones

### Detección
- Alerta: `DecisionFailureRate > 10%`
- Métrica: `rate(agent_decisions_total{outcome="failure"}) > 0.1`

### Impacto
- Decisions incorrectas o incompletas
- Potencial impacto en procesos de negocio

### Pasos de Respuesta

1. **Identificar tipo de decisión fallida**
   ```sql
   SELECT decision_type, COUNT(*) as failures
   FROM agent_decisions
   WHERE status = 'failure'
   AND timestamp > NOW() - 1 hour
   GROUP BY decision_type;
   ```

2. **Revisar errores específicos**
   ```python
   # Buscar errores en logs
   logs.query('agent_id="X" AND level="error" AND timestamp>now-1h')
   ```

3. **Verificar modelo LLM**
   - Revisar latencia del proveedor LLM
   - Verificar cuota disponible
   - Revisar errores de rate limiting

4. **Verificar herramientas**
   - Probar cada herramienta manualmente
   - Verificar conectividad a sistemas externos

5. **Si el modelo tiene problemas:**
   - Cambiar a modelo alternativo
   - Aumentar timeout
   - Revisar prompts

6. **Si herramientas fallan:**
   - Notificar a equipo de integración
   - Implementar fallback

### Prevención
- Implementar circuit breaker
- Agregar reintentos con backoff
- Mantener modelos alternativos disponibles
```

## Ejercicios Prácticos

### Ejercicio 1: Implementar Métricas de Agente (45 minutos)

**Objetivo:** Implementar un sistema completo de métricas para un agente industrial.

**Requisitos:**
1. Crear módulo de métricas con Prometheus client
2. Implementar métricas para decisiones, herramientas, memoria y reasoning
3. Configurar exportador de métricas en endpoint /metrics
4. Crear reglas de alerting en Prometheus

**Solución:**

```python
# metrics/agent_metrics_complete.py
from prometheus_client import (
    Counter, Histogram, Gauge, CollectorRegistry,
    generate_latest, CONTENT_TYPE_LATEST
)
from typing import Optional
import time
import uuid

class CompleteAgentMetrics:
    """Sistema completo de métricas para agentes industriales"""
    
    def __init__(self, agent_id: str, registry: Optional[CollectorRegistry] = None):
        self.agent_id = agent_id
        self.registry = registry or CollectorRegistry()
        self._setup_metrics()
    
    def _setup_metrics(self):
        # Decision metrics
        self.decisions_total = Counter(
            'agent_decisions_total',
            'Total de decisiones por tipo y resultado',
            ['agent_id', 'decision_type', 'outcome'],
            registry=self.registry
        )
        
        self.decision_duration = Histogram(
            'agent_decision_duration_seconds',
            'Duración de decisiones en segundos',
            ['agent_id', 'decision_type'],
            buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0],
            registry=self.registry
        )
        
        # Tool metrics
        self.tool_calls = Counter(
            'agent_tool_calls_total',
            'Llamadas a herramientas',
            ['agent_id', 'tool_name', 'status'],
            registry=self.registry
        )
        
        self.tool_duration = Histogram(
            'agent_tool_duration_seconds',
            'Duración de herramientas',
            ['agent_id', 'tool_name'],
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
            registry=self.registry
        )
        
        # Memory metrics
        self.memory_ops = Counter(
            'agent_memory_operations_total',
            'Operaciones de memoria',
            ['agent_id', 'operation', 'memory_type', 'status'],
            registry=self.registry
        )
        
        self.memory_duration = Histogram(
            'agent_memory_duration_seconds',
            'Duración de operaciones de memoria',
            ['agent_id', 'memory_type'],
            buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5],
            registry=self.registry
        )
        
        self.memory_size = Gauge(
            'agent_memory_size_bytes',
            'Tamaño de memoria en bytes',
            ['agent_id', 'memory_type'],
            registry=self.registry
        )
        
        # Reasoning metrics
        self.reasoning_cycles = Histogram(
            'agent_reasoning_cycles_total',
            'Ciclos de razonamiento por decisión',
            ['agent_id', 'decision_type'],
            buckets=[1, 2, 3, 4, 5, 8, 10, 15, 20, 30, 50],
            registry=self.registry
        )
        
        self.reasoning_tokens = Counter(
            'agent_reasoning_tokens_total',
            'Tokens usados en reasoning',
            ['agent_id', 'token_type'],
            registry=self.registry
        )
        
        # State metrics
        self.state_size = Gauge(
            'agent_state_size_bytes',
            'Tamaño del estado del agente',
            ['agent_id', 'state_component'],
            registry=self.registry
        )
        
        self.active = Gauge(
            'agent_active',
            'Agente activo (1=si, 0=no)',
            ['agent_id'],
            registry=self.registry
        )
        
        # Error metrics
        self.errors = Counter(
            'agent_errors_total',
            'Errores del agente',
            ['agent_id', 'error_type', 'severity'],
            registry=self.registry
        )
    
    def record_decision(self, decision_type: str, outcome: str, duration: float):
        """Registra una decisión del agente"""
        self.decisions_total.labels(
            agent_id=self.agent_id,
            decision_type=decision_type,
            outcome=outcome
        ).inc()
        
        self.decision_duration.labels(
            agent_id=self.agent_id,
            decision_type=decision_type
        ).observe(duration)
    
    def record_tool(self, tool_name: str, status: str, duration: float):
        """Registra una llamada a herramienta"""
        self.tool_calls.labels(
            agent_id=self.agent_id,
            tool_name=tool_name,
            status=status
        ).inc()
        
        if status == 'success':
            self.tool_duration.labels(
                agent_id=self.agent_id,
                tool_name=tool_name
            ).observe(duration)
    
    def record_memory(self, operation: str, memory_type: str, 
                     status: str, duration: float, size: int):
        """Registra una operación de memoria"""
        self.memory_ops.labels(
            agent_id=self.agent_id,
            operation=operation,
            memory_type=memory_type,
            status=status
        ).inc()
        
        if status == 'success':
            self.memory_duration.labels(
                agent_id=self.agent_id,
                memory_type=memory_type
            ).observe(duration)
        
        self.memory_size.labels(
            agent_id=self.agent_id,
            memory_type=memory_type
        ).set(size)
    
    def record_reasoning(self, decision_type: str, cycles: int, token_count: int):
        """Registra métricas de reasoning"""
        self.reasoning_cycles.labels(
            agent_id=self.agent_id,
            decision_type=decision_type
        ).observe(cycles)
        
        self.reasoning_tokens.labels(
            agent_id=self.agent_id,
            token_type='total'
        ).inc(token_count)
    
    def record_error(self, error_type: str, severity: str):
        """Registra un error"""
        self.errors.labels(
            agent_id=self.agent_id,
            error_type=error_type,
            severity=severity
        ).inc()
    
    def set_state_size(self, component: str, size: int):
        """Actualiza tamaño del estado"""
        self.state_size.labels(
            agent_id=self.agent_id,
            state_component=component
        ).set(size)
    
    def set_active(self, active: bool):
        """Marca agente como activo/inactivo"""
        self.active.labels(agent_id=self.agent_id).set(1 if active else 0)
    
    def export_metrics(self) -> bytes:
        """Exporta métricas en formato Prometheus"""
        return generate_latest(self.registry)


class MetricsServer:
    """Servidor HTTP para exponer métricas"""
    
    def __init__(self, metrics: CompleteAgentMetrics, port: int = 8000):
        self.metrics = metrics
        self.port = port
    
    def get_metrics(self):
        """Endpoint para obtener métricas"""
        return self.metrics.export_metrics()


# Demo de uso
if __name__ == "__main__":
    # Crear métricas para un agente
    agent_metrics = CompleteAgentMetrics(agent_id="agent-factory-01")
    
    # Simular decisiones
    import random
    
    for i in range(100):
        decision_type = random.choice(['process_order', 'check_inventory', 
                                      'approve_request', 'route_ticket'])
        outcome = random.choices(['success', 'failure'], weights=[0.95, 0.05])[0]
        duration = random.uniform(0.1, 5.0)
        
        agent_metrics.record_decision(decision_type, outcome, duration)
        
        if outcome == 'success':
            cycles = random.randint(1, 10)
            tokens = random.randint(100, 5000)
            agent_metrics.record_reasoning(decision_type, cycles, tokens)
    
    # Simular llamadas a herramientas
    tools = ['get_order', 'update_inventory', 'send_notification', 
             'query_database', 'call_api']
    
    for i in range(50):
        tool = random.choice(tools)
        status = random.choices(['success', 'failure'], weights=[0.92, 0.08])[0]
        duration = random.uniform(0.01, 2.0)
        
        agent_metrics.record_tool(tool, status, duration)
    
    # Simular operaciones de memoria
    for i in range(200):
        operation = random.choice(['read', 'write', 'search'])
        memory_type = random.choice(['short_term', 'long_term', 'working'])
        status = random.choices(['success', 'failure'], weights=[0.98, 0.02])[0]
        duration = random.uniform(0.001, 0.1)
        size = random.randint(1000, 100000)
        
        agent_metrics.record_memory(operation, memory_type, status, duration, size)
    
    # Simular errores
    error_types = ['timeout', 'invalid_input', 'resource_unavailable', 'logic_error']
    for i in range(5):
        error_type = random.choice(error_types)
        severity = random.choice(['warning', 'error'])
        
        agent_metrics.record_error(error_type, severity)
    
    # Exportar métricas
    metrics_output = agent_metrics.export_metrics()
    print(metrics_output.decode('utf-8'))
```

### Ejercicio 2: Configurar Dashboard en Grafana (30 minutos)

**Objetivo:** Crear un dashboard completo para monitorear agentes industriales.

**Solución:** El código anterior incluye la especificación JSON del dashboard. Para implementarlo:

1. Guardar el JSON en `grafana/dashboards/agent-overview.json`
2. Importar en Grafana via API o UI
3. Configurar datasource de Prometheus

### Ejercicio 3: Configurar Alerting Completo (30 minutos)

**Objetivo:** Implementar un sistema de alerting completo para agentes.

**Solución:**

```python
# alerting/agent_alerting_system.py
from dataclasses import dataclass
from typing import Callable, Optional
import time
from enum import Enum

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class AlertRule:
    name: str
    condition: Callable[[], bool]
    severity: AlertSeverity
    message: str
    cooldown_seconds: int = 300
    
    def __post_init__(self):
        self.last_triggered = 0

class AlertManager:
    """Sistema de gestión de alertas para agentes"""
    
    def __init__(self):
        self.rules: list[AlertRule] = []
        self.handlers: dict[AlertSeverity, list[Callable]] = {
            severity: [] for severity in AlertSeverity
        }
    
    def add_rule(self, rule: AlertRule):
        """Agrega una regla de alerta"""
        self.rules.append(rule)
    
    def register_handler(self, severity: AlertSeverity, handler: Callable):
        """Registra un manejador de alertas"""
        self.handlers[severity].append(handler)
    
    def check_rules(self):
        """Verifica todas las reglas de alerta"""
        current_time = time.time()
        
        for rule in self.rules:
            # Verificar cooldown
            if current_time - rule.last_triggered < rule.cooldown_seconds:
                continue
            
            # Verificar condición
            if rule.condition():
                rule.last_triggered = current_time
                self._trigger_alert(rule)
    
    def _trigger_alert(self, rule: AlertRule):
        """Dispara una alerta"""
        print(f"[{rule.severity.value.upper()}] {rule.name}: {rule.message}")
        
        # Notificar handlers
        for handler in self.handlers[rule.severity]:
            try:
                handler(rule)
            except Exception as e:
                print(f"Error en handler de alerta: {e}")


# Ejemplo de uso
def create_agent_alerting_system(
    agent_metrics,
    pagerduty_key: Optional[str] = None
) -> AlertManager:
    """Crea un sistema de alerting completo para agentes"""
    
    manager = AlertManager()
    
    # Regla: Alta latencia de decisiones
    manager.add_rule(AlertRule(
        name="high_decision_latency",
        condition=lambda: agent_metrics.decision_duration._value.get('p99', 0) > 5.0,
        severity=AlertSeverity.WARNING,
        message="Latencia de decisiones elevada",
        cooldown_seconds=300
    ))
    
    # Regla: Tasa de fallos alta
    manager.add_rule(AlertRule(
        name="high_failure_rate",
        condition=lambda: agent_metrics.get_failure_rate() > 0.1,
        severity=AlertSeverity.CRITICAL,
        message="Tasa de fallos en decisiones > 10%",
        cooldown_seconds=60
    ))
    
    # Regla: Memoria elevada
    manager.add_rule(AlertRule(
        name="high_memory_usage",
        condition=lambda: agent_metrics.get_total_memory_size() > 1_000_000_000,
        severity=AlertSeverity.WARNING,
        message="Uso de memoria > 1GB",
        cooldown_seconds=600
    ))
    
    # Regla: Herramientas fallando
    manager.add_rule(AlertRule(
        name="tool_failures",
        condition=lambda: agent_metrics.get_tool_failure_rate() > 0.05,
        severity=AlertSeverity.ERROR,
        message="Herramientas fallando > 5%",
        cooldown_seconds=180
    ))
    
    return manager
```

## Resumen de Puntos Clave

1. **Observabilidad Agéntica**: Los agentes requieren métricas, logs y traces específicos que capturen su comportamiento único (decisiones, herramientas, memoria, reasoning).

2. **SLI/SLA**: Los indicadores deben reflejar la naturaleza de los agentes - latencia de decisiones, éxito de herramientas, consistencia de estado, calidad de reasoning.

3. **Arquitectura de Monitoreo**: Stack basado en Prometheus + Grafana + Alertmanager + sistemas de escalamiento (PagerDuty/OpsGenie).

4. **Dashboards**: Necesarios múltiples dashboards - overview, reasoning, herramientas, memoria - para diferentes aspectos del sistema.

5. **Alerting**: Configurar reglas específicas para incidentes de agentes con procedimientos de respuesta (runbooks) y escalamiento automático.

## Referencias Externas

- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Grafana Dashboards Best Practices](https://grafana.com/docs/grafana/latest/dashboards/)
- [PagerDuty Incident Management](https://support.pagerduty.com/docs)
- [OpsGenie Alerting](https://docs.opsgenie.com/docs/alert-api)
- [Google SRE Book - Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Observability Engineering Book](https://www.oreilly.com/library/view/observability-engineering/9781492076438/)