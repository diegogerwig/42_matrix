from matrix import Matrix
from utils import *

def wrapper_row_echelon(mat_data):
    res = Matrix(mat_data).row_echelon().data
    return [[round(val, 5) for val in row] for row in res]

def run():
    print_header(10, "ROW-ECHELON FORM")

    cases = [
        (([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]],), [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]),
        (([[1., 2.], [3., 4.]],), [[1., 0.], [0., 1.]]),
        (([[1., 2.], [2., 4.]],), [[1., 2.], [0., 0.]]), 
        (
            ([[8., 5., -2., 4., 28.], 
              [4., 2.5, 20., 4., -4.], 
              [8., 5., 1., 4., 17.]],), 
            [[1.0, 0.625, 0.0, 0.0, -12.16667], 
             [0.0, 0.0, 1.0, 0.0, -3.66667], 
             [0.0, 0.0, 0.0, 1.0, 29.5]]
        ),
        (([[0., 0.], [0., 0.]],), [[0., 0.], [0., 0.]]),
        (([[4., 2.], [2., 1.]],), [[1., 0.5], [0., 0.]]),
        (([[-7., 2.], [4., 8.]],), [[1., 0.], [0., 1.]]),
        (([[1., 2.], [4., 8.]],), [[1., 2.], [0., 0.]]),
        (([[1., 2., 5.], [2., 5., 12.]],), [[1., 0., 1.], [0., 1., 2.]]),
        # CASOS DE ERROR CONTROLADO
    ]

    def custom_desc(m):
        return f"Matrix({m}).row_echelon()"

    run_cases(10, wrapper_row_echelon, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()