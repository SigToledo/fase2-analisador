# Projeto Fase 2 – Analisador Léxico e Sintático

Este repositório contém o projeto desenvolvido para a disciplina **Linguagens Formais e Compiladores (PUCPR – 2025/1)**, orientada pelo professor Frank Coelho de Alcântara.

---

## 📌 Descrição

O objetivo é implementar um **analisador léxico e sintático** em Python, capaz de:

- Ler expressões matemáticas em **notação pós-fixa (RPN)**
- Identificar e classificar os **tokens** (número, operador, comandos especiais)
- Verificar a **sintaxe** de cada linha, incluindo parênteses, estrutura e comandos válidos
- Emitir relatórios de erro léxico ou sintático quando necessário

---

## 🧠 Linguagem Reconhecida

- Números reais e inteiros
- Operadores: `+`, `-`, `*`, `/`, `%`, `^`, `|`
- Comandos especiais: `MEM`, `RES`
- Parênteses para aninhamento de expressões
- Estruturas personalizadas (a serem implementadas):
  - Laço: `for`
  - Condicional: `if ... then ... else`

---

## 📁 Estrutura de pastas

- fase2_analisador/
  - analisador/
    - analisador_lexico.py
    - analisador_sintatico.py
  - testes/
    - teste1.txt
  - docs/
    - MEF.png
  - main.py
  - README.md

---

## ✅ Como executar

1. Instale o Python 3.10 ou superior.
2. Execute o arquivo `main.py`:

```bash
python main.py
