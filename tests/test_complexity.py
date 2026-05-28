import os
import sys
import psutil
import matplotlib.pyplot as plt
import tracemalloc
import gc
import time
import math

# Aseguramos que Python encuentre las clases
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from vector import Vector
from matrix import Matrix

# Colores terminal
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
NC = '\033[0m'

# =========================================================================
# FUNCIONES DE PREPARACIÓN Y TEST PARA CADA EJERCICIO
# =========================================================================
def vector_add_complexity(size):
    v1 = Vector([1.0] * size)
    v2 = Vector([2.0] * size)
    return v1 + v2

def matrix_add_complexity(size):
    # Genera matrices cuadradas de size x size
    m1 = Matrix([[1.0] * size for _ in range(size)])
    m2 = Matrix([[2.0] * size for _ in range(size)])
    return m1 + m2

def linear_combination_complexity(size):
    from vector import Vector
    # Simula la ex01: comb. lineal de 'size' vectores de tamaño 'size'
    vectors = [Vector([1.0] * size) for _ in range(size)]
    scalars = [2.0] * size
    res = Vector([0.0] * size)
    for v, coef in zip(vectors, scalars):
        res.add(v.scl(coef))
    return res

def dot_product_complexity(size):
    v1 = Vector([1.5] * size)
    v2 = Vector([2.5] * size)
    return v1.dot(v2)

def matrix_mult_complexity(size):
    m1 = Matrix([[1.0] * size for _ in range(size)])
    m2 = Matrix([[2.0] * size for _ in range(size)])
    return m1.mul_mat(m2)

def transpose_complexity(size):
    m = Matrix([[1.0] * size for _ in range(size)])
    return m.transpose()

def row_echelon_complexity(size):
    # Genera una matriz diagonal (fácil de escalonar pero obliga a recorrer)
    m = Matrix([[1.0 if i == j else 0.5 for j in range(size)] for i in range(size)])
    return m.row_echelon()

def determinant_complexity(size):
    m = Matrix([[1.0 if i == j else 0.5 for j in range(size)] for i in range(size)])
    return m.determinant()

def inverse_complexity(size):
    m = Matrix([[2.0 if i == j else 0.5 for j in range(size)] for i in range(size)])
    return m.inverse()

# =========================================================================
# MOTOR DE ANÁLISIS
# =========================================================================
def measure_complexity(func, size):
    gc.collect() # Limpiamos basura antes de medir
    tracemalloc.start()

    start_time = time.time()
    
    # Ignoramos errores matemáticos intencionados si ocurren en tests
    try:
        func(size)
    except Exception:
        pass
        
    execution_time = (time.time() - start_time) * 1000  # ms

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return peak / 1024, execution_time  # Retorna KB y ms

def estimate_big_o(sizes, metrics):
    """
    Calcula la pendiente logarítmica empírica O(N^k)
    k = log(M2/M1) / log(S2/S1)
    """
    # Ignoramos el primer punto (N muy pequeño) por el overhead de Python
    if len(sizes) < 3 or metrics[-1] <= 0 or metrics[1] <= 0:
        return "O(1) o No Determinable"
        
    slope = math.log(metrics[-1] / metrics[1]) / math.log(sizes[-1] / sizes[1])
    
    if slope < 0.5:
        return "O(1)"
    elif slope < 1.5:
        return "O(N)"
    elif slope < 2.5:
        return "O(N²)"
    elif slope < 3.5:
        return "O(N³)"
    else:
        return f"O(N^{slope:.1f})"

def analyze_complexity():
    # Diccionario de funciones a probar con sus tamaños máximos soportables
    # O(N) pueden llegar a 4096, pero O(N^3) (inversas) las limitamos a 128
    test_suite = [
        (vector_add_complexity, [4, 16, 64, 256, 1024, 4096]),
        (dot_product_complexity, [4, 16, 64, 256, 1024, 4096]),
        (matrix_add_complexity, [4, 8, 16, 32, 64, 128, 256]),
        (linear_combination_complexity, [4, 8, 16, 32, 64, 128, 256]),
        (transpose_complexity, [4, 8, 16, 32, 64, 128, 256]),
        (matrix_mult_complexity, [4, 8, 16, 32, 64, 128]),
        (row_echelon_complexity, [4, 8, 16, 32, 64, 128]),
        (determinant_complexity, [4, 8, 16, 32, 64, 128]),
        (inverse_complexity, [4, 8, 16, 32, 64, 128]),
    ]

    print(f"\n{CYAN}================================================={NC}")
    print(f"{CYAN}🧠 ANÁLISIS GLOBAL DE COMPLEJIDAD (TIME & SPACE) 🧠{NC}")
    print(f"{CYAN}================================================={NC}\n")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(current_dir, '..', 'display_output'))
    os.makedirs(out_dir, exist_ok=True)

    for func, sizes in test_suite:
        func_name = func.__name__.replace('_complexity', '').upper()
        print(f"{YELLOW}▶ Analizando: {func_name}{NC}")
        print(f"{'Input size (N)':<15} | {'Memory (KB)':<15} | {'Time (ms)':<15}")
        print("-" * 50)

        results = list(map(lambda size: measure_complexity(func, size), sizes))
        memory_usage, time_usage = zip(*results)

        for size, mem, time_taken in zip(sizes, memory_usage, time_usage):
            print(f"{size:<15} | {mem:<15.2f} | {time_taken:<15.2f}")

        mem_o = estimate_big_o(sizes, memory_usage)
        time_o = estimate_big_o(sizes, time_usage)

        print(f"\n{GREEN}↳ Memory Complexity: {mem_o}{NC}")
        print(f"{GREEN}↳ Time Complexity:   {time_o}{NC}\n")

        fig, ax1 = plt.subplots(figsize=(10, 6), facecolor='#1e1e1e')
        ax1.set_facecolor('#2d2d2d')
        
        ax1.plot(sizes, memory_usage, 'o-', color='#00ffcc', label='Memory (KB)', linewidth=2)
        ax1.set_xlabel('Input size (N) [Escala Log]', color='white', fontsize=11)
        ax1.set_ylabel('Memory usage (KB)', color='#00ffcc', fontsize=11)
        ax1.tick_params(axis='y', labelcolor='#00ffcc', colors='white')
        ax1.tick_params(axis='x', colors='white')

        ax2 = ax1.twinx()
        ax2.plot(sizes, time_usage, 's-', color='#ff3366', label='Time (ms)', linewidth=2)
        ax2.set_ylabel('Execution time (ms)', color='#ff3366', fontsize=11)
        ax2.tick_params(axis='y', labelcolor='#ff3366')

        ax1.set_xscale('log', base=2)
        ax1.set_yscale('log', base=10)
        ax2.set_yscale('log', base=10)

        plt.title(f'Complexity graph - {func_name}', color='white', pad=20, fontsize=14)
        ax1.grid(True, linestyle='--', alpha=0.2, color='#ffffff')

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        legend = ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', facecolor='#1e1e1e')
        for text in legend.get_texts():
            text.set_color("white")

        out_path = os.path.join(out_dir, f"complexity_{func_name.lower()}.png")
        plt.tight_layout()
        plt.savefig(out_path, facecolor=fig.get_facecolor(), dpi=150)
        plt.close()

    print(f"{CYAN}✅ Análisis completado. Gráficas exportadas a:{NC}")
    print(f"{GREEN}   ↳ {out_dir}{NC}\n")


if __name__ == "__main__":
    analyze_complexity()