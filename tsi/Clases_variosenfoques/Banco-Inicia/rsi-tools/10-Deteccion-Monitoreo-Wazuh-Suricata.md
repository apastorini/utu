# TOOLS-10 · Detección y Monitoreo: Wazuh, Suricata, Grafana/Loki, Sysmon

> **Función del MCU 5.0:** Detectar (DE.CM, DE.AE): monitoreo continuo, correlación de eventos y alertas de anomalías.
> **ISO/IEC 27001:** Anexo A.8.15–A.8.17 (registro de eventos, monitoreo, protección de logs).
> **BCU:** La guía EMG y el RNRCSF exigen monitoreo de seguridad y gestión de logs (BCU-04). El Decreto 66/025 pide trazabilidad ≥12 meses.
> **URCDP:** Los logs de acceso a datos personales son evidencia para el Documento de Seguridad y para investigar vulneraciones.
> **Nivel del curso:** 🔴 Dominar

---

## 1. Qué es y para qué sirve

- **Wazuh** (SIEM + XDR open source): centraliza logs de los equipos, aplica reglas de correlación y genera **alertas**. Es la herramienta central de este módulo.
- **Suricata** (IDS/IPS): analiza el tráfico de red en busca de ataques (firmas) y puede bloquear (IPS).
- **Grafana + Loki**: paneles de monitoreo y almacenamiento de logs (visión "en tiempo real" y búsquedas).
- **Sysmon** (Windows) / **auditd** (Linux): registran eventos detallados del sistema operativo en los endpoints, que Wazuh centraliza.

---

## 2. Instalar Wazuh (en la VM del laboratorio)

Wazuh tiene instalador todo-en-uno (all-in-one):

```bash
# Requisitos: VM con 4 GB RAM, 50 GB disco, Ubuntu Server
curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh
sudo bash ./wazuh-install.sh -a
```

Al terminar te muestra la **clave del panel** y la URL (`https://<IP>:443`). Guardala.

> ⚠️ La instalación completa (Wazuh indexer + server + dashboard) tarda varios minutos y necesita una VM dedicada de ~4 GB RAM.

### 3. Primeros pasos en Wazuh

1. Accedé al **dashboard** (`https://<IP>:443`, usuario `admin`, clave mostrada al instalar).
2. **Agents → Deploy new agent**: elegí la plataforma (Windows/Linux), poné la IP del servidor Wazuh, y copiá el comando de instalación.
3. Instalá el agente en una **VM cliente de prueba** (Windows o Linux) y verificá que aparezca como **Active**.
4. **Security events**: vas a ver los eventos que llegan. Explorá las secciones **Vulnerability detection**, **FIM** (integridad de archivos), **Syscheck**, **PM** (gestión de parches).

---

## 3. Instalar Sysmon (Windows) y auditd (Linux) en los endpoints

### Sysmon (Windows)

Descargá Sysmon de Microsoft Sysinternals y usá una config básica:

```powershell
# Descargar de https://learn.microsoft.com/sysinternals/downloads/sysmon
.\Sysmon64.exe -accepteula -i sysmonconfig.xml   # con una config
```

### auditd (Linux)

```bash
sudo apt install -y auditd
sudo auditctl -e 1    # habilitar
```

Ambos envían eventos al agente Wazuh, que los correlaciona.

---

## 4. Instalar Suricata (IDS)

En la VM o en un punto de la red de laboratorio:

```bash
sudo apt install -y suricata
sudo suricata-update          # descargar reglas (Emerging Threats)
sudo systemctl enable --now suricata
```

Configurar la interfaz a monitorear en `/etc/suricata/suricata.yaml` (variable `HOME_NET` y `interface`), luego:

```bash
sudo systemctl restart suricata
```

Verificar alertas:

```bash
sudo tail -f /var/log/suricata/fast.log
```

---

## 5. Instalar Grafana + Loki (paneles y logs)

```bash
# Grafana
sudo apt install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt update
sudo apt install -y grafana
sudo systemctl enable --now grafana-server

# Loki (agregar a docker-compose del TOOLS-06 o como binario)
wget https://github.com/grafana/loki/releases/download/v2.9.2/loki-linux-amd64.zip
```

En Grafana (`http://<IP>:3000`, admin/admin) agregá Loki como **data source** y creá un panel con "número de alertas Wazuh por día".

> Sugerencia: Wazuh ya trae su propio dashboard; Grafana/Loki es el extra cuando querés paneles unificados de monitoreo.

---

## 6. Reglas de alertas útiles para el RSI

Configurá en Wazuh (Decoders/Rules) o alertas mínimas:

| Evento a alertar | Fuente | Regla sugerida |
|---|---|---|
| Login fallido repetido (fuerza bruta) | Sysmon/auditd | 5 fallos en 10 min |
| Usuario con privilegios elevados | Sysmon | Evento de escalada |
| Archivo crítico modificado (FIM) | Wazuh FIM | Cualquier cambio |
| Conexión a IP de riesgo | Suricata/Wazuh | Firma detectada |
| Antivirus/EDR desactivado | Sysmon | Evento 104 / 7036 |

---

## 7. Cómo volcarlo a las plantillas del kit

- **DE-01 (Monitoreo y Registro)**: la arquitectura (Wazuh + Suricata + Sysmon), retención de logs (≥12 meses por Decreto 66/025) y alertas configuradas.
- **DE-02 (Anomalías e Intrusiones)**: los casos de uso de alertas y cómo se investigan.
- **RS-02 (Notificación)**: los logs de Wazuh son evidencia para la notificación de vulneraciones (URCDP, CERTuy).
- **BCU-04**: evidencia de monitoreo continuo.

---

## 8. Lista de verificación del módulo

- ☐ Wazuh instalado (all-in-one) y dashboard accesible.
- ☐ Agente instalado en una VM de prueba y en estado Active.
- ☐ Sysmon (Windows) o auditd (Linux) configurados.
- ☐ Suricata instalado con reglas actualizadas y alertas generadas.
- ☐ Grafana + Loki corriendo y conectados.
- ☐ Al menos 3 alertas configuradas y probadas.
- ☐ Retención de logs definida (≥12 meses) y documentada en DE-01.

---

**Documentos relacionados:** DE-01, DE-02, RS-02, BCU-04, URCDP-02
