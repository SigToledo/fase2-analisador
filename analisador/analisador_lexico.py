# analisador_lexico.py

def classificar_token(token):
    if token.isdigit() or is_float(token):
        return "NUM"
    elif token in {"+", "-", "*", "/", "%", "^", "|"}:
        return "OP"
    elif token == "MEM":
        return "MEM"
    elif token == "RES":
        return "RES"
    elif token == "(":
        return "PAR_ABRE"
    elif token == ")":
        return "PAR_FECHA"
    else:
        return "INVALIDO"

def is_float(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

def analisar_linha(linha):
    tokens = linha.strip().split()
    resultado = []
    for pos, token in enumerate(tokens):
        classe = classificar_token(token)
        resultado.append({
            "valor": token,
            "classe": classe,
            "posição": pos
        })
    return resultado
