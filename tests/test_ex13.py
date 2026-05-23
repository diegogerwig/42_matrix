from matrix import Matrix
from utils import *

def wrapper_rank(mat_data):
    return Matrix(mat_data).rank()

def run():
    print_header(13, "RANK")

    cases = [
        (([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]],), 3),
        (([[1., 2., 0., 0.], [2., 4., 0., 0.], [-1., 2., 1., 1.]],), 2), # Fila 1 y 2 dependientes
        (([[8., 5., -2.], [4., 7., 20.], [7., 6., 1.], [21., 18., 7.]],), 3), # Fila 4 es combinación lineal de las otras 3
        (([[0., 0.], [0., 0.]],), 0), # Matriz completamente nula
        (([[1., 0.], [0., 1.]],), 2),
        (([[2., 0.], [0., 2.]],), 2),
        (([[1., 1.], [1., 1.]],), 1), # Filas idénticas colapsan a rango 1
        (([[0., 1.], [1., 0.]],), 2),
        (([[1., 2.], [3., 4.]],), 2),
        (([[-7., 5.], [4., 6.]],), 2),
    ]

    def custom_desc(m):
        return f"Matrix({m}).rank()\n  ↳ Resultado"

    run_cases(13, wrapper_rank, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()