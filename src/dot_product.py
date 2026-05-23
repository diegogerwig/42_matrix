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
    
    for i in range(len(u.data)):
        val_u = u.data[i]
        val_v = v.data[i]
        
        if isinstance(val_u, complex):
            val_u = val_u.conjugate()
            result += val_u * val_v
        else:
            if use_fma:
                result = math.fma(float(val_u), float(val_v), result)
            else:
                result += float(val_u) * float(val_v)
            
    return result