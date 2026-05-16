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

    def __str__(self):
        return "\n".join(["[" + ", ".join(f"{x}" for x in row) + "]" for row in self.data])