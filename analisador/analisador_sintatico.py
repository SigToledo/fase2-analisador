# analisador_sintatico.py

# Este módulo define a estrutura básica do analisador sintático.
# Ele recebe uma lista de tokens do analisador léxico e verifica se a sequência é válida.

def analisar_sintaticamente(tokens):
    """
    Função principal que inicia a análise sintática com base na gramática esperada.
    Retorna True se a expressão for sintaticamente correta, ou False com mensagem de erro.
    A análise considera expressões aritméticas, comandos com memória, e estruturas de repetição 'for'.
    """
    try:
        pos = 0
        pos = parse_expr(tokens, pos)  # tenta consumir uma expressão completa
        if pos == len(tokens):
            return True  # todos os tokens foram consumidos com sucesso
        else:
            raise SyntaxError(f"Tokens restantes após análise. Esperado fim, mas sobrou: {tokens[pos:]}")
    except SyntaxError as e:
        print(f"Erro sintático: {e}")
        return False

def parse_expr(tokens, pos):
    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_ABRE':
        pos += 1  # Consome PAR_ABRE

        if is_for_loop(tokens, pos):
            return parse_for_loop(tokens, pos)

        if is_short_expr(tokens, pos):
            return parse_short_expr(tokens, pos)

        return parse_binary_expr(tokens, pos)

    raise SyntaxError("Expressão mal formada ou inesperada")

def is_for_loop(tokens, pos):
    return (pos + 6 < len(tokens) and
            tokens[pos]['classe'] == 'FOR' and
            tokens[pos + 1]['classe'] == 'ID' and
            tokens[pos + 2]['classe'] == 'OP' and tokens[pos + 2]['valor'] == '=' and
            tokens[pos + 3]['classe'] == 'NUM' and
            tokens[pos + 4]['classe'] == 'TO' and
            tokens[pos + 5]['classe'] == 'NUM' and
            tokens[pos + 6]['classe'] == 'DO')

def parse_for_loop(tokens, pos):
    pos += 7

    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_ABRE':
        pos = parse_expr(tokens, pos)
    else:
        raise SyntaxError("Esperado '(' antes da expressão do corpo do for")

    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_FECHA':
        pos += 1
    else:
        raise SyntaxError("Esperado ')' para fechar bloco do for")

    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_FECHA':
        pos += 1
    else:
        raise SyntaxError("Esperado ')' final do comando for")

    return pos

def is_short_expr(tokens, pos):
    return ((pos + 2 < len(tokens) and
             tokens[pos]['classe'] in ['NUM', 'ID'] and tokens[pos + 1]['classe'] in ['MEM', 'RES'] and
             tokens[pos + 2]['classe'] == 'PAR_FECHA') or
            (pos + 1 < len(tokens) and
             tokens[pos]['classe'] in ['MEM', 'ID'] and
             tokens[pos + 1]['classe'] == 'PAR_FECHA'))

def parse_short_expr(tokens, pos):
    if tokens[pos + 1]['classe'] in ['MEM', 'RES']:
        return pos + 3
    return pos + 2

def parse_binary_expr(tokens, pos):
    expr_stack = []

    for i in range(2):
        if pos < len(tokens):
            if tokens[pos]['classe'] == 'PAR_ABRE':
                pos = parse_expr(tokens, pos)
                expr_stack.append('EXPR')
            elif tokens[pos]['classe'] in ['NUM', 'MEM', 'RES', 'ID']:
                expr_stack.append(tokens[pos]['classe'])
                pos += 1
            else:
                raise SyntaxError(f"Operando {i + 1} inválido: {tokens[pos]['valor']}")
        else:
            raise SyntaxError(f"Esperado operando {i + 1}, mas a expressão terminou")

    if pos < len(tokens) and tokens[pos]['classe'] == 'OP':
        pos += 1
    else:
        raise SyntaxError("Esperado operador após dois operandos")

    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_FECHA':
        return pos + 1
    else:
        raise SyntaxError("Esperado PAR_FECHA")
