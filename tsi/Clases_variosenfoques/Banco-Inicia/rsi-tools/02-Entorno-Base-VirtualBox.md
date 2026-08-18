# TOOLS-02 · Entorno Base: VirtualBox + Máquinas Virtuales

> **Función del MCU 5.0:** Proveer un entorno aislado para practicar los controles de PR y DE sin riesgo para la red del Banco.
> **ISO/IEC 27001:** Respalda el control de entornos de desarrollo/prueba separados de producción (A.8.31) y la validación de cambios.
> **BCU:** La guía EMG valora que los cambios se prueben en laboratorio antes de producción (RNRCSF art. 492).
> **URCDP:** Permite probar medidas técnicas sin exponer datos personales.
> **Nivel del curso:** 🟡 Practicar

---

## 1. Qué es y para qué sirve

**VirtualBox** es un hipervisor open source: un programa que te permite correr **máquinas virtuales (VMs)** dentro de tu PC. Una VM es una computadora completa (sistema operativo + programas) que corre "como un archivo" dentro de tu equipo real (el *host*).

Para el RSI es la herramienta más importante del curso porque:

- Podés **probar herramientas** (Wazuh, OpenVAS, TheHive…) sin ensuciar tu PC de trabajo.
- Podés **destruir y recrear** el entorno cuantas veces quieras (instantáneas/snapshots).
- Podés **aislar** las herramientas de ataque (nmap, Metasploit) del resto.

> **Regla de oro:** las VMs del laboratorio **nunca** se conectan a la red de producción del Banco, y **nunca** se cargan con datos reales de clientes.

---

## 2. Instalación de VirtualBox (Windows)

1. Descargá VirtualBox desde el sitio oficial: https://www.virtualbox.org → **Downloads**.
2. Elegí "Windows hosts" y ejecutá el instalador.
3. Aceptá los términos, dejá las opciones por defecto y presioná **Next** hasta **Install**.
4. Durante la instalación te puede advertir que se reinstalará el driver de red; aceptá (es necesario).
5. Al final, abrí VirtualBox.

> ⚠️ **Windows te avisará** sobre el driver de red ("Would you like to install this device software?"). Aceptá siempre (sí / Install).

### 2.1 Verificar la virtualización (VT-x/AMD-V)

1. Presioná `Ctrl+Shift+Esc` → pestaña **Rendimiento** → **CPU**.
2. Verificá que "Virtualización" diga **Habilitada**.
3. Si está deshabilitada, hay que activarla en la BIOS/UEFI (opción "Intel VT-x" o "SVM Mode"). Reiniciá, entrá a la BIOS (F2/Del/Esc) y activala.

---

## 3. Descargar las imágenes de sistema operativo

Necesitás los ISO de los SO que vas a usar en las VMs:

| ISO | Dónde descargar | Para qué |
|---|---|---|
| **Ubuntu Server 22.04/24.04 LTS** | https://ubuntu.com/download/server | Servidores del laboratorio (Wazuh, OpenVAS, TheHive, etc.) |
| **Ubuntu Desktop 22.04/24.04 LTS** | https://ubuntu.com/download/desktop | Clientes Linux de prueba |
| **Windows 10/11** | Descarga oficial de Microsoft (media creation tool) | Clientes Windows de prueba |

---

## 4. Crear tu primera VM (Ubuntu Server)

1. Abrí VirtualBox → **Nueva**.
2. Nombre: `lab-srv-01`. **Carpeta**: dejá la de VMs. Tipo: **Linux**, Versión: **Ubuntu (64-bit)**.
3. **Memoria**: 2048 MB (2 GB) mínimo; si tu PC tiene 16 GB, poné 4096 MB.
4. **Disco duro**: "Crear un disco duro virtual ahora" → VDI → **Dinámicamente asignado** → 25 GB.
5. Terminá y seleccioná la VM → **Configuración**:
   - **Sistema → Procesador**: 2 CPUs.
   - **Almacenamiento**: en "Controlador: IDE", elegí el CD vacío → icono de disco → **Elegir archivo de disco óptico virtual** → el ISO de Ubuntu Server.
   - **Red**: "Adaptador puente" si querés que la VM tenga IP de tu red local de laboratorio, o "Red interna" para aislarla. Para empezar: **Red NAT** (por defecto).
6. **Iniciar** → sigue el instalador de Ubuntu (idioma, teclado, disco completo, usuario `rsi` con contraseña `Laboratorio2026!` como ejemplo).

> **Sugerencia:** configurá el servidor con **OpenSSH server** durante la instalación (te va a preguntar). Así podés conectarte por terminal.

---

## 5. Instantáneas (snapshots): tu seguro de vida

Antes de instalar cualquier herramienta del curso, creá una instantánea:

1. Con la VM apagada, seleccionala → menú **Máquina → Tomar instantánea**.
2. Ponedle nombre: `base-limpia-ubuntu` y una descripción.
3. Si algo se rompe: **Máquina → Restaurar instantánea**.

Esta práctica te permite probar libremente y volver a un estado conocido.

---

## 6. Comandos básicos que vas a usar en las VMs

Todos los módulos siguientes asumen que sabés entrar a la VM por consola o por SSH:

```bash
ssh rsi@<IP-de-la-VM>          # conectarse por SSH
sudo apt update                # actualizar lista de paquetes
sudo apt upgrade -y            # actualizar el sistema
sudo apt install -y <paquete>  # instalar un paquete
```

---

## 7. Cómo volcarlo a las plantillas del kit

- **PR-04 (Seguridad Física)**: el laboratorio es un "entorno aislado"; documentá en PR-04 que los entornos de prueba están separados.
- **PR-06 (Gestión de vulnerabilidades)**: los parches del laboratorio se prueban antes de producción.
- **ID-01 (Inventario de activos)**: registrá las VMs como activos del entorno de pruebas.

---

## 8. Lista de verificación del módulo

- ☐ VirtualBox instalado desde el sitio oficial.
- ☐ Virtualización habilitada en BIOS.
- ☐ ISO de Ubuntu Server descargado.
- ☐ VM `lab-srv-01` creada e instalada.
- ☐ Conectado por SSH a la VM.
- ☐ Instantánea `base-limpia-ubuntu` creada.

---

**Documentos relacionados:** ID-01, PR-04, PR-06, BCU-04
