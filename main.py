import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import ast
import re
import os

from lexer import lexer
from parser_ import Parser
from semantic import semantic_check
from ir_generator import generate_ir
from optimizer import optimize
from executor import execute


# Lista de funções math aceitas
ALLOWED_FUNCS = {
    "sqrt","pow","exp","log","log10","sin","cos","tan",
    "floor","ceil","modf","remainder","isqrt","fmod","trunc",
    "degrees","radians","cbrt"
}


class ComPyleInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("ComPyle - Compilador Matemático (.py)")
        self.root.configure(bg="#0B223A")

        self.top_frame = tk.Frame(root, bg="#0B223A", pady=10)
        self.top_frame.pack()

        # ==========================
        # LOGO (com verificação automática)
        # ==========================
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(current_dir, "logo.png")

            if not os.path.exists(logo_path):
                raise FileNotFoundError(f"Logo não encontrada em: {logo_path}")

            img = Image.open(logo_path)
            img = img.resize((200, 200))
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(self.top_frame, image=self.logo_img, bg="#0B223A").pack(pady=10)

        except Exception as e:
            print(f"⚠️ Erro ao carregar logo: {e}")
            tk.Label(
                self.top_frame,
                text="[LOGO COMPILE AQUI]",
                font=("Arial", 16, "bold"),
                fg="white",
                bg="#0B223A"
            ).pack(pady=10)

        # ==========================
        # INTERFACE PRINCIPAL
        # ==========================
        self.center_frame = tk.Frame(root, bg="#0B223A", pady=20)
        self.center_frame.pack()

        tk.Label(
            self.center_frame,
            text="Selecione um arquivo .py para compilar:",
            font=("Arial", 12),
            fg="white",
            bg="#0B223A"
        ).pack()

        self.file_path = tk.StringVar()
        tk.Entry(
            self.center_frame,
            textvariable=self.file_path,
            width=50,
            font=("Arial", 12)
        ).pack(pady=5)

        tk.Button(
            self.center_frame,
            text="Procurar Arquivo",
            command=self.escolher_arquivo,
            bg="#1C3A5E",
            fg="white",
            activebackground="#2B5A88",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(pady=5)

        tk.Button(
            self.center_frame,
            text="Compilar Arquivo .py",
            command=self.compilar_arquivo_py,
            bg="#1C5E2B",
            fg="white",
            activebackground="#2A8B45",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(pady=10)

        tk.Button(
            self.center_frame,
            text="Limpar Saída",
            command=self.limpar_saida,
            bg="#5E1C1C",
            fg="white",
            activebackground="#8B2A2A",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(pady=5)

        # ==========================
        # CAIXA DE RESULTADO
        # ==========================
        self.result_frame = tk.Frame(root, bg="#0B223A")
        self.result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_box = tk.Text(
            self.result_frame,
            height=18,
            bg="white",
            fg="black",
            font=("Courier", 10),
            wrap=tk.WORD
        )
        self.result_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # ------------------------------------------------------------
    # FUNÇÕES DE INTERFACE
    # ------------------------------------------------------------
    def escolher_arquivo(self):
        path = filedialog.askopenfilename(
            title="Selecione um arquivo Python",
            filetypes=[("Python files", "*.py"), ("Todos os arquivos", "*.*")]
        )
        if path:
            self.file_path.set(path)

    def limpar_saida(self):
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete(1.0, tk.END)
        self.result_box.config(state=tk.DISABLED)

    def mostrar_resultado(self, texto):
        self.result_box.config(state=tk.NORMAL)
        self.result_box.insert(tk.END, texto + "\n" + "-" * 60 + "\n\n")
        self.result_box.config(state=tk.DISABLED)
        self.result_box.see(tk.END)

    # ------------------------------------------------------------
    # LÓGICA DE LEITURA E COMPILAÇÃO DE ARQUIVO .PY
    # ------------------------------------------------------------
    def compilar_arquivo_py(self):
        caminho = self.file_path.get().strip()
        if not caminho:
            messagebox.showwarning("Atenção", "Selecione um arquivo .py primeiro.")
            return

        try:
            with open(caminho, "r", encoding="utf-8") as f:
                src = f.read()
        except Exception as e:
            self.mostrar_resultado(f"Erro ao abrir o arquivo: {e}")
            return

        expressoes = self.extrair_expressoes_math(src)
        if not expressoes:
            self.mostrar_resultado("Nenhuma expressão matemática compatível encontrada no arquivo.")
            return

        for i, expr in enumerate(expressoes, 1):
            try:
                resultado = self.compilar_expressao(expr, i)
                self.mostrar_resultado(resultado)
            except Exception as e:
                self.mostrar_resultado(f"Erro ao compilar a expressão {i} ('{expr}'): {e}")

    def extrair_expressoes_math(self, codigo_src):
        """
        Usa o módulo AST para encontrar expressões com chamadas às funções math.
        Remove 'math.' e 'print(...)' se necessário.
        """
        tree = ast.parse(codigo_src)
        expressoes = []

        for node in tree.body:
            # Se for atribuição (ex: x = math.sqrt(9))
            if isinstance(node, ast.Assign) and self._tem_funcao_permitida(node.value):
                expr = self._limpar_expressao(node.value)
                expressoes.append(expr)

            # Se for apenas uma expressão (ex: print(math.sin(1)))
            elif isinstance(node, ast.Expr):
                val = node.value
                if isinstance(val, ast.Call):
                    # se for print(math.xxx)
                    if isinstance(val.func, ast.Name) and val.func.id == "print" and val.args:
                        if self._tem_funcao_permitida(val.args[0]):
                            expr = self._limpar_expressao(val.args[0])
                            expressoes.append(expr)
                    elif self._tem_funcao_permitida(val):
                        expr = self._limpar_expressao(val)
                        expressoes.append(expr)

        # remove duplicadas mantendo a ordem
        unicas = []
        [unicas.append(e) for e in expressoes if e not in unicas]
        return unicas

    def _tem_funcao_permitida(self, node):
        """Verifica se há chamadas às funções math permitidas dentro do nó AST."""
        for n in ast.walk(node):
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name) and n.func.id in ALLOWED_FUNCS:
                    return True
                if isinstance(n.func, ast.Attribute) and n.func.attr in ALLOWED_FUNCS:
                    return True
        return False

    def _limpar_expressao(self, node):
        """Remove 'math.' e converte AST de volta para texto legível."""
        try:
            expr_src = ast.unparse(node)
        except Exception:
            expr_src = str(node)
        expr_src = re.sub(r"\bmath\.", "", expr_src)
        if expr_src.startswith("print(") and expr_src.endswith(")"):
            expr_src = expr_src[6:-1]
        return expr_src.strip()

    def compilar_expressao(self, expressao, idx):
        saida = f"\n================ EXPRESSÃO {idx} ================\n{expressao}\n\n"
        tokens = lexer(expressao)
        saida += "=== Etapa 1: Análise Léxica ===\n"
        saida += f"{tokens}\n\n"

        parser = Parser(tokens)
        arvore = parser.parse()
        saida += "=== Etapa 2: Análise Sintática ===\n"
        saida += f"{arvore}\n\n"

        semantic_check(arvore)
        saida += "=== Etapa 3: Análise Semântica ===\n"
        saida += "Semântica válida\n\n"

        ir, _ = generate_ir(arvore)
        saida += "=== Etapa 4: Geração de Código Intermediário ===\n"
        for instr in ir:
            saida += f"{instr}\n"
        saida += "\n"

        ir_otimizado = optimize(ir)
        saida += "=== Etapa 5: Otimização ===\n"
        for instr in ir_otimizado:
            saida += f"{instr}\n"
        saida += "\n"

        resultado_env = execute(ir_otimizado)
        resultado = list(resultado_env.values())[-1] if resultado_env else None
        saida += "=== Etapa 6: Execução ===\n"
        saida += f"Resultado final: {resultado}\n"
        return saida


if __name__ == "__main__":
    root = tk.Tk()
    app = ComPyleInterface(root)
    root.geometry("800x700")
    root.mainloop()
