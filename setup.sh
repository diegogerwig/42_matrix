#!/bin/bash

B_BLUE='\033[1;34m'
B_CYAN='\033[1;36m'
B_GREEN='\033[1;32m'
B_YELLOW='\033[1;33m'
B_RED='\033[1;31m'
NC='\033[0m'

MODE=${1:-test}
SPECIFIC_TEST=$2

# Verificación de uv
if ! command -v uv &> /dev/null; then
    echo -e "${B_RED}❌ Error: 'uv' no está instalado. Por favor, instálalo primero.${NC}"
    exit 1
fi

TARGET_DIR="$HOME"
if [[ "$(uname -s)" == "Linux" && -d "$HOME/sgoinfre" ]]; then
    TARGET_DIR="$HOME/sgoinfre"
fi

VENV_PATH="$TARGET_DIR/.matrix_venv"
unset TEST_RESULTS
declare -a TEST_RESULTS=()
ALL_TESTS_PASSED=true

echo -e "\n${B_BLUE}╔═══════════════════════════════════╗${NC}"
echo -e   "${B_BLUE}║             MATRIX                ║${NC}"
echo -e   "${B_BLUE}╚═══════════════════════════════════╝${NC}"

if [[ "$MODE" == "clean" ]]; then
    echo -ne "${B_CYAN}🧹 Limpiando cachés y entorno virtual...${NC}"
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
    rm -rf "$VENV_PATH"
    echo -e " ${B_GREEN}Hecho.${NC}"
    exit 0
fi

# Creación del entorno virtual con uv
if [ ! -d "$VENV_PATH" ]; then
    echo -ne "${B_YELLOW}⚙️  Creando entorno virtual con uv...${NC}"
    uv venv "$VENV_PATH" > /dev/null 2>&1
    echo -e " ${B_GREEN}Hecho.${NC}"
fi

source "$VENV_PATH/bin/activate"

# Instalación ultrarrápida con uv pip
if [ -f "requirements.txt" ]; then
    echo -ne "${B_YELLOW}📦 Instalando dependencias con uv...${NC}"
    uv pip install -r requirements.txt > /dev/null 2>&1
    echo -e " ${B_GREEN}Hecho.${NC}"
fi

if [[ "$MODE" == "venv" ]]; then
    echo -e "\n${B_GREEN}✅ Entorno virtual preparado.${NC}"
    TMP_RC=$(mktemp)
    cat ~/.bashrc > "$TMP_RC" 2>/dev/null
    echo "source '$VENV_PATH/bin/activate'" >> "$TMP_RC"
    echo "export PYTHONPATH=\"\$PYTHONPATH:$(pwd)/src\"" >> "$TMP_RC"
    echo "rm -f '$TMP_RC'" >> "$TMP_RC"
    exec bash --rcfile "$TMP_RC"
else
    export PYTHONPATH=$PYTHONPATH:$(pwd)/src

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
        done
    fi

    echo -e "\n${B_BLUE}╔═══════════════════════════════════╗${NC}"
    echo -e "${B_BLUE}║          RESUMEN FINAL            ║${NC}"
    echo -e "${B_BLUE}╚═══════════════════════════════════╝${NC}\n"

    for result in "${TEST_RESULTS[@]}"; do
        echo -e "  $result"
    done

    if [ "$ALL_TESTS_PASSED" = true ]; then
        echo -e "\n${B_GREEN}✅ RESULTADO GLOBAL: TODO OK${NC}\n"
    else
        echo -e "\n${B_RED}❌ RESULTADO GLOBAL: ALGUNOS TESTS FALLARON${NC}\n"
    fi
fi