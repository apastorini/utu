# Guia de Respuesta - Escenario 02: Ransomware
## Banco del Sol - Curso Tectonic BHU

---

## Fase 1: Deteccion

### 1.1 Identificar encriptacion en progreso
```bash
# Conectar a core-bank desde blue-team-ws
ssh admin_banco@core-bank

# Buscar archivos con extension .encrypted
find /srv/banco/documentos -name "*.encrypted" -ls

# Verificar si hay archivos siendo modificados
ls -la /srv/banco/documentos/ | head -30

# Verificar proceso de Python ejecutandose
ps aux | grep python3
ps aux | grep ransomware

# Verificar archivos recien creados o modificados
find /srv/banco/documentos -mmin -5 -ls
```

### 1.2 Verificar nota de rescate
```bash
# Verificar existencia de nota de rescate
cat /srv/banco/documentos/README_RANSOM.txt

# Ver hash de archivos encriptados
find /srv/banco/documentos -name "*.encrypted" -exec sha256sum {} \;
```

### 1.3 Analizar trafico de red
```bash
# Capturar trafico de red durante el ataque
sudo tcpdump -i any -nn host core-bank -w /tmp/ransomware_capture.pcap

# Ver conexiones SSH activas
ss -tnp | grep ESTABLISHED
netstat -tnp | grep ssh
```

---

## Fase 2: Analisis

### 2.1 Identificar variante de ransomware
```bash
# Leer la nota de rescate para identificar variante
cat /srv/banco/documentos/README_RANSOM.txt

# Identificar la direccion de Bitcoin
grep "Bitcoin" /srv/banco/documentos/README_RANSOM.txt

# Verificar tipo de encriptacion
file /srv/banco/documentos/*.encrypted | head -10

# Analizar la estructura de archivos encriptados
xxd /srv/banco/documentos/cuenta_cliente_1.txt.encrypted | head -20
```

### 2.2 Determinar alcance del ataque
```bash
# Contar archivos encriptados vs originales
echo "=== Resumen de archivos ==="
echo "Originales: $(find /srv/banco/documentos -type f ! -name '*.encrypted' ! -name 'README*' | wc -l)"
echo "Encriptados: $(find /srv/banco/documentos -name '*.encrypted' | wc -l)"
echo "Total: $(find /srv/banco/documentos -type f | wc -l)"

# Verificar backup (NO encriptado)
echo "=== Archivos en backup (sin encriptar) ==="
ls -la /srv/banco/backup/

# Verificar timestamp de encriptacion
find /srv/banco/documentos -name "*.encrypted" -printf "%T+ %p\n" | sort | head -10
```

### 2.3 Analizar el script ransomware
```bash
# Buscar el script de ransomware en el sistema
find / -name "ransomware.py" 2>/dev/null
find / -name "*ransom*" 2>/dev/null

# Verificar historial de comandos
cat /root/.bash_history
cat /home/admin_banco/.bash_history

# Verificar archivos temporales
find /tmp -name "*.py" -ls
```

---

## Fase 3: Contencion

### 3.1 aislar core-bank inmediatamente
```bash
# IMPORTANTE: NO APAGAR el servidor (preservar evidencia en memoria)

# Conectar a core-bank
ssh admin_banco@core-bank

# Bloquear todo el trafico excepto SSH desde blue-team-ws
sudo iptables -A INPUT -s <IP_BLUE_TEAM> -p tcp --dport 22 -j ACCEPT
sudo iptables -A OUTPUT -d <IP_BLUE_TEAM> -p tcp --sport 22 -j ACCEPT
sudo iptables -A INPUT -j DROP
sudo iptables -A OUTPUT -j DROP
sudo iptables -A FORWARD -j DROP

# Verificar reglas
sudo iptables -L -v -n

# Matar procesos de encriptacion
sudo pkill -f python3
sudo pkill -f ransomware
```

### 3.2 Preservar evidencia volatile
```bash
# Capturar estado del sistema
ps aux > /tmp/evidencia_ps.txt
ss -tlnp > /tmp/evidencia_netstat.txt
netstat -tnp > /tmp/evidencia_conexiones.txt
last -50 > /tmp/evidencia_login.txt
cat /root/.bash_history > /tmp/evidencia_history.txt

# Capturar memoria (si es posible)
sudo dd if=/dev/mem of=/tmp/evidencia_memoria.dump bs=1M 2>/dev/null

# Verificar procesos activos
ps aux | grep -E "python|nc|netcat|ncat" > /tmp/evidencia_procesos.txt
```

### 3.3 Deshabilitar servicios innecesarios
```bash
# En core-bank
sudo systemctl stop ssh
# Mantener SSH solo para blue-team-ws
sudo iptables -I INPUT -s <IP_BLUE_TEAM> -p tcp --dport 22 -j ACCEPT
sudo systemctl start ssh
```

---

## Fase 4: Analisis y Erradicacion

### 4.1 Identificar vector de ataque
```bash
# Verificar como se ejecuto el ransomware
cat /root/.bash_history | grep -i python
cat /home/admin_banco/.bash_history

# Verificar si se uso SSH desde attack-ws
grep "Accepted" /var/log/auth.log | tail -20
grep "Failed" /var/log/auth.log | tail -20

# Verificar archivos temporales
find /tmp -name "*.py" -o -name "*ransom*" 2>/dev/null
```

### 4.2 Eliminar artefactos del ransomware
```bash
# Eliminar script de ransomware
find / -name "ransomware.py" -delete 2>/dev/null
find / -name "*ransom*" -type f -delete 2>/dev/null

# Eliminar procesos activos
sudo pkill -9 -f python3
sudo pkill -9 -f ransomware

# Verificar que no haya procesos sospechosos
ps aux | grep -E "python|nc|netcat"
```

### 4.3 Revocar credenciales comprometidas
```bash
# Cambiar contrasena del usuario administrador
sudo passwd admin_banco

# Cambiar claves SSH
sudo rm /home/admin_banco/.ssh/authorized_keys
sudo systemctl restart ssh

# Verificar que no haya claves SSH no autorizadas
find / -name "authorized_keys" 2>/dev/null
```

---

## Fase 5: Recuperacion

### 5.1 Restaurar desde backups
```bash
# Verificar integridad de backups
ls -la /srv/banco/backup/
sha256sum /srv/banco/backup/*

# Restaurar archivos desde backup
for file in /srv/banco/backup/*; do
    basename=$(basename "$file")
    echo "Restaurando: $basename"
    cp "$file" "/srv/banco/documentos/$basename"
done

# Verificar restauracion
echo "=== Archivos restaurados ==="
ls -la /srv/banco/documentos/
```

### 5.2 Verificar integridad de datos restaurados
```bash
# Comparar hashes de archivos restaurados
for file in /srv/banco/backup/*; do
    basename=$(basename "$file")
    echo "=== $basename ==="
    echo "Original: $(sha256sum "$file" | awk '{print $1}')"
    echo "Restaurado: $(sha256sum "/srv/banco/documentos/$basename" | awk '{print $1}')"
done

# Verificar que los archivos sean legibles
file /srv/banco/documentos/*.txt | head -10
cat /srv/banco/documentos/cuenta_cliente_1.txt
```

### 5.3 Limpiar archivos encriptados
```bash
# Eliminar archivos encriptados
find /srv/banco/documentos -name "*.encrypted" -delete
find /srv/banco/documentos -name "README_RANSOM.txt" -delete

# Verificar limpieza
ls -la /srv/banco/documentos/
```

---

## Fase 6: Reporte

### 6.1 Plantilla de reporte a CERTuy

```
========================================
REPORTE DE INCIDENTE DE SEGURIDAD
Banco del Sol - Incidente #002
========================================

INSTITUCION: Banco del Sol
CUIT: 30-XXXXXXXX-X
RESPONSABLE: [Nombre del Responsable de Seguridad]
TELEFONO: [Telefono de contacto]
EMAIL: [Email de contacto]

FECHA DEL INCIDENTE: [Fecha]
HORA DE DETECCION: [Hora]
HORA DE CONTENCION: [Hora]

RESUMEN:
Ataque de ransomware contra el sistema bancario core. Se encriptaron
50 archivos financieros con AES-256-CBC. Se dejo nota de rescate
solicitando 0.5 Bitcoin.

ARCHIVOS AFECTADOS:
- /srv/banco/documentos/*.encrypted (50 archivos)
- /srv/banco/documentos/README_RANSOM.txt (nota de rescate)

DATOS COMPROMETIDOS:
- Informacion de clientes (nombres, CUITS, direcciones)
- Datos de cuentas bancarias
- Historial de transacciones

ACCIONES TOMADAS:
1. Aislamiento del servidor
2. Preservacion de evidencia
3. Erradicacion del malware
4. Restauracion desde backups
5. Cambio de credenciales

ESTADO ACTUAL:
- Servicios restaurados
- Datos recuperados desde backup
- Credenciales renovadas

========================================
```

### 6.2 Plantilla de notificacion a URCDP (72 horas)

```
NOTIFICACION DE INCIDENTE DE SEGURIDAD
Banco del Sol - URCDP

Fecha de notificacion: [Fecha]
Plazo: 72 horas desde la deteccion

1. DESCRIPCION DEL INCIDENTE
   Tipo: Ransomware
   Fecha: [Fecha del incidente]
   Duracion: [Duracion]

2. DATOS PERSONALES AFECTADOS
   - Cantidad de registros: [Cantidad]
   - Tipos de datos: Nombres, CUITS, direcciones, datos bancarios

3. MEDIDAS DE PROTECCION
   - Aislamiento inmediato del sistema
   - Restauracion desde backups
   - Cambio de credenciales

4. PERSONAS AFECTADAS
   - Clientes del banco: [Cantidad]
   - Empleados: [Cantidad]

5. CONSECUENCIAS
   - Impacto en clientes: [Descripcion]
   - Impacto en operaciones: [Descripcion]

========================================
```

---

## Fase 7: Prevencion

### 7.1 Medidas recomendadas
- Implementar monitoreo de integridad de archivos (AIDE, Tripwire)
- Segmentacion de red para servidores criticos
- Backups regulares con verificacion de integridad
- Capacitacion en seguridad para empleados
- Implementar solucion anti-ransomware
- Monitoreo activo de procesos

### 7.2 Herramientas utilizadas
- find (para buscar archivos encriptados)
- sha256sum (para verificar integridad)
- iptables (para aislamiento)
- ps/netstat/ss (para analisis de procesos)
- cp (para restauracion)
- dd (para preservacion de memoria)

### 7.3 Tiempos de respuesta
| Fase | Tiempo Objetivo | Tiempo Real |
|------|----------------|-------------|
| Deteccion | < 5 minutos | [Medir] |
| Contencion | < 15 minutos | [Medir] |
| Analisis | < 1 hora | [Medir] |
| Erradicacion | < 2 horas | [Medir] |
| Recuperacion | < 4 horas | [Medir] |
| Reporte CERTuy | < 24 horas | [Medir] |
| Reporte URCDP | < 72 horas | [Medir] |
