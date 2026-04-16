# PLANTILLA SGSI - SISTEMA DE GESTIÓN DE SEGURIDAD DE LA INFORMACIÓN

**Versión:** 1.0  
**Fecha:** 2026  
**Organización:** [NOMBRE DE LA ORGANIZACIÓN]  
**Clasificación:** Confidencial

---

## ÍNDICE

1. Contexto de la Organización
2. Liderazgo y Compromiso
3. Política de Seguridad
4. Planificación del SGSI
5. Soporte
6. Operación
7. Evaluación del Desempeño
8. Mejora Continua
9. Anexos

---

## 1. CONTEXTO DE LA ORGANIZACIÓN

### 1.1. Información General

| Campo | Descripción |
|-------|-------------|
| **Razón Social** | |
| **RUT** | |
| **Actividad Principal** | |
| **Dirección** | |
| **Teléfono** | |
| **Email** | |
| **Sitio Web** | |
| **Cantidad de empleados** | |
| **Sedes** | |

### 1.2. Alcance del SGSI

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALCANCE DEL SGSI                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INCLUIDOS:                                                    │
│  ├── [Sede Central]                                          │
│  ├── [Sede Sucursal 1]                                       │
│  ├── [Sede Sucursal 2]                                       │
│  ├── [Data Center Principal]                                   │
│  └── [Data Center Secundario]                                 │
│                                                                 │
│  SISTEMAS INCLUIDOS:                                          │
│  ├── Sistema de Core Bancario                                   │
│  ├── Sistema de Canales Digitales                              │
│  ├── Sistema de Gestión de Riesgos                            │
│  └── Red de Comunicaciones                                    │
│                                                                 │
│  EXCLUIDOS:                                                   │
│  └── [Justificación de exclusiones]                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3. Partes Interesadas

| Parte Interesada | Expectativas | Requisitos de Seguridad |
|-----------------|-------------|------------------------|
| Clientes | Confidencialidad de datos | Ley 18.331, BCU |
| BCU | Cumplimiento regulatorio | Comunicación BCU |
| ACCIONISTAS | Protección de activos | Gobierno corporativo |
| EMPLEADOS | Ambiente seguro | Contratos, políticas |
| PROVEEDORES | Seguridad de servicios | Contratos SLAs |
| SOCIEDAD | Estabilidad financiera | Responsabilidad social |

---

## 2. LIDERAZGO Y COMPROMISO

### 2.1. Dirección

| Rol | Nombre | Cargo | Email |
|-----|--------|-------|-------|
| **Director General** | | | |
| **CISO / Responsable Seguridad** | | | |
| **Director TI** | | | |
| **DPO** | | | |
| **Director de Riesgos** | | | |

### 2.2. Comité de Seguridad

| Miembro | Rol | Frecuencia Reuniones |
|---------|----|---------------------|
| | Presidente | Mensual |
| | Secretaria | Mensual |
| | Miembro | Mensual |
| | Miembro | Mensual |
| | Miembro | Mensual |

### 2.3. Compromiso de la Dirección

```
ACTA DE COMPROMISO DE LA DIRECCIÓN
═══════════════════════════════════════════════════════════════

Fecha: [FECHA]
Lugar: [LUGAR]

En [LUGAR], siendo las [HORA], se reúne el Comité de Dirección
de [ORGANIZACIÓN] para tratar el establecimiento del Sistema de
Gestión de Seguridad de la Información (SGSI).

ACUERDA:

1. Establecer, implementar, mantener y mejorar continuamente un
   Sistema de Gestión de Seguridad de la Información conforme a
   ISO/IEC 27001:2022.

2. Asignar los recursos humanos, tecnológicos y presupuestales
   necesarios para el funcionamiento del SGSI.

3. Designar al responsable de seguridad de la información
   con autoridad y recursos para cumplir sus funciones.

4. Revisar el desempeño del SGSI al menos una vez al año.

5. Asegurar que la política de seguridad sea comunicada a
   todos los colaboradores y partes interesadas relevantes.

Firmado:

_________________________
[NOMBRE]
Director General

_________________________
[NOMBRE]
CISO / Responsable Seguridad
```

---

## 3. POLÍTICA DE SEGURIDAD

### 3.1. Política General de Seguridad

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    POLÍTICA DE SEGURIDAD DE LA INFORMACIÓN                 ║
║                           [ORGANIZACIÓN]                                  ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  1. OBJETIVO                                                           ║
║     Establecer un marco de gestión de la seguridad de la información      ║
║     que proteja los activos de información de la organización.            ║
║                                                                           ║
║  2. ALCANCE                                                            ║
║     Esta política aplica a todas las actividades, procesos y sistemas      ║
║     de la organización, incluyendo personal interno, proveedores          ║
║     y terceros.                                                         ║
║                                                                           ║
║  3. PRINCIPIOS                                                          ║
║     • Confidencialidad: Proteger información sensible                    ║
║     • Integridad: Garantizar exactitud de los datos                    ║
║     • Disponibilidad: Asegurar acceso cuando se requiera                ║
║     • Cumplimiento: Observar leyes y regulaciones aplicables            ║
║     • Mejora continua: Evaluar y mejorar constantemente                  ║
║                                                                           ║
║  4. ROLES Y RESPONSABILIDADES                                          ║
║     • Dirección: Aprobar recursos y revisar desempeño                   ║
║     • CISO: Gestionar el SGSI                                          ║
║     • Todo el personal: Cumplir políticas y reportar incidentes         ║
║                                                                           ║
║  5. CUMPLIMIENTO                                                       ║
║     El incumplimiento de esta política será sancionado según             ║
║     el reglamento interno y normativa aplicable.                        ║
║                                                                           ║
║  Fecha de aprobación: ___________                                       ║
║  Fecha de revisión: ___________                                          ║
║  Versión: 1.0                                                          ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### 3.2. Políticas Específicas

| Política | Código | Versión | Fecha |
|---------|--------|---------|-------|
| Política de Control de Acceso | POL-001 | | |
| Política de Uso de Recursos | POL-002 | | |
| Política de Contraseñas | POL-003 | | |
| Política de Internet y Email | POL-004 | | |
| Política de Datos Personales | POL-005 | | |
| Política de BYOD | POL-006 | | |
| Política de Respuesta a Incidentes | POL-007 | | |
| Política de Continuidad | POL-008 | | |

---

## 4. PLANIFICACIÓN DEL SGSI

### 4.1. Evaluación de Riesgos

| Elemento | Descripción |
|----------|-------------|
| **Metodología** | ISO 27005 / NIST SP 800-30 |
| **Criterios de aceptación** | Riesgo residual ≤ Nivel aceptable |
| **Frecuencia** | Anual o ante cambios significativos |
| **Responsable** | CISO / Equipo de Seguridad |

### 4.2. Evaluación de Riesgos - Metodología

```
EVALUACIÓN DE RIESGOS
═══════════════════════════════════════════════════════════════

PROBABILIDAD (1-5):
1 = Muy baja (menos de 1 vez/año)
2 = Baja (1-2 veces/año)
3 = Media (trimestral)
4 = Alta (mensual)
5 = Muy alta (semanal/diario)

IMPACTO (1-5):
1 = Muy bajo (menor a USD 1,000)
2 = Bajo (USD 1,000 - 10,000)
3 = Medio (USD 10,000 - 100,000)
4 = Alto (USD 100,000 - 1,000,000)
5 = Muy alto (mayor a USD 1,000,000)

NIVEL DE RIESGO = PROBABILIDAD × IMPACTO
1-8   = BAJO (aceptable)
9-15  = MEDIO (requiere tratamiento)
16-25 = ALTO (requiere tratamiento urgente)

RIESGO RESIDUAL = RIESGO - CONTROLES EXISTENTES
```

### 4.3. Registro de Activos

| ID | Activo | Tipo | Propietario | Criticidad | Ubicación |
|----|--------|------|-------------|-----------|-----------|
| AST-001 | Base de datos clientes | Información | Gerencia Riesgo | Crítica | Data Center |
| AST-002 | Servidor Core Banking | Sistema | Dirección TI | Crítica | Data Center |
| AST-003 | Red corporativa | Servicio | Dirección TI | Alta | Todas las sedes |
| AST-004 | Equipos de trabajo | HW | RRHH | Media | Sucursales |
| AST-005 | Aplicación mobile | Sistema | Canales Digitales | Alta | Cloud |

---

## 5. SOPORTE

### 5.1. Recursos

| Tipo | Recurso | Responsable |
|------|---------|-------------|
| **Humano** | Equipo de seguridad (X personas) | CISO |
| **Tecnológico** | Herramientas SIEM, EDR, FW | Dirección TI |
| **Financiero** | Presupuesto anual USD | Dirección |
| **Tiempo** | X horas/mes para SGSI | Todos |

### 5.2. Competencia y Concienciación

| Tipo | Descripción | Frecuencia | Registro |
|------|-------------|------------|---------|
| Capacitación新入 | 온보딩 seguridad | Al ingreso | SIGC-001 |
| Taller práctico | Phishing, contraseñas | Trimestral | SIGC-002 |
| Simulacro | Ejercicio de respuesta | Semestral | SIGC-003 |
| Actualización | Cambios normativos | Anual | SIGC-004 |

---

## 6. OPERACIÓN

### 6.1. Gestión de Riesgos

| ID | Amenaza | Activo | Prob | Impact | Riesgo | Controles | Res.idual | Tratamiento |
|----|--------|-------|------|--------|--------|---------|-----------|------------|
| R-001 | Ransomware | Sistemas críticos | 3 | 5 | 15 | Backup, EDR, MFA | 8 | Mitigar |
| R-002 | Acceso no autorizado | Base datos | 3 | 4 | 12 | RBAC, MFA, Logs | 6 | Mitigar |
| R-003 | Phishing | Usuarios | 4 | 3 | 12 | Filtros, Capacitación | 6 | Mitigar |
| R-004 | DDoS | Web | 2 | 4 | 8 | CDN, WAF | 4 | Aceptar |

### 6.2. Declaración de Aplicabilidad

```
╔═══════════════════════════════════════════════════════════════════════════╗
║              DECLARACIÓN DE APLICABILIDAD - Anexo A ISO 27001              ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  A.5 - Controles organizacionales                                       ║
║  ├─ A.5.1 Políticas de seguridad ✓                                     ║
║  ├─ A.5.2 Roles y responsabilidades ✓                                  ║
║  ├─ A.5.3 Segregación de funciones ✓                                  ║
║  └─ A.5.4 Contacto con autoridades ✗ N/A                               ║
║                                                                           ║
║  A.6 - Controles humanos                                               ║
║  ├─ A.6.1 Selección de personal ✓                                      ║
║  ├─ A.6.2 Capacitación ✓                                              ║
║  └─ A.6.3 Terminación ✓                                               ║
║                                                                           ║
║  A.7 - Controles físicos                                               ║
║  ├─ A.7.1 Seguridad de instalaciones ✓                                 ║
║  └─ A.7.2 Seguridad de equipos ✓                                       ║
║                                                                           ║
║  A.8 - Controles tecnológicos                                         ║
║  ├─ A.8.1 Gestión de activos ✓                                        ║
║  ├─ A.8.2 Cifrado ✓                                                  ║
║  ├─ A.8.3 Gestión de vulnerabilidades ✓                                ║
║  └─ A.8.4 Gestión de incidentes ✓                                     ║
║                                                                           ║
║  ✓ = Aplicable    ✗ = No aplicable    ─ = Excluido                    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 7. EVALUACIÓN DEL DESEMPEÑO

### 7.1. Indicadores Clave

| Indicador | Meta | Frecuencia | Responsable |
|-----------|------|------------|-------------|
| Incidentes críticos | 0 | Mensual | CISO |
| Hallazgos pendientes | < 5 | Mensual | CISO |
| Personal capacitado | > 90% | Trimestral | RRHH |
| Uptime sistemas críticos | > 99.99% | Mensual | TI |
| Cobertura antivirus | > 99% | Mensual | TI |

### 7.2. Auditorías

| Tipo | Frecuencia | Auditor | Último | Próximo |
|------|-------------|---------|--------|----------|
| Interna | Anual | Equipo interno | [FECHA] | [FECHA] |
| Externa | Anual | [AUDITORA] | [FECHA] | [FECHA] |
| Certificación | 3 años | [CERTIFICADORA] | - | [FECHA] |

---

## 8. MEJORA CONTINUA

### 8.1. No Conformidades

| ID | No Conformidad | Fecha | Severidad | Causa | Acción | Estado |
|----|----------------|------|-----------|-------|--------|--------|
| NC-001 | | | | | | |
| NC-002 | | | | | | |

### 8.2. Acciones Correctivas

| ID | Acción | Responsable | Fecha Inicio | Fecha Cierre | Eficacia |
|----|--------|-------------|--------------|--------------|-----------|
| AC-001 | | | | | |
| AC-002 | | | | | |

---

## 9. ANEXOS

### Anexo A: Glosario
### Anexo B: Referencias Normativas
### Anexo C: Organigrama de Seguridad
### Anexo D: Matriz de Roles y Responsabilidades
### Anexo E: Inventario de Activos
### Anexo F: Plan de Tratamiento de Riesgos

---

**Documento:** Plantilla SGSI - Sistema de Gestión de Seguridad de la Información  
**Versión:** 1.0  
**Elaborado por:**   
**Revisado por:**   
**Aprobado por:**   
**Fecha:**   
