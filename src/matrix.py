class Matrix:
    def __init__(self, data: list[list]):
        self.data = [list(row) for row in data]
        self.shape = (len(data), len(data[0]) if data else 0)

    def add(self, v: 'Matrix') -> None:
        """Añade una matriz a la matriz actual (in-place)."""
        if self.shape != v.shape:
            raise ValueError("Las matrices deben tener las mismas dimensiones.")
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.data[i][j] += v.data[i][j]

    def sub(self, v: 'Matrix') -> None:
        """Resta una matriz a la matriz actual (in-place)."""
        if self.shape != v.shape:
            raise ValueError("Las matrices deben tener las mismas dimensiones.")
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.data[i][j] -= v.data[i][j]

    def scl(self, a) -> None:
        """Escala la matriz por un escalar 'a' (in-place)."""
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.data[i][j] *= a

    def __str__(self):
        # Formato requerido por el PDF
        return "\n".join(["[" + ", ".join(f"{float(x)}" for x in row) + "]" for row in self.data])