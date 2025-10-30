import pygame
import math
import threading


class Funciones:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ancho, self.alto = ventana.get_size()

    # --- Métodos de Dibujo de Primitivas ---
    def dibujar_pixel(self, x, y, color, grosor=1):
        centro_offset = grosor // 2
        px, py = int(x - centro_offset), int(y - centro_offset)
        for i in range(grosor):
            for j in range(grosor):
                if 0 <= px + i < self.ancho and 0 <= py + j < self.alto:
                    self.ventana.set_at((px + i, py + j), color)

    def dibujar_lineada(self, xi, yi, xf, yf, color):
        dx, dy = xf - xi, yf - yi
        if dx == 0 and dy == 0:
            self.dibujar_pixel(round(xi), round(yi), color)
            return
        pasos = max(abs(dx), abs(dy))
        if pasos == 0: return
        xinc, yinc = dx / pasos, dy / pasos
        x, y = xi, yi
        for _ in range(int(pasos) + 1):
            self.dibujar_pixel(round(x), round(y), color)
            x += xinc
            y += yinc

    # --- Funciones de Enmallado ---
    def dibujar_malla_uniforme(self, puntos_x, puntos_y, x_start, y_start, ancho_celda, alto_celda, color_linea,
                               color_nodo):
        if not puntos_x or not puntos_y: return
        num_puntos_x, num_puntos_y = len(puntos_x), len(puntos_y)
        x_end, y_end = x_start + (num_puntos_x - 1) * ancho_celda, y_start + (num_puntos_y - 1) * alto_celda
        for i in range(num_puntos_y):
            y = y_start + i * alto_celda
            self.dibujar_lineada(x_start, y, x_end, y, color_linea)
        for i in range(num_puntos_x):
            x = x_start + i * ancho_celda
            self.dibujar_lineada(x, y_start, x, y_end, color_linea)
        for i in range(num_puntos_x):
            for j in range(num_puntos_y):
                x_nodo, y_nodo = x_start + i * ancho_celda, y_start + j * alto_celda
                self.dibujar_pixel(x_nodo, y_nodo, color_nodo, grosor=5)

    def dibujar_malla_cartesiana(self, puntos_x, puntos_y, escala, offset_x, offset_y, color_linea, color_nodo):
        if not puntos_x or not puntos_y: return

        def transformar(punto):
            x, y = punto;
            tx, ty = x * escala + offset_x, -y * escala + offset_y
            return tx, ty

        x_min, x_max = min(puntos_x), max(puntos_x)
        for y_val in puntos_y:
            p_inicio, p_fin = transformar((x_min, y_val)), transformar((x_max, y_val))
            self.dibujar_lineada(p_inicio[0], p_inicio[1], p_fin[0], p_fin[1], color_linea)
        y_min, y_max = min(puntos_y), max(puntos_y)
        for x_val in puntos_x:
            p_inicio, p_fin = transformar((x_val, y_min)), transformar((x_val, y_max))
            self.dibujar_lineada(p_inicio[0], p_inicio[1], p_fin[0], p_fin[1], color_linea)
        for x_val in puntos_x:
            for y_val in puntos_y:
                nodo = transformar((x_val, y_val))
                self.dibujar_pixel(nodo[0], nodo[1], color_nodo, grosor=5)

    # --- Función para graficar puntos ---
    def dibujar_puntos_conectados(self, puntos_lista, color, escala_x=1, escala_y=1, offset_x=0, offset_y=0,
                                  dibujar_puntos_individuales=False, color_puntos_individuales=(255, 0, 0),
                                  grosor_punto=3):
        if not puntos_lista: return
        puntos_transformados = []
        for x, y in puntos_lista:
            tx, ty = x * escala_x + offset_x, y * escala_y + offset_y
            puntos_transformados.append((tx, ty))
            if dibujar_puntos_individuales:
                self.dibujar_pixel(tx, ty, color_puntos_individuales, grosor=grosor_punto)
        for i in range(len(puntos_transformados) - 1):
            p1, p2 = puntos_transformados[i], puntos_transformados[i + 1]
            self.dibujar_lineada(p1[0], p1[1], p2[0], p2[1], color)

    # --- Algoritmos de Relleno ---
    def relleno_por_inundacion(self, x, y, color_relleno, color_borde):
        if not (0 <= x < self.ancho and 0 <= y < self.alto): return
        color_actual = self.ventana.get_at((x, y))
        if color_actual != color_borde and color_actual != color_relleno:
            self.dibujar_pixel(x, y, color_relleno)
            self.relleno_por_inundacion(x + 1, y, color_relleno, color_borde)
            self.relleno_por_inundacion(x - 1, y, color_relleno, color_borde)
            self.relleno_por_inundacion(x, y + 1, color_relleno, color_borde)
            self.relleno_por_inundacion(x, y - 1, color_relleno, color_borde)

    def relleno_scanline(self, vertices, color):
        if not vertices: return
        y_min, y_max = int(min(v[1] for v in vertices)), int(max(v[1] for v in vertices))
        for y in range(y_min, y_max + 1):
            intersecciones = []
            for i in range(len(vertices)):
                p1, p2 = vertices[i], vertices[(i + 1) % len(vertices)]
                if p1[1] != p2[1]:
                    if min(p1[1], p2[1]) <= y < max(p1[1], p2[1]):
                        x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                        intersecciones.append(x)
            intersecciones.sort()
            for i in range(0, len(intersecciones), 2):
                if i + 1 < len(intersecciones):
                    x_start, x_end = math.ceil(intersecciones[i]), math.floor(intersecciones[i + 1])
                    for x in range(x_start, x_end + 1):
                        self.dibujar_pixel(x, y, color)

    # --- Métodos para Obtener Vértices ---
    def obtener_vertices_hexagono(self, x, y, radio, escala):
        x_esc, y_esc = x * escala, y * escala;
        r = radio * escala;
        vertices = []
        for i in range(6):
            angulo = i * math.pi / 3;
            vx, vy = x_esc + r * math.cos(angulo), y_esc + r * math.sin(angulo)
            vertices.append((vx, vy))
        return vertices

    def obtener_vertices_octagono(self, centro_x, centro_y, radio, escala):
        cx, cy = centro_x * escala, centro_y * escala;
        r = radio * escala;
        puntos = []
        for i in range(8):
            angulo = 2 * math.pi * i / 8;
            x, y = cx + r * math.cos(angulo), cy + r * math.sin(angulo)
            puntos.append((x, y))
        return puntos

    # --- Dibujo de Figuras Geométricas ---
    def dibujar_curva_parametrica(self, offset_x, offset_y, escala, color, segmentos=500):
        puntos = []
        t_inicio, t_fin = 0, 10
        for i in range(segmentos + 1):
            t = t_inicio + (t_fin - t_inicio) * i / segmentos
            x, y = t - 3 * math.sin(t), 4 - 3 * math.cos(t)
            px, py = x * escala + offset_x, -y * escala + offset_y
            puntos.append((px, py))
        for i in range(len(puntos) - 1):
            self.dibujar_lineada(puntos[i][0], puntos[i][1], puntos[i + 1][0], puntos[i + 1][1], color)

    def dibujar_curva_compleja(self, centro_x, centro_y, escala, color, segmentos=400):
        puntos = []
        for i in range(segmentos + 1):
            t = 2 * math.pi * i / segmentos
            x = math.cos(t) + (1 / 2) * math.cos(7 * t) + (1 / 3) * math.sin(17 * t)
            y = math.sin(t) + (1 / 2) * math.sin(7 * t) + (1 / 3) * math.cos(17 * t)
            px, py = x * escala + centro_x, y * escala + centro_y
            puntos.append((px, py))
        for i in range(len(puntos) - 1):
            self.dibujar_lineada(puntos[i][0], puntos[i][1], puntos[i + 1][0], puntos[i + 1][1], color)

    def dibujar_curva_hipotrocoide(self, centro_x, centro_y, escala, color, segmentos=1000):
        puntos = []
        for i in range(segmentos + 1):
            t = 14 * math.pi * i / segmentos
            x = 17 * math.cos(t) + 7 * math.cos((17 / 7) * t)
            y = 17 * math.sin(t) - 7 * math.sin((17 / 7) * t)
            px, py = x * escala + centro_x, y * escala + centro_y
            puntos.append((px, py))
        for i in range(len(puntos) - 1):
            self.dibujar_lineada(puntos[i][0], puntos[i][1], puntos[i + 1][0], puntos[i + 1][1], color)

    def dibujar_cuadrado(self, x1, y1, x2, y2, escala, color):
        x1_esc, y1_esc = x1 * escala, y1 * escala;
        x2_esc, y2_esc = x2 * escala, y2 * escala
        x_min, x_max = min(x1_esc, x2_esc), max(x1_esc, x2_esc);
        y_min, y_max = min(y1_esc, y2_esc), max(y1_esc, y2_esc)
        puntos = [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]
        for i in range(len(puntos)):
            self.dibujar_lineada(puntos[i][0], puntos[i][1], puntos[(i + 1) % len(puntos)][0],
                                 puntos[(i + 1) % len(puntos)][1], color)

    def dibujar_triangulo_rectangulo(self, x1, y1, x2, y2, escala, color):
        x1_esc, y1_esc = x1 * escala, y1 * escala;
        x2_esc, y2_esc = x2 * escala, y2 * escala
        x_min, x_max = min(x1_esc, x2_esc), max(x1_esc, x2_esc);
        y_min, y_max = min(y1_esc, y2_esc), max(y1_esc, y2_esc)
        p1, p2, p3 = (x_min, y_max), (x_max, y_max), (x_min, y_min)
        self.dibujar_lineada(p1[0], p1[1], p2[0], p2[1], color)
        self.dibujar_lineada(p2[0], p2[1], p3[0], p3[1], color)
        self.dibujar_lineada(p3[0], p3[1], p1[0], p1[1], color)

    def dibujar_estrella_5_picos(self, x, y, radio_exterior, escala, color):
        x_esc, y_esc = x * escala, y * escala;
        r_ext = radio_exterior * escala;
        r_int = r_ext * 0.5;
        vertices = []
        for i in range(10):
            angulo = i * math.pi / 5
            if i % 2 == 0:
                vx, vy = x_esc + r_ext * math.sin(angulo), y_esc - r_ext * math.cos(angulo)
            else:
                vx, vy = x_esc + r_int * math.sin(angulo), y_esc - r_int * math.cos(angulo)
            vertices.append((vx, vy))
        for i in range(len(vertices)):
            self.dibujar_lineada(round(vertices[i][0]), round(vertices[i][1]),
                                 round(vertices[(i + 1) % len(vertices)][0]),
                                 round(vertices[(i + 1) % len(vertices)][1]), color)

    def dibujar_hexagono(self, x, y, radio, escala, color):
        vertices = self.obtener_vertices_hexagono(x, y, radio, escala)
        for i in range(len(vertices)):
            self.dibujar_lineada(round(vertices[i][0]), round(vertices[i][1]),
                                 round(vertices[(i + 1) % len(vertices)][0]),
                                 round(vertices[(i + 1) % len(vertices)][1]), color)

    def dibujar_octagono(self, centro_x, centro_y, radio, escala, color):
        puntos = self.obtener_vertices_octagono(centro_x, centro_y, radio, escala)
        for i in range(len(puntos)):
            self.dibujar_lineada(round(puntos[i][0]), round(puntos[i][1]), round(puntos[(i + 1) % len(puntos)][0]),
                                 round(puntos[(i + 1) % len(puntos)][1]), color)

    def dibujar_circulo(self, centro_x, centro_y, radio, escala, color, segmentos=44):
        cx, cy = centro_x * escala, centro_y * escala;
        r = radio * escala;
        puntos = []
        for i in range(segmentos):
            angulo = 2 * math.pi * i / segmentos;
            x, y = cx + r * math.cos(angulo), cy + r * math.sin(angulo)
            puntos.append((x, y))
        for i in range(len(puntos)):
            self.dibujar_lineada(round(puntos[i][0]), round(puntos[i][1]), round(puntos[(i + 1) % len(puntos)][0]),
                                 round(puntos[(i + 1) % len(puntos)][1]), color)

    def dibujar_elipse(self, centro_x, centro_y, radio_a, radio_b, escala, color, segmentos=50):
        cx, cy = centro_x * escala, centro_y * escala;
        ra, rb = radio_a * escala, radio_b * escala;
        puntos = []
        for i in range(segmentos):
            angulo = 2 * math.pi * i / segmentos;
            x, y = cx + ra * math.cos(angulo), cy + rb * math.sin(angulo)
            puntos.append((x, y))
        for i in range(len(puntos)):
            self.dibujar_lineada(round(puntos[i][0]), round(puntos[i][1]), round(puntos[(i + 1) % len(puntos)][0]),
                                 round(puntos[(i + 1) % len(puntos)][1]), color)

    def dibujar_infinito(self, centro_x, centro_y, r, color, segmentos=200):
        puntos = []
        for i in range(segmentos + 1):
            t = 2 * math.pi * i / segmentos;
            denominador = 1 + (math.cos(t) ** 2)
            x, y = r * math.sin(t) / denominador, r * math.sin(t) * math.cos(t) / denominador
            puntos.append((x + centro_x, y + centro_y))
        for i in range(len(puntos) - 1):
            self.dibujar_lineada(puntos[i][0], puntos[i][1], puntos[i + 1][0], puntos[i + 1][1], color)

    # --- Dibujo y Proyección 3D ---

    def _proyectar_3d(self, x, y, z, origen_x, origen_y, escala_xy, escala_z, angulo_oblicuo=0.785):
        factor_profundidad = 0.5
        screen_x = x * escala_xy + (y * escala_xy * factor_profundidad * math.cos(angulo_oblicuo)) + origen_x
        screen_y = -z * escala_z - (y * escala_xy * factor_profundidad * math.sin(angulo_oblicuo)) + origen_y
        return screen_x, screen_y

    def dibujar_ejes_3d(self, origen_x, origen_y, longitud_eje, color):
        p_z_inicio, p_z_fin = (origen_x, origen_y), (origen_x, origen_y - longitud_eje)
        self.dibujar_lineada(p_z_inicio[0], p_z_inicio[1], p_z_fin[0], p_z_fin[1], color)
        p_x_inicio = (origen_x, origen_y);
        p_x_fin, _ = self._proyectar_3d(longitud_eje, 0, 0, origen_x, origen_y, 1,
                                        1)  # Proyectar solo para obtener X final
        self.dibujar_lineada(p_x_inicio[0], p_x_inicio[1], p_x_fin, p_x_inicio[1], color)  # Dibujar horizontal en 2D
        p_y_inicio = (origen_x, origen_y);
        p_y_fin_x, p_y_fin_y = self._proyectar_3d(0, longitud_eje, 0, origen_x, origen_y, 1, 1)
        self.dibujar_lineada(p_y_inicio[0], p_y_inicio[1], p_y_fin_x, p_y_fin_y, color)

    def dibujar_espiral_3d(self, origen_x, origen_y, escala_xy, escala_z, color_linea, color_nodo, segmentos=500):
        puntos_2d = [];
        t_inicio, t_fin = 0, 8 * math.pi
        for i in range(segmentos + 1):
            t = t_inicio + (t_fin - t_inicio) * i / segmentos
            x, y, z = math.cos(t), math.sin(t), t
            screen_x, screen_y = self._proyectar_3d(x, y, z, origen_x, origen_y, escala_xy, escala_z)
            puntos_2d.append((screen_x, screen_y))
        for i in range(len(puntos_2d) - 1):
            self.dibujar_lineada(puntos_2d[i][0], puntos_2d[i][1], puntos_2d[i + 1][0], puntos_2d[i + 1][1],
                                 color_linea)
        num_nodos = 80
        for i in range(num_nodos + 1):
            t = t_inicio + (t_fin - t_inicio) * i / num_nodos
            x, y, z = math.cos(t), math.sin(t), t
            screen_x, screen_y = self._proyectar_3d(x, y, z, origen_x, origen_y, escala_xy, escala_z)
            self.dibujar_pixel(screen_x, screen_y, color_nodo, grosor=4)

    def dibujar_curva_trebol_3d(self, origen_x, origen_y, escala_xy, escala_z, color_linea, segmentos=500):
        """
        Dibuja la curva 3D de la Figura 3.13. ¡NUEVA!
        """
        puntos_2d = []
        t_inicio, t_fin = -math.pi, math.pi

        for i in range(segmentos + 1):
            t = t_inicio + (t_fin - t_inicio) * i / segmentos
            # Ecuaciones paramétricas de la Figura 3.13
            x = math.cos(3 * t)
            y = 2 * (math.cos(t) ** 2)
            z = math.sin(2 * t)

            # Proyectar 3D a 2D y añadir a la lista
            screen_x, screen_y = self._proyectar_3d(x, y, z, origen_x, origen_y, escala_xy, escala_z)
            puntos_2d.append((screen_x, screen_y))

        # Dibujar líneas conectando los puntos
        for i in range(len(puntos_2d) - 1):
            self.dibujar_lineada(puntos_2d[i][0], puntos_2d[i][1], puntos_2d[i + 1][0], puntos_2d[i + 1][1],
                                 color_linea)

    # --- Transformaciones Geométricas 2D ---
    def rotar_punto(self, x, y, cx, cy, angulo):
        x_temp, y_temp = x - cx, y - cy
        x_rotado = x_temp * math.cos(angulo) - y_temp * math.sin(angulo)
        y_rotado = x_temp * math.sin(angulo) + y_temp * math.cos(angulo)
        x_final, y_final = x_rotado + cx, y_rotado + cy
        return x_final, y_final

    def dibujar_cuadrado_rotado(self, x1, y1, x2, y2, angulo, color):
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        puntos = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        puntos_rotados = [self.rotar_punto(px, py, cx, cy, angulo) for (px, py) in puntos]
        for i in range(len(puntos_rotados)):
            self.dibujar_lineada(puntos_rotados[i][0], puntos_rotados[i][1],
                                 puntos_rotados[(i + 1) % len(puntos_rotados)][0],
                                 puntos_rotados[(i + 1) % len(puntos_rotados)][1], color)

    def trasladar_punto(self, x, y, tx, ty):
        return x + tx, y + ty

    def dibujar_cuadrado_trasladado(self, x1, y1, x2, y2, tx, ty, color):
        puntos = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        puntos_trasladados = [self.trasladar_punto(x, y, tx, ty) for (x, y) in puntos]
        for i in range(len(puntos_trasladados)):
            self.dibujar_lineada(puntos_trasladados[i][0], puntos_trasladados[i][1],
                                 puntos_trasladados[(i + 1) % len(puntos_trasladados)][0],
                                 puntos_trasladados[(i + 1) % len(puntos_trasladados)][1], color)

    def escalar_punto(self, x, y, sx, sy):
        return x * sx, y * sy

    def dibujar_cuadrado_escalado(self, x1, y1, x2, y2, sx, sy, color):
        puntos = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        puntos_escalados = [self.escalar_punto(x, y, sx, sy) for (x, y) in puntos]
        for i in range(len(puntos_escalados)):
            self.dibujar_lineada(puntos_escalados[i][0], puntos_escalados[i][1],
                                 puntos_escalados[(i + 1) % len(puntos_escalados)][0],
                                 puntos_escalados[(i + 1) % len(puntos_escalados)][1], color)

    def _rellenar_region(self, pxarray, x1, y1, x2, y2, color):
        for x in range(x1, x2):
            for y in range(y1, y2):
                pxarray[x, y] = color

    def rellenar_cuadro_con_hilos(self, x1, y1, x2, y2, color, num_hilos=4):
        pxarray = pygame.PixelArray(self.ventana)
        x_min, x_max = min(x1, x2), max(x1, x2);
        y_min, y_max = min(y1, y2), max(y1, y2)
        alto = y_max - y_min;
        franja = max(1, alto // num_hilos);
        hilos = []
        for i in range(num_hilos):
            y_inicio = y_min + i * franja;
            y_fin = y_min + (i + 1) * franja if i < num_hilos - 1 else y_max
            hilo = threading.Thread(target=self._rellenar_region, args=(pxarray, x_min, y_inicio, x_max, y_fin, color))
            hilos.append(hilo);
            hilo.start()
        for hilo in hilos: hilo.join()
        del pxarray