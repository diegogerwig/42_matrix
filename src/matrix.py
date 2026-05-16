import math
from vector import Vector

class Matrix:
    def __init__(self, data: list[list]):
        if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
            raise ValueError("La estructura base de la Matrix debe ser una lista de listas.")
        
        if data:
            cols = len(data[0])
            for row in data:
                if len(row) != cols:
                    raise ValueError("Todas las filas de la matriz deben tener la misma longitud.")
                for x in row:
                    if not isinstance(x, (int, float, complex)):
                        raise ValueError("Los elementos de la Matrix deben ser numéricos.")
                        
        self.data = [list(row) for row in data]
        self.shape = (len(data), len(data[0]) if data else 0)

    def add(self, v: 'Matrix') -> None:
        if self.shape != v.shape:
            raise ValueError("Las matrices deben tener las mismas dimensiones para sumarse.")
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.data[i][j] += v.data[i][j]

    def sub(self, v: 'Matrix') -> None:
        if self.shape != v.shape:
            raise ValueError("Las matrices deben tener las mismas dimensiones para restarse.")
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.data[i][j] -= v.data[i][j]

    def scl(self, a) -> None:
        if not isinstance(a, (int, float, complex)):
            raise ValueError("El escalar debe ser un valor numérico.")
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.data[i][j] *= a

    def mul_vec(self, vec: 'Vector') -> 'Vector':
        if not isinstance(vec, Vector):
            raise TypeError("El argumento debe ser un objeto Vector.")
        if self.shape[1] != len(vec.data):
            raise ValueError(f"Incompatibilidad: matriz {self.shape} con vector de dimensión {len(vec.data)}.")
            
        m, n = self.shape
        res_data = [0.0] * m
        use_fma = hasattr(math, 'fma')
        
        for i in range(m):
            for j in range(n):
                if use_fma:
                    res_data[i] = math.fma(float(self.data[i][j]), float(vec.data[j]), res_data[i])
                else:
                    res_data[i] += float(self.data[i][j]) * float(vec.data[j])
                    
        return Vector(res_data)

    def mul_mat(self, mat: 'Matrix') -> 'Matrix':
        if not isinstance(mat, Matrix):
            raise TypeError("El argumento debe ser un objeto Matrix.")
        if self.shape[1] != mat.shape[0]:
            raise ValueError(f"Dimensiones incompatibles para multiplicación: {self.shape} x {mat.shape}.")
            
        m, n = self.shape
        _, p = mat.shape
        res_data = [[0.0] * p for _ in range(m)]
        use_fma = hasattr(math, 'fma')
        
        for i in range(m):
            for k in range(n):
                val_ik = float(self.data[i][k])
                for j in range(p):
                    if use_fma:
                        res_data[i][j] = math.fma(val_ik, float(mat.data[k][j]), res_data[i][j])
                    else:
                        res_data[i][j] += val_ik * float(mat.data[k][j])
                        
        return Matrix(res_data)

    def __str__(self):
        return "\n".join(["[" + ", ".join(f"{x}" for x in row) + "]" for row in self.data])