# Clase 43: Presentacion de Proyectos - Red Team + Cierre

**Numero de clase:** 32  
**Duracion:** 2 horas  
**Curso:** Taller de Ciberseguridad Orientada al Desarrollo

---

## Objetivos de Aprendizaje

- Presentar ataques Red Team sobre las aplicaciones desarrolladas
- Demostrar ataques y defensas en escenarios reales
- Reflexionar sobre las lecciones aprendidas durante el curso
- Identificar recursos para continuar la formacion en seguridad
- Recibir certificados simbolicos y cerrar el curso

---

## Contenido Detallado

### 1. Estructura de la Sesion (10 min)

**Organizacion del tiempo (2 horas):**

| Actividad | Duracion |
|-----------|----------|
| Introduccion y recordatorio | 10 min |
| Presentaciones Red Team (5 grupos x 8 min) | 40 min |
| Preguntas por presentacion | 15 min |
| Lecciones aprendidas y discusion final | 20 min |
| Recursos para seguir aprendiendo | 15 min |
| Entrega de certificados y feedback | 20 min |

### 2. Criterios de Evaluacion - Ataque Red Team (10 min)

| Criterio | Peso | Excelente (4) | Bueno (3) | Suficiente (2) | Insuficiente (1) |
|----------|------|---------------|-----------|----------------|-------------------|
| Identificacion de vulnerabilidades | 25% | 3+ vulnerabilidades reales encontradas | 2 vulnerabilidades | 1 vulnerabilidad | Ninguna |
| Tecnica de ataque | 25% | Ataque ejecutado con exito, con herramientas reales | Ataque parcialmente exitoso | Solo teorico | Sin ataque |
| Defensa propuesta | 25% | Defensa completa con codigo correctivo | Defensa teorica correcta | Defensa incompleta | Sin defensa |
| Presentacion | 25% | Clara, demostracion en vivo, responde preguntas | Buena exposicion | Presentacion basica | Sin preparacion |

### 3. Guia para la Presentacion Red Team (5 min)

**Estructura recomendada (8 min):**

1. **Introduccion (1 min):** Que aplicacion atacaron, objetivo del ataque
2. **Reconocimiento (1 min):** Que informacion recolectaron (puertos, tecnologias)
3. **Vulnerabilidad encontrada (2 min):** Cual es, como se explota, impacto
4. **Demostracion del ataque (2 min):** Ejecutar el ataque en vivo o grabado
5. **Defensa implementada (1.5 min):** Codigo correctivo, que cambio, por que funciona
6. **Conclusion (30 seg):** Leccion aprendida, recomendacion

**Ejemplos de ataques para presentar:**
- Fuerza bruta a login (y como rate limiting lo bloquea)
- Manipulacion de JWT (y como la firma HMAC lo detecta)
- IDOR en endpoints (y como la verificacion de ownership lo previene)
- SQL injection (y como SQLAlchemy ORM lo evita)
- XSS en campos de texto (y como el escaping lo neutraliza)
- Path traversal (y como la normalizacion de rutas lo bloquea)

---

## Ejercicio: Escribir "Lessons Learned" de 3 Vulnerabilidades

**Enunciado:** Cada estudiante o grupo debe escribir un documento de "lessons learned" que describa 3 vulnerabilidades encontradas durante el ataque Red Team, incluyendo: descripcion, impacto, ataque, defensa implementada y reflexion personal.

**Solucion - Documento de ejemplo completo:**

```
LESSONS LEARNED - TALLER DE CIBERSECURIDAD
===========================================

Estudiante: [Nombre]
Fecha: [Fecha]

Introduccion:
Durante el ataque Red Team a la aplicacion segura desarrollada
en las clases 28-29, se identificaron y analizaron 3 vectores
de ataque. A continuacion se documentan los hallazgos, ataques
ejecutados y defensas implementadas.

--- VULNERABILIDAD 1: FUERZA BRUTA EN LOGIN ---

Descripcion:
El endpoint POST /auth/login permite multiples intentos de
autenticacion sin restriccion de velocidad inicial (antes de
agregar rate limiting).

Impacto:
Un atacante puede probar miles de combinaciones de usuario/
contrasena en minutos, comprometiendo cuentas con contrasenas
debilmente protegidas.

Ataque ejecutado:
Se utilizo un script bash con curl en un bucle for:

    for password in $(cat passwords.txt); do
      curl -s -X POST http://localhost:8000/auth/login \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"admin\",\"password\":\"$password\"}" \
        | grep -q "access_token" && echo "FOUND: $password"
    done

Resultado: Se lograron probar 1000 contrasenas en 3 minutos.

Defensa implementada:
Se agrego rate limiting con SlowAPI:

    from slowapi import Limiter
    from slowapi.util import get_remote_address

    limiter = Limiter(key_func=get_remote_address)

    @router.post("/login")
    @limiter.limit("5/minute")
    def login(credentials: UserLogin, request: Request, ...):
        ...

Codigo adicional: Se agrego bloqueo temporal de IP despues de
10 intentos fallidos en 15 minutos.

Reflexion:
El rate limiting es una defensa simple pero extremadamente
efectiva contra fuerza bruta. Combinado con bloqueo temporal
de IP, hace que atacar un solo usuario sea impracticable.
La leccion principal es que la autenticacion siempre debe
tener proteccion anti-fuerza bruta desde el primer dia.


--- VULNERABILIDAD 2: IDOR EN ENDPOINT DE ITEMS ---

Descripcion:
El endpoint GET /api/items/{item_id} inicialmente no verificaba
que el item perteneciera al usuario autenticado.

Impacto:
Un usuario malicioso podia cambiar el item_id en la URL para
acceder, modificar o eliminar items de otros usuarios.

Ataque ejecutado:
1. Login como usuario1, obtener token1
2. Crear item, obtener item_id=1
3. Login como usuario2, obtener token2
4. GET /api/items/1 con token2 (deberia estar prohibido)

    curl -H "Authorization: Bearer $TOKEN2" \
      http://localhost:8000/api/items/1

Resultado: Sin proteccion, usuario2 accedia al item de usuario1.
Con proteccion, retorna 403 Forbidden.

Defensa implementada:
Se agrego verificacion de ownership en cada endpoint:

    @router.get("/{item_id}")
    def get_item(item_id: int, current_user=Depends(get_current_user), ...):
        item = db.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404)
        if item.owner_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="No autorizado")
        return item

Reflexion:
Nunca confiar en que el usuario enviara solo IDs que le
pertenecen. Siempre verificar propiedad o permisos en el
servidor. Esta vulnerabilidad es muy comun en APIs REST
y una de las mas explotadas en la actualidad (OWASP Top 10:
Broken Access Control #1).


--- VULNERABILIDAD 3: EXPOSICION DE INFORMACION EN LOGS ---

Descripcion:
El logging inicial registraba los cuerpos completos de los
requests, incluyendo contrasenas y tokens.

Impacto:
Un atacante con acceso a los archivos de log podia obtener
credenciales de usuarios y tokens JWT validos. Ademas,
viola regulaciones como GDPR al almacenar datos personales
sin proteccion.

Ataque ejecutado:
Se accedio (simulado) al archivo app.log:

    cat app.log | grep "password"
    # Output: {"password": "MiPassword123", "username": "admin"}

Resultado: Contrasenas en texto plano en los logs.

Defensa implementada:
Se implemento un SecureLogger que redacta campos sensibles:

    class SecureLogger:
        SENSITIVE_FIELDS = ["password", "secret", "token",
                          "authorization", "credit_card"]

        def _sanitize(self, data):
            sanitized = {}
            for key, value in data.items():
                key_lower = key.lower()
                if any(f in key_lower for f in self.SENSITIVE_FIELDS):
                    sanitized[key] = "***REDACTED***"
                elif isinstance(value, dict):
                    sanitized[key] = self._sanitize(value)
                else:
                    sanitized[key] = value
            return sanitized

Reflexion:
El logging es una herramienta de debugging y auditoria, pero
puede convertirse en un riesgo de seguridad si no se filtra
la informacion sensible. La leccion: todo lo que se registra
debe considerarse publico. Si no quieres que alguien lo vea,
no lo registres.


--- CONCLUSION FINAL ---

Este ejercicio demostro que las vulnerabilidades mas comunes
(OWASP Top 10) siguen siendo las mas efectivas. Sin embargo,
defensas simples y bien implementadas (parametrized queries,
rate limiting, verificacion de ownership, logging seguro)
pueden detener la mayoria de los ataques.

La seguridad no es un producto, es un proceso continuo que
debe integrarse en cada etapa del desarrollo.

Recursos para seguir aprendiendo:
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- PortSwigger Web Security Academy: https://portswigger.net/web-security
```

---

## Recursos para Seguir Aprendiendo (15 min)

### OWASP (Open Web Application Security Project)
- **OWASP Top 10:** Las 10 vulnerabilidades mas criticas en aplicaciones web
- **OWASP ASVS (Application Security Verification Standard):** Framework de verificacion con 3 niveles de seguridad
- **OWASP Cheat Sheets:** Guias rapidas por tema (autenticacion, autorizacion, cifrado)
- **OWASP Juice Shop:** Aplicacion vulnerable para practicar hacking etico
- **Web:** https://owasp.org/

### SANS Institute
- **SANS Cyber Aces Online:** Cursos gratuitos de introduccion
- **SANS Holiday Hack Challenge:** Evento anual gratuito de hacking
- **Web:** https://www.sans.org/

### Certificaciones
- **CSSLP (Certified Secure Software Lifecycle Professional):** Certificacion de (ISC)2 enfocada en desarrollo seguro
- **CEH (Certified Ethical Hacker):** Certificacion de hacking etico de EC-Council
- **OSCP (Offensive Security Certified Professional):** Certificacion practica de pentesting de Offensive Security
- **CompTIA Security+:** Certificacion de entrada en seguridad
- **AWS Security Specialty:** Especialidad en seguridad en la nube AWS

### Plataformas de practica
- **HackTheBox:** Maquinas vulnerables para practicar pentesting
- **TryHackMe:** Plataforma educativa con salas guiadas
- **PortSwigger Web Security Academy:** Labs gratuitos de seguridad web
- **PentesterLab:** Ejercicios progresivos de seguridad

### Herramientas recomendadas (post-curso)
- **Burp Suite Professional:** Proxy de interceptacion (version commercial)
- **Metasploit Framework:** Framework de explotacion
- **BloodHound:** Analisis de relaciones en Active Directory
- **Wireshark:** Analisis de trafico de red
- **Ghidra:** Reverse engineering de codigo

### Libros recomendados
- "The Web Application Hacker's Handbook" - Stuttard & Pinto
- "OWASP Testing Guide" - OWASP Foundation
- "Hacking: The Art of Exploitation" - Jon Erickson
- "Security Engineering" - Ross Anderson
- "The Tangled Web" - Michal Zalewski

---

## Entrega de Certificados Simbolicos (10 min)

**Modelo de certificado:**

```
=============================================
           TALLER DE CIBERSEGURIDAD
          ORIENTADA AL DESARROLLO
=============================================

       Certificado de Participacion

  Por medio del presente, se certifica que:

              [NOMBRE DEL ESTUDIANTE]

  Ha completado satisfactoriamente el taller
  "Ciberseguridad Orientada al Desarrollo"
  con una duracion de 32 horas (8 semanas).

  Temas cubiertos:
  - Fundamentos de seguridad en desarrollo
  - SAST, SCA, DAST en pipelines CI/CD
  - Seguridad en contenedores e IaC
  - Secure Code Review
  - Desarrollo de API REST segura
  - Pruebas de penetracion y hacking etico

  Fecha: [Fecha de finalizacion]

  _________________________________
  Profesor del Taller

=============================================
```

---

## Encuesta de Feedback del Curso (10 min)

**Modelo de encuesta:**

```
ENCUESTA DE FEEDBACK - TALLER DE CIBERSEGURIDAD
================================================

1. CONTENIDO DEL CURSO (1-5, donde 5 es excelente)
   - Relevancia del contenido: ___
   - Nivel de profundidad adecuado: ___
   - Calidad de los ejercicios practicos: ___
   - Utilidad de los ejemplos de codigo: ___

2. METODOLOGIA
   - Claridad de las explicaciones: ___
   - Ritmo de las clases (1=lento, 5=rapido): ___
   - Balance teoria/practica: ___
   - Calidad del material (archivos markdown): ___

3. TEMAS ESPECIFICOS
   - Clases 1-4 (Fundamentos): ___
   - Clases 5-8 (OWASP Top 10): ___
   - Clases 9-12 (Criptografia): ___
   - Clases 13-16 (Autenticacion): ___
   - Clases 17-20 (SAST/SCA): ___
   - Clases 21-24 (DAST/Contenedores): ___
   - Clases 25-28 (CI/CD + App segura): ___
   - Clases 29-32 (App segura + Proyectos): ___

4. PREGUNTAS ABIERTAS
   - Que fue lo que mas te gusto del curso?
     _________________________________
   - Que mejorarias?
     _________________________________
   - Que tema te gustaria profundizar?
     _________________________________
   - Recomendarias este curso a un colega? (SI/NO)
   - Comentarios adicionales:
     _________________________________
```

---

## Discusion Final: El Futuro de la Seguridad en Desarrollo (10 min)

**Temas de discusion:**

1. **Shift Left:** La seguridad se mueve cada vez mas a etapas tempranas del desarrollo
2. **AI/ML en seguridad:** Herramientas como CodeQL, Semgrep y GitHub Copilot (con cuidado)
3. **Supply Chain Security:** La importancia de firmar artefactos (SLSA, Sigstore)
4. **Zero Trust:** "Never trust, always verify" aplicado a APIs y microservicios
5. **DevSecOps cultura:** La seguridad no es solo del equipo de security, es de todos
6. **IA generativa:** Nuevos riesgos (prompt injection, modelos adversarios) y oportunidades

**Mensaje final para los estudiantes:**

"La seguridad no es un destino, es un viaje. Cada dia aparecen nuevas vulnerabilidades, nuevos vectores de ataque, nuevas defensas. Lo que aprendieron en este curso es la base: los principios fundamentales no cambian. Validar entrada, controlar acceso, cifrar datos, auditar acciones. Apliquen estos principios siempre, en cada linea de codigo que escriban. Y nunca dejen de aprender."

---

## Preguntas y Respuestas

**1. Que certificaciones de seguridad recomiendan para empezar?**

CompTIA Security+ para fundamentos, luego CSSLP si te enfocas en desarrollo seguro, o CEH/OSCP si te interesa el hacking etico. Para cloud, AWS Security Specialty o Azure Security Engineer.

**2. Donde puedo practicar hacking etico legalmente?**

Plataformas como HackTheBox, TryHackMe, PortSwigger Web Security Academy, OWASP Juice Shop. Todas son legales y tienen entornos controlados. Nunca practiques en sistemas sin autorizacion explicita.

**3. Que es OWASP y por que es importante?**

OWASP (Open Web Application Security Project) es una comunidad sin fines de lucro dedicada a mejorar la seguridad del software. Publican el OWASP Top 10 (vulnerabilidades mas comunes), ASVS (estandar de verificacion), Cheat Sheets, y herramientas como ZAP. Es la referencia principal en seguridad web.

**4. Como mantenerse actualizado en ciberseguridad?**

Seguir blogs como Krebs on Security, PortSwigger Research, SANS Internet Storm Center. Leer los boletines de CVE. Participar en comunidades como OWASP local chapters. Asistir a conferencias como BlackHat, DEF CON, OWASP Global AppSec.

**5. Que es Shift Left y por que es importante?**

Shift Left es mover las pruebas de seguridad a etapas tempranas del desarrollo (izquierda en el timeline). En lugar de probar seguridad al final (cuando es caro corregir), se integra desde el diseno y codificacion. Reduce costos, acelera entregas y mejora la calidad.

**6. Que es SLSA y por que es relevante?**

SLSA (Supply-chain Levels for Software Artifacts) es un framework para asegurar la cadena de suministro de software. Define niveles de confianza desde build documentado hasta integridad total. Relevante despues de ataques como SolarWinds.

**7. Como seguir aprendiendo seguridad en desarrollo despues del curso?**

Leer OWASP Testing Guide, practicar en labs (PortSwigger, HackTheBox), contribuir a proyectos open source de seguridad, obtener certificaciones (CSSLP), y sobre todo: aplicar lo aprendido en proyectos reales.

---

## Tarea / Lectura Recomendada (Post-Curso)

- Leer: OWASP Application Security Verification Standard (ASVS) nivel 2 completo
- Practicar: Resolver los 30 labs de PortSwigger Web Security Academy
- Leer: "The Web Application Hacker's Handbook" - Stuttard & Pinto
- Implementar: Un proyecto personal aplicando DevSecOps desde el inicio
- Unirse: Al capitulo local de OWASP o comunidad de seguridad de tu ciudad
- Mantenerse al dia: Suscribirse a CVE alerts y OWASP newsletter



