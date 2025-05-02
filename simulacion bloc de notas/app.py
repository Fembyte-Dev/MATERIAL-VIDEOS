import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from numba import jit
import time

# Configuración del fractal
WIDTH, HEIGHT = 1920, 1080  # Resolución Full HD
MAX_ITER = 256              # Número máximo de iteraciones
ZOOM = 1.0                  # Nivel de zoom inicial
X_OFFSET = -0.5             # Desplazamiento en el eje X
Y_OFFSET = 0.0              # Desplazamiento en el eje Y

# Paleta de colores personalizada (puedes modificarla)
colors = [
    (0, 0, 0.3),       # Azul muy oscuro
    (0, 0, 1),         # Azul
    (0, 1, 1),         # Cyan
    (0.5, 1, 0.5),     # Verde claro
    (1, 1, 0),         # Amarillo
    (1, 0.5, 0),       # Naranja
    (1, 0, 0),         # Rojo
    (0.5, 0, 0),       # Rojo oscuro
    (0.5, 0, 0.5),     # Púrpura
    (1, 1, 1)          # Blanco (para el centro)
]
cmap = LinearSegmentedColormap.from_list('mandelbrot', colors)

@jit(nopython=True)  # Aceleración con Numba
def mandelbrot(c, max_iter):
    z = 0j
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

@jit(nopython=True)  # Aceleración con Numba
def create_fractal(width, height, zoom, x_offset, y_offset, max_iter):
    fractal = np.zeros((height, width))
    for x in range(width):
        for y in range(height):
            # Convertir coordenadas de píxel a coordenadas complejas
            zx = 1.5 * (x - width / 2) / (0.5 * zoom * width) + x_offset
            zy = (y - height / 2) / (0.5 * zoom * height) + y_offset
            c = complex(zx, zy)
            fractal[y, x] = mandelbrot(c, max_iter)
    return fractal

def plot_fractal(fractal, cmap, save=False):
    plt.figure(figsize=(16, 9), dpi=120)
    plt.imshow(fractal, cmap=cmap, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"Conjunto de Mandelbrot - Iteraciones: {MAX_ITER} - Zoom: {ZOOM}x", 
              color='white', pad=20)
    
    # Añadir información en la esquina inferior derecha
    info_text = f"Resolución: {WIDTH}x{HEIGHT}\n"
    info_text += f"Offset: ({X_OFFSET}, {Y_OFFSET})"
    plt.text(WIDTH-10, HEIGHT-10, info_text, 
             color='white', ha='right', va='bottom', fontsize=8)
    
    if save:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"mandelbrot_{timestamp}.png"
        plt.savefig(filename, bbox_inches='tight', pad_inches=0, dpi=300)
        print(f"Fractal guardado como {filename}")
    plt.show()

if __name__ == "__main__":
    print("Generando fractal de Mandelbrot...")
    start_time = time.time()
    
    fractal = create_fractal(WIDTH, HEIGHT, ZOOM, X_OFFSET, Y_OFFSET, MAX_ITER)
    
    end_time = time.time()
    print(f"Fractal generado en {end_time - start_time:.2f} segundos")
    
    plot_fractal(fractal, cmap, save=True)