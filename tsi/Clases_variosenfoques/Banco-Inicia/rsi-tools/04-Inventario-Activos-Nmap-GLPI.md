# TOOLS-04 · Inventario de Activos: Nmap/Zenmap + GLPI

> **Función del MCU 5.0:** Identificar (ID.AM): inventariar hardware, software, datos y sistemas, y mantener el registro actualizado.
> **ISO/IEC 27001:** Anexo A.5.9 (inventario de activos) y A.5.10 (propiedad de la información).
> **BCU:** La guía EMG y el art. 492 exigen conocer los activos tecnológicos como base del análisis de riesgo.
> **URCDP:** Ley 18.331 art. 10 (medidas adecuadas) y el Documento de Seguridad exigen listar los sistemas que tratan datos personales.
> **Nivel del curso:** 🟡 Practicar

---

## 1. Qué es y para qué sirve

- **Nmap** es un escáner de red open source: descubre **qué dispositivos hay conectados** a una red y **qué puertos/servicios** tienen abiertos. Es la herramienta número 1 para armar el inventario de activos desde la red.
- **Zenmap** es la interfaz gráfica de Nmap.
- **GLPI** es una plataforma de gestión de activos de TI e incidencias (open source): el "libro mayor" donde se registra cada activo con su responsable, ubicación y estado.

> ⚠️ **Regla de oro:** Nmap solo se ejecuta sobre las redes del propio Banco (o del laboratorio), con autorización del área de TI. Nunca contra redes de terceros sin permiso (es ilegal en Uruguay sin autorización).

---

## 2. Instalación de Nmap + Zenmap

### En Windows (host de trabajo)

```powershell
winget install Insecure.Nmap
```

O descargá el instalador desde https://nmap.org/download.html (Windows binaries) y ejecutalo con las opciones por defecto. Zenmap se instala junto.

### En Linux (VM del laboratorio)

```bash
sudo apt update
sudo apt install -y nmap zenmap
```

---

## 3. Primer escaneo de la red de laboratorio

Primero, averiguá tu propia IP y subred:

```bash
ip a           # Linux: buscar la IP (ej. 192.168.1.100/24)
ipconfig       # Windows
```

Luego escaneá la subred completa:

```bash
nmap -sn 192.168.1.0/24        # descubrimiento de hosts (ping scan)
nmap -O 192.168.1.0/24         # descubrimiento + detección de sistema operativo
nmap -sV 192.168.1.10          # servicios y versiones de un host puntual
nmap -sS 192.168.1.10          # escaneo de puertos TCP (stealth)
```

Guardá la salida en un archivo de evidencia:

```bash
nmap -sV -oA inventario-red-lab 192.168.1.0/24
```

Esto genera `inventario-red-lab.nmap`, `.gnmap` y `.xml`. El `.xml` es el que se puede importar o documentar.

---

## 4. Instalación de GLPI (en la VM del laboratorio)

GLPI necesita un servidor web + base de datos. La forma más fácil es usar un servidor LAMP:

```bash
sudo apt update
sudo apt install -y apache2 mariadb-server php php-mysql php-ldap php-curl php-gd php-intl php-xml php-bcmath php-mbstring php-zip
```

Descargar e instalar GLPI (versión estable desde https://glpi-project.org/downloads/):

```bash
cd /tmp
wget https://github.com/glpi-project/glpi/releases/download/10.0.x/glpi-10.0.x.tgz
sudo tar -xzf glpi-10.0.x.tgz -C /var/www/html/
sudo chown -R www-data:www-data /var/www/html/glpi
```

Crear la base de datos:

```bash
sudo mysql -e "CREATE DATABASE glpi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER 'glpi'@'localhost' IDENTIFIED BY 'ClaveLaboratorio2026!';"
sudo mysql -e "GRANT ALL PRIVILEGES ON glpi.* TO 'glpi'@'localhost'; FLUSH PRIVILEGES;"
```

Completar la instalación:

1. Abrí `http://<IP-de-la-VM>/glpi` en el navegador.
2. Elegí idioma español → **Continuar** → instalación por defecto.
3. Base de datos: servidor `localhost`, usuario `glpi`, clave que definiste, base `glpi`.
4. Al final te da el usuario inicial: **glpi** / **glpi**. Cambiá las claves del usuario glpi y del técnico post-otras (te lo pide al final).

---

## 5. Primeros pasos en GLPI

1. **Configuración → General**: nombre de la entidad "Banco – Laboratorio".
2. **Activos → Computadoras**: creá un equipo manualmente (nombre, tipo, responsable).
3. **Inventario → Red**: podés vincular el escaneo de Nmap cargando los hosts descubiertos.
4. **Asistencia → Tickets**: el flujo de incidencias (útil también para RS).

> **Sugerencia:** exportá el inventario Nmap (.xml) y, con una planilla, cargá en GLPI los activos más importantes. La automatización total (agente de inventario GLPI) se cubre en el nivel Dominar.

---

## 6. Cómo volcarlo a las plantillas del kit

- **ID-01 (Inventario de Activos)**: los resultados de Nmap + GLPI son la fuente de datos para completar el inventario formal del SGSI (activo, tipo, responsable, ubicación).
- **ID-03 (Análisis de Riesgos)**: solo se puede valorar el riesgo de lo que está inventariado.
- **URCDP-01 (Documento de Seguridad)**: los sistemas que tratan datos personales salen de este inventario.

---

## 7. Lista de verificación del módulo

- ☐ Nmap + Zenmap instalados.
- ☐ Primer escaneo de la red de laboratorio ejecutado (`nmap -sV -oA ...`).
- ☐ GLPI instalado en la VM (web, BD, usuario glpi).
- ☐ Entidad del laboratorio creada y al menos un activo registrado.
- ☐ Salida de Nmap guardada como evidencia.
- ☐ Resultados volcados al ID-01 (borrador).

---

**Documentos relacionados:** ID-01, ID-02, ID-03, URCDP-01, BCU-04
