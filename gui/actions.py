"""
Funções e ações da interface gráfica
"""
import os
import threading
from pathlib import Path
from tkinter import Tk, filedialog, messagebox

from config.config import config
from excel_export import gerar_planilha, processar_multiplos_xmls
from xml_parser import extrair_dados_xml


def selecionar_arquivo(entry):
    """
    Abre diálogo para seleção de arquivo XML e atualiza o campo de entrada
    
    Args:
        entry: Widget Entry para receber o caminho do arquivo
    """
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo XML",
        filetypes=[("Arquivos XML", "*.xml")]
    )
    if arquivo:
        entry.delete(0, 'end')
        entry.insert(0, arquivo)


def selecionar_pasta(entry):
    """
    Abre diálogo para seleção de pasta e atualiza o campo de entrada
    
    Args:
        entry: Widget Entry para receber o caminho da pasta
    """
    pasta = filedialog.askdirectory(title="Selecione a pasta com arquivos XML")
    if pasta:
        entry.delete(0, 'end')
        entry.insert(0, pasta)


def processar_arquivo(entry_arquivo, root, status_label):
    """
    Processa um único arquivo XML e atualiza a interface
    
    Args:
        entry_arquivo: Widget Entry com o caminho do arquivo
        root: Janela principal da aplicação
        status_label: Label para exibir o status do processamento
    """
    arquivo = entry_arquivo.get()
    if not arquivo:
        messagebox.showerror("Erro", "Selecione um arquivo XML")
        return
        
    try:
        caminho = Path(arquivo)
        if not caminho.exists():
            messagebox.showerror("Erro", f"O arquivo {arquivo} não existe!")
            return
            
        if caminho.suffix.lower() != '.xml':
            messagebox.showerror("Erro", f"O arquivo {arquivo} não é um XML válido!")
            return
        
        # Mostrar progresso
        status_label.config(text="Processando arquivo...")
        root.update_idletasks()
        
        # Executar o processamento em uma thread separada
        threading.Thread(
            target=_processar_arquivo_thread,
            args=(caminho, root, status_label)
        ).start()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        status_label.config(text="")


def _processar_arquivo_thread(caminho, root, status_label):
    """
    Thread para processamento de arquivo sem bloquear a interface
    
    Args:
        caminho: Caminho do arquivo XML
        root: Janela principal da aplicação
        status_label: Label para exibir o status do processamento
    """
    try:
        # Extrair dados para verificar se o XML é válido
        dados, data = extrair_dados_xml(caminho)
        if dados:
            # Gerar a planilha Excel
            caminho_planilha = gerar_planilha(caminho)
            
            if caminho_planilha:
                # Usar o after para atualizar a interface do usuário da thread principal
                root.after(0, lambda: mostrar_sucesso(dados, caminho_planilha, root))
            else:
                root.after(0, lambda: messagebox.showerror("Erro", "Não foi possível gerar a planilha Excel"))
        else:
            root.after(0, lambda: messagebox.showerror("Erro", "Não foi possível extrair dados do arquivo"))
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}"))
    finally:
        root.after(0, lambda: status_label.config(text=""))


def mostrar_sucesso(dados, caminho_planilha, root):
    """
    Exibe mensagem de sucesso e oferece opção de abrir a planilha gerada
    
    Args:
        dados: Dados processados do XML
        caminho_planilha: Caminho da planilha gerada
        root: Janela principal da aplicação
    """
    messagebox.showinfo("Sucesso", 
                      f"Arquivo processado com sucesso!\n"
                      f"{len(dados)} itens encontrados.\n"
                      f"Planilha salva em: {caminho_planilha}")
    # Oferecer opção para abrir a planilha
    if messagebox.askyesno("Abrir Arquivo", "Deseja abrir a planilha agora?"):
        os.startfile(caminho_planilha)


def processar_pasta(entry_pasta, root, status_label):
    """
    Processa todos os arquivos XML em uma pasta
    
    Args:
        entry_pasta: Widget Entry com o caminho da pasta
        root: Janela principal da aplicação
        status_label: Label para exibir o status do processamento
    """
    pasta = entry_pasta.get()
    if not pasta:
        messagebox.showerror("Erro", "Selecione uma pasta")
        return
        
    try:
        caminho = Path(pasta)
        if not caminho.exists():
            messagebox.showerror("Erro", f"A pasta {pasta} não existe!")
            return
            
        # Mostrar progresso
        status_label.config(text="Processando arquivos da pasta...")
        root.update_idletasks()
        
        # Executar o processamento em uma thread separada
        threading.Thread(
            target=_processar_pasta_thread,
            args=(caminho, root, status_label)
        ).start()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        status_label.config(text="")


def _processar_pasta_thread(caminho, root, status_label):
    """
    Thread para processamento de pasta sem bloquear a interface
    
    Args:
        caminho: Caminho da pasta contendo arquivos XML
        root: Janela principal da aplicação
        status_label: Label para exibir o status do processamento
    """
    try:
        planilhas = processar_multiplos_xmls(caminho)
        root.after(0, lambda: mostrar_resultado_pasta(planilhas, root))
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}"))
    finally:
        root.after(0, lambda: status_label.config(text=""))


def mostrar_resultado_pasta(planilhas, root):
    """
    Exibe resultado do processamento em lote e oferece opção para abrir pasta
    
    Args:
        planilhas: Lista com caminhos das planilhas geradas
        root: Janela principal da aplicação
    """
    if planilhas:
        messagebox.showinfo("Sucesso", 
                          f"Processamento concluído!\n"
                          f"{len(planilhas)} planilhas geradas/atualizadas.")
        
        # Oferecer opção para abrir a pasta de saída
        if messagebox.askyesno("Abrir Pasta", "Deseja abrir a pasta de planilhas?"):
            os.startfile(os.path.dirname(planilhas[0]))
    else:
        messagebox.showinfo("Aviso", "Nenhuma planilha foi gerada ou atualizada.")


def registrar_acoes(ui_elements):
    """
    Registra todas as ações nos elementos da interface
    
    Args:
        ui_elements (dict): Dicionário contendo os elementos da interface
    """
    # Registra ações para a aba de arquivo único
    ui_elements['btn_selecionar_arquivo'].config(
        command=lambda: selecionar_arquivo(ui_elements['entry_arquivo'])
    )
    ui_elements['btn_processar_arquivo'].config(
        command=lambda: processar_arquivo(
            ui_elements['entry_arquivo'], 
            ui_elements['root'],
            ui_elements['status_label']
        )
    )
    
    # Registra ações para a aba de processamento em lote
    ui_elements['btn_selecionar_pasta'].config(
        command=lambda: selecionar_pasta(ui_elements['entry_pasta'])
    )
    ui_elements['btn_processar_pasta'].config(
        command=lambda: processar_pasta(
            ui_elements['entry_pasta'], 
            ui_elements['root'],
            ui_elements['status_label']
        )
    )