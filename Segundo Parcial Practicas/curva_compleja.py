# curva_compleja.py
import pygame
from Funciones import Funciones
import math
import sys

sys.setrecursionlimit(2000)

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Curva Paramétrica Compleja (Fig. 3.6)")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Crear objeto Funciones
func = Funciones(ventana)

# --- Configuración para la gráfica ---
centro_x = 400
centro_y = 300
# La escala ajusta el tamaño de la figura. Puedes experimentar con este valor.
escala = 150

# Bucle principal
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    ventana.fill(NEGRO)

    # Dibujar la curva
    func.dibujar_curva_compleja(centro_x, centro_y, escala, BLANCO)

    pygame.display.update()

pygame.quit()