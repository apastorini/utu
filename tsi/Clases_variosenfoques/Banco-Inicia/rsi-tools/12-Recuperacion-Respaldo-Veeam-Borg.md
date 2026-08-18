# TOOLS-12 · Recuperación y Respaldo: Veeam, rsync, BorgBackup

> **Función del MCU 5.0:** Recuperar (RC.RP): planes de recuperación y respaldo; mantener la operación tras un incidente o desastre.
> **ISO/IEC 27001:** Anexo A.8.13 (respaldo de la información) y A.5.29 (continuidad).
> **BCU:** La guía EMG y el art. 492 exigen respaldos, pruebas de restauración y continuidad (BCU-06, RC-01/02).
> **URCDP:** La pérdida de datos personales por falta de respaldo es un riesgo documentable; el respaldo es una medida de seguridad.
> **Nivel del curso:** 🟡 Practicar

---

## 1. Qué es y para qué sirve

- **Veeam Community Edition**: respaldo de máquinas virtuales y servidores (gratuito hasta 10 VMs) con interfaces gráficas.
- **rsync**: herramienta de copia/sincronización de archivos (Linux) — simple y poderosa.
- **BorgBackup**: respaldo deduplicado y cifrado (Linux) — ideal para respaldos seguros con compresión.

> **Regla 3-2-1:** al menos **3 copias** de los datos, en **2 medios diferentes**, con **1 copia fuera de sitio** (fuera del edificio).

---

## 2. Instalar Veeam Community (Windows)

```powershell
winget install Veeam.VeeamAgentForWindows
# o descargá "Veeam Community Edition" desde veeam.com → registrá un usuario
```

Veeam Agent for Windows permite respaldar el equipo en el que esté instalado:

1. **Backup Job → PC Backup**.
2. Destino: disco externo o carpeta de red.
3. Seleccioná volúmenes a respaldar → frecuencia (diaria/semanal).
4. **Schedule** y **Retention** (cuántas copias conservar).

---

## 3. Instalar BorgBackup (Linux, en la VM)

```bash
sudo apt install -y borgbackup

# Inicializar el repositorio (con cifrado)
borg init --encryption=repokey-blake2 /mnt/backup/borg/repo-sgs

# Respaldar una carpeta
borg create /mnt/backup/borg/repo-sgs::"sgs-{now:%Y-%m-%d}" /var/www/html /etc

# Listar respaldos
borg list /mnt/backup/borg/repo-sgs

# Restaurar
borg extract /mnt/backup/borg/repo-sgs::"sgs-2026-08-06" /etc
```

> El respaldo de borg está **cifrado**: la clave de repositorio debe guardarse en el gestor (TOOLS-06).

---

## 4. Instalar rsync (Linux)

```bash
sudo apt install -y rsync

# Copia local
rsync -av /ruta/origen /mnt/backup/destino/

# Copia remota por SSH (a otro servidor = "fuera de sitio")
rsync -avz /var/www/html usuario@backup-servidor:/mnt/backup/sgs/
```

---

## 5. Prueba de restauración (la parte que casi nadie hace)

Un respaldo que no se prueba **no es un respaldo**. Hacé esto al menos una vez al mes:

1. Restaurá un archivo de prueba desde el respaldo (Veeam: "Restore Files"; Borg: `borg extract`).
2. Verificá que el archivo restaurado abre y tiene los datos esperados.
3. Documentá la prueba (fecha, archivo restaurado, resultado) como evidencia en **PR-05 / RC-02**.

---

## 6. Qué respaldar en el SGSI

| Datos | Frecuencia sugerida | Herramienta |
|---|---|---|
| Documentos del SGSI (políticas, plantillas) | Diaria | Veeam / rsync |
| Base de datos de riesgos (Eramba) | Diaria | Borg / mysqldump + borg |
| Logs del SIEM (Wazuh) | Diaria | Borg / rsync |
| Configuraciones de red | Ante cada cambio | rsync |
| VMs del laboratorio | Semanal | Veeam / instantáneas VirtualBox |

---

## 7. Cómo volcarlo a las plantillas del kit

- **PR-05 (Respaldo y Recuperación)**: política de respaldo (qué, cuándo, retención), herramientas y prueba de restauración.
- **RC-02 (DRP)**: los respaldos fuera de sitio sustentan la recuperación ante desastres.
- **BCU-06 / RC-01**: continuidad del negocio con respaldos verificados.

---

## 8. Lista de verificación del módulo

- ☐ Veeam Community instalado y un job de respaldo configurado.
- ☐ BorgBackup instalado y repositorio cifrado creado.
- ☐ rsync instalado y una sincronización probada.
- ☐ Regla 3-2-1 documentada (3 copias, 2 medios, 1 fuera de sitio).
- ☐ Prueba de restauración realizada y documentada.
- ☐ Resultados volcados a PR-05 (borrador).

---

**Documentos relacionados:** PR-05, RC-01, RC-02, BCU-06, URCDP-01
