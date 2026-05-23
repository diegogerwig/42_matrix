import math
from matrix import Matrix
from projection import projection
from utils import *

def wrapper_projection(fov, ratio, near, far):
    res = projection(fov, ratio, near, far).data
    return [[round(val, 5) for val in row] for row in res]

def run():
    print_header(14, "PROJECTION MATRIX")

    cases = [
        # CONFIGURACIONES DE CÁMARA 3D (Simuladas)
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
        return f"projection(fov=PI/2, ratio={round(r,2)}, near={n}, far={fa})\n  ↳ Resultado"

    run_cases(14, wrapper_projection, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()