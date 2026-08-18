# TOOLS-06 · Contraseñas y Secretos: Bitwarden/Vaultwarden + TOTP

> **Función del MCU 5.0:** Proteger (PR.AA): gestión de identidades y control de acceso; gestión de contraseñas robustas.
> **ISO/IEC 27001:** Anexo A.5.15–A.5.18 (control de acceso, identidades, contraseñas) y A.8.24 (gestión de claves criptográficas).
> **BCU:** La guía EMG pide controles de acceso a sistemas sensibles; BCU-03 exige que la función de seguridad gestione las identidades privilegiadas.
> **URCDP:** Los accesos a bases de datos personales deben estar controlados (Documento de Seguridad).
> **Nivel del curso:** 🟡 Practicar

---

## 1. Qué es y para qué sirve

- **Bitwarden**: gestor de contraseñas open source (gratuito en su nube o autohospedado). Guarda las claves cifradas y permite compartir en organizaciones con permisos.
- **Vaultwarden**: implementación open source *self-hosted* compatible con Bitwarden: corrés tu propio servidor de contraseñas dentro del Banco (la recomendación para producción).
- **TOTP (Authenticator)**: apps de segundo factor (autenticación de dos pasos) que generan códigos de 6 dígitos: **Aegis** (Android, open source), **KeePassXC**, o el integrado de Bitwarden.

> **Regla de oro:** una contraseña por servicio, larga (≥16 caracteres), única, y segundo factor en todos los accesos privilegiados. Nada de claves escritas en post-its ni en archivos Excel.

---

## 2. Instalar Vaultwarden (en la VM del laboratorio)

Con Docker (recomendado) en la VM Ubuntu:

```bash
# Instalar Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker

# Crear carpeta de datos
sudo mkdir -p /opt/vaultwarden/data
```

Crear `docker-compose.yml`:

```bash
sudo bash -c 'cat > /opt/vaultwarden/docker-compose.yml <<EOF
services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: unless-stopped
    environment:
      DOMAIN: "https://vault.lab.local"
      SIGNUPS_ALLOWED: "true"      # cambiar a false cuando esté en producción
    volumes:
      - /opt/vaultwarden/data:/data
    ports:
      - "8080:80"
EOF'
```

Levantarlo:

```bash
cd /opt/vaultwarden
sudo docker-compose up -d
```

Abrí `http://<IP-de-la-VM>:8080` → creá la cuenta administrador → **crear la organización** → deshabilitá el registro libre (`SIGNUPS_ALLOWED=false`) una vez creados los usuarios.

---

## 3. Instalar el cliente Bitwarden

En el navegador (Chrome/Firefox/Edge): extensión **Bitwarden**. En el celular: app **Bitwarden** (o **Aegis** para TOTP, open source).

Configurá el servidor:

1. En la app/extensión → **Settings → Server URL** → poné `http://<IP-de-la-VM>:8080` (o el dominio en producción).
2. Iniciá sesión con el usuario que creaste.
3. Habilita el **segundo factor** (TOTP) en tu cuenta.

---

## 4. Primeros pasos útiles para el RSI

1. **Carpetas**: creá carpetas por dominio (BCU, Agesic, URCDP, Redes, Proveedores).
2. **Items**: cargá los accesos de las herramientas del laboratorio (VMs, GLPI, Eramba, Wazuh…).
3. **Organización**: creá la org "Banco – Seguridad" y definí **colecciones** (ej. "Solo RSI", "TI Redes") con permisos.
4. **Segundo factor**: activá TOTP en cada cuenta del laboratorio y probá el inicio de sesión.
5. **Checkup**: usá el "Reporte de contraseñas reutilizadas/débiles" de Bitwarden para priorizar cambios.

> **Sugerencia para producción:** en el Banco, evaluar Vaultwarden en un servidor interno con HTTPS (certificado interno o de CA pública), respaldo de la BD (`data` encriptado) y política de contraseñas ≥16 caracteres.

---

## 5. Cómo volcarlo a las plantillas del kit

- **PR-01 (Control de Acceso)**: la política debe exigir gestor de contraseñas + segundo factor; el despliegue es la evidencia.
- **PR-03 (Seguridad de Datos)**: las claves criptográficas se gestionan con el gestor de secretos.
- **BCU-03**: la función de seguridad administra los accesos privilegiados.

---

## 6. Lista de verificación del módulo

- ☐ Vaultwarden instalado en la VM (Docker + web).
- ☐ Cuenta administrador + organización creadas.
- ☐ Registro libre deshabilitado.
- ☐ Cliente Bitwarden conectado al servidor del laboratorio.
- ☐ Segundo factor TOTP activado.
- ☐ Carpeta "Banco – Seguridad" con al menos 5 items de prueba.

---

**Documentos relacionados:** PR-01, PR-03, BCU-03, URCDP-01
