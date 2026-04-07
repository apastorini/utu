# Clase 26: Casos de Uso por Industria

## 📅 Duración: 4 horas (240 minutos)

---

## 🎯 Objetivos de Aprendizaje

Al finalizar esta clase, los participantes serán capaces de:

1. **Identificar oportunidades de automatización** específicas para su industria
2. **Analizar casos de éxito reales** y extraer lecciones aplicables
3. **Adaptar soluciones de otras industrias** a su contexto particular
4. **Seleccionar herramientas tecnológicas** apropiadas para cada caso de uso
5. **Diseñar soluciones prácticas** considerando restricciones de cada sector
6. **Entender compliance y regulaciones** específicas por industria

---

## 📚 Contenidos Detallados

### MÓDULO 1: Retail y E-commerce (60 minutos)

#### 1.1 Panorama del Sector Retail

El retail y e-commerce enfrentan desafíos únicos: márgenes ajustados, alta competencia, demanda estacional impredecible, y expectativas de entrega cada vez más rápidas. La IA y automatización ofrecen soluciones concretas a estos problemas.

```
┌─────────────────────────────────────────────────────────────────┐
│              DESAFÍOS DEL RETAIL MODERNO                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐    │
│   │                                                         │    │
│   │   COMPETENCIA DIGITAL                    Margen Bajo    │    │
│   │         ▲                                     ▲        │    │
│   │         │                                     │        │    │
│   │    Amazon        ─────────────────────▶    Tiendas    │    │
│   │    Mercado       Éxito = Eficiencia          Locales   │    │
│   │    Shopify                                       ▲     │    │
│   │         │                                        │     │    │
│   │         ▼                                        │        │    │
│   │   Expectativas de Cliente                        │        │    │
│   │   • Entrega en 24 horas                          │        │    │
│   │   • Precios personalizados                       │        │    │
│   │   • Experiencia omnicanal                        │        │    │
│   │                                                         │    │
│   └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│   SOLUCIÓN: Automatización inteligente + IA                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 1.2 Casos de Uso Específicos

**Caso 1: Gestión Automatizada de Inventario**

*Problema:* Un retailer de moda con 3 tiendas físicas y e-commerce maneja 5,000 SKUs. El conteo manual de inventario toma 40 horas semanales y tiene 8% de error, resultando en roturas de stock y sobre-stock.

*Solución Implementada:*
```
┌─────────────────────────────────────────────────────────────────┐
│         SISTEMA AUTOMATIZADO DE INVENTARIO                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │POS/Tienda│    │E-commerce│    │ Proveedor│    │  WMS     │  │
│  │  (POS)   │───▶│  (Shopify)│───▶│   EDI    │───▶│(Zoho/Green)│  │
│  └──────────┘    └──────────┘    └──────────┘    └────┬─────┘  │
│                                                        │        │
│                                                        ▼        │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    n8n WORKFLOW                          │  │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │  │
│   │  │Sync Inv │  │Calc Req │  │Order Sup│  │Alert Low│    │  │
│   │  │◄────────│  │◄────────│  │◄────────│  │◄────────│    │  │
│   │  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    AI INSIGHTS                           │  │
│   │  • Predicción de demanda (30 días)                      │  │
│   │  • Recomendaciones de compra                            │  │
│   │  • Detección de anomalías                               │  │
│   │  • Análisis de tendencias                               │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   RESULTADOS:                                                   │
│   ✓ Reducción de 40h a 2h semanales (95% menos trabajo)        │
│   ✓ Error reducido de 8% a 0.5%                                │
│   ✓ Rotura de stock reducida 85%                                │
│   ✓ Capital de trabajo optimizado 20%                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Caso 2: Personalización de Marketing con IA**

*Problema:* Un e-commerce envía emails promocionales genéricos. Tasa de apertura 15%, conversión 2%.

*Solución con IA:*
1. **Segmentación automática** basada en comportamiento de navegación
2. **Generación de contenido personalizado** usando GPT-4
3. **Timing óptimo de envío** predicho por modelo
4. **A/B testing automatizado** de asunto y contenido

*Herramientas:*
- n8n para orquestación
- OpenAI/GPT-4 para generación de contenido
- Brevo (antes Sendinblue) para email marketing
- Google Analytics para datos de comportamiento

*Resultados:*
- Tasa de apertura: 15% → 34%
- Tasa de conversión: 2% → 5.2%
- ROI de email marketing: +180%

**Caso 3: Chatbot de Atención al Cliente**

```
┌─────────────────────────────────────────────────────────────────┐
│         ARQUITECTURA DE CHATBOT INTELIGENTE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CLIENTE                                                       │
│      │                                                          │
│      ▼                                                          │
│   ┌─────────────────┐                                           │
│   │  WHATSAPP/      │                                           │
│   │  WEB CHAT       │                                           │
│   └────────┬────────┘                                           │
│            │                                                     │
│            ▼                                                     │
│   ┌─────────────────┐                                           │
│   │  CLASIFICACIÓN  │  ¿Es consulta simple?                     │
│   │  (Decision AI)  │                                           │
│   └────────┬────────┘                                           │
│       ┌────┴────┐                                                │
│      SÍ        NO                                                │
│       │         │                                                │
│       ▼         ▼                                                │
│   ┌────────┐ ┌──────────────────────────────────┐               │
│   │ AUTO   │ │  ESCALADO A HUMANO               │               │
│   │ RESPONSE│ │  ┌────────┐  ┌────────┐         │               │
│   │        │ │  │Ticket  │  │Notificar│         │               │
│   │ 50%    │ │  │CRM     │  │Agente   │         │               │
│   └────────┘ │  └────────┘  └────────┘         │               │
│              └──────────────────────────────────┘               │
│                            │                                     │
│                            ▼                                     │
│                   ┌─────────────────┐                           │
│                   │  HUMAN AGENT     │                           │
│                   │  (50% remaining) │                           │
│                   └─────────────────┘                           │
│                                                                  │
│   AUTO-RESPUESTAS:                                              │
│   • Estado de pedido                                           │
│   • Políticas de devolución                                    │
│   • Horarios de atención                                       │
│   • FAQ generales                                              │
│   • Rastreo de envío                                           │
│                                                                  │
│   RESULTADOS:                                                   │
│   ✓ 50% consultas resueltas sin agente                         │
│   ✓ Tiempo de respuesta: 0-2 segundos                         │
│   ✓ Disponibilidad 24/7                                        │
│   ✓ Satisfacción cliente: 4.2/5                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 1.3 ROI Típico en Retail

| Inversión | Retorno Típico | Período |
|-----------|----------------|---------|
| Automatización inventario | 300-500% | 6-12 meses |
| Marketing automation | 180-400% | 3-6 meses |
| Chatbot atención | 50-150% | 3-6 meses |
| Predictivo demanda | 200-400% | 6-12 meses |

---

### MÓDULO 2: Servicios Profesionales (60 minutos)

#### 2.1 Panorama del Sector

Los servicios profesionales incluyen: consultorías, agencias de marketing, estudios contables, bufetes de abogados, consultorios médicos, despachos de arquitectura, y más. Su principal "producto" es el tiempo de sus profesionales.

```
┌─────────────────────────────────────────────────────────────────┐
│              ECUACIÓN DEL SERVICIO PROFESIONAL                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                                                                  │
│         ┌─────────────────────────────────────────┐            │
│         │                                         │            │
│         │        💰 INGRESOS =                   │            │
│         │                                         │            │
│         │        Hrs Facturables × Tarifa        │            │
│         │                                         │            │
│         │              +                          │            │
│         │                                         │            │
│         │        Ingresos Pasivos                │            │
│         │                                         │            │
│         │              -                          │            │
│         │                                         │            │
│         │        Costos Operativos               │            │
│         │        (Personal, Tools, Overhead)     │            │
│         │                                         │            │
│         │              =                          │            │
│         │                                         │            │
│         │        MARGEN DE BENEFICIO              │            │
│         │                                         │            │
│         └─────────────────────────────────────────┘            │
│                                                                  │
│   EL DESAFÍO: Maximizar horas facturables MINIMIZANDO costos    │
│                                                                  │
│   LA SOLUCIÓN: Automatizar TODO lo no-facturable               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.2 Casos de Uso Específicos

**Caso 1: Agencia de Marketing Digital**

*Perfil:* 12 empleados, facturación $120K USD/mes

*Automatizaciones implementadas:*

```
┌─────────────────────────────────────────────────────────────────┐
│         AUTOMATIZACIONES DE AGENCIA DE MARKETING                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ADQUISICIÓN DE CLIENTES                                       │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                         │  │
│   │  Lead Website ──▶ Clasificación IA ──▶ Scoring ──▶ CRM │  │
│   │       │               │               │              │  │
│   │       ▼               ▼               ▼              │  │
│   │   Formulario    Analiza perfil   >70: Hot Lead       │  │
│   │   Web           Comportamiento  <70: Nurturing       │  │
│   │                                    <30: Low priority  │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                   │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  GENERACIÓN DE CONTENIDO (semanal)                      │  │
│   │                                                         │  │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │  │
│   │  │ Trends   │─▶│ AI Brief │─▶│ Content  │──▶ Aprobación│  │
│   │  │ Finder   │  │ Creator  │  │ Draft    │    Cliente   │  │
│   │  │(Semrush) │  │(GPT-4)   │  │(Jasper)  │              │  │
│   │  └──────────┘  └──────────┘  └──────────┘              │  │
│   │       │              │              │                   │  │
│   │       ▼              ▼              ▼                   │  │
│   │  Top 10 trends   Brief completo  Borrador listo        │  │
│   │  del sector      + keywords      para revisión          │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                   │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  REPORTING AUTOMATIZADO                                │  │
│   │                                                         │  │
│   │  Data Sources           Process              Output    │  │
│   │  ┌──────────┐  ┌──────────────┐  ┌──────────────┐      │  │
│   │  │Google Ads│  │              │  │              │      │  │
│   │  │Facebook  │─▶│ n8n Pipeline │─▶│ Report PDF   │      │  │
│   │  │Analytics │  │ + AI Summary │  │ Auto-envío   │      │  │
│   │  │CRM Data  │  │              │  │              │      │  │
│   │  └──────────┘  └──────────────┘  └──────────────┘      │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   HORAS AHORRADAS/MES:                                          │
│   • Generación de reportes: 40h                                │
│   • Creación de contenido: 60h                                  │
│   • Gestión de leads: 20h                                      │
│   • TOTAL: 120h = 3 semanas de trabajo                         │
│                                                                  │
│   INVERSIÓN: $800/mes en herramientas                          │
│   AHORRO: $9,600/mes (120h × $80/hr)                           │
│   ROI: 1,100%                                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Caso 2: Consultorio Médico**

*Perfil:* 2 médicos, 4 staff administrativo, 150 pacientes/semana

*Flujo automatizado:*

```
┌─────────────────────────────────────────────────────────────────┐
│         AUTOMATIZACIÓN DE CONSULTORIO MÉDICO                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   AGENDA INTELIGENTE                                            │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                         │  │
│   │  Solicitud    Clasificación    Slot Optimal   Confirm.   │  │
│   │  Paciente ──▶ IA ───────────▶ Sistema ──────▶ Envío    │  │
│   │               │               │               │         │  │
│   │               ▼               ▼               ▼         │  │
│   │          Nuevo        Busca por       WhatsApp         │  │
│   │          Seguimiento  preferencia      automático      │  │
│   │          Urgencia     + disponibilidad  + Recordatorio │  │
│   │          Check-up     médico           24h antes       │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                   │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  RECORDATORIOS Y SEGUIMIENTO                            │  │
│   │                                                         │  │
│   │  48h antes          2h antes         Post-consulta     │  │
│   │  ┌────────┐        ┌────────┐        ┌────────┐        │  │
│   │  │Confir- │        │Recorda-│        │Resumen │        │  │
│   │  │mación  │───────▶│torio   │───────▶│+ Next  │        │  │
│   │  │Cita    │        │        │        │Appointm│        │  │
│   │  └────────┘        └────────┘        └────────┘        │  │
│   │                                                         │  │
│   │  ¿Confirmar?      ¿Dónde está?    Seguimiento          │  │
│   │  • SÍ → Listo      • Link Google   automático          │  │
│   │  • NO → Reasign    Maps incluido   para estudios       │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                   │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  RESULTADOS MÉDICOS                                    │  │
│   │                                                         │  │
│   │  Laboratorio ──▶ Clasificación IA ──▶ Notificación    │  │
│   │  (email)         de urgencia        paciente          │  │
│   │       │               │                 │              │  │
│   │       ▼               ▼                 ▼              │  │
│   │   Resultados     Normal: Info       WhatsApp           │  │
│   │   digitales      Anormal: Flag      o email            │  │
│   │                  Urgente: Alert     según tipo         │  │
│   │                                     + clasificación   │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   RESULTADOS:                                                   │
│   ✓ Inasistencias reducidas 65% (de 12% a 4%)                  │
│   ✓ Tiempo administrativo: 25h → 8h semanales                  │
│   ✓ Satisfacción paciente: 4.5/5                              │
│   ✓ Ingresos por slot disponible: +15%                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Caso 3: Despacho Contable**

*Proceso de temporada fiscal automatizado:*

```
┌─────────────────────────────────────────────────────────────────┐
│         TEMPORADA FISCAL AUTOMATIZADA                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   FASE 1: RECOPILACIÓN (Enero - Febrero)                        │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                         │  │
│   │  Clientes                                               │  │
│   │  │                                                      │  │
│   │  ├──► Portal Documentos                                 │  │
│   │  │         │                                            │  │
│   │  │         ▼                                            │  │
│   │  ├──► Recopilación Automática                          │  │
│   │  │         │  • Bank statements (plaid)                 │  │
│   │  │         │  • Facturas (email parsing)                 │  │
│   │  │         │  • Comprobantes (upload)                    │  │
│   │  │         ▼                                            │  │
│   │  └──► Validación IA                                     │  │
│   │              │  • OCR de documentos                       │  │
│   │              │  • Extracción de datos                     │  │
│   │              │  • Clasificación automática                │  │
│   │              ▼                                            │  │
│   │         Dashboard Cliente ──▶ Revisión                  │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                   │
│   FASE 2: PROCESAMIENTO (Marzo)                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                         │  │
│   │  AI Asistente                                          │  │
│   │  │                                                      │  │
│   │  ├──► Pre-clasificación de ingresos/gastos              │  │
│   │  ├──► Detección de deducciones potenciales              │  │
│   │  ├──► Flags de revisión humana                          │  │
│   │  └──► Generación de borrador                            │  │
│   │              │                                          │  │
│   │              ▼                                          │  │
│   │         Contador revisa ──▶ Aprobación                  │  │
│   │              │                                          │  │
│   │              ▼                                          │  │
│   │         Contador firma ──▶ Envío                        │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                   │
│   RESULTADOS:                                                   │
│   ✓ Tiempo por declaración: 8h → 2.5h                          │
│   ✓ Clientes atendidos: 50 → 120                               │
│   ✓ Errores en declaraciones: -80%                             │
│   ✓ Satisfacción cliente: 4.8/5                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### MÓDULO 3: Salud y Bienestar (45 minutos)

#### 3.1 Consideraciones Especiales del Sector Salud

El sector salud tiene regulaciones estrictas (HIPAA, GDPR, NOM-035) que deben considerarse en cualquier automatización. La privacidad de datos del paciente es crítica.

```
┌─────────────────────────────────────────────────────────────────┐
│              COMPLIANCE EN SALUD                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   REGULACIONES PRINCIPALES:                                     │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    HIPAA (USA)                          │  │
│   │                                                         │  │
│   │  Protected Health Information (PHI):                    │  │
│   │  • Datos demográficos                                  │  │
│   │  • Historial médico                                    │  │
│   │  • Tratamientos                                        │  │
│   │  • Pagos de seguros                                    │  │
│   │                                                         │  │
│   │  REQUISITOS:                                           │  │
│   │  ✓ Cifrado de datos en reposo y tránsito              │  │
│   │  ✓ Control de acceso basado en roles                   │  │
│   │  ✓ Bitácora de accesos                                 │  │
│   │  ✓ Acuerdos de socio de negocio (BAA)                  │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                 NOM-035 (México)                        │  │
│   │                                                         │  │
│   │  Factores de riesgo psicosocial:                       │  │
│   │  • Identificación de estresores laborales              │  │
│   │  • Evaluación de ambiente de trabajo                   │  │
│   │  • Plan de intervención                                │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   CONSEJO: Cuando hay duda, NO automatizar datos sensibles     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 3.2 Casos de Uso en Salud

**Caso 1: Programa de Wellness Corporativo**

*Contexto:* Empresa de 500 empleados, área de RRHH busca reducir costos de salud.

*Solución:*

```
┌─────────────────────────────────────────────────────────────────┐
│         PLATAFORMA DE WELLNESS CORPORATIVO                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   MÓDULO 1: INSCRIPCIÓN Y ONBOARDING                            │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                         │  │
│   │  Nuevo empleado                                         │  │
│   │  │                                                      │  │
│   │  ├──► Cuestionario salud inicial (form)                │  │
│   │  │         │                                            │  │
│   │  │         ▼                                            │  │
│   │  ├──► Perfil de riesgo IA                               │  │
│   │  │         │  • Sedentario/Alto                         │  │
│   │  │         │  • Estrés moderado/alto                   │  │
│   │  │         │  • Factores de riesgo específicos          │  │
│   │  │         ▼                                            │  │
│   │  └──► Plan personalizado                               │  │
│   │              │  • Desafíos apropiados                   │  │
│   │              │  • Grupos recomendados                   │  │
│   │              │  • Recursos sugeridos                    │  │
│   │              ▼                                            │  │
│   │         Bienvenida + Inicio                             │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                   │
│   MÓDULO 2: SEGUIMIENTO Y ENGAGEMENT                            │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                         │  │
│   │  Integraciones wearables (opcional):                    │  │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │  │
│   │  │Fitbit    │  │Apple     │  │Garmin    │              │  │
│   │  │Health    │  │Health    │  │Connect   │              │  │
│   │  └────┬─────┘  └────┬─────┘  └────┬─────┘              │  │
│   │       └─────────────┼─────────────┘                    │  │
│   │                     ▼                                   │  │
│   │            ┌────────────────┐                           │  │
│   │            │ Agregador de  │                           │  │
│   │            │ datos anónimo  │ (SIN PHI)                │  │
│   │            └───────┬────────┘                           │  │
│   │                    ▼                                    │  │
│   │            ┌────────────────┐                           │  │
│   │            │ Gamificación   │                           │  │
│   │            │ + Desafíos     │                           │  │
│   │            │ + Competición   │                           │  │
│   │            │ + Recompensas   │                           │  │
│   │            └────────────────┘                           │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                   │
│   MÓDULO 3: REPORTING A RRHH                                   │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                         │  │
│   │  Dashboard aggregate (anónimo):                         │  │
│   │  • Participación por departamento                      │  │
│   │  • Reducción de sedentarismo                           │  │
│   │  • Satisfacción laboral                                 │  │
│   │  • Reducción de días de enfermedad                      │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   IMPACTO:                                                      │
│   ✓ Participación: 45% → 78%                                   │
│   ✓ Días de enfermedad: -12%                                    │
│   ✓ Satisfacción laboral: +15%                                  │
│   ✓ Ahorro en costos de salud: $85K/año                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### MÓDULO 4: Manufactura Ligera (45 minutos)

#### 4.1 Panorama de Manufactura

La manufactura ligera incluye: talleres de producción, artesanías, personalización de productos, empaque, y manufactura bajo pedido. Este sector se beneficia enormemente de la automatización en gestión de órdenes y producción.

```
┌─────────────────────────────────────────────────────────────────┐
│              FLUJO DE VALOR EN MANUFACTURA                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                                                                  │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│   │ DISEÑO  │───▶│ MATERIA │───▶│PRODUC-  │───▶│ CONTROL │      │
│   │         │    │ PRIMA   │    │CIÓN     │    │CALIDAD  │      │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘      │
│       │                                             │            │
│       │                                             │            │
│       ▼                                             ▼            │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │              GESTIÓN DE ÓRDENES                        │  │
│   │                                                         │  │
│   │   Cliente ──▶ Pedido ──▶ Producción ──▶ Entrega      │  │
│   │                │           │            │              │  │
│   │                ▼           ▼            ▼              │  │
│   │            Confirm.    Tracking    Notificación        │  │
│   │            + Anticipo   producción  + Seguimiento      │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   DONDE AUTOMATIZAR:                                            │
│   ✓ Captura de pedidos (todas las fuentes)                     │
│   ✓ Gestión de inventario materials                            │
│   ✓ Secuenciación de producción                                 │
│   ✓ Control de calidad                                         │
│   ✓ Comunicación con cliente                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.2 Caso de Uso: Taller de Impresión 3D Personalizada

*Perfil:* Taller de impresión 3D con 3 máquinas, produce partes personalizadas para clientes industriales y consumidores.

*Flujo automatizado:*

```
┌─────────────────────────────────────────────────────────────────┐
│         TALLER DE IMPRESIÓN 3D AUTOMATIZADO                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   RECEPCIÓN DE PEDIDOS                                          │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                         │  │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │  │
│   │  │Web      │  │Email    │  │WhatsApp │  │API      │   │  │
│   │  │Store    │  │Orders   │  │Orders   │  │Partners │   │  │
│   │  └───┬─────┘  └───┬─────┘  └───┬─────┘  └───┬─────┘   │  │
│   │      └────────────┴────────────┴────────────┘          │  │
│   │                           │                               │  │
│   │                           ▼                               │  │
│   │              ┌─────────────────────────┐                 │  │
│   │              │    n8n WORKFLOW          │                 │  │
│   │              │  • Validación archivo   │                 │  │
│   │              │  • Estimación costo     │                 │  │
│   │              │  • Tiempo producción    │                 │  │
│   │              │  • Confirmación cliente  │                 │  │
│   │              └────────────┬────────────┘                 │  │
│   │                           │                               │  │
│   │                           ▼                               │  │
│   │              ┌─────────────────────────┐                 │  │
│   │              │    ACEPTACIÓN           │                 │  │
│   │              │  Cliente confirma       │                 │  │
│   │              │  + Pago                 │                 │  │
│   │              └────────────┬────────────┘                 │  │
│   │                           │                               │  │
│   └───────────────────────────┼───────────────────────────────┘  │
│                               │                                   │
│   PLANIFICACIÓN DE PRODUCCIÓN                                    │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                         │  │
│   │              Cola de Producción                         │  │
│   │              │                                          │  │
│   │              ▼                                          │  │
│   │  ┌─────────────────────────────────────────────────┐   │  │
│   │  │              SCHEDULER INTELIGENTE              │   │  │
│   │  │                                                 │   │  │
│   │  │  Factores considerados:                         │   │  │
│   │  │  • Tiempo de impresión por pieza               │   │  │
│   │  │  • Material disponible                        │   │  │
│   │  │  • Deadlines de entrega                       │   │  │
│   │  │  • Optimización de cama (batch printing)      │   │  │
│   │  │  • Prioridad del cliente                      │   │  │
│   │  │                                                 │   │  │
│   │  └─────────────────────────────────────────────────┘   │  │
│   │                           │                               │  │
│   │         ┌─────────────────┼─────────────────┐             │  │
│   │         ▼                 ▼                 ▼             │  │
│   │  ┌────────────┐   ┌────────────┐   ┌────────────┐      │  │
│   │  │ Ender 3    │   │ Prusa MK4  │   │ Formlabs   │      │  │
│   │  │ (Protos)   │   │ (Produc)   │   │ (Precisión)│      │  │
│   │  └────────────┘   └────────────┘   └────────────┘      │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                   │
│   MONITOREO Y CONTROL                                          │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                         │  │
│   │  • Cámara por impresora (OctoPrint/Raspberry)          │  │
│   │  • Sensor de temperatura y humedad                      │  │
│   │  • Alertas de falla o desviación                       │  │
│   │  • Actualización automática de progreso                │  │
│   │  • Notificación al cliente al completar                 │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   RESULTADOS:                                                   │
│   ✓ Órdenes procesadas: 50 → 180/mes                          │
│   ✓ Tiempo administrativo: 15h → 3h/semana                    │
│   ✓ Utilización de máquinas: 45% → 78%                        │
│   ✓ Satisfacción cliente: 4.6/5                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### MÓDULO 5: Selección de Herramientas por Industria (30 minutos)

```
┌─────────────────────────────────────────────────────────────────┐
│              MATRIZ DE HERRAMIENTAS POR INDUSTRIA               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   INDUSTRIA          │ CORE TOOLS       │ AI TOOLS    │ CRM    │
│   ───────────────────┼──────────────────┼─────────────┼────────│
│   Retail/E-commerce  │ Shopify/Woo      │ GPT-4       │ HubSpot│
│                      │ n8n               │ Midjourney  │ Klaviyo│
│                      │ Stripe            │             │        │
│   ───────────────────┼──────────────────┼─────────────┼────────│
│   Servicios Prof.    │ Notion/Airtable  │ GPT-4       │ Pipedrive
│                      │ Calendly          │ Claude      │ HubSpot│
│                      │ n8n               │             │        │
│   ───────────────────┼──────────────────┼─────────────┼────────│
│   Salud/Wellness     │ Calendly          │ GPT-4       │ Acenda │
│                      │ n8n               │ (HIPAA)     │ HubSpot│
│                      │ (con HIPAA BAA)   │             │        │
│   ───────────────────┼──────────────────┼─────────────┼────────│
│   Manufactura        │ Airtable          │ GPT-4 Vision│ Zoho   │
│                      │ n8n               │             │ HubSpot│
│                      │ QuickBooks        │             │        │
│   ───────────────────┼──────────────────┼─────────────┼────────│
│   Restaurants        │ Square/Toast      │ GPT-4       │ Toast  │
│                      │ n8n               │             │ HubSpot│
│                      │ DoorDash API      │             │        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tecnologías Específicas

### Por Categoría

**Automatización Central**
| Herramienta | Mejor Para | Costo |
|-------------|-----------|-------|
| n8n | Flujos complejos, integración APIs | Freemium |
| Make (Integromat) | No-coders, UI visual | Freemium |
| Zapier | Integraciones simples | Freemium |
| Workato | Enterprise | Alto |

**CRM y Ventas**
| Herramienta | Mejor Para | Costo |
|-------------|-----------|-------|
| HubSpot | Inbound marketing | Freemium |
| Pipedrive | Ventas | Prueba gratis |
| Zoho CRM | Manufactura | Freemium |
| Salesforce | Enterprise | Alto |

**IA Generativa**
| Herramienta | Mejor Para | Costo |
|-------------|-----------|-------|
| OpenAI GPT-4 | Texto, análisis | Pay-per-use |
| Claude | Análisis,写作 | Freemium |
| Gemini | Multimodal | Freemium |
| DALL-E/Midjourney | Imágenes | Suscripción |

---

## 📝 Ejercicios Prácticos RESUELTOS

### Ejercicio 1: Análisis de Oportunidades para Retail

**Escenario:** Tienes una tienda de zapatos con 2 locations físicas y vendes por Instagram y WhatsApp. Facturación actual: $30K USD/mes.

**Paso 1: Identificar procesos manuales**

```
Procesos actuales (tiempo semanal):
• Responder mensajes de Instagram: 10h
• Gestionar inventario: 6h
• Tomar fotos y subir productos: 4h
• Enviar status de pedido: 3h
• Actualizar redes sociales: 5h
• TOTAL: 28h/semana
```

**Paso 2: Priorizar automatización**

| Proceso | Tiempo | Fácil/Difícil | Impacto | Prioridad |
|---------|--------|---------------|---------|-----------|
| Responder mensajes IG | 10h | Fácil | Alto | 1 |
| Status de pedido | 3h | Fácil | Medio | 2 |
| Actualizar inventario | 6h | Medio | Alto | 3 |
| Publicar productos | 4h | Fácil | Medio | 4 |
| Contenido redes | 5h | Medio | Bajo | 5 |

**Paso 3: Diseñar soluciones**

*Prioridad 1: Chatbot de Instagram/WhatsApp*
```
Herramientas: Manychat + ChatGPT
Flujo:
1. Cliente manda DM
2. Manychat clasifica intención
3. Si es pregunta común → respuesta automática
4. Si es venta → recopila datos y crea orden
5. Si es complejo → notifica humano
Ahorro esperado: 8h/semana
```

*Prioridad 2: Auto-actualización de inventario*
```
Herramientas: n8n + Google Sheets + WhatsApp Business API
Flujo:
1. Venta en tienda → registra en Google Sheets
2. Venta online → registra en Sheets
3. n8n sincroniza y calcula inventario
4. Alerta cuando stock bajo
5. Actualización automática en IG Shop
Ahorro esperado: 5h/semana
```

*Prioridad 3: Publicación automática de productos*
```
Herramientas: n8n + Instagram Graph API + ChatGPT
Flujo:
1. Producto nuevo en inventario
2. ChatGPT genera descripción
3. n8n crea post en IG
4. Programa publicación
5. Notifica al dueño
Ahorro esperado: 3h/semana
```

**Resultado proyectado:**
- Inversión mensual: $200 USD (herramientas)
- Ahorro de tiempo: 16h/mes = $480 USD (a $30/hr)
- ROI: 140% mensual

---

### Ejercicio 2: Caso de Consultorio Médico

**Escenario:** Consultorio dental con 3 dentists, 8 staff, atiende 200 pacientes/semana. Problema: 15% de inasistencias.

**Solución implementada:**

**Paso 1: Diagnóstico de inasistencias**
- 30% no recuerdan la cita
- 25% olvidaron que tenían compromiso
- 20% no podían comunicarse para cancelar
- 15% encontraron horario mejor
- 10% otras razones

**Paso 2: Sistema de recordatorios**

```
┌─────────────────────────────────────────┐
│         SISTEMA DE CITAS                │
├─────────────────────────────────────────┤
│                                         │
│  7 DÍAS ANTES                          │
│  ┌─────────────────────────────────┐   │
│  │ WhatsApp:                       │   │
│  │ "Hola [Nombre], tienes cita    │   │
│  │ el [fecha] a las [hora] con    │   │
│  │ Dr. [nombre]. ¿Confirmas?      │   │
│  │ Responde SÍ o NO"              │   │
│  └─────────────────────────────────┘   │
│                                         │
│  48 HORAS ANTES                        │
│  ┌─────────────────────────────────┐   │
│  │ WhatsApp:                       │   │
│  │ "Recordatorio: tu cita es      │   │
│  │ mañana [fecha] a las [hora].   │   │
│  │ ¿Necesitas reprogramar?"        │   │
│  └─────────────────────────────────┘   │
│                                         │
│  2 HORAS ANTES                        │
│  ┌─────────────────────────────────┐   │
│  │ WhatsApp:                       │   │
│  │ "Te esperamos en 2 horas.      │   │
│  │ Recordatorio: Traer [requisitos]│   │
│  │ Dirección: [link Google Maps]   │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

**Paso 3: Sistema de reagendado fácil**
```
Si responde "NO" o no confirma:
1. WhatsApp ofrece 3 alternativas
2. Si acepta, actualiza calendario automáticamente
3. Si no, agenda en lista de espera
```

**Resultados después de 3 meses:**
- Inasistencias: 15% → 5%
- Pacientes adicionales atendidos: 40/mes
- Ingresos adicionales: $8,000/mes
- Satisfacción paciente: 4.2 → 4.7/5

---

## 🔬 Actividades de Laboratorio

### Actividad 1: Mapeo de Procesos de tu Industria (60 minutos)

**Objetivo:** Documentar todos los procesos de tu negocio identificando oportunidades de automatización.

**Instrucciones:**
1. Lista todos los procesos que realizas manualmente (aunque sean pequeños)
2. Para cada proceso, estima:
   - Tiempo semanal dedicado
   - Frecuencia (diario, semanal, mensual)
   - Nivel de complejidad técnica
   - Impacto en negocio si se automatiza
3. Prioriza los top 5 procesos
4. Para cada uno, esboza una solución de automatización

**Entregable:** Documento con matriz de procesos y soluciones propuestas.

### Actividad 2: Análisis de Competitor (30 minutos)

**Objetivo:** Investigar cómo competidores o empresas similares usan automatización.

**Instrucciones:**
1. Identifica 3 empresas similares a la tuya (pueden ser de otra ciudad/país)
2. Investiga sus procesos visibles ( redes sociales, website, reviews)
3. Identifica qué parece estar automatizado
4. Documenta qué herramientas podrían estar usando
5. Analiza qué podrías implementar similar

**Entregable:** Presentación de hallazgos con recomendaciones.

### Actividad 3: Workshop de Soluciones (60 minutos)

**Objetivo:** En grupos, diseñar soluciones para casos de diferentes industrias.

**Casos a resolver (asignar uno por grupo):**
1. Restaurante de comida rápida: automatizar toma de pedidos y cocina
2. Agencia de viajes: automatizar búsqueda y propuesta de paquetes
3. Gimnasio: automatizar membresías y seguimiento de asistencia
4. Tienda de mascotas: automatizar ventas y recordatorios de vacunas

**Entregable:** Diagrama de flujo y lista de herramientas.

---

## 📚 Referencias Externas

1. **McKinsey - Automation in Retail**
   https://www.mckinsey.com/industries/retail/our-insights

2. **Shopify - E-commerce Automation Guide**
   https://www.shopify.com/blog/ecommerce-automation

3. **Salesforce - Service Cloud for Healthcare**
   https://www.salesforce.com/products/service-cloud/smb/

4. **AWS - Manufacturing Solutions**
   https://aws.amazon.com/manufacturing/

5. **HIPAA Journal - Healthcare Automation**
   https://www.hipaajournal.com/

6. **Forrester - Professional Services Automation**
   https://www.forrester.com/

---

## 📋 Resumen de Puntos Clave

### Retail y E-commerce
- ✅ Automatizar inventario es el ROI más alto
- ✅ Marketing personalizado con IA multiplica conversiones
- ✅ Chatbots manejan 50%+ de consultas sin intervención humana
- ✅ Omnicanalidad requiere integración de todos los canales

### Servicios Profesionales
- ✅ Maximizar horas facturables = maximizar ingresos
- ✅ Automatizar todo lo no-facturable (admin, reporting)
- ✅ La IA puede asistir pero no reemplazar el juicio profesional
- ✅ Documentación automática libera tiempo para clientes

### Salud y Bienestar
- ✅ Cumplimiento regulatorio (HIPAA, GDPR) es obligatorio
- ✅ Recordatorios reducen inasistencias 50%+
- ✅ Wellness programs automatizados engagement
- ✅ Nunca automatizar decisiones médicas críticas

### Manufactura
- ✅ Optimizar uso de recursos (máquinas, materiales)
- ✅ Scheduling inteligente reduce tiempos muertos
- ✅ Control de calidad automatizado detecta defectos
- ✅ Tracking de producción en tiempo real

### Selección de Herramientas
- ✅ No existe una herramienta para todo
- ✅ Integración > herramienta individual
- ✅ El costo debe calibrarse con el ROI esperado
- ✅ La simplicidad a veces vence a la功能

---

## 🔄 Próxima Clase

En la **Clase 27**, exploraremos **Escalamiento de Automatizaciones**, aprendiendo a llevar tus soluciones desde MVP hasta producción a escala empresarial, manejando múltiples clientes, sucursales o franquicias.

---

*Material preparado para el curso "IA para Líderes y Dueños de PYME (No-Code)"*
*Clase 26: Casos de Uso por Industria*
