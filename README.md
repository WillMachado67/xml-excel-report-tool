# Processador de Notas Fiscais XML

Sistema para processamento de arquivos XML de notas fiscais eletrônicas (NF-e) e exportação para planilhas Excel organizadas por mês.

## Funcionalidades

- **Processamento individual**: Processe um único arquivo XML de NF-e
- **Processamento em lote**: Processe todos os arquivos XML em uma pasta
- **Organização automática**: Planilhas são separadas por mês de emissão
- **Verificação de duplicatas**: Evita inserir o mesmo produto duas vezes
- **Interface gráfica intuitiva**: Fácil de usar mesmo para iniciantes

## Requisitos

- Python 3.6 ou superior
- Bibliotecas:
  - `pandas`: Para manipulação de dados e exportação para Excel
  - `xmltodict`: Para conversão de XML para dicionários Python
  - `tkinter`: Para a interface gráfica (geralmente vem com a instalação do Python)

## Instalação

1. Certifique-se de ter o Python instalado em seu sistema
2. Clone ou baixe este repositório
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

ou usando Poetry:

```bash
poetry install
```

## Como usar

### Execução da interface gráfica

Execute o arquivo `gui.py`:

```bash
python gui.py
```

### Processamento de um único arquivo

1. Na aba "Arquivo Único", clique no botão "Selecionar"
2. Escolha o arquivo XML da NF-e
3. Clique em "Processar Arquivo"
4. Uma planilha Excel será gerada na pasta "planilhas"

### Processamento em lote

1. Na aba "Processamento em Lote", clique no botão "Selecionar"
2. Escolha a pasta que contém os arquivos XML da NF-e
3. Clique em "Processar Pasta"
4. As planilhas serão geradas/atualizadas na pasta "planilhas"

## Estrutura do projeto

```
relatorio_xml/
├── config/              # Configurações do sistema
│   ├── __init__.py
│   └── config.py        # Gerenciamento das configurações
├── gui/                 # Interface gráfica do usuário
│   ├── __init__.py
│   ├── actions.py       # Ações e callbacks dos elementos da interface
│   └── layout.py        # Layout e criação dos elementos visuais
├── excel_export.py      # Exportação para Excel
├── gui.py               # Ponto de entrada da interface gráfica
├── pyproject.toml       # Configurações do projeto (Poetry)
└── xml_parser.py        # Processamento e extração de dados dos XMLs
```

## Configurações

O sistema mantém um arquivo de configuração `config.json` com as seguintes opções:

- `output_directory`: Pasta onde as planilhas Excel serão salvas
- `verificar_duplicatas`: Se verdadeiro, evita duplicação de itens nas planilhas

## Formato das planilhas geradas

As planilhas Excel geradas contêm as seguintes colunas:

- **Data de Emissão**: Data em que a NF-e foi emitida (formato DD/MM/AAAA)
- **Nome do Fornecedor**: Nome da empresa emitente da nota fiscal
- **Número da Nota**: Número da NF-e
- **Descrição do Produto**: Descrição do produto/serviço
- **Valor do Item**: Valor individual do item

## Contribuições

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.
