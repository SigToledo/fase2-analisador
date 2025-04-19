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
    Expressão válida: ( expr )  ou  NUM NUM OP  ou  RES NUM OP  etc.
    """
    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_ABRE':
        pos += 1
        pos = parse_expr(tokens, pos)
        if tokens[pos]['classe'] == 'PAR_FECHA':
            return pos + 1
        else:
            raise SyntaxError("Esperado PAR_FECHA")

    elif pos + 2 < len(tokens):
        # Padrões como NUM NUM OP ou MEM NUM OP etc.
        if tokens[pos]['classe'] in ['NUM', 'MEM', 'RES'] and \
           tokens[pos + 1]['classe'] in ['NUM', 'MEM', 'RES'] and \
           tokens[pos + 2]['classe'] == 'OP':
            return pos + 3

    raise SyntaxError(f"Expressão inválida a partir do token {tokens[pos]['valor']} (classe {tokens[pos]['classe']})")
