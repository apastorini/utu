# EV-03 · Sistematización de las Evidencias (cómo guardar, nombrar y seguir)

> **Función del MCU 5.0:** Gobernar (GV.OV) y todas las funciones: la evidencia sistematizada es la prueba del SGSI ante BCU, Agesic, URCDP y auditoría.
> **ISO/IEC 27001:** Cláusula 7.5 (información documentada).
> **BCU:** Los EMG y las inspecciones piden evidencia ordenada, fechada y trazable.
> **URCDP:** Documento de Seguridad y notificaciones requieren evidencia reproducible.
> **Nivel del curso:** 🔴 Dominar · **Uso:** procedimiento de trabajo del RSI.

---

## 1. El problema que resuelve

Sin sistematización, las evidencias se pierden en correos, carpetas personales y capturas sin fecha. Cuando el BCU o la URCDP piden una prueba, el RSI "no la encuentra" o "sabe que existe pero no está documentada". Esto equivale a **no tenerla**.

La sistematización responde a 4 preguntas:

1. **¿Dónde guardar?** → repositorio único de evidencias (EST-CARPETAS-001).
2. **¿Cómo nombrar?** → nomenclatura estándar.
3. **¿Cómo saber el estado?** → planilla de seguimiento de evidencias.
4. **¿Cómo mantenerla?** → ciclo de renovación y validación.

---

## 2. Dónde guardar (repositorio de evidencias)

Siguiendo EST-CARPETAS-001, todas las evidencias van en una única carpeta de evidencia separada de las plantillas:

```
06-CUMPLIMIENTO\
├── 01-URCDP\
│   ├── URCDP-01_Documento-Seguridad\
│   ├── URCDP-02_Vulneraciones\
│   └── ...
├── 02-BCU\
│   ├── BCU-01_Gobierno\
│   ├── BCU-02_Marco-Riesgos\
│   ├── BCU-03_Funcion-Seguridad\
│   ├── BCU-04_Funcion-TI\
│   ├── BCU-05_Auditoria\
│   ├── BCU-06_Continuidad\
│   └── reportes-al-BCU\
├── 03-AUDITORIAS\
│   ├── 2026-01-Auditoria-Interna\
│   └── 2026-02-Auditoria-Externa\
└── 04-EVIDENCIA-GENERAL\
    ├── ID-01_Inventario\
    ├── PR-02_Concientizacion\
    └── ...
```

> Si usás el repositorio por función del MCU 5.0 (00-GOBERNANZA…07-MEJORA), creá en cada función una subcarpeta `04-Evidencia/` para que cada evidencia quede junto a su tema. La regla es **un solo lugar de verdad** y **separación plantilla vs. evidencia**.

---

## 3. Nomenclatura de archivos de evidencia

Formato: `EV-[###]_[CodigoDocumento]_[QueEs]_[AAAA-MM-DD].[ext]`

Ejemplos:

- `EV-012_BCU-06_PruebaRestauracion_2026-08-06.pdf`
- `EV-005_ID-01_ExportInventario-GLPI_2026-07-15.xlsx`
- `EV-023_PR-02_ResultadoSimulacroPhishing_2026-05-20.csv`
- `EV-031_URCDP-01_DocumentoSeguridad-Firmado_2026-04-30.pdf`

Reglas:

- **Un EV por evidencia** (el número sale de la planilla de seguimiento, no al revés).
- **Siempre la fecha** en formato `AAAA-MM-DD` (permite ordenar y saber vigencia).
- **Nada de "final", "final2", "nuevo_final"**: si cambia, se renombra con versión nueva y se registra.
- Las evidencias firmadas/PDF se guardan como tal; los reportes de sistemas se exportan (no capturas de pantalla sueltas si se puede exportar).

---

## 4. Planilla de seguimiento de evidencias (el registro maestro)

Mantené una planilla (LibreOffice Calc/Excel) `Registro-Evidencias.xlsx` con columnas:

| Campo | Ejemplo |
|---|---|
| **ID** | EV-012 |
| **Control / requisito** | BCU-06 · art. 492 (resguardo de datos) |
| **Documento del kit** | BCU-06 §5 · PR-05 |
| **Evidencia pedida** | Prueba de restauración de respaldo |
| **Área responsable** | Div. TI |
| **Formato** | PDF firmado / export |
| **Estado** | Solicitada · Recibida · Validada · Brecha |
| **Fecha pedido** | 2026-07-20 |
| **Fecha recibida** | 2026-07-28 |
| **Validada por** | RSI (nombre) |
| **Fecha de vigencia / próxima revisión** | 2026-11-01 |
| **Ruta** | `06-CUMPLIMIENTO\02-BCU\BCU-06\EV-012_BCU-06_PruebaRestauracion_2026-08-06.pdf` |
| **Observaciones** | Se repite semestral |

> Esta planilla es la **misma** que propone RELEV-07 (estados Solicitada → Recibida → Validada / "No existe → brecha"). La diferencia aquí es que se usa **de forma permanente**, no solo durante el relevamiento.

---

## 5. Ciclo de vida de una evidencia

1. **Definir**: para cada control del EV-02, decidir qué evidencia se pide y su frecuencia.
2. **Solicitar**: pedido por escrito (plantilla RELEV-07) al área responsable.
3. **Recibir**: registrar en la planilla (fecha recibida, formato).
4. **Validar**: ¿fechada? ¿íntegra? ¿trazable? ¿de la fuente correcta? (atributos INFRA-08).
5. **Guardar**: copiar al repositorio con la nomenclatura EV y actualizar la ruta.
6. **Renovar**: según la frecuencia del control (mensual/semestral/anual), pedir la actualización antes de que venza.
7. **Archivar/descartar**: las versiones viejas se archivan (no se borran) con la fecha; se conserva la retención definida (ver §6).

---

## 6. Retención de evidencias

| Tipo de evidencia | Retención sugerida |
|---|---|
| Logs de eventos (Decreto 66/025) | ≥ 12 meses |
| Evidencias de respaldo / restauración | 2 ciclos + 12 meses |
| Notificaciones a URCDP/BCU/CERTuy | 5 años |
| Documentos firmados del SGSI (políticas, actas) | 5 años (o el plazo legal mayor) |
| Informes de auditoría | 5 años |
| Evidencias de concientización | 2 años |

> Verificá siempre los plazos legales vigentes (URCDP, BCU, Agesic) y la política de retención del Banco. Lo que no se conserva, no se puede demostrar.

---

## 7. Herramientas para sistematizar (open source, del curso rsi-tools)

| Herramienta | Para qué |
|---|---|
| **GLPI** (TOOLS-04) | Inventario de activos y tickets (evidencia de gestión) |
| **Eramba / planilla** (TOOLS-05) | Registro de riesgos y tratamientos (evidencia ID) |
| **Vaultwarden/Bitwarden** (TOOLS-06) | Custodia de claves de repositorios cifrados |
| **VeraCrypt/7-Zip** (TOOLS-07) | Cifrar el repositorio de evidencias confidenciales |
| **Wazuh** (TOOLS-10) | Logs y alertas (evidencia DE, retención) |
| **TheHive** (TOOLS-11) | Casos de incidentes (evidencia RS) |
| **Veeam/BorgBackup** (TOOLS-12) | Respaldo del propio repositorio de evidencias |
| **Obsidian/Joplin/LibreOffice** (TOOLS-03) | Índice y edición de la documentación |

---

## 8. Cómo presentar las evidencias ante un supervisor o auditor

1. **Resumen ejecutivo** (1 página): qué control demuestra cada evidencia (usá EV-01/EV-02).
2. **MATRIZ-001**: mapa norma → documento → evidencia.
3. **Índice de evidencias**: la planilla de seguimiento filtrada por requisito.
4. **Las evidencias mismas**: abiertas, legibles, con fecha visible.
5. **Si falta algo**: mostrá la brecha, el riesgo asociado (ID-02/03) y el plan de cierre (ID-04/GV-04). Un supervisor valora más la honestidad con plan que la evidencia falsa.

---

## 9. Checklist de cierre del RSI

- ☐ El repositorio de evidencias sigue EST-CARPETAS-001 (un solo lugar de verdad).
- ☐ Todas las evidencias tienen nomenclatura `EV-[###]_...`.
- ☐ La planilla de seguimiento está actualizada (estados, fechas, rutas).
- ☐ Cada control del EV-02 tiene su evidencia elegida y solicitada.
- ☐ Las evidencias se renuevan según frecuencia y están validadas.
- ☐ El repositorio está respaldado (TOOLS-12) y las claves custodiadas (TOOLS-06).
- ☐ Se puede presentar un expediente completo en menos de 1 día hábil.

---

**Documentos relacionados:** EST-CARPETAS-001, INFRA-08, RELEV-07, EV-01, EV-02, EV-04, EV-05, MATRIZ-001, TOOLS-04/05/06/07/10/11/12
