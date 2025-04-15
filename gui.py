"""
Ponto de entrada para a interface gráfica do processador de XML
"""

from gui.actions import registrar_acoes
from gui.layout import criar_interface


def iniciar_gui():
    """
    Inicializa e executa a interface gráfica
    """
    # Cria os elementos da interface
    ui_elements = criar_interface()
    
    # Registra as funções/callbacks nos elementos da interface
    registrar_acoes(ui_elements)
    
    # Inicia o loop principal da interface gráfica
    root = ui_elements['root']
    root.mainloop()


if __name__ == "__main__":
    iniciar_gui()