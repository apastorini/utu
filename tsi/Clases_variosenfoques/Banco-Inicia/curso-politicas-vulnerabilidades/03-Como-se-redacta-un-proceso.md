# VPOL-03 · Cómo se redacta un proceso de seguridad

> **Función del MCU 5.0:** Detectar (DE.CM — monitoreo) · Responder (RS) · Recuperar (RC) · Gobernar (GV)
> **ISO/IEC 27001:** A.5.22 (selección de controles) · A.8.8 (gestión de vulnerabilidades) · A.16 (gestión de incidentes)
> **BCU:** EMG — procesos formalizados para gestionar el riesgo tecnológico y la continuidad
> **URCDP:** Ley 18.331 art. 10 y régimen de notificación de vulneraciones (procesos obligatorios)
> **Nivel del curso:** 🟡 Practicar → 🔴 Dominar

---

## 1. ¿Qué es un proceso?

Un **proceso** describe **cómo** se cumple una política: secuencia ordenada de actividades, con responsables, plazos, entradas y salidas. Mientras la política dice "los parches críticos se aplican en 72 h", el proceso dice *quién* detecta, *cómo* se prioriza, *quién* aprueba la ventana, *cómo* se verifica y *qué* se registra.

> La política es el **destino**; el proceso es el **mapa** para llegar.

## 2. Estructura estándar de un proceso

| Bloque | Contenido |
|---|---|
| Objetivo y alcance | Para qué sirve y a qué activos/servicios aplica |
| Entradas | Documentos, datos o señales que disparan el proceso (ej. reporte de escaneo, alerta SIEM) |
| Actividades numeradas | Pasos 1..N, cada uno con responsable y plazo |
| Salidas | Entregables que produce (ej. informe de parcheo, ticket cerrado) |
| Responsables | Rol que ejecuta, rol que aprueba, rol que audita |
| Indicadores (KPIs) | Cómo se mide que el proceso funciona |
| Referencias | Políticas y documentos relacionados |
| Registros | Evidencia que queda documentada (logs, tickets, actas) |

## 3. Cómo escribir cada actividad

Formato de una actividad dentro del proceso:

> **1.3 — Verificar parcheo en el activo afectado.**
> - **Responsable:** Administrador de Sistemas.
> - **Entrada:** ticket de parcheo con CVE y activo.
> - **Pasos:** (a) validar que el parche está instalado, (b) ejecutar un escaneo puntual del activo, (c) registrar el resultado en el ticket.
> - **Salida:** ticket cerrado con evidencia de escaneo.
> - **Plazo:** dentro de las 24 h posteriores a la aplicación.

## 4. Ejemplo completo resumido

**Proceso: Gestión de vulnerabilidades críticas (complementa PR-06)**

1. Detectar hallazgo crítico (escaneo mensual, alerta CERTuy, aviso de proveedor). — *RSI/Operaciones de Seguridad*
2. Confirmar la vulnerabilidad y el activo afectado (cruzando con ID-01). — *Operaciones de Seguridad*
3. Priorizar: CVSS + contexto (exposición, datos, exploit activo). — *RSI*
4. Elegir tratamiento: parchear / mitigación temporal / excepción. — *RSI + Jefe de Riesgos*
5. Aplicar el parche en ventana (o mitigación inmediata). — *Administrador de Sistemas*
6. Verificar (escaneo puntual + prueba de servicio). — *Administrador de Sistemas*
7. Registrar y medir (ticket, KPI, revisión mensual). — *RSI*

## 5. Errores comunes al redactar procesos

- ❌ Sin responsables explícitos → nadie es dueño.
- ❌ Sin plazos → nunca es "urgente".
- ❌ Sin salidas/registros → no hay evidencia para el auditor.
- ❌ Sin indicadores → no se sabe si funciona.
- ❌ Confundir proceso con procedimiento (el procedimiento es más detallado: pasos a nivel de pantalla/comando).

## 6. Cómo se evidencian los procesos en el kit

| Proceso | Evidencia en el kit |
|---|---|
| Gestión de vulnerabilidades | PR-06 (política) + registros de OpenVAS/Trivy + tickets |
| Gestión de incidentes | RS-01, DE-01, DE-02 + alertas del SIEM (Wazuh) |
| Gestión de accesos | PR-01 + solicitudes/aprobaciones + revisión de cuentas |
| Respaldos | PR-05, RC-02 + logs de backup + pruebas de restauración |
| Notificación de vulneraciones | URCDP-02 + registro de incidentes y acta de notificación |

> **Recuerde:** un proceso que no produce registros es un proceso que no existe a los ojos del auditor.
