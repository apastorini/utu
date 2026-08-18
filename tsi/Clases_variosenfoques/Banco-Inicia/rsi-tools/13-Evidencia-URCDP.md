# TOOLS-13 · Evidencia para la URCDP: Documento de Seguridad, ROPA y Notificación

> **Función del MCU 5.0:** Responder (RS) e Identificar (ID) aplicados al cumplimiento de protección de datos personales; soporte documental de la URCDP.
> **ISO/IEC 27001:** La protección de datos personales se integra al SGSI (identificación de requisitos legales, A.5.34–A.5.36).
> **BCU:** La evidencia de protección de datos se cruza con los EMG y con la notificación de incidentes.
> **URCDP:** Ley 18.331 (art. 10 medidas de seguridad, art. 14–17 ARCO, art. 22 inscripción), Ley 19.670 (art. 38 notificación en 72 h) y Decreto 64/020.
> **Nivel del curso:** 🔴 Dominar

---

## 1. La conexión entre las herramientas y la URCDP

Las herramientas de los módulos anteriores **producen la evidencia** que la URCDP y la normativa de protección de datos piden. Este módulo te muestra cómo volcar cada evidencia a los documentos URCDP del kit.

| Evidencia (dónde se produce) | Documento URCDP del kit |
|---|---|
| Inventario de sistemas y activos (Nmap/GLPI, TOOLS-04) | URCDP-01 (Documento de Seguridad) · URCDP-04 (inscripción) |
| Análisis de riesgos (planilla Agesic/Eramba, TOOLS-05) | URCDP-01 (medidas proporcionales) · URCDP-05 (DPIA) |
| Control de accesos y contraseñas (Bitwarden, TOOLS-06) | URCDP-01 (medidas) |
| Cifrado (VeraCrypt/7-Zip, TOOLS-07) | URCDP-01 (medidas técnicas) |
| Concientización (Gophish, TOOLS-08) | URCDP-01 (medidas organizativas) |
| Vulnerabilidades y parches (OpenVAS/Trivy/ZAP, TOOLS-09) | URCDP-01 (medidas técnicas) |
| Logs de acceso y monitoreo (Wazuh/Sysmon, TOOLS-10) | URCDP-01 (trazabilidad) · URCDP-02 (investigación de vulneración) |
| Registro de incidentes (TheHive, TOOLS-11) | URCDP-02 (notificación 72 h) |
| Respaldos (Veeam/Borg, TOOLS-12) | URCDP-01 (disponibilidad/recuperación) |

---

## 2. Preparar el inventario de tratamientos (ROPA)

La URCDP espera conocer **qué bases de datos hay, con qué finalidad, qué datos, quién los trata y con qué medidas**. Para cada sistema que trata datos personales, completá una ficha:

| Campo | De dónde sale |
|---|---|
| Nombre de la base/sistema | Inventario (TOOLS-04) |
| Finalidad del tratamiento | Relevamiento de área (Curso-relevamiento) |
| Datos personales tratados | Relevamiento / dossier por división |
| Categorías especiales (si aplica) | Relevamiento |
| Medidas de seguridad aplicadas | Herramientas PR (TOOLS-06 a TOOLS-09) |
| Plazos de conservación | Documento de Seguridad (URCDP-01) |
| Transferencias (internas/externas) | Relevamiento |

> El ROPA (registro de actividades de tratamiento) se arma con URCDP-01 y URCDP-04.

---

## 3. Cargar la evidencia de las herramientas

Creá una carpeta de evidencia por sistema:

```
04-EVIDENCIA\
├── SISTEMA-01-Core\
│   ├── inventario-nmap.xml
│   ├── riesgo-Eramba-export.csv
│   ├── reporte-openvas.pdf
│   ├── prueba-cifrado.docx.enc.log
│   └── prueba-restauracion-2026-08-06.txt
└── ...
```

Cada evidencia debe llevar: fecha, herramienta, sistema y quién la generó. Esa carpeta es lo que sustentas ante una inspección de la URCDP.

---

## 4. Simular una vulneración y practicar la notificación (72 h)

1. En TheHive (TOOLS-11) abrí un caso simulado: "Acceso no autorizado a base de clientes".
2. Reuní la evidencia: logs de Wazuh (accesos), inventario del sistema, análisis de riesgo.
3. Completá **URCDP-02** (notificación de vulneración): qué pasó, qué datos, alcance, medidas tomadas, medidas para prevenir.
4. Verificá que el borrador está listo para enviarse **dentro de las 72 h** de detectada la vulneración (Ley 19.670 art. 38).

---

## 5. Documento de Seguridad (URCDP-01): el resumen final

Con todo lo anterior, completá URCDP-01 con:

- **Medidas técnicas**: cifrado (TOOLS-07), control de accesos (TOOLS-06), parches (TOOLS-09), monitoreo (TOOLS-10).
- **Medidas organizativas**: concientización (TOOLS-08), roles y responsabilidades (GV-03).
- **Procedimientos**: de respuesta (TOOLS-11), de notificación (URCDP-02), de respaldo (TOOLS-12).
- **Inventario de sistemas** y sus medidas.

---

## 6. Cómo volcarlo a las plantillas del kit

- **URCDP-01 (Documento de Seguridad)**: todas las medidas, procedimientos e inventarios.
- **URCDP-02 (Notificación de Vulneraciones)**: el caso simulado y la práctica de las 72 h.
- **URCDP-05 (Evaluación de Impacto)**: para tratamientos de alto riesgo, con el análisis de riesgos (TOOLS-05).
- **URCDP-04 (Inscripción)**: el inventario de bases alimenta la inscripción de bases de datos.

---

## 7. Lista de verificación del módulo

- ☐ ROPA armado con al menos un sistema real de prueba.
- ☐ Carpeta 04-EVIDENCIA con evidencia de cada función.
- ☐ Caso simulado de vulneración en TheHive.
- ☐ URCDP-02 completado en borrador dentro del plazo de práctica.
- ☐ URCDP-01 con medidas técnicas y organizativas documentadas.

---

**Documentos relacionados:** URCDP-01, URCDP-02, URCDP-04, URCDP-05, RS-02, PR-03
