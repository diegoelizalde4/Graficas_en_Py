# Transformaciones3D.py
import numpy as np
import math



def crear_matriz_traslacion(tx, ty, tz):

    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ], dtype=float)


def crear_matriz_escalado(sx, sy, sz):

    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def crear_matriz_rotacion_x(angulo_grados):

    angulo_rad = math.radians(angulo_grados)
    cos_a = math.cos(angulo_rad)
    sin_a = math.sin(angulo_rad)

    # y' = y*cos(θ) - z*sin(θ)
    # z' = y*sin(θ) + z*cos(θ)
    return np.array([
        [1, 0, 0, 0],
        [0, cos_a, -sin_a, 0],
        [0, sin_a, cos_a, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def crear_matriz_rotacion_y(angulo_grados):

    angulo_rad = math.radians(angulo_grados)
    cos_a = math.cos(angulo_rad)
    sin_a = math.sin(angulo_rad)

    # x' = x*cos(θ) + z*sin(θ)
    # z' = -x*sin(θ) + z*cos(θ)
    return np.array([
        [cos_a, 0, sin_a, 0],
        [0, 1, 0, 0],
        [-sin_a, 0, cos_a, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def crear_matriz_rotacion_z(angulo_grados):

    angulo_rad = math.radians(angulo_grados)
    cos_a = math.cos(angulo_rad)
    sin_a = math.sin(angulo_rad)

    # x' = x*cos(θ) - y*sin(θ)
    # y' = x*sin(θ) + y*cos(θ)
    return np.array([
        [cos_a, -sin_a, 0, 0],
        [sin_a, cos_a, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def aplicar_transformacion(vertice_3d, matriz):

    # Convertir el vértice (x, y, z) a un vector columna homogéneo [x, y, z, 1]
    vertice_homogeneo = np.array([vertice_3d[0], vertice_3d[1], vertice_3d[2], 1.0])

    # Aplicar la transformación: P' = M * P
    vertice_transformado = matriz.dot(vertice_homogeneo)

    # Convertir de nuevo a coordenadas 3D (x, y, z)
    # (Ignoramos la 'w' que debería ser 1)
    return (vertice_transformado[0], vertice_transformado[1], vertice_transformado[2])