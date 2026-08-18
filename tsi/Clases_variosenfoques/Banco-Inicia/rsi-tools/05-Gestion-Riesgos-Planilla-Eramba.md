# TOOLS-05 · Gestión de Riesgos: Planilla Agesic + Eramba/OpenRisk

> **Función del MCU 5.0:** Identificar (ID.RA): metodología y evaluación de riesgos; Gobernar (GV.RM): tratamiento de riesgos.
> **ISO/IEC 27001:** Cláusula 6.1 (riesgos y oportunidades) y Anexo A.5.5 (contacto con autoridades) / A.5.7 (inteligencia de amenazas).
> **BCU:** La guía EMG exige un marco de gestión de riesgos (BCU-02) y evidencia del análisis (BCU-03).
> **URCDP:** Ley 18.331 art. 10 exige medidas "proporcionales al riesgo"; la evaluación de impacto (URCDP-05) parte del análisis de riesgos.
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

---

## 1. Qué es y para qué sirve

- **Planilla de Agesic** ("Implantación SGSI – Inventario de activos y Evaluación de riesgos .xlsx"): la forma más rápida de arrancar el análisis de riesgos sin instalar nada. Es la que el kit ID-03 referencia.
- **Eramba** (o **OpenRisk**): aplicaciones web open source de gestión de riesgos: registro de activos, amenazas, vulnerabilidades, riesgos con impacto/probabilidad y plan de tratamiento. Sirven cuando el volumen supera la planilla.

> **Regla de oro:** primero se hace el análisis con la planilla (rápido, para entender la metodología); cuando hay +50 riesgos, se pasa a Eramba/OpenRisk.

---

## 2. Cargar la planilla de Agesic

1. Descargá la planilla xlsx desde el sitio de Agesic (ver README sección 7: "Guías sobre Marco de Ciberseguridad").
2. Abrila con **LibreOffice Calc** (open source) o Excel.
3. Revisá las pestañas típicas: **Activos**, **Amenazas**, **Vulnerabilidades**, **Riesgos** (con escalas de probabilidad e impacto).
4. Cargá 3 activos de prueba (ej. "Sistema Core", "Base de datos de clientes", "Red de sucursales") siguiendo la metodología de ID-02.

> Esta planilla es la base de **ID-03_Analisis-Riesgos** del kit.

---

## 3. Instalar Eramba (en la VM del laboratorio)

Eramba requiere PHP + MySQL. Con la VM de Ubuntu Server del TOOLS-02:

```bash
sudo apt update
sudo apt install -y apache2 mariadb-server php php-mysql php-gd php-xml php-mbstring php-zip php-curl php-json git unzip
```

Descargar Eramba (Community) desde https://eramba.org (solicitá la Community Edition o usá el repositorio):

```bash
cd /var/www/html
sudo git clone https://github.com/eramba/eramba_community.git eramba
sudo chown -R www-data:www-data eramba
```

Crear la base de datos:

```bash
sudo mysql -e "CREATE DATABASE eramba CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER 'eramba'@'localhost' IDENTIFIED BY 'ClaveLaboratorio2026!';"
sudo mysql -e "GRANT ALL PRIVILEGES ON eramba.* TO 'eramba'@'localhost'; FLUSH PRIVILEGES;"
```

Configurar Apache:

```bash
sudo bash -c 'echo "<VirtualHost *:80>
    DocumentRoot /var/www/html/eramba
    <Directory /var/www/html/eramba>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>" > /etc/apache2/sites-available/eramba.conf'
sudo a2enmod rewrite
sudo a2ensite eramba
sudo systemctl restart apache2
```

Completá la instalación desde el navegador: `http://<IP-de-la-VM>/eramba` → asistente (idioma, base de datos, usuario admin).

---

## 4. Primeros pasos en Eramba

1. **Settings → Users**: creá usuarios (ej. RSI, oficial de seguridad).
2. **Risk Management → Assets**: registrá los activos del inventario.
3. **Risk Management → Threats/Vulnerabilities**: cargá amenazas (malware, phishing, error humano, corte eléctrico) y vulnerabilidades.
4. **Risk Management → Risks**: creá un riesgo asociando activo + amenaza + vulnerabilidad, asigná **probabilidad** e **impacto** según la escala, y el sistema calcula el nivel.
5. **Risks → Treatment**: definí el tratamiento (mitigar, aceptar, transferir, evitar) y enlazalo al ID-04.

---

## 5. Escalas sugeridas (alineadas a ID-02)

| Probabilidad | Impacto | Nivel |
|---|---|---|
| 1 – Muy baja | 1 – Menor | Bajo |
| 2 – Baja | 2 – Menor/Moderado | Bajo/Medio |
| 3 – Media | 3 – Moderado | Medio |
| 4 – Alta | 4 – Alto | Alto |
| 5 – Muy alta | 5 – Crítico | Crítico |

Regla de cálculo simple: **Nivel = Probabilidad × Impacto** (1–25). Umbral típico: ≥12 requiere tratamiento prioritario; ≥20 es crítico y va al Comité.

---

## 6. Cómo volcarlo a las plantillas del kit

- **ID-02 (Metodología)**: la escala y regla de cálculo del kit deben coincidir con la que configurás en Eramba.
- **ID-03 (Análisis de Riesgos)**: exportá los riesgos de Eramba (CSV) y volcalos al registro formal.
- **ID-04 (Plan de Tratamiento)**: cada riesgo con tratamiento "mitigar" tiene su control/plan asociado.
- **BCU-02 (Marco de Gestión de Riesgos)**: Eramba es la evidencia de que existe un marco funcionando.

---

## 7. Lista de verificación del módulo

- ☐ Planilla de Agesic descargada y con 3 activos de prueba cargados.
- ☐ Eramba instalado en la VM (web + BD + admin).
- ☐ Usuarios y activos registrados.
- ☐ Al menos 1 riesgo completo (activo+amenaza+vulnerabilidad+probabilidad+impacto).
- ☐ Tratamiento definido para ese riesgo.
- ☐ Exportación CSV como evidencia.

---

**Documentos relacionados:** ID-02, ID-03, ID-04, ID-05, BCU-02, BCU-03, URCDP-05
