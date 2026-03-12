# CURSO COMPLETO DE CIBERSEGURIDAD - PARTE 10

## MÓDULO 14: COMPLIANCE Y ESTÁNDARES INTERNACIONALES

### 14.1 Panorama de Compliance

```
┌────────────────────────────────────────────────────────────┐
│         PRINCIPALES ESTÁNDARES Y REGULACIONES              │
└────────────────────────────────────────────────────────────┘

SEGURIDAD DE LA INFORMACIÓN
├─ ISO/IEC 27001 (Internacional)
├─ ISO/IEC 27002 (Controles)
├─ NIST Cybersecurity Framework (EE.UU.)
└─ CIS Controls (Internacional)

PRIVACIDAD DE DATOS
├─ GDPR (Unión Europea)
├─ Ley 18.331 (Uruguay)
├─ CCPA (California, EE.UU.)
└─ LGPD (Brasil)

INDUSTRIAS ESPECÍFICAS
├─ PCI-DSS (Pagos con tarjeta)
├─ HIPAA (Salud - EE.UU.)
├─ SOX (Empresas públicas - EE.UU.)
└─ GLBA (Servicios financieros - EE.UU.)

AUDITORÍA Y CERTIFICACIÓN
├─ SOC 2 (Service Organization Control)
├─ ISO 9001 (Calidad)
└─ ISO 22301 (Continuidad del negocio)
```

### 14.2 ISO/IEC 27001

#### 14.2.1 Estructura del Estándar

```
┌────────────────────────────────────────────────────────────┐
│              ISO/IEC 27001:2022                            │
└────────────────────────────────────────────────────────────┘

CLÁUSULAS PRINCIPALES:

4. CONTEXTO DE LA ORGANIZACIÓN
   ├─ Comprender la organización
   ├─ Necesidades de partes interesadas
   ├─ Alcance del SGSI
   └─ Sistema de Gestión

5. LIDERAZGO
   ├─ Compromiso de la dirección
   ├─ Política de seguridad
   └─ Roles y responsabilidades

6. PLANIFICACIÓN
   ├─ Evaluación de riesgos
   ├─ Tratamiento de riesgos
   └─ Objetivos de seguridad

7. SOPORTE
   ├─ Recursos
   ├─ Competencia
   ├─ Concienciación
   └─ Comunicación

8. OPERACIÓN
   ├─ Planificación operacional
   ├─ Evaluación de riesgos
   └─ Tratamiento de riesgos

9. EVALUACIÓN DEL DESEMPEÑO
   ├─ Monitoreo y medición
   ├─ Auditoría interna
   └─ Revisión por la dirección

10. MEJORA
    ├─ No conformidades
    ├─ Acciones correctivas
    └─ Mejora continua
```

#### 14.2.2 Anexo A - 93 Controles

```
┌────────────────────────────────────────────────────────────┐
│         ISO 27001:2022 - ANEXO A (Controles)              │
└────────────────────────────────────────────────────────────┘

A.5 CONTROLES ORGANIZACIONALES (37 controles)
├─ A.5.1 Políticas de seguridad
├─ A.5.7 Threat intelligence
├─ A.5.10 Uso aceptable de información
├─ A.5.23 Seguridad en la nube
└─ ...

A.6 CONTROLES DE PERSONAS (8 controles)
├─ A.6.1 Selección de personal
├─ A.6.2 Términos y condiciones de empleo
├─ A.6.3 Concienciación en seguridad
└─ ...

A.7 CONTROLES FÍSICOS (14 controles)
├─ A.7.1 Perímetros de seguridad física
├─ A.7.4 Monitoreo de seguridad física
├─ A.7.7 Clear desk y clear screen
└─ ...

A.8 CONTROLES TECNOLÓGICOS (34 controles)
├─ A.8.1 Dispositivos de usuario final
├─ A.8.5 Autenticación segura
├─ A.8.9 Gestión de configuración
├─ A.8.16 Actividades de monitoreo
├─ A.8.23 Filtrado web
└─ ...
```

#### 14.2.3 Implementación Práctica

```python
# Ejemplo: Matriz de Aplicabilidad de Controles

class ControlISO27001:
    def __init__(self, codigo, nombre, aplicable, justificacion, implementado):
        self.codigo = codigo
        self.nombre = nombre
        self.aplicable = aplicable
        self.justificacion = justificacion
        self.implementado = implementado
        self.evidencia = []
    
    def agregar_evidencia(self, tipo, descripcion, ubicacion):
        self.evidencia.append({
            'tipo': tipo,
            'descripcion': descripcion,
            'ubicacion': ubicacion
        })

# Ejemplo de controles
controles = [
    ControlISO27001(
        codigo="A.5.1",
        nombre="Políticas de seguridad de la información",
        aplicable=True,
        justificacion="Requerido para establecer dirección de seguridad",
        implementado=True
    ),
    ControlISO27001(
        codigo="A.8.5",
        nombre="Autenticación segura",
        aplicable=True,
        justificacion="Proteger acceso a sistemas críticos",
        implementado=True
    )
]

# Agregar evidencia
controles[0].agregar_evidencia(
    tipo="Documento",
    descripcion="Política de Seguridad v2.1",
    ubicacion="/documentos/politicas/seguridad_v2.1.pdf"
)

controles[1].agregar_evidencia(
    tipo="Configuración",
    descripcion="MFA habilitado en todos los sistemas",
    ubicacion="Azure AD > Security > MFA Settings"
)

# Generar reporte de cumplimiento
def generar_reporte_cumplimiento(controles):
    total = len(controles)
    aplicables = sum(1 for c in controles if c.aplicable)
    implementados = sum(1 for c in controles if c.aplicable and c.implementado)
    
    porcentaje = (implementados / aplicables) * 100 if aplicables > 0 else 0
    
    print(f"Controles totales: {total}")
    print(f"Controles aplicables: {aplicables}")
    print(f"Controles implementados: {implementados}")
    print(f"Cumplimiento: {porcentaje:.1f}%")
    
    # Controles pendientes
    pendientes = [c for c in controles if c.aplicable and not c.implementado]
    if pendientes:
        print("\nControles pendientes:")
        for c in pendientes:
            print(f"  - {c.codigo}: {c.nombre}")

generar_reporte_cumplimiento(controles)
```

### 14.3 PCI-DSS (Payment Card Industry Data Security Standard)

#### 14.3.1 12 Requisitos

```
┌────────────────────────────────────────────────────────────┐
│              PCI-DSS v4.0 (2024)                           │
└────────────────────────────────────────────────────────────┘

CONSTRUIR Y MANTENER RED SEGURA
├─ 1. Instalar y mantener firewall
└─ 2. No usar contraseñas por defecto

PROTEGER DATOS DE TARJETAHABIENTES
├─ 3. Proteger datos almacenados
└─ 4. Cifrar transmisión de datos

MANTENER PROGRAMA DE GESTIÓN DE VULNERABILIDADES
├─ 5. Proteger contra malware
└─ 6. Desarrollar sistemas seguros

IMPLEMENTAR MEDIDAS DE CONTROL DE ACCESO
├─ 7. Restringir acceso por necesidad de negocio
├─ 8. Identificar y autenticar acceso
└─ 9. Restringir acceso físico

MONITOREAR Y PROBAR REDES
├─ 10. Registrar y monitorear accesos
└─ 11. Probar sistemas regularmente

MANTENER POLÍTICA DE SEGURIDAD
└─ 12. Mantener política de seguridad de información
```

#### 14.3.2 Niveles de Cumplimiento

```
┌────────────────────────────────────────────────────────────┐
│         NIVELES DE COMERCIANTES PCI-DSS                    │
└────────────────────────────────────────────────────────────┘

NIVEL 1
├─ Volumen: > 6 millones transacciones/año
├─ Validación: Auditoría anual por QSA
├─ Escaneo: Trimestral por ASV
└─ Reporte: ROC (Report on Compliance)

NIVEL 2
├─ Volumen: 1-6 millones transacciones/año
├─ Validación: SAQ anual
├─ Escaneo: Trimestral por ASV
└─ Puede requerir auditoría

NIVEL 3
├─ Volumen: 20,000-1 millón transacciones/año
├─ Validación: SAQ anual
└─ Escaneo: Trimestral por ASV

NIVEL 4
├─ Volumen: < 20,000 transacciones/año
├─ Validación: SAQ anual
└─ Escaneo: Trimestral por ASV (recomendado)
```

#### 14.3.3 Ejemplo: Tokenización de Tarjetas

```python
# Implementación de tokenización para PCI-DSS

import hashlib
import secrets
from cryptography.fernet import Fernet

class TokenizadorTarjetas:
    def __init__(self):
        # Clave de cifrado (debe estar en HSM en producción)
        self.clave = Fernet.generate_key()
        self.cipher = Fernet(self.clave)
        self.vault = {}  # Base de datos de tokens
    
    def tokenizar(self, numero_tarjeta):
        """
        Convierte número de tarjeta en token
        Almacena tarjeta cifrada en vault seguro
        """
        # Validar formato de tarjeta
        if not self._validar_tarjeta(numero_tarjeta):
            raise ValueError("Número de tarjeta inválido")
        
        # Generar token único
        token = self._generar_token()
        
        # Cifrar número de tarjeta
        tarjeta_cifrada = self.cipher.encrypt(numero_tarjeta.encode())
        
        # Almacenar en vault (en producción: base de datos segura)
        self.vault[token] = tarjeta_cifrada
        
        return token
    
    def detokenizar(self, token):
        """
        Recupera número de tarjeta original desde token
        Solo para procesos autorizados
        """
        if token not in self.vault:
            raise ValueError("Token no encontrado")
        
        tarjeta_cifrada = self.vault[token]
        numero_tarjeta = self.cipher.decrypt(tarjeta_cifrada).decode()
        
        return numero_tarjeta
    
    def _generar_token(self):
        """Genera token aleatorio de 16 caracteres"""
        return secrets.token_hex(8).upper()
    
    def _validar_tarjeta(self, numero):
        """Validación básica de formato"""
        # Eliminar espacios y guiones
        numero = numero.replace(' ', '').replace('-', '')
        
        # Verificar que sean solo dígitos
        if not numero.isdigit():
            return False
        
        # Verificar longitud (13-19 dígitos)
        if len(numero) < 13 or len(numero) > 19:
            return False
        
        # Algoritmo de Luhn
        return self._luhn_check(numero)
    
    def _luhn_check(self, numero):
        """Algoritmo de Luhn para validar tarjetas"""
        def digitos(n):
            return [int(d) for d in str(n)]
        
        digitos_tarjeta = digitos(numero)
        checksum = digitos_tarjeta[-1]
        digitos_tarjeta = digitos_tarjeta[:-1]
        digitos_tarjeta.reverse()
        
        total = 0
        for i, d in enumerate(digitos_tarjeta):
            if i % 2 == 0:
                d = d * 2
                if d > 9:
                    d = d - 9
            total += d
        
        return (total + checksum) % 10 == 0

# Uso
tokenizador = TokenizadorTarjetas()

# Procesar pago
numero_tarjeta = "4532-1234-5678-9010"
token = tokenizador.tokenizar(numero_tarjeta)
print(f"Token: {token}")  # Almacenar en BD

# Procesar reembolso (requiere número original)
numero_original = tokenizador.detokenizar(token)
print(f"Tarjeta: {numero_original[-4:]}")  # Mostrar solo últimos 4 dígitos
```

### 14.4 SOC 2 (Service Organization Control)

#### 14.4.1 Trust Service Criteria

```
┌────────────────────────────────────────────────────────────┐
│              SOC 2 TRUST SERVICE CRITERIA                  │
└────────────────────────────────────────────────────────────┘

SEGURIDAD (Obligatorio)
├─ Control de acceso
├─ Detección de amenazas
├─ Gestión de cambios
└─ Respuesta a incidentes

DISPONIBILIDAD (Opcional)
├─ Monitoreo de performance
├─ Recuperación ante desastres
└─ Gestión de capacidad

INTEGRIDAD DE PROCESAMIENTO (Opcional)
├─ Validación de datos
├─ Manejo de errores
└─ Procesamiento completo y preciso

CONFIDENCIALIDAD (Opcional)
├─ Cifrado de datos
├─ Gestión de claves
└─ Disposición segura

PRIVACIDAD (Opcional)
├─ Consentimiento
├─ Derechos del titular
└─ Retención de datos
```

#### 14.4.2 Tipos de Reportes

```
SOC 2 TIPO I
├─ Evaluación: Diseño de controles
├─ Momento: Punto en el tiempo
├─ Duración: 1 día
└─ Uso: Validar que controles existen

SOC 2 TIPO II
├─ Evaluación: Diseño y efectividad operativa
├─ Momento: Período de tiempo (6-12 meses)
├─ Duración: Auditoría continua
└─ Uso: Demostrar que controles funcionan
```

### 14.5 GDPR (General Data Protection Regulation)

#### 14.5.1 Principios Fundamentales

```
┌────────────────────────────────────────────────────────────┐
│              PRINCIPIOS DEL GDPR                           │
└────────────────────────────────────────────────────────────┘

1. LICITUD, LEALTAD Y TRANSPARENCIA
   └─ Base legal para procesamiento

2. LIMITACIÓN DE LA FINALIDAD
   └─ Datos solo para propósito específico

3. MINIMIZACIÓN DE DATOS
   └─ Solo datos necesarios

4. EXACTITUD
   └─ Datos actualizados y correctos

5. LIMITACIÓN DEL PLAZO DE CONSERVACIÓN
   └─ Retener solo el tiempo necesario

6. INTEGRIDAD Y CONFIDENCIALIDAD
   └─ Seguridad apropiada

7. RESPONSABILIDAD PROACTIVA
   └─ Demostrar cumplimiento
```

#### 14.5.2 Derechos de los Titulares

```python
# Implementación de derechos GDPR

class GDPRCompliance:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def derecho_acceso(self, usuario_id):
        """
        Art. 15 GDPR: Derecho de acceso
        Exportar todos los datos del usuario
        """
        datos = {
            'informacion_personal': self.db.query(
                "SELECT * FROM usuarios WHERE id = ?", usuario_id
            ),
            'pedidos': self.db.query(
                "SELECT * FROM pedidos WHERE usuario_id = ?", usuario_id
            ),
            'actividad': self.db.query(
                "SELECT * FROM logs WHERE usuario_id = ?", usuario_id
            )
        }
        
        # Generar archivo JSON
        import json
        with open(f'datos_usuario_{usuario_id}.json', 'w') as f:
            json.dump(datos, f, indent=2)
        
        return datos
    
    def derecho_rectificacion(self, usuario_id, campo, nuevo_valor):
        """
        Art. 16 GDPR: Derecho de rectificación
        Corregir datos inexactos
        """
        self.db.execute(
            f"UPDATE usuarios SET {campo} = ? WHERE id = ?",
            (nuevo_valor, usuario_id)
        )
        
        # Registrar cambio para auditoría
        self.db.execute(
            "INSERT INTO auditoria (usuario_id, accion, campo, valor_anterior, valor_nuevo) VALUES (?, ?, ?, ?, ?)",
            (usuario_id, 'rectificacion', campo, None, nuevo_valor)
        )
    
    def derecho_supresion(self, usuario_id):
        """
        Art. 17 GDPR: Derecho al olvido
        Eliminar o anonimizar datos
        """
        # Verificar si hay obligación legal de retener
        if self._tiene_obligacion_retencion(usuario_id):
            # Anonimizar en lugar de eliminar
            self._anonimizar_usuario(usuario_id)
        else:
            # Eliminar completamente
            self.db.execute("DELETE FROM usuarios WHERE id = ?", usuario_id)
            self.db.execute("DELETE FROM pedidos WHERE usuario_id = ?", usuario_id)
        
        # Registrar eliminación
        self.db.execute(
            "INSERT INTO auditoria (usuario_id, accion) VALUES (?, ?)",
            (usuario_id, 'supresion')
        )
    
    def derecho_portabilidad(self, usuario_id):
        """
        Art. 20 GDPR: Derecho a la portabilidad
        Exportar datos en formato estructurado
        """
        datos = self.derecho_acceso(usuario_id)
        
        # Convertir a CSV para portabilidad
        import csv
        with open(f'portabilidad_usuario_{usuario_id}.csv', 'w') as f:
            writer = csv.writer(f)
            # Escribir datos en formato portable
            for tabla, registros in datos.items():
                writer.writerow([tabla])
                if registros:
                    writer.writerow(registros[0].keys())
                    for registro in registros:
                        writer.writerow(registro.values())
    
    def derecho_oposicion(self, usuario_id, finalidad):
        """
        Art. 21 GDPR: Derecho de oposición
        Oponerse a ciertos procesamientos (ej: marketing)
        """
        self.db.execute(
            "UPDATE consentimientos SET activo = FALSE WHERE usuario_id = ? AND finalidad = ?",
            (usuario_id, finalidad)
        )
    
    def _anonimizar_usuario(self, usuario_id):
        """Anonimizar datos personales"""
        self.db.execute("""
            UPDATE usuarios 
            SET 
                nombre = 'Usuario Anonimizado',
                email = CONCAT('anonimo_', id, '@deleted.com'),
                telefono = NULL,
                direccion = NULL,
                fecha_nacimiento = NULL
            WHERE id = ?
        """, usuario_id)
    
    def _tiene_obligacion_retencion(self, usuario_id):
        """Verificar si hay obligación legal de retener datos"""
        # Ejemplo: retener datos fiscales por 5 años
        resultado = self.db.query("""
            SELECT COUNT(*) as count 
            FROM pedidos 
            WHERE usuario_id = ? 
            AND fecha > DATE_SUB(NOW(), INTERVAL 5 YEAR)
        """, usuario_id)
        
        return resultado[0]['count'] > 0
```

### 14.6 Auditoría y Certificación

#### 14.6.1 Proceso de Auditoría ISO 27001

```
┌────────────────────────────────────────────────────────────┐
│         PROCESO DE CERTIFICACIÓN ISO 27001                 │
└────────────────────────────────────────────────────────────┘

FASE 1: PREPARACIÓN (3-6 meses)
├─ Gap analysis
├─ Implementar controles
├─ Documentar políticas
├─ Capacitar personal
└─ Auditoría interna

FASE 2: AUDITORÍA ETAPA 1 (1-2 días)
├─ Revisión documental
├─ Verificar alcance
├─ Evaluar preparación
└─ Identificar no conformidades mayores

FASE 3: CORRECCIONES (1-2 meses)
└─ Corregir no conformidades

FASE 4: AUDITORÍA ETAPA 2 (2-5 días)
├─ Auditoría en sitio
├─ Entrevistas
├─ Revisión de evidencias
└─ Verificar efectividad de controles

FASE 5: CERTIFICACIÓN
├─ Emisión de certificado
├─ Válido por 3 años
└─ Auditorías de vigilancia anuales

MANTENIMIENTO:
├─ Año 1: Auditoría de vigilancia
├─ Año 2: Auditoría de vigilancia
└─ Año 3: Auditoría de recertificación
```

#### 14.6.2 Checklist de Auditoría

```markdown
# CHECKLIST DE AUDITORÍA ISO 27001

## A.5.1 Políticas de Seguridad
- [ ] Política de seguridad documentada
- [ ] Aprobada por dirección
- [ ] Comunicada a empleados
- [ ] Revisada anualmente
- [ ] Evidencia: Documento firmado, emails de comunicación

## A.8.5 Autenticación Segura
- [ ] MFA implementado
- [ ] Políticas de contraseñas fuertes
- [ ] Gestión de sesiones
- [ ] Evidencia: Capturas de configuración, logs de acceso

## A.8.16 Actividades de Monitoreo
- [ ] SIEM implementado
- [ ] Logs centralizados
- [ ] Alertas configuradas
- [ ] Revisión regular de logs
- [ ] Evidencia: Dashboard de SIEM, reportes de revisión

## A.5.23 Seguridad en la Nube
- [ ] Evaluación de proveedores cloud
- [ ] Acuerdos de nivel de servicio (SLA)
- [ ] Cifrado de datos en tránsito y reposo
- [ ] Evidencia: Contratos, configuraciones de cifrado
```

### 14.7 Laboratorio: Preparación para Auditoría

```bash
# Script para recopilar evidencias de cumplimiento

#!/bin/bash

FECHA=$(date +%Y%m%d)
DIR_EVIDENCIAS="evidencias_auditoria_$FECHA"

mkdir -p $DIR_EVIDENCIAS

echo "Recopilando evidencias para auditoría ISO 27001..."

# A.8.9 Gestión de configuración
echo "1. Configuraciones de seguridad..."
cp /etc/ssh/sshd_config $DIR_EVIDENCIAS/
cp /etc/security/pwquality.conf $DIR_EVIDENCIAS/

# A.8.16 Monitoreo
echo "2. Logs de seguridad..."
cp /var/log/auth.log $DIR_EVIDENCIAS/
cp /var/log/syslog $DIR_EVIDENCIAS/

# A.8.5 Autenticación
echo "3. Políticas de contraseñas..."
grep -E "^(PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_MIN_LEN)" /etc/login.defs > $DIR_EVIDENCIAS/password_policy.txt

# A.7.4 Monitoreo físico
echo "4. Logs de acceso físico..."
# (Exportar desde sistema de control de acceso)

# A.8.23 Filtrado web
echo "5. Configuración de firewall..."
sudo iptables -L -n -v > $DIR_EVIDENCIAS/firewall_rules.txt

# Comprimir evidencias
tar -czf $DIR_EVIDENCIAS.tar.gz $DIR_EVIDENCIAS/
echo "Evidencias recopiladas en: $DIR_EVIDENCIAS.tar.gz"
```

