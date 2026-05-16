from vector import Vector
from norm import norm_1, norm, norm_inf
from utils import *

def wrapper_norm_1(u_data):
    return norm_1(Vector(u_data))

def wrapper_norm(u_data):
    return round(norm(Vector(u_data)), 9)

def wrapper_norm_inf(u_data):
    return norm_inf(Vector(u_data))

def run():
    print_header(4, "NORM")

    norm_cases_1 = [
        (([0.],), 0.0),
        (([1.],), 1.0),
        (([0., 0.],), 0.0),
        (([1., 0.],), 1.0),
        (([2., 1.],), 3.0),
        (([4., 2.],), 6.0),
        (([-4., -2.],), 6.0),
    ]

    norm_cases_2 = [
        (([0.],), 0.0),
        (([1.],), 1.0),
        (([0., 0.],), 0.0),
        (([1., 0.],), 1.0),
        (([2., 1.],), 2.236067977),
        (([4., 2.],), 4.472135955),
        (([-4., -2.],), 4.472135955),
    ]

    norm_cases_inf = [
        (([0.],), 0.0),
        (([1.],), 1.0),
        (([0., 0.],), 0.0),
        (([1., 0.],), 1.0),
        (([2., 1.],), 2.0),
        (([4., 2.],), 4.0),
        (([-4., -2.],), 4.0),
    ]

    print(f"\n{CYAN}--- Pruebas de Norma 1 (Manhattan) ---{NC}")
    run_cases(4, wrapper_norm_1, norm_cases_1, custom_desc_func=lambda u: f"norm_1({u})")

    print(f"\n{CYAN}--- Pruebas de Norma 2 (Euclidiana) ---{NC}")
    run_cases(4, wrapper_norm, norm_cases_2, custom_desc_func=lambda u: f"norm({u})")

    print(f"\n{CYAN}--- Pruebas de Norma Suprema (Infinity) ---{NC}")
    run_cases(4, wrapper_norm_inf, norm_cases_inf, custom_desc_func=lambda u: f"norm_inf({u})")


if __name__ == "__main__":
    run()