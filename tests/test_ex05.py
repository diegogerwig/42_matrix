from vector import Vector
from cosine import angle_cos
from utils import *

def wrapper_angle_cos(u_data, v_data):
    res = angle_cos(Vector(u_data), Vector(v_data))
    return round(res, 9)

def run():
    print_header(5, "COSINE")

    cases = [
        (([1., 0.], [0., 1.]), 0.0),
        (([8., 7.], [3., 2.]), 0.991454296),
        (([1., 1.], [1., 1.]), 1.0),
        (([4., 2.], [1., 1.]), 0.948683298),
        (([-7., 3.], [6., 4.]), -0.546267781),
        (([3., 2.], [8., 7.]), 0.991454296),  # Prueba de Conmutatividad (Mismo resultado invirtiendo parámetros)
        # CASOS DE ERROR CONTROLADO
        (([1., 2.], [1., 2., 3.]), None),  # Dimensiones diferentes
        (([0., 0.], [1., 1.]), None),      # Vector nulo (división por cero)
    ]

    def custom_desc(u, v):
        return f"angle_cos({u}, {v})"

    run_cases(5, wrapper_angle_cos, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()