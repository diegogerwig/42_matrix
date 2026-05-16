# 🧮 Matrix

---

## 🛠️ Guía de Uso del Entorno

Este proyecto utiliza un entorno automatizado gestionado con **`uv`** para garantizar una instalación ultrarrápida de las dependencias y una ejecución robusta de las pruebas en cualquier sistema (WSL, Linux 42, etc.).

### 1. Script MASTER: `setup.sh`
El archivo `setup.sh` detecta automáticamente tu sistema operativo, inicializa el entorno de forma eficiente mediante `uv` e instala las dependencias de desarrollo necesarias.

| Comando | Descripción |
| :--- | :--- |
| **`bash setup.sh test`** | **(Opción por defecto)** Crea/limpia el entorno, instala dependencias con `uv` y ejecuta **todos** los tests de la carpeta `tests/` en orden. |
| **`bash setup.sh test 00`** | Filtra la automatización para ejecutar únicamente las pruebas del Ejercicio 00. |
| **`bash setup.sh venv`** | Configura el entorno y abre una terminal interactiva con el entorno virtual activo y el `PYTHONPATH` listo para reconocer la carpeta `src/`. |
| **`bash setup.sh clean`** | Borra el entorno virtual `.matrix_venv` y limpia recursivamente los archivos de caché `__pycache__`. |

### 2. Ejecución Individual de Tests
Si deseas ejecutar las pruebas de un solo ejercicio de forma aislada con el entorno virtual previamente activado (utilizando `setup.sh venv`), puedes invocar el archivo de pruebas directamente:

```bash
python3 tests/test_ex00.py
```

### 3. Ejecución Manual del Código

Si quieres verificar el comportamiento algebraico de las estructuras de forma interactiva, primero asegúrate de abrir Python con las rutas configuradas. Puedes hacerlo de dos formas:
1. Ejecutando `bash setup.sh venv` para abrir una terminal con el entorno cargado y luego escribiendo `python3`.
2. Escribiendo `python3` directamente en la pausa interactiva de los tests automatizados.

Una vez dentro de la consola de Python (`>>>`), puedes operar tus clases de la siguiente manera:

```python
from vector import Vector
from matrix import Matrix

# Ejemplo de suma in-place con Vectores
u = Vector([2.0, 3.0])
v = Vector([5.0, 7.0])
u.add(v)
print(u)
# [7.0]
# [10.0]
```

---

## ⚡ Guía Rápida de Componentes y Restricciones

Tabla de referencia con el comportamiento algebraico y operacional de las estructuras de la librería:

| Estructura | Representación Operativa | Restricción Dimensional | Efecto Matemático / Lógico |
| --- | --- | --- | --- |
| **Vector** | Arreglo unidimensional (`list`) | Longitud idéntica para `add` / `sub` | Modificación coordenada a coordenada (*in-place*). |
| **Matrix** | Arreglo bidimensional (`list[list]`) | Mismo `shape` (filas $\times$ columnas) | Modificación elemento a elemento (*in-place*). |
| **Escalar** | Número flotante (`float`) o Complejo | Universal (aplica a cualquier dimensión) | Escala la magnitud homogéneamente (*distributivo*). |

---

## 📖 Documentación

[Essence of linear algrebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)

---
---

## EX00 - Add, Subtract and Scale

### 💡 Descripción

Este ejercicio establece las operaciones elementales fundamentales de nuestro espacio vectorial. El objetivo es implementar los mecanismos para sumar, restar y escalar vectores y matrices. De acuerdo con las especificaciones técnicas del módulo, todas las transformaciones se deben realizar **in-place** (mutando internamente la instancia que invoca el método), minimizando la sobrecarga en memoria.

### 🧠 Lógica

Para garantizar la consistencia matemática antes de proceder con cualquier mutación interna, el sistema aplica validaciones estructurales estrictas:

1. **La Suma Parcial y Resta (`add` / `sub`)**:
La operación se realiza elemento a elemento en la misma posición de la cuadrícula o arreglo.
* En **Vectores**: Se verifica que `len(self.data) == len(v.data)`.
* En **Matrices**: Se verifica que las tuplas de dimensiones `shape` sean idénticas tanto en número de filas como de columnas.
* Si las dimensiones difieren, la operación carece de sentido algebraico, por lo que se interrumpe lanzando un error de valor (`ValueError`).


2. **El Escalado Homogéneo (`scl`)**:
La operación multiplica cada componente del contenedor por un factor numérico escalar común $\alpha$. Al tratarse de una transformación lineal pura, altera la magnitud del objeto conservando intacta su geometría y proporciones dimensionales originales.

### 📊 Ejemplo de Flujo de Datos (In-place)

En cada llamada, la instancia que ejecuta el método absorbe los cambios directamente en sus arreglos internos.

#### Operación en Vectores: `u.add(v)`

```text
Vector Inicial (u):      [2.0, 3.0]
Vector Entrada (v):      [5.0, 7.0]
---------------------------------------
Estado Final (u.data):   [7.0, 10.0]   
```

#### Operación en Matrices: `m1.scl(a)`

```text
Matriz Inicial (m1):     [[1.0, 2.0], [3.0, 4.0]]
Factor Escalar (a):      2.0
-------------------------------------------------
Estado Final (m1.data):  [[2.0, 4.0], [6.0, 8.0]] 
```

---
---

