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

    def trace(self) -> float:
        """
        Calcula la traza de la matriz (suma de la diagonal principal).
        Solo está definida para matrices cuadradas.
        Complejidad temporal: O(n) donde n es el número de filas/columnas.
        Complejidad espacial: O(1).
        """
        if self.shape[0] != self.shape[1]:
            raise ValueError("La traza solo está definida para matrices cuadradas.")
            
        res = 0.0
        for i in range(self.shape[0]):
            res += float(self.data[i][i])
            
        return res

    def transpose(self) -> 'Matrix':
        """
        Calcula y devuelve la transpuesta de la matriz (intercambia filas por columnas).
        Complejidad temporal: O(m * n) donde m y n son las dimensiones de la matriz.
        Complejidad espacial: O(m * n) para almacenar la nueva matriz.
        """
        m, n = self.shape
        
        res_data = [[0.0] * m for _ in range(n)]
        
        for i in range(m):
            for j in range(n):
                res_data[j][i] = float(self.data[i][j])
                
        return Matrix(res_data)

    def row_echelon(self) -> 'Matrix':
        """
        Calcula la Forma Escalonada Reducida por Filas (RREF) mediante Gauss-Jordan.
        Complejidad temporal: O(n^3) 
        Complejidad espacial: O(n^2)
        """
        m, n = self.shape
        data = [[float(val) for val in row] for row in self.data]
        use_fma = hasattr(math, 'fma')
        
        r = 0
        for c in range(n):
            if r >= m:
                break
                
            pivot_row = r
            max_val = abs(data[r][c])
            for i in range(r + 1, m):
                if abs(data[i][c]) > max_val:
                    max_val = abs(data[i][c])
                    pivot_row = i
                    
            if max_val < 1e-7:
                for i in range(r, m):
                    data[i][c] = 0.0
                continue
                
            if pivot_row != r:
                data[r], data[pivot_row] = data[pivot_row], data[r]
                
            pivot_val = data[r][c]
            for j in range(c, n):
                data[r][j] /= pivot_val
                
            for i in range(m):
                if i != r:
                    factor = data[i][c]
                    for j in range(c, n):
                        if use_fma:
                            data[i][j] = math.fma(-factor, data[r][j], data[i][j])
                        else:
                            data[i][j] -= factor * data[r][j]
                            
            r += 1
            
        return Matrix(data)

    def __str__(self):
        return "\n".join(["[" + ", ".join(f"{x}" for x in row) + "]" for row in self.data])