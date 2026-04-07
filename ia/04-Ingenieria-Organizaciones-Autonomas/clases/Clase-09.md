# Clase 9: Agent-Ops - Observabilidad

## Duración
**4 horas** (240 minutos)

---

## Objetivos de Aprendizaje

Al finalizar esta clase, el estudiante será capaz de:

1. **Comprender** los fundamentos de la observabilidad en sistemas multi-agente
2. **Implementar** logging estructurado con correlación de trazas
3. **Diseñar** y construir dashboards operativos para monitoreo de agentes
4. **Configurar** distributed tracing para arquitecturas de agentes distribuidos
5. **Integrar** sistemas de metrics collection en pipelines de agentes
6. **Establecer** alertas y thresholds apropiados para métricas de agentes
7. **Utilizar** OpenTelemetry como estándar de instrumentación

---

## 1. Fundamentos de Observabilidad en Sistemas Multi-Agente

### 1.1 ¿Qué es la Observabilidad?

La observabilidad es la capacidad de comprender el estado interno de un sistema a través de sus salidas externas. En el contexto de organizaciones de agentes autónomos, esto significa poder entender:

- **Qué está haciendo** cada agente en cualquier momento
- **Por qué** un agente tomó una decisión específica
- **Cuándo** terjadi problemas de rendimiento o comportamiento
- **Dónde** se encuentran los cuellos de botella en la cadena de procesamiento

### 1.2 Los Tres Pilares de la Observabilidad

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PILARES DE OBSERVABILIDAD                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                │
│    │             │    │             │    │             │                │
│    │    LOGS     │    │   METRICS   │    │   TRACES    │                │
│    │             │    │             │    │             │                │
│    │  Eventos    │    │  Números    │    │  Caminos    │                │
│    │  discretos  │    │  agregados  │    │  de请求      │                │
│    │             │    │             │    │             │                │
│    └─────────────┘    └─────────────┘    └─────────────┘                │
│         │                   │                   │                       │
│         └───────────────────┼───────────────────┘                       │
│                             │                                           │
│                    ┌────────▼────────┐                                  │
│                    │                 │                                  │
│                    │  OBSERVABILIDAD │                                  │
│                    │    COMPLETA     │                                  │
│                    │                 │                                  │
│                    └─────────────────┘                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Por qué la Observabilidad es Crítica para Agentes

Los sistemas de agentes autónomos presentan desafíos únicos:

| Desafío | Descripción | Impacto sin Observabilidad |
|---------|-------------|---------------------------|
| **Decisiones No Determinísticas** | Los agentes pueden tomar diferentes caminos | Imposible auditar el razonamiento |
| **Cadenas de Dependencias** | Un agente触发 múltiples sub-agentes | Difícil rastrear el flujo completo |
| ** Estados Implícitos** | El contexto se mantiene en memoria | No hay forma de recrear una situación |
| **Efectos Colaterales** | Acciones pueden afectar otros agentes | Imposible identificar la causa raíz |
| **Latencia Variable** | Tiempos de respuesta impredecibles | No se puede optimizar el rendimiento |

---

## 2. Logging Estructurado

### 2.1 Conceptos Fundamentales

El logging estructurado es un enfoque donde los logs se escriben en un formato machines-readable (generalmente JSON) en lugar de texto libre. Esto permite:

- **Búsqueda eficiente** por campos específicos
- **Agregación** automática de eventos relacionados
- **Correlación** entre diferentes componentes
- **Análisis** programático de patrones

### 2.2 Formato de Log Estructurado

```json
{
  "timestamp": "2024-01-15T14:32:15.123Z",
  "level": "INFO",
  "service": "agent-coordinator",
  "agent_id": "agent-orchestrator-001",
  "trace_id": "abc123-def456-ghi789",
  "span_id": "span-001",
  "message": "Agente completado exitosamente",
  "context": {
    "task_id": "task-xyz789",
    "execution_time_ms": 1234,
    "tokens_consumed": 5678,
    "model": "gpt-4-turbo"
  },
  "tags": ["agent", "completion", "success"]
}
```

### 2.3 Implementación de Logging Estructurado en Python

```python
# logging_structured.py
import logging
import json
import uuid
from datetime import datetime, timezone
from contextvars import ContextVar
from typing import Any, Dict, Optional
from functools import wraps
import traceback

# Context variables para correlación
trace_id_var: ContextVar[str] = ContextVar('trace_id', default='')
span_id_var: ContextVar[str] = ContextVar('span_id', default='')
agent_id_var: ContextVar[str] = ContextVar('agent_id', default='')

class StructuredJSONFormatter(logging.Formatter):
    """
    Formateador que convierte logs a JSON estructurado.
    Implementa el estándar de logging de la OpenTelemetry.
    """
    
    def __init__(self, include_extra: bool = True):
        super().__init__()
        self.include_extra = include_extra
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "trace_id": trace_id_var.get() or None,
            "span_id": span_id_var.get() or None,
            "agent_id": agent_id_var.get() or None,
        }
        
        # Agregar información de excepción si existe
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": traceback.format_exception(*record.exc_info)
            }
        
        # Agregar campos extra
        if self.include_extra and hasattr(record, 'extra_fields'):
            log_data["context"] = record.extra_fields
        
        return json.dumps(log_data, default=str)


class AgentLogger:
    """
    Logger especializado para agentes con capacidades de correlación.
    """
    
    def __init__(self, name: str, agent_id: str):
        self.logger = logging.getLogger(name)
        self.agent_id = agent_id
        agent_id_var.set(agent_id)
        
        # Configurar handler con JSON
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredJSONFormatter())
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
    
    def _log(self, level: int, message: str, **kwargs: Any) -> None:
        """Método base para logging con campos extra."""
        extra = logging.makeLogRecord({"extra_fields": kwargs})
        self.logger.log(level, message, extra=extra)
    
    def info(self, message: str, **kwargs: Any) -> None:
        self._log(logging.INFO, message, **kwargs)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        self._log(logging.DEBUG, message, **kwargs)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs: Any) -> None:
        self._log(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs: Any) -> None:
        self._log(logging.CRITICAL, message, **kwargs)
    
    def log_agent_action(self, action: str, target: str, params: Dict[str, Any], 
                        result: Optional[Dict] = None, error: Optional[str] = None) -> None:
        """Log especializado para acciones de agentes."""
        log_entry = {
            "action_type": "agent_action",
            "action": action,
            "target": target,
            "params": params,
        }
        if result:
            log_entry["result"] = result
        if error:
            log_entry["error"] = error
            self.error(f"Agent action failed: {action}", **log_entry)
        else:
            self.info(f"Agent action completed: {action}", **log_entry)
    
    def log_decision(self, decision_type: str, context: Dict, 
                    reasoning: str, choice: str, confidence: float) -> None:
        """Log especializado para decisiones de agentes."""
        self.info(
            f"Agent decision: {decision_type}",
            action_type="agent_decision",
            decision_type=decision_type,
            context=context,
            reasoning=reasoning,
            choice=choice,
            confidence=confidence
        )
    
    def log_llm_interaction(self, prompt_tokens: int, completion_tokens: int,
                           model: str, latency_ms: float, 
                           response_summary: str, cost: float) -> None:
        """Log especializado para interacciones con LLMs."""
        self.info(
            "LLM interaction completed",
            action_type="llm_interaction",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            model=model,
            latency_ms=latency_ms,
            cost_usd=cost,
            response_summary=response_summary[:200]  # Truncar para no saturar logs
        )


def trace_context(trace_id: Optional[str] = None, span_id: Optional[str] = None):
    """Decorador para establecer contexto de traza en funciones."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            old_trace = trace_id_var.get()
            old_span = span_id_var.get()
            
            try:
                if trace_id:
                    trace_id_var.set(trace_id)
                else:
                    trace_id_var.set(str(uuid.uuid4()))
                
                if span_id:
                    span_id_var.set(span_id)
                else:
                    span_id_var.set(str(uuid.uuid4())[:8])
                
                return func(*args, **kwargs)
            finally:
                trace_id_var.set(old_trace)
                span_id_var.set(old_span)
        
        return wrapper
    return decorator


# Ejemplo de uso
if __name__ == "__main__":
    # Crear logger para un agente específico
    agent_logger = AgentLogger("orchestrator", "agent-001")
    
    @trace_context()
    def process_user_request(request_id: str, query: str):
        agent_logger.info(
            "Processing user request",
            request_id=request_id,
            query_preview=query[:100],
            query_length=len(query)
        )
        
        # Simular procesamiento
        agent_logger.log_llm_interaction(
            prompt_tokens=150,
            completion_tokens=300,
            model="gpt-4-turbo",
            latency_ms=1250.5,
            response_summary="Generated response about...",
            cost=0.015
        )
        
        agent_logger.log_decision(
            decision_type="route_to_specialist",
            context={"query_type": "technical", "complexity": "high"},
            reasoning="Query contains technical terms requiring specialist agent",
            choice="route_to_technical_agent",
            confidence=0.92
        )
        
        agent_logger.log_agent_action(
            action="delegate",
            target="technical-specialist-agent",
            params={"specialization": "code-review", "priority": "high"},
            result={"task_id": "task-123", "estimated_time_ms": 5000}
        )
        
        return {"status": "delegated", "task_id": "task-123"}
    
    process_user_request("req-001", "¿Cómo optimizo este algoritmo de búsqueda?")
```

### 2.4 Logging Distribuido con Correlación

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    FLUJO DE LOGGING DISTRIBUIDO                              │
│                                                                              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐ │
│  │   Agent 1   │     │   Agent 2   │     │   Agent 3   │     │   Agent 4   │ │
│  │ trace:abc   │     │ trace:abc   │     │ trace:abc   │     │ trace:abc   │ │
│  │ span:001    │────▶│ span:002    │────▶│ span:003    │────▶│ span:004    │ │
│  └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘ │
│        │                   │                   │                   │        │
│        └───────────────────┴───────────────────┴───────────────────┘        │
│                                    │                                        │
│                                    ▼                                        │
│                    ┌───────────────────────────────┐                       │
│                    │     LOG AGGREGATOR            │                       │
│                    │   (Fluentd, Vector, etc.)     │                       │
│                    └───────────────────────────────┘                       │
│                                    │                                        │
│                                    ▼                                        │
│                    ┌───────────────────────────────┐                       │
│                    │    STORAGE BACKEND            │                       │
│                    │  (Elasticsearch, Loki, etc.) │                       │
│                    └───────────────────────────────┘                       │
│                                    │                                        │
│                                    ▼                                        │
│                    ┌───────────────────────────────┐                       │
│                    │    VISUALIZATION              │                       │
│                    │   (Kibana, Grafana)           │                       │
│                    └───────────────────────────────┘                       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Distributed Tracing

### 3.1 Introducción al Tracing Distribuido

El distributed tracing permite seguir una请求 a través de múltiples servicios y agentes, correlacionando todos los logs y métricas asociados con esa solicitud específica.

### 3.2 Conceptos Clave

- **Trace**: La representación completa de una请求 desde inicio hasta fin
- **Span**: Una unidad de trabajo individual dentro de un trace
- **Parent Span**: El span que creó otro span
- **Span Context**: Información de contexto que se propaga entre servicios

### 3.3 Implementación con OpenTelemetry

```python
# distributed_tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.propagate import set_global_textmap
from contextlib import contextmanager
from typing import Any, Dict, Optional, Generator
import time
import json

# Configuración del proveedor de trazas
def setup_tracing(service_name: str, otlp_endpoint: str) -> trace.Tracer:
    """
    Configura OpenTelemetry para distributed tracing.
    
    Args:
        service_name: Nombre del servicio/агент
        otlp_endpoint: URL del collector OTLP (ej: http://localhost:4317)
    
    Returns:
        Tracer configurado listo para usar
    """
    # Crear resource con información del servicio
    resource = Resource.create({
        ResourceAttributes.SERVICE_NAME: service_name,
        ResourceAttributes.SERVICE_VERSION: "1.0.0",
        ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "production",
    })
    
    # Configurar proveedor de trazas
    provider = TracerProvider(resource=resource)
    
    # Configurar exportador OTLP
    otlp_exporter = OTLPSpanExporter(
        endpoint=otlp_endpoint,
        insecure=True  # Para desarrollo, en producción usar TLS
    )
    
    # Agregar procesador de spans en batch
    span_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)
    
    # Establecer como proveedor global
    trace.set_tracer_provider(provider)
    
    # Configurar propagador de contexto (W3C Trace Context)
    set_global_textmap(TraceContextTextMapPropagator())
    
    return trace.get_tracer(service_name)


class AgentSpan:
    """
    Clase helper para crear y gestionar spans de OpenTelemetry
    con convenciones específicas para agentes.
    """
    
    def __init__(self, tracer: trace.Tracer, agent_name: str, agent_version: str = "1.0.0"):
        self.tracer = tracer
        self.agent_name = agent_name
        self.agent_version = agent_version
        self.propagator = TraceContextTextMapPropagator()
    
    @contextmanager
    def create_span(self, 
                    operation_name: str,
                    span_type: str = "agent.operation",
                    attributes: Optional[Dict[str, Any]] = None,
                    parent_context: Optional[Dict] = None) -> Generator[trace.Span, None, None]:
        """
        Crea un span para una operación de agente.
        
        Args:
            operation_name: Nombre descriptivo de la operación
            span_type: Tipo de operación (agent.thought, agent.action, etc.)
            attributes: Atributos adicionales para el span
            parent_context: Contexto de propagación (para continuar un trace)
        """
        span_kind = trace.SpanKind.INTERNAL
        
        # Si hay contexto padre, extraerlo
        ctx = None
        if parent_context:
            ctx = self.propagator.extract(carrier=parent_context)
            span_kind = trace.SpanKind.CLIENT
        
        # Agregar atributos base
        base_attributes = {
            "agent.name": self.agent_name,
            "agent.version": self.agent_version,
            "agent.operation.type": span_type,
            "agent.timestamp": time.time(),
        }
        
        if attributes:
            base_attributes.update(attributes)
        
        with self.tracer.start_as_current_span(
            operation_name,
            kind=span_kind,
            context=ctx,
            attributes=base_attributes
        ) as span:
            try:
                yield span
            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise
    
    def trace_llm_call(self, 
                       model: str,
                       prompt_tokens: int,
                       completion_tokens: int,
                       latency_ms: float,
                       error: Optional[str] = None):
        """Crea un span para llamadas a LLMs."""
        with self.create_span(
            f"LLM.{model}",
            span_type="agent.llm_call",
            attributes={
                "llm.model": model,
                "llm.prompt_tokens": prompt_tokens,
                "llm.completion_tokens": completion_tokens,
                "llm.total_tokens": prompt_tokens + completion_tokens,
                "llm.latency_ms": latency_ms,
            }
        ) as span:
            if error:
                span.set_attribute("error", True)
                span.set_attribute("error.message", error)
    
    def trace_tool_execution(self,
                            tool_name: str,
                            tool_input: Dict,
                            tool_output: Any,
                            execution_time_ms: float,
                            error: Optional[str] = None):
        """Crea un span para ejecución de herramientas."""
        with self.create_span(
            f"Tool.{tool_name}",
            span_type="agent.tool_execution",
            attributes={
                "tool.name": tool_name,
                "tool.input_size": len(str(tool_input)),
                "tool.output_size": len(str(tool_output)),
                "tool.execution_time_ms": execution_time_ms,
            }
        ) as span:
            if error:
                span.set_attribute("error", True)
                span.set_attribute("error.message", error)
    
    def trace_agent_delegation(self,
                              target_agent: str,
                              task: str,
                              priority: str = "normal"):
        """Crea un span para delegación a otros agentes."""
        with self.create_span(
            f"Delegate.to.{target_agent}",
            span_type="agent.delegation",
            attributes={
                "delegation.target_agent": target_agent,
                "delegation.task": task,
                "delegation.priority": priority,
            }
        ) as span:
            return span
    
    def trace_decision_point(self,
                            decision_type: str,
                            options: list,
                            selected_option: str,
                            reasoning: str,
                            confidence: float):
        """Crea un span para puntos de decisión."""
        with self.create_span(
            f"Decision.{decision_type}",
            span_type="agent.decision",
            attributes={
                "decision.type": decision_type,
                "decision.options_count": len(options),
                "decision.selected": selected_option,
                "decision.reasoning_length": len(reasoning),
                "decision.confidence": confidence,
            }
        ) as span:
            span.add_event(
                "decision.options",
                attributes={"options": json.dumps(options)}
            )
            span.add_event(
                "decision.reasoning",
                attributes={"reasoning": reasoning}
            )
    
    def extract_context_for_propagation(self, span: trace.Span) -> Dict[str, str]:
        """Extrae el contexto del span para propagar a otros servicios."""
        carrier: Dict[str, str] = {}
        self.propagator.inject(carrier, context=trace.set_span_in_context(span))
        return carrier


class MultiAgentTraceManager:
    """
    Gestiona trazas distribuidas entre múltiples agentes.
    """
    
    def __init__(self, coordinator_agent_name: str, otlp_endpoint: str):
        self.tracer = setup_tracing(coordinator_agent_name, otlp_endpoint)
        self.agent_spans: Dict[str, AgentSpan] = {}
        self.active_traces: Dict[str, trace.Span] = {}
    
    def register_agent(self, agent_name: str) -> AgentSpan:
        """Registra un agente y retorna su span helper."""
        if agent_name not in self.agent_spans:
            self.agent_spans[agent_name] = AgentSpan(self.tracer, agent_name)
        return self.agent_spans[agent_name]
    
    @contextmanager
    def start_trace(self, trace_id: str, operation_name: str, 
                   initial_attributes: Optional[Dict] = None):
        """Inicia una nueva traza completa."""
        with self.tracer.start_as_current_span(
            operation_name,
            kind=trace.SpanKind.SERVER,
            attributes=initial_attributes or {}
        ) as span:
            span.set_attribute("trace.id", trace_id)
            self.active_traces[trace_id] = span
            try:
                yield span
            finally:
                self.active_traces.pop(trace_id, None)
    
    def propagate_trace(self, from_agent: str, to_agent: str, 
                       trace_id: str, task_context: Dict) -> Dict[str, str]:
        """Propaga una traza de un agente a otro."""
        if trace_id in self.active_traces:
            span = self.active_traces[trace_id]
            return self.agent_spans[from_agent].extract_context_for_propagation(span)
        return {}


# Ejemplo de uso integrado
def example_multi_agent_tracing():
    """Ejemplo completo de tracing multi-agente."""
    
    # Configurar tracing
    trace_manager = MultiAgentTraceManager(
        coordinator_agent_name="agent-coordinator",
        otlp_endpoint="http://localhost:4317"
    )
    
    # Registrar agentes
    orchestrator = trace_manager.register_agent("orchestrator")
    specialist = trace_manager.register_agent("specialist-agent")
    evaluator = trace_manager.register_agent("evaluator-agent")
    
    # Iniciar traza para una solicitud
    with trace_manager.start_trace("trace-001", "user.request.processing") as main_span:
        main_span.set_attribute("request.type", "code_review")
        main_span.set_attribute("request.priority", "high")
        
        # Orquestador recibe la solicitud
        with orchestrator.create_span(
            "receive.user.request",
            span_type="agent.receive"
        ) as span:
            span.set_attribute("user.id", "user-123")
            span.set_attribute("request.content", "Review my PR")
        
        # Simular análisis inicial
        with orchestrator.trace_llm_call(
            model="gpt-4-turbo",
            prompt_tokens=200,
            completion_tokens=150,
            latency_ms=1500.0
        ):
            pass
        
        # Tomar decisión de enrutamiento
        orchestrator.trace_decision_point(
            decision_type="route_request",
            options=["code-review", "documentation", "testing"],
            selected_option="code-review",
            reasoning="PR contains complex algorithmic changes",
            confidence=0.95
        )
        
        # Delegar al agente especialista
        delegation_context = orchestrator.trace_agent_delegation(
            target_agent="specialist-agent",
            task="comprehensive_code_review",
            priority="high"
        )
        delegation_context["trace_id"] = "trace-001"
        
        # Agente especialista procesa
        with specialist.create_span(
            "process.code.review",
            span_type="agent.process",
            parent_context=delegation_context
        ) as span:
            span.set_attribute("review.scope", "full")
            span.set_attribute("files.count", 15)
            
            # Simular ejecución de herramientas
            specialist.trace_tool_execution(
                tool_name="git-diff",
                tool_input={"files": ["src/main.py", "src/utils.py"]},
                tool_output={"changes": 42, "additions": 150, "deletions": 30},
                execution_time_ms=500.0
            )
            
            specialist.trace_llm_call(
                model="claude-3-opus",
                prompt_tokens=3000,
                completion_tokens=800,
                latency_ms=3000.0
            )
        
        # Regresar resultado al orquestador
        with orchestrator.create_span(
            "aggregate.results",
            span_type="agent.aggregate"
        ) as span:
            span.add_event("received_specialist_results")
        
        # Evaluador valida el resultado
        with evaluator.create_span(
            "validate.aggregated.results",
            span_type="agent.validate"
        ) as span:
            evaluator.trace_llm_call(
                model="gpt-4-turbo",
                prompt_tokens=500,
                completion_tokens=100,
                latency_ms=800.0
            )
            span.set_attribute("validation.passed", True)
        
        main_span.add_event("processing_complete")


if __name__ == "__main__":
    example_multi_agent_tracing()
```

---

## 4. Metrics Collection

### 4.1 Tipos de Métricas para Agentes

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    TAXONOMÍA DE MÉTRICAS PARA AGENTES                       │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        MÉTRICAS DE RED                            │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  • Request rate (req/s)                                            │   │
│  │  • Error rate (% de requests con errores)                         │   │
│  │  • Duration (latencia de procesamiento)                          │   │
│  │  • Saturation (uso de recursos)                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     MÉTRICAS DE NEGOCIO                            │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  • Tasks completed successfully                                    │   │
│  │  • Tasks failed                                                    │   │
│  │  • Task duration by type                                           │   │
│  │  • Escalation rate (delegaciones a humanos)                        │   │
│  │  • User satisfaction score                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    MÉTRICAS DE LLM                                  │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  • Tokens consumed (prompt + completion)                          │   │
│  │  • LLM latency                                                     │   │
│  │  • LLM error rate                                                  │   │
│  │  • Cost per request                                                │   │
│  │  • Token efficiency (% de tokens útiles)                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                  MÉTRICAS DE AGENTE                                 │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  • Decision latency                                                │   │
│  │  • Actions taken                                                   │   │
│  │  • Context window utilization                                      │   │
│  │  • Memory usage                                                    │   │
│  │  • Confidence score distribution                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Implementación con Prometheus

```python
# metrics_collection.py
from prometheus_client import Counter, Histogram, Gauge, Summary, CollectorRegistry, push_to_gateway
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from typing import Dict, List, Optional, Callable
import time
import functools
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading

# Registry personalizado para evitar conflictos
AGENT_REGISTRY = CollectorRegistry()


@dataclass
class AgentMetrics:
    """
    Colección completa de métricas para un agente individual.
    """
    agent_name: str
    registry: CollectorRegistry = field(default_factory=lambda: AGENT_REGISTRY)
    
    # Contadores
    tasks_total: Counter = field(init=False)
    tasks_success: Counter = field(init=False)
    tasks_failed: Counter = field(init=False)
    llm_calls_total: Counter = field(init=False)
    llm_errors: Counter = field(init=False)
    tool_calls_total: Counter = field(init=False)
    tool_errors: Counter = field(init=False)
    delegations_total: Counter = field(init=False)
    escalations_to_human: Counter = field(init=False)
    
    # Histogramas
    task_duration_seconds: Histogram = field(init=False)
    llm_latency_seconds: Histogram = field(init=False)
    llm_tokens_total: Histogram = field(init=False)
    llm_cost_dollars: Histogram = field(init=False)
    tool_execution_seconds: Histogram = field(init=False)
    decision_latency_seconds: Histogram = field(init=False)
    context_window_usage: Histogram = field(init=False)
    
    # Gauges
    active_tasks: Gauge = field(init=False)
    queue_depth: Gauge = field(init=False)
    memory_usage_bytes: Gauge = field(init=False)
    current_confidence: Gauge = field(init=False)
    
    def __post_init__(self):
        prefix = f"agent_{self.agent_name.replace('-', '_')}"
        
        # Inicializar contadores
        self.tasks_total = Counter(
            f"{prefix}_tasks_total",
            "Total de tareas recibidas",
            ["task_type"],
            registry=self.registry
        )
        
        self.tasks_success = Counter(
            f"{prefix}_tasks_success_total",
            "Tareas completadas exitosamente",
            ["task_type"],
            registry=self.registry
        )
        
        self.tasks_failed = Counter(
            f"{prefix}_tasks_failed_total",
            "Tareas que fallaron",
            ["task_type", "error_type"],
            registry=self.registry
        )
        
        self.llm_calls_total = Counter(
            f"{prefix}_llm_calls_total",
            "Llamadas totales a LLM",
            ["model", "status"],
            registry=self.registry
        )
        
        self.llm_errors = Counter(
            f"{prefix}_llm_errors_total",
            "Errores de llamadas LLM",
            ["model", "error_type"],
            registry=self.registry
        )
        
        self.tool_calls_total = Counter(
            f"{prefix}_tool_calls_total",
            "Ejecuciones de herramientas totales",
            ["tool_name", "status"],
            registry=self.registry
        )
        
        self.tool_errors = Counter(
            f"{prefix}_tool_errors_total",
            "Errores de herramientas",
            ["tool_name", "error_type"],
            registry=self.registry
        )
        
        self.delegations_total = Counter(
            f"{prefix}_delegations_total",
            "Delegaciones a otros agentes",
            ["target_agent", "reason"],
            registry=self.registry
        )
        
        self.escalations_to_human = Counter(
            f"{prefix}_escalations_human_total",
            "Escalaciones a supervisión humana",
            ["reason"],
            registry=self.registry
        )
        
        # Inicializar histogramas
        self.task_duration_seconds = Histogram(
            f"{prefix}_task_duration_seconds",
            "Duración de tareas en segundos",
            ["task_type"],
            buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0),
            registry=self.registry
        )
        
        self.llm_latency_seconds = Histogram(
            f"{prefix}_llm_latency_seconds",
            "Latencia de llamadas LLM",
            ["model"],
            buckets=(0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 60.0),
            registry=self.registry
        )
        
        self.llm_tokens_total = Histogram(
            f"{prefix}_llm_tokens_total",
            "Tokens consumidos por llamada",
            ["model", "token_type"],
            buckets=(10, 50, 100, 500, 1000, 5000, 10000, 50000),
            registry=self.registry
        )
        
        self.llm_cost_dollars = Histogram(
            f"{prefix}_llm_cost_dollars",
            "Costo de llamadas LLM en USD",
            ["model"],
            buckets=(0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0),
            registry=self.registry
        )
        
        self.tool_execution_seconds = Histogram(
            f"{prefix}_tool_execution_seconds",
            "Tiempo de ejecución de herramientas",
            ["tool_name"],
            buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0),
            registry=self.registry
        )
        
        self.decision_latency_seconds = Histogram(
            f"{prefix}_decision_latency_seconds",
            "Latencia en puntos de decisión",
            ["decision_type"],
            buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 2.5),
            registry=self.registry
        )
        
        self.context_window_usage = Histogram(
            f"{prefix}_context_window_usage_ratio",
            "Porcentaje de context window utilizado",
            ["model"],
            buckets=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95),
            registry=self.registry
        )
        
        # Inicializar gauges
        self.active_tasks = Gauge(
            f"{prefix}_active_tasks",
            "Número de tareas actualmente en procesamiento",
            registry=self.registry
        )
        
        self.queue_depth = Gauge(
            f"{prefix}_queue_depth",
            "Profundidad de cola de tareas pendientes",
            registry=self.registry
        )
        
        self.memory_usage_bytes = Gauge(
            f"{prefix}_memory_usage_bytes",
            "Uso de memoria del agente en bytes",
            registry=self.registry
        )
        
        self.current_confidence = Gauge(
            f"{prefix}_current_confidence",
            "Confianza actual del agente en última decisión",
            registry=self.registry
        )


class MetricsCollector:
    """
    Recolector centralizado de métricas para el sistema multi-agente.
    """
    
    def __init__(self, push_gateway: str = "localhost:9091", 
                 job_name: str = "multi_agent_system"):
        self.push_gateway = push_gateway
        self.job_name = job_name
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.aggregated_metrics = AggregatedMetrics(AGENT_REGISTRY)
        self._lock = threading.Lock()
    
    def get_agent_metrics(self, agent_name: str) -> AgentMetrics:
        """Obtiene o crea métricas para un agente específico."""
        with self._lock:
            if agent_name not in self.agent_metrics:
                self.agent_metrics[agent_name] = AgentMetrics(agent_name)
            return self.agent_metrics[agent_name]
    
    def record_task_start(self, agent_name: str, task_type: str, task_id: str):
        """Registra el inicio de una tarea."""
        metrics = self.get_agent_metrics(agent_name)
        metrics.tasks_total.labels(task_type=task_type).inc()
        metrics.active_tasks.inc()
        return time.time()
    
    def record_task_end(self, agent_name: str, task_type: str, 
                       start_time: float, success: bool = True,
                       error_type: Optional[str] = None):
        """Registra el fin de una tarea."""
        metrics = self.get_agent_metrics(agent_name)
        duration = time.time() - start_time
        
        metrics.task_duration_seconds.labels(task_type=task_type).observe(duration)
        metrics.active_tasks.dec()
        
        if success:
            metrics.tasks_success.labels(task_type=task_type).inc()
        else:
            metrics.tasks_failed.labels(task_type=task_type, error_type=error_type or "unknown").inc()
    
    def record_llm_call(self, agent_name: str, model: str, 
                       latency_seconds: float, prompt_tokens: int,
                       completion_tokens: int, cost_dollars: float,
                       success: bool = True, error_type: Optional[str] = None):
        """Registra una llamada a LLM."""
        metrics = self.get_agent_metrics(agent_name)
        
        status = "success" if success else "error"
        metrics.llm_calls_total.labels(model=model, status=status).inc()
        
        if success:
            metrics.llm_latency_seconds.labels(model=model).observe(latency_seconds)
            metrics.llm_tokens_total.labels(model=model, token_type="prompt").observe(prompt_tokens)
            metrics.llm_tokens_total.labels(model=model, token_type="completion").observe(completion_tokens)
            metrics.llm_cost_dollars.labels(model=model).observe(cost_dollars)
            
            # Calcular uso de context window
            context_usage = (prompt_tokens + completion_tokens) / 128000  # Asumiendo 128k contexto
            metrics.context_window_usage.labels(model=model).observe(context_usage)
        else:
            metrics.llm_errors.labels(model=model, error_type=error_type or "unknown").inc()
    
    def record_tool_execution(self, agent_name: str, tool_name: str,
                             duration_seconds: float, success: bool = True,
                             error_type: Optional[str] = None):
        """Registra ejecución de herramienta."""
        metrics = self.get_agent_metrics(agent_name)
        
        status = "success" if success else "error"
        metrics.tool_calls_total.labels(tool_name=tool_name, status=status).inc()
        
        if success:
            metrics.tool_execution_seconds.labels(tool_name=tool_name).observe(duration_seconds)
        else:
            metrics.tool_errors.labels(tool_name=tool_name, error_type=error_type or "unknown").inc()
    
    def record_delegation(self, agent_name: str, target_agent: str, reason: str):
        """Registra una delegación."""
        metrics = self.get_agent_metrics(agent_name)
        metrics.delegations_total.labels(target_agent=target_agent, reason=reason).inc()
    
    def record_escalation(self, agent_name: str, reason: str):
        """Registra una escalación a humano."""
        metrics = self.get_agent_metrics(agent_name)
        metrics.escalations_to_human.labels(reason=reason).inc()
    
    def update_queue_depth(self, agent_name: str, depth: int):
        """Actualiza la profundidad de cola."""
        metrics = self.get_agent_metrics(agent_name)
        metrics.queue_depth.set(depth)
    
    def update_memory_usage(self, agent_name: str, bytes_used: int):
        """Actualiza uso de memoria."""
        metrics = self.get_agent_metrics(agent_name)
        metrics.memory_usage_bytes.set(bytes_used)
    
    def push_metrics(self):
        """Envía métricas al PushGateway de Prometheus."""
        try:
            push_to_gateway(
                self.push_gateway,
                job=self.job_name,
                registry=AGENT_REGISTRY
            )
        except Exception as e:
            print(f"Error pushing metrics: {e}")


@dataclass
class AggregatedMetrics:
    """
    Métricas agregadas a nivel de sistema.
    """
    registry: CollectorRegistry
    
    # Contadores agregados
    system_tasks_total: Counter = field(init=False)
    system_llm_cost_total: Counter = field(init=False)
    system_delegations_total: Counter = field(init=False)
    
    # Gauges agregados
    total_active_agents: Gauge = field(init=False)
    system_health_score: Gauge = field(init=False)
    
    def __post_init__(self):
        self.system_tasks_total = Counter(
            "system_tasks_total",
            "Tareas totales procesadas por el sistema",
            registry=self.registry
        )
        
        self.system_llm_cost_total = Counter(
            "system_llm_cost_total_dollars",
            "Costo total de LLM en USD",
            registry=self.registry
        )
        
        self.system_delegations_total = Counter(
            "system_delegations_total",
            "Delegaciones totales en el sistema",
            ["source_agent"],
            registry=self.registry
        )
        
        self.total_active_agents = Gauge(
            "system_total_active_agents",
            "Número total de agentes activos",
            registry=self.registry
        )
        
        self.system_health_score = Gauge(
            "system_health_score",
            "Puntuación de salud del sistema (0-100)",
            registry=self.registry
        )


def measure_latency(metric: Histogram, labels: Dict[str, str] = None):
    """Decorador para medir latencia de funciones."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start
                if labels:
                    metric.labels(**labels).observe(duration)
                else:
                    metric.observe(duration)
        return wrapper
    return decorator


# Ejemplo de uso
if __name__ == "__main__":
    collector = MetricsCollector(push_gateway="localhost:9091")
    
    # Registrar inicio de tarea
    start_time = collector.record_task_start("orchestrator", "code_review", "task-001")
    
    # Simular llamada LLM
    collector.record_llm_call(
        agent_name="orchestrator",
        model="gpt-4-turbo",
        latency_seconds=1.5,
        prompt_tokens=500,
        completion_tokens=800,
        cost_dollars=0.025
    )
    
    # Simular ejecución de herramienta
    collector.record_tool_execution(
        agent_name="orchestrator",
        tool_name="git_analyzer",
        duration_seconds=0.5,
        success=True
    )
    
    # Simular delegación
    collector.record_delegation(
        agent_name="orchestrator",
        target_agent="code-reviewer",
        reason="specialized_task"
    )
    
    # Registrar fin de tarea
    collector.record_task_end("orchestrator", "code_review", start_time, success=True)
    
    # Actualizar métricas de sistema
    collector.agent_metrics["orchestrator"].queue_depth.set(5)
    collector.agent_metrics["orchestrator"].memory_usage_bytes.set(512 * 1024 * 1024)
    
    # Push a Prometheus
    collector.push_metrics()
```

---

## 5. Dashboards Operativos

### 5.1 Arquitectura de Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA DE DASHBOARD MULTI-LEVEL                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                         ┌─────────────────────────┐                        │
│                         │    EXECUTIVE DASHBOARD   │                        │
│                         │    (Nivel C-Suite)       │                        │
│                         │                         │                        │
│                         │  • SLA Compliance %     │                        │
│                         │  • Cost per Transaction  │                        │
│                         │  • Agent Utilization     │                        │
│                         │  • Customer Satisfaction │                        │
│                         └────────────┬────────────┘                        │
│                                      │                                      │
│                                      ▼                                      │
│                         ┌─────────────────────────┐                        │
│                         │   OPERATIONS DASHBOARD  │                        │
│                         │   (Nivel NOC/SRE)       │                        │
│                         │                         │                        │
│                         │  • Error Rates          │                        │
│                         │  • Latency P50/P95/P99  │                        │
│                         │  • Throughput            │                        │
│                         │  • Active Incidents      │                        │
│                         └────────────┬────────────┘                        │
│                                      │                                      │
│                                      ▼                                      │
│                         ┌─────────────────────────┐                        │
│                         │    AGENT DEBUGGER       │                        │
│                         │   (Nivel Developer)     │                        │
│                         │                         │                        │
│                         │  • Individual Traces    │                        │
│                         │  • Decision Trees       │                        │
│                         │  • LLM Interactions      │                        │
│                         │  • Memory State         │                        │
│                         └─────────────────────────┘                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Configuración de Grafana Dashboard

```yaml
# grafana_dashboard_agents.json
{
  "annotations": {
    "list": []
  },
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": null,
  "links": [],
  "liveNow": false,
  "panels": [
    {
      "gridPos": {"h": 4, "w": 6, "x": 0, "y": 0},
      "id": 1,
      "title": "Total Tasks",
      "type": "stat",
      "targets": [
        {
          "expr": "sum(increase(system_tasks_total[24h]))",
          "legendFormat": "Tasks (24h)"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "palette-classic"},
          "unit": "short",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "green", "value": null},
              {"color": "yellow", "value": 1000},
              {"color": "red", "value": 5000}
            ]
          }
        }
      }
    },
    {
      "gridPos": {"h": 4, "w": 6, "x": 6, "y": 0},
      "id": 2,
      "title": "LLM Cost (24h)",
      "type": "stat",
      "targets": [
        {
          "expr": "sum(increase(system_llm_cost_total_dollars[24h]))",
          "legendFormat": "Cost USD"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "currencyUSD",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "green", "value": null},
              {"color": "yellow", "value": 100},
              {"color": "red", "value": 500}
            ]
          }
        }
      }
    },
    {
      "gridPos": {"h": 4, "w": 6, "x": 12, "y": 0},
      "id": 3,
      "title": "Error Rate",
      "type": "gauge",
      "targets": [
        {
          "expr": "sum(rate(system_tasks_failed_total[5m])) / sum(rate(system_tasks_total[5m])) * 100"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percent",
          "max": 100,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "green", "value": null},
              {"color": "yellow", "value": 1},
              {"color": "red", "value": 5}
            ]
          }
        }
      }
    },
    {
      "gridPos": {"h": 4, "w": 6, "x": 18, "y": 0},
      "id": 4,
      "title": "Avg Latency",
      "type": "stat",
      "targets": [
        {
          "expr": "histogram_quantile(0.50, sum(rate(agent_orchestrator_task_duration_seconds_bucket[5m])) by (le))"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "s"
        }
      }
    },
    {
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 4},
      "id": 5,
      "title": "Tasks Over Time",
      "type": "timeseries",
      "targets": [
        {
          "expr": "sum(rate(system_tasks_total[5m])) by (task_type)",
          "legendFormat": "{{task_type}}"
        }
      ]
    },
    {
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 4},
      "id": 6,
      "title": "LLM Latency Distribution",
      "type": "histogram",
      "targets": [
        {
          "expr": "sum(rate(agent_orchestrator_llm_latency_seconds_bucket[5m])) by (le)"
        }
      ]
    },
    {
      "gridPos": {"h": 8, "w": 8, "x": 0, "y": 12},
      "id": 7,
      "title": "Agent Utilization",
      "type": "bargauge",
      "targets": [
        {
          "expr": "agent_orchestrator_active_tasks"
        }
      ]
    },
    {
      "gridPos": {"h": 8, "w": 8, "x": 8, "y": 12},
      "id": 8,
      "title": "Cost by Model",
      "type": "piechart",
      "targets": [
        {
          "expr": "sum(increase(agent_orchestrator_llm_cost_dollars_bucket[24h])) by (model)"
        }
      ]
    },
    {
      "gridPos": {"h": 8, "w": 8, "x": 16, "y": 12},
      "id": 9,
      "title": "Delegation Flow",
      "type": "sankey",
      "targets": [
        {
          "expr": "sum(increase(system_delegations_total[24h])) by (source_agent, target_agent)"
        }
      ]
    }
  ],
  "refresh": "10s",
  "schemaVersion": 38,
  "style": "dark",
  "tags": ["agents", "observability"],
  "templating": {
    "list": [
      {
        "name": "agent",
        "type": "query",
        "query": "label_values(agent_active_tasks, agent_name)"
      }
    ]
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "title": "Multi-Agent System Overview",
  "uid": "multi-agent-overview",
  "version": 1
}
```

---

## 6. Tecnologías de Observabilidad

### 6.1 Stack Completo

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         STACK DE OBSERVABILIDAD COMPLETO                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         INSTRUMENTATION                                 │ │
│  │                                                                         │ │
│  │   OpenTelemetry SDK ─────► Auto-instrumentation ─────► Custom Spans   │ │
│  │        │                         │                        │           │ │
│  │        ▼                         ▼                        ▼           │ │
│  │   OTLP Exporter ─────────── OTLP Exporter ───────── OTLP Exporter     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                       │
│                                      ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         COLLECTION LAYER                               │ │
│  │                                                                         │ │
│  │        ┌─────────────┐     ┌─────────────┐     ┌─────────────┐        │ │
│  │        │   Jaeger    │     │ Prometheus  │     │    Loki     │        │ │
│  │        │  (Traces)   │     │  (Metrics)  │     │   (Logs)    │        │ │
│  │        └──────┬──────┘     └──────┬──────┘     └──────┬──────┘        │ │
│  └────────────────┼──────────────────┼──────────────────┼───────────────┘ │
│                   │                  │                  │                  │
│                   ▼                  ▼                  ▼                  │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         STORAGE BACKEND                                │ │
│  │                                                                         │ │
│  │        ┌─────────────┐     ┌─────────────┐     ┌─────────────┐        │ │
│  │        │ Elasticsearch│     │ Prometheus  │     │   MinIO/S3  │        │ │
│  │        │             │     │  TSDB       │     │             │        │ │
│  │        └─────────────┘     └─────────────┘     └─────────────┘        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                       │
│                                      ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         VISUALIZATION                                  │ │
│  │                                                                         │ │
│  │   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐     │ │
│  │   │  Grafana  │   │   Kibana  │   │   Jaeger  │   │  Tempo    │     │ │
│  │   │           │   │           │   │   UI      │   │           │     │ │
│  │   └───────────┘   └───────────┘   └───────────┘   └───────────┘     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Configuración de OpenTelemetry Collector

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

  prometheus:
    config:
      scrape_configs:
        - job_name: 'agent-metrics'
          scrape_interval: 15s
          static_configs:
            - targets: ['localhost:9090']

processors:
  batch:
    timeout: 10s
    send_batch_size: 1024

  memory_limiter:
    check_interval: 1s
    limit_mib: 512
    spike_limit_mib: 128

  resource:
    attributes:
      - action: upsert
        key: service.namespace
        value: "multi-agent-system"
      - action: upsert
        key: deployment.environment
        value: "${DEPLOYMENT_ENV:development}"

  k8sattributes:
    auth_type: "serviceAccount"
    passthrough: false

exporters:
  otlp/traces:
    endpoint: "${JAEGER_ENDPOINT:localhost:4317}"
    tls:
      insecure: true

  prometheus:
    endpoint: "0.0.0.0:8889"
    namespace: "otel"
    const_labels:
      service: multi-agent

  loki:
    endpoint: "http://localhost:3100/loki/api/v1/push"
    labels:
      attributes:
        service.name: ""

  elasticsearch:
    endpoints: ["http://localhost:9200"]
    logs_index: "agent-logs-{.%Y.%m.%d}"
    traces_index: "agent-traces-{.%Y.%m.%d}"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, resource, k8sattributes]
      exporters: [otlp/traces, elasticsearch]
    
    metrics:
      receivers: [prometheus]
      processors: [memory_limiter, batch, resource]
      exporters: [prometheus, elasticsearch]
    
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch, resource, k8sattributes]
      exporters: [loki, elasticsearch]

  telemetry:
    logs:
      level: "info"
    metrics:
      address: "localhost:8888"
```

---

## 7. Ejercicios Prácticos Resueltos

### Ejercicio 1: Implementación de Logging Correlacionado

```python
# ejercicio_1_correlated_logging.py
"""
EJERCICIO: Implementar sistema de logging correlacionado para multi-agente
"""

import logging
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from contextlib import contextmanager
import threading

# ============================================================
# SOLUCIÓN: Sistema de Logging Correlacionado
# ============================================================

class CorrelationContext:
    """Contexto de correlación para trazas distribuidas."""
    
    _local = threading.local()
    
    @classmethod
    def get_trace_id(cls) -> str:
        return getattr(cls._local, 'trace_id', None)
    
    @classmethod
    def set_trace_id(cls, trace_id: str):
        cls._local.trace_id = trace_id
    
    @classmethod
    def get_span_id(cls) -> str:
        return getattr(cls._local, 'span_id', None)
    
    @classmethod
    def set_span_id(cls, span_id: str):
        cls._local.span_id = span_id
    
    @classmethod
    def get_agent_id(cls) -> str:
        return getattr(cls._local, 'agent_id', None)
    
    @classmethod
    def set_agent_id(cls, agent_id: str):
        cls._local.agent_id = agent_id


@dataclass
class StructuredLogEntry:
    """Entrada de log estructurada."""
    timestamp: str
    level: str
    trace_id: Optional[str]
    span_id: Optional[str]
    agent_id: Optional[str]
    service: str
    operation: str
    message: str
    context: Dict[str, Any] = field(default_factory=dict)
    error: Optional[Dict[str, Any]] = None
    
    def to_json(self) -> str:
        return json.dumps(self.__dict__, default=str, ensure_ascii=False)


class CorrelatedLogger:
    """
    Logger con soporte para correlación de trazas.
    
    Permite seguir el flujo de ejecución a través de múltiples
    agentes y servicios mediante trace_ids y span_ids.
    """
    
    def __init__(self, service_name: str, output_file: Optional[str] = None):
        self.service_name = service_name
        self.output_file = output_file
        self._lock = threading.Lock()
        
        # Configurar logging de Python para errores no manejados
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(message)s'
        )
        self.logger = logging.getLogger(service_name)
    
    def _create_entry(self, level: str, operation: str, message: str,
                     context: Optional[Dict] = None, 
                     error: Optional[Exception] = None) -> StructuredLogEntry:
        """Crea una entrada de log estructurada."""
        
        error_dict = None
        if error:
            error_dict = {
                "type": type(error).__name__,
                "message": str(error),
                "traceback": self._format_traceback(error)
            }
        
        return StructuredLogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            level=level,
            trace_id=CorrelationContext.get_trace_id(),
            span_id=CorrelationContext.get_span_id(),
            agent_id=CorrelationContext.get_agent_id(),
            service=self.service_name,
            operation=operation,
            message=message,
            context=context or {},
            error=error_dict
        )
    
    def _format_traceback(self, error: Exception) -> str:
        import traceback
        return ''.join(traceback.format_exception(type(error), error, error.__traceback__))
    
    def _emit(self, entry: StructuredLogEntry):
        """Emite el log a stdout y opcionalmente a archivo."""
        json_line = entry.to_json()
        
        # stdout
        print(json_line)
        
        # archivo si está configurado
        if self.output_file:
            with self._lock:
                with open(self.output_file, 'a', encoding='utf-8') as f:
                    f.write(json_line + '\n')
    
    def debug(self, operation: str, message: str, **context):
        entry = self._create_entry("DEBUG", operation, message, context)
        self._emit(entry)
    
    def info(self, operation: str, message: str, **context):
        entry = self._create_entry("INFO", operation, message, context)
        self._emit(entry)
    
    def warning(self, operation: str, message: str, **context):
        entry = self._create_entry("WARNING", operation, message, context)
        self._emit(entry)
    
    def error(self, operation: str, message: str, error: Optional[Exception] = None, **context):
        entry = self._create_entry("ERROR", operation, message, context, error)
        self._emit(entry)
    
    @contextmanager
    def span(self, operation: str, agent_id: Optional[str] = None, 
            parent_trace_id: Optional[str] = None):
        """
        Crea un contexto de span para seguimiento de operaciones.
        
        Usage:
            with logger.span("process_order", agent_id="order-agent") as span:
                span.set("order_id", "12345")
                # ... operations ...
        """
        # Generar o usar trace_id existente
        if parent_trace_id:
            CorrelationContext.set_trace_id(parent_trace_id)
        elif not CorrelationContext.get_trace_id():
            CorrelationContext.set_trace_id(str(uuid.uuid4()))
        
        # Generar nuevo span_id
        span_id = str(uuid.uuid4())[:8]
        CorrelationContext.set_span_id(span_id)
        
        if agent_id:
            CorrelationContext.set_agent_id(agent_id)
        
        self.info(operation, f"Span started: {span_id}", 
                 parent_trace=parent_trace_id)
        
        start_time = datetime.now(timezone.utc)
        
        try:
            yield SpanContext(self, operation)
        except Exception as e:
            self.error(operation, f"Span failed: {span_id}", error=e)
            raise
        finally:
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            self.info(operation, f"Span completed: {span_id}",
                    duration_seconds=duration)
            CorrelationContext.set_span_id(None)
    
    def log_agent_action(self, action: str, target: str, 
                        params: Dict, result: Optional[Dict] = None,
                        error: Optional[Exception] = None):
        """Registra una acción específica de agente."""
        context = {
            "action_type": "agent_action",
            "action": action,
            "target": target,
            "params": params
        }
        
        if result:
            context["result"] = result
        
        if error:
            self.error("agent_action", f"Action failed: {action}", 
                      error=error, **context)
        else:
            self.info("agent_action", f"Action completed: {action}", **context)


class SpanContext:
    """Contexto de span para agregar información."""
    
    def __init__(self, logger: CorrelatedLogger, operation: str):
        self.logger = logger
        self.operation = operation
        self.attributes: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any):
        """Establece un atributo en el span."""
        self.attributes[key] = value
        self.logger.debug(self.operation, f"Span attribute set: {key}={value}")
    
    def set_multiple(self, **kwargs):
        """Establece múltiples atributos."""
        for key, value in kwargs.items():
            self.set(key, value)


# ============================================================
# EJEMPLO DE USO
# ============================================================

if __name__ == "__main__":
    # Crear logger
    logger = CorrelatedLogger("orchestrator-agent", output_file="logs/orchestrator.jsonl")
    
    # Establecer contexto de agente
    CorrelationContext.set_agent_id("orchestrator-001")
    
    # Iniciar traza principal
    with logger.span("process_user_request", agent_id="orchestrator-001") as span:
        span.set("request_id", "req-12345")
        span.set("user_id", "user-67890")
        
        # Simular procesamiento
        logger.log_agent_action(
            action="analyze_intent",
            target="nlp-processor",
            params={"text": "¿Cuál es el estado de mi pedido?"},
            result={"intent": "query_order_status", "confidence": 0.95}
        )
        
        # Crear sub-span para llamada LLM
        with logger.span("call_llm", parent_trace_id=CorrelationContext.get_trace_id()) as llm_span:
            llm_span.set("model", "gpt-4-turbo")
            llm_span.set("tokens_in", 150)
            llm_span.set("tokens_out", 80)
            logger.info("llm_call", "LLM request completed", duration_ms=1250)
        
        # Delegar a otro agente
        with logger.span("delegate_to_specialist", parent_trace_id=CorrelationContext.get_trace_id()) as del_span:
            del_span.set("target_agent", "order-status-agent")
            del_span.set("task_type", "order_inquiry")
            
            logger.log_agent_action(
                action="delegate",
                target="order-status-agent",
                params={"order_id": "ORD-12345"}
            )
        
        # Completar procesamiento
        span.set("result_status", "success")
    
    print("\n" + "="*60)
    print("Logs generados. Busca el trace_id en todos los entries.")
    print("="*60)
```

### Ejercicio 2: Dashboard Prometheus + Grafana

```python
# ejercicio_2_dashboard_setup.py
"""
EJERCICIO: Configurar dashboard de Grafana para monitoreo de agentes
"""

import subprocess
import json
from typing import Dict, List

# ============================================================
# PARTE 1: Generar queries Prometheus optimizadas
# ============================================================

class PrometheusQueries:
    """Colección de queries Prometheus para métricas de agentes."""
    
    @staticmethod
    def task_success_rate(agent_name: str, window: str = "5m") -> str:
        """
        Calcula tasa de éxito de tareas para un agente.
        
        Returns:
            Query Prometheus que retorna porcentaje de éxito
        """
        return f'''
        (
            sum(rate({agent_name}_tasks_success_total[{window}]))
            /
            sum(rate({agent_name}_tasks_total[{window}]))
        ) * 100
        '''
    
    @staticmethod
    def p95_latency(agent_name: str, metric: str = "task_duration_seconds") -> str:
        """
        Calcula latencia P95 para un agente.
        
        Returns:
            Query Prometheus para percentil 95
        """
        return f'''
        histogram_quantile(0.95, 
            sum(rate({agent_name}_{metric}_bucket[5m])) by (le)
        )
        '''
    
    @staticmethod
    def llm_cost_per_task(agent_name: str) -> str:
        """
        Costo promedio de LLM por tarea.
        """
        return f'''
        (
            sum(rate({agent_name}_llm_cost_dollars_sum[1h]))
            /
            sum(rate({agent_name}_tasks_success_total[1h]))
        )
        '''
    
    @staticmethod
    def agent_health_score(agent_name: str) -> str:
        """
        Score de salud compuesto para un agente.
        
        Combina:
        - Tasa de éxito (peso 40%)
        - Latencia P95 vs SLO (peso 30%)
        - Uso de recursos (peso 30%)
        """
        success_rate = PrometheusQueries.task_success_rate(agent_name)
        p95_latency = PrometheusQueries.p95_latency(agent_name)
        
        return f'''
        (
            ({success_rate}) * 0.4
            +
            (100 - ({p95_latency} / 10 * 100)) * 0.3
            +
            (100 - (agent_{agent_name}_memory_usage_bytes / 1000000000 * 100)) * 0.3
        )
        '''
    
    @staticmethod
    def delegation_rate(agent_name: str, window: str = "1h") -> str:
        """Tasa de delegación a otros agentes."""
        return f'''
        sum(rate({agent_name}_delegations_total[{window}]))
        '''
    
    @staticmethod
    def escalation_rate(agent_name: str, window: str = "1h") -> str:
        """Tasa de escalación a humanos."""
        total_tasks = f'sum(rate({agent_name}_tasks_total[{window}]))'
        escalations = f'sum(rate({agent_name}_escalations_human_total[{window}]))'
        
        return f'''
        ({escalations} / {total_tasks}) * 100
        '''


# ============================================================
# PARTE 2: Generar configuración de dashboard
# ============================================================

def generate_grafana_dashboard(agents: List[str]) -> Dict:
    """
    Genera configuración completa de dashboard de Grafana
    para múltiples agentes.
    """
    
    dashboard = {
        "annotations": {"list": []},
        "editable": True,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 0,
        "id": None,
        "links": [],
        "liveNow": False,
        "panels": [],
        "refresh": "30s",
        "schemaVersion": 38,
        "style": "dark",
        "tags": ["multi-agent", "observability"],
        "templating": {
            "list": [
                {
                    "name": "Agent",
                    "type": "query",
                    "query": f'label_values({agents[0]}_active_tasks, agent_name)',
                    "refresh": 1
                }
            ]
        },
        "time": {"from": "now-1h", "to": "now"},
        "title": "Multi-Agent System Monitor",
        "uid": "multi-agent-monitor",
        "version": 1,
        "variables": []
    }
    
    # Panel 1: Health Score Overview
    dashboard["panels"].append({
        "title": "Agent Health Scores",
        "type": "gauge",
        "gridPos": {"h": 6, "w": 8, "x": 0, "y": 0},
        "targets": [
            {
                "expr": PrometheusQueries.agent_health_score("${Agent}"),
                "legendFormat": "${Agent}"
            }
        ],
        "fieldConfig": {
            "defaults": {
                "max": 100,
                "min": 0,
                "thresholds": {
                    "mode": "absolute",
                    "steps": [
                        {"color": "red", "value": None},
                        {"color": "yellow", "value": 60},
                        {"color": "green", "value": 80}
                    ]
                },
                "unit": "none"
            }
        }
    })
    
    # Panel 2: Task Success Rate
    dashboard["panels"].append({
        "title": "Task Success Rate",
        "type": "timeseries",
        "gridPos": {"h": 6, "w": 8, "x": 8, "y": 0},
        "targets": [
            {
                "expr": PrometheusQueries.task_success_rate("${Agent}"),
                "legendFormat": "Success Rate %"
            }
        ],
        "fieldConfig": {
            "defaults": {
                "unit": "percent",
                "custom": {"lineWidth": 2},
                "thresholds": {
                    "mode": "absolute",
                    "steps": [
                        {"color": "red", "value": None},
                        {"color": "yellow", "value": 90},
                        {"color": "green", "value": 95}
                    ]
                }
            }
        }
    })
    
    # Panel 3: Latency Distribution
    dashboard["panels"].append({
        "title": "Latency Distribution (P50/P95/P99)",
        "type": "timeseries",
        "gridPos": {"h": 6, "w": 8, "x": 16, "y": 0},
        "targets": [
            {
                "expr": f'histogram_quantile(0.50, sum(rate(${{Agent}}_task_duration_seconds_bucket[5m])) by (le))',
                "legendFormat": "P50"
            },
            {
                "expr": f'histogram_quantile(0.95, sum(rate(${{Agent}}_task_duration_seconds_bucket[5m])) by (le))',
                "legendFormat": "P95"
            },
            {
                "expr": f'histogram_quantile(0.99, sum(rate(${{Agent}}_task_duration_seconds_bucket[5m])) by (le))',
                "legendFormat": "P99"
            }
        ],
        "fieldConfig": {
            "defaults": {
                "unit": "s",
                "custom": {"lineWidth": 2}
            }
        }
    })
    
    # Panel 4: LLM Cost Tracking
    dashboard["panels"].append({
        "title": "LLM Cost Over Time",
        "type": "timeseries",
        "gridPos": {"h": 6, "w": 12, "x": 0, "y": 6},
        "targets": [
            {
                "expr": f'sum(rate(${{Agent}}_llm_cost_dollars_sum[1h]))',
                "legendFormat": "Cost/hour"
            }
        ],
        "fieldConfig": {
            "defaults": {
                "unit": "currencyUSD"
            }
        }
    })
    
    # Panel 5: Token Usage
    dashboard["panels"].append({
        "title": "Token Usage",
        "type": "timeseries",
        "gridPos": {"h": 6, "w": 12, "x": 12, "y": 6},
        "targets": [
            {
                "expr": f'sum(rate(${{Agent}}_llm_tokens_total_sum[1h])) by (token_type)',
                "legendFormat": "{{token_type}}"
            }
        ],
        "fieldConfig": {
            "defaults": {
                "unit": "short"
            }
        }
    })
    
    # Panel 6: Delegations and Escalations
    dashboard["panels"].append({
        "title": "Delegations vs Escalations",
        "type": "timeseries",
        "gridPos": {"h": 6, "w": 12, "x": 0, "y": 12},
        "targets": [
            {
                "expr": PrometheusQueries.delegation_rate("${Agent}"),
                "legendFormat": "Delegations"
            },
            {
                "expr": PrometheusQueries.escalation_rate("${Agent}"),
                "legendFormat": "Escalations %"
            }
        ]
    })
    
    # Panel 7: Resource Usage
    dashboard["panels"].append({
        "title": "Resource Usage",
        "type": "gauge",
        "gridPos": {"h": 6, "w": 6, "x": 12, "y": 12},
        "targets": [
            {
                "expr": f'${{Agent}}_memory_usage_bytes / 1073741824',
                "legendFormat": "Memory (GB)"
            }
        ],
        "fieldConfig": {
            "defaults": {
                "unit": "bytes",
                "max": 8
            }
        }
    })
    
    # Panel 8: Queue Depth
    dashboard["panels"].append({
        "title": "Queue Depth",
        "type": "gauge",
        "gridPos": {"h": 6, "w": 6, "x": 18, "y": 12},
        "targets": [
            {
                "expr": f'${{Agent}}_queue_depth',
                "legendFormat": "Pending Tasks"
            }
        ]
    })
    
    return dashboard


# ============================================================
# EJEMPLO DE USO
# ============================================================

if __name__ == "__main__":
    # Definir agentes en el sistema
    agents = [
        "orchestrator",
        "code-reviewer", 
        "documentation-agent",
        "test-agent"
    ]
    
    # Generar dashboard
    dashboard = generate_grafana_dashboard(agents)
    
    # Guardar como JSON
    with open("grafana_dashboard_agents.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    
    print("Dashboard generado: grafana_dashboard_agents.json")
    print("\n" + "="*60)
    print("QUERY EJEMPLO - Health Score:")
    print(PrometheusQueries.agent_health_score("orchestrator"))
    print("\n" + "="*60)
    print("QUERY EJEMPLO - Task Success Rate:")
    print(PrometheusQueries.task_success_rate("orchestrator"))
```

---

## 8. Actividades de Laboratorio

### Laboratorio 1: Instrumentación Completa de un Agente

**Duración**: 90 minutos

**Objetivo**: Instrumentar un agente existente con logging, tracing y métricas.

**Pasos**:

1. **Configurar OpenTelemetry** (20 min)
   - Instalar dependencias
   - Configurar collector
   - Crear configuración base

2. **Implementar Logging Estructurado** (30 min)
   - Crear clase AgentLogger
   - Agregar contexto de correlación
   - Configurar output a Elasticsearch

3. **Agregar Distributed Tracing** (30 min)
   - Instrumentar puntos de decisión
   - Propagar trazas entre agentes
   - Visualizar en Jaeger

4. **Configurar Métricas Prometheus** (30 min)
   - Definir métricas custom
   - Configurar histogramas
   - Crear alerts

**Entregable**: Agente completamente instrumentado con dashboard funcional.

### Laboratorio 2: Construir Dashboard Operativo

**Duración**: 90 minutos

**Objetivo**: Crear dashboard de Grafana para monitoreo del sistema multi-agente.

**Pasos**:

1. **Configurar Fuentes de Datos** (15 min)
   - Conectar Prometheus
   - Conectar Loki
   - Conectar Jaeger

2. **Crear Paneles de Salud** (30 min)
   - Health scores
   - Error rates
   - SLI compliance

3. **Construir Vista de Trazas** (30 min)
   - Trace timeline
   - Dependency graph
   - Error correlation

4. **Configurar Alerts** (15 min)
   - Thresholds dinámicos
   - Notificaciones
   - Runbooks

---

## 9. Resumen de Puntos Clave

### Conceptos Fundamentales

1. **Observabilidad = Logs + Metrics + Traces**
   - Los tres pilares son complementarios
   - Cada uno revela diferentes aspectos del sistema

2. **Logging Estructurado**
   - Formato JSON para machine readability
   - Incluir trace_id y span_id en cada entrada
   - Contextos anidados para debugging

3. **Distributed Tracing**
   - W3C Trace Context como estándar
   - Propagación de contexto entre servicios
   - Spans jerárquicos para representar flujo

4. **Métricas de Agentes**
   - Métricas de negocio (tareas, éxito)
   - Métricas técnicas (latencia, errores)
   - Métricas de costos (tokens, LLM)

### Mejores Prácticas

| Área | Práctica | Beneficio |
|------|----------|----------|
| Logging | Correlación con trace_id | Debugging distribuido |
| Logging | Sampling inteligente | Reducir volumen |
| Traces | Span naming consistente | Análisis automatizado |
| Traces | Atributos ricos | Queries avanzados |
| Metrics | Histogramas para latencia | Percentiles exactos |
| Metrics | Labels de alta cardinalidad | Segmentación detallada |

### Herramientas Clave

- **OpenTelemetry**: Estándar abierto para instrumentación
- **Prometheus**: Colección de métricas
- **Grafana**: Visualización
- **Jaeger**: Distributed tracing
- **Loki/Elasticsearch**: Agregación de logs

---

## 10. Referencias Externas

1. **OpenTelemetry Documentation**
   https://opentelemetry.io/docs/

2. **Prometheus Query Language (PromQL)**
   https://prometheus.io/docs/prometheus/latest/querying/basics/

3. **Grafana Dashboard Best Practices**
   https://grafana.com/docs/grafana/latest/dashboards/

4. **Distributed Tracing with OpenTelemetry**
   https://opentelemetry.io/docs/concepts/observability-tutorial/

5. **The RED Method (Rate, Errors, Duration)**
   https://thenewstack.io/monitoring-microservices-red-method/

6. **Google SRE Book - Monitoring Distributed Systems**
   https://sre.google/sre-book/monitoring-distributed-systems/

7. **OpenTelemetry Collector Configuration**
   https://opentelemetry.io/docs/collector/configuration/

8. **Prometheus Histograms and Summaries**
   https://prometheus.io/docs/practices/histograms/

---

**Fin de la Clase 9**
