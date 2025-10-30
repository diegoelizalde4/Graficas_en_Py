# proyeccion_paralela_cubo.py
import pygame
from Funcion3d import Funcion3d # Asume que Funcion3d.py está en el mismo directorio
import math
import sys

sys.setrecursionlimit(2000)

# --- Función de Proyección Paralela ---
def proyectar_paralelo(punto_3d, vp=(1, 2, 1)):
    """Proyecta un punto 3D al plano XY (z=0) usando proyección paralela."""
    x1, y1, z1 = punto_3d
    xp, yp, zp = vp

    if zp == 0:
        return (x1, y1)

    # Fórmulas de proyección paralela sobre el plano z=0
    x2 = x1 - xp * (z1 / zp)
    y2 = y1 - yp * (z1 / zp)
    return (x2, y2)

# --- Definición del Cubo ---
vertices_3d = {
    'A': (2, 3, 2), 'B': (3, 3, 2), 'C': (3, 3, 3), 'D': (2, 3, 3),
    'E': (2, 2, 2), 'F': (3, 2, 2), 'G': (3, 2, 3), 'H': (2, 2, 3)
}

aristas = [
    ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), # Cara superior
    ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'E'), # Cara inferior
    ('A', 'E'), ('B', 'F'), ('C', 'G'), ('D', 'H')  # Conexiones verticales
]

vector_proyeccion = (1, 2, 1)

# --- Inicializar Pygame ---
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Proyección Paralela de un Cubo (Origen Superior)")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Crear objeto Funcion3d
func3d = Funcion3d(ventana)

# --- Configuración de visualización ---
escala = 100
offset_x = 350 # Mantenemos el ajuste horizontal
offset_y = 150 # <-- Ajustado para poner el origen cerca del borde SUPERIOR (antes 500)

# --- Proyectar los vértices ---
vertices_2d_proyectados = {}
for nombre, coords_3d in vertices_3d.items():
    coords_2d = proyectar_paralelo(coords_3d, vector_proyeccion)
    screen_x = coords_2d[0] * escala + offset_x
    screen_y = -coords_2d[1] * escala + offset_y # Invertir Y para Pygame
    vertices_2d_proyectados[nombre] = (screen_x, screen_y)

# Bucle principal
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    ventana.fill(NEGRO)

    # Dibujar las aristas proyectadas
    for arista in aristas:
        p1_nombre, p2_nombre = arista
        p1_coords = vertices_2d_proyectados[p1_nombre]
        p2_coords = vertices_2d_proyectados[p2_nombre]
        func3d.dibujar_linea_2d(p1_coords[0], p1_coords[1], p2_coords[0], p2_coords[1], BLANCO)

    # Opcional: Dibujar los vértices proyectados
    for nombre, coords_2d in vertices_2d_proyectados.items():
        func3d.dibujar_pixel_2d(coords_2d[0], coords_2d[1], ROJO, grosor=5)

    pygame.display.update()

pygame.quit()