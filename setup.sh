#!/bin/bash

B_BLUE='\033[1;34m'
B_CYAN='\033[1;36m'
B_GREEN='\033[1;32m'
B_YELLOW='\033[1;33m'
B_RED='\033[1;31m'
NC='\033[0m'

# ==========================================
# 0. LECTURA DE ARGUMENTOS Y VERIFICACIÓN
# ==========================================

if [ "$#" -gt 2 ]; then
    echo -e "${B_RED}❌ Error: Demasiados argumentos ($#). Se esperaban máximo 2.${NC}"
    echo -e "${B_YELLOW}Uso correcto:${NC}"
    echo -e "  bash setup.sh           -> [Default] Crea/usa venv y ejecuta TODOS los tests."
    echo -e "  bash setup.sh test      -> Crea/usa venv, ejecuta TODOS los tests y sale."
    echo -e "  bash setup.sh test x    -> Ejecuta SOLO el test x (admite del 0 al 15)."
    echo -e "  bash setup.sh venv      -> Crea/usa venv y lo deja activado en la terminal."
    echo -e "  bash setup.sh clean     -> Borra el entorno virtual y limpia las cachés."
    echo -e "  bash setup.sh complexity-> Ejecuta el Test de Complejidad (Time & Space)."
    exit 1
fi

MODE=${1:-test}
SPECIFIC_TEST=$2

if [[ "$MODE" != "test" && "$MODE" != "venv" && "$MODE" != "clean" && "$MODE" != "memory" && "$MODE" != "complexity" ]]; then
    echo -e "${B_RED}❌ Argumento inválido: $MODE${NC}"
    echo -e "${B_YELLOW}Uso correcto:${NC}"
    echo -e "  bash setup.sh           -> [Default] Crea/usa venv y ejecuta TODOS los tests."
    echo -e "  bash setup.sh test      -> Crea/usa venv, ejecuta TODOS los tests y sale."
    echo -e "  bash setup.sh test x    -> Ejecuta SOLO el test x (admite del 0 al 15)."
    echo -e "  bash setup.sh venv      -> Crea/usa venv y lo deja activado en la terminal."
    echo -e "  bash setup.sh clean     -> Borra el entorno virtual y limpia las cachés."
    echo -e "  bash setup.sh complexity-> Ejecuta el Test de Complejidad (Time & Space)."
    exit 1
fi

if [[ -n "$SPECIFIC_TEST" ]]; then
    if ! [[ "$SPECIFIC_TEST" =~ ^[0-9]+$ ]] || [ "$SPECIFIC_TEST" -lt 0 ] || [ "$SPECIFIC_TEST" -gt 15 ]; then
        echo -e "${B_RED}❌ Error: El número de test debe ser un valor numérico entre 0 y 15.${NC}"
        exit 1
    fi
fi

if ! command -v uv &> /dev/null; then
    echo -e "${B_RED}❌ Error: 'uv' no está instalado. Por favor, instálalo primero.${NC}"
    exit 1
fi

# ==========================================
# 1. DETECCIÓN DE ENTORNO Y RUTA DEL VENV
# ==========================================
OS_NAME=$(uname -s)
USER_HOME=$HOME

if [[ "$OS_NAME" == "Linux" && -d "$USER_HOME/sgoinfre" ]]; then
    TARGET_DIR="$USER_HOME/sgoinfre"
    VENV_NAME="matrix_venv"
    echo -e "\n${B_YELLOW}🖥️  Sistema detectado: Linux (42 Campus)${NC}"
else
    # Estándar absoluto: carpeta .venv en la raíz del proyecto
    TARGET_DIR="$(pwd)"
    VENV_NAME=".venv"
    echo -e "\n${B_YELLOW}🖥️  Sistema detectado: Local / WSL${NC}"
fi

VENV_PATH="$TARGET_DIR/$VENV_NAME"
unset TEST_RESULTS
declare -a TEST_RESULTS=()
ALL_TESTS_PASSED=true

echo -e "\n${B_BLUE}╔═══════════════════════════════════╗${NC}"
echo -e   "${B_BLUE}║              MATRIX               ║${NC}"
echo -e   "${B_BLUE}╚═══════════════════════════════════╝${NC}"

# ==========================================
# 2. MODO CLEAN
# ==========================================
if [[ "$MODE" == "clean" ]]; then
    echo -e "\n${B_CYAN}⚙️  Modo seleccionado: ${NC}clean"
    echo -ne "${B_CYAN}🧹 Limpiando cachés...${NC}"
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
    echo -e " ${B_GREEN}Hecho.${NC}"

    if [ -d "$VENV_PATH" ]; then
        echo -ne "${B_YELLOW}⚙️  Borrando entorno virtual en $VENV_PATH...${NC}"
        rm -rf "$VENV_PATH"
        echo -e " ${B_GREEN}Hecho.${NC}"
    fi
    exit 0
fi

echo -e "\n${B_CYAN}📂 Ruta del entorno: ${NC}$VENV_PATH"
echo -e "${B_CYAN}⚙️  Modo seleccionado: ${NC}$MODE"
if [[ -n "$SPECIFIC_TEST" && "$MODE" == "test" ]]; then
    echo -e "${B_CYAN}🎯 Filtro de test: ${NC}Ejercicio $(printf "%02d" "$SPECIFIC_TEST")"
fi

echo -ne "${B_CYAN}🧹 Limpiando cachés...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo -e " ${B_GREEN}Hecho.${NC}"

# ==========================================
# 3. CREACIÓN Y ACTIVACIÓN DEL VENV CON UV
# ==========================================
if [ ! -d "$VENV_PATH" ]; then
    echo -ne "${B_YELLOW}⚙️  Creando entorno virtual con uv...${NC}"
    mkdir -p "$TARGET_DIR"
    uv venv "$VENV_PATH" > /dev/null 2>&1
    echo -e " ${B_GREEN}Hecho.${NC}"
else
    echo -e "${B_CYAN}⚙️  Entorno virtual detectado. Omitiendo creación...${NC}"
fi

source "$VENV_PATH/bin/activate"

PY_VER=$(python3 --version)
PY_LOC=$(which python3)
echo -e "${B_GREEN}🐍 Python Activo:${NC} $PY_VER"
echo -e "   └── $PY_LOC"

# Instalación ultrarrápida con uv pip
if [ -f "requirements.txt" ]; then
    echo -ne "${B_YELLOW}📦 Verificando dependencias con uv (requirements.txt)...${NC}"
    uv pip install -r requirements.txt > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e " ${B_GREEN}Hecho.${NC}"
    else
        echo -e "\n${B_RED}❌ Error instalando/verificando dependencias.${NC}"
        exit 1
    fi
else
    echo -e "${B_CYAN}ℹ️  No se encontró requirements.txt${NC}"
fi

export PYTHONPATH=$PYTHONPATH:$(pwd)/src

# ==========================================
# 4. RAMIFICACIÓN SEGÚN EL MODO ELEGIDO
# ==========================================
if [[ "$MODE" == "venv" ]]; then
    echo -e "\n${B_GREEN}✅ Entorno virtual preparado y listo para usar.${NC}"
    echo -e "${B_CYAN}🚀 Entrando al entorno interactivo...${NC}"
    echo -e "${B_YELLOW}(Escribe 'exit' o presiona Ctrl+D para salir y desactivarlo)${NC}\n"

    TMP_RC=$(mktemp)
    cat ~/.bashrc > "$TMP_RC" 2>/dev/null
    echo "source '$VENV_PATH/bin/activate'" >> "$TMP_RC"
    echo "export PYTHONPATH=\"\$PYTHONPATH:$(pwd)/src\"" >> "$TMP_RC"
    echo "rm -f '$TMP_RC'" >> "$TMP_RC"
    exec bash --rcfile "$TMP_RC"

elif [[ "$MODE" == "complexity" ]]; then
    echo -e "\n${B_CYAN}⚙️  Iniciando Test de Complejidad Completo...${NC}"
    python3 tests/test_complexity.py

elif [[ "$MODE" == "test" ]]; then
    # ==========================================
    # 🔧 REPARACIÓN AUTOMÁTICA DE PERMISOS
    # ==========================================
    VISOR_BIN="$(pwd)/display_linux/matrix_display/display"
    if [ -f "$VISOR_BIN" ]; then
        chmod +x "$VISOR_BIN" 2>/dev/null || true
    fi

    if [ -d "tests" ]; then
        if [[ -n "$SPECIFIC_TEST" ]]; then
            FORMATTED_NUM=$(printf "%02d" "$SPECIFIC_TEST")
            TEST_FILES=$(ls tests/test_ex${FORMATTED_NUM}*.py 2>/dev/null)
        else
            TEST_FILES=$(ls tests/test_*.py | sort)
        fi

        for file in $TEST_FILES; do
            echo -e "\n${B_BLUE}────────────────────────────────────────────────────────────────${NC}"
            echo -e "${B_YELLOW} 🚀 EJECUTANDO ARCHIVO: ${B_CYAN}$(basename "$file")${NC}"
            echo -e "${B_BLUE}────────────────────────────────────────────────────────────────${NC}"
            
            python3 "$file"
            
            if [ $? -eq 0 ]; then
                TEST_RESULTS+=("${B_GREEN}✔ PASS${NC}  $(basename "$file")")
            else
                TEST_RESULTS+=("${B_RED}✘ FAIL${NC}  $(basename "$file")")
                ALL_TESTS_PASSED=false
            fi

            # Interfaz interactiva de pausa y prueba manual
            PREFIX=$(basename "$file" | grep -o 'ex[0-9]\{2\}')
            while true; do
                echo -e "\n${B_CYAN}╭────────────────────────────────────────────────────────╮${NC}"
                echo -e "${B_CYAN}│ ⌛ ESPERANDO CONFIRMACIÓN...                           │${NC}"
                echo -e "${B_CYAN}╰────────────────────────────────────────────────────────╯${NC}"
                echo -e "${B_YELLOW} ↳ OPCIONES:${NC}"
                echo -e "${B_YELLOW} ↳   1. Presiona ${B_GREEN}[ENTER]${B_YELLOW} para avanzar al siguiente test.${NC}"
                echo -e "${B_YELLOW} ↳   2. Escribe '${B_GREEN}python3${B_YELLOW}' para abrir la consola interactiva y probar tus clases.${NC}"
                echo -e "${B_YELLOW} ↳   3. Escribe un comando de terminal (ls, cat, ...).${NC}\n"
                
                echo -ne "${B_GREEN} > ${NC}"
                read -r user_input

                if [[ -z "$user_input" ]]; then
                    break
                elif [[ "$user_input" == "python" || "$user_input" == "python3" ]]; then
                    # Si escribes python, aseguramos que el PYTHONPATH esté bien inyectado
                    PYTHONPATH="$(pwd)/src" python3
                else
                    eval "$user_input"
                fi
            done
        done
    fi

    # ==========================================
    # 5. RESUMEN FINAL DE LOS TESTS
    # ==========================================
    echo -e "\n${B_BLUE}╔═══════════════════════════════════╗${NC}"
    echo -e "${B_BLUE}║          RESUMEN FINAL            ║${NC}"
    echo -e "${B_BLUE}╚═══════════════════════════════════╝${NC}\n"

    for result in "${TEST_RESULTS[@]}"; do
        echo -e "  $result"
    done

    echo ""
    if [ "$ALL_TESTS_PASSED" = true ]; then
        echo -e "${B_GREEN}✅ RESULTADO GLOBAL: TODO OK${NC}\n"
    else
        echo -e "${B_RED}❌ RESULTADO GLOBAL: ALGUNOS TESTS FALLARON${NC}\n"
    fi
fi