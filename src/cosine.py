from vector import Vector
from dot_product import dot
from norm import norm

def angle_cos(u: 'Vector', v: 'Vector') -> float:
    """
    Calcula el coseno del ángulo entre dos vectores.
    Complejidad temporal: O(n)
    Complejidad espacial: O(1)
    """
    if not isinstance(u, Vector) or not isinstance(v, Vector):
        raise TypeError("Los argumentos deben ser de la clase Vector.")
        
    dot_prod = dot(u, v)
    norm_u = norm(u)
    norm_v = norm(v)
    
    if norm_u == 0.0 or norm_v == 0.0:
        raise ValueError("El coseno no está definido si uno de los vectores es nulo (norma 0).")
        
    return dot_prod / (norm_u * norm_v)