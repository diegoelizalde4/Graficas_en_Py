
import pygame
import math


class Funcion3d:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ancho, self.alto = ventana.get_size()

    # --- Primitivas de Dibujo 2D ---
    def dibujar_pixel_2d(self, x, y, color, grosor=1):
        centro_offset = grosor // 2
        px, py = int(x - centro_offset), int(y - centro_offset)
        for i in range(grosor):
            for j in range(grosor):
                if 0 <= px + i < self.ancho and 0 <= py + j < self.alto:
                    self.ventana.set_at((px + i, py + j), color)

    def dibujar_linea_2d(self, xi, yi, xf, yf, color):
        dx, dy = xf - xi, yf - yi
        if dx == 0 and dy == 0:
            self.dibujar_pixel_2d(round(xi), round(yi), color)
            return
        pasos = max(abs(dx), abs(dy))
        if pasos == 0: return
        xinc, yinc = dx / pasos, dy / pasos
        x, y = xi, yi
        for _ in range(int(pasos) + 1):
            self.dibujar_pixel_2d(round(x), round(y), color)
            x += xinc
            y += yinc

    # --- Proyección y Ejes 3D ---
    def _proyectar_3d(self, x, y, z, origen_x, origen_y, escala_xy, escala_z, angulo_oblicuo=0.785):
        factor_profundidad = 0.5
        screen_x = x * escala_xy + (y * escala_xy * factor_profundidad * math.cos(angulo_oblicuo)) + origen_x
        screen_y = -z * escala_z - (y * escala_xy * factor_profundidad * math.sin(angulo_oblicuo)) + origen_y
        return screen_x, screen_y

    def dibujar_ejes_3d(self, origen_x, origen_y, longitud_eje, color):
        p_z_inicio, p_z_fin = (origen_x, origen_y), (origen_x, origen_y - longitud_eje)
        self.dibujar_linea_2d(p_z_inicio[0], p_z_inicio[1], p_z_fin[0], p_z_fin[1], color)
        p_x_inicio = (origen_x, origen_y);
        p_x_fin, _ = self._proyectar_3d(longitud_eje, 0, 0, origen_x, origen_y, 1, 1)
        self.dibujar_linea_2d(p_x_inicio[0], p_x_inicio[1], p_x_fin, p_x_inicio[1], color)
        p_y_inicio = (origen_x, origen_y);
        p_y_fin_x, p_y_fin_y = self._proyectar_3d(0, longitud_eje, 0, origen_x, origen_y, 1, 1)
        self.dibujar_linea_2d(p_y_inicio[0], p_y_inicio[1], p_y_fin_x, p_y_fin_y, color)

    # --- Dibujo de Figuras 3D (Curvas paramétricas 3D) ---
    def dibujar_espiral_3d(self, origen_x, origen_y, escala_xy, escala_z, color_linea, color_nodo, segmentos=500):
        puntos_2d = [];
        t_inicio, t_fin = 0, 8 * math.pi
        for i in range(segmentos + 1):
            t = t_inicio + (t_fin - t_inicio) * i / segmentos
            x, y, z = math.cos(t), math.sin(t), t
            screen_x, screen_y = self._proyectar_3d(x, y, z, origen_x, origen_y, escala_xy, escala_z)
            puntos_2d.append((screen_x, screen_y))
        for i in range(len(puntos_2d) - 1):
            self.dibujar_linea_2d(puntos_2d[i][0], puntos_2d[i][1], puntos_2d[i + 1][0], puntos_2d[i + 1][1],
                                  color_linea)
        num_nodos = 80
        for i in range(num_nodos + 1):
            t = t_inicio + (t_fin - t_inicio) * i / num_nodos
            x, y, z = math.cos(t), math.sin(t), t
            screen_x, screen_y = self._proyectar_3d(x, y, z, origen_x, origen_y, escala_xy, escala_z)
            self.dibujar_pixel_2d(screen_x, screen_y, color_nodo, grosor=4)

    def dibujar_curva_trebol_3d(self, origen_x, origen_y, escala_xy, escala_z, color_linea, segmentos=500):
        puntos_2d = [];
        t_inicio, t_fin = -math.pi, math.pi
        for i in range(segmentos + 1):
            t = t_inicio + (t_fin - t_inicio) * i / segmentos
            x, y, z = math.cos(3 * t), 2 * (math.cos(t) ** 2), math.sin(2 * t)
            screen_x, screen_y = self._proyectar_3d(x, y, z, origen_x, origen_y, escala_xy, escala_z)
            puntos_2d.append((screen_x, screen_y))
        for i in range(len(puntos_2d) - 1):
            self.dibujar_linea_2d(puntos_2d[i][0], puntos_2d[i][1], puntos_2d[i + 1][0], puntos_2d[i + 1][1],
                                  color_linea)

    # --- Adaptación de Figuras 2D a 3D (en plano Z=0) ---

    def dibujar_curva_hipotrocoide_3d(self, origen_x_2d, origen_y_2d, escala_xy, escala_z, color, segmentos=1000):
        puntos_2d_proyectados = []
        for i in range(segmentos + 1):
            t = 14 * math.pi * i / segmentos  # Rango [0, 14π]
            # Coordenadas 3D (z=0)
            x3d = 17 * math.cos(t) + 7 * math.cos((17 / 7) * t)
            y3d = 17 * math.sin(t) - 7 * math.sin((17 / 7) * t)
            z3d = 0

            # Proyectar a 2D
            px, py = self._proyectar_3d(x3d, y3d, z3d, origen_x_2d, origen_y_2d, escala_xy, escala_z)
            puntos_2d_proyectados.append((px, py))

        # Dibujar las líneas conectando los puntos proyectados
        for i in range(len(puntos_2d_proyectados) - 1):
            self.dibujar_linea_2d(puntos_2d_proyectados[i][0], puntos_2d_proyectados[i][1],
                                  puntos_2d_proyectados[i + 1][0], puntos_2d_proyectados[i + 1][1], color)

    def dibujar_curva_compleja_3d(self, origen_x_2d, origen_y_2d, escala_xy, escala_z, color, segmentos=400):
        puntos_2d_proyectados = []
        for i in range(segmentos + 1):
            t = 2 * math.pi * i / segmentos
            x3d = math.cos(t) + (1 / 2) * math.cos(7 * t) + (1 / 3) * math.sin(17 * t)
            y3d = math.sin(t) + (1 / 2) * math.sin(7 * t) + (1 / 3) * math.cos(17 * t)
            z3d = 0
            px, py = self._proyectar_3d(x3d, y3d, z3d, origen_x_2d, origen_y_2d, escala_xy, escala_z)
            puntos_2d_proyectados.append((px, py))
        for i in range(len(puntos_2d_proyectados) - 1):
            self.dibujar_linea_2d(puntos_2d_proyectados[i][0], puntos_2d_proyectados[i][1],
                                  puntos_2d_proyectados[i + 1][0], puntos_2d_proyectados[i + 1][1], color)

    def dibujar_circulo_3d(self, centro_x_3d, centro_y_3d, radio, origen_x_2d, origen_y_2d, escala_xy, escala_z, color,
                           segmentos=44):
        puntos_2d_proyectados = []
        for i in range(segmentos + 1):
            angulo = 2 * math.pi * i / segmentos
            x3d, y3d, z3d = centro_x_3d + radio * math.cos(angulo), centro_y_3d + radio * math.sin(angulo), 0
            px, py = self._proyectar_3d(x3d, y3d, z3d, origen_x_2d, origen_y_2d, escala_xy, escala_z)
            puntos_2d_proyectados.append((px, py))
        for i in range(len(puntos_2d_proyectados) - 1):
            self.dibujar_linea_2d(puntos_2d_proyectados[i][0], puntos_2d_proyectados[i][1],
                                  puntos_2d_proyectados[i + 1][0], puntos_2d_proyectados[i + 1][1], color)

    def dibujar_cuadrado_3d(self, x1_3d, y1_3d, x2_3d, y2_3d, origen_x_2d, origen_y_2d, escala_xy, escala_z, color):
        z3d = 0
        puntos_3d = [(x1_3d, y1_3d, z3d), (x2_3d, y1_3d, z3d), (x2_3d, y2_3d, z3d), (x1_3d, y2_3d, z3d)]
        puntos_2d = [self._proyectar_3d(p[0], p[1], p[2], origen_x_2d, origen_y_2d, escala_xy, escala_z) for p in
                     puntos_3d]
        for i in range(len(puntos_2d)):
            self.dibujar_linea_2d(puntos_2d[i][0], puntos_2d[i][1], puntos_2d[(i + 1) % len(puntos_2d)][0],
                                  puntos_2d[(i + 1) % len(puntos_2d)][1], color)

