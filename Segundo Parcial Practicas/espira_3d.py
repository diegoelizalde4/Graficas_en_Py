# espiral_3d.py
import pygame
from Funciones import Funciones
import math
import sys

sys.setrecursionlimit(2000)

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Curva Paramétrica 3D (Espiral)")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
GRIS = (100, 100, 100)

# Crear objeto Funciones
func = Funciones(ventana)

# --- Configuración para la gráfica 3D ---
# Punto de origen de los ejes en la pantalla
origen_x = 400
origen_y = 500

# Escalas para cada eje
escala_xy = 150  # Escala para el "ancho" (x, y)
escala_z = 15  # Escala para la "altura" (z)

# Bucle principal
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    ventana.fill(NEGRO)

    # 1. Dibujar los ejes 3D como referencia
    func.dibujar_ejes_3d(origen_x, origen_y, 200, GRIS)

    # 2. Dibujar la curva 3D
    func.dibujar_espiral_3d(
        origen_x,
        origen_y,
        escala_xy,
        escala_z,
        BLANCO,
        ROJO
    )

    pygame.display.update()

pygame.quit()