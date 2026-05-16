class Vector:
    def __init__(self, data: list):
        if not isinstance(data, list):
            raise ValueError("La estructura base del Vector debe ser una lista.")
        
        # Validación estricta de tipos numéricos
        for x in data:
            if not isinstance(x, (int, float, complex)):
                raise ValueError("Los elementos del Vector deben ser numéricos (int, float, complex).")
                
        self.data = list(data)

    def add(self, v: 'Vector') -> None:
        if len(self.data) != len(v.data):
            raise ValueError("Los vectores deben tener la misma dimensión para sumarse.")
        for i in range(len(self.data)):
            self.data[i] += v.data[i]

    def sub(self, v: 'Vector') -> None:
        if len(self.data) != len(v.data):
            raise ValueError("Los vectores deben tener la misma dimensión para restarse.")
        for i in range(len(self.data)):
            self.data[i] -= v.data[i]

    def scl(self, a) -> None:
        if not isinstance(a, (int, float, complex)):
            raise ValueError("El escalar debe ser un valor numérico.")
        for i in range(len(self.data)):
            self.data[i] *= a

    def __str__(self):
        # Usamos format simple para que soporte floats y complejos sin romper
        return "\n".join([f"[{x}]" for x in self.data])