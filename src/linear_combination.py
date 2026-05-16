import math
from vector import Vector

def linear_combination(u: list['Vector'], coefs: list[float]) -> 'Vector':
    """
    Calcula la combinación lineal de una lista de vectores escalados por sus coeficientes.
    Complejidad temporal: O(n) donde n es la cantidad total de coordenadas procesadas.
    Complejidad espacial: O(n) para almacenar el vector resultante.
    """
    if not isinstance(u, list) or not isinstance(coefs, list):
        raise TypeError("Los argumentos deben ser listas.")
    
    if len(u) != len(coefs):
        raise ValueError("Debe haber exactamente un coeficiente por cada vector.")
        
    if not u:
        raise ValueError("Se requiere al menos un vector para realizar la combinación.")
    
    dim = len(u[0].data)
    
    for vec in u:
        if not isinstance(vec, Vector):
            raise TypeError("El primer argumento debe contener únicamente objetos Vector.")
        if len(vec.data) != dim:
            raise ValueError("Todos los vectores deben tener la misma dimensión.")
            
    for coef in coefs:
        if not isinstance(coef, (int, float, complex)):
            raise TypeError("Los coeficientes deben ser valores numéricos.")

    res_data = [0.0] * dim
    
    use_fma = hasattr(math, 'fma')
    
    for vec, coef in zip(u, coefs):
        for i in range(dim):
            if use_fma:
                res_data[i] = math.fma(float(coef), float(vec.data[i]), res_data[i])
            # else:
            #     res_data[i] += coef * vec.data[i]
                
    return Vector(res_data)