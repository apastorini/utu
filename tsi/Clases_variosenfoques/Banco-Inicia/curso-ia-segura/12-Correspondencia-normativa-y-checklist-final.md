# AISEC-12 · Correspondencia normativa y checklist final

> **Función del MCU 5.0:** Este módulo cierra el curso vinculando cada aprendizaje con los requisitos auditables: funciones GV/ID/PR/DE/RS/RC y dominios transversales CN y PD del Marco de Ciberseguridad de Agesic 5.0.
> **ISO/IEC 27001:** Control A.5.31 (requisitos legales) y A.5.34 (protección de datos personales): la correspondencia permite demostrar cumplimiento con evidencia.
> **BCU:** Los EMG y el RNRCSF exigen demostrar la gestión del riesgo de IA con evidencia.
> **URCDP:** Los requisitos PD del MCU 5.0 y la Ley 18.331/Ley 19.670 quedan aterrizados en controles verificables.
> **Nivel del curso:** 🔴 Dominar

---

## 1. Correspondencia normativa completa

| Tema del curso | Norma / requisito | Evidencia a presentar |
|---|---|---|
| Herramientas autorizadas | EMG, RNRCSF, A.5.9, GV-02 | Inventario de herramientas de IA autorizadas |
| Política de uso | templates-ISACA-02, VPOL-07, GV-01 | Política aprobada y firmada |
| Datos que entran | PD.1, PD.3, PD.6, A.5.31 | Matriz de clasificación de datos (módulo 06) |
| Minimización | PD.2, Ley 18.331 art. 9 | Guía de anonimización y ejemplos |
| Seguridad del ecosistema | PD.5, A.8.12, A.8.20-A.8.21, PR | Configuración DLP, firewall, segmentación |
| Modelos locales | A.8.8, PR.06 | Registro de versiones y parches de Ollama/vLLM |
| RAG | PD.3, PD.5, PD.7, A.5.12 | Registro de documentos indexados y filtros por rol |
| Revisión humana | A.5.15, RS-02 | Procedimiento de revisión documentado |
| Monitoreo | DE-01/DE-03, A.8.15-A.8.16 | Reportes de logs, DLP, tráfico |
| Incidentes | RS-02, Decreto 64/020, Decreto 66/025 | Registro de incidentes y notificaciones |
| Capacitación | A.6.3, PR.AT, Ley 19.670 | Registro de capacitación de 300 funcionarios |
| EIPD | PD.7, Ley 19.670 | Evaluaciones de impacto aprobadas |
| Gobierno | GV-01 a GV-03, ISO 42001 | Política, actas, matriz de roles y responsabilidades |
| Auditoría | CN.1-CN.3, EV-01 a EV-05 | Informes de auditoría y matrices de evidencia |

---

## 2. Checklist final del curso (para cada rol)

### Para todos los funcionarios
- [ ] Conozco la herramienta oficial (BigPickle) y sé abrirla.
- [ ] Conozco las reglas de oro de datos (tabla 🟢/🟡/🔴).
- [ ] Sé anonimizar y cuándo preguntar al DPD.
- [ ] Reviso siempre los resultados de la IA antes de usarlos.
- [ ] Firmé la política de uso aceptable de IA.
- [ ] Sé a quién avisar ante una sospecha o un incidente.

### Para desarrollo / TI
- [ ] OpenCode configurado contra el servicio interno (no a internet).
- [ ] Trabajo solo con datos de desarrollo/QA, nunca producción.
- [ ] Reviso el diff antes de aceptar cambios.
- [ ] El RAG respeta roles y registra fuentes.

### Para el RSI
- [ ] Inventario de herramientas de IA actualizado.
- [ ] Política de IA aprobada, comunicada y archivada.
- [ ] EIPD realizados para usos con datos personales.
- [ ] Logs, DLP y monitoreo activos.
- [ ] Plan de respuesta ante incidentes de IA probado.
- [ ] Matriz de evidencia completa (módulo 09).
- [ ] Reporte de indicadores a dirección.

---

## 3. Checklist operativo de control

### Semanal
- [ ] Revisar alertas DLP y tráfico hacia IA externa.
- [ ] Confirmar que no hay extensiones de IA nuevas en los equipos.

### Mensual
- [ ] Revisar logs de uso de BigPickle/OpenCode (patrones anómalos).
- [ ] Verificar actualizaciones de Ollama, vLLM y modelos.
- [ ] Actualizar el inventario de herramientas.

### Trimestral
- [ ] Revisar roles y permisos de los usuarios de IA.
- [ ] Revisar documentos indexados en el RAG (retirar vencidos).
- [ ] Probar prompt injection sobre el RAG y las herramientas.

### Anual
- [ ] Revisar y volver a aprobar la política de IA.
- [ ] Repetir la capacitación (al menos una píldora de actualización).
- [ ] Auditar el uso de IA e informar a dirección.
- [ ] Actualizar la matriz de correspondencia normativa.

---

## 4. Respuestas a los ejercicios

### Módulo 06 (clasificar datos)
1. "Cliente con 90 días de mora en sucursal 3" → 🟡 Condicionado (puede combinarse e identificar; requiere anonimización o permiso).
2. "Juan Pérez, 4.500 USD de deuda" → 🔴 Prohibido (dato personal identificable).
3. "Borrador de correo de bienvenida a nuevos clientes (sin datos)" → 🟢 Seguro.
4. "código del módulo de liquidación de intereses" → 🟡 Condicionado (solo OpenCode en entorno de desarrollo; nunca herramientas externas).

---

## 5. Cierre del curso

Usted terminó el curso **"Inteligencia artificial y ciberseguridad: usar la IA bien, sin filtrar nada"**. Lo que debe quedarse grabado:

1. **La IA es una herramienta de redacción, no una fuente de verdad**: se revisa siempre.
2. **El dato que identifica a una persona no entra por chat**: anonimizar o no usar.
3. **La herramienta oficial existe para que no necesite otra**: úsela y pida mejoras.
4. **Las fugas se evitan con cultura, no solo con tecnología**: política + capacitación + monitoreo + alternativa.
5. **Todo queda documentado**: ese es el expediente que responde ante URCDP, BCU y Agesic.

> **La regla de oro final:** en el Banco, la IA se usa con la herramienta oficial, con los datos que la política autoriza, y siempre con revisión humana. Lo que no está autorizado, no se hace — ni "por única vez". Si algún día la herramienta oficial no le alcanza, se pide por el canal formal; la respuesta llega y, mientras tanto, se espera. Proteger los datos de los clientes es proteger la confianza en el Banco.
