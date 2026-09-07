# Tarea 2 — Sistema de Gestión Integrada para el RSI

## Contenido

- **`LETRA.md`** — La letra completa de la tarea: marco teórico, glosario, requerimientos funcionales/no funcionales, arquitectura sugerida, Partes Blue Team y Red Team, matriz de documentación, hitos, KPIs y criterios de evaluación.
- **`docs/`** — Carpeta de trabajo del equipo para la documentación de la solución.

## Cómo empezar

1. Lea `LETRA.md` completo.
2. Revise la matriz de documentación (sección 8) para saber qué plantilla llenar en cada semana.
3. Copie de `../plantilla/isaca/` las plantillas indicadas a su carpeta `docs/`.
4. Trabaje en su repositorio GIT y congele la entrega con `git tag v1.0` en el hito H4.

## Documentación que debe entregar (resumen)

| Fecha | Documento |
|---|---|
| Semana 1 (14-18/09) | Arquitectura (4+1 y C4), modelo de datos, política, inventario de activos, Excel activos |
| Semana 2 (21-25/09) | Análisis de riesgos, Excel controles MCU (Avanzado) |
| Semana 3-4 (28/09-02/10) | Gestión de accesos (TOTP/WebAuthn/Hello/Argon2), monitoreo/logs, bitácora |
| Semana 5 (05-07/10) | Vulnerabilidades, plan de continuidad, SoA + brecha MCU, notificaciones |
| **Miércoles 07/10/2026** | **Pre-entrega congelada** (`git tag v1.0`) + Excel/bitácora completos |
| **Miércoles 14/10/2026** | **Auditoría formal por función MCU 5.0 (defensa)** + demo de exportadores |
| **Miércoles 28/10/2026** | **Pre-entrega Red Team** (informe preliminar ≥ 70%) |
| **Lunes 09/11/2026** | **Entrega final Red Team** (informe `plantilla/informe-red-team.md` + presentación) |

> **Obligatorio**: demostrar en la auditoría la exportación en vivo de al menos 3 documentos (MCU 5.0 perfil Avanzado, SoA ISO 27001, reporte BCU).

- **Equipo A (Blue Team):** construye el sistema y rinde la auditoría (semana del 14/09 al 14/10).
- **Equipo B (Red Team):** ataca el sistema entregado (28/10 → 09/11) y emite informe.