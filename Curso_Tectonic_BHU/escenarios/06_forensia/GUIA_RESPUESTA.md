# Guia de Respuesta - Escenario 06: Analisis Forense Post-Incidente
## Banco del Sol - Curso Tectonic BHU

---

## Fase 1: Preservacion de Evidencia

### 1.1 Documentar cadena de custodia
```bash
# Conectar a blue-team-ws
ssh blue-team-ws@blue-team-ws

# Crear registro de cadena de custodia
cat > /opt/forensics/custody_chain.txt << 'EOF'
========================================
CADENA DE CUSTODIA DE EVIDENCIA
========================================
Caso: Incidente #006 - Banco del Sol
Fecha de inicio: [Fecha]
Analista: [Nombre]

EVIDENCIA RECOGIDA:
1. Dump de memoria: /opt/memory_dump.txt
2. Logs del sistema: /var/log/auth.log, /var/log/syslog
3. Archivos ocultos: /opt/.hidden/
4. Timeline del ataque: /opt/.hidden/attack_timeline.txt

CADENA DE CUSTODIA:
- [Fecha/Hora] Evidencia recogida por [Analista]
- [Fecha/Hora] Evidencia transferida a [Ubicacion]
- [Fecha/Hora] Hashes calculados para integridad

========================================
EOF
```

### 1.2 Crear copias de seguridad de evidencia
```bash
# Crear directorio de evidencia
EVIDENCE_DIR="/opt/forensics/evidence/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$EVIDENCE_DIR"

# Copiar dump de memoria
ssh admin@db-srv "cat /opt/memory_dump.txt" > "$EVIDENCE_DIR/memory_dump.txt"

# Copiar logs
ssh admin@db-srv "cat /var/log/auth.log" > "$EVIDENCE_DIR/auth.log"
ssh admin@db-srv "cat /var/log/syslog" > "$EVIDENCE_DIR/syslog"

# Copiar archivos ocultos
ssh admin@db-srv "cat /opt/.hidden/attack_timeline.txt" > "$EVIDENCE_DIR/attack_timeline.txt"
ssh admin@db-srv "cat /opt/.hidden/credentials.txt" > "$EVIDENCE_DIR/credentials.txt"
ssh admin@db-srv "cat /opt/.hidden/data_dump.csv" > "$EVIDENCE_DIR/data_dump.csv"

# Calcular hashes de integridad
cd "$EVIDENCE_DIR"
sha256sum * > hashes.txt
cat hashes.txt
```

---

## Fase 2: Adquisicion Volatil

### 2.1 Capturar procesos activos
```bash
# Conectar a db-srv y capturar procesos
ssh admin@db-srv "ps aux" > "$EVIDENCE_DIR/ps_output.txt"
ssh admin@db-srv "ps -ef" > "$EVIDENCE_DIR/ps_ef_output.txt"

# Ver procesos sospechosos
ssh admin@db-srv "ps aux | grep -E 'nc|netcat|python.*back|ncat'"

# Ver procesos con puertos abiertos
ssh admin@db-srv "ss -tlnp"
ssh admin@db-srv "netstat -tlnp"
```

### 2.2 Capturar conexiones de red
```bash
# Capturar conexiones activas
ssh admin@db-srv "ss -tlnp" > "$EVIDENCE_DIR/ss_output.txt"
ssh admin@db-srv "netstat -tlnp" > "$EVIDENCE_DIR/netstat_output.txt"
ssh admin@db-srv "ss -tnp" > "$EVIDENCE_DIR/ss_established.txt"

# Verificar conexiones ESTABLISHED
ssh admin@db-srv "ss -tnp | grep ESTAB"
```

### 2.3 Capturar historial y sesiones
```bash
# Capturar historial de login
ssh admin@db-srv "last -50" > "$EVIDENCE_DIR/last_output.txt"
ssh admin@db-srv "lastb -20" > "$EVIDENCE_DIR/lastb_output.txt"
ssh admin@db-srv "who" > "$EVIDENCE_DIR/who_output.txt"
ssh admin@db-srv "w" > "$EVIDENCE_DIR/w_output.txt"

# Capturar historial de comandos
ssh admin@db-srv "cat /root/.bash_history" > "$EVIDENCE_DIR/bash_history_root.txt"
ssh admin@db-srv "cat /home/admin/.bash_history" > "$EVIDENCE_DIR/bash_history_admin.txt"
```

### 2.4 Capturar informacion del sistema
```bash
# Informacion del sistema
ssh admin@db-srv "uname -a" > "$EVIDENCE_DIR/uname_output.txt"
ssh admin@db-srv "cat /etc/os-release" > "$EVIDENCE_DIR/os_release.txt"
ssh admin@db-srv "hostname" > "$EVIDENCE_DIR/hostname.txt"
ssh admin@db-srv "ip addr" > "$EVIDENCE_DIR/ip_addr.txt"
ssh admin@db-srv "ip route" > "$EVIDENCE_DIR/ip_route.txt"
ssh admin@db-srv "df -h" > "$EVIDENCE_DIR/df_output.txt"
ssh admin@db-srv "mount" > "$EVIDENCE_DIR/mount_output.txt"
```

---

## Fase 3: Analisis de Logs

### 3.1 Analizar auth.log para brute force SSH
```bash
# Contar intentos fallidos
grep -i "failed" "$EVIDENCE_DIR/auth.log" | wc -l
echo "intentos fallidos de login"

# Identificar IP atacante
grep -i "failed" "$EVIDENCE_DIR/auth.log" | \
  awk '{for(i=1;i<=NF;i++) if($i=="from") print $(i+1)}' | \
  sort | uniq -c | sort -rn | head -10

# Ver intentos exitosos
grep -i "accepted" "$EVIDENCE_DIR/auth.log"

# Ver usuarios objetivo
grep -i "failed\|invalid user" "$EVIDENCE_DIR/auth.log" | \
  awk '{for(i=1;i<=NF;i++) if($i=="for") print $(i+1)}' | \
  sort | uniq -c | sort -rn
```

### 3.2 Analizar syslog para actividad maliciosa
```bash
# Buscar referencias a malware
grep -i "malware\|backdoor\|reverse\|suspicious" "$EVIDENCE_DIR/syslog"

# Buscar actividad de procesos sospechosos
grep -i "nc\|netcat\|ncat\|python.*back" "$EVIDENCE_DIR/syslog"

# Buscar creacion de archivos sospechosos
grep -i "created\|deleted\|modified" "$EVIDENCE_DIR/syslog"

# Buscar actividad de red sospechosa
grep -i "SYN\|flood\|exfiltration" "$EVIDENCE_DIR/syslog"
```

### 3.3 Analizar logs de PostgreSQL (si existen)
```bash
# Verificar logs de PostgreSQL
ssh admin@db-srv "ls /var/log/postgresql/"
ssh admin@db-srv "cat /var/log/postgresql/postgresql-*-main.log" | tail -100

# Buscar consultas sospechosas
ssh admin@db-srv "grep -i 'select\|insert\|drop\|delete' /var/log/postgresql/postgresql-*-main.log"
```

---

## Fase 4: Recuperacion de Archivos

### 4.1 Recuperar archivos con foremost
```bash
# Usar foremost para recuperar archivos eliminados
# Primero necesitamos una imagen del disco
ssh admin@db-srv "sudo dd if=/dev/sda of=/tmp/disk_image.img bs=1M count=100" 2>/dev/null

# Copiar imagen a blue-team-ws
scp admin@db-srv:/tmp/disk_image.img /opt/forensics/

# Recuperar archivos con foremost
foremost -i /opt/forensics/disk_image.img -o /opt/forensics/recovered/

# Verificar archivos recuperados
ls -la /opt/forensics/recovered/
find /opt/forensics/recovered/ -type f | head -20
```

### 4.2 Recuperar archivos con sleuthkit
```bash
# Usar fls para listar archivos (incluidos eliminados)
fls /opt/forensics/disk_image.img 2>/dev/null | head -30

# Buscar archivos eliminados (marcados con *)
fls -r /opt/forensics/disk_image.img 2>/dev/null | grep "\*"

# Extraer archivos recuperados
icat /opt/forensics/disk_image.img [inode_number] > /opt/forensics/recovered_file.txt
```

### 4.3 Buscar archivos ocultos
```bash
# Buscar archivos ocultos en db-srv
ssh admin@db-srv "find / -name '.*' -type f 2>/dev/null | grep -v '/proc\|/sys'"
ssh admin@db-srv "ls -la /opt/.hidden/"

# Copiar archivos ocultos
ssh admin@db-srv "cat /opt/.hidden/credentials.txt"
ssh admin@db-srv "cat /opt/.hidden/data_dump.csv"
ssh admin@db-srv "cat /opt/.hidden/backdoor_config.json"
ssh admin@db-srv "cat /opt/.hidden/password_hashes.txt"
```

---

## Fase 5: Analisis de Memoria

### 5.1 Analizar dump de memoria con volatility3
```bash
# Copiar dump de memoria
ssh admin@db-srv "cat /opt/memory_dump.txt" > /opt/forensics/memory_dump.txt

# Analizar con volatility3 (si hay imagen real)
python3 -m volatility3 -f /opt/forensics/memory_dump.txt windows.pslist 2>/dev/null

# O analizar manualmente el dump simulado
echo "=== Procesos encontrados en memoria ==="
grep -E "^root|^www-data|^postgres" /opt/forensics/memory_dump.txt | head -20

echo ""
echo "=== Conexiones de red en memoria ==="
grep -E "LISTEN|ESTABLISHED" /opt/forensics/memory_dump.txt

echo ""
echo "=== Comandos ejecutados ==="
grep -E "wget|chmod|python|nc|scp|rm" /opt/forensics/memory_dump.txt
```

### 5.2 Identificar procesos maliciosos
```bash
# Procesos sospechosos
echo "=== Procesos maliciosos identificados ==="
echo "1. /usr/bin/python3 /opt/backdoor.py (PID 234)"
echo "   - Reverse shell Python"
echo "   - Conexion a 10.0.0.1:4444"

echo "2. nc -lvnp 4444 (PID 267)"
echo "   - Netcat listener"
echo "   - Puerto 4444"

echo "3. /usr/bin/python3 -m http.server 8080 (PID 334)"
echo "   - Servidor HTTP para distribuir malware"
```

---

## Fase 6: Construccion de Timeline

### 6.1 Crear timeline consolidada
```bash
# Extraer timestamps de auth.log
grep -E "Jul (11|12)" "$EVIDENCE_DIR/auth.log" | \
  awk '{print $1, $2, $3, $5, $6, $7, $8, $9}' | \
  sort -k2 -n > "$EVIDENCE_DIR/timeline_auth.txt"

# Extraer timestamps de syslog
grep -E "Jul (11|12)" "$EVIDENCE_DIR/syslog" | \
  awk '{print $1, $2, $3, $5, $6, $7, $8, $9}' | \
  sort -k2 -n > "$EVIDENCE_DIR/timeline_syslog.txt"

# Consolidar timeline
cat "$EVIDENCE_DIR/timeline_auth.txt" "$EVIDENCE_DIR/timeline_syslog.txt" | \
  sort | uniq > "$EVIDENCE_DIR/complete_timeline.txt"

# Mostrar timeline
cat "$EVIDENCE_DIR/complete_timeline.txt"
```

### 6.2 Timeline del ataque reconstruido

| Fecha/Hora | Fase | Descripcion |
|------------|------|-------------|
| Jul 11 22:15:23 | Acceso Inicial | SSH exitoso con root desde 10.0.0.1 |
| Jul 11 22:30:45 | Reconocimiento | Brute force SSH (15 intentos fallidos) |
| Jul 11 23:15:33 | Instalacion | backdoor.py ejecutado, reverse shell activo |
| Jul 12 01:30:22 | Movimiento Lateral | SSH y exploracion PostgreSQL |
| Jul 12 03:20:33 | Exfiltracion | Backup creado y transferido via SCP |
| Jul 12 03:45:22 | Limpieza | Backdoor eliminado, historial borrado |

---

## Fase 7: Reporte Forense

### 7.1 Plantilla de reporte forense

```
========================================
REPORTE FORENSE - BANCO DEL SOL
Incidente #006 - Analisis Post-Incidente
========================================

DATOS DEL REPORTE:
Fecha: [Fecha]
Analista: [Nombre]
Servidor: db-srv
Caso: Incidente #006

RESUMEN EJECUTIVO:
El servidor db-srv del Banco del Sol fue comprometido mediante
un ataque de brute force SSH, seguido de instalacion de backdoor,
movimiento lateral, exfiltracion de datos y limpieza de evidencia.

METODOLOGIA:
1. Preservacion de evidencia
2. Adquisicion volatil y no volatil
3. Analisis de logs
4. Recuperacion de archivos
5. Construccion de timeline
6. Conclusiones

HALLAZGOS:

1. ACCESO INICIAL (2026-07-11 22:15:23)
   - Metodo: Brute force SSH
   - IP: 10.0.0.1
   - Usuario: root
   - Evidence: auth.log

2. INSTALACION DE MALWARE (2026-07-11 23:15:33)
   - Archivo: /opt/backdoor.py
   - Tipo: Reverse shell Python
   - Puerto: 4444
   - C2: 10.0.0.1
   - Evidence: syslog, memory_dump.txt

3. MOVIMIENTO LATERAL (2026-07-12 01:30:22)
   - SSH a db-srv
   - Exploracion de PostgreSQL
   - Evidence: auth.log

4. EXFILTRACION (2026-07-12 03:20:33)
   - Backup de PostgreSQL comprimido
   - Transferido via SCP
   - Evidence: syslog

5. LIMPIEZA (2026-07-12 03:45:22)
   - Backdoor eliminado
   - Historial borrado
   - Archivos ocultos en /opt/.hidden/
   - Evidence: memory_dump.txt

INDICADORES DE COMPROMISO:
- IP: 10.0.0.1
- Puerto: 4444 (reverse shell)
- Puerto: 8080 (HTTP malware)
- Archivo: backdoor.py
- Hash: [Calcular]

DATOS COMPROMETIDOS:
- Backup de PostgreSQL (clientes, cuentas, transacciones)
- Credenciales del sistema (root, admin, postgres)
- Archivos de configuracion

RECOMENDACIONES:
1. Implementar autenticacion de dos factores (2FA)
2. Monitoreo activo de logs SSH
3. Segmentacion de red
4. Implementar HIDS/IPS
5. Politicas de contrasenas robustas
6. Capacitacion en seguridad

EVIDENCIA:
- Directorio: /opt/forensics/evidence/[timestamp]
- Hashes: hashes.txt
- Timeline: complete_timeline.txt

========================================
```

### 7.2 Herramientas utilizadas
- volatility3 (analisis de memoria)
- foremost (recuperacion de archivos)
- sleuthkit/tsk (analisis de disco)
- wireshark/tshark (analisis de red)
- tcpdump (captura de trafico)
- grep/awk (analisis de logs)
- sha256sum (verificacion de integridad)
- scp/rsync (transferencia de evidencia)

### 7.3 Tiempos de respuesta
| Fase | Tiempo Objetivo | Tiempo Real |
|------|----------------|-------------|
| Preservacion | < 30 minutos | [Medir] |
| Adquisicion | < 2 horas | [Medir] |
| Analisis | < 8 horas | [Medir] |
| Timeline | < 4 horas | [Medir] |
| Reporte | < 24 horas | [Medir] |
