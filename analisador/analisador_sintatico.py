# analisador_sintatico.py

# Este módulo define a estrutura básica do analisador sintático.
# Ele recebe uma lista de tokens do analisador léxico e verifica se a sequência é válida.

def analisar_sintaticamente(tokens):
    """
    Função principal que inicia a análise sintática com base na gramática esperada.
    Retorna True se a expressão for sintaticamente correta, ou False com mensagem de erro.
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
    """
    Expressões válidas:
    - ( NUM NUM OP )
    - ( NUM MEM ), ( NUM RES ), ( MEM )
    - ( ( EXPR ) ( EXPR ) OP )
    - ( for ID = NUM to NUM do ( EXPR ) )
    """
    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_ABRE':
        pos += 1  # Consome PAR_ABRE

        # FOR loop: ( for i = 1 to 3 do ( expr ) )
        if (pos + 8 < len(tokens) and
            tokens[pos]['valor'] == 'for' and
            tokens[pos + 1]['classe'] == 'ID' and
            tokens[pos + 2]['valor'] == '=' and
            tokens[pos + 3]['classe'] == 'NUM' and
            tokens[pos + 4]['valor'] == 'to' and
            tokens[pos + 5]['classe'] == 'NUM' and
            tokens[pos + 6]['valor'] == 'do' and
            tokens[pos + 7]['classe'] == 'PAR_ABRE'):

            pos = pos + 7  # pula até o '('
            pos = parse_expr(tokens, pos)  # analisa bloco interno
            if tokens[pos]['classe'] == 'PAR_FECHA':
                pos += 1
                if tokens[pos]['classe'] == 'PAR_FECHA':
                    return pos + 1
                else:
                    raise SyntaxError("Esperado ')' final após bloco do for")
            else:
                raise SyntaxError("Esperado ')' para fechar bloco do for")

        # Expressões curtas: (NUM MEM), (NUM RES), (MEM)
        if (pos + 1 < len(tokens) and
            tokens[pos]['classe'] == 'NUM' and tokens[pos + 1]['classe'] in ['MEM', 'RES'] and
            tokens[pos + 2]['classe'] == 'PAR_FECHA'):
            return pos + 3

        if (pos < len(tokens) and
            tokens[pos]['classe'] == 'MEM' and
            tokens[pos + 1]['classe'] == 'PAR_FECHA'):
            return pos + 2

        # Dois operandos + operador
        if pos < len(tokens):
            if tokens[pos]['classe'] == 'PAR_ABRE':
                pos = parse_expr(tokens, pos)
            elif tokens[pos]['classe'] in ['NUM', 'MEM', 'RES']:
                pos += 1
            else:
                raise SyntaxError(f"Operando 1 inválido: {tokens[pos]['valor']}")

        if pos < len(tokens):
            if tokens[pos]['classe'] == 'PAR_ABRE':
                pos = parse_expr(tokens, pos)
            elif tokens[pos]['classe'] in ['NUM', 'MEM', 'RES']:
                pos += 1
            else:
                raise SyntaxError(f"Operando 2 inválido: {tokens[pos]['valor']}")

        if pos < len(tokens) and tokens[pos]['classe'] == 'OP':
            pos += 1
        else:
            raise SyntaxError("Esperado operador após dois operandos")

        if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_FECHA':
            return pos + 1
        else:
            raise SyntaxError("Esperado PAR_FECHA")

    raise SyntaxError(f"Expressão inválida a partir do token {tokens[pos]['valor']} (classe {tokens[pos]['classe']})")
