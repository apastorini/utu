# CURSO COMPLETO DE CIBERSEGURIDAD - PARTE 9

## MÓDULO 13: INCIDENT RESPONSE Y FORENSICS

### 13.1 Ciclo de Vida de Respuesta a Incidentes (NIST)

```
┌────────────────────────────────────────────────────────────┐
│         NIST INCIDENT RESPONSE LIFECYCLE                   │
└────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────┐
    │  1. PREPARACIÓN                         │
    │  • Políticas y procedimientos           │
    │  • Herramientas (SIEM, EDR, Forensics)  │
    │  • Equipo CSIRT                         │
    │  • Simulacros (tabletop exercises)      │
    └────────────────┬────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────┐
    │  2. DETECCIÓN Y ANÁLISIS                │
    │  • Alertas de SIEM                      │
    │  • Análisis de logs                     │
    │  • Threat hunting                       │
    │  • Clasificación de severidad           │
    └────────────────┬────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────┐
    │  3. CONTENCIÓN                          │
    │  • Short-term: Aislar sistemas          │
    │  • Long-term: Parches temporales        │
    │  • Preservar evidencia                  │
    │  • Documentar acciones                  │
    └────────────────┬────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────┐
    │  4. ERRADICACIÓN                        │
    │  • Eliminar malware                     │
    │  • Cerrar vulnerabilidades              │
    │  • Cambiar credenciales                 │
    │  • Actualizar sistemas                  │
    └────────────────┬────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────┐
    │  5. RECUPERACIÓN                        │
    │  • Restaurar desde backups              │
    │  • Verificar integridad                 │
    │  • Monitoreo intensivo                  │
    │  • Retorno gradual a operación          │
    └────────────────┬────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────┐
    │  6. POST-INCIDENTE                      │
    │  • Lecciones aprendidas                 │
    │  • Actualizar procedimientos            │
    │  • Reporte ejecutivo                    │
    │  • Mejora continua                      │
    └─────────────────────────────────────────┘
```

### 13.2 Clasificación de Incidentes

```
┌────────────────────────────────────────────────────────────┐
│              MATRIZ DE SEVERIDAD                           │
└────────────────────────────────────────────────────────────┘

CRÍTICO (P1)
├─ Ransomware activo
├─ Brecha de datos masiva
├─ Sistemas críticos caídos
└─ Respuesta: Inmediata (< 15 min)

ALTO (P2)
├─ Malware detectado
├─ Intento de intrusión exitoso
├─ Fuga de datos limitada
└─ Respuesta: < 1 hora

MEDIO (P3)
├─ Phishing dirigido
├─ Vulnerabilidad crítica sin explotar
├─ Acceso no autorizado a sistema no crítico
└─ Respuesta: < 4 horas

BAJO (P4)
├─ Escaneo de puertos
├─ Phishing genérico bloqueado
├─ Violación de política menor
└─ Respuesta: < 24 horas
```

### 13.3 Equipo CSIRT (Computer Security Incident Response Team)

```
┌────────────────────────────────────────────────────────────┐
│              ESTRUCTURA DEL CSIRT                          │
└────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │ INCIDENT MANAGER│
                    │  (Coordinador)  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌─────▼─────┐       ┌─────▼─────┐
   │ ANÁLISIS│         │CONTENCIÓN │       │COMUNICACIÓN│
   │         │         │           │       │            │
   │• Forense│         │• Aislamiento│     │• Stakeholders│
   │• Malware│         │• Mitigación│      │• Legal     │
   │• Logs   │         │• Remediación│     │• Prensa    │
   └─────────┘         └───────────┘       └────────────┘

ROLES Y RESPONSABILIDADES:

Incident Manager:
├─ Coordinar respuesta
├─ Tomar decisiones críticas
├─ Comunicación con dirección
└─ Documentar timeline

Analista de Seguridad:
├─ Análisis de logs
├─ Threat hunting
├─ Identificar IOCs
└─ Análisis forense

Ingeniero de Respuesta:
├─ Contención técnica
├─ Aislar sistemas
├─ Aplicar parches
└─ Restaurar servicios

Comunicador:
├─ Notificaciones internas
├─ Comunicados externos
├─ Coordinación legal
└─ Reporte a reguladores
```

### 13.4 Herramientas de Incident Response

#### 13.4.1 SIEM (Security Information and Event Management)

```bash
# Ejemplo con Elastic Stack (ELK)

# 1. Instalar Elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.11.0-linux-x86_64.tar.gz
tar -xzf elasticsearch-8.11.0-linux-x86_64.tar.gz
cd elasticsearch-8.11.0/
./bin/elasticsearch

# 2. Instalar Kibana
wget https://artifacts.elastic.co/downloads/kibana/kibana-8.11.0-linux-x86_64.tar.gz
tar -xzf kibana-8.11.0-linux-x86_64.tar.gz
cd kibana-8.11.0/
./bin/kibana

# 3. Configurar Filebeat para enviar logs
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/auth.log
    - /var/log/syslog
    - /var/log/apache2/*.log

output.elasticsearch:
  hosts: ["localhost:9200"]

# 4. Crear alerta de detección
POST _watcher/watch/failed_login_alert
{
  "trigger": {
    "schedule": {"interval": "5m"}
  },
  "input": {
    "search": {
      "request": {
        "indices": ["filebeat-*"],
        "body": {
          "query": {
            "bool": {
              "must": [
                {"match": {"event.action": "ssh_login"}},
                {"match": {"event.outcome": "failure"}}
              ],
              "filter": {
                "range": {"@timestamp": {"gte": "now-5m"}}
              }
            }
          }
        }
      }
    }
  },
  "condition": {
    "compare": {"ctx.payload.hits.total": {"gte": 5}}
  },
  "actions": {
    "email_admin": {
      "email": {
        "to": "security@empresa.com",
        "subject": "Alerta: Múltiples intentos de login fallidos",
        "body": "Se detectaron {{ctx.payload.hits.total}} intentos fallidos"
      }
    }
  }
}
```

#### 13.4.2 EDR (Endpoint Detection and Response)

```python
# Ejemplo conceptual de detección con osquery

# Query para detectar procesos sospechosos
SELECT 
    p.pid,
    p.name,
    p.path,
    p.cmdline,
    p.parent,
    pp.name as parent_name
FROM processes p
LEFT JOIN processes pp ON p.parent = pp.pid
WHERE 
    p.name LIKE '%powershell%'
    AND p.cmdline LIKE '%DownloadString%'
    AND p.cmdline LIKE '%IEX%';

# Query para detectar persistencia
SELECT 
    name,
    path,
    source
FROM startup_items
WHERE 
    path NOT LIKE 'C:\\Program Files%'
    AND path NOT LIKE 'C:\\Windows%';

# Query para detectar conexiones sospechosas
SELECT 
    p.name,
    p.path,
    pos.remote_address,
    pos.remote_port
FROM process_open_sockets pos
JOIN processes p ON pos.pid = p.pid
WHERE 
    pos.remote_port IN (4444, 5555, 6666, 7777)
    OR pos.remote_address LIKE '10.0.0.%';
```

### 13.5 Análisis Forense Digital

#### 13.5.1 Orden de Volatilidad

```
┌────────────────────────────────────────────────────────────┐
│         ORDEN DE RECOLECCIÓN DE EVIDENCIA                  │
│              (De más a menos volátil)                      │
└────────────────────────────────────────────────────────────┘

1. REGISTROS DE CPU Y CACHÉ
   ├─ Contenido de registros
   └─ Caché de CPU

2. MEMORIA RAM
   ├─ Procesos en ejecución
   ├─ Conexiones de red activas
   ├─ Claves de cifrado en memoria
   └─ Contraseñas en texto plano

3. ESTADO DEL SISTEMA
   ├─ Tabla de enrutamiento
   ├─ Caché ARP
   ├─ Tabla de procesos
   └─ Estadísticas del kernel

4. SISTEMA DE ARCHIVOS
   ├─ Archivos temporales
   ├─ Swap/Pagefile
   └─ Archivos eliminados recientemente

5. LOGS DEL SISTEMA
   ├─ Event logs
   ├─ Logs de aplicaciones
   └─ Logs de firewall

6. CONFIGURACIÓN DEL SISTEMA
   ├─ Registro de Windows
   ├─ Archivos de configuración
   └─ Topología de red

7. DOCUMENTOS Y ARCHIVOS
   ├─ Documentos de usuario
   ├─ Archivos de datos
   └─ Archivos de aplicación

8. BACKUPS Y ARCHIVOS
   ├─ Backups del sistema
   ├─ Archivos comprimidos
   └─ Medios de almacenamiento externo
```

#### 13.5.2 Adquisición de Memoria RAM

```bash
# Usando LiME (Linux Memory Extractor)
git clone https://github.com/504ensicsLabs/LiME
cd LiME/src
make
sudo insmod lime-$(uname -r).ko "path=/tmp/memoria.lime format=lime"

# Usando DumpIt (Windows)
# Ejecutar DumpIt.exe como administrador
# Genera archivo de memoria en directorio actual

# Análisis con Volatility
volatility -f memoria.lime --profile=LinuxUbuntu2004x64 pslist
volatility -f memoria.lime --profile=LinuxUbuntu2004x64 netscan
volatility -f memoria.lime --profile=LinuxUbuntu2004x64 malfind
```

#### 13.5.3 Análisis de Disco

```bash
# Crear imagen forense del disco
sudo dd if=/dev/sda of=/mnt/evidencia/disco.img bs=4M status=progress

# Calcular hash para cadena de custodia
sha256sum disco.img > disco.img.sha256

# Montar imagen en modo solo lectura
sudo mkdir /mnt/evidencia_montada
sudo mount -o ro,loop disco.img /mnt/evidencia_montada

# Buscar archivos eliminados con Autopsy
autopsy

# Análisis de timeline
fls -r -m / disco.img > timeline.body
mactime -b timeline.body -d > timeline.csv

# Buscar IOCs (Indicators of Compromise)
grep -r "malware.exe" /mnt/evidencia_montada/
grep -r "192.168.1.100" /mnt/evidencia_montada/var/log/
```

### 13.6 Playbooks de Respuesta

#### 13.6.1 Playbook: Ransomware

```yaml
INCIDENTE: Ransomware Detectado
SEVERIDAD: CRÍTICA (P1)
TIEMPO DE RESPUESTA: Inmediato

FASE 1: DETECCIÓN (0-5 minutos)
─────────────────────────────────
□ Alerta de EDR/Antivirus
□ Usuario reporta archivos cifrados
□ Nota de rescate encontrada
□ Identificar sistema(s) afectado(s)

FASE 2: CONTENCIÓN (5-30 minutos)
──────────────────────────────────
□ AISLAR sistema de la red (desconectar cable/WiFi)
□ NO apagar el sistema (preservar memoria RAM)
□ Identificar variante de ransomware
□ Verificar si hay propagación lateral
□ Aislar sistemas adicionales si es necesario
□ Bloquear IOCs en firewall

FASE 3: ANÁLISIS (30-60 minutos)
─────────────────────────────────
□ Capturar memoria RAM
□ Identificar vector de entrada
□ Determinar alcance del cifrado
□ Verificar integridad de backups
□ Buscar herramienta de descifrado (No More Ransom)
□ Documentar timeline del ataque

FASE 4: ERRADICACIÓN (1-4 horas)
─────────────────────────────────
□ Eliminar malware de sistemas afectados
□ Cambiar todas las credenciales
□ Aplicar parches de seguridad
□ Cerrar vector de entrada

FASE 5: RECUPERACIÓN (4-24 horas)
──────────────────────────────────
□ Restaurar desde backup limpio
□ Verificar integridad de archivos restaurados
□ Monitoreo intensivo por 72 horas
□ Retorno gradual a operación normal

FASE 6: POST-INCIDENTE (1-2 semanas)
─────────────────────────────────────
□ Reporte detallado del incidente
□ Lecciones aprendidas
□ Actualizar procedimientos
□ Capacitación adicional
□ Notificar a autoridades si corresponde

DECISIÓN: ¿PAGAR RESCATE?
──────────────────────────
❌ NO RECOMENDADO
├─ No garantiza recuperación
├─ Financia actividad criminal
├─ Puede ser ilegal (sanciones)
└─ Marca a la organización como objetivo

✓ ALTERNATIVAS
├─ Restaurar desde backups
├─ Buscar descifrador gratuito
├─ Reconstruir sistemas
└─ Consultar con autoridades
```

#### 13.6.2 Playbook: Brecha de Datos

```yaml
INCIDENTE: Exposición de Datos Personales
SEVERIDAD: ALTA (P2)
TIEMPO DE RESPUESTA: < 1 hora

FASE 1: CONFIRMACIÓN (0-30 minutos)
────────────────────────────────────
□ Verificar autenticidad del reporte
□ Identificar datos expuestos
□ Determinar número de registros afectados
□ Clasificar sensibilidad de datos

FASE 2: CONTENCIÓN (30-60 minutos)
───────────────────────────────────
□ Cerrar vector de exposición
□ Revocar accesos comprometidos
□ Preservar logs y evidencia
□ Documentar acciones tomadas

FASE 3: EVALUACIÓN (1-4 horas)
──────────────────────────────
□ Determinar causa raíz
□ Identificar período de exposición
□ Evaluar impacto en individuos
□ Determinar obligaciones legales

FASE 4: NOTIFICACIÓN (24-72 horas)
───────────────────────────────────
□ Notificar a URCDP (Uruguay) dentro de 72 horas
□ Notificar a individuos afectados
□ Preparar comunicado de prensa si es necesario
□ Coordinar con equipo legal

FASE 5: REMEDIACIÓN (1-2 semanas)
──────────────────────────────────
□ Implementar controles adicionales
□ Ofrecer servicios de protección (ej: monitoreo de crédito)
□ Actualizar políticas de seguridad
□ Capacitación del personal

OBLIGACIONES LEGALES (Uruguay - Ley 18.331)
────────────────────────────────────────────
✓ Notificar a URCDP dentro de 72 horas
✓ Notificar a titulares de datos si hay alto riesgo
✓ Documentar brecha en registro interno
✓ Cooperar con investigación de URCDP
```

### 13.7 Cadena de Custodia

```
┌────────────────────────────────────────────────────────────┐
│              FORMULARIO DE CADENA DE CUSTODIA              │
└────────────────────────────────────────────────────────────┘

CASO #: 2024-001
FECHA: 2024-01-15
INVESTIGADOR: Juan Pérez

EVIDENCIA RECOLECTADA:
─────────────────────
Item #: 001
Descripción: Disco duro SATA 1TB
Marca/Modelo: Seagate ST1000DM003
Serial: Z1D2ABCD
Hash SHA-256: a3f5b8c9d1e2f3a4b5c6d7e8f9a0b1c2...

RECOLECCIÓN:
────────────
Fecha/Hora: 2024-01-15 14:30
Ubicación: Servidor Web - Rack 3, Posición 2
Método: Imagen forense con dd
Recolectado por: Juan Pérez
Firma: _______________

TRANSFERENCIAS:
───────────────
1. De: Juan Pérez
   A: María González (Analista Forense)
   Fecha: 2024-01-15 15:00
   Propósito: Análisis forense
   Firma: _______________

2. De: María González
   A: Almacén de evidencia
   Fecha: 2024-01-16 18:00
   Propósito: Almacenamiento seguro
   Firma: _______________

NOTAS:
──────
- Evidencia almacenada en caja fuerte #5
- Acceso restringido a personal autorizado
- Mantener a temperatura ambiente
```

### 13.8 Laboratorio: Simulación de Incidente

```bash
# Escenario: Detectar y responder a backdoor

# 1. Preparar entorno
docker run -d --name victima ubuntu:20.04
docker exec -it victima bash

# 2. Simular compromiso (dentro del contenedor)
# Crear backdoor simple
cat > /tmp/backdoor.sh << 'EOF'
#!/bin/bash
while true; do
    nc -l -p 4444 -e /bin/bash
    sleep 5
done
EOF
chmod +x /tmp/backdoor.sh
nohup /tmp/backdoor.sh &

# Crear persistencia
echo "@reboot /tmp/backdoor.sh" | crontab -

# 3. DETECCIÓN (desde host)
# Escanear puertos abiertos
nmap -sV localhost -p 4444

# Verificar procesos sospechosos
docker exec victima ps aux | grep nc

# 4. ANÁLISIS
# Capturar memoria (si fuera sistema real)
# Revisar crontab
docker exec victima crontab -l

# Buscar archivos modificados recientemente
docker exec victima find /tmp -type f -mmin -60

# 5. CONTENCIÓN
# Matar proceso
docker exec victima pkill -f backdoor

# Eliminar persistencia
docker exec victima crontab -r

# 6. ERRADICACIÓN
# Eliminar backdoor
docker exec victima rm /tmp/backdoor.sh

# 7. DOCUMENTACIÓN
cat > incident_report.md << 'EOF'
# Reporte de Incidente #2024-001

## Resumen
Backdoor detectado en contenedor de producción

## Timeline
- 14:30: Alerta de puerto 4444 abierto
- 14:35: Confirmación de backdoor
- 14:40: Proceso terminado
- 14:45: Persistencia eliminada
- 14:50: Sistema limpio

## Causa Raíz
Imagen de contenedor comprometida

## Acciones Correctivas
- Escanear todas las imágenes con Trivy
- Implementar runtime security (Falco)
- Actualizar política de imágenes
EOF
```

