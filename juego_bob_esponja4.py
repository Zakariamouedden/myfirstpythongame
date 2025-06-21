import pygame
import sys
import random

# Inicializa pygame
pygame.init()

# Establece el tamaño de la ventana
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego Básico con Bob Esponja")

# Colores
yellow = (255, 255, 0)
brown = (139, 69, 19)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
explosion_color = (255, 255, 0)  # Amarillo para la explosión
green = (0, 255, 0)

# Posición inicial de Bob Esponja (como un rectángulo amarillo)
bob_width, bob_height = 50, 60
bob_rect = pygame.Rect(50, screen_height // 2 - bob_height // 2, bob_width, bob_height)

# Definir la velocidad de movimiento
speed = 5

# Definir la puerta
door_width, door_height = 60, 100  # Tamaño de la puerta
door_x = screen_width - door_width - 50  # Posición de la puerta
door_y = screen_height // 2 - door_height // 2

# Crear obstáculos (Calamardo)
obstacle_width, obstacle_height = 40, 60
obstacles_up = []  # Obstáculos que suben
obstacles_down = []  # Obstáculos que bajan

# Crear 5 obstáculos (con posiciones aleatorias por toda la pantalla)
for _ in range(5):
    x = random.randint(50, screen_width - 100)  # Posición aleatoria en X
    y_up = random.randint(-200, -50)  # Posición aleatoria fuera de la pantalla, arriba
    y_down = random.randint(screen_height + 50, screen_height + 200)  # Posición aleatoria fuera de la pantalla, abajo
    obstacles_up.append(pygame.Rect(x, y_up, obstacle_width, obstacle_height))
    obstacles_down.append(pygame.Rect(x, y_down, obstacle_width, obstacle_height))

# Función de explosión
def draw_explosion(position):
    pygame.draw.circle(screen, explosion_color, position, 30)
    pygame.draw.circle(screen, explosion_color, position, 20)
    pygame.draw.circle(screen, explosion_color, position, 10)

# Pantalla de atardecer
def draw_sunset_screen():
    screen.fill((255, 223, 186))  # Fondo de atardecer
    font = pygame.font.SysFont("Arial", 40)
    text = font.render("TE AMO AI-LYNG", True, red)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    pygame.display.update()

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento de Bob Esponja
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        bob_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        bob_rect.x += speed
    if keys[pygame.K_UP]:
        bob_rect.y -= speed
    if keys[pygame.K_DOWN]:
        bob_rect.y += speed

    # Comprobar si Bob Esponja entra en la puerta
    if bob_rect.colliderect(pygame.Rect(door_x, door_y, door_width, door_height)):
        draw_sunset_screen()
        pygame.time.wait(2000)  # Espera 2 segundos en la pantalla de atardecer
        running = False  # Terminar el juego después de mostrar el mensaje

    # Rellenar el fondo con un color
    screen.fill(blue)  # Fondo azul

    # Dibujar la puerta
    pygame.draw.rect(screen, (255, 0, 0), (door_x, door_y, door_width, door_height))

    # Dibujar a Bob Esponja
    pygame.draw.rect(screen, yellow, bob_rect)  # Cuerpo

    # Dibujar los ojos de Bob Esponja (círculos blancos y negros con pupilas azules)
    eye_radius = 8
    pygame.draw.circle(screen, white, (bob_rect.x + 15, bob_rect.y + 20), eye_radius)  # Ojo izquierdo
    pygame.draw.circle(screen, white, (bob_rect.x + 35, bob_rect.y + 20), eye_radius)  # Ojo derecho
    pygame.draw.circle(screen, blue, (bob_rect.x + 15, bob_rect.y + 20), eye_radius // 2)  # Pupila izquierda
    pygame.draw.circle(screen, blue, (bob_rect.x + 35, bob_rect.y + 20), eye_radius // 2)  # Pupila derecha

    # Dibujar la nariz larga (como una línea)
    pygame.draw.line(screen, yellow, (bob_rect.x + 25, bob_rect.y + 25), (bob_rect.x + 50, bob_rect.y + 20), 5)

    # Dibujar los pantalones marrones en la mitad del cuerpo
    pygame.draw.rect(screen, brown, (bob_rect.x + 10, bob_rect.y + 30, 30, 15))  # Parte superior de los pantalones
    pygame.draw.rect(screen, brown, (bob_rect.x + 10, bob_rect.y + 45, 30, 15))  # Parte inferior de los pantalones

    # Dibujar las piernas (amarillas)
    pygame.draw.rect(screen, yellow, (bob_rect.x + 10, bob_rect.y + 60, 10, 20))  # Pierna izquierda
    pygame.draw.rect(screen, yellow, (bob_rect.x + 30, bob_rect.y + 60, 10, 20))  # Pierna derecha

    # Dibujar los obstáculos (Calamardo)
    for obstacle in obstacles_up:
        pygame.draw.rect(screen, green, obstacle)  # Obstáculo que sube
        obstacle.y += 5  # Mover hacia abajo
        if obstacle.y > screen_height:
            obstacle.y = random.randint(-200, -50)  # Resetea la posición al tope de la pantalla

    for obstacle in obstacles_down:
        pygame.draw.rect(screen, green, obstacle)  # Obstáculo que baja
        obstacle.y -= 5  # Mover hacia arriba
        if obstacle.y < -obstacle_height:
            obstacle.y = random.randint(screen_height + 50, screen_height + 200)  # Resetea la posición al fondo de la pantalla

    # Comprobar colisiones con obstáculos
    for obstacle in obstacles_up + obstacles_down:
        if bob_rect.colliderect(obstacle):
            # Efecto de explosión
            draw_explosion(bob_rect.center)
            pygame.display.update()
            pygame.time.wait(500)  # Espera para mostrar la explosión
            # Reiniciar posición de Bob Esponja
            bob_rect.x = 50
            bob_rect.y = screen_height // 2 - bob_height // 2

    # Actualizar la pantalla
    pygame.display.update()

    # Controlar la velocidad del juego
    pygame.time.Clock().tick(30)

# Salir del juego
pygame.quit()
sys.exit()



