from vector import Vector
from matrix import Matrix

def linear_interpolation(u, v, t: float):  # Conocida como 'lerp'
    """
    Calcula la interpolación lineal exacta entre u y v con un parámetro t.
    Soporta escalares (float, int), Vectores y Matrices.
    """
    if not isinstance(t, (int, float)):
        raise TypeError("El parámetro de interpolación 't' debe ser un número.")
        
    if type(u) != type(v):
        raise TypeError("Los elementos 'u' y 'v' deben ser del mismo tipo.")

    # 1. Caso Base: Interpolar Números (Escalares)
    if isinstance(u, (int, float, complex)):
        # Fórmula: (1 - t) * u + t * v
        # Esta forma es matemáticamente más estable para floats que u + t * (v - u)
        return (1.0 - t) * float(u) + t * float(v)

    # 2. Caso Recursivo: Interpolar Vectores
    elif isinstance(u, Vector):
        if len(u.data) != len(v.data):
            raise ValueError("Los vectores deben tener la misma dimensión.")
        # Aplicamos la interpolación a cada par de coordenadas
        return Vector([linear_interpolation(u_i, v_i, t) for u_i, v_i in zip(u.data, v.data)])

    # 3. Caso Recursivo: Interpolar Matrices
    elif isinstance(u, Matrix):
        if u.shape != v.shape:
            raise ValueError("Las matrices deben tener las mismas dimensiones.")
        # Aplicamos la interpolación iterando sobre cada fila y cada elemento
        res_data = []
        for row_u, row_v in zip(u.data, v.data):
            res_data.append([linear_interpolation(x, y, t) for x, y in zip(row_u, row_v)])
        return Matrix(res_data)

    else:
        raise TypeError(f"Tipo no soportado para interpolación: {type(u)}")