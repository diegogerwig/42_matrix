import math
from vector import Vector

def dot(u: 'Vector', v: 'Vector') -> float:
    """
    Calcula el producto escalar (dot product) entre dos vectores.
    Complejidad temporal: O(n) donde n es la dimensión del vector.
    Complejidad espacial: O(1) ya que solo almacenamos un acumulador escalar.
    """
    if not isinstance(u, Vector) or not isinstance(v, Vector):
        raise TypeError("Ambos argumentos deben ser de la clase Vector.")
        
    if len(u.data) != len(v.data):
        raise ValueError("Los vectores deben tener la misma dimensión.")
        
    if len(u.data) == 0:
        raise ValueError("Los vectores no pueden estar vacíos.")
        
    result = 0.0
    use_fma = hasattr(math, 'fma')
    
    # Recorremos ambos vectores paralelamente
    for u_i, v_i in zip(u.data, v.data):
        if use_fma:
            # Multiplica y suma al acumulador en un solo ciclo de reloj
            result = math.fma(float(u_i), float(v_i), result)
        else:
            result += float(u_i) * float(v_i)
            
    return result