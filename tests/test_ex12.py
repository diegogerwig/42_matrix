from matrix import Matrix
from utils import *

def wrapper_inverse(mat_data):
    res = Matrix(mat_data).inverse().data
    return [[round(val, 5) for val in row] for row in res]

def run():
    print_header(12, "INVERSE")

    cases = [
        (([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]],), [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]),
        (([[2., 0., 0.], [0., 2., 0.], [0., 0., 2.]],), [[0.5, 0., 0.], [0., 0.5, 0.], [0., 0., 0.5]]),
        (
            ([[8., 5., -2.], [4., 7., 20.], [7., 6., 1.]],), 
            [[0.64943, 0.0977, -0.65517], 
             [-0.78161, -0.12644, 0.96552], 
             [0.14368, 0.07471, -0.2069]]
        ), 
        (([[1., 0.], [0., 1.]],), [[1., 0.], [0., 1.]]), 
        (([[2., 0.], [0., 2.]],), [[0.5, 0.], [0., 0.5]]), 
        (([[0.5, 0.], [0., 0.5]],), [[2., 0.], [0., 2.]]), 
        (([[0., 1.], [1., 0.]],), [[0., 1.], [1., 0.]]),
        (([[1., 2.], [3., 4.]],), [[-2., 1.], [1.5, -0.5]]),
		# CASOS DE ERROR CONTROLADO
        (([[1., 1.], [1., 1.]],), None),     			# Caso Singular: Determinante 0 (No tiene inversa)
        (([[1., 2., 3.], [4., 5., 6.]],), None)         # Falla por no ser cuadrada
    ]

    def custom_desc(m):
        return f"Matrix({m}).inverse()\n  ↳ Resultado"

    run_cases(12, wrapper_inverse, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()