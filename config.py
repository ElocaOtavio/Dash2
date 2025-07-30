"""
Módulo de configuração para o Dashboard Eloca
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Configurações da aplicação"""
    
    # Configurações da API Eloca
    ELOCA_URL = os.getenv("ELOCA_URL", "")
    DESKMANAGER_TOKEN = os.getenv("DESKMANAGER_TOKEN", "")
    
    # Configurações do App
    APP_TITLE = os.getenv("APP_TITLE", "Dashboard Eloca - Gestão de Vendas")
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hora em segundos
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    # Headers para requisições
    HEADERS = {
        "DeskManager": DESKMANAGER_TOKEN,
        "User-Agent": "Eloca-Dashboard/1.0"
    }
    
    # Configurações das abas
    ABAS_PLANILHA = [
        "Metas Individuais",
        "Resultados área 1", 
        "Resultados área 2",
        "Grafico-Individual_1",
        "Grafico-Individual_2"
    ]
    
    @classmethod
    def validate_config(cls):
        """Valida se as configurações essenciais estão definidas"""
        if not cls.ELOCA_URL:
            raise ValueError("ELOCA_URL não está definida")
        if not cls.DESKMANAGER_TOKEN:
            raise ValueError("DESKMANAGER_TOKEN não está definido")
        return True

