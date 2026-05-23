from vector import Vector
from matrix import Matrix
from linear_interpolation import lerp
from utils import *

def wrapper_lerp(u_data, v_data, t):
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
        
    res = lerp(u, v, t)
    
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
        # CASOS ESCALARES
        ((0., 1., 0.), 0.0),
        ((0., 1., 1.), 1.0),
        ((0., 1., 0.5), 0.5),
        ((21., 42., 0.3), 27.3),
        # CASOS VECTORES
        (([2., 1.], [4., 2.], 0.3), [2.6, 1.3]),
        # CASOS MATRICES
        (([[2., 1.], [3., 4.]], [[20., 10.], [30., 40.]], 0.5), [[11., 5.5], [16.5, 22.]]),
        # CASOS DE ERROR CONTROLADO
        (([1., 2.], [1., 2., 3.], 0.5), None),           # Vectores distinto tamaño
        (([[1., 2.]], [[1., 2.], [3., 4.]], 0.5), None), # Matrices distinto tamaño
        ((5., [1., 2.], 0.5), None),                     # Tipos incompatibles
        ((5., 10., "0.5"), None),                        # Valor no numérico
    ]

    def custom_desc(u, v, t):
        # Función auxiliar para formatear visualmente la entrada
        def format_arg(arg):
            if isinstance(arg, list):
                if len(arg) > 0 and isinstance(arg[0], list):
                    return f"Matrix({arg})"
                else:
                    return f"Vector({arg})"
            return str(arg)
            
        return f"lerp({format_arg(u)}, {format_arg(v)}, {t})\n  ↳ Resultado"

    run_cases(2, wrapper_lerp, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()