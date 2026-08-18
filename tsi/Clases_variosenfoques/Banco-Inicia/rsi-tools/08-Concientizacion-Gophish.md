# TOOLS-08 · Concientización: Gophish (Simulacros de Phishing)

> **Función del MCU 5.0:** Proteger (PR.AT): concientización y entrenamiento del personal; Gobernar (GV.RM) al reducir el riesgo del factor humano.
> **ISO/IEC 27001:** Anexo A.5.32 (concienciación, educación y capacitación en seguridad).
> **BCU:** La guía EMG incluye el programa de concientización como control esperado.
> **URCDP:** El error humano es la principal causa de filtración de datos personales; el programa de concientización es una medida de seguridad (art. 10).
> **Nivel del curso:** 🟡 Practicar

---

## 1. Qué es y para qué sirve

**Gophish** es una plataforma open source de **simulacros de phishing**: te permite enviar correos de prueba (clonados o personalizados) a direcciones que cargás, y medir **cuántas personas hicieron clic o entregaron credenciales**.

Sirve para:

- Medir la **línea de base** de vulnerabilidad al phishing del Banco.
- Entrenar al personal de forma realista y sin riesgo real.
- Documentar en **PR-02** que el programa de concientización existe y tiene métricas.

> ⚠️ **Importante:** los simulacros se hacen con **autorización de la dirección y del área legal**, sobre **direcciones de correo del propio Banco**, con un mensaje claramente de prueba (o aprobado) y con política de comunicación posterior. Nunca sobre terceros.

---

## 2. Instalar Gophish (en la VM del laboratorio)

Gophish es un binario único que no necesita base de datos:

```bash
# Descargar la última versión desde https://github.com/gophish/gophish/releases
cd /opt
sudo wget https://github.com/gophish/gophish/releases/download/v0.12.1/gophish-v0.12.1-linux-64bit.zip
sudo apt install -y unzip
sudo unzip gophish-v0.12.1-linux-64bit.zip -d /opt/gophish
cd /opt/gophish
sudo chmod +x gophish
sudo ./gophish
```

En la salida verás la **clave del panel de administración** y la URL (por defecto `https://<IP>:3333`). Accedé con `admin` y esa clave. Cambiala en **Settings**.

---

## 3. Primeros pasos en Gophish

### 3.1 Configurar el perfil de envío (Email Sending Profile)

1. **Sending Profiles → New Profile**.
2. Nombre: `Simulacro Laboratorio`.
3. **SMTP**: usá el servidor SMTP del entorno de pruebas (o un servicio de prueba). En el laboratorio podés usar el de un buzón de prueba.
4. From: `capacitacion.seguridad@banco-laboratorio.uy` (dirección ficticia de prueba).

### 3.2 Crear la lista de destinatarios (Users & Groups)

1. **Users & Groups → New Group**.
2. Cargá 5–10 direcciones **de prueba** (por ejemplo, cuentas de prueba del equipo) con nombre y apellido.

### 3.3 Crear una plantilla de correo (Email Templates)

1. **Email Templates → New Template**.
2. Usá "Import" para subir el HTML de un correo tipo (o editá uno de los que vienen por defecto).
3. Incluí variables `{{.FirstName}}`, `{{.URL}}`, etc.

### 3.4 Crear la página de captura (Landing Page)

1. **Landing Pages → New Page**.
2. Elegí una página tipo login de prueba y activá "Capture Submitted Data" y "Capture Passwords" (para el laboratorio; en producción, según política).

### 3.5 Lanzar la campaña

1. **Campaigns → New Campaign**.
2. Nombre: `Simulacro-01`. Plantilla, página y grupo.
3. **URL**: la de la VM (`http://<IP>:80` o el puerto que uses).
4. **Launch**. Al terminar, en **Campaign Results** vas a ver: enviados, abiertos, clics, credenciales capturadas.

---

## 4. Medir y documentar los resultados

Exportá los resultados (CSV) y calculá la métrica principal:

**Tasa de clics = (clics / enviados) × 100**

| Resultado | Qué significa | Acción |
|---|---|---|
| < 5% de clics | Baja vulnerabilidad | Mantener y medir periódicamente |
| 5–20% de clics | Media | Reforzar con charlas y otro simulacro |
| > 20% de clics | Alta | Programa urgente de concientización + revisar controles técnicos (anti-phishing) |

> Los datos se vuelcan a **PR-02** junto con el plan de formación (charlas, material, periodicidad).

---

## 5. Cómo volcarlo a las plantillas del kit

- **PR-02 (Programa de Concientización)**: el plan, la frecuencia y los resultados de los simulacros.
- **ID-03 (Análisis de Riesgos)**: la tasa de clics es evidencia del riesgo de "phishing" (amenaza) y de la exposición (vulnerabilidad).
- **URCDP-01**: el programa de concientización es una medida de seguridad documentable.

---

## 6. Lista de verificación del módulo

- ☐ Gophish instalado y panel accesible.
- ☐ Perfil de envío creado (SMTP de prueba).
- ☐ Grupo con destinatarios de prueba.
- ☐ Plantilla de correo y página de captura configuradas.
- ☐ Campaña `Simulacro-01` lanzada y resultados revisados.
- ☐ Resultados exportados a CSV.
- ☐ Resultados volcados a PR-02 (borrador).

---

**Documentos relacionados:** PR-02, ID-03, URCDP-01
