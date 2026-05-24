import os
import sys
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Aseguramos que Python encuentre tus clases de la carpeta src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from vector import Vector
from matrix import Matrix
from projection import projection

def load_model():
    """Lee el archivo .obj y extrae vértices y caras."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    obj_path = os.path.join(current_dir, '..', 'display_linux', 'matrix_display', 'assets', 'model.obj')
    
    vertices, faces = [], []
    if not os.path.exists(obj_path):
        print(f"❌ Error: No se encontró el modelo en {obj_path}")
        sys.exit(1)
        
    with open(obj_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3]), 1.0])
            elif line.startswith('f '):
                parts = line.split()
                face_indices = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                faces.append(face_indices)
    return vertices, faces

def run_interactive_viewer():
    vertices, faces = load_model()

    # Ampliamos la ventana para que quepan más controles
    fig, ax = plt.subplots(figsize=(10, 9), facecolor='#1e1e1e')
    plt.subplots_adjust(bottom=0.45) # Hacemos más hueco abajo
    ax.set_facecolor('#1e1e1e')

    # Configuración de los ejes para los Sliders
    axcolor = '#333333'
    ax_fov   = plt.axes([0.20, 0.35, 0.65, 0.03], facecolor=axcolor)
    ax_ratio = plt.axes([0.20, 0.30, 0.65, 0.03], facecolor=axcolor)
    ax_near  = plt.axes([0.20, 0.25, 0.65, 0.03], facecolor=axcolor)
    ax_far   = plt.axes([0.20, 0.20, 0.65, 0.03], facecolor=axcolor)
    
    # ¡NUEVOS CONTROLES DE ROTACIÓN!
    ax_rot_y = plt.axes([0.20, 0.15, 0.65, 0.03], facecolor=axcolor)
    ax_rot_x = plt.axes([0.20, 0.10, 0.65, 0.03], facecolor=axcolor)

    # Creamos los Sliders
    s_fov   = Slider(ax_fov, 'FOV (Grados)', 10.0, 150.0, valinit=60.0, color='#00ffcc')
    s_ratio = Slider(ax_ratio, 'Ratio', 0.5, 3.0, valinit=1.0, color='#00ffcc')
    s_near  = Slider(ax_near, 'Near', 0.1, 10.0, valinit=0.1, color='#ff3366')
    s_far   = Slider(ax_far, 'Far', 10.0, 100.0, valinit=100.0, color='#ff3366')
    
    # Inicializamos la rotación a 0 para que empiece viéndose de frente
    s_rot_y = Slider(ax_rot_y, 'Rotación Y', -180.0, 180.0, valinit=0.0, color='#aa33ff')
    s_rot_x = Slider(ax_rot_x, 'Rotación X', -180.0, 180.0, valinit=0.0, color='#aa33ff')

    # Textos en blanco para modo oscuro
    for slider in [s_fov, s_ratio, s_near, s_far, s_rot_y, s_rot_x]:
        slider.label.set_color('white')
        slider.valtext.set_color('white')

    def update(val):
        """Se ejecuta dinámicamente cada vez que tocas cualquier slider"""
        ax.clear()
        ax.set_xlim([-1.5, 1.5])
        ax.set_ylim([-1.5, 1.5])
        ax.axis('off')

        fov_rad = s_fov.val * math.pi / 180.0
        
        # 1. Calculamos la matriz de proyección (Cámara)
        try:
            proj_matrix = projection(fov_rad, s_ratio.val, s_near.val, s_far.val)
        except:
            fig.canvas.draw_idle()
            return

        # 2. Leemos la rotación solicitada en los sliders
        angle_y = s_rot_y.val * math.pi / 180.0
        angle_x = s_rot_x.val * math.pi / 180.0
        cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
        cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)

        Z_OFFSET = 4.0 
        projected_vertices = []
        
        # 3. Aplicamos Transformaciones
        for v in vertices:
            # A) Rotación Y (Horizontal)
            x_rot = v[0] * cos_y + v[2] * sin_y
            z_rot = -v[0] * sin_y + v[2] * cos_y
            
            # B) Rotación X (Vertical)
            y_rot = v[1] * cos_x - z_rot * sin_x
            z_final = v[1] * sin_x + z_rot * cos_x
            
            # C) Traslación y conversión a vector homogéneo
            v_copy = [x_rot, y_rot, z_final - Z_OFFSET, 1.0]
            
            # D) Multiplicamos por la matriz de PROYECCIÓN
            v_vec = Vector(v_copy)
            try:
                proj_v = proj_matrix.mul_vec(v_vec).data
            except:
                proj_v = [sum(proj_matrix.data[i][j] * v_copy[j] for j in range(4)) for i in range(4)]

            # E) Perspectiva
            if proj_v[3] != 0:
                proj_v[0] /= proj_v[3]
                proj_v[1] /= proj_v[3]
                proj_v[2] /= proj_v[3]

            projected_vertices.append(proj_v)

        # 4. Dibujar líneas con Clipping
        for face in faces:
            clipped = False
            for idx in face:
                if projected_vertices[idx][2] < -1.0 or projected_vertices[idx][2] > 1.0:
                    clipped = True
                    break
            
            if not clipped:
                x_pts = [projected_vertices[idx][0] for idx in face]
                y_pts = [projected_vertices[idx][1] for idx in face]
                x_pts.append(x_pts[0])
                y_pts.append(y_pts[0])
                ax.plot(x_pts, y_pts, color='#00ffcc', linewidth=1, alpha=0.8)

        fig.canvas.draw_idle()

    # Escuchadores de eventos para los sliders
    s_fov.on_changed(update)
    s_ratio.on_changed(update)
    s_near.on_changed(update)
    s_far.on_changed(update)
    s_rot_y.on_changed(update)
    s_rot_x.on_changed(update)

    # Primer dibujado inicial (de frente)
    update(None)
    
    plt.suptitle("Matrix 42 - Interactive Projection & Rotation Viewer", color='white', y=0.96)
    plt.show()

if __name__ == "__main__":
    run_interactive_viewer()