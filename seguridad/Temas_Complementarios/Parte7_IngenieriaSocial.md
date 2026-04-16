# CURSO COMPLETO DE CIBERSEGURIDAD - PARTE 8

## MÓDULO 12: INGENIERÍA SOCIAL Y AWARENESS TRAINING

### 12.1 ¿Qué es la Ingeniería Social?

**Definición:** Manipulación psicológica para que las personas revelen información confidencial o realicen acciones que comprometan la seguridad.

```
┌────────────────────────────────────────────────────────────┐
│         CICLO DE ATAQUE DE INGENIERÍA SOCIAL              │
└────────────────────────────────────────────────────────────┘

1. INVESTIGACIÓN
   ├─ OSINT (Open Source Intelligence)
   ├─ Redes sociales (LinkedIn, Facebook)
   ├─ Sitio web corporativo
   └─ Registros públicos
        │
        ▼
2. ESTABLECER CONFIANZA
   ├─ Hacerse pasar por autoridad
   ├─ Crear urgencia
   ├─ Apelar a emociones
   └─ Ofrecer ayuda
        │
        ▼
3. EXPLOTACIÓN
   ├─ Solicitar credenciales
   ├─ Pedir transferencia de dinero
   ├─ Instalar malware
   └─ Revelar información sensible
        │
        ▼
4. EJECUCIÓN
   └─ Usar información obtenida
```

### 12.2 Técnicas Comunes

#### 12.2.1 Pretexting

**Definición:** Crear un escenario falso para obtener información.

**Ejemplo:**
```
Atacante llama a empleado:

"Buenos días, soy del departamento de IT. Estamos 
actualizando el sistema y necesito verificar tu 
usuario y contraseña para migrar tu cuenta."

Señales de alerta:
❌ IT nunca pide contraseñas
❌ Llamada no solicitada
❌ Urgencia artificial
```

#### 12.2.2 Baiting

**Definición:** Ofrecer algo atractivo para infectar sistemas.

```
┌────────────────────────────────────────┐
│  ESCENARIO: USB MALICIOSO              │
└────────────────────────────────────────┘

1. Atacante deja USB en estacionamiento
   Etiqueta: "Salarios 2024 - CONFIDENCIAL"

2. Empleado curioso lo encuentra
   
3. Conecta USB a computadora corporativa

4. Autorun ejecuta malware

5. Atacante obtiene acceso a red interna
```

#### 12.2.3 Tailgating

**Definición:** Seguir a persona autorizada para acceder a área restringida.

```
┌────────────────────────────────────────┐
│  ESCENARIO FÍSICO                      │
└────────────────────────────────────────┘

Empleado → [Puerta con tarjeta] ← Atacante
    │              │                  │
    │ Pasa tarjeta │                  │
    │──────────────┤                  │
    │              │ Puerta abierta   │
    │              │                  │
    │ Entra        │                  │
    │──────────────>                  │
    │              │ "Espera, llevo   │
    │              │  cajas pesadas"  │
    │              │<─────────────────│
    │ Sostiene     │                  │
    │ puerta       │                  │
    │              │ Entra sin        │
    │              │ autorización     │
    │              │<─────────────────│
```

#### 12.2.4 Quid Pro Quo

**Definición:** Ofrecer servicio a cambio de información.

**Ejemplo:**
```
Atacante: "Soporte técnico, recibimos alerta de 
          virus en su computadora. ¿Puedo acceder 
          remotamente para solucionarlo?"

Víctima: "Sí, por favor"

Atacante: "Descargue este software de acceso remoto..."
          [Instala backdoor]
```

### 12.3 Vectores de Ataque

```
┌────────────────────────────────────────────────────────────┐
│              VECTORES DE INGENIERÍA SOCIAL                 │
└────────────────────────────────────────────────────────────┘

EMAIL (Phishing)
├─ Spear Phishing (dirigido)
├─ Whaling (ejecutivos)
└─ Business Email Compromise (BEC)

TELÉFONO (Vishing)
├─ Soporte técnico falso
├─ Banco/gobierno
└─ Premios/sorteos

SMS (Smishing)
├─ Links maliciosos
├─ Códigos de verificación
└─ Alertas falsas

REDES SOCIALES
├─ Perfiles falsos
├─ Mensajes directos
└─ Ingeniería social inversa

FÍSICO
├─ Tailgating
├─ Dumpster diving
└─ Shoulder surfing
```

### 12.4 Laboratorio: Simulación de Phishing

#### 12.4.1 Herramienta: Gophish

```bash
# Instalar Gophish
wget https://github.com/gophish/gophish/releases/download/v0.12.1/gophish-v0.12.1-linux-64bit.zip
unzip gophish-v0.12.1-linux-64bit.zip
chmod +x gophish
./gophish

# Acceder a https://localhost:3333
# Usuario: admin
# Contraseña: (ver consola)
```

#### 12.4.2 Crear Campaña de Phishing

```yaml
# Configuración de campaña
Nombre: "Simulacro IT - Actualización de Contraseña"

Plantilla de Email:
---
Asunto: Acción Requerida: Actualizar Contraseña

Estimado {{.FirstName}},

Por políticas de seguridad, debe actualizar su contraseña.

Haga clic aquí: {{.URL}}

Si no actualiza en 24 horas, su cuenta será bloqueada.

Saludos,
Departamento de IT
---

Página de Destino:
- Formulario de login falso
- Captura credenciales
- Redirige a sitio real
- Registra quién hizo clic

Grupo Objetivo:
- Departamento de Ventas (50 personas)

Resultados:
├─ Emails enviados: 50
├─ Emails abiertos: 35 (70%)
├─ Links clickeados: 15 (30%)
└─ Credenciales ingresadas: 8 (16%)
```

### 12.5 Programa de Awareness Training

#### 12.5.1 Estructura del Programa

```
┌────────────────────────────────────────────────────────────┐
│         PROGRAMA ANUAL DE CONCIENTIZACIÓN                  │
└────────────────────────────────────────────────────────────┘

MES 1-2: FUNDAMENTOS
├─ Qué es la ingeniería social
├─ Tipos de ataques
├─ Casos reales
└─ Quiz inicial

MES 3-4: PHISHING
├─ Identificar emails sospechosos
├─ Simulacro de phishing
├─ Análisis de resultados
└─ Capacitación remedial

MES 5-6: CONTRASEÑAS
├─ Gestores de contraseñas
├─ MFA obligatorio
├─ Políticas de contraseñas
└─ Ejercicio práctico

MES 7-8: SEGURIDAD FÍSICA
├─ Tailgating
├─ Clean desk policy
├─ Destrucción de documentos
└─ Simulacro físico

MES 9-10: REDES SOCIALES
├─ Oversharing
├─ Perfiles falsos
├─ Ingeniería social inversa
└─ Configuración de privacidad

MES 11-12: EVALUACIÓN
├─ Simulacro final
├─ Certificación
├─ Métricas de mejora
└─ Plan para próximo año
```

#### 12.5.2 Métricas de Éxito

```python
# Script para calcular métricas
class AwarenessMetrics:
    def __init__(self, campañas):
        self.campañas = campañas
    
    def calcular_tasa_clic(self):
        """Porcentaje de usuarios que hacen clic en phishing"""
        total_enviados = sum(c['enviados'] for c in self.campañas)
        total_clics = sum(c['clics'] for c in self.campañas)
        return (total_clics / total_enviados) * 100
    
    def calcular_mejora(self):
        """Mejora entre primera y última campaña"""
        primera = self.campañas[0]['tasa_clic']
        ultima = self.campañas[-1]['tasa_clic']
        return ((primera - ultima) / primera) * 100
    
    def identificar_usuarios_riesgo(self):
        """Usuarios que fallan múltiples simulacros"""
        usuarios_fallos = {}
        for campaña in self.campañas:
            for usuario in campaña['usuarios_fallaron']:
                usuarios_fallos[usuario] = usuarios_fallos.get(usuario, 0) + 1
        
        # Usuarios con 3+ fallos necesitan capacitación adicional
        return [u for u, fallos in usuarios_fallos.items() if fallos >= 3]

# Ejemplo de uso
campañas = [
    {'enviados': 100, 'clics': 30, 'tasa_clic': 30},  # Mes 1
    {'enviados': 100, 'clics': 20, 'tasa_clic': 20},  # Mes 3
    {'enviados': 100, 'clics': 10, 'tasa_clic': 10},  # Mes 6
    {'enviados': 100, 'clics': 5, 'tasa_clic': 5},    # Mes 12
]

metrics = AwarenessMetrics(campañas)
print(f"Mejora anual: {metrics.calcular_mejora():.1f}%")
# Output: Mejora anual: 83.3%
```

### 12.6 Defensa contra Ingeniería Social

#### 12.6.1 Políticas y Procedimientos

```markdown
# POLÍTICA DE SEGURIDAD - INGENIERÍA SOCIAL

## 1. VERIFICACIÓN DE IDENTIDAD
- Nunca revelar información por teléfono sin verificar identidad
- Usar canal alternativo para confirmar solicitudes inusuales
- Verificar emails sospechosos con remitente directamente

## 2. MANEJO DE INFORMACIÓN
- No discutir información confidencial en público
- Usar "need-to-know" basis
- Clasificar y etiquetar documentos

## 3. CONTRASEÑAS
- Nunca compartir contraseñas
- IT NUNCA solicita contraseñas
- Usar gestor de contraseñas corporativo

## 4. DISPOSITIVOS
- No conectar USBs desconocidos
- Bloquear pantalla al alejarse
- Reportar dispositivos perdidos inmediatamente

## 5. REPORTE DE INCIDENTES
- Botón de "Reportar Phishing" en email
- Línea directa de seguridad: ext. 5555
- No sentir vergüenza por reportar
```

#### 12.6.2 Señales de Alerta

```
┌────────────────────────────────────────────────────────────┐
│           RED FLAGS - INGENIERÍA SOCIAL                    │
└────────────────────────────────────────────────────────────┘

🚩 URGENCIA ARTIFICIAL
   "¡Su cuenta será bloqueada en 1 hora!"
   "Acción inmediata requerida"

🚩 AUTORIDAD FALSA
   "Soy del CEO/IT/Banco"
   Sin verificación de identidad

🚩 SOLICITUDES INUSUALES
   "Necesito tu contraseña"
   "Transfiere dinero a esta cuenta"

🚩 ERRORES GRAMATICALES
   Ortografía pobre
   Traducción automática evidente

🚩 INFORMACIÓN GENÉRICA
   "Estimado cliente" (sin nombre)
   Falta de detalles específicos

🚩 LINKS SOSPECHOSOS
   URL acortadas
   Dominios similares (typosquatting)
   HTTP en vez de HTTPS

🚩 ARCHIVOS ADJUNTOS
   Extensiones peligrosas (.exe, .zip, .scr)
   Nombres genéricos (factura.pdf.exe)
```

### 12.7 Ejercicios Prácticos

#### 12.7.1 Análisis de Email de Phishing

```
De: seguridad@bancoo-uruguay.com
Para: empleado@empresa.com
Asunto: URGENTE - Verificación de Cuenta

Estimado cliente,

Detectamos actividad sospechosa en su cuenta bancaria.
Por favor, verifique su identidad haciendo clic aquí:

[Verificar Ahora] → http://bit.ly/3xK9mP2

Si no verifica en 24 horas, su cuenta será suspendida.

Atentamente,
Banco Uruguay

---
EJERCICIO: Identifica 10 señales de alerta
```

**Respuestas:**
1. ❌ Dominio falso: bancoo vs banco
2. ❌ Saludo genérico: "Estimado cliente"
3. ❌ Urgencia artificial: "24 horas"
4. ❌ URL acortada: bit.ly
5. ❌ Amenaza: "cuenta será suspendida"
6. ❌ Solicitud de acción inmediata
7. ❌ Falta firma digital
8. ❌ No menciona nombre del cliente
9. ❌ Remitente no verificable
10. ❌ Banco nunca pide verificación por email

#### 12.7.2 Role-Playing: Vishing

```
ESCENARIO 1: Soporte Técnico Falso
─────────────────────────────────────
Atacante: "Buenos días, soporte de Microsoft. 
          Detectamos virus en su computadora."

Respuesta correcta:
✓ "Microsoft no hace llamadas no solicitadas"
✓ "Voy a colgar y llamar al número oficial"
✓ Reportar intento a seguridad

ESCENARIO 2: CEO Fraud
─────────────────────────────────────
Atacante: "Soy el CEO, necesito que transfieras 
          $50,000 urgentemente a este proveedor."

Respuesta correcta:
✓ "Voy a verificar por otro canal"
✓ Llamar directamente al CEO
✓ Seguir proceso de aprobación formal
```

### 12.8 Recursos y Herramientas

```bash
# Herramientas para Awareness Training

# 1. Gophish (Simulación de phishing)
https://getgophish.com

# 2. KnowBe4 (Plataforma comercial)
https://www.knowbe4.com

# 3. PhishMe (Simulación y reporte)
https://cofense.com

# 4. LUCY (Security Awareness)
https://lucysecurity.com

# 5. Social-Engineer Toolkit (SET)
git clone https://github.com/trustedsec/social-engineer-toolkit
cd social-engineer-toolkit
python setup.py install
```

### 12.9 Caso de Estudio: Twitter Hack 2020

```
┌────────────────────────────────────────────────────────────┐
│         CASO REAL: TWITTER HACK (Julio 2020)              │
└────────────────────────────────────────────────────────────┘

ATAQUE:
1. Atacantes usaron vishing contra empleados de Twitter
2. Se hicieron pasar por IT interno
3. Obtuvieron credenciales de panel administrativo
4. Accedieron a cuentas verificadas (Obama, Musk, Biden)
5. Publicaron scam de Bitcoin

IMPACTO:
- 130 cuentas comprometidas
- $120,000 robados en Bitcoin
- Daño reputacional masivo

LECCIONES:
✓ MFA no era obligatorio para todos
✓ Falta de capacitación en ingeniería social
✓ Acceso excesivo de herramientas internas
✓ No había verificación secundaria para acciones críticas

REMEDIACIONES:
✓ MFA obligatorio para todos
✓ Capacitación intensiva en vishing
✓ Principio de mínimo privilegio
✓ Monitoreo de accesos administrativos
```

