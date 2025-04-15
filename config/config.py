import json
import os
from pathlib import Path


class Config:
    """Gerenciador centralizado de configurações do sistema"""
    
    def __init__(self):
        """Inicializa a configuração com valores padrão e carrega do arquivo"""
        # Diretórios base
        self.ROOT_DIR = Path(__file__).parent.resolve()
        self.CONFIG_FILE = self.ROOT_DIR / "config.json"
        
        # Configurações padrão
        self.DEFAULT_CONFIG = {
            "output_directory": str(self.ROOT_DIR / "planilhas"),
            "verificar_duplicatas": True
        }
        
        # Carrega as configurações do arquivo ou usa padrões
        self._config = self._load_config()
    
    def _load_config(self):
        """Carrega as configurações do arquivo config.json"""
        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Cria o arquivo de configuração com valores padrão
                self._save_config(self.DEFAULT_CONFIG)
                return self.DEFAULT_CONFIG
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            return self.DEFAULT_CONFIG
    
    def _save_config(self, config_data):
        """Salva as configurações no arquivo config.json"""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
    
    @property
    def output_directory(self):
        """Diretório para salvar os arquivos Excel gerados"""
        return Path(self._config["output_directory"])
    
    @property
    def verificar_duplicatas(self):
        """Se devem ser verificadas entradas duplicadas nas planilhas"""
        return self._config.get("verificar_duplicatas", True)
    
    def save(self):
        """Salva as configurações atuais no arquivo"""
        self._save_config(self._config)

# Instância global de configuração
config = Config()

# Funções de compatibilidade com o código existente
def load_config():
    """Função de compatibilidade - Retorna o dicionário de configurações"""
    return {
        "output_directory": str(config.output_directory),
        "verificar_duplicatas": config.verificar_duplicatas
    }

def save_config(config_data):
    """Função de compatibilidade - Salva o dicionário de configurações"""
    for key, value in config_data.items():
        config._config[key] = value
    config.save()