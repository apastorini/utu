# TOOLS-09 · Vulnerabilidades y Parches: OpenVAS, Trivy, OWASP ZAP, Semgrep

> **Función del MCU 5.0:** Proteger (PR.PS) y Detectar (DE.CM): gestión de vulnerabilidades y parches.
> **ISO/IEC 27001:** Anexo A.8.8 (gestión de vulnerabilidades técnicas) y A.8.31 (separación de entornos).
> **BCU:** La guía EMG y el art. 492 exigen un proceso de gestión de vulnerabilidades con evidencia (BCU-04).
> **URCDP:** Las vulnerabilidades no parcheadas son la principal causa de filtraciones de datos personales; mitigarlas es una medida de seguridad (art. 10).
> **Nivel del curso:** 🔴 Dominar

---

## 1. Qué es y para qué sirve

| Herramienta | Tipo | Para qué |
|---|---|---|
| **OpenVAS (Greenbone)** | Escáner de vulnerabilidades de red | Descubrir CVEs y debilidades en sistemas y servicios |
| **Trivy** | Escáner de imágenes/containers | Vulnerabilidades en Docker, Helm, dependencias (útil si el Banco usa contenedores) |
| **OWASP ZAP** | DAST (web) | Probar aplicaciones web en busca de fallas (inyección, XSS, etc.) |
| **Semgrep** | SAST (código) | Analizar código fuente buscando patrones inseguros |

> **Regla de oro:** el ciclo es **escanear → priorizar → corregir (patch) → re-escanear → evidenciar**. Los escaneos se hacen en entornos de prueba y sobre sistemas autorizados.

---

## 2. Instalar OpenVAS (Greenbone) en la VM

La forma más simple es con Docker (la imagen `greenbone/gvm`):

```bash
# Con Docker del TOOLS-06
sudo mkdir -p /opt/gvm
cd /opt/gvm
sudo docker run -d --name gvm -p 443:443 -p 9392:9392 \
  -v /opt/gvm/data:/data greenbone/gvm
```

Accedé a `https://<IP-de-la-VM>:9392` (usuario `admin`, la clave te la muestra el log de arranque; o configurala en el primer inicio). La primera sincronización de la base de CVE puede tardar.

> ⚠️ La primera vez Greenbone descarga la base de vulnerabilidades (puede tardar 20–60 min). Dale tiempo y actualizala periódicamente.

### Primer escaneo

1. **Configuration → Targets → New Target**: nombre `Lab-Red`, hosts `192.168.1.0/24` (o el rango del laboratorio).
2. **Scans → Tasks → New Task**: elegí el target y un scan config por defecto.
3. **Play** (▶) la tarea. Esperá el resultado.
4. **Reports**: abrí el reporte → verás hosts con su **CVSS** y las vulnerabilidades detectadas.

---

## 3. Instalar Trivy (containers)

```bash
sudo apt install -y wget
wget -qO - https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo bash

# Escanear una imagen de prueba
trivy image alpine:3.18
# Escanear un proyecto
trivy fs /ruta/al/proyecto
```

---

## 4. Instalar OWASP ZAP

### Windows (puesto del RSI)

```powershell
winget install OWASP.ZAP
```

### Primer uso (modo asistido)

1. Abrí **ZAP** → **Automated Scan** (o Quick Start).
2. URL de prueba: un sitio web de práctica autorizado (ej. el "WebGoat" o "bWAPP" del laboratorio) o una app interna de pruebas.
3. **Attack** → ZAP recorre la app (spider) y la ataca con su conjunto de pruebas.
4. En **Alerts** vas a ver las fallas con su severidad. **Report → Generate Report** → HTML (evidencia).

---

## 5. Instalar Semgrep (SAST)

```bash
# En Windows
pip install semgrep

# En Linux/VM
sudo apt install -y python3-pip
pip3 install semgrep
```

### Primer escaneo

```bash
# Reglas por defecto sobre un proyecto de prueba
semgrep scan --config auto /ruta/al/proyecto
```

El reporte muestra los hallazgos por regla (falta de validación, SQL injection, etc.).

---

## 6. Priorizar: CVSS y contexto

Usá la escala CVSS v3.1 para priorizar:

| Severidad | Rango CVSS | Plazo sugerido de parche |
|---|---|---|
| Crítico | 9.0–10.0 | Inmediato (máx. 7 días) |
| Alto | 7.0–8.9 | Máx. 30 días |
| Medio | 4.0–6.9 | Según plan |
| Bajo | 0.1–3.9 | A revisar |

> El parche se prueba en el laboratorio (TOOLS-02) antes de producción, y se documenta en PR-06.

---

## 7. Cómo volcarlo a las plantillas del kit

- **PR-06 (Gestión de Vulnerabilidades)**: el proceso (escanear, priorizar, parchear, re-escanear) y los reportes como evidencia.
- **PR-07 (Desarrollo Seguro / SDLC)**: Semgrep (SAST) y ZAP (DAST) se integran en el ciclo de desarrollo.
- **DE-03 (Pruebas de Seguridad)**: los reportes de OpenVAS y ZAP sustentan el programa de pruebas.
- **BCU-04 / ID-04**: la evidencia de parcheo y tratamiento.

---

## 8. Lista de verificación del módulo

- ☐ OpenVAS (Greenbone) corriendo y con la base de CVE actualizada.
- ☐ Target y tarea de escaneo creados; al menos un escaneo completado.
- ☐ Reporte OpenVAS exportado (PDF/XML).
- ☐ Trivy instalado y un escaneo de imagen de prueba.
- ☐ OWASP ZAP instalado y una app de prueba atacada.
- ☐ Semgrep instalado y un escaneo de un proyecto de prueba.
- ☐ Vulnerabilidades priorizadas por CVSS y volcadas a PR-06 (borrador).

---

**Documentos relacionados:** PR-06, PR-07, DE-03, ID-04, BCU-04, URCDP-01
