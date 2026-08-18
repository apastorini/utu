# Módulo 7 · El organigrama del Banco y dónde vive la seguridad

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.

> Nivel del curso: 🟢 Descubrir
> Objetivo: conocer la estructura organizacional del Banco (según su sitio oficial, PDF "SF.PLE.05 - Organigrama Banco" de abril 2026) y **ubicar los roles de seguridad** dentro de ella.

---

## 7.1. El mapa general

```
                        DIRECTORIO
                            │
                    Asesor Letrado de Directorio
                            │
                    GERENCIA GENERAL (Gerente General)
                            │
   ┌────────────┬────────────┼───────────────┬───────────────┐
   │            │            │               │               │
Área        Área         Área          Área          Div. Secretaría
Comercial  Operaciones  Administración  Riesgos       General
           y TI         Financiera
   │            │            │               │               │
Defensor    Div. TI     Div. Contaduría  Div. Seguimiento   Div. Auditoría
del Cliente│ Div. Ops   Div. Admin.      y Recuperación     Interna
Sucursales │            Gral.            de Activos
           │            Div. Finanzas    Oficial de         Div. Capital
           │            y Mercado        Cumplimiento       Humano
           │            de Capitales
                                                             Div. Planificación
                                                             Estratégica
                                                             Div. Servicios
                                                             Jurídicos Notariales
```

---

## 7.2. Detalle por Área (nombres actuales, abril 2026)

### Área Comercial
- **Gerente de Área Comercial:** Cr. Pablo Liard
  - **Gerente de División Banca Persona:** Cr. Alvaro Gandolfo
    - Jefe de Departamento Análisis de Préstamos: Sra. Marina Damiani
    - Jefe de Departamento Atención Personalizada: Sr. Alejandro Pereyra
  - **Gerente de División Canales y Apoyo Comercial:** Lic. Gustavo Bordoni
    - Jefe de Departamento Canales de Atención: Cra. Viviana Trabuco
  - **Defensor del Cliente:** Lic. Adriana Martínez
  - **Gerente 1 de Sucursal**

### Área Operaciones y TI
- **Gerente de Área Operaciones y TI:** (perfil de cargo publicado)
  - **Gerente de División Tecnología de la Información:** Lic. Bernardo Ureta
    - Jefe de Departamento Producción: Ing. Daniel Herrera
    - Jefe de Departamento Sistemas: Lic. Cristian Palo
    - Jefe de Departamento Soporte Técnico: Tec. Ariel Presa
  - **Gerente de División Operaciones:** Ec. Analía Cortizo
    - Jefe de Departamento Procesos: Cra. Ana Paletta
    - Jefe de Departamento Sistema de Pagos: Cr. Guillermo Correa
    - Jefe de Departamento Información y Apoyo Comercial
    - Jefe de Departamento Servicios Generales: Ing. Agustín Araujo

### Área Administración Financiera
- **Gerente de Área Administración Financiera:** Cra. Soledad Carreres
  - **Gerente de División Contaduría:** Cra. Ma. Eugenia Coronel
    - Jefe de Departamento Contabilidad y Tributos: Cra. Ana Karina Rodríguez
  - **Gerente de División Administración General:** Lic. Rosario Larrosa
    - Jefe de Departamento Compras y Contrataciones
  - **Gerente de División Finanzas y Mercado de Capitales:** Cr. Matías Crespo
    - Jefe de Departamento Análisis Financiero

### Área Riesgos
- **Gerente de Área Riesgos:** Ec. Laura Zunino
  - Jefe de Departamento Riesgos Financieros: Ec. Gretel Yaffe
  - **Jefe de Departamento Riesgos No Financieros:** Cra. Melissa Moraes
  - **Gerente de División Seguimiento y Recuperación de Activos:** Cra. Patricia Amodio
    - Jefe de Departamento Gestión de Garantías e Inmuebles: Sr. Pablo Lorenzo
    - Jefe de Departamento Gestión de Morosidad: Sra. Alejandra Olivera
- **Oficial de Cumplimiento:** Cra. Melissa Moraes

### Divisiones que dependen de Gerencia General
- **División Secretaría General:** Sr. Bruno Alonso
- **División Auditoría Interna:** Cr. Marcelo Jorge
- **División Capital Humano:** Sr. Pablo Castro
  - Jefe de Departamento Administración de RRHH: Sr. Bernardo Rocha
  - Jefe de Departamento Desarrollo de RRHH: Ing. Cecilia Cabrera
- **División Planificación Estratégica:** Cr. Pablo Vargha
  - Jefe de Departamento Control de Gestión: Cra. Kariné Dolabdjian
- **División Servicios Jurídicos Notariales:** Dr. Héctor Dotta
- **Asesor Letrado de Directorio**

> Fuente: https://www.bhu.com.uy/sobre-bhu/organigrama (PDF: SF.PLE.05 - Organigrama Banco, abril 2026). Verificar periódicamente porque la estructura cambia.

---

## 7.3. Mapa de la seguridad de la información sobre el organigrama

### La propuesta de gobierno (coherente con Agesic y BCU)

```
                    DIRECTORIO
                        │  aprueba política, recibe informe del RSI
            ┌───────────┴────────────┐
            │  COMITÉ DE SEGURIDAD   │  (nuevo, propuesto)
            │  DE LA INFORMACIÓN     │  integra: Gerente General (o quien
            │                        │  designe), RSI, DPD, Jefe Riesgos No
            │                        │  Financieros, Gerente Div. TI, Oficial
            │                        │  de Cumplimiento, Auditoría (invitado)
            └───────────┬────────────┘
                        │
              RSI (Responsable de Seguridad de la Información)
              → recomendado: dentro del Departamento de Riesgos
                No Financieros (Área Riesgos) → segunda línea, independiente de TI
                        │
   ┌────────────┬───────┴────────┬─────────────┐
   │            │                │             │
Div. TI    DPD / DPO        Oficial de     Div. Auditoría
(1ª línea:  (protección de   Cumplimiento   Interna (3ª línea:
implementa)  datos)          (PLA/FT)        evalúa todo)
```

### Dónde encaja cada rol (cuadro)

| Rol de seguridad | Ubicación sugerida en el organigrama | Justificación |
|---|---|---|
| **RSI** | Área Riesgos → Depto. Riesgos No Financieros | Segunda línea, independiente de TI, reporta al Comité y Directorio |
| **Delegado de Protección de Datos (DPD)** | Puede vivir en Área Riesgos o Servicios Jurídicos Notariales, con independencia funcional | Cumplimiento de datos personales (URCDP) |
| **Oficial de Cumplimiento** | Área Riesgos (ya existe: Cra. Melissa Moraes) | Coordina con RSI en normativa BCU |
| **Gestión de TI / Operaciones** | Área Operaciones y TI (División TI: Producción, Sistemas, Soporte) | Primera línea: implementa los controles |
| **Seguridad física** | Depto. Servicios Generales + Operaciones | Perímetros, sucursales, centros de cómputo |
| **Auditoría Interna** | División Auditoría Interna (Cr. Marcelo Jorge) | Tercera línea: evalúa el SGSI |
| **Recursos humanos / capacitación** | División Capital Humano | Concientización, acuerdos de confidencialidad, investigaciones |
| **Compras / contratos** | Depto. Compras y Contrataciones | Cláusulas de seguridad con proveedores |
| **Planificación** | División Planificación Estratégica | Presupuesto y objetivos de seguridad |

---

## 7.4. ¿Por qué el RSI en Riesgos No Financieros y no en TI?

- El BCU y Agesic piden **independencia** entre quien implementa (TI) y quien controla (seguridad).
- En Riesgos No Financieros, el RSI ya convive con riesgo operacional y continuidad (mismos procesos).
- El **Jefe de Riesgos No Financieros** (Cra. Melissa Moraes) es el par natural del RSI; el RSI puede ser una **función dedicada dentro de ese departamento** o una unidad propia bajo el Área de Riesgos.

---

## 7.5. Ejercicio guiado

1. Abrí el PDF de organigrama del Banco (link en README) y verificá si la estructura cambió.
2. Identificá: ¿quién es el Gerente de Área Riesgos? ¿El Jefe de Riesgos No Financieros?
3. Marcá en el organigrama dónde propondrías: (a) RSI, (b) DPD, (c) Comité de Seguridad.
4. ¿Qué dependencias necesitan coordinación permanente con el RSI?

---

**Siguiente paso:** definí el proyecto en `00-PLANIFICACION/00-Planificacion-SGSI.md`.
