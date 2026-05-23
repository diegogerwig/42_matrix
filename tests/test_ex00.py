from vector import Vector
from matrix import Matrix
from utils import *

def wrapper_vec_add(u_data, v_data):
    u = Vector(u_data)
    v = Vector(v_data)
    u.add(v)
    return u.data

def wrapper_vec_sub(u_data, v_data):
    u = Vector(u_data)
    v = Vector(v_data)
    u.sub(v)
    return u.data

def wrapper_vec_scl(u_data, scalar):
    u = Vector(u_data)
    u.scl(scalar)
    return u.data

def wrapper_mat_add(u_data, v_data):
    u = Matrix(u_data)
    v = Matrix(v_data)
    u.add(v)
    return u.data

def wrapper_mat_sub(u_data, v_data):
    u = Matrix(u_data)
    v = Matrix(v_data)
    u.sub(v)
    return u.data

def wrapper_mat_scl(u_data, scalar):
    u = Matrix(u_data)
    u.scl(scalar)
    return u.data

def run():
    print_header(0, "ADD, SUBTRACT AND SCALE")

    # CASOS DE VECTORES 
    vec_add_cases = [
        (([0., 0.], [0., 0.]), [0., 0.]),
        (([1., 0.], [0., 1.]), [1., 1.]),
        (([1., 1.], [1., 1.]), [2., 2.]),
        (([21., 21.], [21., 21.]), [42., 42.]),
        (([-21., 21.], [21., -21.]), [0., 0.]),
        (([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.], [9., 8., 7., 6., 5., 4., 3., 2., 1., 0.]), [9., 9., 9., 9., 9., 9., 9., 9., 9., 9.]),
        # CASOS DE ERROR CONTROLADO
        ((['a', 2.], [1., 2.]), None),
        (([1., 2.], "No soy una lista"), None),
        (([1., 2.], [1., 2., 3.]), None),
    ]
    
    vec_sub_cases = [
        (([0., 0.], [0., 0.]), [0., 0.]),
        (([1., 0.], [0., 1.]), [1., -1.]),
        (([1., 1.], [1., 1.]), [0., 0.]),
        (([21., 21.], [21., 21.]), [0., 0.]),
        (([-21., 21.], [21., -21.]), [-42., 42.]),
        (([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.], [9., 8., 7., 6., 5., 4., 3., 2., 1., 0.]), [-9., -7., -5., -3., -1., 1., 3., 5., 7., 9.]),
        # CASOS DE ERROR CONTROLADO
        (([1.], [1., 2.]), None),
    ]

    vec_scl_cases = [
        (([0., 0.], 1.), [0., 0.]),
        (([1., 0.], 1.), [1., 0.]),
        (([1., 1.], 2.), [2., 2.]),
        (([21., 21.], 2.), [42., 42.]),
        (([42., 42.], 0.5), [21., 21.]),
        # CASOS DE ERROR CONTROLADO
        (([1., 1.], 'a'), None),
    ]

    # CASOS DE MATRICES
    mat_add_cases = [
        (([[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]), [[0., 0.], [0., 0.]]),
        (([[1., 0.], [0., 1.]], [[0., 0.], [0., 0.]]), [[1., 0.], [0., 1.]]),
        (([[1., 1.], [1., 1.]], [[1., 1.], [1., 1.]]), [[2., 2.], [2., 2.]]),
        (([[21., 21.], [21., 21.]], [[21., 21.], [21., 21.]]), [[42., 42.], [42., 42.]]),
        # CASOS DE ERROR CONTROLADO 
        (([[1., 2.], [3.]], [[1., 2.], [3., 4.]]), None),
        (([['x', 2.], [3., 4.]], [[1., 2.], [3., 4.]]), None),
        (([[1., 2.], [3., 4.]], [[1.]]), None),  
    ]

    mat_sub_cases = [
        (([[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]), [[0., 0.], [0., 0.]]),
        (([[1., 0.], [0., 1.]], [[0., 0.], [0., 0.]]), [[1., 0.], [0., 1.]]),
        (([[1., 1.], [1., 1.]], [[1., 1.], [1., 1.]]), [[0., 0.], [0., 0.]]),
        (([[21., 21.], [21., 21.]], [[21., 21.], [21., 21.]]), [[0., 0.], [0., 0.]]),
        # CASOS DE ERROR CONTROLADO

    ]

    mat_scl_cases = [
        (([[0., 0.], [0., 0.]], 0.), [[0., 0.], [0., 0.]]),
        (([[1., 0.], [0., 1.]], 1.), [[1., 0.], [0., 1.]]),
        (([[1., 2.], [3., 4.]], 2.), [[2., 4.], [6., 8.]]),
        (([[21., 21.], [21., 21.]], 0.5), [[10.5, 10.5], [10.5, 10.5]]),
        # CCASOS DE ERROR CONTROLADO

    ]

    print(f"\n{CYAN}--- Pruebas de Vectores ---{NC}")
    run_cases(0, wrapper_vec_add, vec_add_cases, custom_desc_func=lambda u, v: f"Vector({u}).add({v})\n  ↳ Resultado")
    run_cases(0, wrapper_vec_sub, vec_sub_cases, custom_desc_func=lambda u, v: f"Vector({u}).sub({v})\n  ↳ Resultado")
    run_cases(0, wrapper_vec_scl, vec_scl_cases, custom_desc_func=lambda u, s: f"Vector({u}).scl({s})\n  ↳ Resultado")

    print(f"\n{CYAN}--- Pruebas de Matrices ---{NC}")
    run_cases(0, wrapper_mat_add, mat_add_cases, custom_desc_func=lambda u, v: f"Matrix({u}).add({v})\n  ↳ Resultado")
    run_cases(0, wrapper_mat_sub, mat_sub_cases, custom_desc_func=lambda u, v: f"Matrix({u}).sub({v})\n  ↳ Resultado")
    run_cases(0, wrapper_mat_scl, mat_scl_cases, custom_desc_func=lambda u, s: f"Matrix({u}).scl({s})\n  ↳ Resultado")


if __name__ == "__main__":
    run()

if __name__ == "__main__":
    run()