import math
from matrix import Matrix

def projection(fov: float, ratio: float, near: float, far: float) -> 'Matrix':
    """
    Calcula una Matriz de Proyección en perspectiva 4x4 (estilo OpenGL).
    
    :param fov: Field of View (Campo de visión) en radianes.
    :param ratio: Relación de aspecto de la pantalla (Ancho / Alto).
    :param near: Distancia al plano de recorte cercano (Near clipping plane).
    :param far: Distancia al plano de recorte lejano (Far clipping plane).
    """
    if near == far:
        raise ValueError("Los planos 'near' y 'far' no pueden ser iguales (división por cero).")
    if fov <= 0.0 or fov >= math.pi:
        raise ValueError("El FOV debe estar estrictamente entre 0 y PI radianes.")
    if ratio <= 0.0:
        raise ValueError("El aspect ratio debe ser mayor a 0.")
        
    # 'f' es el factor de escala focal basado en la trigonometría del ángulo de visión
    f = 1.0 / math.tan(fov / 2.0)
    
    # Rango de profundidad para el mapeo Z
    z_range = far - near
    
    # Construimos la matriz 4x4 de proyección en perspectiva
    res_data = [
        [f / ratio, 0.0, 0.0, 0.0],
        [0.0, f, 0.0, 0.0],
        [0.0, 0.0, -(far + near) / z_range, -(2.0 * far * near) / z_range],
        [0.0, 0.0, -1.0, 0.0]
    ]
    
    return Matrix(res_data)