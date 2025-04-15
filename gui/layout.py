"""
Layout da interface gráfica do processador de XML
"""
import tkinter as tk
from tkinter import ttk


def criar_interface():
    """
    Cria a interface gráfica e retorna os elementos principais
    
    Returns:
        dict: Dicionário com os elementos da interface
    """
    # Criar a interface
    root = tk.Tk()
    root.title("Processador de Notas Fiscais XML")
    root.geometry("540x380")  # Tamanho para acomodar o notebook e a barra de status

    # Criar o notebook (abas)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Elementos da interface
    ui_elements = {'root': root, 'notebook': notebook}

    # Criar as abas
    _criar_aba_arquivo_unico(notebook, ui_elements)
    _criar_aba_processamento_lote(notebook, ui_elements)
    
    # Adiciona uma barra de status na janela principal
    _criar_barra_status(root, ui_elements)
    
    # Adiciona rodapé na janela principal
    ttk.Label(
        root, 
        text="Sistema de Processamento de Notas Fiscais XML v1.0", 
        font=("Arial", 8)
    ).pack(side=tk.BOTTOM, pady=5)
    
    return ui_elements


def _criar_aba_arquivo_unico(notebook, ui_elements):
    """
    Cria a aba para processamento de um único arquivo XML
    
    Args:
        notebook: Widget Notebook para adicionar a aba
        ui_elements: Dicionário para armazenar os elementos da interface
    """
    # Aba para processamento de arquivo único
    tab_arquivo = ttk.Frame(notebook)
    notebook.add(tab_arquivo, text="Arquivo Único")

    # Conteúdo da aba de arquivo único
    frame_arquivo = ttk.LabelFrame(
        tab_arquivo, 
        text="Selecione e processe um arquivo XML", 
        padding=(10, 5)
    )
    frame_arquivo.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Label(frame_arquivo, text="Arquivo XML:").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    
    entry_arquivo = ttk.Entry(frame_arquivo, width=50)
    entry_arquivo.grid(row=0, column=1, padx=5, pady=5)

    btn_selecionar_arquivo = ttk.Button(frame_arquivo, text="Selecionar")
    btn_selecionar_arquivo.grid(row=0, column=2, padx=5, pady=5)

    btn_processar_arquivo = ttk.Button(frame_arquivo, text="Processar Arquivo")
    btn_processar_arquivo.grid(row=1, column=1, pady=15)

    # Armazena os widgets no dicionário
    ui_elements.update({
        'tab_arquivo': tab_arquivo,
        'frame_arquivo': frame_arquivo,
        'entry_arquivo': entry_arquivo,
        'btn_selecionar_arquivo': btn_selecionar_arquivo,
        'btn_processar_arquivo': btn_processar_arquivo
    })


def _criar_aba_processamento_lote(notebook, ui_elements):
    """
    Cria a aba para processamento em lote de arquivos XML
    
    Args:
        notebook: Widget Notebook para adicionar a aba
        ui_elements: Dicionário para armazenar os elementos da interface
    """
    # Aba para processamento de pasta
    tab_pasta = ttk.Frame(notebook)
    notebook.add(tab_pasta, text="Processamento em Lote")

    # Conteúdo da aba de pasta
    frame_pasta = ttk.LabelFrame(
        tab_pasta, 
        text="Selecione e processe uma pasta com arquivos XML", 
        padding=(10, 5)
    )
    frame_pasta.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Label(frame_pasta, text="Pasta:").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    
    entry_pasta = ttk.Entry(frame_pasta, width=50)
    entry_pasta.grid(row=0, column=1, padx=5, pady=5)

    btn_selecionar_pasta = ttk.Button(frame_pasta, text="Selecionar")
    btn_selecionar_pasta.grid(row=0, column=2, padx=5, pady=5)

    btn_processar_pasta = ttk.Button(frame_pasta, text="Processar Pasta")
    btn_processar_pasta.grid(row=1, column=1, pady=15)

    # Área de informações sobre o processamento
    info_frame = ttk.LabelFrame(tab_pasta, text="Informações", padding=(10, 5))
    info_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    info_texto = """
    Este modo processa todos os arquivos XML encontrados na pasta selecionada.
    As planilhas serão geradas ou atualizadas com base no mês de emissão de cada nota.
    """
    ttk.Label(
        info_frame, 
        text=info_texto, 
        wraplength=480, 
        justify="left"
    ).pack(padx=5, pady=5)

    # Armazena os widgets no dicionário
    ui_elements.update({
        'tab_pasta': tab_pasta,
        'frame_pasta': frame_pasta,
        'entry_pasta': entry_pasta,
        'btn_selecionar_pasta': btn_selecionar_pasta,
        'btn_processar_pasta': btn_processar_pasta,
        'info_frame': info_frame
    })


def _criar_barra_status(root, ui_elements):
    """
    Cria a barra de status na parte inferior da janela
    
    Args:
        root: Janela principal da aplicação
        ui_elements: Dicionário para armazenar os elementos da interface
    """
    # Adiciona uma barra de status na janela principal
    status_frame = ttk.Frame(root, relief=tk.SUNKEN, border=1)
    status_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    status_label = ttk.Label(status_frame, text="", anchor=tk.W)
    status_label.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=2)
    
    ui_elements.update({
        'status_frame': status_frame,
        'status_label': status_label
    })