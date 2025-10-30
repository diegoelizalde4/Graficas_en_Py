# EnmalladoUniforme.py
import pygame
from Funciones import Funciones
import sys

sys.setrecursionlimit(2000)


# --- Función para obtener y procesar la entrada del usuario ---
def obtener_puntos_desde_consola(nombre_conjunto):
    """Pide al usuario una lista de números y la devuelve como una lista de strings."""
    while True:
        entrada_str = input(f"Ingrese los puntos para el conjunto {nombre_conjunto} (separados por comas): ")
        if not entrada_str:
            print("La entrada no puede estar vacía. Intente de nuevo.")
            continue
        # Simplemente separamos los puntos, no necesitamos convertirlos a número
        puntos = [punto.strip() for punto in entrada_str.split(',')]
        return puntos


# --- Pedir datos al usuario ---
print("--- Creación de Malla Uniforme ---")
puntos_a = obtener_puntos_desde_consola("A(x)")
puntos_b = obtener_puntos_desde_consola("B(y)")

# --- Inicializar Pygame ---
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Enmallado Uniforme")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Crear objeto Funciones
func = Funciones(ventana)

# --- Configuración de la malla ---
# Posición inicial y tamaño de cada celda
pos_x_inicial = 50
pos_y_inicial = 50
ancho_celda = 60
alto_celda = 40

# Bucle principal
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    ventana.fill(NEGRO)

    # Dibujar la malla uniforme
    func.dibujar_malla_uniforme(
        puntos_x=puntos_a,
        puntos_y=puntos_b,
        x_start=pos_x_inicial,
        y_start=pos_y_inicial,
        ancho_celda=ancho_celda,
        alto_celda=alto_celda,
        color_linea=BLANCO,
        color_nodo=ROJO
    )

    pygame.display.update()

pygame.quit()