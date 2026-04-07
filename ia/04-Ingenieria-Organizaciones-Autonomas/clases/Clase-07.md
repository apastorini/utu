# Clase 7: Capas de Abstracción para Agentes

## Duración
4 horas (240 minutos)

## Objetivos de Aprendizaje
- Implementar el patrón Adapter para abstraer sistemas externos
- Diseñar capas ORM para datos legacy
- Integrar message queues para comunicación asíncrona
- Construir sistemas de manejo de errores robustos
- Crear abstracciones reutilizables para agentes

## Contenidos Detallados

### 7.1 Adapter Pattern (75 minutos)

El patrón Adapter es fundamental para crear abstracciones entre los agentes y los sistemas externos. Permite cambiar implementaciones sin modificar el código del agente.

#### 7.1.1 Implementación del Patrón

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ExternalSystemAdapter(ABC):
    """Interfaz base para adapters de sistemas externos"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establece conexión con el sistema"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """Cierra la conexión"""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Verifica el estado de conexión"""
        pass
    
    @abstractmethod
    def execute(self, operation: str, params: Dict) -> Any:
        """Ejecuta una operación"""
        pass


@dataclass
class OperationResult:
    """Resultado de una operación"""
    success: bool
    data: Any = None
    error: str = None
    execution_time: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class BaseAdapter(ExternalSystemAdapter):
    """Clase base para adapters"""
    
    def __init__(self, config: Dict):
        self.config = config
        self._connected = False
        self._connection_time: Optional[datetime] = None
        self._operation_count = 0
    
    def connect(self) -> bool:
        self._connected = True
        self._connection_time = datetime.now()
        logger.info(f"{self.__class__.__name__} connected")
        return True
    
    def disconnect(self):
        self._connected = False
        logger.info(f"{self.__class__.__name__} disconnected")
    
    def is_connected(self) -> bool:
        return self._connected
    
    def execute(self, operation: str, params: Dict) -> OperationResult:
        """Ejecuta operación con logging y manejo de errores"""
        
        start_time = datetime.now()
        
        try:
            result = self._execute_operation(operation, params)
            
            self._operation_count += 1
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return OperationResult(
                success=True,
                data=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            logger.error(f"Operation {operation} failed: {e}")
            
            return OperationResult(
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    @abstractmethod
    def _execute_operation(self, operation: str, params: Dict) -> Any:
        """Implementación específica de la operación"""
        pass
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del adapter"""
        return {
            "connected": self._connected,
            "connection_time": self._connection_time,
            "operation_count": self._operation_count
        }
```

#### 7.1.2 Adapter Composite

```python
from typing import Dict, List


class AdapterComposite:
    """Compuesto de adapters para múltiples sistemas"""
    
    def __init__(self):
        self.adapters: Dict[str, ExternalSystemAdapter] = {}
    
    def register_adapter(self, name: str, adapter: ExternalSystemAdapter):
        """Registra un adapter"""
        self.adapters[name] = adapter
        logger.info(f"Registered adapter: {name}")
    
    def unregister_adapter(self, name: str):
        """Desregistra un adapter"""
        if name in self.adapters:
            adapter = self.adapters[name]
            adapter.disconnect()
            del self.adapters[name]
            logger.info(f"Unregistered adapter: {name}")
    
    def get_adapter(self, name: str) -> Optional[ExternalSystemAdapter]:
        """Obtiene un adapter por nombre"""
        return self.adapters.get(name)
    
    def connect_all(self) -> Dict[str, bool]:
        """Conecta todos los adapters"""
        results = {}
        
        for name, adapter in self.adapters.items():
            try:
                results[name] = adapter.connect()
            except Exception as e:
                logger.error(f"Failed to connect adapter {name}: {e}")
                results[name] = False
        
        return results
    
    def disconnect_all(self):
        """Desconecta todos los adapters"""
        for adapter in self.adapters.values():
            adapter.disconnect()
    
    def execute_on(
        self,
        adapter_name: str,
        operation: str,
        params: Dict
    ) -> OperationResult:
        """Ejecuta operación en un adapter específico"""
        
        adapter = self.adapters.get(adapter_name)
        
        if not adapter:
            return OperationResult(
                success=False,
                error=f"Adapter not found: {adapter_name}"
            )
        
        return adapter.execute(operation, params)
    
    def broadcast(self, operation: str, params: Dict) -> Dict[str, OperationResult]:
        """Ejecuta operación en todos los adapters"""
        
        results = {}
        
        for name, adapter in self.adapters.items():
            try:
                results[name] = adapter.execute(operation, params)
            except Exception as e:
                results[name] = OperationResult(
                    success=False,
                    error=str(e)
                )
        
        return results
    
    def get_all_stats(self) -> Dict[str, Dict]:
        """Obtiene estadísticas de todos los adapters"""
        
        stats = {}
        
        for name, adapter in self.adapters.items():
            if hasattr(adapter, 'get_stats'):
                stats[name] = adapter.get_stats()
        
        return stats
```

### 7.2 ORM para Datos Legacy (60 minutos)

#### 7.2.1 Capa de Abstracción de Datos

```python
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, DateTime, MetaData, Text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class LegacyTable(Base):
    """Modelo base para tablas legacy"""
    __abstract__ = True


class CustomerLegacy(LegacyTable):
    """Tabla de clientes legacy"""
    __tablename__ = 'customers_legacy'
    
    id = Column(Integer, primary_key=True)
    customer_number = Column(String(20), unique=True)
    name = Column(String(200))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class OrderLegacy(LegacyTable):
    """Tabla de pedidos legacy"""
    __tablename__ = 'orders_legacy'
    
    id = Column(Integer, primary_key=True)
    order_number = Column(String(20), unique=True)
    customer_id = Column(Integer)
    total_amount = Column(Float)
    status = Column(String(20))
    order_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)


class ProductLegacy(LegacyTable):
    """Tabla de productos legacy"""
    __tablename__ = 'products_legacy'
    
    id = Column(Integer, primary_key=True)
    sku = Column(String(20), unique=True)
    name = Column(String(200))
    description = Column(Text)
    price = Column(Float)
    stock = Column(Integer)
    category = Column(String(50))
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class LegacyORM:
    """Capa ORM para sistemas legacy"""
    
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """Crea las tablas"""
        Base.metadata.create_all(self.engine)
    
    def get_session(self) -> Session:
        """Obtiene una sesión"""
        return self.SessionLocal()
    
    def close(self):
        """Cierra el engine"""
        self.engine.dispose()


class LegacyCustomerRepository:
    """Repositorio para clientes legacy"""
    
    def __init__(self, orm: LegacyORM):
        self.orm = orm
    
    def get_by_id(self, customer_id: int) -> Optional[CustomerLegacy]:
        """Obtiene cliente por ID"""
        
        session = self.orm.get_session()
        
        try:
            return session.query(CustomerLegacy).filter(
                CustomerLegacy.id == customer_id
            ).first()
        finally:
            session.close()
    
    def get_by_customer_number(self, customer_number: str) -> Optional[CustomerLegacy]:
        """Obtiene cliente por número"""
        
        session = self.orm.get_session()
        
        try:
            return session.query(CustomerLegacy).filter(
                CustomerLegacy.customer_number == customer_number
            ).first()
        finally:
            session.close()
    
    def search(self, query: str, limit: int = 50) -> List[CustomerLegacy]:
        """Busca clientes"""
        
        session = self.orm.get_session()
        
        try:
            return session.query(CustomerLegacy).filter(
                CustomerLegacy.name.ilike(f'%{query}%') |
                CustomerLegacy.email.ilike(f'%{query}%') |
                CustomerLegacy.customer_number.ilike(f'%{query}%')
            ).limit(limit).all()
        finally:
            session.close()
    
    def create(self, customer_data: Dict) -> CustomerLegacy:
        """Crea un cliente"""
        
        session = self.orm.get_session()
        
        try:
            customer = CustomerLegacy(
                customer_number=customer_data['customer_number'],
                name=customer_data['name'],
                email=customer_data.get('email'),
                phone=customer_data.get('phone'),
                address=customer_data.get('address')
            )
            
            session.add(customer)
            session.commit()
            session.refresh(customer)
            
            return customer
            
        except Exception as e:
            session.rollback()
            raise
            
        finally:
            session.close()
    
    def update(self, customer_id: int, data: Dict) -> bool:
        """Actualiza un cliente"""
        
        session = self.orm.get_session()
        
        try:
            customer = session.query(CustomerLegacy).filter(
                CustomerLegacy.id == customer_id
            ).first()
            
            if not customer:
                return False
            
            for key, value in data.items():
                if hasattr(customer, key):
                    setattr(customer, key, value)
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            raise
            
        finally:
            session.close()
    
    def delete(self, customer_id: int) -> bool:
        """Elimina un cliente"""
        
        session = self.orm.get_session()
        
        try:
            customer = session.query(CustomerLegacy).filter(
                CustomerLegacy.id == customer_id
            ).first()
            
            if not customer:
                return False
            
            session.delete(customer)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            raise
            
        finally:
            session.close()
```

#### 7.2.2 Mapper entre Modelos

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class CustomerModel:
    """Modelo de dominio para cliente"""
    id: Optional[int]
    customer_number: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class CustomerMapper:
    """Mapper entre modelo legacy y modelo de dominio"""
    
    @staticmethod
    def to_domain(legacy: CustomerLegacy) -> CustomerModel:
        """Convierte modelo legacy a modelo de dominio"""
        
        return CustomerModel(
            id=legacy.id,
            customer_number=legacy.customer_number,
            name=legacy.name,
            email=legacy.email,
            phone=legacy.phone,
            address=legacy.address,
            created_at=legacy.created_at,
            updated_at=legacy.updated_at
        )
    
    @staticmethod
    def to_legacy(domain: CustomerModel) -> Dict:
        """Convierte modelo de dominio a dict para legacy"""
        
        data = {
            'customer_number': domain.customer_number,
            'name': domain.name
        }
        
        if domain.email:
            data['email'] = domain.email
        if domain.phone:
            data['phone'] = domain.phone
        if domain.address:
            data['address'] = domain.address
        
        return data
    
    @staticmethod
    def to_domain_list(legacy_list: List[CustomerLegacy]) -> List[CustomerModel]:
        """Convierte lista de legacy a dominio"""
        
        return [CustomerMapper.to_domain(legacy) for legacy in legacy_list]
```

### 7.3 Message Queues (75 minutos)

#### 7.3.1 RabbitMQ Integration

```python
import pika
import json
import logging
from typing import Callable, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
import threading
import time

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Mensaje para la cola"""
    message_id: str
    queue: str
    payload: Dict
    timestamp: datetime
    headers: Dict = None
    

class RabbitMQClient:
    """Cliente para RabbitMQ"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
        virtual_host: str = "/"
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.virtual_host = virtual_host
        
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Establece conexión"""
        
        credentials = pika.PlainCredentials(self.username, self.password)
        
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.virtual_host,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        logger.info(f"Connected to RabbitMQ at {self.host}:{self.port}")
    
    def close(self):
        """Cierra la conexión"""
        
        if self.connection and self.connection.is_open:
            self.connection.close()
    
    def declare_queue(
        self,
        queue_name: str,
        durable: bool = True,
        exclusive: bool = False,
        auto_delete: bool = False
    ):
        """Declara una cola"""
        
        self.channel.queue_declare(
            queue=queue_name,
            durable=durable,
            exclusive=exclusive,
            auto_delete=auto_delete
        )
    
    def publish(
        self,
        queue_name: str,
        message: Dict,
        exchange: str = "",
        persistent: bool = True
    ):
        """Publica un mensaje"""
        
        properties = pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent if persistent else 1,
            content_type="application/json",
            timestamp=int(time.time())
        )
        
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=queue_name,
            body=json.dumps(message),
            properties=properties
        )
        
        logger.debug(f"Published to {queue_name}")
    
    def consume(
        self,
        queue_name: str,
        callback: Callable[[Dict], bool],
        auto_ack: bool = False
    ):
        """Consume mensajes"""
        
        def on_message(channel, method, properties, body):
            try:
                message = json.loads(body)
                success = callback(message)
                
                if not auto_ack and success:
                    channel.basic_ack(delivery_tag=method.delivery_tag)
                elif not auto_ack and not success:
                    channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                    
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                if not auto_ack:
                    channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message,
            auto_ack=auto_ack
        )
        
        self.channel.start_consuming()
    
    def consume_messages(self, queue_name: str, max_messages: int = None):
        """Consume un número limitado de mensajes"""
        
        messages = []
        
        def callback(message):
            messages.append(message)
            return len(max_messages) is None or len(messages) < max_messages
        
        self.channel.basic_qos(prefetch_count=max_messages or 10)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
        
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        
        return messages


class AgentMessageQueue:
    """Cola de mensajes para agentes"""
    
    def __init__(self, mq_client: RabbitMQClient):
        self.mq = mq_client
        self.queues = {
            "agent_tasks": "agent.tasks",
            "agent_results": "agent.results",
            "agent_errors": "agent.errors"
        }
    
    def setup_queues(self):
        """Configura las colas necesarias"""
        
        for name, queue_name in self.queues.items():
            self.mq.declare_queue(queue_name, durable=True)
    
    def publish_task(self, task: Dict):
        """Publica una tarea para el agente"""
        
        task_message = {
            "type": "task",
            "payload": task,
            "timestamp": datetime.now().isoformat()
        }
        
        self.mq.publish(self.queues["agent_tasks"], task_message, persistent=True)
    
    def publish_result(self, result: Dict):
        """Publica el resultado de una tarea"""
        
        result_message = {
            "type": "result",
            "payload": result,
            "timestamp": datetime.now().isoformat()
        }
        
        self.mq.publish(self.queues["agent_results"], result_message, persistent=True)
    
    def publish_error(self, error: Dict):
        """Publica un error"""
        
        error_message = {
            "type": "error",
            "payload": error,
            "timestamp": datetime.now().isoformat()
        }
        
        self.mq.publish(self.queues["agent_errors"], error_message, persistent=True)
    
    def process_tasks(self, handler: Callable[[Dict], bool]):
        """Procesa tareas de la cola"""
        
        self.mq.consume(self.queues["agent_tasks"], handler, auto_ack=False)
```

#### 7.3.2 Celery Integration

```python
from celery import Celery
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


# Configuración de Celery
celery_app = Celery(
    "agent_tasks",
    broker="amqp://guest:guest@localhost:5672//",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutos max
    task_soft_time_limit=240  # 4 minutos soft limit
)


@celery_app.task(name="agent.process_request", bind=True)
def process_agent_request(self, request_data: Dict) -> Dict:
    """Tarea para procesar request de agente"""
    
    try:
        logger.info(f"Processing request: {request_data.get('request_id')}")
        
        # Simular procesamiento
        result = {
            "request_id": request_data.get("request_id"),
            "status": "completed",
            "result": {"message": "Processed successfully"}
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Task failed: {e}")
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise


@celery_app.task(name="agent.execute_tool", bind=True)
def execute_agent_tool(self, tool_data: Dict) -> Dict:
    """Tarea para ejecutar una herramienta del agente"""
    
    tool_name = tool_data.get("tool_name")
    params = tool_data.get("params", {})
    
    logger.info(f"Executing tool: {tool_name}")
    
    try:
        # Ejecutar tool (implementación específica)
        result = {"status": "success", "tool": tool_name, "result": {}}
        
        return result
        
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        raise


@celery_app.task(name="agent.process_batch", bind=True)
def process_agent_batch(self, batch_data: Dict) -> Dict:
    """Tarea para procesar un batch de requests"""
    
    items = batch_data.get("items", [])
    results = []
    
    for i, item in enumerate(items):
        try:
            self.update_state(
                state="PROGRESS",
                meta={"current": i + 1, "total": len(items)}
            )
            
            # Procesar item
            results.append({"item": item, "status": "success"})
            
        except Exception as e:
            results.append({"item": item, "status": "error", "error": str(e)})
    
    return {
        "total": len(items),
        "success": sum(1 for r in results if r["status"] == "success"),
        "failed": sum(1 for r in results if r["status"] == "error"),
        "results": results
    }


class AsyncAgentClient:
    """Cliente async para ejecutar tareas de agente"""
    
    def __init__(self, celery_app: Celery):
        self.celery = celery_app
    
    def submit_request(self, request_data: Dict):
        """Envía request para procesamiento async"""
        
        task = self.celery.send_task(
            "agent.process_request",
            args=[request_data],
            kwargs={}
        )
        
        return task.id
    
    def submit_batch(self, items: List[Dict]):
        """Envía batch para procesamiento"""
        
        task = self.celery.send_task(
            "agent.process_batch",
            args=[{"items": items}],
            kwargs={}
        )
        
        return task.id
    
    def get_result(self, task_id: str, timeout: int = 30):
        """Obtiene el resultado de una tarea"""
        
        task = self.celery.AsyncResult(task_id)
        
        if task.ready():
            return task.result
        
        if task.failed():
            raise Exception(f"Task failed: {task.info}")
        
        # Wait for result
        return task.get(timeout=timeout)
```

### 7.4 Error Handling (30 minutos)

```python
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    CONNECTION = "connection"
    TIMEOUT = "timeout"
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    NOT_FOUND = "not_found"
    DATA = "data"
    INTERNAL = "internal"
    EXTERNAL = "external"


@dataclass
class AgentError:
    """Error del agente"""
    error_id: str
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    details: Dict
    timestamp: datetime
    operation: str
    recoverable: bool


class ErrorHandler:
    """Manejador de errores para agentes"""
    
    def __init__(self):
        self.error_log: List[AgentError] = []
        self.error_handlers: Dict[ErrorCategory, callable] = {}
    
    def register_handler(self, category: ErrorCategory, handler: callable):
        """Registra un handler para un tipo de error"""
        self.error_handlers[category] = handler
    
    def handle_error(self, error: Exception, operation: str, context: Dict) -> AgentError:
        """Maneja un error"""
        
        # Clasificar el error
        category = self._classify_error(error)
        severity = self._determine_severity(error, category)
        recoverable = self._is_recoverable(category)
        
        agent_error = AgentError(
            error_id=f"ERR-{datetime.now().timestamp()}",
            category=category,
            severity=severity,
            message=str(error),
            details={
                "operation": operation,
                "context": context,
                "error_type": type(error).__name__
            },
            timestamp=datetime.now(),
            operation=operation,
            recoverable=recoverable
        )
        
        # Loggear error
        self.error_log.append(agent_error)
        
        # Ejecutar handler si existe
        if category in self.error_handlers:
            try:
                self.error_handlers[category](agent_error)
            except Exception as e:
                logger.error(f"Error handler failed: {e}")
        
        # Loggear según severidad
        log_method = {
            ErrorSeverity.LOW: logger.info,
            ErrorSeverity.MEDIUM: logger.warning,
            ErrorSeverity.HIGH: logger.error,
            ErrorSeverity.CRITICAL: logger.critical
        }
        
        log_method[severity](f"Agent error in {operation}: {error}")
        
        return agent_error
    
    def _classify_error(self, error: Exception) -> ErrorCategory:
        """Clasifica el error"""
        
        error_type = type(error).__name__.lower()
        
        if "timeout" in error_type:
            return ErrorCategory.TIMEOUT
        elif "connection" in error_type:
            return ErrorCategory.CONNECTION
        elif "auth" in error_type:
            return ErrorCategory.AUTHENTICATION
        elif "permission" in error_type:
            return ErrorCategory.AUTHORIZATION
        elif "not found" in error_type:
            return ErrorCategory.NOT_FOUND
        elif "validation" in error_type:
            return ErrorCategory.VALIDATION
        elif "data" in error_type:
            return ErrorCategory.DATA
        else:
            return ErrorCategory.INTERNAL
    
    def _determine_severity(self, error: Exception, category: ErrorCategory) -> ErrorSeverity:
        """Determina la severidad del error"""
        
        critical_categories = {
            ErrorCategory.CONNECTION,
            ErrorCategory.AUTHENTICATION,
            ErrorCategory.AUTHORIZATION
        }
        
        if category in critical_categories:
            return ErrorSeverity.HIGH
        
        return ErrorSeverity.MEDIUM
    
    def _is_recoverable(self, category: ErrorCategory) -> bool:
        """Determina si el error es recuperable"""
        
        recoverable_categories = {
            ErrorCategory.TIMEOUT,
            ErrorCategory.CONNECTION,
            ErrorCategory.DATA
        }
        
        return category in recoverable_categories
    
    def get_errors(self, limit: int = 100) -> List[AgentError]:
        """Obtiene errores recientes"""
        return self.error_log[-limit:]
```

## Diagramas

### Diagrama 1: Arquitectura de Capas de Abstracción

```mermaid
flowchart TB
    subgraph "Agente"
        A[Motor de Agente]
    end
    
    subgraph "Capa de Abstracción"
        A --> B[Interface Común]
        B --> C[Adapter Registry]
    end
    
    subgraph "Implementaciones"
        C --> D[Database Adapter]
        C --> E[API Adapter]
        C --> F[Queue Adapter]
        C --> G[File Adapter]
    end
    
    subgraph "Sistemas"
        D --> H[PostgreSQL]
        D --> I[Redis]
        E --> J[REST APIs]
        E --> K[SOAP APIs]
        F --> L[RabbitMQ]
        F --> M[Kafka]
    end
    
    style B fill:#f9f,stroke:#333
    style C fill:#ff9,stroke:#333
```

### Diagrama 2: Message Queue Flow

```mermaid
sequenceDiagram
    participant A as Agente
    participant Q as Message Queue
    participant W as Worker
    participant DB as Database

    A->>Q: Publish Task
    Q->>Q: Queue Task
    Q-->>A: Confirm
    
    W->>Q: Consume Task
    Q->>W: Task Message
    
    W->>W: Process Task
    W->>DB: Save Result
    
    W->>Q: Publish Result
    Q-->>W: Confirm
    
    A->>Q: Poll for Result
    Q-->>A: Return Result
```

## Referencias Externas

1. **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
2. **RabbitMQ Tutorials**: https://www.rabbitmq.com/tutorials/
3. **Celery Documentation**: https://docs.celeryproject.org/
4. **Python Design Patterns**: https://python-patterns.guide/
5. **Pika RabbitMQ Client**: https://pika.readthedocs.io/

## Ejercicios Prácticos Resueltos

### Ejercicio 1: Implementar Adapter Composite

**Problema**: Crear un sistema que permita conectar múltiples sistemas y ejecutar operaciones de forma uniforme.

**Solución**:

```python
"""
Sistema de Capas de Abstracción para Agentes
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==================== INTERFAZ ADAPTER ====================

class SystemAdapter(ABC):
    """Interfaz base para adapters"""
    
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def execute(self, operation: str, params: Dict) -> Dict:
        pass
    
    @abstractmethod
    def health_check(self) -> Dict:
        pass


# ==================== RESULTADO ====================

@dataclass
class OperationResult:
    success: bool
    data: Any = None
    error: str = None
    execution_time: float = 0.0


# ==================== IMPLEMENTACIONES ====================

class DatabaseAdapter(SystemAdapter):
    """Adapter para base de datos"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.connected = False
    
    def connect(self) -> bool:
        self.connected = True
        logger.info("Database connected")
        return True
    
    def disconnect(self):
        self.connected = False
        logger.info("Database disconnected")
    
    def execute(self, operation: str, params: Dict) -> Dict:
        if not self.connected:
            return {"success": False, "error": "Not connected"}
        
        return {
            "success": True,
            "data": {"operation": operation, "result": "ok"},
            "execution_time": 0.1
        }
    
    def health_check(self) -> Dict:
        return {"status": "healthy", "connected": self.connected}


class APIAdapter(SystemAdapter):
    """Adapter para APIs externas"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.connected = False
    
    def connect(self) -> bool:
        self.connected = True
        logger.info("API adapter connected")
        return True
    
    def disconnect(self):
        self.connected = False
    
    def execute(self, operation: str, params: Dict) -> Dict:
        return {
            "success": True,
            "data": {"api_call": operation, "response": "mock"},
            "execution_time": 0.2
        }
    
    def health_check(self) -> Dict:
        return {"status": "healthy", "connected": self.connected}


class QueueAdapter(SystemAdapter):
    """Adapter para message queue"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.connected = False
    
    def connect(self) -> bool:
        self.connected = True
        logger.info("Queue adapter connected")
        return True
    
    def disconnect(self):
        self.connected = False
    
    def execute(self, operation: str, params: Dict) -> Dict:
        return {
            "success": True,
            "data": {"queued": True},
            "execution_time": 0.05
        }
    
    def health_check(self) -> Dict:
        return {"status": "healthy", "connected": self.connected}


# ==================== COMPOSITE ADAPTER ====================

class AdapterComposite:
    """Compuesto de múltiples adapters"""
    
    def __init__(self):
        self.adapters: Dict[str, SystemAdapter] = {}
    
    def register(self, name: str, adapter: SystemAdapter):
        """Registra un adapter"""
        self.adapters[name] = adapter
        logger.info(f"Registered: {name}")
    
    def connect_all(self) -> Dict[str, bool]:
        """Conecta todos los adapters"""
        results = {}
        for name, adapter in self.adapters.items():
            results[name] = adapter.connect()
        return results
    
    def execute(self, adapter_name: str, operation: str, params: Dict) -> OperationResult:
        """Ejecuta en un adapter específico"""
        adapter = self.adapters.get(adapter_name)
        
        if not adapter:
            return OperationResult(
                success=False,
                error=f"Adapter not found: {adapter_name}"
            )
        
        result = adapter.execute(operation, params)
        
        return OperationResult(
            success=result.get("success", False),
            data=result.get("data"),
            error=result.get("error"),
            execution_time=result.get("execution_time", 0)
        )
    
    def broadcast(self, operation: str, params: Dict) -> Dict[str, OperationResult]:
        """Ejecuta en todos los adapters"""
        results = {}
        
        for name, adapter in self.adapters.items():
            result = adapter.execute(operation, params)
            
            results[name] = OperationResult(
                success=result.get("success", False),
                data=result.get("data"),
                error=result.get("error"),
                execution_time=result.get("execution_time", 0)
            )
        
        return results
    
    def health_check_all(self) -> Dict[str, Dict]:
        """Verifica salud de todos"""
        return {
            name: adapter.health_check()
            for name, adapter in self.adapters.items()
        }


# ==================== EJEMPLO ====================

def main():
    print("=" * 60)
    print("EJEMPLO: CAPAS DE ABSTRACCIÓN")
    print("=" * 60)
    
    # Crear composite
    composite = AdapterComposite()
    
    # Registrar adapters
    composite.register("database", DatabaseAdapter({"host": "localhost"}))
    composite.register("api", APIAdapter({"url": "https://api.example.com"}))
    composite.register("queue", QueueAdapter({"host": "localhost"}))
    
    # Conectar todos
    print("\n1. Conectando adapters...")
    results = composite.connect_all()
    for name, success in results.items():
        print(f"   {name}: {'OK' if success else 'FAILED'}")
    
    # Ejecutar en adapter específico
    print("\n2. Ejecutar operación en database:")
    result = composite.execute("database", "query", {"sql": "SELECT * FROM users"})
    print(f"   Resultado: {result.success}")
    print(f"   Tiempo: {result.execution_time:.3f}s")
    
    # Broadcast a todos
    print("\n3. Broadcast a todos:")
    results = composite.broadcast("health_check", {})
    for name, result in results.items():
        print(f"   {name}: {result.success}")
    
    # Health check
    print("\n4. Health check:")
    health = composite.health_check_all()
    for name, status in health.items():
        print(f"   {name}: {status}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
```

**Explicación**:
- **SystemAdapter**: Interfaz abstracta que define la API común
- **AdapterComposite**: Orchestra múltiples adapters
- **execute**: Ejecuta en un adapter específico
- **broadcast**: Ejecuta en todos los adapters
- **health_check_all**: Verifica el estado de todos los sistemas

## Actividades de Laboratorio

### Laboratorio 1: Implementar Adapter Registry

**Duración**: 45 minutos

**Objetivo**: Crear un registry de adapters dinámico.

**Pasos**:
1. Crear clase Registry
2. Implementar registro de adapters
3. Agregar resolución por nombre
4. Implementar lifecycle (connect/disconnect)

**Entregable**: Registry funcional.

### Laboratorio 2: Capa ORM para Legacy

**Duración**: 60 minutos

**Objetivo**: Crear capa de acceso a datos con SQLAlchemy.

**Pasos**:
1. Definir modelos
2. Crear repositorios
3. Implementar mapper
4. Agregar transacciones

**Entregable**: Capa ORM con tests.

## Resumen de Puntos Clave

1. **Adapter Pattern**: Abstrae la complejidad de sistemas externos.

2. **Composite Pattern**: Permite operar múltiples sistemas de forma uniforme.

3. **ORM**: Abstrae el acceso a bases de datos legacy.

4. **Message Queues**: RabbitMQ y Celery para procesamiento asíncrono.

5. **Error Handling**: Clasificación y manejo de errores por categoría.

6. **Reusabilidad**: Los adapters son reutilizables entre diferentes agentes.

7. **Testabilidad**: La abstracción permite mocking de sistemas externos.

8. **Maintainability**: Cambios en sistemas externos no afectan al agente.

9. **Observability**: Logging de operaciones en cada capa.

10. **Escalabilidad**: Los componentes pueden escalarse independientemente.