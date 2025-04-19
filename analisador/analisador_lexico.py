# analisador_lexico.py

import re

def analisar_linha(linha):
    tokens = []
    simbolos = linha.strip().split()
    pos = 0

    for simbolo in simbolos:
        if simbolo == '(':
            tokens.append({'valor': simbolo, 'classe': 'PAR_ABRE', 'posição': pos})
        elif simbolo == ')':
            tokens.append({'valor': simbolo, 'classe': 'PAR_FECHA', 'posição': pos})
        elif simbolo in ['+', '-', '*', '/', '%', '^', '|', '=']:
            tokens.append({'valor': simbolo, 'classe': 'OP', 'posição': pos})
        elif simbolo.upper() == 'MEM':
            tokens.append({'valor': simbolo, 'classe': 'MEM', 'posição': pos})
        elif simbolo.upper() == 'RES':
            tokens.append({'valor': simbolo, 'classe': 'RES', 'posição': pos})
        elif simbolo == 'for':
            tokens.append({'valor': simbolo, 'classe': 'FOR', 'posição': pos})
        elif simbolo == 'to':
            tokens.append({'valor': simbolo, 'classe': 'TO', 'posição': pos})
        elif simbolo == 'do':
            tokens.append({'valor': simbolo, 'classe': 'DO', 'posição': pos})
        elif re.match(r'^[a-zA-Z_]\w*$', simbolo):
            tokens.append({'valor': simbolo, 'classe': 'ID', 'posição': pos})
        elif re.match(r'^-?\d+(\.\d+)?$', simbolo):
            tokens.append({'valor': simbolo, 'classe': 'NUM', 'posição': pos})
        else:
            tokens.append({'valor': simbolo, 'classe': 'INVALIDO', 'posição': pos})
        pos += 1

    return tokens
