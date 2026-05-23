import os
import math
from matrix import Matrix
from projection import projection
from utils import *

def save_proj_file(proj_matrix: Matrix) -> None:
    """
    Guarda la matriz de proyección en el archivo 'proj' dentro del visor
    utilizando rutas relativas seguras.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, '..', 'display_linux', 'matrix_display')
    
    if os.path.exists(folder_path):
        file_path = os.path.join(folder_path, "proj")
        with open(file_path, "w") as f:
            for i in range(4):
                line = ", ".join(f"{proj_matrix.data[i][j]:.6f}" for j in range(4))
                f.write(line + "\n")

def wrapper_projection(fov, ratio, near, far):
    proj_matrix = projection(fov, ratio, near, far)
    
    save_proj_file(proj_matrix)
    
    return [[round(val, 5) for val in row] for row in proj_matrix.data]

def run():
    print_header(14, "PROJECTION MATRIX")

    cases = [
        # ==========================================
        # CONFIGURACIONES DE CÁMARA PARA EL VISOR
        # ==========================================
        # 1. Pantalla Cuadrada (Ratio 1.0), FOV 90 grados (PI/2), near=1.0, far=100.0
        ((math.pi / 2.0, 1.0, 1.0, 100.0), 
         [[1.0, 0.0, 0.0, 0.0],
          [0.0, 1.0, 0.0, 0.0],
          [0.0, 0.0, -1.0202, -2.0202],
          [0.0, 0.0, -1.0, 0.0]]),
          
        # 2. Pantalla Panorámica 16:9 (Ratio 1.777), FOV 90 grados, near=0.1, far=1000.0
        ((math.pi / 2.0, 16.0 / 9.0, 0.1, 1000.0), 
         [[0.5625, 0.0, 0.0, 0.0],
          [0.0, 1.0, 0.0, 0.0],
          [0.0, 0.0, -1.0002, -0.20002],
          [0.0, 0.0, -1.0, 0.0]]),
          
        # CASOS DE ERROR CONTROLADO
        ((math.pi / 2.0, 1.0, 10.0, 10.0), None), # Falla porque near y far son idénticos
        ((-0.5, 1.0, 1.0, 100.0), None),          # Falla por FOV negativo
    ]

    def custom_desc(f, r, n, fa):
        deg = round(f * 180.0 / math.pi, 1)
        return f"projection(fov={deg}°, ratio={round(r,2)}, near={n}, far={fa})\n  ↳ Resultado"

    run_cases(14, wrapper_projection, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()