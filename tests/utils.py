import sys

GREEN = "\033[0;32m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
YELLOW = "\033[1;33m"
BOLD = "\033[1m"
NC = "\033[0m"

PAD_LENGTH = 70


def print_header(ex_nb, title):
    print(f"\n{BLUE}{'=' * 80}{NC}")
    print(f"{BLUE}{BOLD}# EX {ex_nb:02} - {title.upper()}{NC}")
    print(f"{BLUE}{'=' * 80}{NC}")


def print_result(description, result, expected):
    is_correct = result == expected
    status = f"[{GREEN} OK {NC}]" if is_correct else f"[{RED}FAIL{NC}]"
    
    content = f"{description}: {result}"
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if i == len(lines) - 1:
            if len(lines) == 1:
                print(f" {YELLOW}•{NC} {line:<{PAD_LENGTH}} {status}")
            else:
                print(f"{line:<{PAD_LENGTH + 3}} {status}")
        else:
            if i == 0:
                print(f" {YELLOW}•{NC} {line}")
            else:
                print(f"{line}")

    return is_correct


def print_error(description, error_type, error_msg):
    status = f"[{CYAN}{error_type}{NC}]"

    print(f" {YELLOW}•{NC} {description:<{PAD_LENGTH}} {status}")
    print(f"   {BLUE}└── {error_msg}{NC}")


def print_final(exercise_nb, all_ok):
    ex_str = f"EX {exercise_nb:02}"
    if all_ok:
        status = f"{GREEN}✅ TODO OK{NC}"
        print(f"\n{BOLD}{ex_str}:{NC} {status}")
        print(f"{BLUE}{'-' * 80}{NC}\n")
    else:
        status = f"{RED}❌ ERRORES DETECTADOS{NC}"
        print(f"\n{BOLD}{ex_str}:{NC} {status}")
        print(f"{BLUE}{'-' * 80}{NC}\n")
        sys.exit(1)


def run_cases(ex_num: int, funcion_a_testear, casos: list, custom_desc_func=None):
    """
    Motor universal:
    - Formato de cada caso: ( (inputs), esperado )
    - inputs: Debe ser una tupla (arg1, arg2, ...)
    - esperado: El valor que debe devolver o None si se espera un error.
    """
    all_ok = True

    for inputs, expected in casos:
        args = inputs if isinstance(inputs, tuple) else (inputs,)

        if custom_desc_func:
            desc = custom_desc_func(*args)
        else:
            desc = f"{funcion_a_testear.__name__}{args}"

        try:
            res = funcion_a_testear(*args)

            if expected is None:
                print(f" {YELLOW}•{NC} {desc:<70} [{RED}FAIL{NC}]")
                print(f"    {RED}└── Se esperaba un error, pero devolvió: {res}{NC}")
                all_ok = False
            else:
                if not print_result(desc, res, expected):
                    all_ok = False

        except (ValueError, TypeError) as e:
            if expected is None:
                print_error(desc, "ERROR CAPTURADO", str(e))
            else:
                print_error(desc, "CRASH INESPERADO", str(e))
                all_ok = False
        except Exception as e:
            print_error(desc, "UNKNOWN CRASH", str(e))
            all_ok = False

    print_final(ex_num, all_ok)
