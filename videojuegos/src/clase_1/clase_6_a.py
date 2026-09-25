import pygame

from core.Collectible import Collectible
from core.Enemy import Enemy
from core.Player import Player


from utils.Colors import ROJO, AZUL_OSCURO, BLANCO
import random

pygame.init()
pygame.mixer.init()

# 3. Definir el tamaño de la ventana
ANCHO = 800
ALTO = 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))



# 4. Ponerle un título a la ventana
pygame.display.set_caption('Clase 3 y 4')


# --- ANTES DEL BUCLE PRINCIPAL ---
moneda =  Collectible(300, 300, 30, 30, (255, 223, 0))
fuente = pygame.font.Font(None, 36)
reloj = pygame.time.Clock()

# --- CARGAMOS SONIDOS ---
sonido_moneda = pygame.mixer.Sound('assets/sonidos/coin-drop-1.wav')
sonido_golpe = pygame.mixer.Sound('assets/sonidos/hit.mp3')

# --- CARGAMOS Y REPRODUCIMOS MÚSICA ---
pygame.mixer.music.load('assets/musica/music_1.wav')
pygame.mixer.music.play(-1)  # El -1 significa que se repetirá en bucle infinito

# --- CREAMOS VARIABLES Y OBJETOS ---
jugador = Player(50, 50)  # Ya no necesita ancho y alto
#enemigo = Enemy(150, 150)



puntuacion = 0 # Nuestra variable para la puntuación

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
# --- INPUT ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    # Obtenemos las teclas presionadas
    teclas = pygame.key.get_pressed()
# --- UPDATE ---
    jugador.mover(teclas)
    if jugador.rect.colliderect(moneda.rect):
        puntuacion += 1 # Aumentamos la puntuación en 1
        # Movemos la moneda a una nueva posición aleatoria
        moneda.rect.x = random.randint(0, ANCHO - moneda.rect.width)
        moneda.rect.y = random.randint(0, ALTO - moneda.rect.height)
        sonido_moneda.play()  # ¡Reproducimos el sonido!
# --- RENDER --- # 2. RENDERIZAR EL TEXTO
    texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
    PANTALLA.fill(AZUL_OSCURO)
    jugador.dibujar(PANTALLA)
    moneda.dibujar(PANTALLA)

    # 3. DIBUJAR EL TEXTO EN LA PANTALLA
    PANTALLA.blit(texto_puntuacion, (10, 10))
    # Lo ponemos en la esquina sup. izq.
    pygame.display.flip()
    # --- CONTROL DE TIEMPO ---
    # Le decimos al reloj que espere lo necesario para que el bucle
    # no se ejecute más de 60 veces por segundo.
    reloj.tick(60)

pygame.quit()