class Vector:
    def __init__(self, data: list):
        self.data = list(data)

    def add(self, v: 'Vector') -> None:
        if len(self.data) != len(v.data):
            raise ValueError("Los vectores deben tener la misma dimensión.")
        for i in range(len(self.data)):
            self.data[i] += v.data[i]

    def sub(self, v: 'Vector') -> None:
        if len(self.data) != len(v.data):
            raise ValueError("Los vectores deben tener la misma dimensión.")
        for i in range(len(self.data)):
            self.data[i] -= v.data[i]

    def scl(self, a) -> None:
        for i in range(len(self.data)):
            self.data[i] *= a

    def __str__(self):
        return "\n".join([f"[{float(x)}]" for x in self.data])