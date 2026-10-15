# -*- coding: utf-8 -*-
"""
Diagramas para el mazo en la plantilla OWASP UY.
Fondo TRANSPARENTE para que se vea el fondo del template.
Paleta del template: navy 1B2738, azul 74AADC, amarillo OWASP FFCC01.

Salida: img_deck/*.png
"""
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img_deck")
os.makedirs(OUT, exist_ok=True)

NAVY = "#1B2738"
BLUE = "#74AADC"
YEL = "#FFCC01"
GRAY = "#6B7280"
LIGHT = "#EAF2FB"
RED = "#C0392B"
GREEN = "#2E7D32"


def fig_ax(w, h, xlim=(0, 100), ylim=(0, 100)):
    fig, ax = plt.subplots(figsize=(w, h), dpi=220)
    fig.patch.set_alpha(0.0)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("ok", name)


def box(ax, x, y, w, h, text, fc="#FFFFFF", ec=NAVY, tc=NAVY, fs=9, bold=False, lw=1.4):
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                       boxstyle="round,pad=0.3,rounding_size=1.4",
                       fc=fc, ec=ec, lw=lw, zorder=2)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", linespacing=1.3, zorder=3)


def arrow(ax, p1, p2, color=NAVY, lw=1.5, ls="-", rad=0.0):
    a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=12,
                        color=color, lw=lw, linestyle=ls, zorder=1,
                        connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a)


def dot(ax, x, y, r=0.9, c=BLUE):
    ax.add_patch(Circle((x, y), r, fc=c, ec="white", lw=0.8, zorder=3))


# --------------------------------------------------------------- 4. círculos
def d_circles():
    fig, ax = fig_ax(10.6, 8.0, xlim=(0, 132), ylim=(0, 100))
    ax.set_aspect("equal")
    cx, cy = 66, 50
    ax.add_patch(Circle((cx, cy), 13, fc=NAVY, ec="white", lw=1.5, zorder=4))
    ax.text(cx, cy, "TOKEN", ha="center", va="center", color="white",
            fontsize=11, fontweight="bold", zorder=5)

    inner = ["API Gateway", "IAM", "MFA", "Rate limiting", "WAF", "OAuth 2.0 / OIDC"]
    outer = ["JWT", "Scopes", "RBAC / ABAC", "Secret manager",
             "mTLS / DPoP", "Observabilidad", "Zero Trust", "BOLA"]

    def ring(names, r, rr, fs):
        n = len(names)
        for i, name in enumerate(names):
            ang = math.radians(90 - i * 360.0 / n)
            x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
            ax.plot([cx, x], [cy, y], color=BLUE, lw=1.0, zorder=1)
            ax.add_patch(Circle((x, y), rr, fc="white", ec=BLUE, lw=1.4, zorder=3))
            ax.text(x, y, name, ha="center", va="center", color=NAVY,
                    fontsize=fs, fontweight="bold", zorder=4, linespacing=1.1)

    ring(inner, 26, 9.2, 6.6)
    ring(outer, 48, 8.6, 6.4)
    save(fig, "d_circles.png")


# --------------------------------------------------------- 9. familia de tokens
def d_family():
    fig, ax = fig_ax(10, 5, ylim=(0, 50))
    box(ax, 8, 25, 15, 16, "Cliente\n(navegador / app)", fs=9, bold=True)
    box(ax, 40, 25, 22, 14, "Servidor de\nautorización", fc=LIGHT, fs=9, bold=True)
    box(ax, 80, 37, 24, 11, "Access token\n(API · corto)", fc="#FFFFFF", ec=BLUE, fs=8.5)
    box(ax, 80, 25, 24, 11, "Refresh token\n(endpoint de token)", fc="#FFFFFF", ec=BLUE, fs=8.5)
    box(ax, 80, 13, 24, 11, "ID token\n(identifica, no autoriza)", fc="#FFFFFF", ec=BLUE, fs=8.5)
    arrow(ax, (15.6, 27), (29, 27))
    ax.text(22.5, 30.4, "código (1 uso)", ha="center", fontsize=7.6, color=GRAY)
    arrow(ax, (51, 25), (67.6, 37), rad=-0.12)
    arrow(ax, (51, 25), (67.6, 25), rad=0.0)
    arrow(ax, (51, 25), (67.6, 13), rad=0.12)
    ax.text(60.5, 33.5, "emite tokens", ha="center", fontsize=7.6, color=GRAY)
    save(fig, "d_family.png")


# --------------------------------------------------------- 11. anatomía del JWT
def d_jwt():
    fig, ax = fig_ax(10, 5, ylim=(0, 50))
    parts = [
        ("HEADER", '{"alg":"RS256",\n"typ":"JWT"}', RED),
        ("PAYLOAD", '{iss, sub, aud,\nexp, scope, amr}', BLUE),
        ("SIGNATURE", "firma del\nemisor", GREEN),
    ]
    xs = [17, 50, 83]
    for (name, content, col), x in zip(parts, xs):
        box(ax, x, 30, 26, 15, content, fc="white", ec=col, tc=NAVY, fs=8.2, lw=1.8)
        ax.text(x, 42.5, name, ha="center", fontsize=8.8, color=col, fontweight="bold")
    for x in (33, 66.5):
        ax.text(x, 30, ".", ha="center", va="center", fontsize=22, color=NAVY)
    ax.text(50, 20.5, "cada parte va en base64url  ·  base64 NO es cifrado",
            ha="center", fontsize=8.4, color=GRAY, style="italic")
    ax.text(50, 9, "firmado ≠ sellado:  el payload lo lee cualquiera  →  JWE para confidencialidad",
            ha="center", fontsize=8.6, color=NAVY, fontweight="bold")
    save(fig, "d_jwt.png")


# --------------------------------------------------------------- 13. transporte
def d_transport():
    fig, ax = fig_ax(10, 5, ylim=(0, 50))
    box(ax, 17, 28, 26, 16, "Cabecera\nAuthorization: Bearer …", fc="#FFFFFF", ec=GREEN, fs=9, bold=True)
    box(ax, 50, 28, 26, 16, "Cookie\nHttpOnly + SameSite", fc="#FFFFFF", ec=GREEN, fs=9, bold=True)
    box(ax, 83, 28, 26, 16, "Query string\n?access_token=…", fc="#FDECEA", ec=RED, fs=9, bold=True)
    ax.plot([70.4, 95.6], [33.4, 22.6], color=RED, lw=3, zorder=5)
    ax.plot([70.4, 95.6], [22.6, 33.4], color=RED, lw=3, zorder=5)
    ax.text(17, 12.5, "inmune a CSRF\n(no la envía el navegador sola)", ha="center", fontsize=7.8, color=GRAY, linespacing=1.3)
    ax.text(50, 12.5, "protege de XSS\n(exige mitigar CSRF)", ha="center", fontsize=7.8, color=GRAY, linespacing=1.3)
    ax.text(83, 12.0, "prohibido: RFC 9700 (2025)\nqueda en logs, Referer e historial", ha="center", fontsize=7.8, color=RED, linespacing=1.3)
    save(fig, "d_transport.png")


# ---------------------------------------------------------- 14. timeline de MFA
def d_mfa():
    fig, ax = fig_ax(10, 4.6, ylim=(0, 46))
    y = 26
    ax.plot([6, 94], [y, y], color=NAVY, lw=2.0, zorder=1)
    steps = [(12, "Password"), (30, "MFA"), (48, "Emisión"), (72, "Token"), (92, "API")]
    for x, t in steps:
        dot(ax, x, y, 1.4, YEL if t == "MFA" else NAVY)
        ax.text(x, y + 6.2, t, ha="center", fontsize=9, color=NAVY, fontweight="bold")
    ax.text(72, y - 7.2, "vive 30 días o más", ha="center", fontsize=8.2, color=GRAY, style="italic")
    # llave de la MFA
    a = FancyArrowPatch((24, 12.5), (36, 12.5), arrowstyle="-", lw=1.4, color=YEL)
    ax.add_patch(a)
    ax.text(30, 8.0, "la MFA protege este instante", ha="center", fontsize=8.4, color="#B8860B", fontweight="bold")
    # llave de la vida del token
    b = FancyArrowPatch((54, 39.5), (90, 39.5), arrowstyle="-", lw=1.4, color=BLUE)
    ax.add_patch(b)
    ax.text(72, 35.5, "acá ya solo viaja un string", ha="center", fontsize=8.4, color="#2A6FB0", fontweight="bold")
    save(fig, "d_mfa.png")


# ----------------------------------------------------------- 19. OWASP API Top 10
def d_owasp():
    fig, ax = fig_ax(10, 5.6, ylim=(0, 56))
    items = [
        ("Api1 · BOLA — autorización a nivel de objeto", True),
        ("Api2 · Autenticación rota", False),
        ("Api3 · BOPLA — exposición de propiedades", False),
        ("Api4 · Consumo de recursos sin límites", False),
        ("Api5 · BFLA — autorización a nivel de función", False),
        ("Api6 · Acceso a flujos de negocio sensibles", False),
        ("Api7 · SSRF", False),
        ("Api8 · Configuración de seguridad incorrecta", False),
        ("Api9 · Gestión impropia del inventario", False),
        ("Api10 · Consumo inseguro de APIs de terceros", False),
    ]
    y0, dy = 51, 5.0
    for i, (t, hot) in enumerate(items):
        y = y0 - i * dy
        fc = "#FDECEA" if hot else "#FFFFFF"
        ec = RED if hot else BLUE
        box(ax, 50, y, 84, 4.2, t, fc=fc, ec=ec, fs=8.6,
            bold=hot, lw=1.8 if hot else 1.1)
    ax.text(50, 1.2, "El token es la puerta; estos riesgos viven en todo el edificio.",
            ha="center", fontsize=8.4, color=GRAY, style="italic")
    save(fig, "d_owasp.png")


# --------------------------------------------------------------- 23. PoP / atado
def d_pop():
    fig, ax = fig_ax(10, 5, ylim=(0, 50))
    box(ax, 26, 37, 40, 13, "mTLS + token atado\nal certificado\n(RFC 8705, 2020)", fc="#FFFFFF", ec=BLUE, fs=8.6, bold=True)
    box(ax, 74, 37, 40, 13, "DPoP: firma por request\njti · htm · htu\n(RFC 9449, 2023)", fc="#FFFFFF", ec=BLUE, fs=8.6, bold=True)
    box(ax, 50, 13, 54, 12, "Token atado a su portador\n(sender-constrained)", fc=LIGHT, ec=NAVY, fs=10, bold=True)
    arrow(ax, (26, 30.4), (42, 19.4), rad=-0.15)
    arrow(ax, (74, 30.4), (58, 19.4), rad=0.15)
    ax.text(50, 45.5, "Si la posesión no basta, se exige prueba de posesión.",
            ha="center", fontsize=8.8, color=GRAY, style="italic")
    save(fig, "d_pop.png")


# --------------------------------------------------------- 24. rotación del refresh
def d_refresh():
    fig, ax = fig_ax(10, 5, ylim=(0, 50))
    box(ax, 22, 33, 30, 13, "Refresh token\n(vigente)", fc="#FFFFFF", ec=BLUE, fs=9, bold=True)
    box(ax, 75, 33, 30, 13, "Nuevo access\n+ nuevo refresh", fc=LIGHT, ec=NAVY, fs=9, bold=True)
    box(ax, 22, 12, 30, 12, "Refresh viejo\nINVALIDADO", fc="#FDECEA", ec=RED, fs=9, bold=True)
    arrow(ax, (37, 33), (60, 33))
    ax.text(48.5, 36.6, "se usa una vez", ha="center", fontsize=8, color=GRAY)
    arrow(ax, (75, 26.4), (75, 19), rad=0)
    arrow(ax, (60, 16), (37, 16), rad=0)
    ax.text(48.5, 9.1, "si vuelve a aparecer, delata el reuso",
            ha="center", fontsize=8.2, color=RED, style="italic")
    save(fig, "d_refresh.png")


if __name__ == "__main__":
    d_circles(); d_family(); d_jwt(); d_transport(); d_mfa(); d_owasp(); d_pop(); d_refresh()
    print("listo ->", OUT)
