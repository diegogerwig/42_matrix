from vector import Vector
from dot_product import dot
from utils import *

def wrapper_dot(u_data, v_data):
    u = Vector(u_data)
    v = Vector(v_data)
    return dot(u, v)

def run():
    print_header(3, "DOT PRODUCT")

    cases = [
        (([0., 0.], [1., 1.]), 0.0),
        (([1., 1.], [1., 1.]), 2.0),
        (([-1., 6.], [3. , 2.]), 9.0),
        (([0., 0.], [0., 0.]), 0.0),
        (([1., 0.], [0., 0.]), 0.0),
        (([1., 0.], [1., 0.]), 1.0),
        (([1., 0.], [0., 1.]), 0.0),       # Vectores perpendiculares = producto escalar 0
        (([4., 2.], [2., 1.]), 10.0),
        (([-4., -5.], [3. , 2.]), -22.0),
        (([-4., -5.], [-3. , -2.]), 22.0),
        # CASOS DE ERROR CONTROLADO
        (([1., 2.], [1., 2., 3.]), None),  # Dimensiones diferentes
        (([], []), None),                  # Vectores vacíos
        (([4., 2.], ['a', 1.]), None),     # Valores no numéricos
    ]

    def custom_desc(u, v):
        return f"dot({u}, {v})"

    run_cases(3, wrapper_dot, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()