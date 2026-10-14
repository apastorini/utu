# -*- coding: utf-8 -*-
"""Genera los diagramas (PNG) de la clase completa con matplotlib."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(OUT, exist_ok=True)

ACCENT = "#0b7285"; DARK = "#1f3b66"; LIGHT = "#e7f5ff"; GRAY = "#495057"
GREEN = "#2b8a3e"; RED = "#c92a2a"; AMBER = "#e8590c"; PURPLE = "#5f3dc4"

def new_ax(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    return fig, ax

def box(ax, x, y, w, h, text, fc=LIGHT, ec=ACCENT, tc=DARK, fs=9, bold=False):
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                       boxstyle="round,pad=0.4,rounding_size=1.2",
                       fc=fc, ec=ec, lw=1.3)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", linespacing=1.35)

def arrow(ax, x1, y1, x2, y2, color=GRAY, lw=1.5, ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, linestyle=ls))

def title(ax, t):
    ax.text(50, 98, t, ha="center", va="top", fontsize=13.5, color=DARK, fontweight="bold")

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.18, facecolor="white")
    plt.close(fig)
    print("ok", name)

# ------------------------------------------------------------------ 1. timeline
def d_timeline():
    fig, ax = new_ax(11, 13)
    title(ax, "Línea de tiempo: de las credenciales al token atado")
    world = [
        ("1996", "Cookies de sesión (Netscape)", "estado en el servidor"),
        ("1999", "HTTP Basic/Digest (RFC 2617)", "credenciales en cada request"),
        ("2004", "WS-Security (OASIS)", "aserciones XML firmadas"),
        ("2005", "SAML 2.0 (OASIS)", "federación XML"),
        ("2006", "API keys (AWS, arquetipo)", "identificador estático"),
        ("2010", "OAuth 1.0 (RFC 5849) · borrador JWT (28 dic)", "firmar cada request"),
        ("2012", "OAuth 2.0 (RFC 6749) y bearer (RFC 6750); se abandona el tipo MAC", "un string en una cabecera"),
        ("2013", "Revocación de tokens (RFC 7009)", "cortar antes de expirar"),
        ("2014", "OpenID Connect Core 1.0 (26 feb)", "ID token: quién y cómo"),
        ("2015", "JWT (RFC 7519) · PKCE (RFC 7636) · introspección (RFC 7662)", "claims y candado del código"),
        ("2018", "Token Binding (RFC 8471-8473)", "intento sin adopción"),
        ("2020", "mTLS atado a certificado (RFC 8705) · JWT BCP (RFC 8725)", "atar el token al portador"),
        ("2021", "Perfil JWT para access tokens (RFC 9068)", "exp obligatorio"),
        ("2023", "DPoP: prueba de posesión (RFC 9449)", "firma por request"),
        ("2025", "RFC 9700 (mejores prácticas) · NIST SP 800-63-4", "sender-constrained y PKCE obligatorios"),
    ]
    x = 12; y0, y1 = 6, 93
    ax.plot([x, x], [y0, y1], color=ACCENT, lw=2.5)
    step = (y1 - y0) / (len(world) - 1)
    for i, (year, event, note) in enumerate(world):
        y = y1 - i * step
        c = Circle((x, y), 1.1, fc=ACCENT, ec="white", lw=1.0, zorder=3)
        ax.add_patch(c)
        ax.text(x - 3.2, y, year, ha="right", va="center", fontsize=10.5,
                color=DARK, fontweight="bold")
        ax.text(x + 3.0, y + 1.2, event, ha="left", va="center", fontsize=9.6, color=DARK)
        ax.text(x + 3.0, y - 1.7, note, ha="left", va="center", fontsize=8.3,
                color=GRAY, style="italic")
    save(fig, "01_timeline.png")

# ------------------------------------------------------------- 2. token family
def d_token_family():
    fig, ax = new_ax(11, 7)
    title(ax, "La familia de tokens: quién nace, dónde y para qué")
    box(ax, 12, 78, 18, 12, "Persona\n(navegador/app)", fc="#fff", bold=True)
    box(ax, 42, 86, 26, 12, "Servidor de\nautorización (IdP)", fc="#d0ebff", bold=True)
    box(ax, 80, 78, 22, 12, "API de recursos\n(Resource Server)", fc="#fff", bold=True)
    box(ax, 42, 46, 20, 11, "Cliente", fc="#fff", bold=True)

    arrow(ax, 21, 80, 29, 85, ls="--"); arrow(ax, 29, 85, 21, 80, color="#adb5bd")
    ax.text(25, 90, "1) login (front)", fontsize=8, color=GRAY, ha="center")
    arrow(ax, 21, 74, 32, 60, ls="--")
    ax.text(20, 66, "2) authorization code\n(front channel, 1 uso)", fontsize=7.6, color=GRAY)
    arrow(ax, 42, 51, 42, 80)
    ax.text(55, 66, "3) canje por canal trasero\n(client auth + PKCE)", fontsize=7.6, color=GRAY)
    arrow(ax, 42, 80, 42, 52, color=ACCENT)

    box(ax, 42, 20, 20, 10, "access token", fc="#d3f9d8", ec=GREEN, fs=8.5, bold=True)
    box(ax, 66, 20, 20, 10, "refresh token", fc="#fff3bf", ec=AMBER, fs=8.5, bold=True)
    box(ax, 18, 20, 20, 10, "ID token", fc="#e5dbff", ec=PURPLE, fs=8.5, bold=True)
    arrow(ax, 52, 20, 72, 76, color=GREEN)
    ax.text(63, 48, "4) va a la API", fontsize=7.6, color=GREEN)
    arrow(ax, 66, 15, 66, 9, color=AMBER); arrow(ax, 66, 9, 42, 9, color=AMBER); arrow(ax, 42, 9, 42, 15, color=AMBER)
    ax.text(54, 6, "5) solo al endpoint de token", fontsize=7.6, color=AMBER)
    arrow(ax, 18, 20, 14, 72, color=PURPLE)
    ax.text(6, 46, "6) a la app\n(NO a la API)", fontsize=7.6, color=PURPLE)
    save(fig, "02_token_family.png")

# ------------------------------------------------------------- 3. jwt anatomy
def d_jwt():
    fig, ax = new_ax(11, 5)
    title(ax, "Anatomía de un JWT: firmado, no sellado")
    box(ax, 18, 55, 30, 30,
        "HEADER\n\n{\n \"alg\": \"RS256\",\n \"kid\": \"k1\",\n \"typ\": \"JWT\"\n}",
        fc="#d0ebff", fs=8.2)
    box(ax, 50, 55, 30, 30,
        "PAYLOAD (claims)\n\n{\n \"iss\": \"https://idp\",\n \"aud\": \"mi-api\",\n \"sub\": \"123\",\n \"exp\": 1700000000,\n \"scope\": \"read\"\n}",
        fc="#d3f9d8", fs=8.2)
    box(ax, 82, 55, 30, 30,
        "SIGNATURE\n\nfirma con la\nclave privada\ndel emisor\n(se valida con\nla clave pública)",
        fc="#ffe3e3", ec=RED, fs=8.2)
    ax.text(18, 70, "", fontsize=1)
    ax.text(50, 18, "Base64url NO es cifrado: cualquiera lee el header y el payload.",
            ha="center", fontsize=9.5, color=RED, fontweight="bold")
    ax.text(50, 8, "El algoritmo se fija en la CONFIGURACIÓN del validador, nunca en el token (RFC 8725).",
            ha="center", fontsize=8.6, color=DARK)
    save(fig, "03_jwt_anatomy.png")

# ------------------------------------------------------------- 4. transport
def d_transport():
    fig, ax = new_ax(11, 5.4)
    title(ax, "Dónde viaja el token: cabecera, cookie o query")
    box(ax, 18, 52, 30, 55,
        "CABECERA\n(Authorization: Bearer)\n\n+ Inmune a CSRF\n+ Estándar RFC 6750\n− Hay que almacenarla\n− localStorage = XSS\n\nRecomendado",
        fc="#d3f9d8", ec=GREEN, fs=8.2)
    box(ax, 50, 52, 30, 55,
        "COOKIE\n(HttpOnly + Secure + SameSite)\n\n+ Protege de XSS (HttpOnly)\n+ Contexto navegador\n− Requiere anti-CSRF\n− No aplica a nativo/M2M",
        fc="#fff3bf", ec=AMBER, fs=8.2)
    box(ax, 82, 52, 30, 55,
        "QUERY STRING\n(?access_token=)\n\n+ (ninguno)\n\n− Queda en logs, Referer,\n  historial y CDN\n− PROHIBIDO por RFC 9700 (2025)",
        fc="#ffe3e3", ec=RED, fs=8.2)
    save(fig, "04_transport.png")

# ------------------------------------------------------------- 5. mfa timeline
def d_mfa_timeline():
    fig, ax = new_ax(11, 4.2)
    title(ax, "La MFA protege un instante; el token vive mucho más")
    ax.annotate("", xy=(96, 50), xytext=(4, 50),
                arrowprops=dict(arrowstyle="-|>", color=DARK, lw=2))
    stages = [(14, "Password"), (30, "MFA"), (48, "Emisión\ndel token"),
              (72, "Token vivo\n(minutos, días, meses)"), (90, "API")]
    for x, t in stages:
        ax.plot([x, x], [46, 54], color=DARK, lw=1.5)
        ax.text(x, 61, t, ha="center", va="bottom", fontsize=9, color=DARK, fontweight="bold")
    ax.add_patch(FancyBboxPatch((24, 30), 12, 8, boxstyle="round,pad=0.3",
                                fc="#d3f9d8", ec=GREEN, lw=1.2))
    ax.text(30, 34, "protege esto", ha="center", va="center", fontsize=7.8, color=GREEN)
    ax.annotate("", xy=(30, 30), xytext=(30, 46), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.3))
    ax.add_patch(FancyBboxPatch((56, 12), 34, 8, boxstyle="round,pad=0.3",
                                fc="#ffe3e3", ec=RED, lw=1.2))
    ax.text(73, 16, "y de acá en adelante, la MFA no cubre nada", ha="center", va="center",
            fontsize=7.8, color=RED)
    save(fig, "05_mfa_timeline.png")

# ------------------------------------------------------------- 6. person vs system
def d_person_vs_system():
    fig, ax = new_ax(11, 6)
    title(ax, "Persona vs. sistema: dos preguntas distintas")
    rows = [
        ("Qué se prueba", "Un humano ante un IdP", "Un workload pidió el token"),
        ("Segundo factor", "Passkey / OTP / push", "No aplica"),
        ("Artefacto", "Sesión + access + refresh", "Token corto / credencial efímera"),
        ("Vida típica", "Minutos a horas (access)", "Minutos, con rotación"),
        ("Fallo típico", "Fatiga MFA, AiTM, robo", "Secretos eternos en CI/repos"),
        ("Revocación", "RFC 7009 + logout", "Rotación de claves/identidad"),
    ]
    ax.text(30, 90, "PERSONA", ha="center", fontsize=11, color=DARK, fontweight="bold")
    ax.text(72, 90, "SISTEMA (máquina)", ha="center", fontsize=11, color=DARK, fontweight="bold")
    y = 82
    for r in rows:
        ax.text(6, y, r[0], ha="left", va="center", fontsize=8.6, color=GRAY, fontweight="bold")
        box(ax, 30, y, 34, 9, r[1], fc="#d0ebff", fs=8.0)
        box(ax, 72, y, 34, 9, r[2], fc="#e5dbff", ec=PURPLE, fs=8.0)
        y -= 13
    save(fig, "06_person_vs_system.png")

# ------------------------------------------------------------- 7. sender-constrained
def d_sender():
    fig, ax = new_ax(11, 5.2)
    title(ax, "Del bearer al token atado a su portador")
    box(ax, 17, 55, 28, 45,
        "BEARER (2012)\n\nQuien tiene el string,\nlo usa.\n\nRobar el token = entrar.\nNo hay prueba de quién lo\npresenta.",
        fc="#ffe3e3", ec=RED, fs=8.4)
    box(ax, 50, 55, 28, 45,
        "mTLS (RFC 8705, 2020)\n\nEl token queda atado al\ncertificado del cliente.\n\nRobar el token no alcanza:\nfalta el par de claves.",
        fc="#d0ebff", fs=8.4)
    box(ax, 83, 55, 28, 45,
        "DPoP (RFC 9449, 2023)\n\nEl cliente firma cada request\ncon su clave privada.\n\njti + htm + htu evitan replay.\nNo necesita PKI.",
        fc="#d3f9d8", ec=GREEN, fs=8.4)
    arrow(ax, 31, 55, 36, 55); arrow(ax, 64, 55, 69, 55)
    ax.text(50, 12, "RFC 9700 (2025): los tokens sender-constrained se recomiendan donde sea posible.",
            ha="center", fontsize=8.6, color=DARK, fontstyle="italic")
    save(fig, "07_sender_constrained.png")

# ------------------------------------------------------------- 8. oauth flows
def d_flows():
    fig, ax = new_ax(11, 5.6)
    title(ax, "Flujos de OAuth 2.0: cuáles usar y cuáles se retiraron")
    box(ax, 27, 74, 44, 16, "AUTHORIZATION CODE + PKCE (RFC 6749 / 7636)\nUsuarios con navegador. El preferido; PKCE obligatorio (RFC 9700).",
        fc="#d3f9d8", ec=GREEN, fs=8.2)
    box(ax, 27, 54, 44, 14, "CLIENT CREDENTIALS (RFC 6749 §4.4)\nServicio a servicio: no hay usuario. Identidad de workload.",
        fc="#d0ebff", fs=8.2)
    box(ax, 27, 35, 44, 13, "REFRESH TOKEN (RFC 6749 §6)\nRenovar access sin volver a autenticar. Rotación + detección de reuso.",
        fc="#fff3bf", ec=AMBER, fs=8.2)
    box(ax, 27, 17, 44, 13, "DEVICE CODE (RFC 8628)\nDispositivos sin navegador (TV, IoT).",
        fc="#e5dbff", ec=PURPLE, fs=8.2)
    box(ax, 80, 62, 30, 40, "RETIRADOS\n\nIMPLICIT GRANT\n(no hay código; token en la URL)\n\nPASSWORD GRANT\n(la app maneja la password)\n\nBearer en query string\n\nRFC 9700 (2025)",
        fc="#ffe3e3", ec=RED, fs=8.2)
    save(fig, "08_oauth_flows.png")

# ------------------------------------------------------------- 9. protocol stack
def d_stack():
    fig, ax = new_ax(11, 5.6)
    title(ax, "Los protocolos involucrados, por capas")
    capas = [
        (86, "Aplicación de identidad", "OAuth 2.0 · OpenID Connect · SAML 2.0 · WS-Federation · SCIM", "#d0ebff"),
        (68, "Token y criptografía (JOSE)", "JWT · JWS · JWE · JWK · JWA · XML-DSig", "#d3f9d8"),
        (50, "Prueba de posesión / transporte seguro", "bearer · MAC (abandonado) · mTLS (8705) · DPoP (9449) · Token Binding", "#fff3bf"),
        (32, "Transporte", "TLS/SSL · mTLS · HTTPS · WebAuthn/FIDO2 · OTP (HOTP/TOTP)", "#e5dbff"),
        (14, "Red", "HTTP/1.1 · HTTP/2 · HTTP/3 (QUIC) · TCP · DNS · gRPC · WebSocket", "#ffe3e3"),
    ]
    for y, t, sub, fc in capas:
        box(ax, 50, y, 88, 14, f"{t}\n{sub}", fc=fc, fs=8.4)
    save(fig, "09_protocol_stack.png")

# ------------------------------------------------------------- 10. lifecycle
def d_lifecycle():
    fig, ax = new_ax(8.5, 8.5)
    title(ax, "Ciclo de vida de un token")
    import math
    steps = ["Emitir", "Transportar", "Usar", "Expirar", "Rotar", "Revocar"]
    R = 33
    ax.add_patch(Circle((50, 50), R, fc="none", ec="#ced4da", lw=1.5, ls="--"))
    for i, s in enumerate(steps):
        ang = math.radians(90 - i * (360 / len(steps)))
        x = 50 + R * math.cos(ang); y = 50 + R * math.sin(ang)
        box(ax, x, y, 22, 11, s, fc="#d0ebff", fs=9.5, bold=True)
    for i in range(len(steps)):
        a1 = math.radians(90 - i * (360 / len(steps)) - 360 / len(steps) * 0.28)
        a2 = math.radians(90 - i * (360 / len(steps)) - 360 / len(steps) * 0.72)
        arrow(ax, 50 + R * math.cos(a1), 50 + R * math.sin(a1),
              50 + 1 + R * math.cos(a2), 50 + R * math.sin(a2), color=ACCENT)
    ax.text(50, 50, "VIDA\nCORTA", ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
    save(fig, "10_lifecycle.png")

# ------------------------------------------------------------- 11. owasp
def d_owasp():
    fig, ax = new_ax(11, 6.4)
    title(ax, "OWASP API Security Top 10 (2023)")
    items = [
        ("API1", "BOLA", "autorización a nivel de objeto"),
        ("API2", "Broken Authentication", "autenticación rota"),
        ("API3", "BOPLA", "mass assignment / propiedades"),
        ("API4", "Unrestricted Resource Consumption", "sin límites de consumo"),
        ("API5", "BFLA", "autorización a nivel de función"),
        ("API6", "Sensitive Business Flows", "abuso de lógica de negocio"),
        ("API7", "SSRF", "peticiones del servidor a URLs"),
        ("API8", "Security Misconfiguration", "configuración insegura"),
        ("API9", "Improper Inventory", "versiones y shadow APIs"),
        ("API10", "Unsafe Consumption", "confiar en terceros sin validar"),
    ]
    y = 86
    for code, name, desc in items:
        fc = "#ffe3e3" if code == "API1" else "#e7f5ff"
        ec = RED if code == "API1" else ACCENT
        box(ax, 26, y, 40, 8.4, f"{code} · {name}", fc=fc, ec=ec, fs=8.4, bold=True)
        ax.text(48, y, desc, ha="left", va="center", fontsize=8.0, color=GRAY)
        y -= 9.6
    save(fig, "11_owasp_top10.png")

# ------------------------------------------------------------- 12. reference arch
def d_arch():
    fig, ax = new_ax(11, 6)
    title(ax, "Arquitectura de referencia de una API segura")
    box(ax, 10, 72, 16, 12, "Cliente\n(SPA/móvil/M2M)", fc="#fff", bold=True)
    box(ax, 34, 72, 18, 12, "API Gateway\n(authz, cuotas, WAF)", fc="#d0ebff", bold=True)
    box(ax, 62, 72, 20, 12, "API / Servicios\n(validación, authz objeto)", fc="#d3f9d8", bold=True)
    box(ax, 88, 72, 16, 12, "Datos\n(RBAC/ABAC)", fc="#fff", bold=True)
    box(ax, 34, 40, 20, 12, "IdP / OAuth 2.0 · OIDC\n(emisión, MFA, claims)", fc="#e5dbff", ec=PURPLE, bold=True)
    box(ax, 64, 40, 20, 12, "Secret Manager\n+ KMS/HSM", fc="#fff3bf", ec=AMBER, bold=True)
    box(ax, 16, 40, 20, 12, "Observabilidad / SIEM\n(logs, trazas, alertas)", fc="#ffe3e3", ec=RED, bold=True)
    arrow(ax, 18, 72, 25, 72); arrow(ax, 43, 72, 52, 72); arrow(ax, 72, 72, 80, 72)
    arrow(ax, 34, 66, 34, 46, ls="--"); ax.text(30, 56, "tokens", fontsize=7.6, color=PURPLE, ha="right")
    arrow(ax, 62, 66, 64, 46, ls="--")
    arrow(ax, 26, 46, 26, 66, ls="--", color=RED)
    ax.text(50, 20, "Cada capa agrega un control. El token es solo una de ellas.",
            ha="center", fontsize=9.2, color=DARK, fontstyle="italic")
    save(fig, "12_reference_arch.png")

# ------------------------------------------------------------- 13. circles
def d_circles():
    fig, ax = new_ax(9.5, 9.5)
    title(ax, "Alrededor del token hay un sistema entero")
    import math
    ax.add_patch(Circle((50, 47), 9, fc="#0b7285", ec="white", lw=1.5))
    ax.text(50, 47, "TOKEN", ha="center", va="center", fontsize=9.5, color="white", fontweight="bold")
    items = ["API Gateway", "IAM", "MFA", "Rate Limiting", "WAF", "API Keys",
             "OAuth/OIDC", "JWT", "Scopes", "RBAC/ABAC", "Secret Manager",
             "mTLS/DPoP", "Observabilidad", "Zero Trust", "Authz de objeto"]
    R = 33
    for i, it in enumerate(items):
        ang = math.radians(90 - i * (360 / len(items)))
        x = 50 + R * math.cos(ang); y = 47 + R * math.sin(ang)
        ax.add_patch(Circle((x, y), 7.4, fc="#e7f5ff", ec="#0b7285", lw=1.1))
        ax.text(x, y, it, ha="center", va="center", fontsize=6.9, color="#1f3b66")
        ax.plot([50 + 10 * math.cos(ang), x - 7.4 * math.cos(ang)],
                [47 + 10 * math.sin(ang), y - 7.4 * math.sin(ang)],
                color="#ced4da", lw=0.8, zorder=0)
    save(fig, "13_circles.png")

for fn in [d_timeline, d_token_family, d_jwt, d_transport, d_mfa_timeline,
           d_person_vs_system, d_sender, d_flows, d_stack, d_lifecycle,
           d_owasp, d_arch, d_circles]:
    fn()
print("Diagramas generados en", OUT)
