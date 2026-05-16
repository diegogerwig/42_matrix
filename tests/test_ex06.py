from vector import Vector
from cross_product import cross_product
from utils import *

def wrapper_cross(u_data, v_data):
    res = cross_product(Vector(u_data), Vector(v_data))
    return res.data

def run():
    print_header(6, "CROSS PRODUCT")

    cases = [
        (([0., 0., 1.], [1., 0., 0.]), [0., 1., 0.]),            # Eje Z cruzado con Eje X = Eje Y
        (([1., 2., 3.], [4., 5., 6.]), [-3., 6., -3.]),          # Vectores genéricos
        (([4., 2., -3.], [-2., -5., 16.]), [17., -58., -16.]),   # Vectores con negativos
        (([0., 0., 0.], [0., 0., 0.]), [0., 0., 0.]),
        (([1., 0., 0.], [0., 0., 0.]), [0., 0., 0.]),
        (([1., 0., 0.], [0., 1., 0.]), [0., 0., 1.]),            # Eje X cruzado con Eje Y = Eje Z
        (([8., 7., -4.], [3., 2., 1.]), [15., -20., -5.]),
        (([1., 1., 1.], [0., 0., 0.]), [0., 0., 0.]),
        (([1., 1., 1.], [1., 1., 1.]), [0., 0., 0.]),            # Un vector cruzado consigo mismo es 0
        # CASOS DE ERROR CONTROLADO
        (([1., 0.], [0., 1.]), None),                            # Falla por ser 2D
        (([1., 0., 0., 0.], [0., 1., 0., 0.]), None),            # Falla por ser 4D
    ]

    def custom_desc(u, v):
        return f"cross_product({u}, {v})"

    run_cases(6, wrapper_cross, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()