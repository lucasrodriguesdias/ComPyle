# 🐍 ComPyle – Compilador Matemático em Python

![Logo do ComPyle](logo.png)

O **ComPyle** é um compilador educacional desenvolvido em **Python**, capaz de **analisar, otimizar e executar expressões matemáticas** escritas em código.  
Ele foi criado com o objetivo de **demonstrar visualmente o processo de compilação**, passando por todas as etapas fundamentais de um compilador real.

---

## ⚙️ Funcionalidades

- 🧠 **Leitura automática de arquivos `.py`**
- 🔍 **Análise Léxica:** tokenização dos elementos da expressão  
- 🧩 **Análise Sintática:** construção da árvore de derivação  
- ✅ **Análise Semântica:** validação de funções e operações permitidas  
- ⚡ **Geração de Código Intermediário (IR)**
- 🧮 **Otimização de Instruções**
- 🚀 **Execução e exibição do resultado final**
- 🎨 **Interface Gráfica (Tkinter)** com exibição das etapas e saída formatada

---

## 🧮 Funções matemáticas suportadas

O ComPyle reconhece e explica automaticamente as seguintes funções do módulo `math`:

sqrt, pow, exp, log, log10, sin, cos, tan,
floor, ceil, modf, remainder, isqrt, fmod, trunc,
degrees, radians, cbrt

yaml
Copiar código

---

## 🖥️ Interface

A interface gráfica foi construída com **Tkinter**, utilizando o tema escuro e elementos estilizados.  
É possível selecionar um **arquivo `.py`** que contenha expressões matemáticas, e o compilador irá:

1. Extrair automaticamente as funções `math`
2. Exibir todas as etapas do processo de compilação
3. Mostrar o **resultado final da execução**

![Tela do ComPyle](screenshot.png)

---

## 📁 Estrutura do Projeto

```plaintext
Compyle/
 ├── lexer.py
 ├── parser_.py
 ├── semantic.py
 ├── ir_generator.py
 ├── optimizer.py
 ├── executor.py
 ├── main.py
 ├── logo.png
 ├── test.py
 └── README.md
🚀 Como executar
🐍 Pré-requisitos
Python 3.9+

Biblioteca Pillow (para exibir a logo)

Instale o Pillow com o comando:

bash
Copiar código
pip install pillow
▶️ Executar a Interface Gráfica
Na pasta principal do projeto, execute:

bash
Copiar código
python main.py
Passos:

Clique em “Procurar Arquivo”

Selecione um arquivo .py (exemplo: test.py)

Clique em “Compilar Arquivo .py”

Acompanhe todas as etapas da compilação na área branca inferior

🧾 Exemplo de arquivo test.py
python
Copiar código
import math

a = math.sqrt(9)
b = math.pow(2, 5) + math.log10(100)
print(math.sin(1.57) + math.cos(0))
resultado = math.cbrt(27) + math.trunc(3.9)
🧠 Conceitos Envolvidos
Etapa	Descrição
Léxica	Reconhecimento dos tokens (números, operadores, nomes)
Sintática	Construção da árvore de análise
Semântica	Validação de funções e variáveis
Intermediário	Tradução para instruções IR
Otimização	Simplificação de código redundante
Execução	Cálculo e exibição do resultado

👨‍💻 Autor
Lucas Rodrigues Dias
📍 Desenvolvedor & Estudante de Sistemas de Informação
💼 GitHub: @lucasrodriguesdias
✉️ E-mail: adicione seu contato aqui, se quiser

🪪 Licença
Este projeto foi desenvolvido para fins educacionais e demonstração prática de conceitos de compiladores.
Licença livre para uso e modificação, desde que citada a fonte original.

