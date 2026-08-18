# TOOLS-11 · Respuesta a Incidentes: TheHive + Cortex, Volatility, Autopsy

> **Función del MCU 5.0:** Responder (RS.MA, RS.AN): respuesta a incidentes y análisis forense.
> **ISO/IEC 27001:** Anexo A.5.24–A.5.28 (plan de respuesta, gestión de incidentes, lecciones aprendidas) y A.5.9 (evidencia).
> **BCU:** La guía EMG y la Circular 2227 exigen gestión de incidentes y respuesta ante el BCU.
> **URCDP:** Ley 19.670 art. 38 exige **notificar vulneraciones** de datos personales en 72 h; el registro de incidentes y la evidencia forense son la base.
> **Decreto 66/025:** Exige notificación de incidentes al CERTuy y trazabilidad.
> **Nivel del curso:** 🔴 Dominar

---

## 1. Qué es y para qué sirve

- **TheHive + Cortex** (open source): plataforma de **gestión de incidentes**. Abrís un caso por incidente, registrás tareas, alertas y evidencias, y Cortex ejecuta análisis automáticos (hashes, dominios, IPs).
- **Volatility**: forense de **memoria RAM** (analizar qué corría en el equipo en el momento del incidente).
- **Autopsy** (o FTK Imager): forense de **disco** (recuperar y analizar archivos preservando la evidencia).

> **Regla de oro de la evidencia:** durante la respuesta, **no alterar la evidencia**: se duplica el disco (imagen forense) y se trabaja sobre la copia. Se documenta todo en el caso de TheHive.

---

## 2. Instalar TheHive + Cortex (en la VM del laboratorio)

TheHive y Cortex se instalan mejor con Docker Compose. Creá `/opt/thehive/docker-compose.yml`:

```bash
sudo mkdir -p /opt/thehive && cd /opt/thehive
sudo bash -c 'cat > docker-compose.yml <<EOF
services:
  cortex:
    image: thehiveproject/cortex:latest
    container_name: cortex
    restart: unless-stopped
    environment:
      - JOB_DIRECTORY=/tmp/cortex-jobs
    volumes:
      - /opt/thehive/cortex:/var/lib/cortex
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - "9001:9001"

  thehive:
    image: thehiveproject/thehive4:latest
    container_name: thehive
    restart: unless-stopped
    depends_on:
      - cortex
    volumes:
      - /opt/thehive/thehive:/var/lib/thehive
    environment:
      - CORTEX_URL=http://cortex:9001
    ports:
      - "9000:9000"
EOF'
sudo docker-compose up -d
```

1. **Cortex**: `http://<IP>:9001` → creá la organización y el usuario.
2. **TheHive**: `http://<IP>:9000` → configurá el administrador inicial (suele ser `admin` en el primer arranque) y conectalo a Cortex (organización + clave de API de Cortex).

---

## 3. Primeros pasos en TheHive

1. **Organizaciones**: creá la org "Banco – CSIRT".
2. **Analysts**: usuarios (RSI, oficiales, TI).
3. **TTP / Case**: creá un caso de práctica: "Simulacro de incidente – phishing con credenciales capturadas".
4. Agregá **observables** (dominio, IP, hash) y ejecutá un **Cortex analyzer** (ej. "Virustotal" o "Hash lookup") para ver el enriquecimiento automático.
5. **Tasks**: el checklist de respuesta (contener, erradicar, recuperar, lecciones).

> Cuando llega una alerta de Wazuh (TOOLS-10), se crea un caso en TheHive automáticamente o de forma manual, con la evidencia adjunta.

---

## 4. Instalar Volatility (forense de memoria)

```bash
# Volatility 3 (Linux/Windows)
pip3 install volatility3
vol3 --help

# Ejemplo de análisis de una imagen de memoria (archivo .mem)
vol3 -f /ruta/captura.mem windows.pslist      # procesos en ejecución
vol3 -f /ruta/captura.mem windows.cmdline     # líneas de comando
vol3 -f /ruta/captura.mem windows.malfind     # sospecha de malware
```

> En el laboratorio podés obtener una captura de memoria de una VM de prueba (volcado `.mem`) y practicar la detección de un proceso anómalo.

---

## 5. Instalar Autopsy (forense de disco)

### Windows (puesto del RSI)

```powershell
winget install SleuthKit.Autopsy
```

### Primer caso

1. Abrí Autopsy → **New Case** → nombre y ubicación.
2. **Select Data Source**: elegí una imagen de disco o una unidad de prueba (idealmente una **copia/imagen** del disco, no el original).
3. **Ingest Modules**: activá las por defecto (fotos, imágenes, web history, strings).
4. Explorá los resultados: archivos borrados, historial web, búsqueda de palabras clave (ej. "password", "cuenta").

> ⚠️ **Evidencia**: en un caso real, el disco se duplica primero con una herramienta de imagen forense (FTK Imager, open source) y el análisis se hace sobre la copia; el original se sella y resguarda (cadena de custodia).

---

## 6. Flujo de respuesta mínima para un incidente

1. **Detectar**: alerta de Wazuh/Suricata o denuncia del usuario.
2. **Registrar**: abrir caso en TheHive (inicio, hora, alcance preliminar).
3. **Contener**: aislar el equipo de la red, deshabilitar cuentas afectadas.
4. **Evidenciar**: imagen de disco (Autopsy) + captura de memoria (Volatility) sobre copias.
5. **Erradicar y recuperar**: limpiar, restaurar desde respaldo (TOOLS-12).
6. **Comunicar**: notificar según RS-02/URCDP-02 (72 h) y CERTuy (Decreto 66/025).
7. **Lecciones**: RC-04 (lecciones aprendidas).

---

## 7. Cómo volcarlo a las plantillas del kit

- **RS-01 (Plan de Respuesta)**: roles, flujo y herramientas del CSIRT.
- **RS-03 (Forense y Evidencia)**: procedimiento de preservación (imagen sobre copia, cadena de custodia) y herramientas usadas.
- **RS-02 / URCDP-02 (Notificación)**: el caso de TheHive es la fuente para completar la notificación a la URCDP (72 h) y al CERTuy.
- **RC-04**: lecciones aprendidas tras cada incidente.

---

## 8. Lista de verificación del módulo

- ☐ TheHive + Cortex instalados y conectados.
- ☐ Org "Banco – CSIRT" y usuarios creados.
- ☐ Caso de práctica creado con observables analizados por Cortex.
- ☐ Volatility instalado y análisis de práctica sobre una imagen de memoria.
- ☐ Autopsy instalado y un caso de práctica con una imagen de disco.
- ☐ Flujo de respuesta documentado en RS-01 (borrador).

---

**Documentos relacionados:** RS-01, RS-02, RS-03, RC-04, URCDP-02
