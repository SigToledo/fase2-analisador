# main.py

from analisador.analisador_lexico import analisar_linha
from analisador.analisador_sintatico import analisar_sintaticamente

# Caminho do arquivo de teste
caminho = "testes/teste1.txt"

# Leitura do arquivo linha a linha
with open(caminho, 'r') as arquivo:
    linhas = [linha.strip() for linha in arquivo if linha.strip()]

# Processamento de cada linha
for i, linha in enumerate(linhas):
    print(f"\nLinha {i + 1}: {linha}")
    tokens = analisar_linha(linha)  # Análise léxica
    for token in tokens:
        print("  ->", token)

    # Análise sintática
    if analisar_sintaticamente(tokens):
        print("  ✅ Expressão sintaticamente válida!")
    else:
        print("  ❌ Expressão inválida.")
