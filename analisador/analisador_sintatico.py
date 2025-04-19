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
    Expressão válida: ( expr ) ou comandos como (NUM NUM OP), (NUM MEM), (NUM RES), (MEM), (RES NUM OP)
    Também suporta expressões aninhadas como ((EXPR) (EXPR) OP)
    """
    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_ABRE':
        pos += 1  # Consome PAR_ABRE

        # Verifica expressões curtas como (NUM MEM), (NUM RES), (MEM)
        if (pos + 1 < len(tokens) and
            tokens[pos]['classe'] == 'NUM' and tokens[pos + 1]['classe'] in ['MEM', 'RES'] and
            tokens[pos + 2]['classe'] == 'PAR_FECHA'):
            return pos + 3

        if (pos < len(tokens) and
            tokens[pos]['classe'] == 'MEM' and
            tokens[pos + 1]['classe'] == 'PAR_FECHA'):
            return pos + 2

        # Tenta consumir primeiro operando (pode ser expressão ou token simples)
        if pos < len(tokens):
            if tokens[pos]['classe'] == 'PAR_ABRE':
                pos = parse_expr(tokens, pos)
            elif tokens[pos]['classe'] in ['NUM', 'MEM', 'RES']:
                pos += 1
            else:
                raise SyntaxError(f"Operando 1 inválido: {tokens[pos]['valor']}")

        # Tenta consumir segundo operando (também pode ser expressão ou token simples)
        if pos < len(tokens):
            if tokens[pos]['classe'] == 'PAR_ABRE':
                pos = parse_expr(tokens, pos)
            elif tokens[pos]['classe'] in ['NUM', 'MEM', 'RES']:
                pos += 1
            else:
                raise SyntaxError(f"Operando 2 inválido: {tokens[pos]['valor']}")

        # Tenta consumir operador
        if pos < len(tokens) and tokens[pos]['classe'] == 'OP':
            pos += 1
        else:
            raise SyntaxError("Esperado operador após dois operandos")

        # Verifica PAR_FECHA
        if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_FECHA':
            return pos + 1
        else:
            raise SyntaxError("Esperado PAR_FECHA")

    raise SyntaxError(f"Expressão inválida a partir do token {tokens[pos]['valor']} (classe {tokens[pos]['classe']})")