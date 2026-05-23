from matrix import Matrix
from utils import *

def wrapper_transpose(mat_data):
    return Matrix(mat_data).transpose().data

def run():
    print_header(9, "TRANSPOSE")

    cases = [
        (([[0., 0.], [0., 0.]],), [[0., 0.], [0., 0.]]),
        (([[1., 0.], [0., 1.]],), [[1., 0.], [0., 1.]]),
        (([[1., 2.], [3., 4.]],), [[1., 3.], [2., 4.]]),
        (([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]],), [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]),
        (([[1., 2.], [3., 4.], [5., 6.]],), [[1., 3., 5.], [2., 4., 6.]]),
        # CASOS DE ERROR CONTROLADO
    ]

    def custom_desc(m):
        return f"Matrix.transpose()"

    run_cases(9, wrapper_transpose, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()