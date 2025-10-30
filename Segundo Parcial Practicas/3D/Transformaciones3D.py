# Transformaciones3D.py
import numpy as np
import math



def crear_matriz_traslacion(tx, ty, tz):
    """
    Crea una matriz de traslación 4x4.
    [cite_start]Basado en 'Traslación' (página 2)[cite: 13].
    """
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ], dtype=float)


def crear_matriz_escalado(sx, sy, sz):
    """
    Crea una matriz de escalado 4x4.
    [cite_start]Basado en 'Escalar' (página 3)[cite: 17].
    """
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def crear_matriz_rotacion_x(angulo_grados):
    """
    Crea una matriz de rotación 4x4 alrededor del eje X.
    [cite_start]Usamos las ecuaciones de 'Rotación X' (página 5) [cite: 30, 32]
    [cite_start]ya que la matriz en la página 4 [cite: 21] tiene los signos de seno invertidos
    (probablemente para una convención de rotación horaria).
    """
    angulo_rad = math.radians(angulo_grados)
    cos_a = math.cos(angulo_rad)
    sin_a = math.sin(angulo_rad)

    # [cite_start]Ecuaciones de Pág 5[cite: 32]:
    # y' = y*cos(θ) - z*sin(θ)
    # z' = y*sin(θ) + z*cos(θ)
    return np.array([
        [1, 0, 0, 0],
        [0, cos_a, -sin_a, 0],
        [0, sin_a, cos_a, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def crear_matriz_rotacion_y(angulo_grados):
    """
    Crea una matriz de rotación 4x4 alrededor del eje Y.
    [cite_start]Usamos las ecuaciones de 'Rotación Y' (página 6)[cite: 37, 40].
    """
    angulo_rad = math.radians(angulo_grados)
    cos_a = math.cos(angulo_rad)
    sin_a = math.sin(angulo_rad)

    # [cite_start]Ecuaciones de Pág 6[cite: 37, 40]:
    # x' = x*cos(θ) + z*sin(θ)
    # z' = -x*sin(θ) + z*cos(θ)
    return np.array([
        [cos_a, 0, sin_a, 0],
        [0, 1, 0, 0],
        [-sin_a, 0, cos_a, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def crear_matriz_rotacion_z(angulo_grados):
    """
    Crea una matriz de rotación 4x4 alrededor del eje Z.
    [cite_start]Usamos las ecuaciones de 'Rotación Z' (página 7)[cite: 46].
    """
    angulo_rad = math.radians(angulo_grados)
    cos_a = math.cos(angulo_rad)
    sin_a = math.sin(angulo_rad)

    # [cite_start]Ecuaciones de Pág 7[cite: 46]:
    # x' = x*cos(θ) - y*sin(θ)
    # y' = x*sin(θ) + y*cos(θ)
    return np.array([
        [cos_a, -sin_a, 0, 0],
        [sin_a, cos_a, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def aplicar_transformacion(vertice_3d, matriz):
    """
    Aplica una matriz de transformación 4x4 a un vértice 3D (x, y, z).
    """
    # Convertir el vértice (x, y, z) a un vector columna homogéneo [x, y, z, 1]
    vertice_homogeneo = np.array([vertice_3d[0], vertice_3d[1], vertice_3d[2], 1.0])

    # Aplicar la transformación: P' = M * P
    vertice_transformado = matriz.dot(vertice_homogeneo)

    # Convertir de nuevo a coordenadas 3D (x, y, z)
    # (Ignoramos la 'w' que debería ser 1)
    return (vertice_transformado[0], vertice_transformado[1], vertice_transformado[2])