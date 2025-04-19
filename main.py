# main.py

from analisador.analisador_lexico import analisar_linha
from analisador.analisador_sintatico import analisar_sintaticamente

# Caminho do arquivo de teste
caminho = "testes/teste3.txt"

# Leitura do arquivo linha a linha
with open(caminho, 'r') as arquivo:
    linhas = [linha.strip() for linha in arquivo if linha.strip()]

# Processamento de cada linha
for i, linha in enumerate(linhas):
    linha_sem_comentario = linha.split('#')[0].strip()
    print(f"\nLinha {i + 1}: {linha_sem_comentario}")
    tokens = analisar_linha(linha_sem_comentario)  # Análise léxica
    for token in tokens:
        print("  ->", token)

    # Análise sintática
    if analisar_sintaticamente(tokens):
        print("  ✅ Expressão sintaticamente válida!")
    else:
        print("  ❌ Expressão inválida.")
