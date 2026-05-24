import os
import math
import subprocess
from vector import Vector
from matrix import Matrix
from projection import projection
from utils import *

def save_proj_file(proj_matrix: Matrix) -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, '..', 'display_linux', 'matrix_display')
    if os.path.exists(folder_path):
        file_path = os.path.join(folder_path, "proj")
        with open(file_path, "w") as f:
            for i in range(4):
                line = ", ".join(f"{proj_matrix.data[i][j]:.6f}" for j in range(4))
                f.write(line + "\n")

def render_model_to_image(fov, ratio, near, far, proj_matrix: Matrix):
    """
    Renderiza el modelo 3D APLICANDO tu matriz de proyección.
    Dibuja un wireframe para que la figura sea reconocible.
    """
    try:
        import matplotlib.pyplot as plt
        # Aunque no usemos Axes3D directamente ahora (proyectamos a 2D), 
        # es buena práctica capturar el error de importación por si falta la librería.
    except ImportError:
        return

    current_dir = os.path.dirname(os.path.abspath(__file__))
    obj_path = os.path.join(current_dir, '..', 'display_linux', 'matrix_display', 'assets', 'model.obj')
    out_dir = os.path.join(current_dir, '..', 'display_output')
    os.makedirs(out_dir, exist_ok=True)
    
    deg = round(fov * 180.0 / math.pi, 1)
    r = round(ratio, 2)
    filename = f"render_fov{deg}_ratio{r}_near{near}_far{far}.png"
    out_path = os.path.join(out_dir, filename)

    if not os.path.exists(obj_path):
        return

    # 1. Extraer vértices y caras
    vertices = []
    faces = []
    with open(obj_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.split()
                # Añadimos W=1 para coordenadas homogéneas
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3]), 1.0])
            elif line.startswith('f '):
                parts = line.split()
                # Los índices en OBJ empiezan en 1, así que restamos 1
                face_indices = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                faces.append(face_indices)

    # 2. APLICAR TU MATRIZ DE PROYECCIÓN A LOS PUNTOS
    projected_vertices = []
    
    # Para que se vea bien en cámara, alejamos un poco el logo en Z antes de proyectar
    Z_OFFSET = 2.0 
    
    for v in vertices:
        # Movemos el vértice lejos de la cámara
        v[2] -= Z_OFFSET 
        
        # Lo multiplicamos por tu matriz de proyección (¡Esto prueba tu código!)
        v_vec = Vector([v[0], v[1], v[2], v[3]])
        try:
            proj_v = proj_matrix.mul_vec(v_vec).data
        except:
            # Fallback simple si tu mul_vec es muy estricto con las dimensiones
            proj_v = [0, 0, 0, 1]
            for i in range(4):
                proj_v[i] = sum(proj_matrix.data[i][j] * v[j] for j in range(4))

        # Perspectiva: División por W
        w = proj_v[3]
        if w != 0:
            proj_v[0] /= w
            proj_v[1] /= w
            proj_v[2] /= w

        projected_vertices.append(proj_v)

    # 3. Configurar el lienzo 2D (ya que la matriz proyecta de 3D a 2D)
    fig = plt.figure(figsize=(8, 8), facecolor='#1e1e1e')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#1e1e1e')

    # 4. Dibujar las caras (Wireframe retro estilo Matrix)
    for face in faces:
        x_pts = [projected_vertices[idx][0] for idx in face]
        y_pts = [projected_vertices[idx][1] for idx in face]
        # Cerrar el polígono conectando el último punto con el primero
        x_pts.append(x_pts[0])
        y_pts.append(y_pts[0])
        ax.plot(x_pts, y_pts, color='#00ffcc', linewidth=1, alpha=0.8)

    ax.axis('equal') # Mantener la proporción
    ax.axis('off')   # Ocultar los ejes y cuadrículas

    plt.savefig(out_path, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
    plt.close()

def wrapper_projection(fov, ratio, near, far):
    # Genera la matriz
    proj_matrix = projection(fov, ratio, near, far)
    # Guarda el fichero txt tradicional por si alguna vez se necesita el binario de C
    save_proj_file(proj_matrix)
    
    # ¡Genera la imagen renderizada con tu propia matriz!
    render_model_to_image(fov, ratio, near, far, proj_matrix)
    
    return [[round(val, 5) for val in row] for row in proj_matrix.data]

def run():
    print_header(14, "PROJECTION MATRIX")

    cases = [
        ((math.pi / 2.0, 1.0, 1.0, 100.0), 
         [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, -1.0202, -2.0202], [0.0, 0.0, -1.0, 0.0]]),
        ((math.pi / 2.0, 16.0 / 9.0, 0.1, 1000.0), 
         [[0.5625, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, -1.0002, -0.20002], [0.0, 0.0, -1.0, 0.0]]),
        ((math.pi / 2.0, 1.0, 10.0, 10.0), None),
        ((-0.5, 1.0, 1.0, 100.0), None),
    ]

    def custom_desc(f, r, n, fa):
        deg = round(f * 180.0 / math.pi, 1)
        return f"projection(fov={deg}°, ratio={round(r,2)}, near={n}, far={fa})\n  ↳ Resultado"

    run_cases(14, wrapper_projection, cases, custom_desc_func=custom_desc)

    # Mensaje final indicando la ubicación de las imágenes generadas
    current_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(current_dir, '..', 'display_output'))
    print(f"\n{CYAN}📸 Renders 3D (Wireframe) generados con éxito para cada test válido en:{NC}")
    print(f"{GREEN}   ↳ {out_dir}{NC}\n")

if __name__ == "__main__":
    run()