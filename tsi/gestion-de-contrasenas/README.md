# Curso Completo: Gestión de Contraseñas

## Objetivo General
Capacitar a los estudiantes en la gestión segura de contraseñas, desde fundamentos teóricos hasta la implementación de soluciones empresariales con herramientas open source, incluyendo análisis de ataques, continuidad de negocio y arquitecturas híbridas.

---

## Estructura del Curso

### 📘 Módulo 1: Marco Teórico
| # | Archivo | Tema |
|---|---------|------|
| 1.1 | [Fundamentos de Seguridad](01-marco-teorico/01-fundamentos-seguridad.md) | Gestores de contraseñas, cifrado E2E, zero-knowledge, derivación de claves |
| 1.2 | [Amenazas Comunes](01-marco-teorico/02-amenazas-comunes.md) | Fuerza bruta, phishing, keyloggers, credential stuffing, rainbow tables |
| 1.3 | [Principios de Criptografía](01-marco-teorico/03-principios-cripografia.md) | AES-256, PBKDF2, Argon2id, HMAC, RSA, certificados TLS |

### 📗 Módulo 2: Herramientas
| # | Archivo | Tema |
|---|---------|------|
| 2.1 | [Comparativa de Herramientas](02-herramientas/01-comparativa-herramientas.md) | KeePass, Vaultwarden, Passbolt, Bitwarden, ProtonPass, Padloc |
| 2.2 | [Análisis por Escenarios](02-herramientas/02-analisis-escenarios.md) | PYME, personal, banco, empresa mediana |
| 2.3 | [Características Comunes](02-herramientas/03-caracteristicas-comunes.md) | Qué debe tener toda herramienta de gestión |
| 2.4 | [Gestión de API Keys](02-herramientas/04-gestion-api-keys.md) | API keys, tokens JWT, certificados SSL, HashiCorp Vault |

### 📙 Módulo 3: Actividad Práctica
| # | Archivo | Tema |
|---|---------|------|
| 3.1 | [Guía Completa Paso a Paso](03-actividad-practica/01-guia-completa-paso-a-paso.md) | Actividad completa con marco teórico y verificación |
| 3.2 | [Configuración Vaultwarden](03-actividad-practica/02-configuracion-vaultwarden.md) | Docker Compose, PostgreSQL, NGINX, alta disponibilidad |
| 3.3 | [Pruebas y Verificación](03-actividad-practica/03-pruebas-verificacion.md) | Tests de seguridad, cifrado, compartición, respaldo |
| 3.4 | [Análisis y Mejoras](03-actividad-practica/04-analisis-mejoras.md) | Evaluación crítica, fortalezas, debilidades, mejoras |

### 📕 Módulo 4: Soluciones Empresariales
| # | Archivo | Tema |
|---|---------|------|
| 4.1 | [Solución BHU](04-soluciones-empresariales/01-solucion-bhu.md) | Arquitectura completa híbrida para BHU |
| 4.2 | [Políticas de Seguridad](04-soluciones-empresariales/02-politicas-seguridad.md) | Política de contraseñas, compartición, emergencia |
| 4.3 | [Admins y Privilegiados](04-soluciones-empresariales/03-admin-privilegiados.md) | Usuarios, administradores, cuentas de servicio, API keys |
| 4.4 | [Arquitecturas Comparadas](04-soluciones-empresariales/04-arquitecturas-comparadas.md) | Opción A/B/C/D, pros/contras, recomendación para banco |
| 4.5 | [Políticas por Sistema](04-soluciones-empresariales/05-politicas-por-sistema.md) | Regex por sistema, rotación individual, generación automática |

### 📒 Módulo 5: Ataque a KeePass (Defensiva)
| # | Archivo | Tema |
|---|---------|------|
| 5.1 | [Actividad de Ataque KeePass](05-ataque-keepass/01-actividad-ataque-keepass.md) | Rainbow tables, Hashcat, John the Ripper desde Windows |
| 5.1 | [Herramientas de Ataque](05-ataque-keepass/02-herramientas-ataque.md) | Herramientas para Windows, configuración, wordlists |
| 5.3 | [Defensas y Contramedidas](05-ataque-keepass/03-defensas-contramedidas.md) | Cómo protegerse de estos ataques |

### 📓 Módulo 6: Plan de Continuidad y Recuperación
| # | Archivo | Tema |
|---|---------|------|
| 6.1 | [Arquitectura Híbrida](06-plan-continuidad/01-arquitectura-hibrida.md) | Contraseñas locales + servidor central de notificaciones |
| 6.2 | [Continuidad de Negocio](06-plan-continuidad/02-continuidad-negocio.md) | BCP: estrategias, RPO, RTO, procedimientos |
| 6.3 | [Recuperación ante Desastres](06-plan-continuidad/03-recuperacion-desastres.md) | DRP: backup, restauración, failover, escenarios |
| 6.4 | [Gestión de Emergencias](06-plan-continuidad/04-gestion-emergencias.md) | Master password olvidada, break-glass, recuperación de cuentas |
| 6.5 | [Procedimientos Offline](06-plan-continuidad/05-procedimientos-offline.md) | Teletrabajo, acceso sin servidor, sync después de reconexión |

### 📄 Plantillas
| # | Archivo | Tema |
|---|---------|------|
| P.1 | [Política de Contraseñas](plantillas/politica-contrasenas.md) | Plantilla configurable para empresa |
| P.2 | [Checklist de Seguridad](plantillas/checklist-seguridad.md) | Lista de verificación periódica |

---

## Duración Estimada del Curso
- **Módulo 1** (Teórico): 4 horas
- **Módulo 2** (Herramientas): 3 horas
- **Módulo 3** (Práctica): 6 horas
- **Módulo 4** (Empresarial): 5 horas (2h adicionales para arquitecturas y políticas)
- **Módulo 5** (Ataque KeePass): 3 horas
- **Módulo 6** (Continuidad): 5 horas (1h adicional para procedimientos offline)
- **Total**: ~26 horas

## Prerrequisitos
- Conocimientos básicos de línea de comandos
- Docker instalado (para actividades prácticas)
- Windows 10/11 (para actividades de ataque)
- Conocimientos básicos de red y seguridad

## Stack Tecnológico Utilizado
| Componente | Tecnología | Licencia |
|------------|------------|----------|
| Gestor de contraseñas | Vaultwarden | AGPL-3.0 |
| Base de datos | PostgreSQL | PostgreSQL License |
| Reverse proxy | NGINX | BSD-2 |
| Contenedores | Docker / Docker Compose | Apache 2.0 |
| Ataque a KeePass | Hashcat / John the Ripper | MIT |
| API Server (actividad híbrida) | Flask (Python) | BSD-3 |
| Cola de eventos offline | SQLite | Public Domain |
| Notificaciones | Correo SMTP / Webhook | - |

---

> **Nota**: Esta carpeta está diseñada para el curso de Seguridad Informática de la UTU/UTEC. Todos los ejemplos utilizan herramientas de código abierto y gratuitas. Las actividades de ataque son exclusivamente educativas y deben realizarse únicamente en entornos controlados.
