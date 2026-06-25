# LEY 18.331 - PROTECCIÓN DE DATOS PERSONALES URUGUAY

---

## ÍNDICE

1. Marco Normativo Uruguayo
2. Ámbito de Aplicación
3. Principios Fundamentales
4. Derechos de los Titulares (ARCO+)
5. Obligaciones de los Responsables
6. Autoridades de Control
7. Sanciones y Penalidades
8. Implementación Técnica
9. Guía de Cumplimiento
10. Plantilla: Registro de Actividades de Tratamiento

---

## 1. MARCO NORMATIVO URUGUAYO

```
┌─────────────────────────────────────────────────────────────────┐
│           MARCO NORMATIVO DE PROTECCIÓN DE DATOS EN URUGUAY      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CONSTITUCIÓN URUGUAY                                         │
│  └─ Artículo 72: Derecho a la protección de datos personales    │
│                                                                 │
│  LEY 18.331                                                     │
│  ├─ Ley de Protección de Datos Personales                      │
│  ├─ Regula el tratamiento de datos personales                  │
│  └─ Créase la URCDP                                           │
│                                                                 │
│  DECRETOS REGLAMENTARIOS                                       │
│  └─ Decreto 414/009: Reglamento de la Ley 18.331             │
│                                                                 │
│  AUTORIDADES                                                  │
│  └─ URCDP: Unidad Reguladora y de Control de Datos Personales │
│  └─ APD: Agencia de Protección de Datos (nueva)               │
│                                                                 │
│  CONEXIONES                                                   │
│  ├─ Ley 18.381: Acceso a la Información Pública              │
│  ├─ Ley 19.670: Documento de Identidad y Civil             │
│  └─ Ley 18.787: Servicios de Confianza para Firmas Digitales │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.1. Historia y Contexto

**Ley N° 18.331** fue promulgada el **11 de agosto de 2008** y modificada parcialmente por la Ley N° 19.670 del 29 de marzo de 2018.

**Objetivos:**
- Proteger los derechos fundamentales de las personas respecto a sus datos personales
- Regular el tratamiento automatizado y no automatizado de datos
- Garantizar el derecho al honor, intimidad y autodeterminación informativa

---

## 2. ÁMBITO DE APLICACIÓN

### 2.1. Ámbito Territorial

```
┌─────────────────────────────────────────────────────────────────┐
│                    ÁMBITO TERRITORIAL                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  La Ley 18.331 aplica a:                                       │
│                                                                 │
│  ✓ TODO tratamiento de datos de personas físicas                 │
│    residentes en Uruguay                                         │
│                                                                 │
│  ✓ TODO tratamiento realizado por                              │
│    organizaciones establecidas en Uruguay                        │
│                                                                 │
│  ✓ TRATAMIENTO desde Uruguay de datos de                     │
│    personas en el extranjero (si aplica ley local)             │
│                                                                 │
│  ✓ Organismos públicos y privados                              │
│                                                                 │
│  NO aplica a:                                                   │
│  ✗ Personas físicas en uso doméstico personal                  │
│  ✗ Actividades periodísticas o литературные                  │
│  ✗ Bases de datos con fines de seguridad pública              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2. Definiciones Clave

| Término | Definición |
|---------|------------|
| **Dato Personal** | Toda información sobre persona física identificada o identificable |
| **Dato Sensible** | Datos que revelan origen racial, étnico, político, religioso, filosófico, sindical, sexual, salud, biometric |
| **Tratamiento** | Cualquier operación sobre datos: collection, storage, retrieval, modification, disclosure |
| **Responsable** | Persona física o jurídica que decide sobre el tratamiento |
| **Encargado** | Persona que trata datos por cuenta del responsable |
| **Titular** | Persona física cuyos datos son tratados |
| ** Consentimiento** | Manifestación libre, voluntaria e informada |

---

## 3. PRINCIPIOS FUNDAMENTALES

### 3.1. Los 8 Principios de la Ley 18.331

```
┌─────────────────────────────────────────────────────────────────┐
│               PRINCIPIOS FUNDAMENTALES - LEY 18.331               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PRINCIPIO DE LEGALIDAD                                      │
│     └─ Todo tratamiento debe estar fundamentado legalmente     │
│                                                                 │
│  2. PRINCIPIO DE FINALIDAD                                     │
│     └─ Los datos se recopilan para fines específicos          │
│     └─ No usar para fines distintos a los declarados          │
│                                                                 │
│  3. PRINCIPIO DE PROPORCIONALIDAD                              │
│     └─ Solo recopilar datos necesarios para la finalidad        │
│     └─ Evitar exceso de información                            │
│                                                                 │
│  4. PRINCIPIO DE CALIDAD                                       │
│     └─ Datos exactos, completos y actualizados                  │
│     └─ Relevantes para la finalidad del tratamiento           │
│                                                                 │
│  5. PRINCIPIO DE TRANSPARENCIA                                 │
│     └─ Informar al titular sobre el tratamiento de sus datos    │
│     └─ Consentimiento informado                                │
│                                                                 │
│  6. PRINCIPIO DE SEGURIDAD                                    │
│     └─ Medidas técnicas y organizativas apropiadas              │
│     └─ Proteger contra acceso no autorizado                    │
│                                                                 │
│  7. PRINCIPIO DE CONFIDENCIALIDAD                              │
│     └─ Obligación de secreto profesional                       │
│     └─ No divulgar datos sin autorización                      │
│                                                                 │
│  8. PRINCIPIO DE RESPONSABILIDAD                               │
│     └─ El responsable debe demostrar cumplimiento              │
│     └─ Accountability (rendición de cuentas)                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2. Aplicación de Principios - Ejemplos

```python
# ============================================
# PRINCIPIO DE FINALIDAD - CUMPLIMIENTO
# ============================================

# ❌ INCORRECTO: Usar datos para fines no declarados
class ClienteService:
    def registrar_cliente(self, nombre, email, telefono):
        # Declara: datos para facturación
        self.db.guardar(nombre, email, telefono)
        
        # PROHIBIDO: Vender datos a terceros para marketing
        # sin consentimiento específico
        self.marketing_db.compartir(email, telefono)


# ✅ CORRECTO: Cumplimiento del principio de finalidad
class ClienteService:
    def registrar_cliente(self, nombre, email, telefono):
        # Solo usar para los fines declarados
        self.db.guardar(nombre, email, telefono, 
                       finalidad="facturacion")
        
        # Si quiere marketing, solicitar consentimiento separado
        if self.obtener_consentimiento_marketing(email):
            self.marketing_db.agregar(email)


# ============================================
# PRINCIPIO DE PROPORCIONALIDAD - CUMPLIMIENTO
# ============================================

# ❌ INCORRECTO: Recopilar datos excesivos
class FormularioRegistro:
    campos = [
        "nombre",           # Necesario
        "email",           # Necesario
        "telefono",        # Necesario
        # ❌ "color_ojos",     # Innecesario para banco
        # ❌ "altura",         # Innecesario
        # ❌ "religion",       # Dato sensible innecesario
    ]

# ✅ CORRECTO: Solo datos necesarios
class FormularioRegistro:
    campos_necesarios = {
        "nombre": "Para identificar al titular",
        "email": "Para notificaciones",
        "cedula": "Para verificación legal",
        # Solo lo estrictamente necesario
    }
```

---

## 4. DERECHOS DE LOS TITULARES (ARCO+)

### 4.1. Derechos ARCO+ Completos

```
┌─────────────────────────────────────────────────────────────────┐
│                 DERECHOS ARCO+ DEL TITULAR                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  A - ACCESO                                                     │
│  ├─ Conocer qué datos tienen sobre mí                         │
│  ├─ Origen de los datos                                        │
│  ├─ Finalidad del tratamiento                                 │
│  └─ Cómo contactarlos                                         │
│                                                                 │
│  R - RECTIFICACIÓN                                             │
│  ├─ Corregir datos inexactos o incompletos                    │
│  ├─ Actualizar datos desactualizados                           │
│  └─ Plazo: 10 días hábiles                                    │
│                                                                 │
│  C - CANCELACIÓN (Supresión)                                   │
│  ├─ Eliminar datos (derecho al olvido)                         │
│  ├─ Cuando ya no son necesarios                               │
│  ├─ Cuando se retira consentimiento                            │
│  └─ Excepto: obligaciones legales de conservación           │
│                                                                 │
│  O - OPOSICIÓN                                                 │
│  ├─ Oponerse al tratamiento                                    │
│  ├─ Tratamiento para marketing directo                        │
│  └─ Decisiones automatizadas                                   │
│                                                                 │
│  + PORTABILIDAD                                                │
│  ├─ Recibir datos en formato estructurado                     │
│  ├─ Transmitir a otro responsable                             │
│  └─ Formato: CSV, JSON, XML                                   │
│                                                                 │
│  + INFORMACIÓN                                                  │
│  ├─ Conocer la lógica de decisiones automatizadas              │
│  └─ Significado e consecuencias del tratamiento               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2. Implementación de Derechos

```python
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Base de datos simulada
usuarios_db = {
    "12345678": {
        "nombre": "Juan Pérez",
        "email": "juan@email.com",
        "cedula": "12345678",
        "telefono": "099123456",
        "fecha_nacimiento": "1990-05-15",
        "consenti_marketing": True,
        "fecha_registro": "2024-01-15"
    }
}

# ============================================
# DERECHO A - ACCESO
# ============================================

@app.route('/api/derechos/acceso', methods=['POST'])
def derecho_acceso():
    """
    El titular puede solicitar acceso a sus datos.
    """
    data = request.json
    cedula = data.get('cedula')
    
    # Verificar identidad
    if not verificar_identidad(cedula, data.get('codigo_verificacion')):
        return jsonify({"error": "Identidad no verificada"}), 401
    
    usuario = usuarios_db.get(cedula)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    # Información adicional requerida por Ley 18.331
    return jsonify({
        "datos": usuario,
        "informacion_adicional": {
            "origen_datos": "Recopilados directamente del titular",
            "finalidad": "Gestión de servicios financieros",
            "destinatarios": ["Auditoría interna", "BCU (por ley)"],
            "plazo_conservacion": "10 años (obligación legal)",
            "ultima_actualizacion": datetime.now().isoformat()
        },
        "fecha_respuesta": datetime.now().isoformat()
    })

# ============================================
# DERECHO R - RECTIFICACIÓN
# ============================================

@app.route('/api/derechos/rectificacion', methods=['POST'])
def derecho_rectificacion():
    """
    El titular puede corregir datos inexactos.
    """
    data = request.json
    cedula = data.get('cedula')
    
    if not verificar_identidad(cedula, data.get('codigo_verificacion')):
        return jsonify({"error": "Identidad no verificada"}), 401
    
    usuario = usuarios_db.get(cedula)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    # Campos que se pueden rectificar
    campos_permitidos = ['nombre', 'email', 'telefono', 'direccion']
    
    for campo in campos_permitidos:
        if campo in data.get('datos_nuevos', {}):
            usuario[campo] = data['datos_nuevos'][campo]
    
    usuario['ultima_rectificacion'] = datetime.now().isoformat()
    
    return jsonify({
        "mensaje": "Datos rectificados correctamente",
        "datos_actualizados": usuario,
        "plazo": "10 días hábiles (comunicado a receptores)"
    })

# ============================================
# DERECHO C - CANCELACIÓN (SUPLEMENTACIÓN)
# ============================================

@app.route('/api/derechos/cancelacion', methods=['POST'])
def derecho_cancelacion():
    """
    El titular puede solicitar eliminación de datos.
    """
    data = request.json
    cedula = data.get('cedula')
    
    if not verificar_identidad(cedula, data.get('codigo_verificacion')):
        return jsonify({"error": "Identidad no verificada"}), 401
    
    usuario = usuarios_db.get(cedula)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    # Verificar excepciones legales
    if tiene_obligacion_legal_conservacion(cedula):
        return jsonify({
            "error": "Datos protegidos por obligación legal",
            "detalle": "Los datos deben conservarse por normativa BCU",
            "plazo_conservacion": "10 años"
        }), 400
    
    # Eliminar datos (en la práctica, marcar como eliminados)
    usuario['estado'] = 'eliminado'
    usuario['fecha_eliminacion'] = datetime.now().isoformat()
    usuario['causa'] = 'Solicitud de titular - Derecho C'
    
    return jsonify({
        "mensaje": "Datos eliminados correctamente",
        "fecha_eliminacion": datetime.now().isoformat(),
        "nota": "Se mantienen datos anonimizados para estadísticas"
    })

# ============================================
# DERECHO O - OPOSICIÓN
# ============================================

@app.route('/api/derechos/oposicion', methods=['POST'])
def derecho_oposicion():
    """
    El titular puede oponerse al tratamiento.
    """
    data = request.json
    cedula = data.get('cedula')
    motivo = data.get('motivo')
    tipo_tratamiento = data.get('tipo_tratamiento')
    
    if not verificar_identidad(cedula, data.get('codigo_verificacion')):
        return jsonify({"error": "Identidad no verificada"}), 401
    
    usuario = usuarios_db.get(cedula)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    # Registrar oposición
    oposicion = {
        "fecha": datetime.now().isoformat(),
        "motivo": motivo,
        "tipo_tratamiento": tipo_tratamiento,
        "estado": "procedente"
    }
    
    # Si es marketing directo, cesar inmediatamente
    if tipo_tratamiento == 'marketing_directo':
        usuario['consenti_marketing'] = False
        oposicion["estado"] = "aplicada_inmediatamente"
    
    return jsonify({
        "mensaje": "Oposición registrada",
        "detalle": oposicion,
        "plazo_respuesta": "10 días hábiles"
    })

# ============================================
# DERECHO + PORTABILIDAD
# ============================================

@app.route('/api/derechos/portabilidad', methods=['POST'])
def derecho_portabilidad():
    """
    El titular puede recibir sus datos en formato portable.
    """
    data = request.json
    cedula = data.get('cedula')
    formato = data.get('formato', 'json')
    
    if not verificar_identidad(cedula, data.get('codigo_verificacion')):
        return jsonify({"error": "Identidad no verificada"}), 401
    
    usuario = usuarios_db.get(cedula)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    # Preparar datos en formato solicitado
    datos_portables = preparar_datos_portables(usuario, formato)
    
    return jsonify({
        "datos": datos_portables,
        "formato": formato,
        "fecha_extraccion": datetime.now().isoformat(),
        "nota": "Datos para transmisión a otro responsable"
    })

def verificar_identidad(cedula, codigo):
    """Verificación básica de identidad"""
    # En producción: verificar con múltiples factores
    return cedula and codigo

def tiene_obligacion_legal_conservacion(cedula):
    """Verificar obligaciones legales de conservación"""
    # BCU requiere conservación de datos financieros
    return True  # Simplificado

def preparar_datos_portables(datos, formato):
    """Preparar datos en formato portable"""
    if formato == 'csv':
        return convertir_a_csv(datos)
    elif formato == 'json':
        return datos
    return datos
```

---

## 5. OBLIGACIONES DE LOS RESPONSABLES

### 5.1. Obligaciones Principales

```
┌─────────────────────────────────────────────────────────────────┐
│              OBLIGACIONES DEL RESPONSABLE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  OBLIGACIONES PREVENTIVAS                                      │
│  ├─ Registrar la base de datos ante URCDP                      │
│  ├─ Implementar medidas de seguridad técnicas                  │
│  ├─ Designar responsable de seguridad                         │
│  └─ Realizar evaluaciones de impacto (EIPD)                  │
│                                                                 │
│  OBLIGACIONES DURANTE EL TRATAMIENTO                           │
│  ├─ Obtener consentimiento válido                              │
│  ├─ Informar al titular sobre el tratamiento                  │
│  ├─ Mantener secreto profesional                             │
│  ├─ Notificar brechas de seguridad                           │
│  └─ Mantener registro de actividades                         │
│                                                                 │
│  OBLIGACIONES POST-TRATAMIENTO                                 │
│  ├─ Responder ejercicios de derechos en 10 días               │
│  ├─ Cesar tratamiento si hay oposición                        │
│  ├─ Eliminar datos cuando finalice plazo                      │
│  └─ Certificar destrucción de datos                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2. Registro de Actividades de Tratamiento (RAT)

```markdown
# REGISTRO DE ACTIVIDADES DE TRATAMIENTO
# Conforme a Ley 18.331 - Uruguay

## 1. INFORMACIÓN GENERAL

| Campo | Descripción |
|-------|-------------|
| Identificación del responsable | Banco XYZ Uruguay S.A. |
| RUT | 21.123.456-7 |
| Actividad económica | Servicios financieros |
| Responsable de datos | Juan García, DPO |
| Contacto | dpo@bancoxyz.com.uy / 2900 1234 |

---

## 2. BASE DE DATOS: CLIENTES

| Campo | Descripción |
|-------|-------------|
| Nombre de la BD | CLIENTES_FINANCIEROS |
| Finalidad | Gestión de cuentas, préstamos, tarjetas |
| Base legal | Ejecución contractual + Obligación legal (BCU) |
| Categorías de interesados | Personas físicas clientas |

### 2.1 Categorías de Datos

| Categoría | Ejemplos | ¿Sensible? |
|----------|----------|-------------|
| Identificación | Nombre, CI, RUT, firma | No |
| Contacto | Email, teléfono, dirección | No |
| Financieros | Cuenta, saldo, movimientos | No |
| Transaccionales | Fecha, monto, tipo operación | No |
| Crediticios | Score, historial, deudas | No |
| Salud | (no se recopilan) | - |

### 2.2 Origen de los Datos

| Origen | Método |
|--------|--------|
| Directamente del titular | Formularios, contratos, entrevistas |
| Fuentes públicas | BCU (central de riesgos), BPS |
| Terceros autorizados | Burós de crédito |

### 2.3 Destinatarios (Comunicación de Datos)

| Destinatario | Datos compartidos | Finalidad | Base legal |
|--------------|-------------------|-----------|------------|
| BCU | Datos crediticios | Supervisión financiera | Ley 18.331 Art. 21 |
| Brady | Información crediticia | Consulta de riesgo | Consentimiento |
| Proveedor Cloud AWS | Todos los datos | Almacenamiento | Contrato con cláusula ADP |
| Auditoría externa | Datos estructurados | Auditoría anual | Obligación legal |

### 2.4 Transferencias Internacionales

| Destinatario | País | Garantías | Finalidad |
|--------------|------|-----------|-----------|
| AWS US-East | EE.UU. | Cláusulas contractuales tipo | Procesamiento en la nube |

### 2.5 Plazos de Conservación

| Categoría | Plazo | Justificación |
|-----------|-------|---------------|
| Datos de cuenta | 10 años | Obligación BCU |
| Transacciones | 10 años | Obligación BCU |
| Documentos KYC | 10 años | Ley lavado de activos |
| Correos informativos | 5 años | Conservación comercial |

### 2.6 Medidas de Seguridad

| Medida | Implementación |
|--------|----------------|
| Cifrado en tránsito | TLS 1.3 |
| Cifrado en reposo | AES-256 |
| Control de acceso | RBAC + MFA |
| Auditoría | Logs inmutables, 2 años |
| Backup | Diario, retención 30 días |
| Pruebas penetración | Anual |

---

## 3. BASE DE DATOS: MARKETING

| Campo | Descripción |
|-------|-------------|
| Nombre | MARKETING_CLIENTES |
| Finalidad | Envío de ofertas, newsletters |
| Base legal | **Consentimiento expreso** |
| Categorías interesados | Clientes que optaron por marketing |

### Datos Recopitados

| Campo | Ejemplos | Finalidad |
|-------|----------|------------|
| Email | usuario@email.com | Contacto |
| Teléfono | 099123456 | SMS marketing |
| Preferencias | Intereses declarados | Ofertas personalizadas |

### Consentimiento

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONSENTIMIENTO MARKETING                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ☐ Acepto recibir comunicaciones comerciales de Banco XYZ    │
│    por email, SMS y WhatsApp                                  │
│                                                                 │
│  ☐ Acepto recibir ofertas personalizadas basadas en          │
│    mi perfil y comportamiento                                  │
│                                                                 │
│  Puedo revocar este consentimiento en cualquier momento       │
│  desde mi perfil o enviando email a: bajas@bancoxyz.com.uy   │
│                                                                 │
│  Última actualización de preferencias: ___________            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. EVALUACIÓN DE IMPACTO (EIPD)

Para tratamientos de datos sensibles o de alto riesgo, se debe realizar EIPD:

```markdown
# EVALUACIÓN DE IMPACTO DE PROTECCIÓN DE DATOS
# Conforme a Ley 18.331

## 1. DESCRIPCIÓN DEL TRATAMIENTO

| Campo | Descripción |
|-------|-------------|
| Nombre | Sistema de Score Crediticio con IA |
| Responsable | Banco XYZ |
| Fecha | 01/03/2024 |

## 2. EVALUACIÓN DE NECESIDAD

- ¿El tratamiento es necesario? Sí - Decisiones crediticias
- ¿Existe alternativa menos invasiva? No - Requerimiento BCU
- ¿Los beneficios justifican el riesgo? Sí - Mitigaciones implementadas

## 3. EVALUACIÓN DE RIESGOS

| Riesgo | Probabilidad | Impacto | Medida de mitigación |
|--------|--------------|---------|----------------------|
| Decisión automatizada errónea | Media | Alto | Revisión humana obligatoria > $50,000 |
| Discriminación algorítmica | Baja | Alto | Auditoría de sesgo trimestral |
| Brecha de datos | Baja | Muy alto | AES-256 + MFA + SOC 2 |

## 4. CONCLUSIÓN

El tratamiento puede proceder con las medidas de mitigación propuestas.
```

---

## 6. AUTORIDADES DE CONTROL

### 6.1. URCDP - Unidad Reguladora y de Control de Datos Personales

```
┌─────────────────────────────────────────────────────────────────┐
│                    URCDP - FUNCIONES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FUNCIONES PRINCIPALES:                                         │
│                                                                 │
│  1. REGISTRO                                                   │
│     └─ Inscribir bases de datos                               │
│     └─ Llevar registro de responsables                         │
│                                                                 │
│  2. CONTROL                                                     │
│     └─ Fiscalizar cumplimiento                                │
│     └─ Realizar inspecciones                                  │
│     └─ Investigar denuncias                                    │
│                                                                 │
│  3. SANCION                                                     │
│     └─ Multas                                                   │
│     └─ Clausura                                                │
│     └─ Decomiso de datos                                       │
│                                                                 │
│  4. ASESORAMIENTO                                              │
│     └─ Emitir dictámenes                                      │
│     └─ Publicar guías y mejores prácticas                     │
│                                                                 │
│  CONTACTO:                                                     │
│  └─ web: www.gub.uy/urcdp                                    │
│  └─ email: urcdp@agesic.gub.uy                              │
│  └─ teléfono: 134 (interno) o 150                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2. Procedimiento de Registro

```python
# ============================================
# REGISTRO DE BASE DE DATOS ANTE URCDP
# ============================================

class RegistroURCDP:
    """
    Representa el registro de una base de datos ante URCDP.
    """
    
    def __init__(self):
        self.campos_requeridos = [
            "nombre_base_datos",
            "responsable",
            "finalidad",
            "categorias_datos",
            "categorias_interesados",
            "origen_datos",
            "destinatarios",
            "transferencias_internacionales",
            "plazo_conservacion",
            "medidas_seguridad",
            "contacto_dpo"
        ]
    
    def generar_solicitud(self, datos):
        """
        Genera la solicitud de inscripción de base de datos.
        """
        # Validar campos requeridos
        for campo in self.campos_requeridos:
            if campo not in datos:
                raise ValueError(f"Campo requerido: {campo}")
        
        # Formato según normativa URCDP
        return {
            "tipo_solicitud": "INSCRIPCION_BASE_DATOS",
            "numero_registro": generar_numero_registro(),
            "fecha_solicitud": datetime.now().isoformat(),
            "datos": datos,
            "firmado_por": "Responsable de datos / DPO",
            "fecha_inscripcion": None,  # Completado por URCDP
            "estado": "pendiente"
        }


# Ejemplo de uso
registro = RegistroURCDP()
solicitud = registro.generar_solicitud({
    "nombre_base_datos": "CLIENTES_FINANCIEROS",
    "responsable": "Banco XYZ Uruguay S.A.",
    "finalidad": "Gestión de servicios financieros y cumplimiento normativo BCU",
    "categorias_datos": ["identificación", "financieros", "transaccionales"],
    "categorias_interesados": ["clientes personas físicas"],
    "origen_datos": ["directo del titular", "fuentes públicas"],
    "destinatarios": ["BCU", "Brady", "proveedores autorizados"],
    "transferencias_internacionales": [],
    "plazo_conservacion": "10 años",
    "medidas_seguridad": ["cifrado AES-256", "MFA", "logs auditoría"],
    "contacto_dpo": "dpo@bancoxyz.com.uy"
})
```

---

## 7. SANCIONES Y PENALIDADES

### 7.1. Régimen Sancionatorio

```
┌─────────────────────────────────────────────────────────────────┐
│                 SANCIONES - LEY 18.331                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INFRACCIONES LEVES                                             │
│  ├─ No informar al titular sobre tratamiento                   │
│  ├─ No atender ejercicio de derechos en plazo                  │
│  └─ Multa: 100-1.000 UI                                        │
│                                                                 │
│  INFRACCIONES GRAVES                                            │
│  ├─ Tratamiento sin consentimiento válido                     │
│  ├─ Violación de principios fundamentales                      │
│  ├─ No implementar medidas de seguridad                        │
│  ├─ No notificar brecha de seguridad                          │
│  └─ Multa: 1.000-50.000 UI                                     │
│                                                                 │
│  INFRACCIONES MUY GRAVES                                        │
│  ├─ Tratar datos sensibles sin consentimiento                  │
│  ├─ Generar bases de datos para fines illicitados             │
│  ├─ Obstruir labor de fiscalización                           │
│  └─ Multa: 50.000-500.000 UI                                    │
│                                                                 │
│  OTRAS MEDIDAS                                                  │
│  ├─ Clausura temporal del tratamiento                         │
│  ├─ Clausura definitiva                                        │
│  ├─ Decomiso de los datos                                      │
│  └─ Publicación de la sanción                                 │
│                                                                 │
│  RESPONSABILIDAD PENAL                                          │
│  └─ Artículo 301 bis Código Penal:                             │
│     Difusión indebida de datos personales                      │
│     Pena: 6 meses - 2 años de prisión                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2. Cálculo de UI

```python
# ============================================
# CÁLCULO DE SANCIONES EN UI
# ============================================

class CalculadoraSanciones:
    """
    Calcula el rango de sanciones según Ley 18.331
    """
    
    # Valor de UI (aproximado, verificar valor actual)
    VALOR_UI_URUGUAY = 4.10  # dólares aproximadamente
    
    INFRACCIONES = {
        "leve": {"min": 100, "max": 1000, "tipo": "UI"},
        "grave": {"min": 1000, "max": 50000, "tipo": "UI"},
        "muy_grave": {"min": 50000, "max": 500000, "tipo": "UI"},
    }
    
    @classmethod
    def calcular_sancion(cls, tipo_infraccion, agravantes=None):
        """
        Calcula el rango de sanción
        
        Args:
            tipo_infraccion: 'leve', 'grave', 'muy_grave'
            agravantes: lista de factores agravantes
        
        Returns:
            dict con rango en UI y USD
        """
        rango = cls.INFRACCIONES.get(tipo_infraccion, {})
        
        if not rango:
            return {"error": "Tipo de infracción no válido"}
        
        # Aplicar agravantes
        multiplicador = 1.0
        if agravantes:
            for agravante in agravantes:
                multiplicador += 0.25  # 25% por cada agravante
        
        min_ui = rango["min"] * multiplicador
        max_ui = rango["max"] * multiplicador
        
        return {
            "tipo": tipo_infraccion,
            "rango_ui": f"{min_ui:,.0f} - {max_ui:,.0f} UI",
            "rango_usd": f"${min_ui * cls.VALOR_UI_URUGUAY:,.0f} - ${max_ui * cls.VALOR_UI_URUGUAY:,.0f}",
            "agravantes_aplicados": len(agravantes) if agravantes else 0
        }

# Ejemplos
print(CalculadoraSanciones.calcular_sancion("grave"))
# {'tipo': 'grave', 'rango_ui': '1,000 - 50,000 UI', 
#  'rango_usd': '$4,100 - $205,000'}

print(CalculadoraSanciones.calcular_sancion(
    "muy_grave", 
    ["datos_sensibles", "afectados_mayores_1000"]
))
# {'tipo': 'muy_grave', 'rango_ui': '125,000 - 1,250,000 UI', 
#  'rango_usd': '$512,500 - $5,125,000'}
```

---

## 8. IMPLEMENTACIÓN TÉCNICA

### 8.1. Checklist de Cumplimiento

```markdown
# CHECKLIST DE CUMPLIMIENTO - LEY 18.331

## REGISTRO Y DOCUMENTACIÓN
- [ ] Registro de bases de datos ante URCDP actualizado
- [ ] Registro de actividades de tratamiento (RAT) documentado
- [ ] Políticas de privacidad publicadas
- [ ] Avisos de cookies implementados
- [ ] Términos y condiciones de servicio actualizados

## CONSENTIMIENTO
- [ ] Consentimiento informado obtenido
- [ ] Consentimiento específico para datos sensibles
- [ ] Consentimiento explícito para marketing
- [ ] Registro de consentimientos con fecha y hora
- [ ] Mecanismo de revocación implementado

## DERECHOS ARCO+
- [ ] Portal de ejercicios de derechos funcionando
- [ ] Proceso de verificación de identidad implementado
- [ ] Plazo de respuesta 10 días hábiles configurado
- [ ] Proceso de portabilidad disponible
- [ ] Proceso de oposición documentado

## SEGURIDAD
- [ ] Cifrado de datos en reposo (AES-256)
- [ ] Cifrado de datos en tránsito (TLS 1.3)
- [ ] Control de acceso basado en roles (RBAC)
- [ ] Autenticación multifactor (MFA)
- [ ] Logs de auditoría inmutables
- [ ] Plan de respuesta a brechas documentado
- [ ] Notificación a URCDP en caso de brecha (72 horas)

## GOVERNANCE
- [ ] DPO (Delegado de Protección de Datos) designado
- [ ] Capacitación del personal anual
- [ ] Evaluación de impacto (EIPD) para tratamientos de riesgo
- [ ] Revisión periódica de medidas de seguridad
- [ ] Contratos con encargados de tratamiento firmados
```

### 8.2. Implementación de Medidas de Seguridad

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import hashlib
import hmac

class SeguridadLey18331:
    """
    Implementa medidas de seguridad según Ley 18.331
    """
    
    # ============================================
    # CIFRADO DE DATOS
    # ============================================
    
    @staticmethod
    def cifrar_dato_sensible(dato, clave_master):
        """
        Cifra datos sensibles con AES-256
        Requerido para datos sensibles bajo Ley 18.331
        """
        # Generar clave de sesión
        salt = os.urandom(16)
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        clave_sesion = kdf.derive(clave_master)
        
        # Cifrar con Fernet (AES-CBC)
        f = Fernet(clave_sesion)
        dato_cifrado = f.encrypt(dato.encode())
        
        return {
            "dato_cifrado": dato_cifrado,
            "salt": salt,
            "algoritmo": "AES-256-CBC",
            "iteraciones": 480000
        }
    
    # ============================================
    # CONTROL DE ACCESO
    # ============================================
    
    @staticmethod
    def verificar_acceso(usuario, recurso, accion):
        """
        Implementa control de acceso según principio de menor privilegio
        """
        permisos = {
            "admin": ["leer", "escribir", "eliminar", "auditar"],
            "operador": ["leer", "escribir"],
            "consulta": ["leer"],
            "auditor": ["leer", "auditar"]
        }
        
        rol = usuario.get("rol", "consulta")
        permisos_rol = permisos.get(rol, [])
        
        if accion not in permisos_rol:
            raise PermisoDenegado(f"Acceso denegado a {recurso}")
        
        # Registrar en log de auditoría
        registrar_acceso(usuario, recurso, accion)
        
        return True
    
    # ============================================
    # NOTIFICACIÓN DE BRECHAS
    # ============================================
    
    @staticmethod
    def notificar_brecha(brecha):
        """
        Notifica brecha a URCDP en 72 horas
        Requerido por Ley 18.331
        """
        notificacion = {
            "tipo": "BRECHA_DATOS_PERSONALES",
            "fecha_deteccion": datetime.now().isoformat(),
            "naturaleza_brecha": brecha.get("descripcion"),
            "datos_afectados": brecha.get("categorias_datos"),
            "categorias_interesados": brecha.get("interesados"),
            "consecuencias_probables": brecha.get("impacto"),
            "medidas_adoptadas": brecha.get("mitigacion"),
            "medidas_propuestas": brecha.get("acciones_futuras"),
            "contacto_dpo": brecha.get("contacto_dpo")
        }
        
        # Enviar a URCDP dentro de 72 horas
        enviar_notificacion_urcdp(notificacion)
        
        # Notificar afectados si es necesario
        if brecha.get("riesgo_interesados"):
            notificar_interesados(brecha)
        
        return {"estado": "notificacion_enviada", "fecha_limite": calcular_fecha_limite()}


# ============================================
# DECORADOR PARA VERIFICAR CONSENTIMIENTO
# ============================================

def verificar_consentimiento(tipo_tratamiento):
    """
    Decorador que verifica consentimiento antes de procesar datos
    """
    def decorador(funcion):
        def wrapper(usuario, *args, **kwargs):
            # Verificar si existe consentimiento válido
            if not usuario.tiene_consentimiento(tipo_tratamiento):
                raise ConsentimientoRequerido(
                    f"Se requiere consentimiento para: {tipo_tratamiento}"
                )
            
            # Verificar si el consentimiento está vigente
            if usuario.consentimiento_expirado(tipo_tratamiento):
                raise ConsentimientoExpirado(
                    f"El consentimiento para {tipo_tratamiento} ha expirado"
                )
            
            return funcion(usuario, *args, **kwargs)
        return wrapper
    return decorador


# Uso
@verificar_consentimiento("marketing_directo")
def enviar_marketing(usuario, mensaje):
    # Solo se ejecuta si hay consentimiento válido
    pass
```

---

## 9. GUÍA DE CUMPLIMIENTO

### 9.1. Pasos para Implementar Cumplimiento

```
┌─────────────────────────────────────────────────────────────────┐
│              GUÍA DE CUMPLIMIENTO - LEY 18.331                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 1: DIAGNÓSTICO (Meses 1-2)                              │
│  ─────────────────────────────────                             │
│  □ Inventariar todas las bases de datos                        │
│  □ Identificar flujos de datos personales                       │
│  □ Evaluar nivel de cumplimiento actual                         │
│  □ Identificar gaps y riesgos                                  │
│                                                                 │
│  FASE 2: DISEÑO (Meses 3-4)                                   │
│  ────────────────────────                                      │
│  □ Diseñar arquitectura de privacidad                          │
│  □ Implementar Privacy by Design                               │
│  □ Definir políticas y procedimientos                         │
│  □ Seleccionar herramientas técnicas                           │
│                                                                 │
│  FASE 3: IMPLEMENTACIÓN (Meses 5-8)                           │
│  ────────────────────────────────────                          │
│  □ Implementar controles técnicos                               │
│  □ Configurar sistemas de gestión                              │
│  □ Capacitar personal                                          │
│  □ Realizar pruebas                                            │
│                                                                 │
│  FASE 4: REGISTRO Y DOCUMENTACIÓN (Mes 9)                     │
│  ────────────────────────────────────────                     │
│  □ Registrar bases de datos ante URCDP                         │
│  □ Publicar políticas de privacidad                           │
│  □ Documentar procedimientos                                  │
│  □ Implementar portal de ejercicios de derechos               │
│                                                                 │
│  FASE 5: MONITOREO CONTINUO                                    │
│  ──────────────────────────────                                │
│  □ Auditorías periódicas                                       │
│  □ Revisión de medidas de seguridad                           │
│  □ Actualización de registros                                 │
│  □ Formación continua                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2. Recursos y Referencias

| Recurso | Descripción | Link |
|---------|-------------|------|
| Portal URCDP | Autoridad de control | gub.uy/urcdp |
| Guía ADP | Guía de implementación | agesic.gub.uy |
| Ley 18.331 | Texto completo | Parlamento.gub.uy |
| Decreto 414/009 | Reglamento | legislativen.gub.uy |
| Modelo de Registro | Plantilla URCDP | Portal URCDP |

---

## 10. PLANTILLA: REGISTRO DE ACTIVIDADES DE TRATAMIENTO

```markdown
# PLANTILLA: REGISTRO DE ACTIVIDADES DE TRATAMIENTO
# Conforme a Ley 18.331 de Uruguay
# Última actualización: [FECHA]
# Responsable del registro: [NOMBRE/DPO]

---

## INFORMACIÓN DEL RESPONSABLE

| Campo | Valor |
|-------|-------|
| Razón Social | |
| RUT | |
| Dirección | |
| Teléfono | |
| Email de contacto | |
| DPO/Delegado de Protección | |
| Email DPO | |

---

## BASE DE DATOS: [NOMBRE]

### Información General

| Campo | Descripción |
|-------|-------------|
| Identificador | |
| Denominación | |
| Finalidad | |
| Base legal | |

### Categorías de Datos

| Categoría | Ejemplos | ¿Sensible? |
|-----------|----------|-------------|
| | | |

### Categorías de Interesados

| Categoría | Descripción |
|-----------|-------------|
| | |

### Origen de los Datos

| Origen | Método de recopilación |
|--------|------------------------|
| | |

### Comunicación de Datos (Destinatarios)

| Destinatario | Datos | Finalidad | Base legal |
|--------------|-------|-----------|------------|
| | | | |

### Transferencias Internacionales

| Destinatario | País | Garantías |
|--------------|------|-----------|
| | | |

### Plazo de Conservación

| Categoría de datos | Plazo | Justificación legal |
|-------------------|-------|-------------------|
| | | |

### Medidas de Seguridad Implementadas

| Medida | Implementación |
|--------|----------------|
| | |

---

## HISTORIAL DE ACTUALIZACIONES

| Fecha | Descripción del cambio | Responsable |
|-------|----------------------|-------------|
| | | |
```

---

**Documento:** Ley 18.331 - Protección de Datos Personales Uruguay  
**Versión:** 1.0  
**Última actualización:** 2026
