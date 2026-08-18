# VPOL-21 · Correspondencia normativa y checklist final

> **Función del MCU 5.0:** Todas — este módulo integra Gobernar, Proteger, Detectar, Responder y Recuperar
> **ISO/IEC 27001:** Trazabilidad entre políticas y controles del Anexo A
> **BCU:** Correspondencia con los EMG y el RNRCSF
> **URCDP:** Correspondencia con la Ley 18.331
> **Nivel del curso:** 🔴 Dominar

---

## 1. Correspondencia de las 15 plantillas con los marcos

| Plantilla | MCU 5.0 | ISO/IEC 27001 | BCU | URCDP |
|---|---|---|---|---|
| 01 · Acceptable Use | GV.OR, PR.AC | A.5.10, A.8.1 | EMG-gobierno | arts. 9-10 |
| 02 · AI Acceptable Use | GV.OR, GV.RM | A.5.9, A.8.12 | EMG-gobierno | art. 10 |
| 03 · Change Management | PR.PS | A.8.32 | EMG, C.2280 | art. 10 |
| 04 · Clear Desk | PR.PS | A.7.7 | EMG | art. 10 |
| 05 · Cloud Usage | GV.OR, PR.DS | A.5.19-21, A.8.11 | EMG, C.2280 | arts. 10, 27-bis |
| 06 · Data Backup | RC.RP, PR.DS | A.8.13 | RNRCSF | art. 10 |
| 07 · Classification | ID.RA, PR.DS | A.5.9, A.5.12 | EMG | art. 10 |
| 08 · Info Security (madre) | GV.OR | cláusula 5.2, A.5.1 | EMG | art. 10 |
| 09 · Logging & Monitoring | DE.AE, DE.CM | A.8.15-17 | EMG | arts. 10, 27-bis |
| 10 · Network Security | PR.AC, PR.PS | A.8.20-23 | EMG, C.2280 | art. 10 |
| 11 · Personnel Security | GV.OR, PR.AT | A.6.1-6 | EMG | art. 10 |
| 12 · Removable Media | PR.DS | A.8.3, A.8.10 | EMG | arts. 10, 27-bis |
| 13 · Third-Party Mgmt | GV.RM | A.5.19-23 | EMG, C.2280 | arts. 10, 27-bis |
| 14 · User Access Mgmt | PR.AC | A.5.15-18, A.8.5 | EMG | art. 10 |
| 15 · Vulnerability Mgmt | PR.PS, DE.CM | A.8.8, A.8.9 | EMG, RNRCSF | art. 10 |

## 2. Checklist del ciclo completo del curso

### A. Gestión de vulnerabilidades (enfoque Uruguay)
- [ ] Inventario de activos (ID-01) actualizado y clasificado.
- [ ] Escaneo periódico definido (frecuencia, herramienta, alcance).
- [ ] Criterios de priorización por CVSS + contexto.
- [ ] Plazos de corrección por criticidad definidos (y aprobados).
- [ ] Ventanas de mantenimiento y prueba en homologación.
- [ ] Proceso de excepciones con aceptación del riesgo residual.
- [ ] Verificación post-parcheo con escaneo puntual.
- [ ] KPIs definidos y reportados al Comité.

### B. Redacción de políticas, procesos y controles
- [ ] Política madre (VPOL-13) aprobada por el Directorio.
- [ ] 15 plantillas ISACA completadas con los `[COMPLETAR]` del Banco.
- [ ] Cada política con objetivo, alcance, roles, reglas, cumplimiento y revisión.
- [ ] Cada política con su proceso operativo (quién, cómo, plazos, salidas).
- [ ] Cada proceso con sus controles (preventivo/detectivo/correctivo).
- [ ] Cada control con su evidencia (fecha, alcance, herramienta, resultado).
- [ ] Relación política ↔ proceso ↔ control ↔ evidencia documentada.
- [ ] Publicación en el SGSI + control de cambios (GV-06).

### C. Cumplimiento normativo
- [ ] Mapeo a MCU 5.0 (Agesic) verificado.
- [ ] Mapeo a ISO/IEC 27001 (Anexo A) verificado.
- [ ] Mapeo a los EMG del BCU verificado.
- [ ] Ley 18.331 (URCDP) contemplada, incluida la notificación de vulneraciones.
- [ ] Revisión anual programada para cada política.

## 3. Próximos pasos en el kit
1. Completá las plantillas en `templates-ISACA/` y convertí a `.docx` con `md_a_docx.py`.
2. Integrá cada política con su documento canónico de `02-ENTREGABLES/`.
3. Practicá la redacción con la **actividad 44** del curso RSI (políticas/procesos/controles).
4. Practicá la **actividad 45** (direccionamiento IP v4/v6, NAT y firewall/WAF en modo bloqueo).
5. Reportá las métricas de vulnerabilidades en el **tablero de KPIs** (actividad 43).
