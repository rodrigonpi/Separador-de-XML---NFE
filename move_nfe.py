import os                                   # Para manipulação de arquivos e diretórios
import shutil                               # Para mover arquivos
import xml.etree.ElementTree as ET          # Para ler e interpretar arquivos XML
import customtkinter as ctk                 # Interface gráfica moderna (baseada em tkinter)
from tkinter import filedialog, messagebox  # Janelas de seleção e mensagens pop-up

# Função para extrair namespace do XML
def get_namespace(element):
    if element.tag.startswith('{'):
        return element.tag.split('}')[0].strip('{')   # Extrai apenas o namespace entre {}
    return ''                                         # Retorna vazio se não houver namespace

# Função principal de processamento
def mover_xmls():
    origem = pasta_origem.get()             # Lê a pasta de origem selecionada na interface
    destino = pasta_destino.get()           # Lê a pasta de destino selecionada
    
    # Verifica se ambas as pastas foram selecionadas
    if not origem or not destino:
        messagebox.showwarning("Atenção", "Selecione as pastas de origem e destino.")
        return
    
    # Lista apenas arquivos .xml na pasta de origem
    arquivos = [f for f in os.listdir(origem) if f.endswith('.xml')]
    total = len(arquivos)
    if total == 0:
        messagebox.showinfo("Info", "Nenhum arquivo XML encontrado.")
        return

    progresso.set(0)                         # Zera a barra de progresso
    barra_progresso.update()                 # Atualiza visualmente

    processados = 0                          # Contador de arquivos lidos
    movidos = 0                              # Contador de arquivos movidos

    # Itera sobre todos os arquivos XML
    for i, arquivo in enumerate(arquivos, 1):
        caminho_arquivo = os.path.join(origem, arquivo)

        try:
            tree = ET.parse(caminho_arquivo) # Faz parsing do XML
            root = tree.getroot()

            ns = get_namespace(root)         # Descobre o namespace
            nsmap = {'ns': ns} if ns else {}

            # Tenta encontrar a tag <tpNF>, com ou sem namespace
            tpNF = root.find('.//ns:tpNF', nsmap) if ns else root.find('.//tpNF')

            processados += 1

            # Se encontrou e o valor for '0', move o arquivo
            if tpNF is not None and tpNF.text.strip() == '0':
                shutil.move(caminho_arquivo, os.path.join(destino, arquivo))
                movidos += 1

        except ET.ParseError:
            print(f"Erro ao ler XML: {arquivo}")

        progresso.set(i / total)             # Atualiza barra de progresso
        barra_progresso.update()             # Redesenha na interface

    # Exibe resumo do processo em pop-up
    messagebox.showinfo("Finalizado", f"Arquivos processados: {processados}\nMovidos: {movidos}")
    app.destroy()  # <- Fecha o aplicativo após concluir
# Funções para selecionar pastas
def selecionar_origem():
    caminho = filedialog.askdirectory(title="Selecione a pasta de origem")
    pasta_origem.set(caminho)               # Atualiza o campo da interface com o caminho escolhido

def selecionar_destino():
    caminho = filedialog.askdirectory(title="Selecione a pasta de destino")
    pasta_destino.set(caminho)

# Início da interface com customtkinter
# Define o tema visual: claro ou escuro
ctk.set_appearance_mode("system")            # Pode usar "dark" também
ctk.set_default_color_theme("blue")         # Tema de cores base


app = ctk.CTk()                             # Cria a janela principal
app.title("Mover NF-es - Emissão Propria")  # Título da janela
app.geometry("500x350")                     # Define tamanho da janela


# Variáveis
pasta_origem = ctk.StringVar()              # Armazena a pasta de origem selecionada
pasta_destino = ctk.StringVar()             # Armazena a pasta de destino
progresso = ctk.DoubleVar()                 # Armazena o valor da barra de progresso (0 a 1)

# Elementos visuais
ctk.CTkLabel(app, text="Selecione a pasta de origem:").pack(pady=(20, 5))
ctk.CTkEntry(app, textvariable=pasta_origem, width=350).pack()
ctk.CTkButton(app, text="Escolher pasta", command=selecionar_origem).pack(pady=5)

ctk.CTkLabel(app, text="Selecione a pasta de destino:").pack(pady=(20, 5))
ctk.CTkEntry(app, textvariable=pasta_destino, width=350).pack()
ctk.CTkButton(app, text="Escolher pasta", command=selecionar_destino).pack(pady=5)

ctk.CTkLabel(app, text="Progresso:").pack(pady=(20, 5))
barra_progresso = ctk.CTkProgressBar(app, variable=progresso, width=400)
barra_progresso.pack()

ctk.CTkButton(app, text="Iniciar processamento", command=mover_xmls, fg_color="#0C6D0F", hover_color="#0C6D0F").pack(pady=10)

app.mainloop()
