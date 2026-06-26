# CLASE 25: Proyecto Memory Bank Completo

## Duración: 4 horas

---

## 1. Objetivos de Aprendizaje

Al finalizar esta clase, el estudiante será capaz de:

1. **Diseñar una arquitectura completa** para un sistema de memoria persistente basado en LLMs
2. **Implementar pipelines end-to-end** utilizando LangChain y PostgreSQL
3. **Crear mecanismos de recuperación de información** semántica eficiente
4. **Implementar estrategias de indexación** y chunking optimizadas
5. **Desarrollar APIs RESTful** para interactuar con el sistema de memoria
6. **Aplicar patrones de diseño** empresariales para sistemas de producción
7. **Implementar tests automatizados** para validar la funcionalidad del sistema
8. **Optimizar el rendimiento** de consultas vectoriales a escala

---

## 2. Contenidos Detallados

### 2.1 Arquitectura General del Sistema

El proyecto Memory Bank representa un sistema de gestión de conocimiento persistente que permite a aplicaciones de IA almacenar, recuperar y razonar sobre información contextual. A diferencia de sistemas de memoria efímera, Memory Bank persiste la información entre sesiones y permite consultas semánticas sofisticadas.

```mermaid
graph TB
    subgraph "Capa de Presentación"
        A[API REST] --> B[FastAPI Application]
        B --> C[WebSocket Server]
    end
    
    subgraph "Capa de Negocio"
        D[Memory Manager] --> E[Vector Store Manager]
        D --> F[Query Engine]
        D --> G[Context Builder]
        E --> H[Embedding Service]
    end
    
    subgraph "Capa de Datos"
        I[(PostgreSQL<br/>pgvector)] --> J[Vector Store]
        I --> K[Metadata Store]
        I --> L[Document Store]
        M[(Redis Cache)] --> N[Query Cache]
    end
    
    subgraph "Capa de Integración"
        O[LangChain Agent] --> D
        P[External LLMs] --> O
    end
    
    A --> D
    H --> E
    J --> E
```

### 2.2 Diseño de la Base de Datos

#### Schema de PostgreSQL con pgvector

El diseño de la base de datos es fundamental para el rendimiento del sistema. Utilizamos PostgreSQL con la extensión pgvector para almacenar embeddings y metadata asociada.

```sql
-- Extensión pgvector para búsquedas de similitud vectorial
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla principal de documentos/memorias
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL UNIQUE,
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    access_count INTEGER DEFAULT 0,
    is_deleted BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}'
);

-- Índices para optimización de consultas
CREATE INDEX idx_memories_embedding ON memories USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX idx_memories_created_at ON memories (created_at DESC);
CREATE INDEX idx_memories_access_count ON memories (access_count DESC);
CREATE INDEX idx_memories_content_hash ON memories (content_hash);

-- Tabla de categorías/espacios de memoria
CREATE TABLE memory_spaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id VARCHAR(255),
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Relación muchos a muchos entre memorias y espacios
CREATE TABLE memory_space_membership (
    memory_id UUID REFERENCES memories(id) ON DELETE CASCADE,
    space_id UUID REFERENCES memory_spaces(id) ON DELETE CASCADE,
    importance_score FLOAT DEFAULT 0.5,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (memory_id, space_id)
);

-- Tabla de tags para organización flexible
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    color VARCHAR(7),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE memory_tags (
    memory_id UUID REFERENCES memories(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (memory_id, tag_id)
);

-- Tabla de versiones para control de cambios
CREATE TABLE memory_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    memory_id UUID REFERENCES memories(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    version_number INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    change_summary TEXT
);

CREATE INDEX idx_versions_memory ON memory_versions (memory_id, version_number DESC);

-- Tabla de relationships entre memorias
CREATE TABLE memory_relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_memory_id UUID REFERENCES memories(id) ON DELETE CASCADE,
    target_memory_id UUID REFERENCES memories(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL,
    strength FLOAT DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(source_memory_id, target_memory_id, relationship_type)
);

CREATE INDEX idx_relationships_source ON memory_relationships (source_memory_id);
CREATE INDEX idx_relationships_target ON memory_relationships (target_memory_id);

-- Función para actualizar timestamps automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_memories_updated_at
    BEFORE UPDATE ON memories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_memory_spaces_updated_at
    BEFORE UPDATE ON memory_spaces
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 2.3 Implementación del Sistema

#### Estructura del Proyecto

```
memory_bank/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada FastAPI
│   ├── config.py               # Configuración
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── memories.py     # Endpoints de memorias
│   │   │   ├── spaces.py       # Endpoints de espacios
│   │   │   ├── search.py       # Endpoints de búsqueda
│   │   │   └── health.py       # Health checks
│   │   ├── dependencies.py     # Dependencias FastAPI
│   │   └── middleware.py       # Middleware personalizado
│   ├── core/
│   │   ├── __init__.py
│   │   ├── memory_manager.py   # Gestor principal
│   │   ├── vector_store.py     # Gestión de vectores
│   │   ├── query_engine.py     # Motor de consultas
│   │   ├── context_builder.py  # Constructor de contexto
│   │   └── embedding_service.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py         # Conexión a PostgreSQL
│   │   ├── models.py           # Modelos SQLAlchemy
│   │   └── repositories/
│   │       ├── memory_repo.py
│   │       ├── space_repo.py
│   │       └── tag_repo.py
│   ├── schemas/
│   │   ├── memory_schemas.py
│   │   ├── space_schemas.py
│   │   └── search_schemas.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_processor.py
│   │   ├── embedding_generator.py
│   │   └── cache_service.py
│   └── utils/
│       ├── __init__.py
│       ├── chunking.py
│       ├── text_processing.py
│       └── security.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_memory_manager.py
│   │   ├── test_vector_store.py
│   │   └── test_query_engine.py
│   └── integration/
│       ├── test_api_memories.py
│       └── test_search.py
├── migrations/
│   └── versions/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
└── README.md
```

#### Configuración del Sistema

```python
# src/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os


class Settings(BaseSettings):
    """Configuración centralizada del sistema Memory Bank."""
    
    # Aplicación
    APP_NAME: str = "Memory Bank API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"
    
    # Base de datos
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/memorybank"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600
    
    # Embeddings
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    EMBEDDING_DIMENSIONS: int = 1536
    OPENAI_API_KEY: Optional[str] = None
    
    # Chunking
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Vector Store
    VECTOR_SEARCH_LIMIT: int = 10
    SIMILARITY_THRESHOLD: float = 0.7
    
    # Seguridad
    API_KEY_HEADER: str = "X-API-Key"
    SECRET_KEY: str = "change-this-in-production"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Obtiene la configuración cacheada."""
    return Settings()
```

#### Gestor Principal de Memoria

```python
# src/core/memory_manager.py
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from uuid import UUID
import hashlib
import json
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_
import numpy as np

from src.db.models import Memory, MemorySpace, MemoryTag, MemoryVersion
from src.db.repositories.memory_repo import MemoryRepository
from src.core.vector_store import VectorStore
from src.core.embedding_service import EmbeddingService
from src.schemas.memory_schemas import (
    MemoryCreate, MemoryUpdate, MemoryResponse,
    MemorySearchResult, MemorySearchQuery
)


class MemoryManager:
    """
    Gestor principal del sistema de memoria.
    Coordina todas las operaciones relacionadas con memorias.
    """
    
    def __init__(
        self,
        session: AsyncSession,
        vector_store: VectorStore,
        embedding_service: EmbeddingService
    ):
        self.session = session
        self.memory_repo = MemoryRepository(session)
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self._cache = {}
    
    async def create_memory(
        self,
        memory_data: MemoryCreate,
        generate_embedding: bool = True
    ) -> MemoryResponse:
        """
        Crea una nueva memoria en el sistema.
        
        Args:
            memory_data: Datos de la memoria a crear
            generate_embedding: Si True, genera embedding automáticamente
            
        Returns:
            MemoryResponse con la memoria creada
        """
        # Verificar si ya existe (por hash de contenido)
        content_hash = self._compute_content_hash(memory_data.content)
        
        existing = await self.memory_repo.get_by_hash(content_hash)
        if existing:
            # Actualizar access_count en lugar de crear duplicado
            await self.memory_repo.increment_access(existing.id)
            return MemoryResponse.model_validate(existing)
        
        # Generar embedding si es necesario
        embedding = None
        if generate_embedding:
            embedding = await self.embedding_service.generate_embedding(
                memory_data.content
            )
        
        # Preparar metadata
        metadata = memory_data.metadata or {}
        metadata.update({
            "source": memory_data.source,
            "created_by": memory_data.created_by
        })
        
        # Crear la memoria
        memory = Memory(
            content=memory_data.content,
            content_hash=content_hash,
            embedding=embedding,
            metadata=metadata
        )
        
        # Guardar en la base de datos
        created_memory = await self.memory_repo.create(memory)
        
        # Guardar en el vector store
        if embedding is not None:
            await self.vector_store.insert_vector(
                id=str(created_memory.id),
                embedding=embedding,
                metadata={
                    "content": memory_data.content[:500],  # Primeros 500 chars
                    "created_at": created_memory.created_at.isoformat()
                }
            )
        
        # Crear versión inicial
        await self.memory_repo.create_version(
            memory_id=created_memory.id,
            content=memory_data.content,
            version_number=1,
            change_summary="Versión inicial"
        )
        
        return MemoryResponse.model_validate(created_memory)
    
    async def get_memory(self, memory_id: UUID) -> Optional[MemoryResponse]:
        """Obtiene una memoria por su ID."""
        memory = await self.memory_repo.get_by_id(memory_id)
        
        if memory:
            await self.memory_repo.increment_access(memory_id)
        
        return MemoryResponse.model_validate(memory) if memory else None
    
    async def update_memory(
        self,
        memory_id: UUID,
        update_data: MemoryUpdate
    ) -> Optional[MemoryResponse]:
        """
        Actualiza una memoria existente.
        
        Args:
            memory_id: ID de la memoria a actualizar
            update_data: Nuevos datos para la memoria
            
        Returns:
            MemoryResponse con la memoria actualizada o None si no existe
        """
        memory = await self.memory_repo.get_by_id(memory_id)
        if not memory:
            return None
        
        # Obtener siguiente número de versión
        versions = await self.memory_repo.get_versions(memory_id)
        next_version = max([v.version_number for v in versions]) + 1 if versions else 1
        
        # Crear versión del contenido anterior
        await self.memory_repo.create_version(
            memory_id=memory_id,
            content=memory.content,
            version_number=next_version,
            change_summary=update_data.change_summary or "Actualización"
        )
        
        # Actualizar campos
        if update_data.content is not None:
            memory.content = update_data.content
            memory.content_hash = self._compute_content_hash(update_data.content)
            
            # Regenerar embedding
            new_embedding = await self.embedding_service.generate_embedding(
                update_data.content
            )
            memory.embedding = new_embedding
            
            # Actualizar vector store
            await self.vector_store.update_vector(
                id=str(memory_id),
                embedding=new_embedding,
                metadata={"content": update_data.content[:500]}
            )
        
        if update_data.metadata is not None:
            memory.metadata = update_data.metadata
        
        await self.session.commit()
        await self.session.refresh(memory)
        
        return MemoryResponse.model_validate(memory)
    
    async def delete_memory(
        self,
        memory_id: UUID,
        soft_delete: bool = True
    ) -> bool:
        """
        Elimina una memoria.
        
        Args:
            memory_id: ID de la memoria a eliminar
            soft_delete: Si True, marca como eliminada; si False, elimina físicamente
            
        Returns:
            True si se eliminó correctamente, False si no existe
        """
        memory = await self.memory_repo.get_by_id(memory_id)
        if not memory:
            return False
        
        if soft_delete:
            memory.is_deleted = True
            await self.session.commit()
            # También marcar como eliminada en el vector store
            await self.vector_store.delete_vector(str(memory_id))
        else:
            await self.memory_repo.delete(memory_id)
            await self.vector_store.delete_vector(str(memory_id))
        
        return True
    
    async def search_memories(
        self,
        query: MemorySearchQuery
    ) -> List[MemorySearchResult]:
        """
        Busca memorias usando búsqueda semántica.
        
        Args:
            query: Parámetros de búsqueda
            
        Returns:
            Lista de memorias ordenadas por relevancia
        """
        # Generar embedding de la consulta
        query_embedding = await self.embedding_service.generate_embedding(query.text)
        
        # Buscar en el vector store
        vector_results = await self.vector_store.search(
            query_vector=query_embedding,
            limit=query.limit or 10,
            threshold=query.similarity_threshold or 0.7
        )
        
        # Obtener detalles completos de las memorias
        results = []
        for vector_result in vector_results:
            memory_id = UUID(vector_result["id"])
            memory = await self.memory_repo.get_by_id(memory_id)
            
            if memory and not memory.is_deleted:
                results.append(MemorySearchResult(
                    memory=MemoryResponse.model_validate(memory),
                    similarity_score=vector_result["score"],
                    highlight=vector_result.get("highlight")
                ))
        
        # Aplicar filtros adicionales si se especifican
        if query.space_id:
            results = await self._filter_by_space(results, query.space_id)
        
        if query.tags:
            results = await self._filter_by_tags(results, query.tags)
        
        if query.date_from or query.date_to:
            results = await self._filter_by_date(
                results, query.date_from, query.date_to
            )
        
        return results
    
    async def get_context_for_llm(
        self,
        query: str,
        max_memories: int = 10,
        max_tokens: int = 4000
    ) -> str:
        """
        Construye un contexto de memoria para ser usado por un LLM.
        
        Args:
            query: Consulta o tema para recuperar memorias relevantes
            max_memories: Número máximo de memorias a incluir
            max_tokens: Límite de tokens en el contexto
            
        Returns:
            String formateado con el contexto de memoria
        """
        search_results = await self.search_memories(
            MemorySearchQuery(
                text=query,
                limit=max_memories,
                similarity_threshold=0.6
            )
        )
        
        context_parts = []
        total_tokens = 0
        
        for result in search_results:
            memory_text = result.memory.content
            estimated_tokens = len(memory_text.split()) * 1.3  # Aproximación
            
            if total_tokens + estimated_tokens > max_tokens:
                break
            
            context_parts.append(
                f"[Recuerdo #{len(context_parts) + 1}] "
                f"(Relevancia: {result.similarity_score:.2f})\n"
                f"{memory_text}\n"
            )
            total_tokens += estimated_tokens
        
        if not context_parts:
            return "No se encontraron memorias relevantes para esta consulta."
        
        header = f"=== CONTEXTO DE MEMORIA ({len(context_parts)} recuerdos) ===\n\n"
        footer = "\n=== FIN DEL CONTEXTO DE MEMORIA ==="
        
        return header + "\n\n".join(context_parts) + footer
    
    async def get_related_memories(
        self,
        memory_id: UUID,
        max_results: int = 5
    ) -> List[MemoryResponse]:
        """Obtiene memorias relacionadas basadas en similitud vectorial."""
        memory = await self.memory_repo.get_by_id(memory_id)
        if not memory or not memory.embedding:
            return []
        
        search_results = await self.vector_store.search(
            query_vector=memory.embedding,
            limit=max_results + 1,  # +1 para excluir la propia memoria
            threshold=0.5
        )
        
        results = []
        for result in search_results:
            result_id = UUID(result["id"])
            if result_id != memory_id:
                memory = await self.memory_repo.get_by_id(result_id)
                if memory and not memory.is_deleted:
                    results.append(MemoryResponse.model_validate(memory))
        
        return results[:max_results]
    
    def _compute_content_hash(self, content: str) -> str:
        """Calcula un hash único para el contenido."""
        return hashlib.sha256(content.encode()).hexdigest()
    
    async def _filter_by_space(
        self,
        results: List[MemorySearchResult],
        space_id: UUID
    ) -> List[MemorySearchResult]:
        """Filtra resultados por espacio de memoria."""
        filtered = []
        for result in results:
            membership = await self.memory_repo.get_membership(
                result.memory.id, space_id
            )
            if membership:
                filtered.append(result)
        return filtered
    
    async def _filter_by_tags(
        self,
        results: List[MemorySearchResult],
        tags: List[str]
    ) -> List[MemorySearchResult]:
        """Filtra resultados por tags."""
        filtered = []
        for result in results:
            memory_tags = await self.memory_repo.get_tags(result.memory.id)
            if any(tag in memory_tags for tag in tags):
                filtered.append(result)
        return filtered
    
    async def _filter_by_date(
        self,
        results: List[MemorySearchResult],
        date_from: Optional[datetime],
        date_to: Optional[datetime]
    ) -> List[MemorySearchResult]:
        """Filtra resultados por rango de fechas."""
        filtered = []
        for result in results:
            created = result.memory.created_at
            if date_from and created < date_from:
                continue
            if date_to and created > date_to:
                continue
            filtered.append(result)
        return filtered
```

#### Motor de Consultas Vectoriales

```python
# src/core/vector_store.py
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import json


class VectorStore:
    """
    Gestor del vector store usando pgvector.
    Maneja todas las operaciones de búsqueda vectorial.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.dimensions = 1536  # Dimensiones de text-embedding-ada-002
    
    async def insert_vector(
        self,
        id: str,
        embedding: List[float],
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Inserta un vector en el store.
        
        Args:
            id: Identificador único del vector
            embedding: Vector de embedding
            metadata: Metadatos asociados
            
        Returns:
            True si la inserción fue exitosa
        """
        embedding_str = "[" + ",".join(map(str, embedding)) + "]"
        metadata_json = json.dumps(metadata)
        
        query = text("""
            INSERT INTO memories (id, embedding, metadata)
            VALUES (:id, :embedding, :metadata::jsonb)
            ON CONFLICT (content_hash) DO NOTHING
            RETURNING id
        """)
        
        # Nota: En un sistema real, necesitaríamos el content_hash
        # Este es un ejemplo simplificado
        return True
    
    async def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        threshold: float = 0.7,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca vectores similares usando búsqueda de similitud coseno.
        
        Args:
            query_vector: Vector de la consulta
            limit: Número máximo de resultados
            threshold: Umbral mínimo de similitud (0-1)
            filters: Filtros adicionales para la búsqueda
            
        Returns:
            Lista de diccionarios con id, score y metadata
        """
        # Convertir query_vector a formato SQL
        query_vector_str = "[" + ",".join(map(str, query_vector)) + "]"
        
        # Construir query con filtros
        base_query = """
            SELECT 
                id,
                1 - (embedding <=> :query_vector::vector) as similarity,
                content,
                metadata,
                created_at
            FROM memories
            WHERE is_deleted = false
        """
        
        params = {"query_vector": query_vector_str, "limit": limit}
        
        if filters:
            if "space_id" in filters:
                base_query += """
                    AND id IN (
                        SELECT memory_id FROM memory_space_membership
                        WHERE space_id = :space_id
                    )
                """
                params["space_id"] = str(filters["space_id"])
            
            if "tags" in filters:
                base_query += """
                    AND id IN (
                        SELECT memory_id FROM memory_tags mt
                        JOIN tags t ON mt.tag_id = t.id
                        WHERE t.name = ANY(:tags)
                    )
                """
                params["tags"] = filters["tags"]
            
            if "date_from" in filters:
                base_query += " AND created_at >= :date_from"
                params["date_from"] = filters["date_from"]
            
            if "date_to" in filters:
                base_query += " AND created_at <= :date_to"
                params["date_to"] = filters["date_to"]
        
        base_query += """
            ORDER BY embedding <=> :query_vector::vector
            LIMIT :limit
        """
        
        result = await self.session.execute(
            text(base_query),
            params
        )
        
        results = []
        for row in result:
            similarity = float(row.similarity)
            if similarity >= threshold:
                results.append({
                    "id": str(row.id),
                    "score": similarity,
                    "content": row.content,
                    "metadata": row.metadata,
                    "created_at": row.created_at.isoformat() if row.created_at else None,
                    "highlight": self._generate_highlight(row.content, query_vector)
                })
        
        return results
    
    async def search_hybrid(
        self,
        query: str,
        query_vector: List[float],
        limit: int = 10,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Búsqueda híbrida que combina similitud vectorial con BM25.
        
        Args:
            query: Texto de la consulta
            query_vector: Vector de embedding de la consulta
            limit: Número máximo de resultados
            vector_weight: Peso de la similitud vectorial
            keyword_weight: Peso del ranking por palabras clave
            
        Returns:
            Lista de resultados combinados
        """
        # Obtener resultados vectoriales
        vector_results = await self.search(query_vector, limit=limit * 2)
        vector_scores = {r["id"]: r["score"] for r in vector_results}
        
        # Obtener resultados por palabras clave (BM25 simulado)
        keyword_results = await self._keyword_search(query, limit=limit * 2)
        keyword_scores = {r["id"]: r["score"] for r in keyword_results}
        
        # Combinar scores
        all_ids = set(vector_scores.keys()) | set(keyword_scores.keys())
        
        combined_results = []
        for id in all_ids:
            vec_score = vector_scores.get(id, 0)
            key_score = keyword_scores.get(id, 0)
            
            # Normalización y combinación
            combined_score = (
                vector_weight * vec_score +
                keyword_weight * key_score
            )
            
            # Obtener datos del resultado
            result_data = None
            for r in vector_results:
                if r["id"] == id:
                    result_data = r
                    break
            if not result_data:
                for r in keyword_results:
                    if r["id"] == id:
                        result_data = r
                        break
            
            if result_data:
                combined_results.append({
                    **result_data,
                    "score": combined_score,
                    "vector_score": vec_score,
                    "keyword_score": key_score
                })
        
        # Ordenar por score combinado
        combined_results.sort(key=lambda x: x["score"], reverse=True)
        
        return combined_results[:limit]
    
    async def _keyword_search(
        self,
        query: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Búsqueda por palabras clave usando ts_rank de PostgreSQL."""
        query = text("""
            SELECT 
                id,
                ts_rank(to_tsvector('spanish', content), plainto_tsquery('spanish', :query)) as score,
                content,
                metadata
            FROM memories
            WHERE 
                is_deleted = false
                AND to_tsvector('spanish', content) @@ plainto_tsquery('spanish', :query)
            ORDER BY score DESC
            LIMIT :limit
        """)
        
        result = await self.session.execute(query, {"query": query, "limit": limit})
        
        results = []
        max_score = 1.0
        for row in result:
            results.append({
                "id": str(row.id),
                "score": float(row.score) / max_score if row.score else 0,
                "content": row.content,
                "metadata": row.metadata
            })
        
        return results
    
    def _generate_highlight(
        self,
        content: str,
        query_vector: List[float]
    ) -> str:
        """Genera un fragmento destacado del contenido."""
        # Extraer una porción del contenido relevante
        max_length = 300
        if len(content) <= max_length:
            return content
        
        # Buscar punto de corte en oración completa
        cut_point = content[:max_length].rfind(". ")
        if cut_point == -1:
            cut_point = content[:max_length].rfind(" ")
        
        highlight = content[:cut_point + 1] if cut_point > 0 else content[:max_length]
        
        if len(content) > max_length:
            highlight += "..."
        
        return highlight
    
    async def update_vector(
        self,
        id: str,
        embedding: List[float],
        metadata: Dict[str, Any]
    ) -> bool:
        """Actualiza un vector existente."""
        embedding_str = "[" + ",".join(map(str, embedding)) + "]"
        metadata_json = json.dumps(metadata)
        
        query = text("""
            UPDATE memories
            SET 
                embedding = :embedding::vector,
                metadata = :metadata::jsonb,
                updated_at = NOW()
            WHERE id = :id AND is_deleted = false
        """)
        
        result = await self.session.execute(
            query,
            {"id": id, "embedding": embedding_str, "metadata": metadata_json}
        )
        
        await self.session.commit()
        return result.rowcount > 0
    
    async def delete_vector(self, id: str) -> bool:
        """Elimina un vector (soft delete)."""
        query = text("""
            UPDATE memories
            SET is_deleted = true
            WHERE id = :id
        """)
        
        result = await self.session.execute(query, {"id": id})
        await self.session.commit()
        return result.rowcount > 0
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de la colección."""
        query = text("""
            SELECT 
                COUNT(*) as total_memories,
                COUNT(*) FILTER (WHERE is_deleted = false) as active_memories,
                AVG(vector_norm(embedding)) as avg_vector_norm,
                MIN(created_at) as oldest_memory,
                MAX(created_at) as newest_memory
            FROM memories
        """)
        
        result = await self.session.execute(query)
        row = result.fetchone()
        
        return {
            "total_memories": row.total_memories,
            "active_memories": row.active_memories,
            "avg_vector_norm": float(row.avg_vector_norm) if row.avg_vector_norm else 0,
            "oldest_memory": row.oldest_memory.isoformat() if row.oldest_memory else None,
            "newest_memory": row.newest_memory.isoformat() if row.newest_memory else None
        }
```

### 2.4 API REST con FastAPI

```python
# src/main.py
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Optional
from uuid import UUID

from src.config import get_settings
from src.db.database import get_db, engine, Base
from src.core.memory_manager import MemoryManager
from src.core.vector_store import VectorStore
from src.core.embedding_service import EmbeddingService
from src.schemas.memory_schemas import (
    MemoryCreate, MemoryUpdate, MemoryResponse,
    MemorySearchQuery, MemorySearchResult, MemoryBulkCreate
)
from src.api.routes import memories, search, spaces, health

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación."""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(memories.router, prefix=settings.API_PREFIX)
app.include_router(search.router, prefix=settings.API_PREFIX)
app.include_router(spaces.router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
```

```python
# src/api/routes/memories.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
import asyncio

from src.db.database import get_db
from src.core.memory_manager import MemoryManager
from src.core.vector_store import VectorStore
from src.core.embedding_service import EmbeddingService
from src.schemas.memory_schemas import (
    MemoryCreate, MemoryUpdate, MemoryResponse, MemoryBulkCreate,
    MemorySearchQuery, MemorySearchResult, MemoryDeleteResponse
)

router = APIRouter(prefix="/memories", tags=["Memories"])


def get_memory_manager(db: AsyncSession = Depends(get_db)) -> MemoryManager:
    """Dependency injection para MemoryManager."""
    return MemoryManager(
        session=db,
        vector_store=VectorStore(db),
        embedding_service=EmbeddingService()
    )


@router.post(
    "",
    response_model=MemoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva memoria"
)
async def create_memory(
    memory_data: MemoryCreate,
    background_tasks: BackgroundTasks,
    manager: MemoryManager = Depends(get_memory_manager)
):
    """
    Crea una nueva memoria en el sistema.
    
    - **content**: Contenido de la memoria (obligatorio)
    - **metadata**: Metadatos opcionales
    - **tags**: Lista de tags opcionales
    - **space_id**: ID del espacio de memoria (opcional)
    """
    try:
        memory = await manager.create_memory(memory_data)
        return memory
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear memoria: {str(e)}"
        )


@router.post(
    "/bulk",
    response_model=List[MemoryResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Crear múltiples memorias"
)
async def create_bulk_memories(
    bulk_data: MemoryBulkCreate,
    background_tasks: BackgroundTasks,
    manager: MemoryManager = Depends(get_memory_manager)
):
    """
    Crea múltiples memorias en una sola operación.
    
    Útil para importar grandes cantidades de datos.
    """
    results = []
    
    for memory_data in bulk_data.memories:
        try:
            memory = await manager.create_memory(memory_data)
            results.append(memory)
        except Exception as e:
            # Continuar con las siguientes memorias
            continue
    
    return results


@router.get(
    "/{memory_id}",
    response_model=MemoryResponse,
    summary="Obtener memoria por ID"
)
async def get_memory(
    memory_id: UUID,
    manager: MemoryManager = Depends(get_memory_manager)
):
    """Obtiene una memoria específica por su ID."""
    memory = await manager.get_memory(memory_id)
    
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memoria {memory_id} no encontrada"
        )
    
    return memory


@router.put(
    "/{memory_id}",
    response_model=MemoryResponse,
    summary="Actualizar memoria"
)
async def update_memory(
    memory_id: UUID,
    update_data: MemoryUpdate,
    manager: MemoryManager = Depends(get_memory_manager)
):
    """
    Actualiza una memoria existente.
    
    - **content**: Nuevo contenido (opcional)
    - **metadata**: Nuevos metadatos (opcional)
    - **change_summary**: Resumen del cambio realizado
    """
    memory = await manager.update_memory(memory_id, update_data)
    
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memoria {memory_id} no encontrada"
        )
    
    return memory


@router.delete(
    "/{memory_id}",
    response_model=MemoryDeleteResponse,
    summary="Eliminar memoria"
)
async def delete_memory(
    memory_id: UUID,
    soft_delete: bool = True,
    manager: MemoryManager = Depends(get_memory_manager)
):
    """
    Elimina una memoria.
    
    Por defecto, realiza un soft delete (marca como eliminada).
    Use soft_delete=false para eliminar físicamente.
    """
    success = await manager.delete_memory(memory_id, soft_delete)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memoria {memory_id} no encontrada"
        )
    
    return MemoryDeleteResponse(
        id=memory_id,
        deleted=True,
        message="Memoria eliminada correctamente"
    )


@router.get(
    "/{memory_id}/related",
    response_model=List[MemoryResponse],
    summary="Obtener memorias relacionadas"
)
async def get_related_memories(
    memory_id: UUID,
    max_results: int = 5,
    manager: MemoryManager = Depends(get_memory_manager)
):
    """Obtiene memorias semánticamente relacionadas a la memoria especificada."""
    return await manager.get_related_memories(memory_id, max_results)


@router.get(
    "/{memory_id}/versions",
    response_model=List[dict],
    summary="Obtener historial de versiones"
)
async def get_memory_versions(
    memory_id: UUID,
    manager: MemoryManager = Depends(get_memory_manager)
):
    """Obtiene el historial de versiones de una memoria."""
    memory = await manager.get_memory(memory_id)
    
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memoria {memory_id} no encontrada"
        )
    
    # Aquí se obtendría el historial de versiones
    return []
```

### 2.5 Sistema de Chunks y Procesamiento de Documentos

```python
# src/utils/chunking.py
from typing import List, Tuple, Optional
import re


class DocumentChunker:
    """
    Divide documentos en chunks optimizados para embeddings.
    Implementa múltiples estrategias de chunking.
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        min_chunk_size: int = 100
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
    
    def chunk_by_tokens(
        self,
        text: str,
        tokenizer: Optional[callable] = None
    ) -> List[Tuple[str, int, int]]:
        """
        Divide el texto en chunks basados en tokens.
        
        Args:
            text: Texto a dividir
            tokenizer: Función para contar tokens (default: word-based approximation)
            
        Returns:
            Lista de tuplas (chunk_text, start_token, end_token)
        """
        if tokenizer is None:
            tokenizer = self._approx_token_count
        
        tokens = text.split()
        chunks = []
        start = 0
        
        while start < len(tokens):
            end = start + self._get_tokens_for_chunk(tokenizer)
            
            if end < len(tokens):
                # Encontrar límite de oración
                chunk_text = " ".join(tokens[start:end])
                last_period = chunk_text.rfind(".")
                last_newline = chunk_text.rfind("\n")
                
                cutoff = max(last_period, last_newline)
                if cutoff > self.chunk_size // 4:  # Al menos 25% del chunk
                    chunk_text = chunk_text[:cutoff + 1]
                    tokens_processed = len(chunk_text.split())
                    end = start + tokens_processed
            
            chunk = " ".join(tokens[start:end]).strip()
            
            if len(chunk) >= self.min_chunk_size:
                chunks.append((
                    chunk,
                    start,
                    min(end, len(tokens))
                ))
            
            # Mover con solapamiento
            start = end - self._count_overlap_tokens()
        
        return chunks
    
    def chunk_by_sentences(
        self,
        text: str,
        sentences_per_chunk: int = 5
    ) -> List[Tuple[str, int, int]]:
        """
        Divide el texto en chunks de oraciones completas.
        
        Args:
            text: Texto a dividir
            sentences_per_chunk: Número de oraciones por chunk
            
        Returns:
            Lista de tuplas (chunk_text, start_sentence, end_sentence)
        """
        sentences = self._split_into_sentences(text)
        chunks = []
        
        for i in range(0, len(sentences), sentences_per_chunk):
            chunk_sentences = sentences[i:i + sentences_per_chunk]
            chunk_text = " ".join(chunk_sentences).strip()
            
            if len(chunk_text) >= self.min_chunk_size:
                chunks.append((
                    chunk_text,
                    i,
                    min(i + sentences_per_chunk, len(sentences))
                ))
        
        return chunks
    
    def chunk_by_paragraphs(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Divide el texto en chunks de párrafos.
        
        Returns:
            Lista de tuplas (chunk_text, start_para, end_para)
        """
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks = []
        
        current_chunk = []
        current_size = 0
        start_para = 0
        
        for i, para in enumerate(paragraphs):
            para_size = len(para)
            
            if current_size + para_size > self.chunk_size and current_chunk:
                chunks.append((
                    "\n\n".join(current_chunk),
                    start_para,
                    i
                ))
                current_chunk = [para]
                current_size = para_size
                start_para = i
            else:
                current_chunk.append(para)
                current_size += para_size
        
        # Agregar el último chunk
        if current_chunk:
            chunks.append((
                "\n\n".join(current_chunk),
                start_para,
                len(paragraphs)
            ))
        
        return chunks
    
    def chunk_by_sections(
        self,
        text: str,
        section_headers: Optional[List[str]] = None
    ) -> List[Tuple[str, int, int]]:
        """
        Divide el texto en chunks basado en encabezados de sección.
        
        Args:
            text: Texto a dividir
            section_headers: Lista de patrones de headers (regex)
        """
        if section_headers is None:
            section_headers = [
                r"^#{1,6}\s+.+$",           # Markdown headers
                r"^[A-Z][A-Z\s]{5,}$",      # ALL CAPS headers
                r"^\d+\.\s+[A-Z]",          # Numbered sections
            ]
        
        sections = self._split_by_headers(text, section_headers)
        chunks = []
        
        current_chunk = []
        current_size = 0
        
        for section in sections:
            if current_size + len(section) > self.chunk_size and current_chunk:
                chunks.append(("\n\n".join(current_chunk), 0, len(current_chunk)))
                current_chunk = [section]
                current_size = len(section)
            else:
                current_chunk.append(section)
                current_size += len(section)
        
        if current_chunk:
            chunks.append(("\n\n".join(current_chunk), 0, len(current_chunk)))
        
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Divide texto en oraciones."""
        pattern = r"(?<=[.!?])\s+"
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _split_by_headers(
        self,
        text: str,
        header_patterns: List[str]
    ) -> List[str]:
        """Divide texto por encabezados."""
        combined_pattern = "|".join(f"({p})" for p in header_patterns)
        parts = re.split(combined_pattern, text, flags=re.MULTILINE)
        
        sections = []
        current_section = []
        
        for part in parts:
            if part and any(re.match(p, part.strip()) for p in header_patterns):
                if current_section:
                    sections.append("\n".join(current_section))
                    current_section = []
            current_section.append(part)
        
        if current_section:
            sections.append("\n".join(current_section))
        
        return [s.strip() for s in sections if s.strip()]
    
    def _approx_token_count(self, text: str) -> int:
        """Aproximación de tokens basada en palabras."""
        return len(text.split())
    
    def _get_tokens_for_chunk(self, tokenizer: callable) -> int:
        """Calcula el número de tokens para un chunk."""
        # Suponiendo ~4 caracteres por token en promedio
        return self.chunk_size // 4
    
    def _count_overlap_tokens(self) -> int:
        """Calcula el número de tokens de solapamiento."""
        return self.chunk_overlap // 4


class SemanticChunker(DocumentChunker):
    """
    Chunker semántico que usa embeddings para determinar
    dónde dividir el texto de manera más coherente.
    """
    
    def __init__(
        self,
        embedding_service,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        similarity_threshold: float = 0.7
    ):
        super().__init__(chunk_size, chunk_overlap)
        self.embedding_service = embedding_service
        self.similarity_threshold = similarity_threshold
    
    async def semantic_chunk(
        self,
        text: str,
        max_iterations: int = 10
    ) -> List[dict]:
        """
        Divide el texto usando similitud semántica entre secciones.
        
        Args:
            text: Texto a dividir
            max_iterations: Máximo de iteraciones para refinement
            
        Returns:
            Lista de chunks con metadatos de similitud
        """
        # Dividir inicialmente por párrafos
        initial_chunks = self.chunk_by_paragraphs(text)
        
        # Combinar chunks hasta que la similitud sea baja
        final_chunks = []
        current_chunk = ""
        current_start = 0
        
        for i, (chunk_text, start_para, end_para) in enumerate(initial_chunks):
            if not current_chunk:
                current_chunk = chunk_text
                current_start = start_para
                continue
            
            # Calcular similitud entre chunks actuales
            combined = current_chunk + " " + chunk_text
            combined_embedding = await self.embedding_service.generate_embedding(combined)
            current_embedding = await self.embedding_service.generate_embedding(current_chunk)
            
            similarity = self._cosine_similarity(current_embedding, combined_embedding)
            
            if similarity >= self.similarity_threshold and len(combined) < self.chunk_size * 2:
                # Combinar chunks
                current_chunk = combined
            else:
                # Guardar chunk actual e iniciar nuevo
                final_chunks.append({
                    "text": current_chunk,
                    "start_paragraph": current_start,
                    "end_paragraph": start_para,
                    "num_paragraphs": start_para - current_start
                })
                current_chunk = chunk_text
                current_start = start_para
        
        # Agregar último chunk
        if current_chunk:
            final_chunks.append({
                "text": current_chunk,
                "start_paragraph": current_start,
                "end_paragraph": len(initial_chunks),
                "num_paragraphs": len(initial_chunks) - current_start
            })
        
        return final_chunks
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calcula similitud coseno entre dos vectores."""
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(y * y for y in b) ** 0.5
        return dot_product / (norm_a * norm_b)
```

### 2.6 Diagrama de Flujo de Operaciones

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI
    participant MM as Memory Manager
    participant VS as Vector Store
    participant ES as Embedding Service
    participant DB as PostgreSQL

    Note over Client,DB: CREAR NUEVA MEMORIA

    Client->>API: POST /memories {content, metadata}
    API->>MM: create_memory(data)
    
    MM->>MM: compute_content_hash()
    
    alt Memoria existe
        MM->>DB: get_by_hash(hash)
        DB-->>MM: existing_memory
        MM->>DB: increment_access()
        MM-->>API: return existing_memory
    else Nueva memoria
        MM->>ES: generate_embedding(content)
        ES-->>MM: embedding_vector
        
        MM->>DB: create(Memory)
        DB-->>MM: created_memory
        
        MM->>VS: insert_vector(id, embedding, metadata)
        VS-->>MM: success
        
        MM->>DB: create_version()
        DB-->>MM: version_created
        
        MM-->>API: return created_memory
    end
    
    API-->>Client: 201 Created + MemoryResponse

    Note over Client,DB: BÚSQUEDA SEMÁNTICA

    Client->>API: GET /search?query=...
    API->>MM: search_memories(query)
    
    MM->>ES: generate_embedding(query)
    ES-->>MM: query_embedding
    
    MM->>VS: search(query_embedding, limit, threshold)
    VS->>DB: SELECT with vector similarity
    DB-->>VS: results
    VS-->>MM: search_results
    
    alt Aplicar filtros
        loop Para cada filtro
            MM->>MM: _filter_by_*(results)
        end
    end
    
    MM-->>API: List[MemorySearchResult]
    API-->>Client: 200 OK + Results
```

---

## 3. Ejercicios Prácticos Resueltos

### Ejercicio 1: Implementación Completa del Memory Bank

**Enunciado**: Implementa un sistema completo de Memory Bank con todas las funcionalidades descritas.

**Solución**:

```python
# ejercicio_1/memory_bank_complete.py

"""
Ejercicio 1: Implementación completa del sistema Memory Bank
Este script demuestra todas las funcionalidades principales del sistema.
"""

import asyncio
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
import hashlib

# Simulación de dependencias externas
class MockEmbeddingService:
    """Servicio de embeddings simulado para pruebas."""
    
    def __init__(self, dimensions: int = 1536):
        self.dimensions = dimensions
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Genera un embedding simulado basado en el hash del texto."""
        import random
        random.seed(hash(text) % (2**32))
        return [random.random() for _ in range(self.dimensions)]


class MockDatabase:
    """Base de datos simulada en memoria."""
    
    def __init__(self):
        self.memories = {}
        self.versions = {}
        self.relationships = []
        self.spaces = {}
    
    async def create(self, memory: dict) -> dict:
        """Crea una memoria en la base de datos."""
        self.memories[memory["id"]] = memory.copy()
        return self.memories[memory["id"]]
    
    async def get(self, memory_id: UUID) -> Optional[dict]:
        """Obtiene una memoria por ID."""
        return self.memories.get(str(memory_id))
    
    async def get_by_hash(self, content_hash: str) -> Optional[dict]:
        """Obtiene una memoria por hash de contenido."""
        for memory in self.memories.values():
            if memory.get("content_hash") == content_hash:
                return memory
        return None
    
    async def update(self, memory_id: UUID, updates: dict) -> Optional[dict]:
        """Actualiza una memoria."""
        if str(memory_id) in self.memories:
            self.memories[str(memory_id)].update(updates)
            return self.memories[str(memory_id)]
        return None
    
    async def delete(self, memory_id: UUID) -> bool:
        """Elimina una memoria."""
        if str(memory_id) in self.memories:
            del self.memories[str(memory_id)]
            return True
        return False
    
    async def list_all(self) -> List[dict]:
        """Lista todas las memorias."""
        return list(self.memories.values())


class MemoryBankSystem:
    """
    Sistema completo de Memory Bank.
    Implementación demostrativa con todas las funcionalidades.
    """
    
    def __init__(self):
        self.db = MockDatabase()
        self.embedding_service = MockEmbeddingService()
        self._vector_store = {}  # id -> embedding
        self._cache = {}
    
    async def initialize(self):
        """Inicializa el sistema."""
        print("=" * 60)
        print("INICIALIZANDO SISTEMA MEMORY BANK")
        print("=" * 60)
        print("✓ Base de datos en memoria conectada")
        print("✓ Servicio de embeddings inicializado")
        print("✓ Vector store preparado")
        print("✓ Cache habilitado")
        print("=" * 60)
        print()
    
    async def store_memory(
        self,
        content: str,
        metadata: Optional[dict] = None,
        tags: Optional[List[str]] = None
    ) -> dict:
        """
        Almacena una nueva memoria.
        
        Args:
            content: Contenido de la memoria
            metadata: Metadatos opcionales
            tags: Tags opcionales
            
        Returns:
            Diccionario con la memoria creada
        """
        print(f"\n📝 Almacenando nueva memoria...")
        print(f"   Contenido: {content[:50]}...")
        
        # Verificar si ya existe
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        existing = await self.db.get_by_hash(content_hash)
        
        if existing:
            print(f"   ⚠️  Memoria ya existe (ID: {existing['id']})")
            existing["access_count"] += 1
            existing["last_accessed"] = datetime.now().isoformat()
            return existing
        
        # Generar embedding
        print(f"   🔄 Generando embedding semántico...")
        embedding = await self.embedding_service.generate_embedding(content)
        
        # Crear memoria
        memory_id = str(uuid4())
        memory = {
            "id": memory_id,
            "content": content,
            "content_hash": content_hash,
            "metadata": metadata or {},
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "accessed_at": datetime.now().isoformat(),
            "access_count": 1,
            "is_deleted": False,
            "version": 1
        }
        
        # Guardar en DB y vector store
        await self.db.create(memory)
        self._vector_store[memory_id] = embedding
        
        print(f"   ✅ Memoria creada (ID: {memory_id})")
        print(f"   📊 Embedding: {len(embedding)} dimensiones")
        
        return memory
    
    async def retrieve_memory(self, memory_id: UUID) -> Optional[dict]:
        """Recupera una memoria por ID."""
        print(f"\n🔍 Recuperando memoria {memory_id}...")
        
        memory = await self.db.get(memory_id)
        
        if not memory:
            print(f"   ❌ Memoria no encontrada")
            return None
        
        if memory.get("is_deleted"):
            print(f"   ❌ Memoria eliminada")
            return None
        
        # Actualizar estadísticas de acceso
        memory["access_count"] += 1
        memory["accessed_at"] = datetime.now().isoformat()
        
        print(f"   ✅ Memoria recuperada")
        print(f"   📈 Total de accesos: {memory['access_count']}")
        
        return memory
    
    async def search_similar(
        self,
        query: str,
        limit: int = 5,
        threshold: float = 0.5
    ) -> List[dict]:
        """
        Busca memorias similares a la consulta.
        
        Args:
            query: Texto de búsqueda
            limit: Número máximo de resultados
            threshold: Umbral de similitud mínimo
            
        Returns:
            Lista de memorias ordenadas por similitud
        """
        print(f"\n🔎 Buscando: '{query}'")
        print(f"   Límite: {limit}, Umbral: {threshold}")
        
        # Generar embedding de la consulta
        query_embedding = await self.embedding_service.generate_embedding(query)
        
        # Calcular similitud con todas las memorias
        similarities = []
        
        for memory_id, memory_embedding in self._vector_store.items():
            memory = await self.db.get(UUID(memory_id))
            
            if not memory or memory.get("is_deleted"):
                continue
            
            similarity = self._cosine_similarity(query_embedding, memory_embedding)
            
            if similarity >= threshold:
                similarities.append({
                    "memory": memory,
                    "similarity": similarity
                })
        
        # Ordenar por similitud
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        print(f"   📊 {len(similarities)} resultados encontrados")
        
        return similarities[:limit]
    
    async def update_memory(
        self,
        memory_id: UUID,
        new_content: Optional[str] = None,
        new_metadata: Optional[dict] = None
    ) -> Optional[dict]:
        """Actualiza una memoria existente."""
        print(f"\n✏️  Actualizando memoria {memory_id}...")
        
        memory = await self.db.get(memory_id)
        
        if not memory:
            print(f"   ❌ Memoria no encontrada")
            return None
        
        # Guardar versión anterior
        version_key = f"{memory_id}_{memory['version']}"
        self.db.versions[version_key] = memory.copy()
        
        # Actualizar campos
        if new_content:
            print(f"   📝 Nuevo contenido: {new_content[:30]}...")
            memory["content"] = new_content
            memory["content_hash"] = hashlib.sha256(new_content.encode()).hexdigest()
            
            # Regenerar embedding
            new_embedding = await self.embedding_service.generate_embedding(new_content)
            self._vector_store[memory_id] = new_embedding
        
        if new_metadata:
            print(f"   📋 Nuevos metadatos: {new_metadata}")
            memory["metadata"].update(new_metadata)
        
        memory["version"] += 1
        memory["updated_at"] = datetime.now().isoformat()
        
        print(f"   ✅ Memoria actualizada (v{memory['version']})")
        
        return memory
    
    async def delete_memory(self, memory_id: UUID, soft: bool = True) -> bool:
        """Elimina una memoria."""
        print(f"\n🗑️  Eliminando memoria {memory_id} (soft={soft})...")
        
        memory = await self.db.get(memory_id)
        
        if not memory:
            print(f"   ❌ Memoria no encontrada")
            return False
        
        if soft:
            memory["is_deleted"] = True
            print(f"   ✅ Eliminación suave completada")
        else:
            del self._vector_store[memory_id]
            await self.db.delete(memory_id)
            print(f"   ✅ Eliminación física completada")
        
        return True
    
    async def get_context_for_llm(
        self,
        query: str,
        max_memories: int = 5,
        max_chars: int = 2000
    ) -> str:
        """Genera contexto de memoria para un LLM."""
        print(f"\n🤖 Generando contexto para LLM...")
        
        results = await self.search_similar(query, limit=max_memories)
        
        if not results:
            return "No hay memorias relevantes disponibles."
        
        context_parts = []
        total_chars = 0
        
        for i, result in enumerate(results):
            memory = result["memory"]
            memory_text = f"[Recuerdo {i+1}] {memory['content']}"
            
            if total_chars + len(memory_text) > max_chars:
                break
            
            context_parts.append(memory_text)
            total_chars += len(memory_text)
        
        header = f"=== CONTEXTO DE MEMORIA ({len(context_parts)} recuerdos) ===\n"
        footer = "\n=== FIN DEL CONTEXTO ==="
        
        return header + "\n\n".join(context_parts) + footer
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calcula similitud coseno."""
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(y * y for y in b) ** 0.5
        return dot_product / (norm_a * norm_b) if norm_a * norm_b > 0 else 0
    
    async def get_statistics(self) -> dict:
        """Obtiene estadísticas del sistema."""
        all_memories = await self.db.list_all()
        active = [m for m in all_memories if not m.get("is_deleted")]
        
        return {
            "total_memories": len(all_memories),
            "active_memories": len(active),
            "deleted_memories": len(all_memories) - len(active),
            "total_embeddings": len(self._vector_store),
            "cache_entries": len(self._cache),
            "total_accesses": sum(m.get("access_count", 0) for m in active)
        }


async def main():
    """Función principal de demostración."""
    
    # Crear sistema
    system = MemoryBankSystem()
    await system.initialize()
    
    # 1. Almacenar memorias
    print("\n" + "=" * 60)
    print("EJERCICIO 1.1: ALMACENAR MEMORIAS")
    print("=" * 60)
    
    memories_data = [
        {
            "content": "Python es un lenguaje de programación de alto nivel creado por Guido van Rossum en 1991. Se caracteriza por su sintaxis clara y legible.",
            "metadata": {"category": "programacion", "language": "python"},
            "tags": ["python", "lenguajes", "programacion"]
        },
        {
            "content": "FastAPI es un framework web moderno y rápido para construir APIs con Python. Soporta validación de datos con Pydantic y generación automática de documentación.",
            "metadata": {"category": "framework", "language": "python"},
            "tags": ["fastapi", "api", "python", "web"]
        },
        {
            "content": "PostgreSQL es un sistema de gestión de bases de datos relacional poderoso y de código abierto. Soporta tipos de datos avanzados y extensiones como pgvector.",
            "metadata": {"category": "database", "type": "relacional"},
            "tags": ["postgresql", "database", "sql"]
        },
        {
            "content": "LangChain es un framework para desarrollar aplicaciones impulsadas por modelos de lenguaje. Proporciona componentes para chain, agents y memory.",
            "metadata": {"category": "ai", "type": "llm-framework"},
            "tags": ["langchain", "ai", "llm"]
        },
        {
            "content": "Docker es una plataforma de contenedorización que permite empaquetar aplicaciones con sus dependencias en contenedores ligeros y portátiles.",
            "metadata": {"category": "devops", "type": "containerization"},
            "tags": ["docker", "containers", "devops"]
        }
    ]
    
    created_ids = []
    for data in memories_data:
        memory = await system.store_memory(
            content=data["content"],
            metadata=data["metadata"],
            tags=data["tags"]
        )
        created_ids.append(UUID(memory["id"]))
    
    # 2. Buscar memorias
    print("\n" + "=" * 60)
    print("EJERCICIO 1.2: BÚSQUEDA SEMÁNTICA")
    print("=" * 60)
    
    queries = [
        "frameworks para Python web",
        "bases de datos relacionales",
        "inteligencia artificial"
    ]
    
    for query in queries:
        results = await system.search_similar(query, limit=2)
        print(f"\nBúsqueda: '{query}'")
        for result in results:
            print(f"  - Similitud: {result['similarity']:.3f}")
            print(f"    {result['memory']['content'][:60]}...")
    
    # 3. Generar contexto para LLM
    print("\n" + "=" * 60)
    print("EJERCICIO 1.3: CONTEXTO PARA LLM")
    print("=" * 60)
    
    context = await system.get_context_for_llm(
        query="tecnologías Python para desarrollo web",
        max_memories=3
    )
    print(context)
    
    # 4. Estadísticas
    print("\n" + "=" * 60)
    print("EJERCICIO 1.4: ESTADÍSTICAS DEL SISTEMA")
    print("=" * 60)
    
    stats = await system.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Ejercicio 2: Optimización de Búsqueda Vectorial

**Enunciado**: Implementa un sistema de indexación optimizado para mejorar el rendimiento de búsquedas vectoriales.

**Solución**:

```python
# ejercicio_2/optimized_vector_search.py

"""
Ejercicio 2: Optimización de búsqueda vectorial
Implementación de índice invertido y cache para mejorar rendimiento.
"""

import asyncio
import time
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib


@dataclass
class VectorIndex:
    """Índice vectorial optimizado con múltiples estrategias."""
    
    vectors: Dict[str, List[float]] = field(default_factory=dict)
    metadata: Dict[str, dict] = field(default_factory=dict)
    inverted_index: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))
    cluster_assignments: Dict[str, int] = field(default_factory=dict)
    cluster_centers: Dict[int, List[float]] = field(default_factory=dict)
    
    # Cache de resultados
    search_cache: Dict[str, Tuple[List[dict], float]] = field(default_factory=dict)
    cache_ttl: float = 300  # 5 minutos
    
    def add_vector(
        self,
        vector_id: str,
        embedding: List[float],
        metadata: dict,
        keywords: Optional[List[str]] = None
    ):
        """Añade un vector al índice."""
        self.vectors[vector_id] = embedding
        self.metadata[vector_id] = metadata
        
        # Indexar por keywords
        if keywords:
            for keyword in keywords:
                if keyword not in self.inverted_index[keyword]:
                    self.inverted_index[keyword].append(vector_id)
    
    def search_by_keyword(
        self,
        keyword: str,
        limit: int = 10
    ) -> List[str]:
        """Búsqueda por índice invertido (keywords exactos)."""
        return self.inverted_index.get(keyword, [])[:limit]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Similitud coseno entre vectores."""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(y * y for y in b) ** 0.5
        return dot / (norm_a * norm_b) if norm_a * norm_b > 0 else 0
    
    def _euclidean_distance(self, a: List[float], b: List[float]) -> float:
        """Distancia euclidiana entre vectores."""
        return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5
    
    def brute_force_search(
        self,
        query: List[float],
        limit: int = 10
    ) -> List[Dict]:
        """Búsqueda por fuerza bruta (baseline)."""
        results = []
        
        for vector_id, embedding in self.vectors.items():
            similarity = self._cosine_similarity(query, embedding)
            results.append({
                "id": vector_id,
                "score": similarity,
                "metadata": self.metadata.get(vector_id, {})
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    def search_cached(
        self,
        query: List[float],
        limit: int = 10
    ) -> List[Dict]:
        """Búsqueda con cache."""
        # Generar clave de cache
        query_hash = hashlib.md5(
            str(query[:100]).encode()  # Usar primeros 100 dims para speed
        ).hexdigest()
        
        # Verificar cache
        if query_hash in self.search_cache:
            results, cache_time = self.search_cache[query_hash]
            if time.time() - cache_time < self.cache_ttl:
                return results[:limit]
        
        # Ejecutar búsqueda
        results = self.brute_force_search(query, limit)
        
        # Guardar en cache
        self.search_cache[query_hash] = (results, time.time())
        
        return results


@dataclass
class HNSWIndex:
    """
    Implementación simplificada de HNSW (Hierarchical Navigable Small World).
    Algoritmo de búsqueda aproximativa de vecindad.
    """
    
    max_layer: int = 16
    m: int = 16  # Conexiones por nodo
    ef_construction: int = 200
    ef_search: int = 100
    
    vectors: Dict[str, List[float]] = field(default_factory=dict)
    layers: List[Dict[str, List[str]]] = field(default_factory=list)  # Una lista de diccionarios por capa
    metadata: Dict[str, dict] = field(default_factory=dict)
    
    def __post_init__(self):
        # Inicializar capas
        self.layers = [defaultdict(list) for _ in range(self.max_layer)]
    
    def add_vector(
        self,
        vector_id: str,
        embedding: List[float],
        metadata: dict
    ):
        """Añade un vector al índice HNSW."""
        self.vectors[vector_id] = embedding
        self.metadata[vector_id] = metadata
        
        # Determinar el nivel máximo para este nodo (usando distribución exponencial)
        import random
        level = 0
        while random.random() < 0.5 and level < self.max_layer - 1:
            level += 1
        
        # Añadir conexiones en cada capa hasta el nivel del nodo
        for layer_idx in range(level + 1):
            self._add_connections_at_layer(vector_id, layer_idx)
    
    def _add_connections_at_layer(self, vector_id: str, layer: int):
        """Añade conexiones en una capa específica."""
        if not self.vectors:
            return
        
        embedding = self.vectors[vector_id]
        candidates = []
        
        # Buscar candidatos más cercanos en esta capa
        for existing_id in self.layers[layer]:
            existing_embedding = self.vectors[existing_id]
            dist = self._euclidean_distance(embedding, existing_embedding)
            candidates.append((dist, existing_id))
        
        candidates.sort(key=lambda x: x[0])
        
        # Conectar con los M más cercanos
        for _, candidate_id in candidates[:self.m]:
            self.layers[layer][vector_id].append(candidate_id)
            self.layers[layer][candidate_id].append(vector_id)
    
    def search(
        self,
        query: List[float],
        limit: int = 10
    ) -> List[Dict]:
        """Busca los K vectores más cercanos usando HNSW."""
        if not self.vectors:
            return []
        
        # Fase 1: Búsqueda ascendente (desde capa más alta)
        current_candidates = set()
        
        # Empezar desde la capa más alta
        for vector_id in self.layers[self.max_layer - 1]:
            current_candidates.add(vector_id)
        
        # Buscar el mejor candidato inicial descendiendo capas
        best_candidates = list(current_candidates)
        
        for layer_idx in range(self.max_layer - 2, -1, -1):
            if not best_candidates:
                continue
            
            # Buscar el más cercano en esta capa
            best = None
            best_dist = float('inf')
            
            for candidate_id in best_candidates:
                dist = self._euclidean_distance(
                    query,
                    self.vectors[candidate_id]
                )
                if dist < best_dist:
                    best_dist = dist
                    best = candidate_id
            
            # Expandir desde el mejor
            if best:
                best_candidates = [best]
                for neighbor in self.layers[layer_idx].get(best, []):
                    best_candidates.append(neighbor)
        
        # Fase 2: Búsqueda greedy en la capa 0
        visited = set()
        candidates = [(self._euclidean_distance(query, self.vectors[v]), v) for v in best_candidates]
        results = []
        
        while candidates and len(results) < limit:
            candidates.sort(key=lambda x: x[0])
            dist, candidate_id = candidates.pop(0)
            
            if candidate_id in visited:
                continue
            
            visited.add(candidate_id)
            results.append({
                "id": candidate_id,
                "score": 1 / (1 + dist),  # Convertir distancia a similitud
                "metadata": self.metadata.get(candidate_id, {})
            })
            
            # Explorar vecinos
            for neighbor in self.layers[0].get(candidate_id, []):
                if neighbor not in visited:
                    dist = self._euclidean_distance(query, self.vectors[neighbor])
                    candidates.append((dist, neighbor))
        
        return results
    
    def _euclidean_distance(self, a: List[float], b: List[float]) -> float:
        """Distancia euclidiana."""
        return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


class SearchOptimizer:
    """Optimizador de búsquedas vectoriales."""
    
    def __init__(self, use_hnsw: bool = True):
        self.index = HNSWIndex() if use_hnsw else VectorIndex()
        self.query_times = []
    
    async def benchmark_search(
        self,
        query: List[float],
        iterations: int = 100
    ) -> Dict:
        """Compara rendimiento de diferentes estrategias."""
        times = []
        
        for _ in range(iterations):
            start = time.time()
            self.index.search(query, limit=10)
            elapsed = time.time() - start
            times.append(elapsed * 1000)  # ms
        
        return {
            "mean_ms": sum(times) / len(times),
            "min_ms": min(times),
            "max_ms": max(times),
            "p50_ms": sorted(times)[len(times) // 2],
            "p95_ms": sorted(times)[int(len(times) * 0.95)],
            "p99_ms": sorted(times)[int(len(times) * 0.99)]
        }


async def main():
    """Demostración de optimización de búsqueda."""
    
    print("=" * 60)
    print("EJERCICIO 2: OPTIMIZACIÓN DE BÚSQUEDA VECTORIAL")
    print("=" * 60)
    
    # Crear índice
    optimizer = SearchOptimizer(use_hnsw=True)
    
    # Añadir vectores de prueba
    print("\n📊 Creando índice con 1000 vectores...")
    
    import random
    random.seed(42)
    
    for i in range(1000):
        embedding = [random.random() for _ in range(128)]
        optimizer.index.add_vector(
            vector_id=f"doc_{i}",
            embedding=embedding,
            metadata={"index": i, "category": f"cat_{i % 10}"}
        )
    
    print(f"   ✅ Índice creado con {len(optimizer.index.vectors)} vectores")
    
    # Benchmark
    query = [random.random() for _ in range(128)]
    
    print("\n⏱️  Ejecutando benchmark (100 iteraciones)...")
    results = await optimizer.benchmark_search(query, iterations=100)
    
    print(f"\n📈 Resultados de rendimiento:")
    print(f"   Media: {results['mean_ms']:.3f} ms")
    print(f"   Mínimo: {results['min_ms']:.3f} ms")
    print(f"   Máximo: {results['max_ms']:.3f} ms")
    print(f"   P50: {results['p50_ms']:.3f} ms")
    print(f"   P95: {results['p95_ms']:.3f} ms")
    print(f"   P99: {results['p99_ms']:.3f} ms")
    
    # Ejemplo de búsqueda
    print("\n🔍 Ejemplo de búsqueda:")
    search_results = optimizer.index.search(query, limit=5)
    
    for i, result in enumerate(search_results):
        print(f"   {i+1}. ID: {result['id']}, Score: {result['score']:.4f}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4. Tecnologías Específicas

### 4.1 Stack Tecnológico Completo

| Componente | Tecnología | Propósito |
|------------|------------|-----------|
| **Base de Datos** | PostgreSQL 15+ con pgvector | Almacenamiento vectorial y relacional |
| **ORM** | SQLAlchemy 2.0 (async) | Abstracción de base de datos |
| **API Framework** | FastAPI | Endpoints REST/WebSocket |
| **Embeddings** | OpenAI text-embedding-ada-002 | Generación de vectores semánticos |
| **Cache** | Redis | Cacheo de consultas frecuentes |
| **Containerización** | Docker + Docker Compose | Despliegue reproducible |
| **Testing** | pytest + pytest-asyncio | Tests unitarios e integración |
| **Migraciones** | Alembic | Control de versiones del schema |
| **Monitoreo** | Prometheus + Grafana | Observabilidad |

### 4.2 Instalación y Configuración

```bash
# requirements.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy[asyncio]==2.0.25
asyncpg==0.29.0
psycopg2-binary==2.9.9
redis==5.0.1
pydantic==2.5.3
pydantic-settings==2.1.0
openai==1.10.0
python-dotenv==1.0.0
httpx==0.26.0
pytest==7.4.4
pytest-asyncio==0.23.3
alembic==1.13.1
python-multipart==0.0.6

# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_USER: memorybank
      POSTGRES_PASSWORD: securepassword
      POSTGRES_DB: memorybank
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U memorybank"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://memorybank:securepassword@postgres:5432/memorybank
      REDIS_URL: redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./src:/app/src
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
  redis_data:
```

---

## 5. Actividades de Laboratorio

### Laboratorio 1: Implementación de Memory Bank Básico (90 minutos)

**Objetivo**: Implementar un sistema básico de Memory Bank con funcionalidad CRUD y búsqueda vectorial.

**Pasos**:

1. **Configurar el entorno** (20 minutos)
   - Crear estructura de proyecto
   - Configurar PostgreSQL con pgvector
   - Configurar variables de entorno

2. **Implementar modelos de datos** (30 minutos)
   - Crear tablas para memorias
   - Implementar índice vectorial
   - Configurar migraciones con Alembic

3. **Implementar API básica** (25 minutos)
   - CRUD de memorias
   - Búsqueda por similitud
   - Tests unitarios

4. **Verificación** (15 minutos)
   - Ejecutar tests
   - Probar endpoints con curl o Swagger UI

**Entregables**:
- Código fuente funcionando
- Documentación de API
- Reporte de problemas encontrados

### Laboratorio 2: Sistema de Contextos para LLM (90 minutos)

**Objetivo**: Implementar un sistema que construya contextos retrieval-augmented para LLMs.

**Pasos**:

1. **Diseñar el sistema de contexto** (20 minutos)
   - Analizar diferentes estrategias de retrieval
   - Diseñar formato de contexto optimizado

2. **Implementar constructor de contexto** (35 minutos)
   - Re-ranker para resultados
   - Compresión de contexto
   - Formateador de salida

3. **Integrar con LLM** (25 minutos)
   - Prompt engineering para contexto
   - Manejo de límites de tokens
   - Fallbacks y errores

4. **Testing y optimización** (10 minutos)
   - Pruebas con diferentes queries
   - Medición de latencia

**Entregables**:
- Módulo de contexto funcional
- Ejemplos de prompts generados
- Análisis de calidad de respuestas

---

## 6. Resumen de Puntos Clave

### Conceptos Fundamentales

1. **Arquitectura de Memory Bank**: Sistema de almacenamiento persistente que permite a aplicaciones de IA mantener contexto entre sesiones mediante vectores semánticos.

2. **pgvector**: Extensión de PostgreSQL que permite almacenar y buscar vectores de alta dimensionalidad directamente en la base de datos.

3. **Estrategias de Chunking**: Métodos para dividir documentos grandes en chunks manejables (por tokens, oraciones, párrafos, secciones).

4. **Búsqueda Híbrida**: Combinación de búsqueda vectorial (semántica) con búsqueda por palabras clave (BM25/keyword).

5. **Control de Versiones**: Sistema de versionado de memorias para trackear cambios y permitir rollback.

### Patrones de Diseño

6. **Repository Pattern**: Abstracción de acceso a datos que permite cambiar la implementación de storage sin afectar la lógica de negocio.

7. **Dependency Injection**: Inyección de dependencias en FastAPI mediante `Depends()` para gestionar servicios.

8. **Async/Await**: Programación asíncrona esencial para manejar múltiples operaciones de I/O concurrently.

9. **Soft Delete**: Eliminación lógica en lugar de física para preservar integridad de datos y permitir auditoría.

### Optimizaciones

10. **Caché de Embeddings**: Cachear embeddings generados para evitar recalcular para contenido idéntico.

11. **Índices Approximados**: Usar HNSW o IVF para acelerar búsquedas en datasets grandes con precisión aceptable.

12. **Connection Pooling**: Reutilizar conexiones a la base de datos para reducir overhead.

### Buenas Prácticas

13. **Schema Validation**: Usar Pydantic para validar datos de entrada/salida.

14. **Error Handling**: Manejo robusto de errores con excepciones específicas.

15. **Logging**: Registrar operaciones para debugging y auditoría.

16. **Tests**: Cobertura de tests unitarios e integración.

---

## 7. Referencias Externas

1. **LangChain Memory Documentation**
   - URL: https://python.langchain.com/docs/modules/memory/
   - Descripción: Documentación oficial de gestión de memoria en LangChain

2. **pgvector GitHub Repository**
   - URL: https://github.com/pgvector/pgvector
   - Descripción: Repositorio oficial con ejemplos y documentación

3. **FastAPI Documentation**
   - URL: https://fastapi.tiangolo.com/tutorial/
   - Descripción: Tutorial oficial de FastAPI con ejemplos de async

4. **PostgreSQL Vector Similarity Search**
   - URL: https://neon.tech/postgresql/postgresql-advanced/postgresql-vector-similarity-search
   - Descripción: Guía de búsqueda vectorial en PostgreSQL

5. **LangChain Vector Stores**
   - URL: https://python.langchain.com/docs/modules/data_connection/vectorstores/
   - Descripción: Integración de vector stores en LangChain

6. **Semantic Search with Embeddings**
   - URL: https://platform.openai.com/docs/guides/embeddings
   - Descripción: Documentación de OpenAI sobre embeddings

7. **HNSW Algorithm Paper**
   - URL: https://arxiv.org/abs/1603.09320
   - Descripción: Paper académico sobre el algoritmo HNSW

8. **Retrieval Augmented Generation (RAG)**
   - URL: https://python.langchain.com/docs/tutorials/rag/
   - Descripción: Tutorial de LangChain sobre RAG

---

**Fin de la Clase 25**
