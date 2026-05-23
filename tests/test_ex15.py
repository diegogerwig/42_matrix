from vector import Vector
from matrix import Matrix
from dot_product import dot
from utils import *

def wrapper_complex_dot(u_data, v_data):
    return dot(Vector(u_data), Vector(v_data))

def wrapper_conj_transpose(mat_data):
    return Matrix(mat_data).conjugate_transpose().data

def run():
    print_header(15, "COMPLEX VECTOR SPACES")

    # j en Python representa el número imaginario (i en matemáticas)
    cases_dot = [
        # (2 + 3i) * (4 - i) usando el conjugado del primero
        (([2 + 3j], [4 - 1j]), (2 - 3j) * (4 - 1j)),
        (([1 + 1j, 1 - 1j], [2 + 0j, 0 + 2j]), (1 - 1j) * 2 + (1 + 1j) * 2j),
    ]

    cases_transpose = [
        # La transpuesta cambia filas por columnas y el signo de 'j'
        (([[1 + 2j, 3 - 4j], [5 + 6j, 7 - 8j]],), 
         [[1 - 2j, 5 - 6j], 
          [3 + 4j, 7 + 8j]]),
    ]

    print(f"\n{CYAN}--- Pruebas de Producto Escalar Complejo (Hermitiano) ---{NC}")
    run_cases(15, wrapper_complex_dot, cases_dot, custom_desc_func=lambda u, v: f"dot({u}, {v})\n  ↳ Resultado")

    print(f"\n{CYAN}--- Pruebas de Transpuesta Conjugada ---{NC}")
    run_cases(15, wrapper_conj_transpose, cases_transpose, custom_desc_func=lambda m: f"Matrix({m}).conjugate_transpose()\n  ↳ Resultado")

if __name__ == "__main__":
    run()