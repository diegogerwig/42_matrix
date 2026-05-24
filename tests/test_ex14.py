import os
import math
import subprocess
from matrix import Matrix
from projection import projection
from utils import *

def save_proj_file(proj_matrix: Matrix) -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, '..', 'display_linux', 'matrix_display')
    if os.path.exists(folder_path):
        file_path = os.path.join(folder_path, "proj")
        with open(file_path, "w") as f:
            for i in range(4):
                line = ", ".join(f"{proj_matrix.data[i][j]:.6f}" for j in range(4))
                f.write(line + "\n")

def render_model_to_image(fov, ratio, near, far):
    """
    Renderiza el modelo 3D y lo guarda en 'display_output' nombrando 
    el archivo según los parámetros de la cámara.
    """
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
    except ImportError:
        return

    current_dir = os.path.dirname(os.path.abspath(__file__))
    obj_path = os.path.join(current_dir, '..', 'display_linux', 'matrix_display', 'assets', 'model.obj')
    
    # 1. Creamos la nueva carpeta display_output en la raíz del proyecto
    out_dir = os.path.join(current_dir, '..', 'display_output')
    os.makedirs(out_dir, exist_ok=True)
    
    # 2. Generamos el nombre del archivo inyectando los parámetros
    deg = round(fov * 180.0 / math.pi, 1)
    r = round(ratio, 2)
    filename = f"render_fov{deg}_ratio{r}_near{near}_far{far}.png"
    out_path = os.path.join(out_dir, filename)

    if not os.path.exists(obj_path):
        return

    # Extraer vértices del .obj
    xs, ys, zs = [], [], []
    with open(obj_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.split()
                xs.append(float(parts[1]))
                ys.append(float(parts[2]))
                zs.append(float(parts[3]))

    # Configurar el lienzo de dibujo 3D
    fig = plt.figure(figsize=(8, 8), facecolor='#1e1e1e')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#1e1e1e')

    # Dibujar la nube de puntos del modelo
    ax.scatter(xs, ys, zs, c='#00ffcc', marker='.', s=1, alpha=0.6)
    ax.axis('off')
    ax.grid(False)

    # Guardar imagen y cerrar proceso de dibujo
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
    plt.close()

def wrapper_projection(fov, ratio, near, far):
    # Genera la matriz
    proj_matrix = projection(fov, ratio, near, far)
    # Guarda el fichero txt tradicional
    save_proj_file(proj_matrix)
    
    # ¡NUEVO!: Genera la imagen exclusiva para este caso (solo si no dio error matemático antes)
    render_model_to_image(fov, ratio, near, far)
    
    return [[round(val, 5) for val in row] for row in proj_matrix.data]

def run():
    print_header(14, "PROJECTION MATRIX")

    cases = [
        ((math.pi / 2.0, 1.0, 1.0, 100.0), 
         [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, -1.0202, -2.0202], [0.0, 0.0, -1.0, 0.0]]),
        ((math.pi / 2.0, 16.0 / 9.0, 0.1, 1000.0), 
         [[0.5625, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, -1.0002, -0.20002], [0.0, 0.0, -1.0, 0.0]]),
        ((math.pi / 2.0, 1.0, 10.0, 10.0), None),
        ((-0.5, 1.0, 1.0, 100.0), None),
    ]

    def custom_desc(f, r, n, fa):
        deg = round(f * 180.0 / math.pi, 1)
        return f"projection(fov={deg}°, ratio={round(r,2)}, near={n}, far={fa})\n  ↳ Resultado"

    run_cases(14, wrapper_projection, cases, custom_desc_func=custom_desc)

    # Mensaje final indicando la ubicación de las imágenes generadas
    current_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(current_dir, '..', 'display_output'))
    print(f"\n{CYAN}📸 Renders 3D generados con éxito para cada test válido en:{NC}")
    print(f"{GREEN}   ↳ {out_dir}{NC}\n")

if __name__ == "__main__":
    run()