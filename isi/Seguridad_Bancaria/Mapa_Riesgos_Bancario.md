# Mapa de Riesgos de Seguridad Bancaria

## Introducción

El presente documento establece el mapa de riesgos de seguridad de la información para instituciones bancarias uruguayas, alineado con las normativas del Banco Central del Uruguay (BCU), la Ley 18.331 de Protección de Datos Personales y las mejores prácticas internacionales.

Este mapa debe ser revisado y actualizado trimestralmente por el Comité de Seguridad de la Información.

---

## 1. Taxonomía de Riesgos

### 1.1 Categorías Principales

| Código | Categoría | Descripción |
|--------|-----------|-------------|
| R-INFO | Riesgos de Información | Compromiso de confidencialidad, integridad o disponibilidad de datos |
| R-TEC | Riesgos Tecnológicos | Fallos en sistemas, infraestructura o servicios tecnológicos |
| R-OPE | Riesgos Operativos | Errores humanos, procesos deficientes o fallas en operaciones |
| R-FIS | Riesgos Físicos | Acceso no autorizado a instalaciones, robo de equipos |
| R-LEG | Riesgos Legales/Regulatorios | Incumplimiento de normativas, sanciones |
| R-FRA | Riesgos de Fraude | Actividades fraudulentas internas o externas |
| R-REP | Riesgos de Reputación | Daño a la imagen institucional |

### 1.2 Subcategorías de Riesgos de Información

| Código | Subcategoría | Descripción |
|--------|---------------|-------------|
| R-INFO-01 | Divulgación no autorizada | Exposición de datos sensibles a terceros no autorizados |
| R-INFO-02 | Modificación no autorizada | Alteración de datos sin autorización válida |
| R-INFO-03 | Destrucción de datos | Eliminación o corrupción de información crítica |
| R-INFO-04 | Intercepción de comunicaciones | Captura no autorizada de datos en tránsito |
| R-INFO-05 | Suplantación de identidad | Uso ilegítimo de credenciales de otros usuarios |

---

## 2. Matriz de Riesgo

### 2.1 Escala de Probabilidad

| Nivel | Valor | Descripción | Frecuencia esperada |
|-------|-------|-------------|---------------------|
| Muy Baja | 1 | Improbable que ocurra | < 1 vez cada 5 años |
| Baja | 2 | Poco probable pero posible | 1 vez cada 2-5 años |
| Media | 3 | Podría ocurrir en某些 circunstancias | 1 vez cada 1-2 años |
| Alta | 4 | Probable que ocurra | Varias veces al año |
| Muy Alta | 5 | Ocurrencia casi segura | Continuamente/mensualmente |

### 2.2 Escala de Impacto

| Nivel | Valor | Descripción | Impacto financiero | Impacto reputacional |
|-------|-------|-------------|-------------------|---------------------|
| Muy Bajo | 1 | Incidente menor, sin afect复ón significativa | < USD 10,000 | Mínimo, controlable internamente |
| Bajo | 2 | Afect复ón局部, manejo interno | USD 10,000 - 50,000 | Limitado, manejable |
| Medio | 3 | Afect复ón significativa, comunicación necesaria | USD 50,000 - 250,000 | Moderado, requiere gestión de medios |
| Alto | 4 | Impacto sustancial, posible intervención regulatoria | USD 250,000 - 1,000,000 | Significativo, afecta confianza |
| Muy Alto | 5 | Crisis organizacional, posible liquidación | > USD 1,000,000 | Crítico, pérdida de clientes |

### 2.3 Matriz de Valoración de Riesgos

```
         Impacto
         1     2     3     4     5
Prob  ┌─────┬─────┬─────┬─────┬─────┐
  5   │  5  │ 10  │ 15  │ 20  │ 25  │
      ├─────┼─────┼─────┼─────┼─────┤
  4   │  4  │  8  │ 12  │ 16  │ 20  │
      ├─────┼─────┼─────┼─────┼─────┤
  3   │  3  │  6  │  9  │ 12  │ 15  │
      ├─────┼─────┼─────┼─────┼─────┤
  2   │  2  │  4  │  6  │  8  │ 10  │
      ├─────┼─────┼─────┼─────┼─────┤
  1   │  1  │  2  │  3  │  4  │  5  │
      └─────┴─────┴─────┴─────┴─────┘
```

### 2.4 Clasificación del Nivel de Riesgo

| Rango | Nivel | Color | Acciones requeridas |
|-------|-------|-------|---------------------|
| 1-4 | Bajo | Verde | Monitoreo continuo, revisar annually |
| 5-9 | Medio | Amarillo | Plan de mitig复ón en 6 meses |
| 10-14 | Alto | Naranja | Plan de mitig复ón inmediata, supervisión del Comité |
| 15-25 | Crítico | Rojo | Acción inmediata, escalamiento a Dirección |

---

## 3. Inventario de Riesgos Identificados

### 3.1 Riesgos de Ciberseguridad

| ID | Riesgo | Prob | Imp | Valor | Nivel | Controles actuales |
|----|--------|------|-----|-------|-------|-------------------|
| CIB-001 | Ransomware bancario | 3 | 5 | 15 | Crítico | Antimalware, backups, segmentación |
| CIB-002 | Phishing a empleados | 4 | 3 | 12 | Alto | Capacitación, filtros de correo, MFA |
| CIB-003 | Ataque DDoS | 3 | 4 | 12 | Alto | WAF, CDN, planos de respuesta |
| CIB-004 | Breach de datos de clientes | 2 | 5 | 10 | Alto | Cifrado, DLP, control de acceso |
| CIB-005 | Compromiso de credenciales API | 3 | 4 | 12 | Alto | Rotación de claves, monitoreo |
| CIB-006 | Vulnerabilidad zero-day | 2 | 5 | 10 | Alto | Gestión de parches, detección |
| CIB-007 | Ataque a cadena de suministro | 2 | 4 | 8 | Medio | Verificación de proveedores |
| CIB-008 | Insider malicioso | 1 | 5 | 5 | Medio | Control de acceso privilegiado, auditoría |
| CIB-009 | Exfiltración de datos | 2 | 4 | 8 | Medio | DLP, monitoreo DLP |
| CIB-010 | Compromiso de endpoints | 4 | 3 | 12 | Alto | EDR, gestión de dispositivos |

### 3.2 Riesgos Operativos

| ID | Riesgo | Prob | Imp | Valor | Nivel | Controles actuales |
|----|--------|------|-----|-------|-------|-------------------|
| OPE-001 | Falla de sistemas core banking | 2 | 5 | 10 | Alto | Alta disponibilidad, DRP |
| OPE-002 | Error humano en transacciones | 4 | 2 | 8 | Medio | Validaciones, segregación de funciones |
| OPE-003 | Falla de proveedor crítico | 3 | 4 | 12 | Alto | Due diligence, SLA, backup |
| OPE-004 | Indisponibilidad de personal clave | 3 | 2 | 6 | Medio | Sucesión, documentación |
| OPE-005 | Falla de telecomunicaciones | 3 | 3 | 9 | Medio | Redundancia, failover |

### 3.3 Riesgos de Fraude

| ID | Riesgo | Prob | Imp | Valor | Nivel | Controles actuales |
|----|--------|------|-----|-------|-------|-------------------|
| FRA-001 | Fraude en canales digitales | 4 | 4 | 16 | Crítico | MFA, biometría, monitoreo transaccional |
| FRA-002 | Fraude interno | 2 | 5 | 10 | Alto | Segregación, auditoría |
| FRA-003 | Fraude en pagos (SWIFT) | 2 | 5 | 10 | Alto | Controles SWIFT, dual control |
| FRA-004 | Robo de identidad de clientes | 3 | 4 | 12 | Alto | Verificación reforzada |
| FRA-005 | Lavado de dinero | 3 | 4 | 12 | Alto | AML, SAR, monitoreo |

### 3.4 Riesgos Regulatorios

| ID | Riesgo | Prob | Imp | Valor | Nivel | Controles actuales |
|----|--------|------|-----|-------|-------|-------------------|
| REG-001 | Incumplimiento BCU | 2 | 5 | 10 | Alto | Cumplimiento normativo, auditoria |
| REG-002 | Sanción por breach de datos | 2 | 4 | 8 | Medio | GovSec, cumplimiento legal |
| REG-003 | Incumplimiento PCI-DSS | 2 | 4 | 8 | Medio | Implementación PCI |
| REG-004 | Multas por demora en notificaciones | 3 | 2 | 6 | Medio | Procedimientos de breach |

---

## 4. Mapa de Calor

```
┌─────────────────────────────────────────────────────────────┐
│                    MAPA DE CALOR DE RIESGOS                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   IMPACTO ALTO                                               │
│      │                                                      │
│   5  │  [OPE-004]                                           │
│      │                                                      │
│   4  │  [CIB-003] [CIB-005]        [FRA-001]                │
│      │  [OPE-003] [CIB-010]        [FRA-004]               │
│      │  [FRA-004] [FRA-005]        [FRA-003]                │
│      │  [REG-003]                                          │
│      │                                                      │
│   3  │  [CIB-002] [CIB-010]        [CIB-001]                │
│      │  [OPE-005]                                          │
│      │                                                      │
│   2  │  [OPE-002] [REG-004]                                 │
│      │                                                      │
│   1  │                                                      │
│      └────────────────────────────────────────              │
│         1    2    3    4    5                                │
│                      PROBABILIDAD                            │
│                                                             │
│   [ZONA CRÍTICA - Accion inmediata]                          │
│   [ZONA ALTA - Plan de mitig复ón urgente]                    │
│   [ZONA MEDIA - Monitoreo y planific复ón]                    │
│   [ZONA BAJA - Acept复ón de riesgo]                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Planes de Mitigación

### 5.1 Riesgos Críticos (Valor 15-25)

| ID | Riesgo | Plan de mitigación | Responsable | Plazo |
|----|--------|-------------------|-------------|-------|
| CIB-001 | Ransomware | 1. Implementar backup inmutable<br>2. Segmentar redes<br>3. Simular ejercicios de ransomware<br>4. Contrato con empresa de respuesta | CISO | 3 meses |
| FRA-001 | Fraude digital | 1. Implementar biometría comportamental<br>2. Reforzar autenticación multifactor<br>3. ML para detección de anomalías<br>4. Límites dinámicos | Fracción Fraude | 6 meses |

### 5.2 Riesgos Altos (Valor 10-14)

| ID | Riesgo | Plan de mitigación | Responsable | Plazo |
|----|--------|-------------------|-------------|-------|
| CIB-002 | Phishing | 1. Simulaciones mensuales<br>2. Sandbox de correo<br>3. Passkeys | Seguridad Info | 3 meses |
| CIB-003 | DDoS | 1. Contratar servicio anti-DDoS<br>2. Plan de respuesta<br>3. Pruebas de stress | Infraestructura | 3 meses |
| CIB-004 | Breach datos | 1. Cifrado a nivel de columna<br>2. Tokenización de datos sensibles<br>3. DAM | DPO/Seg Info | 6 meses |
| CIB-005 | Credenciales API | 1. Implementar API Gateway<br>2. Rotación automática<br>3. Monitoreo de uso anómalo | Desarrollo | 4 meses |
| CIB-006 | Zero-day | 1. Suscripción a Threat Intel<br>2. Parches emergency<br>3. Isolación de red | Seguridad Info | 2 meses |
| CIB-010 | Endpoints | 1. EDR en todos los equipos<br>2. Response automation<br>3. Hardening | Infraestructura | 3 meses |
| OPE-001 | Fail sistemas core | 1. Revisar RTO/RPO<br>2. Prueba de failover semestral<br>3. Contratar DRaaS | Infraestructura | 6 meses |
| OPE-003 | Fail proveedor | 1. Inventario de proveedores críticos<br>2. Contratos con SLA<br>3. Plan B documentado | Compras/OPS | 4 meses |
| FRA-003 | Fraude SWIFT | 1. CSP obligatorio<br>2. Dual control<br>3. Transacciones anómalas alertadas | Operaciones | 3 meses |
| FRA-004 | Robo identidad | 1. KYC reforzado<br>2. Notificaciones proactivas<br>3. Verificación en tiempo real | Fracción Fraude | 6 meses |
| FRA-005 | Lavado dinero | 1. Actualizar modelo AML<br>2. SAR automatizados<br>3. Capacitación AML | Cumplimiento | 4 meses |
| REG-001 | Incumplimiento BCU | 1. Gap analysis normativo<br>2. Implementar controles faltantes<br>3. Auditoria interna | Cumplimiento | 6 meses |

---

## 6. Monitoreo y Revisión

### 6.1 Indicadores Clave de Riesgo (KRI)

| KRI | Descripción | Umbral verde | Umbral amarillo | Umbral rojo |
|-----|-------------|--------------|-----------------|-------------|
| KRI-01 | # incidentes ransomware/mes | 0 | 1 | > 1 |
| KRI-02 | Tiempo promedio de detección | < 24h | 24-72h | > 72h |
| KRI-03 | % sistemas sin parches críticos | < 5% | 5-15% | > 15% |
| KRI-04 | # fraudes digitales/mes | < 10 | 10-25 | > 25 |
| KRI-05 | % empleados capacitados | > 95% | 80-95% | < 80% |
| KRI-06 | # hallazgos críticos abiertos | 0 | 1-3 | > 3 |

### 6.2 Frecuencia de Revisión

| Tipo de revisión | Frecuencia | Participantes |
|------------------|------------|---------------|
| Monitoreo KRI | Semanal | Equipo Seguridad |
| Revisión de incidentes | Diaria | SOC |
| Comité de Riesgos | Mensual | CISO, AUD, Cumplimiento |
| Revisión integral | Trimestral | Comité de Dirección |
| Auditoría externa | Anual | Auditor externo |

---

## 7. Gobernanza

### 7.1 Roles y Responsabilidades

| Rol | Responsabilidades |
|-----|------------------|
| Directorio | Aprobación final del apetito de riesgo |
| Comité de Riesgos | Supervisión y aprobación de mitigaciones |
| CISO | Gestión día a día, reporteo, respuesta |
| DPO | Cumplimiento de protección de datos |
| Área de Cumplimiento | Control normativo |
| AUD | Auditoría independiente |
| Unidades de Negocio | Implementación de controles |

### 7.2 Aprobaciones

| Versión | Fecha | Aprobado por | Cargo |
|---------|-------|--------------|-------|
| 1.0 | DD/MM/AAAA | [Nombre] | Directorio/CISO |
| | | | |
| | | | |

---

## 8. Anexo: Glosario

| Término | Definición |
|---------|------------|
| KRI | Key Risk Indicator - Indicador clave de riesgo |
| RTO | Recovery Time Objective - Tiempo máximo de recuperación |
| RPO | Recovery Point Objective - Pérdida máxima de datos aceptable |
| SOC | Security Operations Center - Centro de operaciones de seguridad |
| DLP | Data Loss Prevention - Prevención de pérdida de datos |
| EDR | Endpoint Detection and Response - Detección y respuesta en endpoints |
| AML | Anti-Money Laundering - Contra el lavado de dinero |
| KYC | Know Your Customer - Conoce a tu cliente |
| SAR | Suspicious Activity Report - Reporte de actividad sospechosa |
| CSP | Customer Security Program - Programa de seguridad del cliente (SWIFT) |

---

**Documento preparado para:** [Nombre de la Institución Bancaria]
**Versión:** 1.0
**Clasificación:** Confidencial
**Próxima revisión:** [Fecha + 3 meses]
