# curvas100.py
import pygame
from Funciones import Funciones
import math
import sys

# Ajusta el límite de recursión si vas a usar Flood Fill
sys.setrecursionlimit(2000)

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Representación de y = sen(x) con 100 puntos")

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)

# Crear objeto Funciones
func = Funciones(ventana)

# --- Configuración para la gráfica ---
# Rango para x: de 0 a pi
x_inicio = 0.0
x_fin = math.pi
num_puntos = 100  # ¡Más puntos para una curva más suave!

# Ajuste de escala (mismos valores que para la curva de 8 puntos)
escala_x = 600 / math.pi
escala_y = -300
offset_x = 100
offset_y = 400

# Generar puntos (x, y)
puntos_grafica = []
for i in range(num_puntos):
    x = x_inicio + (x_fin - x_inicio) * i / (num_puntos - 1)
    y = math.sin(x)
    puntos_grafica.append((x, y))

# Bucle principal
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    ventana.fill(NEGRO)

    # Dibujar los puntos conectados (sin dibujar puntos individuales para una curva limpia)
    func.dibujar_puntos_conectados(
        puntos_grafica,
        AZUL,
        escala_x=escala_x,
        escala_y=escala_y,
        offset_x=offset_x,
        offset_y=offset_y,
        dibujar_puntos_individuales=False  # No dibujar los puntos individuales
    )

    pygame.display.update()

pygame.quit()