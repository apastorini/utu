# adventure/scenes/juego_scene.py
"""
Escena de juego de la aventura grafica.

Tres habitaciones conectadas (sala -> biblioteca -> bodega) con:
  - hotspots clicables (NPC, llave, pocion y puerta),
  - salidas de flecha (este / oeste / norte / sur),
  - inventario visible,
  - cursor propio que cambia sobre los hotspots,
  - dialogos con opciones (DialogueBox).

Objetivo: coger la LLAVE en la biblioteca y abrir la PUERTA de la bodega.
"""

import pygame

from engine.ui import Scene
from engine.hotspot import Hotspot
from engine.inventory import Inventory, Item
from engine.cursor import Cursor
from engine.dialogue import DialogueBox, DialogueNode
from engine.particle import ParticleSystem
from engine.ui_elements import Label, Panel

INVENTARIO_ORIGEN = (18, 122)
SLOT = 56


class JuegoScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.screen = game.screen
        self.ancho = game.screen.get_width()
        self.alto = game.screen.get_height()

        # Piezas de aventura del motor.
        self.inventory = Inventory(capacity=6)
        self.cursor = Cursor()
        self.dialogue = DialogueBox(game.screen)
        self.particles = ParticleSystem()

        # Estado de la partida.
        self.recogidos = set()       # objetos ya cogidos (llave, pocion)
        self.hotspots = []           # zonas clicables de la habitacion actual
        self.objetos = []            # (imagen, rect) a dibujar encima del fondo
        self.salidas = []            # (Hotspot, direccion)
        self.hovered = None
        self.mensaje = ""
        self.mensaje_t = 0.0
        self._pending_final = False

        self.font = pygame.font.Font(None, 32)
        self.label_hab = Label("", (self.ancho // 2, 26), size=36,
                               color=(255, 236, 180), align="center")
        self.label_inv = Label("Inventario", (14, 98), size=24,
                               color=(226, 220, 190))

        self._cargar_habitacion("sala")

    # ================================================================== #
    #  Construccion de habitaciones
    # ================================================================== #
    def _add_hotspot(self, name, rect, callback):
        hs = Hotspot(rect, name=name, callback=callback)
        self.hotspots.append(hs)
        return hs

    def _add_objeto(self, nombre, rect):
        img = self.game.assets.get_image(nombre)
        if img.get_size() != rect.size:
            img = pygame.transform.smoothscale(img, rect.size)
        self.objetos.append((img, rect))

    def _add_salida(self, direccion, rect, destino):
        hs = Hotspot(rect, name="salida_" + direccion,
                     callback=lambda _hs: self._ir(destino))
        hs.direccion = direccion
        self.salidas.append((hs, direccion))
        self.hotspots.append(hs)

    def _cargar_habitacion(self, nombre):
        self.habitacion = nombre
        self.hotspots = []
        self.objetos = []
        self.salidas = []
        self.hovered = None
        self._pending_final = False

        self.fondo = self.game.assets.get_image(nombre)

        if nombre == "sala":
            self.label_hab.text = "Sala principal"
            self._add_objeto("npc", pygame.Rect(448, 300, 140, 250))
            self._add_hotspot("npc", pygame.Rect(428, 292, 180, 280),
                              self._hablar_npc)
            self._add_salida("este", pygame.Rect(938, 236, 86, 176), "biblioteca")

        elif nombre == "biblioteca":
            self.label_hab.text = "Biblioteca"
            self._add_salida("oeste", pygame.Rect(0, 236, 86, 176), "sala")
            self._add_salida("norte", pygame.Rect(452, 0, 120, 84), "bodega")
            if "llave" not in self.recogidos:
                r = pygame.Rect(624, 424, 96, 96)
                self._add_objeto("llave", r)
                self._add_hotspot("llave", r.inflate(28, 28), self._coger_llave)

        elif nombre == "bodega":
            self.label_hab.text = "Bodega"
            self._add_salida("sur", pygame.Rect(452, 556, 120, 84), "biblioteca")
            rp = pygame.Rect(400, 205, 240, 350)
            self._add_objeto("puerta", rp)
            self._add_hotspot("puerta", rp, self._usar_puerta)
            if "pocion" not in self.recogidos:
                r2 = pygame.Rect(150, 430, 72, 92)
                self._add_objeto("pocion", r2)
                self._add_hotspot("pocion", r2.inflate(30, 24), self._coger_pocion)

    # ================================================================== #
    #  Acciones de los hotspots
    # ================================================================== #
    def _ir(self, destino):
        self.game.audio.play_sound("click")
        self._cargar_habitacion(destino)

    def _coger_llave(self, _hs):
        if self.inventory.add(Item("llave", self.game.assets.get_image("llave"),
                                   "Abre la puerta de la bodega")):
            self.recogidos.add("llave")
            self.game.audio.play_sound("coin")
            self._set_mensaje("Has cogido la LLAVE dorada.")
            self.particles.emit(672, 470, count=28, color=(255, 212, 70),
                                speed=(60, 210), life=(0.4, 0.9))
            self._cargar_habitacion("biblioteca")

    def _coger_pocion(self, _hs):
        if self.inventory.add(Item("pocion", self.game.assets.get_image("pocion"),
                                   "Una pocion azul que reanima")):
            self.recogidos.add("pocion")
            self.game.audio.play_sound("coin")
            self._set_mensaje("Has cogido una POCION azul.")
            self.particles.emit(186, 470, count=24, color=(90, 170, 255),
                                speed=(50, 180), life=(0.4, 0.9))
            self._cargar_habitacion("bodega")

    def _usar_puerta(self, _hs):
        if self.inventory.has("llave"):
            self.game.audio.play_sound("correct")
            nodos = {"start": DialogueNode(
                "Giras la llave dorada... CLIC. La puerta se abre hacia la salida.",
                "Puerta", choices=[("Salir", None)],
                action=lambda _n: self.game.audio.play_sound("type"))}
            self._pending_final = True
        else:
            self.game.audio.play_sound("wrong")
            nodos = {"start": DialogueNode(
                "La puerta esta cerrada con llave. Tiene que haber una por aqui...",
                "Puerta", choices=[("Vale", None)],
                action=lambda _n: self.game.audio.play_sound("type"))}
        self.dialogue.start(nodos, "start")

    def _hablar_npc(self, _hs):
        self.game.audio.play_sound("click")
        nodos = {
            "start": DialogueNode(
                "Buenas, viajero. Que se te ofrece?", "Anciano",
                choices=[("Donde hay una llave?", "llave"),
                         ("Como salgo de aqui?", "salir"),
                         ("Nada, gracias.", None)],
                action=lambda _n: self.game.audio.play_sound("type")),
            "llave": DialogueNode(
                "Una llave dorada duerme en la biblioteca, al ESTE.", "Anciano",
                choices=[("Gracias.", "gracias"), ("Y la salida?", "salir")],
                action=lambda _n: self.game.audio.play_sound("type")),
            "salir": DialogueNode(
                "Al este la biblioteca; al norte de ella, la bodega. Alli esta la puerta.",
                "Anciano", choices=[("Entendido.", None)],
                action=lambda _n: self.game.audio.play_sound("type")),
            "gracias": DialogueNode(
                "Buena suerte, forastero.", "Anciano",
                choices=[("Adios.", None)],
                action=lambda _n: self.game.audio.play_sound("type")),
        }
        self.dialogue.start(nodos, "start")

    # ================================================================== #
    def _set_mensaje(self, texto):
        self.mensaje = texto
        self.mensaje_t = 3.0

    # ================================================================== #
    def _dialogue_click(self, pos):
        """Selecciona una opcion del dialogo con el raton (o avanza)."""
        d = self.dialogue
        if not d.current:
            return
        x = d.rect.x + 16
        y = d.rect.y + 12
        if d.current.speaker:
            y += d.font.get_height() + 4
        y += len(d.lines) * (d.font.get_height() + 2)
        alto = d.small.get_height() + 2
        for i, _choice in enumerate(d.current.choices):
            rect = pygame.Rect(x + 20, y + i * alto, d.width - 40, alto)
            if rect.collidepoint(pos):
                d.choice_index = i
                break
        d._confirm()

    def handle_events(self, events):
        for event in events:
            # Mientras hay dialogo, todo va al cuadro de dialogo.
            if self.dialogue.active:
                self.dialogue.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._dialogue_click(event.pos)
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
                return

            # Seleccionar objeto del inventario (no dispara hotspots).
            if self.inventory.handle_event(event, INVENTARIO_ORIGEN, SLOT) is not None:
                self.game.audio.play_sound("click")
                continue

            for hs in self.hotspots:
                if hs.handle_event(event):
                    break

    # ================================================================== #
    def update(self):
        dt = 1.0 / max(1, self.game.fps)
        self.particles.update(dt)

        if self.mensaje_t > 0:
            self.mensaje_t = max(0.0, self.mensaje_t - dt)

        # Hotspot bajo el cursor (para cambiar el puntero).
        self.hovered = None
        if not self.dialogue.active:
            pos = pygame.mouse.get_pos()
            for hs in self.hotspots:
                if hs.contains(pos):
                    self.hovered = hs
                    break

        # Al cerrar el dialogo de la puerta abierta, pasamos a la escena final.
        if self._pending_final and not self.dialogue.active:
            self._pending_final = False
            self.game.change_scene("final")

    # ================================================================== #
    def _draw_arrow(self, surface, rect, direccion, hovered):
        color = (255, 236, 120) if hovered else (226, 196, 90)
        cx, cy = rect.center
        s = 26
        if direccion == "este":
            pts = [(cx - s, cy - s), (cx + s, cy), (cx - s, cy + s)]
        elif direccion == "oeste":
            pts = [(cx + s, cy - s), (cx - s, cy), (cx + s, cy + s)]
        elif direccion == "norte":
            pts = [(cx - s, cy + s), (cx, cy - s), (cx + s, cy + s)]
        else:  # sur
            pts = [(cx - s, cy - s), (cx, cy + s), (cx + s, cy - s)]
        pygame.draw.polygon(surface, color, pts)
        pygame.draw.polygon(surface, (52, 34, 12), pts, 3)

    def draw(self, surface):
        surface.blit(self.fondo, (0, 0))

        for img, rect in self.objetos:
            surface.blit(img, rect)

        for hs, direccion in self.salidas:
            self._draw_arrow(surface, hs.rect, direccion, self.hovered is hs)

        self.particles.draw(surface)

        # HUD: nombre de habitacion + inventario.
        self.label_hab.draw(surface)
        self.label_inv.draw(surface)
        self.inventory.draw(surface, INVENTARIO_ORIGEN, SLOT)

        # Aviso temporal.
        if self.mensaje_t > 0:
            panel = Panel((self.ancho // 2 - 270, 66, 540, 46),
                          color=(0, 0, 0, 170), border=(230, 210, 140))
            panel.draw(surface)
            texto = self.font.render(self.mensaje, True, (255, 240, 200))
            surface.blit(texto, texto.get_rect(center=(self.ancho // 2, 66 + 23)))

        self.dialogue.draw()
        self.cursor.draw(surface, hovered=self.hovered is not None)
