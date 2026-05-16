from vector import Vector
from linear_combination import linear_combination
from utils import *

def wrapper_linear_combination(vectors_data, coefs):
    vectors = [Vector(d) for d in vectors_data]
    res = linear_combination(vectors, coefs)
    return res.data

def run():
    print_header(1, "LINEAR COMBINATION")

    cases = [
        #
        (([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]], [10., -2., 0.5]), [10., -2., 0.5]),
        (([[1., 2., 3.], [0., 10., -100.]], [10., -2.]), [10., 0., 230.]),
        (([[-42., 42.]], [-1.]), [42., -42.]),
        #
        (([[-42.], [-42.], [-42.]], [-1., 1., 0.]), [0.]),
        #
        (([[-42., 42.], [1., 3.], [10., 20.]], [1., -10., -1.]), [-62., -8.]),
        (([[-42., 100., -69.5], [1., 3., 5.]], [1., -10.]), [-52., 70., -119.5]),
        # Casos de error 
        (([[1., 2.], [3., 4., 5.]], [1., 2.]), None),  # Dimensiones diferentes
        (([[1., 2.]], [1., 2.]), None),                # Desajuste coeficientes/vectores
        (([], []), None),                              # Vacío
    ]

    def custom_desc(vectors_data, coefs):
        return f"linear_combination({len(vectors_data)} vectors)"

    run_cases(1, wrapper_linear_combination, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()