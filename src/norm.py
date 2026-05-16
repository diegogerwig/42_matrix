import math
from vector import Vector

def norm_1(u: 'Vector') -> float:
    """Norma de Manhattan (L1): Suma de los valores absolutos."""
    if not isinstance(u, Vector):
        raise TypeError("El argumento debe ser un Vector.")
        
    res = 0.0
    for x in u.data:
        res += float(x) if x >= 0 else float(-x)
    return res

def norm(u: 'Vector') -> float:
    """Norma Euclidiana (L2): Raíz cuadrada de la suma de sus componentes al cuadrado."""
    if not isinstance(u, Vector):
        raise TypeError("El argumento debe ser un Vector.")
        
    res = 0.0
    use_fma = hasattr(math, 'fma')
    
    for x in u.data:
        val = float(x)
        if use_fma:
            res = math.fma(val, val, res)
        else:
            res += val * val
            
    return pow(res, 0.5)

def norm_inf(u: 'Vector') -> float:
    """Norma Suprema (L-inf): Máximo valor absoluto de sus componentes."""
    if not isinstance(u, Vector):
        raise TypeError("El argumento debe ser un Vector.")
        
    res = 0.0
    for x in u.data:
        val = float(x) if x >= 0 else float(-x)
        res = max(res, val)
    return res