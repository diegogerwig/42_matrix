from vector import Vector
from matrix import Matrix
from utils import *

def wrapper_mul_vec(mat_data, vec_data):
    return Matrix(mat_data).mul_vec(Vector(vec_data)).data

def wrapper_mul_mat(m1_data, m2_data):
    return Matrix(m1_data).mul_mat(Matrix(m2_data)).data

def run():
    print_header(7, "LINEAR MAP & MATRIX MULTIPLICATION")

    cases_mul_vec = [
        (([[1., 0.], [0., 1.]], [4., 2.]), [4., 2.]),
        (([[2., 0.], [0., 2.]], [4., 2.]), [8., 4.]),
        (([[2., -2.], [-2., 2.]], [4., 2.]), [4., -4.]),
        (([[0., 0.], [0., 0.]], [4., 2.]), [0., 0.]),
        (([[1., 1.], [1., 1.]], [4., 2.]), [6., 6.]),
        (([[2., 0.], [0., 2.]], [2., 1.]), [4., 2.]), # Escala x2
        (([[0.5, 0.], [0., 0.5]], [4., 2.]), [2., 1.]), # Escala x0.5
        (([[1., 2., 3.], [4., 5., 6.]], [1., 2., 3.]), [14., 32.]),  # Matriz 2x3 * Vector 3x1 -> Vector 2x1
        # CASOS DE ERROR CONTROLADO
        (([[1., 2.], [3., 4.]], [1., 2., 3.]), None) # Incompatibilidad Dimensional
    ]

    cases_mul_mat = [
        (([[1., 0.], [0., 1.]], [[1., 0.], [0., 1.]]), [[1., 0.], [0., 1.]]),
        (([[1., 0.], [0., 1.]], [[2., 1.], [4., 2.]]), [[2., 1.], [4., 2.]]),
        (([[3., -5.], [6., 8.]], [[2., 1.], [4., 2.]]), [[-14., -7.], [44., 22.]]),
        (([[1., 2., 3.], [4., 5., 6.]], [[1., 2.], [3., 4.], [5., 6.]]), [[22., 28.], [49., 64.]]),  # 2x3 * 3x2 -> 2x2
        # CASOS DE ERROR CONTROLADO
        (([[1., 2.], [3., 4.]], [[1.], [2.], [3.]]), None)
    ]

    print(f"\n{CYAN}--- Pruebas de Multiplicación (Matriz * Vector) ---{NC}")
    run_cases(7, wrapper_mul_vec, cases_mul_vec, custom_desc_func=lambda m, v: f"Matrix.mul_vec({v})")

    print(f"\n{CYAN}--- Pruebas de Multiplicación (Matriz * Matriz) ---{NC}")
    run_cases(7, wrapper_mul_mat, cases_mul_mat, custom_desc_func=lambda m1, m2: f"Matrix.mul_mat()")

if __name__ == "__main__":
    run()