"""
Decide qué diagramas SVG van en cada clase y en qué punto.

Regla: cada diagrama se inserta UNA vez por clase, en el punto donde se
introduce el concepto. Se busca un ancla textual en el markdown (un encabezado
o una frase clave); si no se encuentra, se cae al inicio de la parte de
teoría correspondiente.

Se usa el contexto (el bloque de texto alrededor del ancla) para no poner
un gráfico de TCP en una clase de subnetting.
"""
import re
import pathlib

import diagramas as DIAG

# diagrama -> (numero_de_clases_a_aparentar, [(anclas, capitulo)])
#   las anclas se prueban en orden; la primera que exista gana
REGLAS = {
    "pila-capas": (
        [2, 3],
        [("# Clase 2", "# Clase 2"),
         ("## 2.2", "# Clase 2"), ("modelo OSI", "# Clase 2")],
    ),
    "encapsulacion": (
        [3],
        [("## 1.1", "# Clase 3"), ("Encapsulación", "# Clase 3")],
    ),
    "subnet-and": (
        [26, 27, 28, 29],
        [("máscara", "# Clase 26"), ("Aplicar la máscara", "# Clase 26"),
         ("Método", "# Clase 27"), ("Paso 1", "# Clase 27")],
    ),
    "topologia-empresa": (
        [28, 29],
        [("Plan de numeración", "# Clase 28"), ("empresa", "# Clase 29"),
         ("Ejercicio", "# Clase 29")],
    ),
    "topologia-nat": (
        [30, 31],
        [("NAT", "# Clase 31"), ("Tabla de enrutamiento", "# Clase 30"),
         ("ARP", "# Clase 30")],
    ),
    "nat-tabla": (
        [31],
        [("tabla NAT", "# Clase 31"), ("Traducción de puerto", "# Clase 31"),
         ("PAT", "# Clase 31")],
    ),
    "sec-arp": (
        [30],
        [("ARP Request", "# Clase 30"), ("ARP Reply", "# Clase 30"),
         ("Secuencia ARP", "# Clase 30"), ("## 1.", "# Clase 30")],
    ),
    "sec-dns": (
        [11, 12],
        [("iterativ", "# Clase 11"), ("Resolución", "# Clase 12"),
         ("## 1.", "# Clase 11")],
    ),
    "sec-handshake": (
        [18],
        [("three-way", "# Clase 18"), ("Three-way", "# Clase 18"),
         ("establecer la conexión", "# Clase 18"), ("## 1.", "# Clase 18")],
    ),
    "cabecera-tcp": (
        [17],
        [("formato de la cabecera", "# Clase 17"), ("campo por campo", "# Clase 17"),
         ("## 1.1", "# Clase 17")],
    ),
    "cabecera-ipv4": (
        [26],
        [("formato del datagrama", "# Clase 26"), ("cabecera", "# Clase 26"),
         ("## 1.1", "# Clase 26")],
    ),
    "cabecera-ipv6": (
        [36],
        [("Cabecera IPv6", "# Clase 36"), ("40 bytes", "# Clase 36"),
         ("## 1.1", "# Clase 36")],
    ),
    "ipv6-modelos": (
        [36],
        [("modelos de comunicación", "# Clase 36"), ("anycast", "# Clase 36"),
         ("tipos de dirección", "# Clase 36")],
    ),
    "grafico-cwnd": (
        [20, 21],
        [("slow start", "# Clase 21"), ("los cuatro algoritmos", "# Clase 21"),
         ("Evolución", "# Clase 21"), ("control de congestión", "# Clase 20")],
    ),
    "pila-http": (
        [8, 9],
        [("modelo cliente/servidor", "# Clase 8"), ("persistente", "# Clase 8"),
         ("## 1.1", "# Clase 8")],
    ),
    "dijkstra": (
        [33],
        [("Dijkstra", "# Clase 33"), ("link-state", "# Clase 33"),
         ("## 1.", "# Clase 33")],
    ),
    "crc-polinomio": (
        [39],
        [("división polinómica", "# Clase 39"), ("CRC", "# Clase 39"),
         ("## 1.", "# Clase 39")],
    ),
    "grafico-aloha": (
        [41],
        [("ALOHA", "# Clase 41"), ("acceso al medio", "# Clase 41"),
         ("## 1.1", "# Clase 41")],
    ),
    "csma-cd": (
        [41],
        [("CSMA/CD", "# Clase 41"), ("backoff", "# Clase 41")],
    ),
    "csma-ca": (
        [43],
        [("CSMA/CA", "# Clase 43"), ("estación oculta", "# Clase 43"),
         ("## 1.1", "# Clase 43")],
    ),
    "cubetas": (
        [45],
        [("leaky bucket", "# Clase 45"), ("token bucket", "# Clase 45"),
         ("Leaky", "# Clase 45")],
    ),
    "mpls-hop": (
        [45],
        [("MPLS", "# Clase 45"), ("etiqueta", "# Clase 45")],
    ),
    "voip-buffer": (
        [44],
        [("jitter", "# Clase 44"), ("buffer", "# Clase 44"), ("## 1.1", "# Clase 44")],
    ),
    "modelo-snmp": (
        [46],
        [("agente", "# Clase 46"), ("gestor", "# Clase 46"), ("SNMP", "# Clase 46")],
    ),
    "los-3-servicios": (
        [47],
        [("confidencialidad", "# Clase 47"), ("integridad", "# Clase 47"),
         ("## 1.1", "# Clase 47")],
    ),
    "handshake-tls": (
        [47, 48],
        [("TLS", "# Clase 48"), ("SSL", "# Clase 48"), ("handshake", "# Clase 48")],
    ),
    "tuneles": (
        [31, 48],
        [("tunneling", "# Clase 48"), ("túnel", "# Clase 48"), ("VPN", "# Clase 48")],
    ),
    "indice-modulos": (
        [7, 15, 23, 37, 48],
        [("Repaso", "# Clase 7"), ("Simulacro", "# Clase 7"), ("mapa mental", "# Clase 7")],
    ),
}


def num_clase(md: str) -> int | None:
    m = re.match(r"#\s+Clase\s+(\d+)", md)
    return int(m.group(1)) if m else None


def figuras_para(md: str) -> list[tuple[str, str]]:
    """Devuelve [(nombre_diagrama, texto_ancla)] para esta clase."""
    n = num_clase(md)
    if n is None:
        return []
    lineas = md.splitlines()
    usados = set()
    salida = []
    for nombre, (clases, anclas) in REGLAS.items():
        if n not in clases:
            continue
        elegido = None
        for ancla, _clase_obj in anclas:
            for i, l in enumerate(lineas):
                if ancla in l:
                    elegido = (nombre, i)
                    break
            if elegido:
                break
        if elegido:
            salida.append(elegido)
            usados.add(nombre)
    return salida


def insertar(md: str, figura_nombre: str, linea_ancla: int) -> str:
    """Inserta la figura DESPUES del bloque de codigo que empieza en linea_ancla."""
    lineas = md.splitlines()
    i = linea_ancla
    # avanzar hasta despues del primer bloque de codigo (para no romper el ASCII)
    dentro = False
    while i < len(lineas):
        s = lineas[i].strip()
        if s.startswith("```"):
            dentro = not dentro
        elif dentro and s.startswith("#"):
            dentro = False      # un encabezado corta el bloque
        i += 1
        if not dentro and i > linea_ancla and lineas[i - 1].strip() == "":
            break
    # saltar lineas en blanco
    while i < len(lineas) and not lineas[i].strip():
        i += 1
    svg = DIAG.DIAGRAMAS[figura_nombre]()
    bloque = [svg, ""]
    return "\n".join(lineas[:i] + bloque + lineas[i:])
