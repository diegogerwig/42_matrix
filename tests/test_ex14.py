import os
import math
from vector import Vector
from matrix import Matrix
from projection import projection
from utils import *

def save_proj_files(fov, ratio, near, far, proj_matrix: Matrix) -> None:
    """
    Guarda la matriz de proyección en dos localizaciones:
    1. En 'display_linux/matrix_display/proj' (el archivo central que lee el binario de C).
    2. En 'display_output/' con un nombre único basado en los parámetros, al lado de la imagen.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Guardar en el visor original (Sobreescritura del archivo central)
    viewer_dir = os.path.join(current_dir, '..', 'display_linux', 'matrix_display')
    if os.path.exists(viewer_dir):
        file_path = os.path.join(viewer_dir, "proj")
        with open(file_path, "w") as f:
            for i in range(4):
                line = ", ".join(f"{proj_matrix.data[i][j]:.6f}" for j in range(4))
                f.write(line + "\n")

    # 2. Guardar con nombre único en 'display_output' junto a los renders PNG
    out_dir = os.path.join(current_dir, '..', 'display_output')
    os.makedirs(out_dir, exist_ok=True)
    
    deg = round(fov * 180.0 / math.pi, 1)
    r = round(ratio, 2)
    filename = f"matrix_fov{deg}_ratio{r}_near{near}_far{far}.proj"
    out_path = os.path.join(out_dir, filename)
    
    with open(out_path, "w") as f:
        for i in range(4):
            line = ", ".join(f"{proj_matrix.data[i][j]:.6f}" for j in range(4))
            f.write(line + "\n")

def render_model_to_image(fov, ratio, near, far, proj_matrix: Matrix):
    """
    Renderiza el modelo 3D aplicando tu matriz de proyección.
    Se fijan los límites de la pantalla (Viewport) y se aplica el Clipping de profundidad
    para apreciar el efecto real de las deformaciones.
    """
    try:
        import matplotlib.pyplot as plt
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

    vertices = []
    faces = []
    with open(obj_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3]), 1.0])
            elif line.startswith('f '):
                parts = line.split()
                face_indices = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                faces.append(face_indices)

    projected_vertices = []
    
    # IMPORTANTE: Colocamos el logo en la posición Z = 4.0 para que caiga dentro 
    # de un frustum normal. Así el Near/Far tendrá un impacto visual dramático.
    Z_OFFSET = 4.0 
    
    for v in vertices:
        v[2] -= Z_OFFSET 
        v_vec = Vector([v[0], v[1], v[2], v[3]])
        try:
            proj_v = proj_matrix.mul_vec(v_vec).data
        except:
            proj_v = [0, 0, 0, 1]
            for i in range(4):
                proj_v[i] = sum(proj_matrix.data[i][j] * v[j] for j in range(4))

        w = proj_v[3]
        if w != 0:
            proj_v[0] /= w
            proj_v[1] /= w
            proj_v[2] /= w

        projected_vertices.append(proj_v)

    fig = plt.figure(figsize=(8, 8), facecolor='#1e1e1e')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#1e1e1e')

    # DIBUJADO CON CLIPPING (Corte)
    for face in faces:
        # Verificamos si la cara se sale de los límites de visión Z (Near y Far)
        # En coordenadas normalizadas, la profundidad válida está entre -1 y 1
        clipped = False
        for idx in face:
            z_depth = projected_vertices[idx][2]
            if z_depth < -1.0 or z_depth > 1.0:
                clipped = True
                break
        
        # Solo dibujamos la cara si no ha sido "recortada" por los planos
        if not clipped:
            x_pts = [projected_vertices[idx][0] for idx in face]
            y_pts = [projected_vertices[idx][1] for idx in face]
            x_pts.append(x_pts[0])
            y_pts.append(y_pts[0])
            ax.plot(x_pts, y_pts, color='#00ffcc', linewidth=1, alpha=0.8)

    # CONGELAR LA CÁMARA: Desactivamos el auto-zoom para ver el tamaño real
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    
    # Ocultar los bordes para mantener la estética limpia
    ax.axis('off')

    plt.savefig(out_path, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
    plt.close()

def wrapper_projection(fov, ratio, near, far):
    # 1. Calculamos la matriz con tu código
    proj_matrix = projection(fov, ratio, near, far)
    
    # 2. Guardamos la matriz tanto en la carpeta del visor como de forma única en display_output
    save_proj_files(fov, ratio, near, far, proj_matrix)
    
    # 3. Generamos la imagen con el logo de 42 proyectado
    render_model_to_image(fov, ratio, near, far, proj_matrix)
    
    return [[round(val, 5) for val in row] for row in proj_matrix.data]

def run():
    print_header(14, "PROJECTION MATRIX")

    cases = [
        # 1. FOV 100° - Caso de la evaluación
        ((100.0 * math.pi / 180.0, 1.0, 1.0, 100.0), 
         [[0.8391, 0.0, 0.0, 0.0], [0.0, 0.8391, 0.0, 0.0], [0.0, 0.0, -1.0202, -2.0202], [0.0, 0.0, -1.0, 0.0]]),

        # 2. FOV 70° - Caso de la evaluación
        ((70.0 * math.pi / 180.0, 1.0, 1.0, 100.0), 
         [[1.42815, 0.0, 0.0, 0.0], [0.0, 1.42815, 0.0, 0.0], [0.0, 0.0, -1.0202, -2.0202], [0.0, 0.0, -1.0, 0.0]]),

        # 3. FOV 40° - Caso de la evaluación (Zoom)
        ((40.0 * math.pi / 180.0, 1.0, 1.0, 100.0), 
         [[2.74748, 0.0, 0.0, 0.0], [0.0, 2.74748, 0.0, 0.0], [0.0, 0.0, -1.0202, -2.0202], [0.0, 0.0, -1.0, 0.0]]),

        # 4. Modificación de Ratio (Distorsión horizontal)
        ((70.0 * math.pi / 180.0, 2.0, 1.0, 100.0), 
         [[0.71407, 0.0, 0.0, 0.0], [0.0, 1.42815, 0.0, 0.0], [0.0, 0.0, -1.0202, -2.0202], [0.0, 0.0, -1.0, 0.0]]),

        # 5. Modificación de planos Near/Far (Objeto visible dentro del Frustum)
        ((70.0 * math.pi / 180.0, 1.0, 2.0, 50.0), 
         [[1.42815, 0.0, 0.0, 0.0], [0.0, 1.42815, 0.0, 0.0], [0.0, 0.0, -1.08333, -4.16667], [0.0, 0.0, -1.0, 0.0]]),

        # 6. Vista "Macro" Extrema (Zoom Máximo). FOV 20°, Ratio 1.0, near 0.1, far 100.0
        ((20.0 * math.pi / 180.0, 1.0, 0.1, 100.0), 
         [[5.67128, 0.0, 0.0, 0.0], 
          [0.0, 5.67128, 0.0, 0.0], 
          [0.0, 0.0, -1.002, -0.2002], 
          [0.0, 0.0, -1.0, 0.0]]),      

        # Casos de Error Controlado
        ((math.pi / 2.0, 1.0, 10.0, 10.0), None),
        ((-0.5, 1.0, 1.0, 100.0), None),
    ]

    def custom_desc(f, r, n, fa):
        deg = round(f * 180.0 / math.pi, 1)
        return f"projection(fov={deg}°, ratio={round(r,2)}, near={n}, far={fa})\n  ↳ Resultado"

    run_cases(14, wrapper_projection, cases, custom_desc_func=custom_desc)

    # Mensaje de confirmación final
    current_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(current_dir, '..', 'display_output'))
    print(f"\n{CYAN}📂 Resultados exportados con éxito en:{NC}")
    print(f"{GREEN}   ↳ {out_dir}{NC}")
    print(f"   (Cada configuración cuenta con su archivo '.png' y su matriz '.proj' correspondiente)\n")

if __name__ == "__main__":
    run()