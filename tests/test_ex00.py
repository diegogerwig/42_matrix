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

    # ----- VECTORES -----
    vec_add_cases = [
        (([2., 3.], [5., 7.]), [7., 10.]),
        (([0., 0.], [0., 0.]), [0., 0.]),
        (([-5., 2.], [5., -2.]), [0., 0.]),
        (([1.], [1.]), [2.]),
        # Casos de error de dimensiones
        (([1., 2.], [1., 2., 3.]), None)
    ]
    
    vec_sub_cases = [
        (([2., 3.], [5., 7.]), [-3., -4.]),
        (([5., 7.], [2., 3.]), [3., 4.]),
        # Casos de error
        (([1.], [1., 2.]), None)
    ]

    vec_scl_cases = [
        (([2., 3.], 2.), [4., 6.]),
        (([2., 3.], 0.), [0., 0.]),
        (([2., 3.], -1.), [-2., -3.])
    ]

    # ----- MATRICES -----
    m1 = [[1., 2.], [3., 4.]]
    m2 = [[7., 4.], [-2., 2.]]
    
    mat_add_cases = [
        ((m1, m2), [[8., 6.], [1., 6.]]),
        # Caso error (diferente shape)
        ((m1, [[1.]]), None)
    ]

    mat_sub_cases = [
        ((m1, m2), [[-6., -2.], [5., 2.]])
    ]

    mat_scl_cases = [
        ((m1, 2.), [[2., 4.], [6., 8.]]),
        ((m1, 0.), [[0., 0.], [0., 0.]])
    ]

    # Ejecución con el formateo exacto de utils.py
    print(f"\n{CYAN}--- Pruebas de Vectores ---{NC}")
    run_cases(0, wrapper_vec_add, vec_add_cases, custom_desc_func=lambda u, v: f"Vector.add({u}, {v})")
    run_cases(0, wrapper_vec_sub, vec_sub_cases, custom_desc_func=lambda u, v: f"Vector.sub({u}, {v})")
    run_cases(0, wrapper_vec_scl, vec_scl_cases, custom_desc_func=lambda u, s: f"Vector.scl({u}, {s})")

    print(f"\n{CYAN}--- Pruebas de Matrices ---{NC}")
    run_cases(0, wrapper_mat_add, mat_add_cases, custom_desc_func=lambda u, v: f"Matrix.add({u}, {v})")
    run_cases(0, wrapper_mat_sub, mat_sub_cases, custom_desc_func=lambda u, v: f"Matrix.sub({u}, {v})")
    run_cases(0, wrapper_mat_scl, mat_scl_cases, custom_desc_func=lambda u, s: f"Matrix.scl({u}, {s})")


if __name__ == "__main__":
    run()