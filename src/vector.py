class Vector:
    def __init__(self, data: list):
        self.data = list(data)

    def add(self, v: 'Vector') -> None:
        """Añade un vector al vector actual (in-place)."""
        if len(self.data) != len(v.data):
            raise ValueError("Los vectores deben tener la misma dimensión.")
        for i in range(len(self.data)):
            self.data[i] += v.data[i]

    def sub(self, v: 'Vector') -> None:
        """Resta un vector al vector actual (in-place)."""
        if len(self.data) != len(v.data):
            raise ValueError("Los vectores deben tener la misma dimensión.")
        for i in range(len(self.data)):
            self.data[i] -= v.data[i]

    def scl(self, a) -> None:
        """Escala el vector por un escalar 'a' (in-place)."""
        for i in range(len(self.data)):
            self.data[i] *= a

    def __str__(self):
        # Formato de columna requerido por el PDF
        return "\n".join([f"[{float(x)}]" for x in self.data])