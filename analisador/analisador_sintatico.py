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
    """
    if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_ABRE':
        pos += 1  # Consome PAR_ABRE

        if pos < len(tokens):
            # (NUM MEM)
            if (pos + 1 < len(tokens) and
                tokens[pos]['classe'] == 'NUM' and
                tokens[pos + 1]['classe'] == 'MEM'):
                pos += 2

            # (NUM RES)
            elif (pos + 1 < len(tokens) and
                  tokens[pos]['classe'] == 'NUM' and
                  tokens[pos + 1]['classe'] == 'RES'):
                pos += 2

            # (MEM)
            elif tokens[pos]['classe'] == 'MEM' and (pos + 1 < len(tokens) and tokens[pos + 1]['classe'] == 'PAR_FECHA'):
                pos += 1

            # (NUM NUM OP), (MEM NUM OP), (RES NUM OP), etc.
            elif (pos + 2 < len(tokens) and
                  tokens[pos]['classe'] in ['NUM', 'MEM', 'RES', 'PAR_ABRE'] and
                  tokens[pos + 1]['classe'] in ['NUM', 'MEM', 'RES', 'PAR_ABRE'] and
                  tokens[pos + 2]['classe'] == 'OP'):
                for i in range(2):
                    if tokens[pos]['classe'] == 'PAR_ABRE':
                        pos = parse_expr(tokens, pos)
                    else:
                        pos += 1
                pos += 1  # Consome o operador

            # Subexpressão única ( (expr) )
            elif tokens[pos]['classe'] == 'PAR_ABRE':
                pos = parse_expr(tokens, pos)

            else:
                raise SyntaxError(f"Expressão inesperada após '(': {tokens[pos]['valor']}")

        if pos < len(tokens) and tokens[pos]['classe'] == 'PAR_FECHA':
            return pos + 1  # Consome PAR_FECHA
        else:
            raise SyntaxError("Esperado PAR_FECHA")

    raise SyntaxError(f"Expressão inválida a partir do token {tokens[pos]['valor']} (classe {tokens[pos]['classe']})")
