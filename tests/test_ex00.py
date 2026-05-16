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

def run():
    print_header(0, "ADD, SUBTRACT AND SCALE")

    # [cite: 312, 318, 325]
    vec_add_cases = [(([2., 3.], [5., 7.]), [7., 10.])]
    vec_sub_cases = [(([2., 3.], [5., 7.]), [-3., -4.])]
    vec_scl_cases = [(([2., 3.], 2.), [4., 6.])]

    print(f"\n{CYAN}--- Pruebas de Vectores ---{NC}")
    run_cases(0, wrapper_vec_add, vec_add_cases, custom_desc_func=lambda u,v: f"Vector({u}) + Vector({v})")
    run_cases(0, wrapper_vec_sub, vec_sub_cases, custom_desc_func=lambda u,v: f"Vector({u}) - Vector({v})")
    run_cases(0, wrapper_vec_scl, vec_scl_cases, custom_desc_func=lambda u,s: f"Vector({u}) * {s}")

    # Wrappers para matrices
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

    # [cite: 330, 345, 358]
    m1 = [[1., 2.], [3., 4.]]
    m2 = [[7., 4.], [-2., 2.]]
    
    mat_add_cases = [((m1, m2), [[8., 6.], [1., 6.]])]
    mat_sub_cases = [((m1, m2), [[-6., -2.], [5., 2.]])]
    mat_scl_cases = [((m1, 2.), [[2., 4.], [6., 8.]])]

    print(f"\n{CYAN}--- Pruebas de Matrices ---{NC}")
    run_cases(0, wrapper_mat_add, mat_add_cases, custom_desc_func=lambda u,v: "Matrix.add()")
    run_cases(0, wrapper_mat_sub, mat_sub_cases, custom_desc_func=lambda u,v: "Matrix.sub()")
    run_cases(0, wrapper_mat_scl, mat_scl_cases, custom_desc_func=lambda u,s: f"Matrix.scl({s})")

if __name__ == "__main__":
    run()