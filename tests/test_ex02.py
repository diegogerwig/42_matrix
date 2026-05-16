from vector import Vector
from matrix import Matrix
from linear_interpolation import linear_interpolation
from utils import *

def wrapper_linear_interpolation(u_data, v_data, t):
    # Detección y parseo dinámico de los inputs
    if isinstance(u_data, list):
        if isinstance(u_data[0], list):
            u = Matrix(u_data)
            v = Matrix(v_data)
        else:
            u = Vector(u_data)
            v = Vector(v_data)
    else:
        u = u_data
        v = v_data
        
    res = linear_interpolation(u, v, t)
    
    # Formateo de salida: Redondeamos A 5 DECIMALES en TODAS las estructuras 
    # para evitar falsos negativos por la precisión de coma flotante de la CPU.
    if isinstance(res, Vector):
        return [round(x, 5) for x in res.data]
    elif isinstance(res, Matrix):
        return [[round(x, 5) for x in row] for row in res.data]
    elif isinstance(res, float):
        return round(res, 5)
        
    return res

def run():
    print_header(2, "LINEAR INTERPOLATION")

    cases = [
        # ==========================================
        # CASOS ESCALARES (Hoja de Evaluación)
        # ==========================================
        ((0., 1., 0.), 0.0),
        ((0., 1., 1.), 1.0),
        ((0., 1., 0.5), 0.5),
        ((21., 42., 0.3), 27.3),
        
        # ==========================================
        # CASOS VECTORES (Hoja de Evaluación)
        # ==========================================
        (([2., 1.], [4., 2.], 0.3), [2.6, 1.3]),
        
        # ==========================================
        # CASOS MATRICES (Hoja de Evaluación)
        # ==========================================
        (([[2., 1.], [3., 4.]], [[20., 10.], [30., 40.]], 0.5), [[11., 5.5], [16.5, 22.]]),
        
        # ==========================================
        # CASOS DE ERROR CONTROLADO
        # ==========================================
        (([1., 2.], [1., 2., 3.], 0.5), None),          # Vectores distinto tamaño
        (([[1., 2.]], [[1., 2.], [3., 4.]], 0.5), None), # Matrices distinto tamaño
        ((5., [1., 2.], 0.5), None),                    # Tipos incompatibles
        ((5., 10., "0.5"), None),                       # t no numérico
    ]

    def custom_desc(u, v, t):
        u_str = str(u) if not isinstance(u, list) else f"{type(Vector(u) if not isinstance(u[0], list) else Matrix(u)).__name__}"
        v_str = str(v) if not isinstance(v, list) else f"{type(Vector(v) if not isinstance(v[0], list) else Matrix(v)).__name__}"
        return f"linear_interpolation({u_str}, {v_str}, {t})"

    run_cases(2, wrapper_linear_interpolation, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()