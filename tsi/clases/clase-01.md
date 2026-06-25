# Clase 1: Introduccion a la Ciberseguridad

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender la definicion y el alcance de la ciberseguridad en el contexto actual
2. Identificar y diferenciar los tipos principales de amenazas informaticas
3. Dominar la triada CIA (Confidencialidad, Integridad, Disponibilidad) y su aplicacion practica
4. Analizar escenarios reales aplicando la triada CIA

---

## Contenido Detallado

### 1. Que es Ciberseguridad?

La ciberseguridad es el conjunto de practicas, procesos y tecnologias disenadas para proteger sistemas informaticos, redes, programas y datos de ataques, danos o accesos no autorizados.

**Alcance de la ciberseguridad:**

```
+--------------------------------------------------+
|              CIBERSEGURIDAD                        |
|  +----------+  +----------+  +----------+         |
|  | Seguridad|  | Seguridad|  | Seguridad|         |
|  | de Red   |  | de Apps  |  de la Info|         |
|  +----------+  +----------+  +----------+         |
|  +----------+  +----------+  +----------+         |
|  | Seguridad|  | Seguridad|  | Continuidad|      |
|  | Operativa|  | en la    |  | del Negocio|      |
|  |          |  | Nube     |  |            |       |
|  +----------+  +----------+  +----------+         |
+--------------------------------------------------+
```

### 2. Tipos de Amenazas

#### Malware
Software malicioso disenado para infiltrarse, danar o deshabilitar sistemas.

- **Virus:** Se adjunta a archivos limpios y se propaga
- **Gusano (Worm):** Se replica automaticamente sin intervencion humana
- **Troyano:** Disfrazado de software legitimo
- **Ransomware:** Encripta datos y exige rescate
- **Spyware:** Espia la actividad del usuario
- **Rootkit:** Obtiene acceso privilegiado ocultandose

#### Phishing
Tecnica de ingenieria social donde el atacante se hace pasar por una entidad confiable para obtener informacion sensible.

```
                    FASE DE ATAQUE PHISHING
+----------+     +----------+     +----------+
| Atacante |---->| Correo   |---->| Usuario  |
| envia    |     | falso de |     | hace clic|
| email    |     | banco    |     | en link  |
+----------+     +----------+     +----------+
                                      |
                                      v
                               +----------+
                               | Pagina   |
                               | falsa que|
                               | roba     |
                               | credenc. |
                               +----------+
```

#### DoS y DDoS (Denegacion de Servicio)
Saturan un servidor con trafico para que no pueda atender peticiones legitimas.

- **DoS:** Un solo origen de ataque
- **DDoS:** Multiples origenes (botnet)

#### MITM (Man-in-the-Middle)
El atacante intercepta la comunicacion entre dos partes sin que ellas lo sepan.

```
Cliente <-----> Atacante <-----> Servidor
         "intercepta y       "reenvia
          modifica datos"     datos modificados"
```

#### Insider Threats
Amenazas provenientes de dentro de la organizacion: empleados, contratistas, proveedores.

- **Malicioso:** Robo intencional de datos
- **Negligente:** Errores no intencionales
- **Comprometido:** Cuenta robada por un externo

### 3. La Triada CIA

La triada CIA son los tres pilares fundamentales de la seguridad de la informacion.

```
                    +-----------+
                    |  CONFIDEN- |
                    |  CIABILIDAD|
                    +-----------+
                         /\
                        /  \
                       /    \
                      /      \
            +--------+        +--------+
            |INTEGRI-|        |DISPONI- |
            |  DAD   |        |BILIDAD  |
            +--------+        +--------+
```

| Pilar | Definicion | Ejemplo de Falla |
|-------|-----------|------------------|
| **Confidencialidad** | Solo quienes estan autorizados pueden acceder a la informacion | Filtracion de datos, leak de passwords |
| **Integridad** | La informacion no ha sido modificada sin autorizacion | Alteracion de registros bancarios |
| **Disponibilidad** | La informacion y los sistemas estan accesibles cuando se necesitan | Ataque DDoS que tumba un sitio web |

#### Relacion entre los pilares

- La **confidencialidad** se protege con cifrado, control de acceso, autenticacion
- La **integridad** se protege con hashing, firmas digitales, checksums
- La **disponibilidad** se protege con redundancia, backups, balanceo de carga, planes de contingencia

---

## Ejercicio Practico: Identificar la Triada CIA en Escenarios Reales

### Escenario 1: Sistema Bancario en Linea

Un banco ofrece banca en linea. Los clientes pueden ver saldos, transferir dinero y pagar facturas. El sistema debe garantizar:

a) Que solo el cliente pueda ver sus propios saldos (__?__)
b) Que cuando se realiza una transferencia, el monto no se modifique en el camino (__?__)
c) Que el sistema este disponible 24/7, especialmente en fines de semana (__?__)

**Solucion:**
- a) Confidencialidad - Solo el titular autenticado accede a su informacion financiera
- b) Integridad - La transaccion no debe ser alterada por un intermediario
- c) Disponibilidad - El servicio debe estar operativo permanentemente

### Escenario 2: Sistema de Historial Medico Electronico

Un hospital digitaliza los historiales medicos de sus pacientes.

a) Solo medicos autorizados pueden leer el diagnostico (__?__)
b) Si un medico modifica una receta, debe quedar registro de la modificacion (__?__)
c) En una emergencia, el medico debe poder acceder al historial aunque el sistema principal este caido (__?__)

**Solucion:**
- a) Confidencialidad - Datos medicos son extremadamente sensibles (protegidos por HIPAA, GDPR)
- b) Integridad - Las modificaciones deben ser trazables y verificables
- c) Disponibilidad - Acceso de emergencia con respaldo

### Escenario 3: Plataforma de E-commerce

Una tienda en linea procesa pagos con tarjeta de credito.

a) Los numeros de tarjeta deben almacenarse cifrados (__?__)
b) El precio mostrado al cliente debe coincidir exactamente con el cobrado (__?__)
c) Durante el Black Friday, el sitio debe soportar 100x el trafico normal (__?__)

**Solucion:**
- a) Confidencialidad - Datos de pago deben estar cifrados (PCI DSS)
- b) Integridad - El precio no debe ser manipulado
- c) Disponibilidad - Escalabilidad para picos de demanda

---

## Preguntas y Respuestas

### Pregunta 1
**Que diferencia hay entre una amenaza y una vulnerabilidad?**

**Respuesta:** Una amenaza es cualquier cosa que puede explotar una vulnerabilidad para causar dano (ej: un hacker, un malware). Una vulnerabilidad es una debilidad en el sistema que puede ser explotada (ej: un puerto abierto, una falta de parche, una contrasena debil). La relacion es: amenaza + vulnerabilidad = riesgo.

### Pregunta 2
**Cual es la diferencia entre un virus y un gusano?**

**Respuesta:** Un virus necesita un archivo huesped para propagarse y requiere intervencion humana (ej: ejecutar un archivo adjunto). Un gusano (worm) es autonomo: se replica y propaga automaticamente a traves de la red sin necesidad de intervencion humana. Los gusanos son generalmente mas peligrosos por su capacidad de propagacion masiva.

### Pregunta 3
**Explique como funciona un ataque MITM y mencione una mitigacion.**

**Respuesta:** En un ataque MITM, el atacante se interpone entre dos partes que se comunican (ej: cliente y servidor). El atacante intercepta, lee y potencialmente modifica los mensajes antes de reenviarlos, haciendo que ambas partes crean que se comunican directamente. La mitigacion principal es usar cifrado de extremo a extremo con TLS/SSL, donde los certificados digitales verifican la identidad del servidor.

### Pregunta 4
**Un sistema de backup que falla afecta principalmente a que pilar de la triada CIA?**

**Respuesta:** Afecta principalmente a la **Disponibilidad**. Los backups son la principal salvaguarda ante perdida de datos por ransomware, desastres naturales o errores humanos. Sin backups funcionales, cuando ocurre un incidente que destruye datos primarios, el sistema no puede restaurarse, afectando directamente la disponibilidad del servicio. Tambien puede afectar a la integridad si no se pueden recuperar datos correctos.

### Pregunta 5
**Por que el phishing sigue siendo tan efectivo a pesar de las campa~nas de concientizacion?**

**Respuesta:** El phishing explota la psicologia humana (ingenieria social) en lugar de vulnerabilidades tecnicas. Sigue siendo efectivo porque: (1) los atacantes mejoran constantemente sus tecnicas (spear phishing personalizado), (2) usan urgencia y miedo para que la victima no piense racionalmente, (3) las tecnicas de suplantacion son cada vez mas sofisticadas (sitios web identicos al real), y (4) el volumen masivo de ataques hace inevitable que alguien caiga.

---

## Tarea / Lectura Recomendada

1. **Leer:** "The CIA Triad" - Articulo de la enciclopedia OWASP: https://owasp.org/www-community/security/CIAtriad
2. **Leer:** Capitulo 1 de "The Web Application Hacker's Handbook" (Stuttard & Pinto)
3. **Ver:** Video "Common Types of Cyber Attacks" de IBM Security (YouTube)
4. **Investigar:** Buscar una noticia actual de ciberseguridad, identificar que tipo de amenaza fue y que pilares de la triada CIA se vieron comprometidos
5. **Practicar:** Configurar un firewall basico en su sistema operativo y documentar las reglas aplicadas
