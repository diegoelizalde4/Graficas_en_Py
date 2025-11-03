# parametrica.py
import pygame
from Funciones import Funciones
import math
import sys

sys.setrecursionlimit(2000)

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Curva Paramétrica")

# Colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)

# Crear objeto Funciones
func = Funciones(ventana)

# --- Configuración para la gráfica ---
escala = 40

# Offset para posicionar el inicio de la curva en la pantalla
offset_x = 50
offset_y = 500  # Un valor alto para que la curva se dibuje desde abajo hacia arriba

# Bucle principal
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    ventana.fill(NEGRO)

    # Dibujar la curva paramétrica
    func.dibujar_curva_parametrica(offset_x, offset_y, escala, VERDE)

    pygame.display.update()

pygame.quit()