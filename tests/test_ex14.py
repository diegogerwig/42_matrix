import os
import math
import subprocess
import stat  # <-- Nueva librería para modificar permisos de archivos
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

def wrapper_projection(fov, ratio, near, far):
    proj_matrix = projection(fov, ratio, near, far)
    save_proj_file(proj_matrix)
    return [[round(val, 5) for val in row] for row in proj_matrix.data]

def run():
    print_header(14, "PROJECTION MATRIX")

    cases = [
        ((math.pi / 2.0, 1.0, 1.0, 100.0), 
         [[1.0, 0.0, 0.0, 0.0],
          [0.0, 1.0, 0.0, 0.0],
          [0.0, 0.0, -1.0202, -2.0202],
          [0.0, 0.0, -1.0, 0.0]]),
          
        ((math.pi / 2.0, 16.0 / 9.0, 0.1, 1000.0), 
         [[0.5625, 0.0, 0.0, 0.0],
          [0.0, 1.0, 0.0, 0.0],
          [0.0, 0.0, -1.0002, -0.20002],
          [0.0, 0.0, -1.0, 0.0]]),
          
        ((math.pi / 2.0, 1.0, 10.0, 10.0), None),
        ((-0.5, 1.0, 1.0, 100.0), None),
    ]

    def custom_desc(f, r, n, fa):
        deg = round(f * 180.0 / math.pi, 1)
        return f"projection(fov={deg}°, ratio={round(r,2)}, near={n}, far={fa})\n  ↳ Resultado"

    run_cases(14, wrapper_projection, cases, custom_desc_func=custom_desc)

    # =========================================================================
    # 🚀 DISPARO AUTÓNOMO DEL VISOR 3D (CON AUTORREPARACIÓN DE PERMISOS)
    # =========================================================================
    current_dir = os.path.dirname(os.path.abspath(__file__))
    viewer_dir = os.path.abspath(os.path.join(current_dir, '..', 'display_linux', 'matrix_display'))
    executable = os.path.join(viewer_dir, 'display')

    if os.path.exists(executable):
        print(f"\n{CYAN}🚀 Abriendo el visor gráfico 3D de forma autónoma...{NC}")
        try:
            # Usamos la ruta ABSOLUTA (executable) en lugar de la relativa ("./display")
            subprocess.Popen(
                [executable], 
                cwd=viewer_dir, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            print(f"{GREEN}¡Hecho! Revisa las ventanas de tu entorno de escritorio.{NC}\n")
        except Exception as e:
            print(f"{RED}No se pudo iniciar el proceso gráfico: {e}{NC}\n")
    else:
        print(f"\n{YELLOW}⚠️  Aviso: No se encontró el binario gráfico en: {executable}{NC}\n")

if __name__ == "__main__":
    run()