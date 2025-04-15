import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import xmltodict

ROOT_DIR = Path(__file__).parent.resolve()

def ler_arquivo_xml(caminho_arquivo: Union[str, Path]) -> Optional[Dict]:
    """
    Lê um arquivo XML e converte para um dicionário Python.
    
    Args:
        caminho_arquivo: Caminho para o arquivo XML
        
    Returns:
        Dicionário com os dados do XML ou None em caso de erro
    """
    try:
        caminho = Path(caminho_arquivo)
        if not caminho.is_file():
            print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
            return None
            
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
        
        return xmltodict.parse(conteudo)
    
    except Exception as e:
        print(f"Erro ao ler o arquivo XML: {e}")
        return None

def formatar_data(data_iso: str) -> str:
    """
    Formata uma data ISO 8601 para o formato dd/MM/aaaa
    
    Args:
        data_iso: Data no formato ISO 8601 (AAAA-MM-DDThh:mm:ssXXX)
        
    Returns:
        Data formatada como dd/MM/aaaa
    """
    try:
        # Trata o caso onde a data pode conter timezone ou outros formatos
        data_iso = data_iso.split('T')[0]  # Pega apenas a parte da data
        data_obj = datetime.strptime(data_iso, '%Y-%m-%d')
        return data_obj.strftime('%d/%m/%Y')
    except Exception as e:
        print(f"Erro ao formatar data: {e}")
        return data_iso  # Retorna a data original em caso de erro

def extrair_dados_xml(caminho_xml: Union[str, Path]) -> Tuple[List[Dict], Optional[str]]:
    """
    Extrai os dados relevantes do XML para uma lista de dicionários
    
    Args:
        caminho_xml: Caminho para o arquivo XML
        
    Returns:
        tuple: (dados, data_emissao) - Lista de dicionários com os dados e a data de emissão formatada
    """
    dados_xml = ler_arquivo_xml(caminho_xml)
    if not dados_xml:
        return [], None
    
    dados_nfe = dados_xml["nfeProc"]["NFe"]
    
    # Dados comuns para todos os itens
    nome_fornecedor = dados_nfe["infNFe"]["emit"]["xNome"]
    numero_nota = dados_nfe["infNFe"]["ide"]["nNF"]
    data_emissao_iso = dados_nfe["infNFe"]["ide"]["dhEmi"]
    data_emissao = formatar_data(data_emissao_iso)
    
    # Pegando os itens da nota fiscal
    itens = dados_nfe["infNFe"]["det"]
    
    # Verificando se é apenas um item ou uma lista de itens
    if isinstance(itens, dict):
        itens = [itens]  # Transformando em lista para uniformizar o tratamento
    
    # Lista para armazenar os dados de cada item
    dados_planilha = []
    
    # Iterando sobre cada item
    for item in itens:
        descricao_produto = item["prod"]["xProd"]
        valor_item = item["prod"]["vProd"]
        
        # Adiciona os dados do item à lista
        dados_planilha.append({
            "Data de Emissão": data_emissao,
            "Nome do Fornecedor": nome_fornecedor,
            "Número da Nota": numero_nota,
            "Descrição do Produto": descricao_produto,
            "Valor do Item": valor_item,
        })
    
    return dados_planilha, data_emissao

def obter_nome_mes(data_formatada: str) -> Optional[str]:
    """
    Retorna o nome do mês a partir de uma data no formato dd/MM/aaaa
    
    Args:
        data_formatada: Data no formato dd/MM/aaaa
        
    Returns:
        Nome do mês por extenso ou None em caso de erro
    """
    try:
        data_obj = datetime.strptime(data_formatada, '%d/%m/%Y')
        meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        nome_mes = meses[data_obj.month - 1]
        return nome_mes
    except Exception as e:
        print(f"Erro ao obter nome do mês: {e}")
        return None

# Exemplo de uso
if __name__ == "__main__":
    # Altere o caminho para o seu arquivo XML
    caminho_xml = ROOT_DIR / "35250107131690000167550010000301901011214752.xml"
    
    # Extrai os dados do XML
    dados_planilha, data_emissao = extrair_dados_xml(caminho_xml)
    
    # Exibe os dados extraídos
    if dados_planilha:
        print("Dados extraídos do arquivo XML:")
        for dado in dados_planilha:
            print(dado)
        
        # Exibe o nome do mês da data de emissão
        nome_mes = obter_nome_mes(data_emissao)
        print("Nome do mês de emissão:", nome_mes)
