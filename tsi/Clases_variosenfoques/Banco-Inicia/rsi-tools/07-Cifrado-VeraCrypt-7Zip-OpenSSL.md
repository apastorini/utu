# TOOLS-07 · Cifrado: VeraCrypt, 7-Zip, OpenSSL, GnuPG

> **Función del MCU 5.0:** Proteger (PR.DS): proteger datos en reposo (discos, archivos) y en tránsito.
> **ISO/IEC 27001:** Anexo A.8.24 (gestión de claves) y A.8.25 (ciclo de vida de datos).
> **BCU:** La guía EMG pide cifrado de información sensible y de datos en medios portátiles.
> **URCDP:** Ley 18.331 art. 10 y el Decreto 64/020 exigen medidas técnicas (cifrado) para datos personales; URCDP-05 lo evalúa.
> **Nivel del curso:** 🟡 Practicar

---

## 1. Qué es y para qué sirve

El **cifrado** transforma datos legibles en ilegibles sin la clave. Es el control que protege los datos aunque el dispositivo se pierda o sea robado.

| Herramienta | Para qué | Open source |
|---|---|---|
| **VeraCrypt** | Cifrar discos enteros, particiones o "contenedores" (archivos-caja) | Sí |
| **7-Zip** (con AES-256) | Cifrar archivos/carpetas al comprimir | Sí |
| **OpenSSL** | Cifrar archivos individuales, gestionar certificados y claves | Sí |
| **GnuPG (gpg)** | Cifrar y firmar archivos/correo con clave pública/privada | Sí |

---

## 2. Instalar las herramientas

### Windows

```powershell
winget install VeraCrypt
winget install 7zip.7zip
winget install GnuPG.GnuPG
```

OpenSSL viene con Git para Windows (git-scm.com) o con el paquete `Win64 OpenSSL` de slproweb.com. Verificá:

```powershell
openssl version
gpg --version
```

### Linux (VM del laboratorio)

```bash
sudo apt update
sudo apt install -y veracrypt p7zip-full openssl gnupg
```

---

## 3. Caso 1 · Contenedor VeraCrypt (el más usado por el RSI)

1. Abrí VeraCrypt → **Create Volume** → "Create an encrypted file container".
2. Elegí "Standard VeraCrypt volume".
3. Ubicación: `C:\Seguridad\Evidencias-RSI.hc` → tamaño: 1 GB.
4. Algoritmo: **AES**, hash **SHA-512** (por defecto).
5. Clave de contraseña: generada con el gestor (TOOLS-06), ≥20 caracteres.
6. Formato de archivo: **exFAT** o **FAT** → creá el volumen.
7. Para usarlo: seleccioná una letra de unidad (ej. `R:`) → **Mount** → poné la clave.

> **Uso típico:** dentro del contenedor montado, guardá las **evidencias confidenciales** del SGSI (borradores de auditoría, listados de riesgos con nombres de personas) que no deben quedar en claro.

---

## 4. Caso 2 · Cifrar un archivo con 7-Zip

1. Clic derecho sobre el archivo → **7-Zip → Add to archive**.
2. Formato: **zip**; en **Encryption**: contraseña fuerte, marcar "**Encrypt file names**" (cifra también los nombres).
3. Aceptar. El resultado es un `.zip` con AES-256.

> Este método sirve para enviar por correo/carpeta compartida archivos con datos personales (solo con el destinatario teniendo la clave por otro canal).

---

## 5. Caso 3 · Cifrar con OpenSSL (línea de comandos)

Cifrar (AES-256-GCM, modo autenticado):

```bash
openssl enc -aes-256-gcm -salt -pbkdf2 -in informe.docx -out informe.docx.enc
```

Descifrar:

```bash
openssl enc -d -aes-256-gcm -pbkdf2 -in informe.docx.enc -out informe.docx
```

> Te pedirá una contraseña. Guardala en el gestor (TOOLS-06).

---

## 6. Caso 4 · GnuPG: cifrar para un destinatario

Generar el par de claves (una sola vez):

```bash
gpg --full-generate-key   # tipo RSA, 3072 bits, con passphrase
```

Exportar tu clave pública para compartirla:

```bash
gpg --export -a "Tu Nombre" > mi_clave_publica.asc
```

Importar la clave pública del destinatario y cifrar para él:

```bash
gpg --import clave_publica_destinatario.asc
gpg --encrypt --recipient "destinatario@banco.uy" documento.pdf
```

Descifrar lo que te envíen:

```bash
gpg --decrypt documento.pdf.gpg
```

---

## 7. Cómo volcarlo a las plantillas del kit

- **PR-03 (Seguridad de Datos)**: definir qué datos se cifran (en reposo y portátiles), con qué algoritmo y quién custodia las claves.
- **URCDP-01 (Documento de Seguridad)**: documentar que los archivos y dispositivos con datos personales están cifrados (VeraCrypt/7-Zip).
- **URCDP-05 (Evaluación de Impacto)**: el cifrado reduce el impacto en caso de pérdida de un dispositivo.

---

## 8. Lista de verificación del módulo

- ☐ VeraCrypt, 7-Zip, OpenSSL y GnuPG instalados.
- ☐ Contenedor VeraCrypt de 1 GB creado y montado.
- ☐ Archivo cifrado con 7-Zip (con cifrado de nombres).
- ☐ Archivo cifrado/descifrado con OpenSSL.
- ☐ Par de claves GnuPG generado y cifrado para un destinatario de prueba.
- ☐ Claves de los contenedores guardadas en el gestor (TOOLS-06).

---

**Documentos relacionados:** PR-03, URCDP-01, URCDP-05, BCU-03
