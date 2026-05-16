import math
from vector import Vector

def cross_product(u: 'Vector', v: 'Vector') -> 'Vector':
    """
    Calcula el producto vectorial (cross product) entre dos vectores 3D.
    Devuelve un nuevo Vector ortogonal a los dos originales.
    """
    if not isinstance(u, Vector) or not isinstance(v, Vector):
        raise TypeError("Los argumentos deben ser de la clase Vector.")
        
    if len(u.data) != 3 or len(v.data) != 3:
        raise ValueError("El producto cruzado solo está definido para vectores de dimensión 3.")
        
    u_x, u_y, u_z = u.data
    v_x, v_y, v_z = v.data
    
    use_fma = hasattr(math, 'fma')
    
    if use_fma:
        c_x = math.fma(float(u_y), float(v_z), -(float(u_z) * float(v_y)))
        c_y = math.fma(float(u_z), float(v_x), -(float(u_x) * float(v_z)))
        c_z = math.fma(float(u_x), float(v_y), -(float(u_y) * float(v_x)))
    else:
        c_x = u_y * v_z - u_z * v_y
        c_y = u_z * v_x - u_x * v_z
        c_z = u_x * v_y - u_y * v_x
        
    return Vector([c_x, c_y, c_z])