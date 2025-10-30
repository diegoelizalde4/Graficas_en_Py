# curvas8.py
import pygame
from Funciones import Funciones
import math
import sys

sys.setrecursionlimit(2000)

pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Representación de y = sen(x) con 8 puntos")

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)  # Para los puntos individuales

# Crear objeto Funciones
func = Funciones(ventana)

# --- Configuración para la gráfica ---
# Rango para x: de 0 a pi
x_inicio = 0.0
x_fin = math.pi
num_puntos = 8

escala_x = 600 / math.pi
escala_y = -300  # Negativo para invertir el eje Y (Pygame tiene Y creciente hacia abajo)

offset_x = 100
offset_y = 400  # Para que el eje Y esté arriba y la curva crezca hacia arriba

puntos_grafica = []
for i in range(num_puntos):
    x = x_inicio + (x_fin - x_inicio) * i / (num_puntos - 1)
    y = math.sin(x)
    puntos_grafica.append((x, y))

corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    ventana.fill(NEGRO)

    func.dibujar_puntos_conectados(
        puntos_grafica,
        AZUL,
        escala_x=escala_x,
        escala_y=escala_y,
        offset_x=offset_x,
        offset_y=offset_y,
        dibujar_puntos_individuales=True,  # Dibuja los puntos rojos
        color_puntos_individuales=ROJO
    )

    pygame.display.update()

pygame.quit()