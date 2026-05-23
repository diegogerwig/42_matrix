from matrix import Matrix
from utils import *

def wrapper_determinant(mat_data):
    res = Matrix(mat_data).determinant()
    return round(res, 5)

def run():
    print_header(11, "DETERMINANT")

    cases = [
        (([[1., -1.], [-1., 1.]],), 0.0),
        (([[2., 0., 0.], [0., 2., 0.], [0., 0., 2.]],), 8.0),
        (([[8., 5., -2.], [4., 7., 20.], [7., 6., 1.]],), -174.0),
        (([[8., 5., -2., 4.], [4., 2.5, 20., 4.], [8., 5., 1., 4.], [28., -4., 17., 1.]],), 1032.0),
        (([[0., 0.], [0., 0.]],), 0.0),
        (([[1., 0.], [0., 1.]],), 1.0),
        (([[2., 0.], [0., 2.]],), 4.0),
        (([[1., 1.], [1., 1.]],), 0.0),
        (([[0., 1.], [1., 0.]],), -1.0),
        (([[1., 2.], [3., 4.]],), -2.0),
        (([[-7., 5.], [4., 6.]],), -62.0),
        (([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]],), 1.0),
        # CASOS DE ERROR CONTROLADO
        (([[1., 2., 3.], [4., 5., 6.]],), None)  # Falla por no ser cuadrada
    ]

    def custom_desc(m):
        # Mantenemos el formato limpio con salto de línea y flecha
        return f"Matrix({m}).determinant()\n  ↳ Resultado"

    run_cases(11, wrapper_determinant, cases, custom_desc_func=custom_desc)

if __name__ == "__main__":
    run()