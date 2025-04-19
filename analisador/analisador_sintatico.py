# analisador_sintatico.py

# Este módulo define a estrutura básica do analisador sintático.
# Ele recebe uma lista de tokens do analisador léxico e verifica se a sequência é válida.

def analisar_sintaticamente(tokens):
    """
    Inicia a análise sintática com base na gramática esperada.

    Parâmetros:
    - tokens: lista de dicionários no formato {'valor': str, 'classe': str, 'posição': int}

    Retorno:
    - True se a expressão for sintaticamente válida.
    - False, imprimindo mensagem de erro, caso contrário.

    Exemplo de uso:
    >>> tokens = [
    ...     {'valor': '(', 'classe': 'PAR_ABRE', 'posição': 0},
    ...     {'valor': '3', 'classe': 'NUM', 'posição': 1},
    ...     {'valor': '4', 'classe': 'NUM', 'posição': 2},
    ...     {'valor': '+', 'classe': 'OP', 'posição': 3},
    ...     {'valor': ')', 'classe': 'PAR_FECHA', 'posição': 4}
    ... ]
    >>> analisar_sintaticamente(tokens)
    True
    """
    try:
        if not verificar_balanceamento(tokens):
            raise SyntaxError("Parênteses desbalanceados na expressão")

        return verificar_estrutura(tokens)
    except SyntaxError as e:
        print(f"Erro sintático: {e}")
        return False

def verificar_balanceamento(tokens):
    """
    Verifica se os parênteses estão balanceados ao longo da expressão.
    """
    count = 0
    for token in tokens:
        if token['classe'] == 'PAR_ABRE':
            count += 1
        elif token['classe'] == 'PAR_FECHA':
            count -= 1
        if count < 0:
            return False  # Fechou mais do que abriu
    return count == 0

def verificar_estrutura(tokens):
    """
    Verifica se a estrutura sintática dos tokens está de acordo com a gramática.
    """
    pos = parse_expr(tokens, 0)
    if pos == len(tokens):
        return True
    raise SyntaxError(f"Tokens restantes após análise. Esperado fim, mas sobrou: {tokens[pos:]}")

def parse_expr(tokens, pos):
    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_ABRE':
        pos += 1  # Consome PAR_ABRE

        if (pos + 6 < len(tokens) and
            tokens[pos]['classe'] == 'FOR' and
            tokens[pos + 1]['classe'] == 'ID' and
            tokens[pos + 2]['classe'] == 'OP' and tokens[pos + 2]['valor'] == '=' and
            tokens[pos + 3]['classe'] == 'NUM' and
            tokens[pos + 4]['classe'] == 'TO' and
            tokens[pos + 5]['classe'] == 'NUM' and
            tokens[pos + 6]['classe'] == 'DO'):
            return parse_for_loop(tokens, pos)

        if (pos + 2 < len(tokens) and
            tokens[pos]['classe'] in ['NUM', 'ID'] and tokens[pos + 1]['classe'] in ['MEM', 'RES'] and
            tokens[pos + 2]['classe'] == 'PAR_FECHA'):
            return pos + 3

        if (pos + 1 < len(tokens) and
            tokens[pos]['classe'] in ['MEM', 'ID'] and
            tokens[pos + 1]['classe'] == 'PAR_FECHA'):
            return pos + 2

        return parse_operacao(tokens, pos)

    raise SyntaxError("Expressão mal formada ou inesperada")

def parse_for_loop(tokens, pos):
    """
    Processa estruturas do tipo: ( for ID = NUM to NUM do ( EXPR ) )
    """
    pos += 7  # Consome for, ID, =, NUM, to, NUM, do

    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_ABRE':
        pos = parse_expr(tokens, pos)
    else:
        raise SyntaxError("Esperado '(' antes da expressão do corpo do for")

    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_FECHA':
        return pos + 1
    else:
        raise SyntaxError("Esperado ')' final do comando for")

def parse_operacao(tokens, pos):
    """
    Processa operações do tipo: ( EXPR EXPR OP )
    """
    expr_stack = []
    for _ in range(2):
        if pos < len(tokens):
            if tokens[pos]['classe'] == 'PAR_ABRE':
                pos = parse_expr(tokens, pos)
                expr_stack.append('EXPR')
            elif tokens[pos]['classe'] in ['NUM', 'MEM', 'RES', 'ID']:
                expr_stack.append(tokens[pos]['classe'])
                pos += 1
            else:
                raise SyntaxError(f"Operando {_+1} inválido: {tokens[pos]['valor']}")
        else:
            raise SyntaxError(f"Esperado operando {_+1}, mas a expressão terminou")

    if pos < len(tokens) and tokens[pos]['classe'] == 'OP':
        pos += 1
    else:
        raise SyntaxError("Esperado operador após dois operandos")

    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_FECHA':
        return pos + 1
    else:
        raise SyntaxError("Esperado PAR_FECHA")
