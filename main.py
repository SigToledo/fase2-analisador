# main.py

from analisador.analisador_lexico import analisar_linha

def main():
    caminho = "testes/teste1.txt"
    with open(caminho, "r") as f:
        for i, linha in enumerate(f):
            print(f"\nLinha {i + 1}: {linha.strip()}")
            tokens = analisar_linha(linha)
            for token in tokens:
                print(f"  -> {token}")

if __name__ == "__main__":
    main()
