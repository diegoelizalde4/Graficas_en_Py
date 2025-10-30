# demo_transformaciones_por_pasos.py
import pygame
from Funcion3d import Funcion3d  # Tu archivo original para dibujar 2D
import Transformaciones3D as t3d  # El NUEVO archivo de funciones 3D
import math
import sys
import numpy as np

sys.setrecursionlimit(2000)


# --- Función de Proyección (la misma de antes) ---
def proyectar_perspectiva_1punto(punto_3d, cz):
    x1, y1, z1 = punto_3d
    if (z1 + cz) <= 0:
        return (x1, y1)
    factor_perspectiva = cz / (z1 + cz)
    x_p = x1 * factor_perspectiva
    y_p = y1 * factor_perspectiva
    return (x_p, y_p)


# --- Definición del Cubo (Centrado en el origen) ---
offset_3d = (2.5, 2.5, 2.5)
vertices_3d_originales = {
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
    ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'),  # Cara superior
    ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'E'),  # Cara inferior
    ('A', 'E'), ('B', 'F'), ('C', 'G'), ('D', 'H')  # Conexiones verticales
]

distancia_cz = 10

# --- Inicializar Pygame ---
pygame.init()
pygame.font.init()  # <-- NUEVO: Inicializar módulo de fuentes
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Transformaciones 3D por Pasos (Presiona ENTER)")  # <-- MODIFICADO
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
GRIS = (150, 150, 150)
func3d = Funcion3d(ventana)

# --- Configuración de visualización ---
escala_pantalla = 20
offset_x = 400
offset_y = 300

# --- NUEVO: Configuración de modos ---
modo_transformacion = 0  # 0=RotX, 1=RotY, 2=RotZ, 3=Tras, 4=Esc, 5=Todo
modos_texto = {
    0: "Modo:  Eje X",
    1: "Modo:  Eje Y",
    2: "Modo:   Z",
    3: "Modo: ",
    4: "Modo: ",
    5: "Modo:  "
}
fuente_ui = pygame.font.SysFont('Arial', 24)

# --- Bucle principal ---
corriendo = True
reloj = pygame.time.Clock()
angulo = 0  # Variable para animar

while corriendo:
    # --- MODIFICADO: Bucle de eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        if event.type == pygame.KEYDOWN:  # <-- NUEVO
            if event.key == pygame.K_RETURN:  # Detectar tecla ENTER
                modo_transformacion = (modo_transformacion + 1) % 6  # Avanza al sig. modo (0-5)

    ventana.fill(NEGRO)

    # 1. --- CREAR MATRICES DE TRANSFORMACIÓN (MODIFICADO) ---

    # Empezamos con matrices de identidad ("sin transformación")
    mat_rot_x = np.identity(4)
    mat_rot_y = np.identity(4)
    mat_rot_z = np.identity(4)
    mat_esc = np.identity(4)
    # Ponemos una traslación base para que el cubo no esté en la cámara
    mat_tras = t3d.crear_matriz_traslacion(0, 0, -5)

    # Aplicamos la transformación según el modo actual
    if modo_transformacion == 0:  # Rotación X
        mat_rot_x = t3d.crear_matriz_rotacion_x(angulo)

    elif modo_transformacion == 1:  # Rotación Y
        mat_rot_y = t3d.crear_matriz_rotacion_y(angulo)

    elif modo_transformacion == 2:  # Rotación Z
        mat_rot_z = t3d.crear_matriz_rotacion_z(angulo)

    elif modo_transformacion == 3:  # Traslación
        tx = math.sin(math.radians(angulo)) * 1.5
        mat_tras = t3d.crear_matriz_traslacion(tx, 0, -5)

    elif modo_transformacion == 4:  # Escalado
        escala_val = 1.0 + (math.sin(math.radians(angulo * 2)) * 0.3)
        mat_esc = t3d.crear_matriz_escalado(escala_val, escala_val, escala_val)

    elif modo_transformacion == 5:  # Todas Combinadas
        mat_rot_x = t3d.crear_matriz_rotacion_x(angulo)
        mat_rot_y = t3d.crear_matriz_rotacion_y(angulo * 0.6)
        mat_rot_z = t3d.crear_matriz_rotacion_z(angulo * 0.3)
        escala_val = 1.0 + (math.sin(math.radians(angulo * 2)) * 0.3)
        mat_esc = t3d.crear_matriz_escalado(escala_val, escala_val, escala_val)
        tx = math.sin(math.radians(angulo)) * 1.5
        mat_tras = t3d.crear_matriz_traslacion(tx, 0, -5)

    # 2. --- COMBINAR MATRICES (Sin cambios) ---
    # Esta parte funciona igual, multiplicará las matrices de identidad
    # (que no hacen nada) por la matriz que sí esté activa.
    mat_rot_total = mat_rot_z.dot(mat_rot_y.dot(mat_rot_x))
    mat_modelo = mat_rot_total.dot(mat_esc)
    mat_final = mat_tras.dot(mat_modelo)

    # 3. --- APLICAR TRANSFORMACIÓN Y PROYECTAR (Sin cambios) ---
    vertices_transformados = {}
    for nombre, vertice in vertices_3d_originales.items():
        vertices_transformados[nombre] = t3d.aplicar_transformacion(vertice, mat_final)

    vertices_2d_proyectados = {}
    for nombre, coords_3d in vertices_transformados.items():
        coords_2d = proyectar_perspectiva_1punto(coords_3d, distancia_cz)
        screen_x = coords_2d[0] * escala_pantalla + offset_x
        screen_y = -coords_2d[1] * escala_pantalla + offset_y
        vertices_2d_proyectados[nombre] = (screen_x, screen_y)

    # 4. --- DIBUJAR ---
    for arista in aristas:
        p1_coords = vertices_2d_proyectados[arista[0]]
        p2_coords = vertices_2d_proyectados[arista[1]]
        func3d.dibujar_linea_2d(p1_coords[0], p1_coords[1], p2_coords[0], p2_coords[1], BLANCO)

    for nombre, coords_2d in vertices_2d_proyectados.items():
        func3d.dibujar_pixel_2d(coords_2d[0], coords_2d[1], ROJO, grosor=5)

    # --- NUEVO: Dibujar texto de UI ---
    texto_modo = fuente_ui.render(modos_texto[modo_transformacion], True, BLANCO)
    ventana.blit(texto_modo, (10, 10))

    texto_instruccion = fuente_ui.render("Presiona ENTER para cambiar", True, GRIS)
    ventana.blit(texto_instruccion, (10, 40))

    # 5. --- ACTUALIZAR ---
    angulo += 1  # Aumentamos el ángulo para la animación

    pygame.display.update()
    reloj.tick(60)  # Limitar a 60 FPS

pygame.quit()