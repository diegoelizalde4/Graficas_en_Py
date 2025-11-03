# curva_trebol_3d.py
import pygame
from Funciones import Funciones
import math
import sys

sys.setrecursionlimit(2000)

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Curva Paramétrica 3D (Fig. 3.13)")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
AZUL = (100, 100, 255)

# Crear objeto Funciones
func = Funciones(ventana)

# --- Configuración para la gráfica 3D ---
# Punto de origen de los ejes en la pantalla
origen_x = 400
origen_y = 300 # Centrado verticalmente

escala_xy = 100 # Escala para el "plano" (x, y)
escala_z = 100 # Escala para la "altura" (z)

# Bucle principal
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    ventana.fill(NEGRO)

    # 1. Dibujar los ejes 3D como referencia
    func.dibujar_ejes_3d(origen_x, origen_y, 150, GRIS) # Ejes más cortos

    # 2. Dibujar la curva 3D
    func.dibujar_curva_trebol_3d(
        origen_x,
        origen_y,
        escala_xy,
        escala_z,
        AZUL
    )

    pygame.display.update()

pygame.quit()