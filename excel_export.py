import os
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd

from config.config import config
from xml_parser import extrair_dados_xml, obter_nome_mes

# Define o diretório de saída
OUTPUT_DIR = config.output_directory

def gerar_planilha(caminho_xml: Union[str, Path]) -> Optional[str]:
    """
    Gera uma planilha Excel com os dados do XML
    
    Args:
        caminho_xml: Caminho para o arquivo XML
        
    Returns:
        Caminho da planilha gerada ou None em caso de erro
    """
    try:
        dados, data_emissao = extrair_dados_xml(caminho_xml)
        
        if not dados:
            print(f"Não foi possível extrair dados do XML: {caminho_xml}")
            return None
        
        # Obtém o nome do mês para o nome do arquivo
        nome_mes = obter_nome_mes(data_emissao)
        
        # Cria um DataFrame com os dados
        df = pd.DataFrame(dados)
        
        # Define o caminho do arquivo Excel
        caminho_excel = OUTPUT_DIR / f"{nome_mes}.xlsx"
        
        # Garante que o diretório de saída exista
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Verifica se o arquivo já existe para adicionar dados ou criar um novo
        if os.path.exists(caminho_excel):
            try:
                df_existente = pd.read_excel(caminho_excel)
                
                # Verificação de duplicatas (condicional conforme configuração)
                if config.verificar_duplicatas:
                    df_final = adicionar_sem_duplicatas(df, df_existente)
                else:
                    # Apenas concatena os dados
                    df_final = pd.concat([df_existente, df], ignore_index=True)
                    
            except Exception as e:
                print(f"Erro ao ler arquivo existente: {e}")
                df_final = df
        else:
            df_final = df
        
        # Salva o DataFrame no arquivo Excel
        df_final.to_excel(caminho_excel, index=False)
        print(f"Planilha gerada com sucesso: {caminho_excel}")
        return str(caminho_excel)
    
    except Exception as e:
        print(f"Erro ao gerar planilha: {str(e)}")
        return None

def adicionar_sem_duplicatas(df_novo: pd.DataFrame, df_existente: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona novos dados sem duplicatas ao DataFrame existente
    
    Args:
        df_novo: DataFrame com os novos dados
        df_existente: DataFrame com os dados existentes
        
    Returns:
        DataFrame combinado sem duplicatas
    """
    # Assumindo que a combinação de Número da Nota e Descrição do Produto é única
    chaves_existentes = set()
    for _, row in df_existente.iterrows():
        chaves_existentes.add((row['Número da Nota'], row['Descrição do Produto']))
    
    # Filtra os novos dados para excluir duplicatas
    novos_dados = []
    for _, row in df_novo.iterrows():
        chave = (row['Número da Nota'], row['Descrição do Produto'])
        if chave not in chaves_existentes:
            novos_dados.append(row)
    
    if not novos_dados:
        print("Todos os dados já existem na planilha. Nenhuma atualização necessária.")
        return df_existente
    
    df_novos = pd.DataFrame(novos_dados)
    return pd.concat([df_existente, df_novos], ignore_index=True)

def processar_multiplos_xmls(pasta_xmls: Optional[Union[str, Path]] = None) -> List[str]:
    """
    Processa múltiplos arquivos XML em uma pasta
    
    Args:
        pasta_xmls: Caminho para a pasta com arquivos XML.
                    Se não fornecido, usa a pasta configurada.
    
    Returns:
        Lista com os caminhos das planilhas geradas
    """
    
    pasta_xmls = Path(pasta_xmls)
    
    # Lista todos os arquivos XML na pasta
    arquivos_xml = list(pasta_xmls.glob('*.xml'))
    planilhas_geradas = []
    
    if not arquivos_xml:
        print(f"Nenhum arquivo XML encontrado em {pasta_xmls}")
        return planilhas_geradas
    
    print(f"Encontrados {len(arquivos_xml)} arquivos XML")
    for arquivo in arquivos_xml:
        print(f"Processando {arquivo.name}...")
        caminho_planilha = gerar_planilha(arquivo)
        if caminho_planilha:
            print(f"Dados de {arquivo.name} adicionados a {caminho_planilha}")
            planilhas_geradas.append(caminho_planilha)
    
    return planilhas_geradas

if __name__ == "__main__":
    # Exemplo: processar um único arquivo XML
    caminho_xml = Path(config.ROOT_DIR) / "35250107131690000167550010000301901011214752.xml"
    gerar_planilha(caminho_xml)
    
    # Exemplo: processar todos os XMLs da pasta
    # processar_multiplos_xmls()