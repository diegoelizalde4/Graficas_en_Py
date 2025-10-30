# curva_compleja_3d.py
import pygame
from Funcion3d import Funcion3d # Importa la clase 3D
import math
import sys

sys.setrecursionlimit(2000)

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Curva Compleja en 3D (Fig. 3.6)")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)

# Crear objeto Funcion3d
func3d = Funcion3d(ventana)

# --- Configuración 3D ---
origen_x = 400
origen_y = 300
escala_xy = 150 # Ajusta la escala según sea necesario
escala_z = 150 # Mantenemos la escala z aunque z=0 para consistencia

# Bucle principal
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    ventana.fill(NEGRO)

    # 1. Dibujar ejes 3D
    func3d.dibujar_ejes_3d(origen_x, origen_y, 250, GRIS) # Ejes un poco más largos

    # 2. Dibujar la curva compleja en 3D (plano z=0)
    func3d.dibujar_curva_compleja_3d(
        origen_x,
        origen_y,
        escala_xy,
        escala_z,
        BLANCO
    )

    pygame.display.update()

pygame.quit()