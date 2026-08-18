# PRO-03 · Procedimiento: Configuración Segura de Estaciones y Servidores (Hardening)

> **Función del MCU 5.0:** Proteger (PR.AC — configuración; PR.IP — líneas base de configuración)
> **ISO/IEC 27001:** A.8.9 (gestión de configuración) · A.8.10 (borrado seguro) · A.8.17-A.8.20 (protección del ciclo de vida de los sistemas)
> **BCU:** EMG — configuración segura y gestión de vulnerabilidades
> **URCDP:** Ley 18.331 art. 10 — medidas técnicas para proteger datos personales
> **Nivel del curso:** 🟡 Practicar

---

## 1. Objetivo y alcance
Aplicar una **configuración de referencia segura** a estaciones de trabajo, notebooks, servidores, equipos de red y bases de datos, reduciendo la superficie de ataque. Aplica a todos los equipos del Banco, incluyendo el entorno de desarrollo de IA (curso AISEC).

## 2. Responsables
- **Div. TI (Administración de sistemas)**: implementa las líneas base.
- **RSI**: define las líneas base, revisa y audita.
- **Seguridad de Red** (si aplica): equipos de red.

## 3. Entradas
- Línea base de configuración por tipo de equipo (basada en guías CIS o de fabricante, adaptada).
- Inventario de equipos (POL-03, ID-01).
- Procedimiento de gestión de vulnerabilidades (PRO-07).

## 4. Línea base mínima de configuración
| Elemento | Requisito mínimo |
|---|---|
| **Sistema operativo** | Versiones soportadas y parcheadas |
| **Cuentas locales** | Deshabilitar invitado; contraseñas según POL-04 |
| **Servicios y puertos** | Solo los necesarios; cerrar el resto |
| **Antivirus/EDR** | Instalado, activo y actualizado (POL-05) |
| **Firewall local** | Activo con reglas mínimas |
| **Cifrado** | Disco cifrado (POL-14) |
| **Autenticación** | Bloqueo de pantalla, MFA donde aplique (POL-04) |
| **Registro de eventos** | Activado y centralizado (POL-06) |
| **Actualizaciones** | Automáticas/repositorio controlado (POL-15) |
| **Software no autorizado** | Bloqueado por whitelist (POL-02) |

## 5. Desarrollo paso a paso
1. **RSI publica** la línea base vigente y su versión.
2. **Div. TI aplica** la línea base en equipos nuevos y existentes (imagen estándar + política de configuración).
3. **Div. TI registra** el equipo y su versión de configuración en el inventario.
4. **RSI realiza** verificaciones técnicas (escaneo) y revisa desvíos.
5. Los desvíos justificados se aprueban como **excepción temporal** con vigencia y responsable.
6. En el **entorno de IA** (curso AISEC-07/AISEC-08), se endurece la configuración de modelos y servidores que los sirven.
7. **Registrar** cualquier cambio a la línea base (control de cambios — POL-15).

## 6. Salidas y registros
- Línea base de configuración (versión vigente).
- Verificaciones y escaneos de hardening.
- Registro de excepciones.
- Reporte de cumplimiento periódico.

## 7. Errores comunes
- Aplicar la línea base "de memoria" sin documentarla.
- No auditar los equipos viejos no alcanzados por la imagen.
- Excepciones sin vencimiento.

## 8. Referencias y evidencia
POL-03 · POL-05 · POL-15 · PRO-07. Alimenta: PR-03 (configuración), ID-01, hallazgos de BCU.
