# -*- coding: utf-8 -*-
"""Ensambla la clase completa (con historia, protocolos, ejemplos y diagramas)
a partir de la clase existente + las secciones nuevas + el laboratorio.
Genera clase_completa.md
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
def p(n): return os.path.join(BASE, n)

def read(n):
    return open(p(n), encoding='utf-8').read()

def lines_of(text):
    return text.splitlines()

def block(ls):
    return "\n".join(ls).strip("\n")

def demote(text):
    """Baja un nivel todos los encabezados (# -> ##, ## -> ###, ...)."""
    out = []
    for l in lines_of(text):
        if re.match(r'^#{1,5} ', l):
            l = "#" + l
        out.append(l)
    return "\n".join(out)

cls_lines = lines_of(read("clase_tokens_seguridad.md"))

def idx_startswith(ls, prefix):
    return next(i for i, l in enumerate(ls) if l.startswith(prefix))

i_index = idx_startswith(cls_lines, "## Índice")
i0 = idx_startswith(cls_lines, "## 0. ")
i1 = idx_startswith(cls_lines, "## 1. ")
i2 = idx_startswith(cls_lines, "## 2. ")
i3 = idx_startswith(cls_lines, "## 3. ")
i4 = idx_startswith(cls_lines, "## 4. ")
i5 = idx_startswith(cls_lines, "## 5. ")
i6 = idx_startswith(cls_lines, "## 6. ")
i7 = idx_startswith(cls_lines, "## 7. ")
i8 = idx_startswith(cls_lines, "## 8. ")

doc_head = block(cls_lines[:i_index])
doc_head = doc_head.replace(
    "# Tokens de identidad, de Basic al DPoP — Clase completa",
    "# Tokens de identidad, de Basic al DPoP — Clase completa\n\n"
    "**Edición extendida: historia, protocolos, ejemplos y diagramas.**")

sec0 = block(cls_lines[i0:i1])
sec1 = block(cls_lines[i1:i2])
sec2 = block(cls_lines[i2:i3])
sec_modules = block(cls_lines[i3:i4])
sec_domains = block(cls_lines[i4:i5])
sec_lab_env = block(cls_lines[i5:i6])
sec_glossary = block(cls_lines[i6:i7])
sec_template = block(cls_lines[i7:i8])
sec_biblio = block(cls_lines[i8:])

# ---- secciones nuevas ----
sec3 = demote(read("sec3_historia.md").strip())
sec4 = demote(read("sec4_protocolos.md").strip())
sec11 = read("sec11_faq.md").strip()

# ---- laboratorio ----
lab_lines = lines_of(read("laboratorio_paso_a_paso.md"))
lab_intro = block(lab_lines[2:8])
lab_body = demote(block(lab_lines[idx_startswith(lab_lines, "## Parte A"):]))

def insert_after_heading(text, head, img):
    ls = lines_of(text)
    i = next(j for j, l in enumerate(ls) if l.startswith(head))
    ls.insert(i + 1, "")
    ls.insert(i + 2, img)
    return "\n".join(ls)

# ---- diagramas dentro de las secciones existentes ----
sec1 = insert_after_heading(sec1, "## 1. ", "![Alrededor del token hay un sistema entero: gateway, IAM, MFA y más](img/13_circles.png)")

img_modules = [
    ("## M5 —", "![Dónde viaja el token: cabecera, cookie o query](img/04_transport.png)"),
    ("## M6 —", "![Anatomía de un JWT](img/03_jwt_anatomy.png)"),
    ("## M7 —", "![Flujos de OAuth 2.0: cuáles usar y cuáles se retiraron](img/08_oauth_flows.png)"),
    ("## M8 —", "![Ciclo de vida de un token](img/10_lifecycle.png)"),
    ("## M9 —", "![Del bearer a los tokens sender-constrained](img/07_sender_constrained.png)"),
    ("## M10 —", "![OWASP API Security Top 10 (2023)](img/11_owasp_top10.png)"),
]
for head, img in img_modules:
    sec_modules = insert_after_heading(sec_modules, head, img)

sec_domains = insert_after_heading(sec_domains, "## 4. ", "![Arquitectura de referencia de una API segura](img/12_reference_arch.png)")

# ---- renumeración de secciones ----
sec_modules = sec_modules.replace("## 3. Módulos técnicos", "## 5. Módulos técnicos")
sec_domains = sec_domains.replace("## 4. La seguridad de API", "## 6. La seguridad de API")
sec_domains = re.sub(r'(?m)^### 4\.', '### 6.', sec_domains)
sec_lab_env = sec_lab_env.replace("## 5. Entorno de laboratorio seguro", "### 7.1 Entorno de laboratorio seguro")
sec_glossary = sec_glossary.replace("## 6. Glosario de atajos", "## 8. Glosario de atajos")
sec_template = sec_template.replace("## 7. Plantilla de reporte responsable", "## 9. Plantilla de reporte responsable")
sec_biblio = sec_biblio.replace("## 8. Bibliografía", "## 10. Bibliografía")

# ---- índice nuevo ----
index = """## Índice

- 0. Cómo usar esta clase y reglas de ética/legal
- 1. El mapa completo: todos los enfoques para abordar la seguridad de APIs
- 2. Taxonomía de las APIs: qué estamos protegiendo exactamente
- 3. Historia: de las credenciales al token atado
- 4. Los protocolos involucrados, de HTTP a DPoP
- 5. Módulos técnicos (M1–M11)
- 6. La seguridad de API más allá del token, dominio por dominio
- 7. Laboratorio paso a paso (con ejemplos)
- 8. Glosario de atajos
- 9. Plantilla de reporte responsable
- 10. Bibliografía
- 11. Preguntas frecuentes (FAQ)"""

# ---- ensamblado ----
parts = [
    doc_head, index, sec0, sec1, sec2, sec3, sec4,
    sec_modules, sec_domains,
    "## 7. Laboratorio paso a paso (con ejemplos)\n\n" + lab_intro + "\n\n" + sec_lab_env + "\n\n" + lab_body,
    sec_glossary, sec_template, sec_biblio, sec11,
]
master = "\n\n".join(x.strip() for x in parts) + "\n"

open(p("clase_completa.md"), "w", encoding="utf-8").write(master)

imgs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', master)
missing = [i for i in imgs if not os.path.exists(p(i))]
print("clase_completa.md | palabras ~", round(len(master) / 5))
print("imagenes referenciadas:", len(imgs), "| faltan:", missing)
print("H1:", sum(1 for l in lines_of(master) if l.startswith("# ")))
print("H2:", sum(1 for l in lines_of(master) if l.startswith("## ")))
print("H3:", sum(1 for l in lines_of(master) if l.startswith("### ")))
