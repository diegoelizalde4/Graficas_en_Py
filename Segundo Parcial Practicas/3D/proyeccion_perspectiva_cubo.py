import pygame
from Funcion3d import Funcion3d # Asume que Funcion3d.py está en el mismo directorio
import math
import sys

sys.setrecursionlimit(2000)

# --- Función de Proyección en Perspectiva
def proyectar_perspectiva_1punto(punto_3d, cz):
    x1, y1, z1 = punto_3d


    if (z1 + cz) <= 0:
        print(f"Advertencia: Punto {punto_3d} está detrás o en el centro de proyección.")
        return (x1, y1) # Simplificación: proyectar como si z1=0

    # Fórmula de perspectiva simple
    factor_perspectiva = cz / (z1 + cz)
    x_p = x1 * factor_perspectiva
    y_p = y1 * factor_perspectiva

    return (x_p, y_p)

# --- Definición del Cubo ---
offset_3d = (2.5, 2.5, 2.5)
vertices_3d = {
    'A': (2 - offset_3d[0], 3 - offset_3d[1], 2 - offset_3d[2]),
    'B': (3 - offset_3d[0], 3 - offset_3d[1], 2 - offset_3d[2]),
    'C': (3 - offset_3d[0], 3 - offset_3d[1], 3 - offset_3d[2]),
    'D': (2 - offset_3d[0], 3 - offset_3d[1], 3 - offset_3d[2]),
    'E': (2 - offset_3d[0], 2 - offset_3d[1], 2 - offset_3d[2]),
    'F': (3 - offset_3d[0], 2 - offset_3d[1], 2 - offset_3d[2]),
    'G': (3 - offset_3d[0], 2 - offset_3d[1], 3 - offset_3d[2]),
    'H': (2 - offset_3d[0], 2 - offset_3d[1], 3 - offset_3d[2])
}


aristas = [
    ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), # Cara superior
    ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'E'), # Cara inferior
    ('A', 'E'), ('B', 'F'), ('C', 'G'), ('D', 'H')  # Conexiones verticales
]

distancia_cz = 10

# --- Inicializar Pygame ---
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Proyección en Perspectiva (1 Punto) - ESTÁTICO")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Crear objeto Funcion3d
func3d = Funcion3d(ventana)

# --- Configuración de visualización ---
escala = 300 # Escala más grande para la perspectiva
offset_x = 400 # Centro de la pantalla
offset_y = 300 # Centro de la pantalla

# --- Proyectar los vértices (se hace UNA SOLA VEZ) ---
vertices_2d_proyectados = {}
for nombre, coords_3d in vertices_3d.items():
    coords_2d = proyectar_perspectiva_1punto(coords_3d, distancia_cz)
    # Escalar y aplicar offset para visualización
    screen_x = coords_2d[0] * escala + offset_x
    screen_y = -coords_2d[1] * escala + offset_y # Invertir Y
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