# demo_superficie_corregido.py
import pygame
from Funcion3d import Funcion3d
import Transformaciones3D as t3d
import math
import sys
import numpy as np

sys.setrecursionlimit(2000)


# --- NUEVA FUNCIÓN DE PROYECCIÓN DE PERSPECTIVA ---
def proyectar_perspectiva_nueva(punto_3d, d_plano):

    x, y, z = punto_3d

    # (Asumimos que la cámara está en 0,0,0 y mira hacia -Z)
    if z >= -0.001:
        return None

    # Fórmula de proyección: xp = d * x / (-z)
    factor_perspectiva = d_plano / (-z)

    x_p = x * factor_perspectiva
    y_p = y * factor_perspectiva

    return (x_p, y_p)



def generar_superficie_param_puntos(num_t_steps, num_phi_steps, t_min, t_max, phi_min, phi_max):
    grid_vertices = []
    t_range = np.linspace(t_min, t_max, num_t_steps)
    phi_range = np.linspace(phi_min, phi_max, num_phi_steps)

    max_z = t_max  # 'z_orig' (t_val)
    min_z = t_min

    for i, t_val in enumerate(t_range):
        row_vertices = []
        for j, phi_val in enumerate(phi_range):
            # El radio sigue dependiendo de 't'
            radio = 2 - math.cos(t_val)

            # El círculo se forma en el plano XZ
            x = radio * math.cos(phi_val)
            y = t_val
            z = radio * math.sin(phi_val)

            # Centrar Y
            y_centrada = y - (t_max + t_min) / 2.0


            # (x, y_centrada, z) se usa para la posición
            row_vertices.append({'coords': (x, y_centrada, z), 'z_orig': t_val})
        grid_vertices.append(row_vertices)

    return grid_vertices, min_z, max_z


# --- GENERACIÓN DE CARAS
def generar_caras_desde_grid(grid_vertices, min_z, max_z):
    caras_a_dibujar = []
    num_t_steps = len(grid_vertices)
    num_phi_steps = len(grid_vertices[0]) if num_t_steps > 0 else 0

    if num_t_steps < 2 or num_phi_steps < 2:
        return []

    for i in range(num_t_steps - 1):
        for j in range(num_phi_steps - 1):
            p1 = grid_vertices[i][j]['coords']
            p2 = grid_vertices[i][j + 1]['coords']
            p3 = grid_vertices[i + 1][j + 1]['coords']
            p4 = grid_vertices[i + 1][j]['coords']

            z_color_ref = grid_vertices[i][j]['z_orig']

            # Calcular color (gradiente de Azul a Rojo)
            normalized_z = (z_color_ref - min_z) / (max_z - min_z) if (max_z - min_z) != 0 else 0.5
            r = int(255 * normalized_z)
            g = 0
            b = int(255 * (1 - normalized_z))
            color_interpolado = (max(0, min(r, 255)), 0, max(0, min(b, 255)))  # Asegurar rango 0-255

            # Dividir en dos triángulos
            caras_a_dibujar.append({'vertices': [p1, p2, p3], 'color': color_interpolado})
            caras_a_dibujar.append({'vertices': [p1, p3, p4], 'color': color_interpolado})

    return caras_a_dibujar


# --- Parámetros de la superficie ---
num_t_steps = 40
num_phi_steps = 40
t_min = -3.0
t_max = 3.0
phi_min = 0.0
phi_max = 2 * math.pi

# Generar los vértices y las caras
grid_vertices_raw, min_z_global, max_z_global = generar_superficie_param_puntos(
    num_t_steps, num_phi_steps, t_min, t_max, phi_min, phi_max
)
caras_originales = generar_caras_desde_grid(grid_vertices_raw, min_z_global, max_z_global)


distancia_plano_proyeccion = 2.5  # <-- Ajusta esto para más/menos perspectiva

# --- Inicializar Pygame ---
pygame.init()
pygame.font.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Proyecto Graficas")
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
func3d = Funcion3d(ventana)

# --- Configuración de visualización ---
escala_pantalla = 50
offset_x = 400
offset_y = 300

# --- Bucle principal ---
corriendo = True
reloj = pygame.time.Clock()
angulo = 0
modo_transformacion = 0
modos_texto = {
    0: "",
    1: "",
    2: "",
    3: "",
    4: "",
    5: ""
}
fuente_ui = pygame.font.SysFont('Arial', 12)
GRIS = (150, 150, 150)

while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                modo_transformacion = (modo_transformacion + 1) % 6

    ventana.fill(NEGRO)

    # 1. --- CREAR MATRICES DE TRANSFORMACIÓN ---
    mat_rot_x = np.identity(4)
    mat_rot_y = np.identity(4)
    mat_rot_z = np.identity(4)
    mat_esc = np.identity(4)
    # Trasladamos la figura más lejos en Z para que la cámara la vea
    mat_tras = t3d.crear_matriz_traslacion(0, 0, -8)

    if modo_transformacion == 0:
        mat_rot_x = t3d.crear_matriz_rotacion_x(angulo)
    elif modo_transformacion == 1:
        mat_rot_y = t3d.crear_matriz_rotacion_y(angulo)
    elif modo_transformacion == 2:
        mat_rot_z = t3d.crear_matriz_rotacion_z(angulo)
    elif modo_transformacion == 3:
        tx = math.sin(math.radians(angulo)) * 1.5
        mat_tras = t3d.crear_matriz_traslacion(tx, 0, -8)
    elif modo_transformacion == 4:
        escala_val = 0.8 + (math.sin(math.radians(angulo * 2)) * 0.2)
        mat_esc = t3d.crear_matriz_escalado(escala_val, escala_val, escala_val)
    elif modo_transformacion == 5:
        mat_rot_x = t3d.crear_matriz_rotacion_x(angulo)
        mat_rot_y = t3d.crear_matriz_rotacion_y(angulo * 0.6)
        mat_rot_z = t3d.crear_matriz_rotacion_z(angulo * 0.3)
        escala_val = 0.8 + (math.sin(math.radians(angulo * 2)) * 0.2)
        mat_esc = t3d.crear_matriz_escalado(escala_val, escala_val, escala_val)
        tx = math.sin(math.radians(angulo)) * 1.5
        mat_tras = t3d.crear_matriz_traslacion(tx, 0, -8)

    # 2. --- COMBINAR MATRICES ---
    mat_rot_total = mat_rot_z.dot(mat_rot_y.dot(mat_rot_x))
    mat_modelo = mat_rot_total.dot(mat_esc)
    mat_final = mat_tras.dot(mat_modelo)

    # 3. --- PROCESAR CARAS
    triangulos_para_dibujar = []
    for cara_info in caras_originales:
        vertices_3d_original_cara = cara_info['vertices']
        color_cara = cara_info['color']

        # Transformar los 3 vértices
        vertices_transformados = []
        z_sum = 0
        for vertice_3d_orig in vertices_3d_original_cara:
            vert_trans = t3d.aplicar_transformacion(vertice_3d_orig, mat_final)
            vertices_transformados.append(vert_trans)
            z_sum += vert_trans[2]  # Sumar Z para el Z-sort

        avg_z = z_sum / 3

        # Proyectar los 3 vértices a 2D
        vertices_2d_proyectados_cara = []
        triangulo_es_visible = True
        for vertice_trans in vertices_transformados:

            coords_2d = proyectar_perspectiva_nueva(vertice_trans, distancia_plano_proyeccion)

            if coords_2d is None:
                triangulo_es_visible = False  # Si un vértice está detrás de la cámara, no dibujamos
                break

            screen_x = coords_2d[0] * escala_pantalla + offset_x
            screen_y = -coords_2d[1] * escala_pantalla + offset_y
            vertices_2d_proyectados_cara.append((screen_x, screen_y))

        if triangulo_es_visible:
            triangulos_para_dibujar.append({
                'vertices_2d': vertices_2d_proyectados_cara,
                'color': color_cara,
                'avg_z': avg_z
            })

    # Ordenar de más lejos (Z mayor negativo) a más cerca (Z menor negativo)
    triangulos_para_dibujar.sort(key=lambda x: x['avg_z'])

    # 4. --- DIBUJAR LOS TRIÁNGULOS (rellenos) ---
    for triangulo in triangulos_para_dibujar:
        # Evitar polígonos inválidos (puntos colineales/demasiado pequeños)
        if len(triangulo['vertices_2d']) == 3:
            pygame.draw.polygon(ventana, triangulo['color'], triangulo['vertices_2d'])

    # --- Dibujar texto de UI ---
    texto_modo = fuente_ui.render(modos_texto[modo_transformacion], True, BLANCO)
    ventana.blit(texto_modo, (10, 10))
    texto_instruccion = fuente_ui.render("", True, GRIS)
    ventana.blit(texto_instruccion, (10, 40))

    # 5. --- ACTUALIZAR ---
    angulo += 1
    pygame.display.update()
    reloj.tick(60)

pygame.quit()