from matrix import Matrix
from utils import *

def wrapper_trace(mat_data):
    return Matrix(mat_data).trace()

def run():
    print_header(8, "TRACE")

    cases = [
        (([[1., 0.], [0., 1.]],), 2.0),
        (([[2., -5., 0.], [4., 3., 7.], [-2., 3., 4.]],), 9.0),
        (([[-2., -8., 4.], [1., -23., 4.], [0., 6., 4.]],), -21.0),
        (([[0., 0.], [0., 0.]],), 0.0),
        (([[1., 0.], [0., 1.]],), 2.0), # Traza de la Identidad 2x2
        (([[1., 2.], [3., 4.]],), 5.0),
        (([[8., -7.], [4., 2.]],), 10.0),
        (([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]],), 3.0), # Traza de la Identidad 3x3
        # CASOS DE ERROR CONTROLADO
        (([[1., 2., 3.], [4., 5., 6.]],), None)  # Falla por no ser cuadrada (2x3)
    ]

    def custom_desc(m):
        return f"Matrix.trace()"

    run_cases(8, wrapper_trace, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()