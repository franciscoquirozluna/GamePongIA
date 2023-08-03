
import pygame
from pygame.locals import *

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 640, 480
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 60
FPS = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Crear la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

# Posiciones iniciales de las paletas y la pelota
paddle1_pos = (HEIGHT - PADDLE_HEIGHT) // 2
paddle2_pos = (HEIGHT - PADDLE_HEIGHT) // 2
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [5, 5]

# Función para actualizar la pantalla
def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (0, paddle1_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - PADDLE_WIDTH, paddle2_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(screen, WHITE, ball_pos, BALL_RADIUS)
    pygame.display.flip()

# Bucle principal del juego
running = True
while running:
    clock.tick(FPS)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Movimiento de las paletas
    if keys[K_w] and paddle1_pos > 0:
        paddle1_pos -= 5
    if keys[K_s] and paddle1_pos < HEIGHT - PADDLE_HEIGHT:
        paddle1_pos += 5
    if keys[K_UP] and paddle2_pos > 0:
        paddle2_pos -= 5
    if keys[K_DOWN] and paddle2_pos < HEIGHT - PADDLE_HEIGHT:
        paddle2_pos += 5

    # Movimiento de la pelota
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Colisiones con las paletas
    if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if ball_pos[0] <= PADDLE_WIDTH and paddle1_pos <= ball_pos[1] <= paddle1_pos + PADDLE_HEIGHT:
        ball_vel[0] = -ball_vel[0]
    if ball_pos[0] >= WIDTH - PADDLE_WIDTH - BALL_RADIUS and paddle2_pos <= ball_pos[1] <= paddle2_pos + PADDLE_HEIGHT:
        ball_vel[0] = -ball_vel[0]

    # Si la pelota sale de la pantalla, reiniciarla en el centro
    if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH - BALL_RADIUS:
        ball_pos = [WIDTH // 2, HEIGHT // 2]

    # Dibujar los elementos del juego
    draw()

# Salir del juego
pygame.quit()
