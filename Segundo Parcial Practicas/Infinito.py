# Infinito.py
import pygame
from Funciones import Funciones
import math
import sys

# Es una buena práctica incluir el aumento del límite de recursión
sys.setrecursionlimit(2000)

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Curva del Infinito (Lemniscata de Gerono)")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Crear objeto Funciones
func = Funciones(ventana)

# --- Configuración para la gráfica ---
# Centro de la figura en la ventana
centro_x = 400
centro_y = 300

# 'r' es el radio o tamaño de la figura. Un valor más grande la hará más grande.
radio = 200

# Bucle principal
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    ventana.fill(NEGRO)

    # Dibujar la curva del infinito
    func.dibujar_infinito(centro_x, centro_y, radio, BLANCO)

    pygame.display.update()

pygame.quit()