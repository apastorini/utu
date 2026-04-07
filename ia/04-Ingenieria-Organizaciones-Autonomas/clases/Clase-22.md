# Clase 22: Escalamiento Horizontal de Agentes

## Duración
**4 horas** (240 minutos)

---

## Objetivos de Aprendizaje

Al finalizar esta clase, el estudiante será capaz de:

1. Comprender las diferencias entre microservicios y agentes autónomos
2. Implementar estrategias de load balancing para sistemas multi-agente
3. Diseñar sistemas de sharding de estado distribuidos
4. Implementar modelos de consistencia apropiados para sistemas de agentes
5. Desplegar agentes en arquitecturas distribuidas con Kubernetes
6. Implementar comunicación inter-servicios con Redis y PostgreSQL

---

## 1. Microservicios vs Agentes

### 1.1 Comparación de Arquitecturas

```mermaid
graph TD
    subgraph Microservices["Arquitectura Microservicios"]
        M1[API Gateway] --> M2[Service A]
        M1 --> M3[Service B]
        M1 --> M4[Service C]
        M2 --> M5[(DB A)]
        M3 --> M6[(DB B)]
        M4 --> M7[(DB C)]
    end
    
    subgraph AgentSwarm["Arquitectura de Agentes"]
        A1[Orchestrator] --> A2[Agent 1]
        A1 --> A3[Agent 2]
        A1 --> A4[Agent 3]
        A2 <--> A3
        A3 <--> A4
        A2 <--> A4
        A1 <--> A5[(Shared State)]
    end
    
    style Microservices fill:#ffd43b
    style AgentSwarm fill:#69db7c
```

### 1.2 Tabla Comparativa

| Aspecto | Microservicios | Agentes Autónomos |
|---------|---------------|-------------------|
| **Estado** | Estadoful por servicio | Estado compartido/distribuido |
| **Comunicación** | REST/gRPC síncrono | Mensajes async, publish/subscribe |
| **Escalamiento** | Por servicio | Por tipo de agente |
| **Orquestación** | API Gateway, Service Mesh | Orchestrator, blackboard |
| **Replicación** | Múltiples instancias idénticas | Múltiples instancias con roles |
| **Descubrimiento** | Service Discovery | Directory Service |
| **Resiliencia** | Circuit breakers | Auto-healing, reasignación |
| **Deploy** | Containers, K8s | Containers, K8s + custom logic |

### 1.3 Híbrido: Microservicios con Agentes

```mermaid
graph TD
    subgraph API["API Layer"]
        G[API Gateway]
    end
    
    subgraph AgentLayer["Agent Layer"]
        O[Orchestrator]
        A1[Agent Pool 1]
        A2[Agent Pool 2]
        A3[Agent Pool 3]
    end
    
    subgraph ServiceLayer["Service Layer"]
        S1[User Service]
        S2[Analytics Service]
        S3[Notification Service]
    end
    
    subgraph DataLayer["Data Layer"]
        R[Redis Cache]
        P[PostgreSQL]
        M[Message Queue]
    end
    
    G --> O
    O --> A1
    O --> A2
    O --> A3
    
    A1 --> S1
    A2 --> S2
    A3 --> S3
    
    A1 --> R
    A2 --> R
    A3 --> R
    
    A1 --> P
    A2 --> P
    A3 --> P
    
    A1 -.->|async| M
    A2 -.->|async| M
    A3 -.->|async| M
    
    style AgentLayer fill:#69db7c
    style API fill:#ffd43b
```

---

## 2. Load Balancing para Agentes

### 2.1 Estrategias de Balanceo

```python
from enum import Enum
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
import random
import time

class LoadBalancingStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED = "weighted"
    RANDOM = "random"
    LEAST_RESPONSE_TIME = "least_response_time"
    IP_HASH = "ip_hash"
    SKIP_BUSY = "skip_busy"

@dataclass
class AgentInstance:
    """Instancia de un agente."""
    instance_id: str
    agent_type: str
    host: str
    port: int
    weight: int = 1
    active_connections: int = 0
    total_requests: int = 0
    total_failures: int = 0
    avg_response_time: float = 0.0
    last_health_check: float = 0.0
    healthy: bool = True

class LoadBalancer:
    """
    Load balancer para instancias de agentes.
    """
    
    def __init__(self, strategy: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN):
        self.strategy = strategy
        self.instances: Dict[str, List[AgentInstance]] = {}  # agent_type -> instances
        self.round_robin_counters: Dict[str, int] = {}
        self.connection_times: Dict[str, List[float]] = {}
    
    def register_instance(self, instance: AgentInstance):
        """Registra una nueva instancia de agente."""
        
        if instance.agent_type not in self.instances:
            self.instances[instance.agent_type] = []
            self.round_robin_counters[instance.agent_type] = 0
        
        self.instances[instance.agent_type].append(instance)
        print(f"Registered {instance.instance_id} for type {instance.agent_type}")
    
    def deregister_instance(self, instance_id: str):
        """Desregistra una instancia."""
        
        for instances in self.instances.values():
            for i, inst in enumerate(instances):
                if inst.instance_id == instance_id:
                    instances.pop(i)
                    print(f"Deregistered {instance_id}")
                    return
    
    def get_instance(self, agent_type: str, 
                   request_context: Dict = None) -> Optional[AgentInstance]:
        """Obtiene la mejor instancia para un request."""
        
        if agent_type not in self.instances:
            return None
        
        instances = [i for i in self.instances[agent_type] if i.healthy]
        
        if not instances:
            return None
        
        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._round_robin(agent_type, instances)
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return self._least_connections(instances)
        elif self.strategy == LoadBalancingStrategy.WEIGHTED:
            return self._weighted(instances)
        elif self.strategy == LoadBalancingStrategy.RANDOM:
            return self._random(instances)
        elif self.strategy == LoadBalancingStrategy.LEAST_RESPONSE_TIME:
            return self._least_response_time(instances)
        elif self.strategy == LoadBalancingStrategy.SKIP_BUSY:
            return self._skip_busy(instances)
        
        return instances[0]
    
    def _round_robin(self, agent_type: str, 
                    instances: List[AgentInstance]) -> AgentInstance:
        """Round robin simple."""
        
        counter = self.round_robin_counters.get(agent_type, 0)
        instance = instances[counter % len(instances)]
        self.round_robin_counters[agent_type] = counter + 1
        
        return instance
    
    def _least_connections(self, instances: List[AgentInstance]) -> AgentInstance:
        """Menos conexiones activas."""
        
        return min(instances, key=lambda i: i.active_connections)
    
    def _weighted(self, instances: List[AgentInstance]) -> AgentInstance:
        """Weighted random based on weight attribute."""
        
        total_weight = sum(i.weight for i in instances)
        r = random.uniform(0, total_weight)
        
        cumulative = 0
        for instance in instances:
            cumulative += instance.weight
            if r <= cumulative:
                return instance
        
        return instances[-1]
    
    def _random(self, instances: List[AgentInstance]) -> AgentInstance:
        """Selección aleatoria."""
        
        return random.choice(instances)
    
    def _least_response_time(self, 
                             instances: List[AgentInstance]) -> AgentInstance:
        """Menor tiempo de respuesta promedio."""
        
        return min(instances, key=lambda i: i.avg_response_time)
    
    def _skip_busy(self, instances: List[AgentInstance]) -> AgentInstance:
        """Skip instancias con alta carga."""
        
        threshold = 0.8  # 80% de capacidad máxima
        
        available = [
            i for i in instances 
            if i.active_connections < i.active_connections * threshold
        ]
        
        if not available:
            return instances[0]  # Fallback
        
        return min(available, key=lambda i: i.active_connections)
    
    def record_request(self, instance_id: str, response_time: float,
                      success: bool):
        """Registra resultado de un request."""
        
        for instances in self.instances.values():
            for instance in instances:
                if instance.instance_id == instance_id:
                    instance.active_connections = max(0, instance.active_connections - 1)
                    instance.total_requests += 1
                    
                    if not success:
                        instance.total_failures += 1
                    
                    # Actualizar tiempo de respuesta promedio
                    times = self.connection_times.get(instance_id, [])
                    times.append(response_time)
                    if len(times) > 100:
                        times.pop(0)
                    self.connection_times[instance_id] = times
                    
                    instance.avg_response_time = sum(times) / len(times) if times else 0
                    
                    return
    
    def health_check(self, instance_id: str, healthy: bool):
        """Actualiza estado de health check."""
        
        for instances in self.instances.values():
            for instance in instances:
                if instance.instance_id == instance_id:
                    instance.healthy = healthy
                    instance.last_health_check = time.time()
                    return


class AgentLoadBalancer:
    """
    Load balancer específico para sistemas de agentes.
    """
    
    def __init__(self):
        self.balancers: Dict[str, LoadBalancer] = {}
        self.agent_types: Dict[str, type] = {}
    
    def register_agent_type(self, agent_type: str, 
                           strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_CONNECTIONS):
        """Registra un nuevo tipo de agente con su estrategia de balanceo."""
        
        self.balancers[agent_type] = LoadBalancer(strategy)
    
    def register_agent(self, agent_type: str, instance: AgentInstance):
        """Registra una instancia de agente."""
        
        if agent_type not in self.balancers:
            self.register_agent_type(agent_type)
        
        self.balancers[agent_type].register_instance(instance)
    
    def dispatch(self, agent_type: str, task: Dict,
                context: Dict = None) -> Optional[AgentInstance]:
        """Dispacha tarea al mejor agente disponible."""
        
        balancer = self.balancers.get(agent_type)
        
        if not balancer:
            return None
        
        instance = balancer.get_instance(agent_type, context)
        
        if instance:
            instance.active_connections += 1
        
        return instance
    
    def complete(self, instance_id: str, response_time: float,
               success: bool):
        """Registra completación de tarea."""
        
        for balancer in self.balancers.values():
            balancer.record_request(instance_id, response_time, success)
```

---

## 3. Sharding de Estado

### 3.1 Estrategias de Particionamiento

```mermaid
graph TD
    subgraph Consistent["Consistent Hashing"]
        CH1[Hash Ring]
        CH2[Node A]
        CH3[Node B]
        CH4[Node C]
        CH1 --> CH2
        CH1 --> CH3
        CH1 --> CH4
    end
    
    subgraph Range["Range-based"]
        R1[0-100] --> R2[Node A]
        R1 --> R3[101-200]
        R1 --> R4[201-300]
    end
    
    subgraph Composite["Composite Sharding"]
        CP1[User Shard]
        CP2[Session Shard]
        CP3[Task Shard]
    end
```

### 3.2 Implementación de Sharding

```python
import hashlib
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import json

@dataclass
class Shard:
    """Representación de un shard."""
    shard_id: str
    nodes: List[str]
    data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}

class ShardManager:
    """
    Gestor de sharding para estado distribuido.
    """
    
    def __init__(self, num_shards: int = 4, replication_factor: int = 2):
        self.num_shards = num_shards
        self.replication_factor = replication_factor
        self.shards: Dict[int, Shard] = {}
        self.ring_positions: Dict[int, int] = {}  # hash -> shard_id
        self._init_shards()
    
    def _init_shards(self):
        """Inicializa shards."""
        
        for i in range(self.num_shards):
            self.shards[i] = Shard(
                shard_id=f"shard_{i}",
                nodes=[f"node_{i % 3}"]  # Simplified node assignment
            )
    
    def _hash_key(self, key: str) -> int:
        """Calcula hash de una key."""
        
        hash_obj = hashlib.md5(key.encode())
        return int(hash_obj.hexdigest(), 16)
    
    def _get_shard_for_key(self, key: str) -> int:
        """Obtiene shard para una key."""
        
        hash_val = self._hash_key(key)
        return hash_val % self.num_shards
    
    def _get_replica_shards(self, primary_shard: int) -> List[int]:
        """Obtiene shards réplicas."""
        
        replicas = [primary_shard]
        for i in range(1, self.replication_factor):
            replica_shard = (primary_shard + i) % self.num_shards
            replicas.append(replica_shard)
        
        return replicas
    
    def put(self, key: str, value: Any, agent_id: str):
        """Almacena valor con clave."""
        
        primary_shard = self._get_shard_for_key(key)
        replicas = self._get_replica_shards(primary_shard)
        
        # Escribir en primario
        self.shards[primary_shard].data[key] = {
            "value": value,
            "agent_id": agent_id,
            "shards": replicas,
            "timestamp": self._current_timestamp()
        }
        
        # Replicar en réplicas
        for shard_id in replicas[1:]:
            self.shards[shard_id].data[key] = self.shards[primary_shard].data[key].copy()
    
    def get(self, key: str) -> Optional[Any]:
        """Obtiene valor por clave."""
        
        shard_id = self._get_shard_for_key(key)
        shard = self.shards.get(shard_id)
        
        if not shard:
            return None
        
        entry = shard.data.get(key)
        
        if entry:
            return entry["value"]
        
        return None
    
    def delete(self, key: str):
        """Elimina valor por clave."""
        
        shard_id = self._get_shard_for_key(key)
        replicas = self._get_replica_shards(shard_id)
        
        for shard_id in replicas:
            if key in self.shards[shard_id].data:
                del self.shards[shard_id].data[key]
    
    def _current_timestamp(self) -> float:
        """Obtiene timestamp actual."""
        
        import time
        return time.time()
    
    def get_shard_stats(self) -> Dict:
        """Obtiene estadísticas de shards."""
        
        stats = {}
        total_size = 0
        
        for shard_id, shard in self.shards.items():
            size = len(json.dumps(shard.data))
            total_size += size
            stats[shard_id] = {
                "num_keys": len(shard.data),
                "size_bytes": size,
                "nodes": shard.nodes
            }
        
        stats["total"] = {
            "num_shards": self.num_shards,
            "total_keys": sum(s["num_keys"] for s in stats.values()),
            "total_size": total_size
        }
        
        return stats


class ConsistentHashRing:
    """
    Consistent Hashing para distribución de carga.
    """
    
    def __init__(self, virtual_nodes: int = 100):
        self.virtual_nodes = virtual_nodes
        self.ring: Dict[int, str] = {}  # hash -> node
        self.sorted_keys: List[int] = []
        self.nodes: Dict[str, Dict] = {}  # node_id -> node_info
    
    def add_node(self, node_id: str, node_info: Dict = None):
        """Añade nodo al ring."""
        
        self.nodes[node_id] = node_info or {}
        
        # Añadir virtual nodes
        for i in range(self.virtual_nodes):
            key = self._hash(f"{node_id}:{i}")
            self.ring[key] = node_id
            self.sorted_keys.append(key)
        
        self.sorted_keys.sort()
    
    def remove_node(self, node_id: str):
        """Remueve nodo del ring."""
        
        if node_id not in self.nodes:
            return
        
        # Remover virtual nodes
        for i in range(self.virtual_nodes):
            key = self._hash(f"{node_id}:{i}")
            if key in self.ring:
                del self.ring[key]
                self.sorted_keys.remove(key)
        
        del self.nodes[node_id]
    
    def get_node(self, key: str) -> Optional[str]:
        """Obtiene nodo para una clave."""
        
        if not self.ring:
            return None
        
        hash_val = self._hash(key)
        
        # Binary search para encontrar nodo
        for node_hash in self.sorted_keys:
            if node_hash >= hash_val:
                return self.ring[node_hash]
        
        # Wrap around al primero
        return self.ring[self.sorted_keys[0]]
    
    def _hash(self, key: str) -> int:
        """Calcula hash."""
        
        hash_obj = hashlib.md5(key.encode())
        return int(hash_obj.hexdigest(), 16)
    
    def get_nodes_for_key_range(self, start_key: str, end_key: str) -> List[str]:
        """Obtiene nodos para un rango de claves."""
        
        start_hash = self._hash(start_key)
        end_hash = self._hash(end_key)
        
        nodes = []
        for node_hash, node_id in self.ring.items():
            if start_hash <= node_hash <= end_hash:
                if node_id not in nodes:
                    nodes.append(node_id)
        
        return nodes


class StateShardManager:
    """
    Gestor de estado particionado para sistemas multi-agente.
    """
    
    def __init__(self, num_shards: int = 8):
        self.shard_manager = ShardManager(num_shards)
        self.hash_ring = ConsistentHashRing()
        self.local_cache: Dict[str, Any] = {}
        self.cache_ttl: float = 300  # 5 minutes
    
    def store_agent_state(self, agent_id: str, state: Dict):
        """Almacena estado de un agente."""
        
        # Usar agent_id como clave principal
        self.shard_manager.put(f"agent:{agent_id}", state, agent_id)
        
        # También guardar en cache local
        self.local_cache[agent_id] = {
            "state": state,
            "timestamp": self._current_time()
        }
    
    def get_agent_state(self, agent_id: str) -> Optional[Dict]:
        """Obtiene estado de un agente."""
        
        # Primero verificar cache local
        if agent_id in self.local_cache:
            cached = self.local_cache[agent_id]
            if self._current_time() - cached["timestamp"] < self.cache_ttl:
                return cached["state"]
        
        # Obtener de shard
        return self.shard_manager.get(f"agent:{agent_id}")
    
    def store_task_result(self, task_id: str, result: Any, owner_agent: str):
        """Almacena resultado de tarea."""
        
        self.shard_manager.put(f"task:{task_id}", {
            "result": result,
            "owner": owner_agent,
            "completed_at": self._current_time()
        }, owner_agent)
    
    def get_task_result(self, task_id: str) -> Optional[Any]:
        """Obtiene resultado de tarea."""
        
        entry = self.shard_manager.get(f"task:{task_id}")
        
        if entry:
            return entry.get("result")
        
        return None
    
    def store_session_data(self, session_id: str, agent_id: str, data: Dict):
        """Almacena datos de sesión."""
        
        self.shard_manager.put(f"session:{session_id}:{agent_id}", data, agent_id)
    
    def _current_time(self) -> float:
        """Obtiene timestamp actual."""
        
        import time
        return time.time()
    
    def get_shard_distribution(self) -> Dict:
        """Obtiene distribución de datos entre shards."""
        
        return self.shard_manager.get_shard_stats()
```

---

## 4. Modelos de Consistencia

### 4.1 Tipos de Consistencia

```mermaid
graph TD
    subgraph Consistency["Modelos de Consistencia"]
        C1[Strong Consistency]
        C2[Sequential Consistency]
        C3[Causal Consistency]
        C4[Eventual Consistency]
    end
    
    C1 --> |Guarantees| G1[All clients see same data immediately]
    C2 --> |Guarantees| G2[Operations appear in order]
    C3 --> |Guarantees| G3[Related operations in order]
    C4 --> |Guarantees| G4[Eventually all replicas converge]
    
    style C1 fill:#ff6b6b
    style C4 fill:#69db7c
```

### 4.2 Implementación de Modelos de Consistencia

```python
from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import threading
import time

class ConsistencyLevel(Enum):
    STRONG = "strong"
    SEQUENTIAL = "sequential"
    CAUSAL = "causal"
    EVENTUAL = "eventual"

@dataclass
class VersionedValue:
    """Valor versionado para control de concurrencia."""
    value: Any
    version: int
    timestamp: float
    agent_id: str

class ConsistencyManager:
    """
    Gestor de consistencia para estado distribuido.
    """
    
    def __init__(self, level: ConsistencyLevel = ConsistencyLevel.SEQUENTIAL):
        self.level = level
        self.storage: Dict[str, List[VersionedValue]] = {}
        self.locks: Dict[str, threading.Lock] = {}
        self.vector_clocks: Dict[str, Dict[str, int]] = {}
    
    def _get_lock(self, key: str) -> threading.Lock:
        """Obtiene lock para una clave."""
        
        if key not in self.locks:
            self.locks[key] = threading.Lock()
        
        return self.locks[key]
    
    def write(self, key: str, value: Any, agent_id: str) -> bool:
        """Escribe valor con consistencia especificada."""
        
        if self.level == ConsistencyLevel.STRONG:
            return self._write_strong(key, value, agent_id)
        elif self.level == ConsistencyLevel.SEQUENTIAL:
            return self._write_sequential(key, value, agent_id)
        elif self.level == ConsistencyLevel.CAUSAL:
            return self._write_causal(key, value, agent_id)
        else:
            return self._write_eventual(key, value, agent_id)
    
    def _write_strong(self, key: str, value: Any, agent_id: str) -> bool:
        """Escritura con consistencia fuerte (locks)."""
        
        lock = self._get_lock(key)
        
        with lock:
            # Obtener siguiente versión
            version = len(self.storage.get(key, []))
            
            entry = VersionedValue(
                value=value,
                version=version + 1,
                timestamp=time.time(),
                agent_id=agent_id
            )
            
            if key not in self.storage:
                self.storage[key] = []
            
            self.storage[key].append(entry)
            
            return True
    
    def _write_sequential(self, key: str, value: Any, agent_id: str) -> bool:
        """Escritura con consistencia secuencial."""
        
        lock = self._get_lock(key)
        
        with lock:
            version = len(self.storage.get(key, []))
            
            entry = VersionedValue(
                value=value,
                version=version + 1,
                timestamp=time.time(),
                agent_id=agent_id
            )
            
            if key not in self.storage:
                self.storage[key] = []
            
            self.storage[key].append(entry)
            
            return True
    
    def _write_causal(self, key: str, value: Any, agent_id: str) -> bool:
        """Escritura con consistencia causal (vector clocks)."""
        
        # Actualizar vector clock del agente
        if agent_id not in self.vector_clocks:
            self.vector_clocks[agent_id] = {}
        
        if key not in self.vector_clocks:
            self.vector_clocks[key] = {}
        
        # Incrementar contador del agente
        for clock in [self.vector_clocks[agent_id], self.vector_clocks[key]]:
            clock[agent_id] = clock.get(agent_id, 0) + 1
        
        version = self.vector_clocks[key].copy()
        
        entry = VersionedValue(
            value=value,
            version=0,  # Usamos vector clock
            timestamp=time.time(),
            agent_id=agent_id
        )
        
        if key not in self.storage:
            self.storage[key] = []
        
        self.storage[key].append(entry)
        
        return True
    
    def _write_eventual(self, key: str, value: Any, agent_id: str) -> bool:
        """Escritura eventual (sin locks)."""
        
        entry = VersionedValue(
            value=value,
            version=int(time.time() * 1000),
            timestamp=time.time(),
            agent_id=agent_id
        )
        
        if key not in self.storage:
            self.storage[key] = []
        
        self.storage[key].append(entry)
        
        return True
    
    def read(self, key: str, agent_id: str = None) -> Optional[Any]:
        """Lee valor con consistencia especificada."""
        
        if key not in self.storage or not self.storage[key]:
            return None
        
        if self.level == ConsistencyLevel.STRONG:
            return self._read_strong(key)
        elif self.level == ConsistencyLevel.SEQUENTIAL:
            return self._read_sequential(key)
        elif self.level == ConsistencyLevel.CAUSAL:
            return self._read_causal(key, agent_id)
        else:
            return self._read_eventual(key)
    
    def _read_strong(self, key: str) -> Any:
        """Lectura con consistencia fuerte."""
        
        lock = self._get_lock(key)
        
        with lock:
            entries = self.storage.get(key, [])
            if entries:
                return entries[-1].value
        
        return None
    
    def _read_sequential(self, key: str) -> Any:
        """Lectura con consistencia secuencial."""
        
        entries = self.storage.get(key, [])
        if entries:
            return entries[-1].value
        
        return None
    
    def _read_causal(self, key: str, agent_id: str) -> Any:
        """Lectura con consistencia causal."""
        
        entries = self.storage.get(key, [])
        if not entries:
            return None
        
        # Encontrar entrada más reciente que no vio entradas futuras
        best_entry = entries[-1]
        
        return best_entry.value
    
    def _read_eventual(self, key: str) -> Any:
        """Lectura eventual."""
        
        entries = self.storage.get(key, [])
        if entries:
            return entries[-1].value
        
        return None


class DistributedLock:
    """
    Lock distribuido simple (en memoria para demo).
    """
    
    def __init__(self, name: str):
        self.name = name
        self.lock = threading.Lock()
        self.holders: List[str] = []
    
    def acquire(self, agent_id: str, timeout: float = None) -> bool:
        """Adquiere el lock."""
        
        acquired = self.lock.acquire(timeout=timeout)
        
        if acquired:
            self.holders.append(agent_id)
        
        return acquired
    
    def release(self, agent_id: str):
        """Libera el lock."""
        
        if agent_id in self.holders:
            self.holders.remove(agent_id)
            self.lock.release()
    
    def is_locked(self) -> bool:
        """Verifica si está bloqueado."""
        
        return self.lock.locked()


class TwoPhaseCommit:
    """
    Implementación simplificada de Two-Phase Commit.
    """
    
    def __init__(self):
        self.coordinators: Dict[str, str] = {}
        self.participants: Dict[str, List[str]] = {}
        self.prepared: Dict[str, set] = {}
        self.committed: Dict[str, bool] = {}
    
    def prepare(self, transaction_id: str, coordinator: str,
               participants: List[str]) -> bool:
        """Fase 1: Prepare."""
        
        self.coordinators[transaction_id] = coordinator
        self.participants[transaction_id] = participants
        self.prepared[transaction_id] = set()
        
        # Enviar prepare a todos los participantes
        for participant in participants:
            # En implementación real, esto sería una llamada de red
            vote = self._simulate_vote(participant)
            
            if vote == "YES":
                self.prepared[transaction_id].add(participant)
            else:
                # Fallo - abortar
                self._abort(transaction_id)
                return False
        
        return len(self.prepared[transaction_id]) == len(participants)
    
    def commit(self, transaction_id: str) -> bool:
        """Fase 2: Commit."""
        
        if transaction_id not in self.coordinators:
            return False
        
        if len(self.prepared.get(transaction_id, set())) != len(self.participants[transaction_id]):
            self._abort(transaction_id)
            return False
        
        # Enviar commit a todos los participantes
        for participant in self.participants[transaction_id]:
            self._simulate_commit(participant)
        
        self.committed[transaction_id] = True
        return True
    
    def _abort(self, transaction_id: str):
        """Abort transacción."""
        
        for participant in self.participants.get(transaction_id, []):
            self._simulate_abort(participant)
        
        self.committed[transaction_id] = False
    
    def _simulate_vote(self, participant: str) -> str:
        """Simula voto de participante."""
        
        return "YES"
    
    def _simulate_commit(self, participant: str):
        """Simula commit de participante."""
        pass
    
    def _simulate_abort(self, participant: str):
        """Simula abort de participante."""
        pass
```

---

## 5. Deployment con Kubernetes

### 5.1 Definiciones de Recursos K8s

```yaml
# deployment.yaml - Deployment de Agente
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-pool-coder
  namespace: agent-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent
      role: coder
  template:
    metadata:
      labels:
        app: agent
        role: coder
    spec:
      containers:
      - name: agent
        image: agent-registry/coder-agent:latest
        ports:
        - containerPort: 8080
        env:
        - name: AGENT_TYPE
          value: "coder"
        - name: REDIS_URL
          value: "redis://redis-cluster:6379"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: role
                  operator: In
                  values:
                  - coder
              topologyKey: kubernetes.io/hostname
```

```yaml
# service.yaml - Service para agentes
apiVersion: v1
kind: Service
metadata:
  name: agent-coder-service
  namespace: agent-system
spec:
  selector:
    app: agent
    role: coder
  ports:
  - name: http
    port: 80
    targetPort: 8080
  type: ClusterIP
```

```yaml
# hpa.yaml - Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: agent-coder-hpa
  namespace: agent-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-pool-coder
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

### 5.2 Helm Chart para Sistema de Agentes

```yaml
# values.yaml - Configuración del Helm chart
replicaCount: 3

image:
  repository: agent-registry
  pullPolicy: IfNotPresent

agents:
  coder:
    enabled: true
    replicas: 3
    resources:
      limits:
        cpu: "1"
        memory: "2Gi"
      requests:
        cpu: "500m"
        memory: "1Gi"
  
  reviewer:
    enabled: true
    replicas: 2
    resources:
      limits:
        cpu: "1"
        memory: "1Gi"
  
  tester:
    enabled: true
    replicas: 2
    resources:
      limits:
        cpu: "500m"
        memory: "512Mi"

redis:
  enabled: true
  architecture: replication
  master:
    resources:
      limits:
        cpu: "500m"
        memory: "256Mi"

postgres:
  enabled: true
  auth:
    database: agent_state
  primary:
    persistence:
      size: 10Gi
    resources:
      limits:
        cpu: "1"
        memory: "1Gi"

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt
  hosts:
  - host: agents.example.com
    paths:
    - path: /
      pathType: Prefix

monitoring:
  enabled: true
  prometheus:
    enabled: true
  grafana:
    enabled: true
```

```yaml
# templates/deployment-agent.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "agent-system.fullname" . }}-{{ .name }}
  labels:
    {{- include "agent-system.labels" . | nindent 4 }}
    agent-type: {{ .name }}
spec:
  replicas: {{ .replicas }}
  selector:
    matchLabels:
      {{- include "agent-system.selectorLabels" . | nindent 6 }}
      agent-type: {{ .name }}
  template:
    metadata:
      labels:
        {{- include "agent-system.selectorLabels" . | nindent 8 }}
        agent-type: {{ .name }}
    spec:
      containers:
      - name: agent
        image: {{ .Values.image.repository }}/{{ .name }}:{{ .Values.image.tag | default .Chart.AppVersion }}
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        env:
        - name: AGENT_TYPE
          value: {{ .name }}
        - name: REDIS_URL
          value: {{ include "agent-system.redis.url" . }}
        - name: DATABASE_URL
          value: {{ include "agent-system.postgres.url" . }}
        - name: LOG_LEVEL
          value: {{ .Values.config.logLevel }}
        resources:
          {{- toYaml .resources | nindent 10 }}
        livenessProbe:
          httpGet:
            path: /health
            port: http
        readinessProbe:
          httpGet:
            path: /ready
            port: http
```

### 5.3 Implementación de Agente K8s-Ready

```python
"""
Agente listo para deployment en Kubernetes.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio
import logging
import os
from prometheus_client import Counter, Histogram, generate_latest
import redis.asyncio as redis
import asyncpg

app = FastAPI(title="K8s-ready Agent")

# Métricas Prometheus
REQUEST_COUNT = Counter(
    'agent_requests_total',
    'Total requests',
    ['agent_type', 'endpoint']
)
REQUEST_LATENCY = Histogram(
    'agent_request_latency_seconds',
    'Request latency',
    ['agent_type', 'endpoint']
)

# Configuración desde environment
AGENT_TYPE = os.getenv("AGENT_TYPE", "generic")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/agent_state")

# Clients
redis_client = None
db_pool = None

class TaskRequest(BaseModel):
    task_id: str
    payload: Dict
    priority: int = 1

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict] = None

@app.on_event("startup")
async def startup():
    """Inicializa conexiones."""
    global redis_client, db_pool
    
    # Redis
    redis_client = await redis.from_url(REDIS_URL)
    
    # PostgreSQL
    db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
    
    logging.info(f"Agent {AGENT_TYPE} started")

@app.on_event("shutdown")
async def shutdown():
    """Limpia conexiones."""
    global redis_client, db_pool
    
    if redis_client:
        await redis_client.close()
    if db_pool:
        await db_pool.close()

@app.get("/health")
async def health():
    """Liveness probe."""
    return {"status": "healthy", "agent_type": AGENT_TYPE}

@app.get("/ready")
async def ready():
    """Readiness probe."""
    checks = []
    
    try:
        await redis_client.ping()
        checks.append(("redis", True))
    except:
        checks.append(("redis", False))
    
    try:
        async with db_pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        checks.append(("postgres", True))
    except:
        checks.append(("postgres", False))
    
    all_ready = all(c[1] for c in checks)
    
    if not all_ready:
        raise HTTPException(status_code=503, detail="Dependencies not ready")
    
    return {
        "status": "ready",
        "agent_type": AGENT_TYPE,
        "checks": dict(checks)
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest()

@app.post("/tasks", response_model=TaskResponse)
async def process_task(task: TaskRequest):
    """Procesa una tarea."""
    
    import time
    start_time = time.time()
    
    try:
        # Log task
        await redis_client.lpush(
            f"task_queue:{AGENT_TYPE}",
            task.json()
        )
        
        # Process (simplified)
        result = await execute_task(task.payload)
        
        # Store result
        await redis_client.setex(
            f"task_result:{task.task_id}",
            3600,
            str(result)
        )
        
        # Store in DB
        async with db_pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO task_results (task_id, agent_type, result, completed_at)
                VALUES ($1, $2, $3, NOW())
                """,
                task.task_id, AGENT_TYPE, str(result)
            )
        
        REQUEST_COUNT.labels(AGENT_TYPE, "tasks").inc()
        REQUEST_LATENCY.labels(AGENT_TYPE, "tasks").observe(
            time.time() - start_time
        )
        
        return TaskResponse(
            task_id=task.task_id,
            status="completed",
            result=result
        )
    
    except Exception as e:
        logging.error(f"Error processing task {task.task_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def execute_task(payload: Dict) -> Dict:
    """Ejecuta lógica de tarea."""
    
    action = payload.get("action", "default")
    
    if action == "process":
        return {"processed": True, "data": payload.get("data")}
    elif action == "analyze":
        return {"analysis": "completed", "insights": []}
    else:
        return {"status": "executed"}

@app.get("/stats")
async def stats():
    """Estadísticas del agente."""
    
    queue_len = await redis_client.llen(f"task_queue:{AGENT_TYPE}")
    
    return {
        "agent_type": AGENT_TYPE,
        "queue_length": queue_len,
        "host": os.getenv("HOSTNAME", "unknown")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

---

## 6. Tecnologías Específicas

| Tecnología | Propósito | Uso |
|------------|-----------|-----|
| **Kubernetes** | Orquestación de containers | Deployment de agentes |
| **Helm** | Package manager K8s | Charts de agentes |
| **Redis** | Cache y pub/sub | Estado compartido |
| **PostgreSQL** | Estado persistente | Datos de agentes |
| **Kafka** | Event streaming | Eventos distribuidos |
| **Istio** | Service mesh | Networking de agentes |
| **Prometheus** | Metrics | Monitoreo |
| **ArgoCD** | GitOps | Deployments |

---

## 7. Actividades de Laboratorio

### Laboratorio 1: Deployment Kubernetes de Sistema de Agentes

**Objetivo**: Desplegar sistema multi-agente en Kubernetes

**Duración**: 2 horas

**Pasos**:

1. **Crear namespace**:
```bash
kubectl create namespace agent-system
```

2. **Deploy con Helm**:
```bash
helm install agent-system ./charts/agent-system \
    --namespace agent-system \
    --set agents.coder.replicas=3 \
    --set agents.reviewer.replicas=2 \
    --set redis.enabled=true \
    --set postgres.enabled=true
```

3. **Escalar dinámicamente**:
```bash
kubectl autoscale deployment agent-system-coder \
    --namespace agent-system \
    --min=2 --max=10 --cpu-percent=70
```

4. **Verificar deployment**:
```bash
kubectl get pods -n agent-system
kubectl get services -n agent-system
kubectl get hpa -n agent-system
```

### Laboratorio 2: Implementación de Sharding Distribuido

**Duración**: 2 horas

```python
# distributed_sharding.py

import hashlib
from typing import Dict, List, Any
import redis
import asyncio

class DistributedShardManager:
    def __init__(self, redis_urls: List[str]):
        self.redis_clients = [redis.from_url(url) for url in redis_urls]
        self.num_shards = len(redis_urls)
    
    def _get_shard_index(self, key: str) -> int:
        hash_val = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return hash_val % self.num_shards
    
    def _get_client(self, key: str):
        return self.redis_clients[self._get_shard_index(key)]
    
    async def put(self, key: str, value: Any, ttl: int = None):
        client = self._get_client(key)
        await client.set(key, str(value), ex=ttl)
    
    async def get(self, key: str) -> Any:
        client = self._get_client(key)
        return await client.get(key)
    
    async def delete(self, key: str):
        client = self._get_client(key)
        await client.delete(key)
    
    def get_shard_stats(self) -> Dict:
        stats = {}
        for i, client in enumerate(self.redis_clients):
            info = client.info('memory')
            stats[f"shard_{i}"] = {
                "used_memory": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients")
            }
        return stats

# Uso
manager = DistributedShardManager([
    "redis://redis-1:6379",
    "redis://redis-2:6379",
    "redis://redis-3:6379",
    "redis://redis-4:6379"
])

asyncio.run(manager.put("agent:1", {"state": "active"}))
result = asyncio.run(manager.get("agent:1"))
```

---

## 8. Resumen de Puntos Clave

### Microservicios vs Agentes

1. **Microservicios**: Servicios stateless con APIs bien definidas
2. **Agentes**: Entidades stateful con comunicación directa
3. **Híbrido**: API layer con agentes internos para procesamiento inteligente

### Load Balancing

1. **Round Robin**: Simple pero ignora carga
2. **Least Connections**: Balancea por carga activa
3. **Weighted**: Considera capacidad de nodos
4. **Least Response Time**: Optimiza latencia

### Sharding

1. **Hash-based**: Distribución uniforme por hash de clave
2. **Consistent Hashing**: Minimiza reorganización al añadir/remover nodos
3. **Range-based**: Particiona por rangos de claves
4. **Replication**: Datos replicados en múltiples shards

### Consistencia

1. **Strong**: Garantiza atomicidad pero tiene latencia
2. **Sequential**: Mantiene orden de operaciones
3. **Causal**: Preserva relaciones causales
4. **Eventual**: Alta disponibilidad, converge eventualmente

---

## Referencias Externas

1. **Kubernetes Documentation**:
   https://kubernetes.io/docs/

2. **Helm Charts Best Practices**:
   https://helm.sh/docs/chart_best_practices/

3. **Redis Cluster**:
   https://redis.io/docs/management/scaling/

4. **Consistent Hashing**:
   https://en.wikipedia.org/wiki/Consistent_hashing

5. **CAP Theorem**:
   https://en.wikipedia.org/wiki/CAP_theorem

6. **Horizontal Pod Autoscaling**:
   https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/

---

**Siguiente Clase**: Clase 23 - Company-in-a-Box: Arquitectura
