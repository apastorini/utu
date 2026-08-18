# GUÍA PRÁCTICA: RESPUESTA A INCIDENTES DE CIBERSEGURIDAD EN EL BHU
## Todo lo que necesitás saber para el día a día

---

## 1. ¿CUÁNTA PROBABILIDAD HAY DE RECIBIR UN CIBERATAQUE?

### Respuesta corta: **Altísima. Es cuándo, no si.**

### Datos reales de Uruguay (CERTuy):
- **2024:** 14.264 incidentes detectados (+187% vs 2023)
- **2025 primer semestre:** 17.015 incidentes
- **2025 total:** 42.768 incidentes (crecimiento del 199,83%)
- **0,17-0,48%** se clasifican como severidad "alta" o "muy alta"

### ¿Por qué un banco es blanco frecuente?
- **Dinero directo:** ransomware, fraude, transferencias no autorizadas
- **Datos valiosos:** cédulas, cuentas, historiales crediticios de millones de uruguayos
- **Ransomware:** el ataque más común - cifran tus sistemas y piden rescate
- **Phishing:** el 95% de los incidentes empiezan por error humano
- **Supply chain:** atacan a tus proveedores para llegar a vos

### Tipos de ataques más probables en un banco uruguayo:
| Tipo | Probabilidad | Impacto |
|------|-------------|---------|
| Phishing a empleados | Muy alta | Medio-Alto |
| Ransomware | Alta | Muy Alto |
| Fraude en transacciones | Alta | Alto |
| Ataque DDoS (negación de servicio) | Media | Medio |
| Infiltración de malware | Media | Alto |
| Robo de credenciales | Alta | Alto |
| Ingeniería social | Muy alta | Medio |
| Ataque a proveedores (supply chain) | Media | Muy Alto |

---

## 2. ¿CÓMO SE MIDE SI UN ATAQUE ES GRAVE O NO?

### Clasificación de severidad (basado en ENISA/CERTuy):

#### Nivel 1 - BAJO (Informativo)
- Intento de ataque fallido
- Phishing detectado y bloqueado
- Vulnerabilidad identificada sin explotación
- **Acción:** Registrar y monitorear

#### Nivel 2 - MEDIO
- Malware detectado en un equipo aislado
- Acceso no autorizado a un sistema no crítico
- Violación menor de políticas de uso
- **Acción:** Investigar, contener, remediar internamente

#### Nivel 3 - ALTO
- Ransomware que afecta sistemas operativos
- Acceso no autorizado a sistemas con datos sensibles
- Pérdida o robo de dispositivo con información crítica
- Ataque que afecta la disponibilidad de servicios al cliente
- **Acción:** Activar plan de respuesta, reportar a CERTuy, evaluar reporte a URCDP

#### Nivel 4 - MUY ALTO (Crítico)
- Ransomware que cifra servidores principales o backups
- Exfiltración masiva de datos de clientes
- Compromiso del core bancario o sistemas de pagos
- Ataque que paraliza completamente la operación
- **Acción:** Activar protocolo de crisis, reportar inmediatamente a CERTuy, URCDP, BCU, Cibercrimen

### Criterios para evaluar gravedad:

**Preguntate:**
1. **¿Qué activos se vieron afectados?** (servidores críticos = grave, workstation aislada = menos grave)
2. **¿Hay datos de clientes comprometidos?** (si = SIEMPRE grave)
3. **¿Se afectó la disponibilidad de servicios?** (si = grave)
4. **¿Hay evidencia de exfiltración de datos?** (si = muy grave)
5. **¿El ataque sigue activo?** (si = urgente)
6. **¿Los backups están intactos?** (si no = crítico)

### Matriz de decisión rápida:

```
¿Hay datos personales comprometidos?
├── SÍ → Grave a Muy Grave → URCDP (72hs) + CERTuy (24hs)
└── NO → Evaluar otros criterios

¿Se afectó la disponibilidad de servicios?
├── SÍ al cliente → Grave → CERTuy (24hs)
└── NO → Evaluar otros criterios

¿El ataque sigue activo?
├── SÍ → URGENTE → Contener primero, reportar después
└── NO → Evaluar alcance

¿Los backups están comprometidos?
├── SÍ → CRÍTICO → Crisis total
└── NO → Recuperable
```

---

## 3. ¿CUÁNDO DEBO AVISAR A LA UNIDAD DE CIBERCRIMEN DEL MINISTERIO DEL INTERIOR?

### Contacto:
- **Email:** dipn-cibercrimen@minterior.gub.uy
- **Teléfono:** (+598) 2030 4625
- **Dirección:** Dirección General de Cibercrimen - Policía Nacional

### ¿Cuándo reportarles?
**SIEMPRE que haya un DELITO informático.** Ellos son la policía, no el CERTuy. Son cosas diferentes.

### Situaciones que requieren denuncia policial:
| Situación | ¿Denunciar? |
|-----------|------------|
| Robo de información/confidencialidad de datos | **SÍ** |
| Fraude electrónico (transferencias no autorizadas) | **SÍ** |
| Ransomware (extorsión) | **SÍ** |
| Suplantación de identidad | **SÍ** |
| Acceso ilícito a sistemas | **SÍ** |
| Daño informático (destrucción de datos) | **SÍ** |
| Ingeniería social para obtener credenciales | **SÍ** |
| Phishing bloqueado sin daño | No necesario (pero sí registrar) |
| Vulnerabilidad detectada internamente | No necesario |

### ¿Cómo se denuncia?
1. Presentar denuncia **presencial** en la Dirección General de Cibercrimen
2. Adjuntar evidencia forense (logs, capturas, informes)
3. Coordinar con ellos la investigación
4. Ellos pueden pedir colaboración internacional si el atacante está en el exterior

### IMPORTANTE:
- La denuncia policial es **paralela** al reporte al CERTuy y URCDP
- No excluye una ni la otra
- La denuncia policial inicia la **investigación judicial**
- El CERTuy ayuda técnicamente, la Policía investiga el delito

---

## 4. ¿CUÁNDO AVISO AL CERTuy?

### Obligación legal (Art. 78 Ley N° 20.212 + Decreto 66/025):
**DENTRO DE LAS 24 HORAS** de detectado el incidente.

### ¿Qué es un incidente que debés reportar?
Cualquier evento que:
- Comprometa la confidencialidad, integridad o disponibilidad de activos de información
- Ponga en riesgo los servicios críticos del banco
- Vulnere las políticas de seguridad de la información
- Pueda afectar a clientes, proveedores o al sistema financiero

### ¿Cómo reportar?
1. **Formulario online:** https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/institucional/contacto
2. **Email:** cert@cert.uy (incluí: nombre, contacto, organización, descripción del problema)
3. **Urgencias:** (+5982) 150 2378 (las 24 horas)

### Qué información enviar al CERTuy:
- Fecha y hora de detección
- Tipo de incidente (malware, ransomware, acceso no autorizado, etc.)
- Sistemas/activos afectados
- Alcance estimado (¿cuántos usuarios/sistemas?)
- Si hay datos personales comprometidos
- Acciones ya tomadas
- Contacto del responsable (vos)

### REGLA DE ORO:
**"Reportá primero, investigá después."**
No esperes a tener toda la información. Reportá con lo que tengas y actualizá.

### El CERTuy puede:
- Intervenir tus sistemas (con tu acuerdo) para ayudar a resolver
- Coordinar con otros organismos
- Analizar evidencia forense
- Proporcionar asistencia técnica
- Guardar reserva de la información

---

## 5. ¿CUÁNDO DEBO AVISAR A LA URCDP (Protección de Datos)?

### Plazo: **DENTRO DE LAS 72 HORAS** de constatada la vulneración

### ¿Cuándo?
**SIEMPRE que se identifique O SE SOSPECHE** de afectación de datos personales.

### Datos personales son:
- Cédulas de identidad
- Nombres y apellidos
- Direcciones
- Teléfonos
- Emails
- Cuentas bancarias
- Historiales crediticios
- Salarios
- Cualquier dato que identifique a una persona

### Ejemplos concretos en un banco:
- Un empleado envió por error una planilla con cédulas a un proveedor
- Un ransomware cifró la base de datos de recursos humanos
- Se detectó que un usuario externo accedió al CRM y exportó contactos
- Un servidor con datos de clientes quedó expuesto en internet
- Robo de un laptop con información de clientes

### ¿Qué informar a la URCDP?
- Fecha cierta o estimada de la vulneración
- Naturaleza del incidente
- Datos personales afectados
- Posibles impactos generados
- Acciones tomadas para minimizar el impacto

### ¿Y a los clientes afectados?
**SÍ.** El Art. 4 del Decreto 64/020 dice que debés comunicar a los titulares de datos que sufrieron "una afectación significativa en sus derechos", en "lenguaje claro y sencillo".

### Contacto URCDP:
- **Teléfono:** (+598) 2901 0065 int. 3
- **Trámite online:** https://tramites.gub.uy/ampliados?id=1671
- **Horario:** lunes a viernes de 09:30 a 17:30

---

## 6. ¿CUÁNDO EJECUTO ACCIONES FORENSES VS. PREVENCIÓN?

### Acciones PREVENTIVAS (antes del incidente):
| Acción | Cuándo |
|--------|--------|
| Parches de seguridad | Mantenimiento regular |
| Monitoreo de vulnerabilidades | Continuo |
| Auditorías de seguridad | Trimestral/Anual |
| Pentests | Anual |
| Capacitación al personal | Continuo |
| Campañas de concientización | Trimestral |
| Respaldos verificados | Semanal/Diario |
| Revisiones de acceso | Mensual |

### Acciones FORENSES (después del incidente):
| Acción | Cuándo |
|--------|--------|
| Captura de evidencia | Inmediatamente al detectar |
| Análisis de logs | Durante la investigación |
| Análisis de malware | Si se encontró software malicioso |
| Cadena de custodia | Siempre que haya evidencia judicial |
| Análisis de memoria/disco | Si hay compromiso de sistema |
| Análisis de red | Si hay evidencia de movimiento lateral |

### REGLA PRÁCTICA:
```
¿Está activo el ataque?
├── SÍ → CONTENER primero (apagar, aislar, bloquear)
│         No hacer forensía todavía, primero parar el daño
└── NO → Preservar evidencia y comenzar análisis forense

¿Necesitás evidencia para denuncia policial?
├── SÍ → cadena de custodia estricta
└── NO → análisis interno, pero preservar por si acaso
```

---

## 7. ¿CÓMO EJECUTO ACCIONES FORENSES?

### Protocolo básico de respuesta forense:

#### Paso 1: Detección y Activación (0-1 horas)
1. Quien detecta el incidente **notifica inmediatamente** al RSI (a vos)
2. Vos activás el **Equipo de Respuesta a Incidentes**
3. Se evalúa la gravedad (usá la matriz del punto 2)
4. Se decide si escalar a crisis

#### Paso 2: Contención (1-4 horas)
**NO TOCAR nada todavía. Primero contener:**
- **Aislar** el sistema afectado (desconectar de red, NO apagar)
- **Bloquear** cuentas comprometidas
- **Cambiar** credenciales de administradores
- **Identificar** si el ataque sigue activo
- **Preservar** evidencia (no borrar logs, no formatear)

#### Paso 3: Recolección de evidencia (4-24 horas)
1. **Capturar imagen forense** del disco afectado (herramientas: FTK Imager, dd, EnCase)
2. **Capturar volátiles** antes de apagar: memoria RAM, conexiones de red, procesos activos
3. **Exportar logs** de firewalls, IDS/IPS, servidores, Active Directory
4. **Documentar TODO**: fechas, horas, quién hizo qué
5. **Mantener cadena de custodia**: quién tocó la evidencia, cuándo, dónde se almacena

#### Paso 4: Análisis (24-72 horas)
- Determinar **cómo entró** el atacante (vector de entrada)
- Determinar **qué hizo** dentro de los sistemas
- Determinar **qué datos** se vieron comprometidos
- Identificar **indicators of compromise (IoC)**
- Buscar **presencia del atacante** en otros sistemas

#### Paso 5: Erradicación y Recuperación (días)
- Eliminar malware y accesos del atacante
- Restaurar sistemas desde backups limpios
- Cambiar TODAS las credenciales que pudieron haberse visto comprometidas
- Parchar la vulnerabilidad que fue explotada

#### Paso 6: Lecciones aprendidas
- Documentar todo el incidente
- Identificar qué salió bien y qué no
- Implementar mejoras
- Actualizar el plan de respuesta

### Herramientas recomendadas (algunas gratuitas):
| Herramienta | Uso | Costo |
|------------|-----|-------|
| FTK Imager | Imágenes forenses de disco | Gratis |
| Autopsy | Análisis forense de disco | Gratis (open source) |
| Volatility | Análisis de memoria RAM | Gratis (open source) |
| Wireshark | Captura de tráfico de red | Gratis |
| YARA | Detección de malware | Gratis |
| Sigma | Detección basada en logs | Gratis |
| Velociraptor | Respuesta a incidentes en endpoints | Gratis (open source) |

---

## 8. ¿TODO DEBE ESTAR PREVIAMENTE POR ESCRITO?

### **SÍ. ABSOLUTAMENTE SÍ.**

Esto no es opcional. Sin documentación previa, cuando ocurra el incidente vas a estar improvisando bajo presión, y eso lleva a errores graves.

### Documentos que DEBEN existir ANTES de cualquier incidente:

#### Obligatorios por normativa:
1. **Política de Seguridad de la Información** (SF.SEG.08 - ya existe en BHU)
2. **Política de Gestión de Riesgos de SI**
3. **Procedimiento de Gestión de Incidentes de SI**
4. **Plan de Respuesta a Incidentes**
5. **Procedimiento de Reporte a Autoridades** (CERTuy, URCDP, Cibercrimen)
6. **Metodología de Evaluación de Riesgos**
7. **Política de Control de Acceso**
8. **Política de Dispositivos Móviles**
9. **Acuerdos de Confidencialidad** con personal
10. **Procedimiento de Desvinculación de Personal**

#### Altamente recomendados:
11. **Plan de Comunicación de Crisis** (quién habla con la prensa, clientes, Directorio)
12. **Matriz de contactos de emergencia** (quién llama a quién)
13. **Procedimiento forense interno**
14. **Acuerdos con proveedores de respuesta a incidentes**
15. **Plan de Continuidad de Negocio**
16. **Procedimiento de copias de seguridad y restauración**

### ¿Por qué es tan importante tenerlo escrito?
- **Presión:** durante un incidente estás estresado, no vas a estar pensando racionalmente
- **Tiempo:** cada minuto cuenta, no podés estar inventando protocolos
- **Legal:** si no tenés procedimientos documentados, la URCDP y BCU pueden sancionarte
- **Evidencia:** si hay investigación policial, necesitás demostrar que tenías controles
- **Coordinación:** todos deben saber qué hacer sin preguntarle a nadie

---

## 9. ¿QUÉ HAGO CON EL EQUIPO DE RESPUESTA A INCIDENTES?

### Composición del equipo (debe estar definido ANTES):

| Rol | Persona | Responsabilidad |
|-----|---------|----------------|
| **Líder del equipo** | RSI (vos) | Coordinar toda la respuesta |
| **Técnico forense** | Jefe de Seguridad de TI o externo | Análisis técnico, evidencia |
| **Representante de TI** | Ing. Herrera o equivalente | Acceso a sistemas, restauración |
| **Comunicaciones** | Secretaría General o prensa | Comunicar interna/externamente |
| **Jurídico** | Dirección Jurídica | Asesoramiento legal, denuncias |
| **Negocio** | Gerencia General | Decisiones de negocio |
| **Capital Humano** | Si hay aspectos laborales | Si el incidente involucra un empleado |

### Flujo de escalamiento:
```
Empleado detecta algo raro
    ↓
Notifica a su jefe
    ↓
Jefe notifica al RSI (vos)
    ↓
RSI evalúa gravedad
    ↓
├── BAJO/MEDIO → Investigación interna
├── ALTO → Activa equipo de respuesta
└── MUY ALTO → Activa protocolo de crisis
    ↓
Notificar a CERTuy (24hs)
    ↓
Si hay datos personales → Notificar URCDP (72hs)
    ↓
Si hay delito → Denunciar a Cibercrimen
    ↓
Seguimiento hasta cierre
```

---

## 10. ¿CUÁNDO NOTIFICO Y QUÉ HAGO CON EL DIRECTORIO/Gerencia?

### Notificación al Directorio/Gerencia General:

| Severidad | ¿Notificar? | Cuándo | Cómo |
|-----------|-------------|--------|------|
| Bajo | No (reporte mensual) | En reporte periódico | Informe escrito |
| Medio | Sí | Dentro de 24 horas | Email + reunión |
| Alto | Sí, urgente | Inmediatamente | Llamada telefónica + reunión presencial |
| Muy Alto | Sí, crisis | Inmediatamente | Reunión de crisis presencial |

### Qué decirle a la Gerencia General:
1. **Qué pasó** (en términos de negocio, no técnicos)
2. **Qué impacto tiene** (clientes afectados, servicios caídos, datos comprometidos)
3. **Qué estamos haciendo** (acciones de contención)
4. **Qué necesitamos** (recursos, decisiones)
5. **Qué plazos hay** (reportes regulatorios, restauración estimada)

---

## 11. ¿ME QUEDO EN LA OFICINA O ME VOY A CASA?

### Depende del tipo de incidente:

#### Si es un incidente MENOR (nivel 1-2):
- Podés irte a casa después de coordinar las acciones iniciales
- Mantener disponibilidad por teléfono
- Seguir el día siguiente con investigación

#### Si es un incidente ALTO (nivel 3):
- **QUEDARSE** hasta estabilizar la situación
- Coordinar con el equipo de respuesta
- Asegurar que la contención esté funcionando
- Reportar a las autoridades (CERTuy, URCDP)
- Recién cuando esté contenido, irse a descansar
- Mantener disponibilidad 24/7 hasta la recuperación

#### Si es un incidente CRÍTICO (nivel 4):
- **NO TE VAS A CASA.** Esto es crisis.
- Activar protocolo de crisis
- Reunir al equipo de respuesta
- Coordinar con CERTuy, URCDP, BCU, Cibercrimen
- Mantener al Directorio informado
- Trabajar en turnos si es necesario (pero vos como RSI debés estar disponible)
- La recuperación puede tardar días

### REGLA GENERAL:
**"Si el incidente sigue activo o hay datos comprometidos, no te vas."**

---

## 12. CHECKLIST RÁPIDA PARA IMPRIMIR Y PEGAR EN TU ESCRITORIO

### SI DETECTÁS UN INCIDENTE:

- [ ] 1. **NO PANTALlear.** Respirá. Los incidentes se manejan, no se resuelven con pánico.
- [ ] 2. **Identificá** qué pasó (tipo de ataque, sistemas afectados, cuándo se detectó)
- [ ] 3. **Contené** (aislá sistemas comprometidos, bloqueá accesos)
- [ ] 4. **Preservá evidencia** (NO borres nada, NO apagues nada)
- [ ] 5. **Notificá** al equipo de respuesta a incidentes
- [ ] 6. **Evaluá gravedad** (usá la matriz)
- [ ] 7. **Reportá al CERTuy** si es nivel 3 o 4 (plazo: 24 horas)
- [ ] 8. **Reportá a URCDP** si hay datos personales comprometidos (plazo: 72 horas)
- [ ] 9. **Denunciá a Cibercrimen** si hay delito (robo, fraude, ransomware)
- [ ] 10. **Notificá** a Gerencia General según severidad
- [ ] 11. **Documentá** TODO (fechas, horas, acciones, personas involucradas)
- [ ] 12. **Coordiná** la recuperación y erradicación
- [ ] 13. **Lecciones aprendidas** al cerrar el incidente

### CONTACTOS DE EMERGENCIA:

| Organización | Contacto | Cuándo usar |
|-------------|----------|-------------|
| CERTuy | cert@cert.uy / (+5982) 150 2378 | SIEMPRE que haya incidente (24hs) |
| URCDP | (+598) 2901 0065 int. 3 | Si hay datos personales (72hs) |
| Cibercrimen | dipn-cibercrimen@minterior.gub.uy / (+598) 2030 4625 | Si hay delito informático |
| BCU Supervisión | (consultar número interno) | Si es relevante para la entidad financiera |

---

## 13. ¿CUÁNDO CONTRATAR AYUDA EXTERNA?

### Considerá contratar un proveedor especializado de respuesta a incidentes si:
- No tenés personal forense especializado interno
- El incidente es complejo (APT, ransomware avanzado)
- Necesitás análisis forense para presentar como evidencia judicial
- El incidente afecta sistemas críticos del core bancario
- NecesitásMonitoreo 24/7 que no podés cubrir internamente

### Proveedores en Uruguay (ejemplos, no son endorsados):
- WhiteJaguars (ciberseguridad bancaria)
- Empresas de consultoría de seguridad con servicio de respuesta
- CERTuy puede asesorar sobre proveedores confiables

### Qué pedirle al proveedor:
- Experiencia en respuesta a incidentes del sector financiero
- Capacidad forense certificada
- Disponibilidad 24/7
- Referencias comprobables
- Acuerdos de confidencialidad
- Cadena de custodia de evidencia

---

*Documento de uso práctico. Imprimí la sección 12 y pegala en tu escritorio.*
*Última actualización: Julio 2026*
