# AISEC-08 · Guía técnica para TI y RSI: implementación segura

> **Función del MCU 5.0:** Este módulo es el manual técnico para proteger (PR), detectar (DE) y responder (RS) en el ecosistema de IA del Banco, con evidencia para auditoría (GV, CN).
> **ISO/IEC 27001:** Controles de red (A.8.20-A.8.21), prevención de fuga de datos (A.8.12), gestión de vulnerabilidades (A.8.8), registros (A.8.15-A.8.16), gestión de incidentes (A.5.24) y seguridad en el desarrollo (A.8.25-A.8.28).
> **BCU:** La implementación técnica de la IA debe estar documentada en los EMG y el RNRCSF, con trazabilidad y evidencia.
> **URCDP:** Seguridad de los datos (PD.5) y registro de tratamientos. La infraestructura de IA es parte del Documento de Seguridad.
> **Nivel del curso:** 🔴 Dominar

---

## 1. Principios de diseño (arquitectura)

| Principio | Descripción | Control ISO 27001 |
|---|---|---|
| **Confidencialidad por defecto** | El dato no sale de la infraestructura del Banco salvo autorización formal | A.8.12, A.8.20 |
| **Aislamiento** | La IA no tiene acceso directo a sistemas productivos (cuentas, pagos, core) | A.8.21, A.8.23 |
| **Menor privilegio** | Cada usuario/rol ve solo lo que necesita | A.5.15, A.8.2-A.8.3 |
| **Trazabilidad total** | Todo uso queda en logs auditables | A.8.15-A.8.16 |
| **Revisión humana** | Nada ejecutable sin aprobación humana | A.5.15, A.5.24 |
| **Fuentes controladas** | Solo documentos internos autorizados entran al RAG | A.5.12, A.8.25 |

---

## 2. Implementación del ecosistema (Ollama + vLLM + BigPickle + OpenCode)

### 2.1 Infraestructura

1. **Servidores de inferencia**: máquinas con GPU dedicadas en el datacenter del Banco (o nube contratada con contrato de protección de datos y residencia definida).
2. **Modelos locales (Ollama)**: se descargan versiones **verificadas y con hash** desde fuentes confiables; se mantienen actualizadas.
3. **vLLM**: expone el modelo como servicio interno con autenticación y limitación de concurrencia.
4. **BigPickle**: interfaz web interna (solo accesible por la red/VPN del Banco), con autenticación por usuario.
5. **OpenCode**: instalado en estaciones de desarrollo, apuntando al servicio interno vLLM.

### 2.2 Configuración de seguridad mínima

- [ ] Autenticación de todos los usuarios (SSO del Banco, MFA).
- [ ] Trazabilidad: registro de cada consulta (usuario, fecha, herramienta, modelo, resumen).
- [ ] **No logging de datos personales**: los logs guardan metadatos, no el contenido de los datos protegidos. Si se guarda el prompt, se anonimiza o se protege en acceso restringido.
- [ ] Límites de uso por usuario/rol (evita extracción masiva).
- [ ] Bloqueo de salida: las herramientas locales **no se conectan a internet** para tareas con datos confidenciales.
- [ ] Actualizaciones y parches de los servidores de IA (gestión de vulnerabilidades).

### 2.3 RAG seguro

1. **Repositorio controlado**: solo documentos internos clasificados y aprobados.
2. **Troceado + vectorización** con embeddings internos.
3. **Base de vectores** en la red del Banco.
4. **Filtro por rol**: cada consulta solo recupera documentos que el rol puede ver.
5. **Registro de fuentes**: se guarda qué documentos respondieron cada consulta.
6. **Revisión periódica**: retirar documentos vencidos (PD.2, PD.8).

---

## 3. Red, firewall y DLP para la IA

| Acción | Detalle |
|---|---|
| **Lista blanca de dominios** | Solo dominios de IA autorizados (si los hay); todo el resto de servicios de IA externos se bloquea en el proxy/firewall |
| **DLP (prevención de fuga de datos)** | Reglas que detectan patrones de datos personales (cédula, tarjetas) en salidas a la web y las bloquean (control A.8.12) |
| **Segmentación** | La red de IA está segmentada; solo los puertos necesarios abiertos (A.8.20) |
| **Registro de tráfico** | Logs de conexiones hacia servicios de IA externos (detección de shadow IA) |
| **VPN** | El acceso remoto a las herramientas de IA solo por VPN corporativa |

---

## 4. Monitoreo y detección (DE)

### Señales de alerta a monitorear (SIEM / logs)

- Conexiones a dominios de IA **no autorizados** (shadow IA).
- Consultas de un usuario con **volumen anómalo** (posible exfiltración).
- Patrones típicos de **prompt injection** en prompts (frases de "ignorá tus instrucciones").
- Intentos de acceso a documentos del RAG fuera del rol.
- Uso fuera de horario habitual (abuso de credenciales).

### Respuesta ante hallazgo

1. **Contener**: bloquear acceso del usuario/tool.
2. **Clasificar**: ¿es incidente de seguridad de datos? ¿Notificable a URCDP (72 h, Decreto 64/020) o al CERTuy (Decreto 66/025)?
3. **Investigar** con los logs.
4. **Corregir** y documentar (RS-02).
5. **Comunicar** según el plan de gestión de incidentes.

---

## 5. Gestión de modelos y vulnerabilidades

| Tarea | Frecuencia |
|---|---|
| Verificar hash/integridad de modelos descargados | En cada descarga |
| Actualizar modelos y software (Ollama, vLLM, OpenCode) | Mensual / cuando haya parches críticos |
| Escanear vulnerabilidades de los servidores de IA | Continuo (igual que el resto de activos) |
| Revisar permisos y roles de los usuarios de IA | Trimestral |
| Prueba de prompt injection sobre el RAG y las herramientas | En cada cambio / semestral |

---

## 6. Evidencias que debe guardar el RSI

| Evidencia | Qué demuestra | Requisito asociado |
|---|---|---|
| Inventario de herramientas de IA autorizadas | Control de activos (no hay shadow IA) | A.5.9, GV-02 |
| Política de uso aceptable de IA firmada | Marco de uso permitido | templates-ISACA-02, VPOL-07 |
| Contrato/protección de datos con proveedores de nube (si aplica) | Base legal y garantías | A.5.31-A.5.35, PD.5 |
| Documento de seguridad actualizado con el ecosistema IA | Seguridad de los tratamientos | URCDP, Decreto 64/020 |
| Logs de consultas (metadatos) | Trazabilidad | A.8.15-A.8.16 |
| Registro de documentos indexados en el RAG | Minimización y finalidad | PD.3, PD.5 |
| Resultado de pruebas de prompt injection | Protección de la aplicación | A.8.26-A.8.28 |
| Registro de capacitación del personal | Concienciación | A.6.3 |
| Reporte de incidentes asociados a IA | Respuesta | RS-02, Decreto 64/020, Decreto 66/025 |

---

## 7. Checklist de implementación (para TI/RSI)

- [ ] Servidores de IA desplegados en la red del Banco (o nube contratada con garantías).
- [ ] Ollama + vLLM configurados y actualizados.
- [ ] BigPickle desplegado con SSO/MFA y límites por rol.
- [ ] OpenCode configurado contra el servicio interno.
- [ ] RAG implementado con filtro por roles y registro de fuentes.
- [ ] Dominios externos de IA bloqueados en proxy/firewall.
- [ ] DLP activo con reglas de datos personales.
- [ ] Logs de uso habilitados (metadatos).
- [ ] Política de uso aceptable aprobada y comunicada.
- [ ] EIPD realizado antes de habilitar usos con datos personales (PD.7).
- [ ] Capacitación del personal realizada y registrada.
- [ ] Plan de respuesta ante incidentes de IA probado.

---

## 8. Conclusión del módulo

- La seguridad de la IA se diseña por **defecto**: aislamiento, menor privilegio, trazabilidad y revisión humana.
- El ecosistema (Ollama, vLLM, BigPickle, OpenCode) se despliega **dentro de la red del Banco**, con bloqueo de salidas no autorizadas.
- El **DLP y el monitoreo** detectan shadow IA, exfiltración y prompt injection.
- **Toda decisión técnica queda documentada**: esa documentación es la evidencia que Agesic, BCU y URCDP van a pedir.

> **Ejercicio (TI/RSI):** Arme el inventario de herramientas de IA actuales del Banco (autorizadas y las que aparezcan). Para cada una, indique: qué datos puede recibir, dónde se procesa, quién tiene acceso y qué evidencia deja. Ese cuadro es la base de los módulos 09 y 12.
