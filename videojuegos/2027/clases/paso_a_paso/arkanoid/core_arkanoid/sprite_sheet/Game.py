import random
import traceback
import pygame


from arkanoid.core_arkanoid.SpriteSheet import SpriteSheet
from arkanoid.core_arkanoid.sprite_sheet.Ball import Ball
from arkanoid.core_arkanoid.sprite_sheet.Brick import Brick
from arkanoid.core_arkanoid.sprite_sheet.Player import Player
from core.Colors import AZUL_OSCURO, NEGRO, ROJO, BLANCO

from core.utils.utils import ANCHO, ALTO

# Importamos la herramienta para extraer sprites


pygame.init()
pygame.mixer.init()

# --- CARGAMOS SONIDOS ---
try:
    sonido_golpe = pygame.mixer.Sound('../assets/sounds/hit.mp3')
    pygame.mixer.music.load('../assets/music/song18.mp3')
    pygame.mixer.music.play(-1)
except FileNotFoundError:
    print("Advertencia: No se encontraron los archivos de audio en la ruta especificada.")


class Game:
    PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Arkanoid')

    fuente = pygame.font.Font(None, 36)
    fuente_grande = pygame.font.Font(None, 72)

    reloj = pygame.time.Clock()

    def __init__(self):
        # 1. Cargamos el spritesheet
        hoja_sprites = SpriteSheet('../../assets/sprites/image_0918c1.png')

        self.NUM_LADRILLOS_FILA = 10
        self.ANCHO_LADRILLO = ANCHO // self.NUM_LADRILLOS_FILA

        # 2. Extraemos las imágenes usando tus coordenadas exactas y quitando el fondo fucsia

        # La pala. Usé valores genéricos, pero si usas el visor puedes poner los exactos:
        imagen_pala = hoja_sprites.obtener_imagen(384, 32, 64, 32, 100, 20, quitar_fondo=True)

        # Ladrillo (Tus medidas: X: 193, Y: 47, Ancho: 30, Alto: 15)
        imagen_ladrillo = hoja_sprites.obtener_imagen(193, 47, 30, 15, self.ANCHO_LADRILLO, 30, quitar_fondo=True)

        # Pelota (Tus medidas: X: 102, Y: 194, Ancho: 21, Alto: 27)
        imagen_pelota = hoja_sprites.obtener_imagen(102, 194, 21, 27, 20, 20, quitar_fondo=True)

        # 3. Inicializamos las variables pasando las imágenes recortadas
        self.jugador = Player(ANCHO // 2 - 50, 450, imagen_pala)
        self.pelota = Ball(50, 350, imagen_pelota)

        self.puntuacion = 0
        self.ladrillos = []
        self.estado_juego = 'jugando'

        if not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.play(-1)
            except:
                pass

        # 4. Crear los ladrillos
        for fila in range(5):
            for col in range(self.NUM_LADRILLOS_FILA):
                ladrillo = Brick(col * self.ANCHO_LADRILLO, fila * 40 + 50, imagen_ladrillo)
                self.ladrillos.append(ladrillo)

    def game_loop(self):
        ejecutando = True
        while ejecutando:
            # --- INPUT PRINCIPAL ---
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

                if self.estado_juego == 'game_over':
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_SPACE:
                            self.__init__()

            # --- LÓGICA SEGÚN ESTADO ---
            if self.estado_juego == 'jugando':
                teclas = pygame.key.get_pressed()

                # --- UPDATE ---
                self.jugador.mover(teclas)
                self.pelota.update()

                # Colisión pelota con pala
                if self.pelota.rect.colliderect(self.jugador.rect):
                    self.pelota.velocidad_y *= -1
                    self.pelota.rect.bottom = self.jugador.rect.top

                # Colisión pelota con ladrillos
                for ladrillo in self.ladrillos[:]:
                    if self.pelota.rect.colliderect(ladrillo.rect):
                        self.ladrillos.remove(ladrillo)
                        self.pelota.velocidad_y *= -1
                        self.puntuacion += 10

                        try:
                            # Descomenta esto cuando el audio funcione
                            # sonido_golpe.play()
                            pass
                        except:
                            pass

                # Si la pelota cae por debajo del borde inferior
                if self.pelota.rect.top > ALTO:
                    self.estado_juego = 'game_over'

                # --- RENDER JUGANDO ---
                self.PANTALLA.fill(AZUL_OSCURO)

                # Dibujamos en orden: primero ladrillos, luego jugador, luego pelota encima
                for ladrillo in self.ladrillos:
                    ladrillo.dibujar(self.PANTALLA)
                self.jugador.dibujar(self.PANTALLA)
                self.pelota.dibujar(self.PANTALLA)

                # Interfaz
                texto_puntuacion = self.fuente.render(f"Puntuación: {self.puntuacion}", True, BLANCO)
                self.PANTALLA.blit(texto_puntuacion, (10, 10))

            elif self.estado_juego == 'game_over':
                # --- RENDER GAME OVER ---
                self.PANTALLA.fill(NEGRO)
                texto_game_over = self.fuente_grande.render("GAME OVER", True, ROJO)
                texto_instruccion = self.fuente.render("Presiona ESPACIO para reiniciar", True, BLANCO)

                pos_game_over = texto_game_over.get_rect(center=(ANCHO / 2, ALTO / 2 - 50))
                pos_instruccion = texto_instruccion.get_rect(center=(ANCHO / 2, ALTO / 2 + 50))

                self.PANTALLA.blit(texto_game_over, pos_game_over)
                self.PANTALLA.blit(texto_instruccion, pos_instruccion)

            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()


# --- PUNTO DE ENTRADA CON DEPURACIÓN ---
if __name__ == "__main__":
    try:
        juego = Game()
        juego.game_loop()
    except Exception as e:
        print("\n" + "=" * 50)
        print("¡EL JUEGO SE CERRÓ POR UN ERROR!")
        print("=" * 50)
        traceback.print_exc()
        print("=" * 50)
        input("Presiona ENTER para salir y corregir el error...")